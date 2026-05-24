"""
Database connection and management module for AI Knowledge Base.

This module provides connection handling for PostgreSQL with pgvector support,
using the configuration from AI_KNOWLEDGE_BASE_GUIDE.md.
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any

import asyncpg
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, ConfigDict, Field

# Note: Embeddings now handled server-side by unified-memory API (nomic-embed-text, 768-dim)

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration model. Reads from environment variables."""

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    host: str = os.environ.get("DB_HOST", "85.25.172.47")
    port: int = int(os.environ.get("DB_PORT", "5433"))
    database: str = os.environ.get("DB_NAME", "aidb")
    username: str = os.environ.get("DB_USER", "ai_admin")
    password: str = os.environ.get("DB_PASSWORD", "")
    db_schema: str = Field(default=os.environ.get("DB_SCHEMA", "ai_kb"), alias="schema")
    max_connections: int = 10
    command_timeout: int = 60


class DatabaseConnection:
    """Database connection manager for AI Knowledge Base."""

    def __init__(self, config: DatabaseConfig | None = None):
        """Initialize database connection manager."""
        self.config = config or DatabaseConfig()
        self.pool: asyncpg.Pool | None = None

    @staticmethod
    async def _init_connection(conn):
        """Initialize each connection with custom type codec for vector."""
        # Set search path first
        await conn.execute("SET search_path TO ai_kb, public")

        # Register vector type codec to handle list -> vector conversion
        # Note: pgvector extension is installed in public schema
        await conn.set_type_codec(
            "vector",
            encoder=lambda value: f"[{','.join(str(x) for x in value)}]",
            decoder=lambda value: [float(x) for x in value.strip("[]").split(",")],
            schema="public",  # pgvector is in public schema
            format="text",
        )

    async def initialize(self):
        """Initialize the database connection pool and embedding model."""
        # Create connection pool
        self.pool = await asyncpg.create_pool(
            host=self.config.host,
            port=self.config.port,
            user=self.config.username,
            password=self.config.password,
            database=self.config.database,
            min_size=1,
            max_size=self.config.max_connections,
            command_timeout=self.config.command_timeout,
            server_settings={"search_path": self.config.db_schema},
            init=self._init_connection,
        )

        logger.info("✅ Database connection pool initialized")

    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_connection(self):
        """Get a database connection from the pool."""
        if not self.pool:
            await self.initialize()

        connection = await self.pool.acquire()
        try:
            yield connection
        finally:
            await self.pool.release(connection)

    def get_sync_connection(self):
        """Get a synchronous database connection for non-async operations."""
        return psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.username,
            password=self.config.password,
            database=self.config.database,
            options=f"-c search_path={self.config.db_schema}",
            cursor_factory=RealDictCursor,
        )

    def generate_embedding(self, text: str) -> list[float]:
        """Legacy stub — embeddings now handled by unified-memory API (nomic-embed-text, 768-dim)."""
        raise NotImplementedError(
            "Direct embedding generation removed. Use unified-memory API for embeddings. "
            "See src/storage/unified_memory_client.py"
        )

    async def test_connection(self) -> bool:
        """Test database connection and return success status."""
        try:
            async with self.get_connection() as conn:
                result = await conn.fetchval("SELECT 1")
                if result == 1:
                    logger.info("✅ Database connection test successful")
                    return True
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False

        return False

    async def check_schema_exists(self) -> bool:
        """Check if the ai_kb schema exists."""
        try:
            async with self.get_connection() as conn:
                result = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = $1)",
                    self.config.db_schema,
                )
                return result
        except Exception as e:
            logger.error(f"Error checking schema existence: {e}")
            return False

    async def get_table_info(self) -> dict[str, Any]:
        """Get information about tables in the ai_kb schema."""
        try:
            async with self.get_connection() as conn:
                tables = await conn.fetch(
                    """
                    SELECT table_name,
                           column_name,
                           data_type,
                           is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = $1
                    ORDER BY table_name, ordinal_position
                """,
                    self.config.db_schema,
                )

                # Group by table
                table_info = {}
                for row in tables:
                    table_name = row["table_name"]
                    if table_name not in table_info:
                        table_info[table_name] = []
                    table_info[table_name].append(
                        {
                            "column": row["column_name"],
                            "type": row["data_type"],
                            "nullable": row["is_nullable"] == "YES",
                        }
                    )

                return table_info
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {}


class SourcesTable:
    """Operations for the sources table."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    async def insert_source(self, source_data: dict[str, Any]) -> int:
        """Insert a new source and return its ID."""
        async with self.db.get_connection() as conn:
            source_id = await conn.fetchval(
                """
                INSERT INTO sources (
                    url, title, channel_name, channel_id, published_date,
                    duration_seconds, view_count, like_count, description,
                    thumbnail_url, quality_score, technical_level, content_type,
                    transcript_available, processing_status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                RETURNING id
            """,
                source_data["url"],
                source_data["title"],
                source_data["channel_name"],
                source_data.get("channel_id", ""),
                source_data["published_date"],
                source_data.get("duration_seconds", 0),
                source_data.get("view_count", 0),
                source_data.get("like_count"),
                source_data.get("description", ""),
                source_data.get("thumbnail_url", ""),
                source_data.get("quality_score", 5),
                source_data.get("technical_level", "intermediate"),
                source_data.get("content_type", "tutorial"),
                source_data.get("transcript_available", True),
                source_data.get("processing_status", "pending"),
            )
            return source_id

    async def get_source_by_url(self, url: str) -> dict[str, Any] | None:
        """Get source by URL."""
        async with self.db.get_connection() as conn:
            result = await conn.fetchrow("SELECT * FROM sources WHERE url = $1", url)
            return dict(result) if result else None


class ChunksTable:
    """Operations for the chunks table."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    async def insert_chunk(self, chunk_data: dict[str, Any]) -> int:
        """Insert a new chunk and return its ID."""
        # Generate embedding for the content
        embedding = self.db.generate_embedding(chunk_data["content"])

        async with self.db.get_connection() as conn:
            chunk_id = await conn.fetchval(
                """
                INSERT INTO chunks (
                    source_id, content, cleaned_content, embedding,
                    start_time, end_time, chunk_index, mentioned_tools,
                    mentioned_prices, quality_score, context_before, context_after
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING id
            """,
                chunk_data["source_id"],
                chunk_data["content"],
                chunk_data.get("cleaned_content", chunk_data["content"]),
                embedding,  # Now passing list directly, codec will handle conversion
                chunk_data.get("start_time", 0),
                chunk_data.get("end_time", 0),
                chunk_data.get("chunk_index", 0),
                chunk_data.get("mentioned_tools", []),
                chunk_data.get("mentioned_prices", []),
                chunk_data.get("quality_score", 5),
                chunk_data.get("context_before", ""),
                chunk_data.get("context_after", ""),
            )
            return chunk_id

    async def semantic_search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Perform semantic search on chunks."""
        query_embedding = self.db.generate_embedding(query)

        async with self.db.get_connection() as conn:
            results = await conn.fetch(
                """
                SELECT c.*, s.title, s.channel_name, s.url,
                       c.embedding <-> $1 as similarity
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                ORDER BY c.embedding <-> $1
                LIMIT $2
            """,
                query_embedding,
                limit,
            )

            return [dict(row) for row in results]


# Global database instance
db = DatabaseConnection()


async def init_database():
    """Initialize the global database instance."""
    await db.initialize()


async def close_database():
    """Close the global database instance."""
    await db.close()


def get_database() -> DatabaseConnection:
    """Get the global database instance."""
    return db


# Table operation classes
def get_sources_table() -> SourcesTable:
    """Get sources table operations."""
    return SourcesTable(db)


def get_chunks_table() -> ChunksTable:
    """Get chunks table operations."""
    return ChunksTable(db)


async def main():
    """Test the database connection and operations."""
    print("🔧 Testing AI Knowledge Base Database Connection...")

    # Test basic connection
    success = await db.test_connection()
    if not success:
        print("❌ Database connection failed")
        return

    # Check schema
    schema_exists = await db.check_schema_exists()
    print(f"📊 Schema 'ai_kb' exists: {schema_exists}")

    # Get table info
    table_info = await db.get_table_info()
    print(f"📋 Found {len(table_info)} tables:")
    for table_name, columns in table_info.items():
        print(f"  - {table_name}: {len(columns)} columns")

    await db.close()
    print("✅ Database testing completed")


if __name__ == "__main__":
    asyncio.run(main())
