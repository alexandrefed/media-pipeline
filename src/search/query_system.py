"""
Query system for AI Knowledge Base using pgvector semantic search.

This module provides natural language query capabilities over the knowledge base,
combining vector similarity search with traditional full-text search and entity filtering.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel

from ..database.connection import get_database
from ..processing.entity_correction import EntityCorrector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryType(str, Enum):
    """Types of queries supported."""

    SEMANTIC = "semantic"  # Pure vector similarity
    HYBRID = "hybrid"  # Vector + full-text search
    ENTITY_FOCUSED = "entity_focused"  # Focus on specific tools/entities
    STRATEGIC = "strategic"  # High-level strategy questions


class SearchMode(str, Enum):
    """Search mode for different use cases."""

    PRECISE = "precise"  # Exact matches, high threshold
    BALANCED = "balanced"  # Good balance of precision/recall
    EXPLORATORY = "exploratory"  # Cast wider net, lower threshold


@dataclass
class QueryResult:
    """Single query result with metadata."""

    chunk_id: int
    content: str
    similarity_score: float
    source_title: str
    source_url: str
    channel_name: str
    start_time: float
    end_time: float
    mentioned_tools: list[str]
    quality_score: float
    context_before: str
    context_after: str
    # Additional metadata fields for complete traceability
    published_date: str  # Video publish date (ISO format)
    source_id: int  # Source video ID for full metadata retrieval
    timestamp_url: str  # Direct YouTube link with timestamp


class QueryConfig(BaseModel):
    """Configuration for query execution."""

    query_type: QueryType = QueryType.HYBRID
    search_mode: SearchMode = SearchMode.BALANCED
    max_results: int = 10
    similarity_threshold: float = 0.3
    quality_threshold: float = 0.2  # Normalized 0-1 range
    include_context: bool = True
    entity_boost: float = 1.2
    recency_boost: float = 1.1


class QueryResponse(BaseModel):
    """Complete query response with results and metadata."""

    query: str
    results: list[QueryResult]
    total_found: int
    search_time_ms: float
    detected_entities: list[str]
    query_type: QueryType
    search_strategy: str
    suggestions: list[str]


class AIKnowledgeQuery:
    """Main query system for AI Knowledge Base."""

    def __init__(self, config: QueryConfig | None = None):
        """Initialize the query system."""
        self.config = config or QueryConfig()
        self.db = get_database()
        self.corrector = EntityCorrector()

    async def search(self, query: str, **kwargs) -> QueryResponse:
        """Execute a search query."""
        import time

        start_time = time.time()

        # Override config with any provided kwargs
        config = self.config.copy()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        logger.info(f"🔍 Executing query: {query}")

        # Apply entity correction to query
        corrected_query = self.corrector.correct_text(query)
        detected_entities = [e["corrected"] for e in corrected_query.detected_entities]

        effective_query = corrected_query.corrected_text
        logger.info(f"✅ Corrected query: {effective_query}")

        # Determine optimal search strategy
        search_strategy = self._determine_search_strategy(effective_query, detected_entities)
        logger.info(f"📊 Using search strategy: {search_strategy}")

        # Execute search based on strategy
        results = await self._execute_search(effective_query, search_strategy, config)

        # Post-process results
        processed_results = self._post_process_results(results, detected_entities, config)

        # Generate suggestions
        suggestions = self._generate_suggestions(effective_query, detected_entities, results)

        search_time_ms = (time.time() - start_time) * 1000

        return QueryResponse(
            query=query,
            results=processed_results,
            total_found=len(processed_results),
            search_time_ms=search_time_ms,
            detected_entities=detected_entities,
            query_type=config.query_type,
            search_strategy=search_strategy,
            suggestions=suggestions,
        )

    def _determine_search_strategy(self, query: str, entities: list[str]) -> str:
        """Determine the optimal search strategy based on query characteristics."""
        query_lower = query.lower()

        # Strategic queries
        if any(
            word in query_lower
            for word in [
                "strategy",
                "approach",
                "best practice",
                "recommendation",
                "should i",
                "how to choose",
                "compare",
                "versus",
                "vs",
            ]
        ):
            return "strategic_semantic"

        # Entity-focused queries
        if entities or any(
            word in query_lower
            for word in ["n8n", "make.com", "zapier", "cursor", "claude", "notion"]
        ):
            return "entity_focused_hybrid"

        # Technical implementation queries
        if any(
            word in query_lower
            for word in ["configure", "setup", "install", "code", "api", "webhook"]
        ):
            return "technical_hybrid"

        # Default to balanced hybrid
        return "balanced_hybrid"

    async def _execute_search(
        self, query: str, strategy: str, config: QueryConfig
    ) -> list[dict[str, Any]]:
        """Execute search using the determined strategy."""
        if strategy == "strategic_semantic":
            return await self._strategic_semantic_search(query, config)
        elif strategy == "entity_focused_hybrid":
            return await self._entity_focused_search(query, config)
        elif strategy == "technical_hybrid":
            return await self._technical_hybrid_search(query, config)
        else:
            return await self._balanced_hybrid_search(query, config)

    async def _strategic_semantic_search(
        self, query: str, config: QueryConfig
    ) -> list[dict[str, Any]]:
        """Search optimized for strategic/high-level questions."""
        # Generate query embedding
        query_embedding = self.db.generate_embedding(query)

        async with self.db.get_connection() as conn:
            results = await conn.fetch(
                """
                SELECT c.*, s.id as source_id, s.title, s.channel_name, s.url, s.published_date,
                       c.embedding <-> $1 as similarity,
                       -- Boost high-quality, strategic content
                       (c.quality_score * 0.3 +
                        CASE WHEN c.content ILIKE '%strategy%' OR c.content ILIKE '%approach%' OR c.content ILIKE '%best practice%'
                             THEN 0.2 ELSE 0 END +
                        CASE WHEN s.view_count > 50000 THEN 0.1 ELSE 0 END) as relevance_boost
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                WHERE c.quality_score >= $2
                  AND s.processing_status = 'completed'
                ORDER BY ((c.embedding <-> $1) + (c.quality_score * 0.3 +
                         CASE WHEN c.content ILIKE '%strategy%' OR c.content ILIKE '%approach%' OR c.content ILIKE '%best practice%'
                              THEN 0.2 ELSE 0 END +
                         CASE WHEN s.view_count > 50000 THEN 0.1 ELSE 0 END))
                LIMIT $3
            """,
                query_embedding,
                config.quality_threshold,
                config.max_results,
            )

            return [dict(row) for row in results]

    async def _entity_focused_search(self, query: str, config: QueryConfig) -> list[dict[str, Any]]:
        """Search focused on specific entities/tools."""
        # Generate query embedding
        query_embedding = self.db.generate_embedding(query)

        # Extract entities from query
        entities = [e["corrected"] for e in self.corrector.correct_text(query).detected_entities]

        async with self.db.get_connection() as conn:
            results = await conn.fetch(
                """
                SELECT c.*, s.id as source_id, s.title, s.channel_name, s.url, s.published_date,
                       c.embedding <-> $1 as similarity,
                       -- Boost content that mentions the entities
                       (CASE WHEN c.mentioned_tools && $4 THEN 0.15 ELSE 0 END +
                        c.quality_score * 0.2) as relevance_boost
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                WHERE c.quality_score >= $2
                  AND s.processing_status = 'completed'
                  AND (c.embedding <-> $1 < $3 OR c.mentioned_tools && $4)
                ORDER BY ((c.embedding <-> $1) + (CASE WHEN c.mentioned_tools && $4 THEN 0.15 ELSE 0 END +
                         c.quality_score * 0.2))
                LIMIT $5
            """,
                query_embedding,
                config.quality_threshold,
                config.similarity_threshold,
                entities,
                config.max_results,
            )

            return [dict(row) for row in results]

    async def _technical_hybrid_search(
        self, query: str, config: QueryConfig
    ) -> list[dict[str, Any]]:
        """Hybrid search optimized for technical implementation questions."""
        # Generate query embedding
        query_embedding = self.db.generate_embedding(query)

        # Extract technical keywords
        self._extract_technical_keywords(query)

        async with self.db.get_connection() as conn:
            results = await conn.fetch(
                """
                SELECT c.*, s.id as source_id, s.title, s.channel_name, s.url, s.published_date,
                       c.embedding <-> $1 as similarity,
                       -- Boost technical implementation content
                       (CASE WHEN c.content ILIKE '%configure%' OR c.content ILIKE '%setup%' OR c.content ILIKE '%install%'
                             THEN 0.1 ELSE 0 END +
                        CASE WHEN c.content ILIKE '%code%' OR c.content ILIKE '%api%' OR c.content ILIKE '%webhook%'
                             THEN 0.1 ELSE 0 END +
                        c.quality_score * 0.2) as relevance_boost,
                       -- Full-text search score
                       ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', $4)) as fts_score
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                WHERE c.quality_score >= $2
                  AND s.processing_status = 'completed'
                  AND (c.embedding <-> $1 < $3 OR to_tsvector('english', c.content) @@ plainto_tsquery('english', $4))
                ORDER BY ((c.embedding <-> $1) + (CASE WHEN c.content ILIKE '%configure%' OR c.content ILIKE '%setup%' OR c.content ILIKE '%install%'
                              THEN 0.1 ELSE 0 END +
                         CASE WHEN c.content ILIKE '%code%' OR c.content ILIKE '%api%' OR c.content ILIKE '%webhook%'
                              THEN 0.1 ELSE 0 END +
                         c.quality_score * 0.2) + (ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', $4)) * 0.1))
                LIMIT $5
            """,
                query_embedding,
                config.quality_threshold,
                config.similarity_threshold,
                query,
                config.max_results,
            )

            return [dict(row) for row in results]

    async def _balanced_hybrid_search(
        self, query: str, config: QueryConfig
    ) -> list[dict[str, Any]]:
        """Balanced hybrid search combining vector and full-text search."""
        # Generate query embedding
        query_embedding = self.db.generate_embedding(query)

        async with self.db.get_connection() as conn:
            results = await conn.fetch(
                """
                SELECT c.*, s.id as source_id, s.title, s.channel_name, s.url, s.published_date,
                       c.embedding <-> $1 as similarity,
                       ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', $4)) as fts_score,
                       c.quality_score * 0.1 as quality_boost
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                WHERE c.quality_score >= $2
                  AND s.processing_status = 'completed'
                  AND (c.embedding <-> $1 < $3 OR to_tsvector('english', c.content) @@ plainto_tsquery('english', $4))
                ORDER BY ((c.embedding <-> $1) + (c.quality_score * 0.1) + (ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', $4)) * 0.15))
                LIMIT $5
            """,
                query_embedding,
                config.quality_threshold,
                config.similarity_threshold,
                query,
                config.max_results,
            )

            return [dict(row) for row in results]

    def _extract_technical_keywords(self, query: str) -> list[str]:
        """Extract technical keywords from query."""
        technical_terms = [
            "api",
            "webhook",
            "json",
            "xml",
            "rest",
            "graphql",
            "configure",
            "setup",
            "install",
            "deploy",
            "build",
            "authentication",
            "auth",
            "token",
            "key",
            "secret",
            "database",
            "sql",
            "query",
            "table",
            "schema",
            "workflow",
            "automation",
            "trigger",
            "action",
            "node",
        ]

        query_lower = query.lower()
        found_terms = [term for term in technical_terms if term in query_lower]

        return found_terms

    def _generate_timestamp_url(self, video_url: str, start_time: float) -> str:
        """Generate YouTube URL with timestamp parameter.

        Args:
            video_url: Original YouTube URL
            start_time: Start time in seconds

        Returns:
            YouTube URL with timestamp parameter
        """
        if not video_url or "youtube.com" not in video_url and "youtu.be" not in video_url:
            return video_url

        # Extract video ID from various YouTube URL formats
        video_id = None
        if "youtube.com/watch?v=" in video_url:
            # Standard format: https://youtube.com/watch?v=VIDEO_ID
            video_id = video_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in video_url:
            # Short format: https://youtu.be/VIDEO_ID
            video_id = video_url.split("youtu.be/")[1].split("?")[0]

        if video_id:
            # Convert float seconds to integer
            time_seconds = int(start_time)
            # Return standardized YouTube URL with timestamp
            return f"https://youtube.com/watch?v={video_id}&t={time_seconds}s"

        # If we can't parse the URL, return original with timestamp appended
        separator = "&" if "?" in video_url else "?"
        return f"{video_url}{separator}t={int(start_time)}s"

    def _post_process_results(
        self, results: list[dict[str, Any]], entities: list[str], config: QueryConfig
    ) -> list[QueryResult]:
        """Post-process and format search results."""
        processed_results = []

        for result in results:
            # Apply entity boost
            similarity_score = result.get("similarity", 1.0)
            if entities and any(entity in result.get("mentioned_tools", []) for entity in entities):
                similarity_score *= config.entity_boost

            # Generate timestamp URL for YouTube videos
            timestamp_url = self._generate_timestamp_url(result["url"], result.get("start_time", 0))

            # Format published date to ISO format string
            published_date = ""
            if result.get("published_date"):
                if hasattr(result["published_date"], "isoformat"):
                    published_date = result["published_date"].isoformat()
                else:
                    published_date = str(result["published_date"])

            # Convert to QueryResult with all metadata
            query_result = QueryResult(
                chunk_id=result["id"],
                content=result["content"],
                similarity_score=similarity_score,
                source_title=result["title"],
                source_url=result["url"],
                channel_name=result["channel_name"],
                start_time=result.get("start_time", 0),
                end_time=result.get("end_time", 0),
                mentioned_tools=result.get("mentioned_tools", []),
                quality_score=result.get("quality_score", 5.0),
                context_before=result.get("context_before", "") if config.include_context else "",
                context_after=result.get("context_after", "") if config.include_context else "",
                published_date=published_date,
                source_id=result.get("source_id", 0),
                timestamp_url=timestamp_url,
            )

            processed_results.append(query_result)

        return processed_results

    def _generate_suggestions(
        self, query: str, entities: list[str], results: list[dict[str, Any]]
    ) -> list[str]:
        """Generate query suggestions based on results."""
        suggestions = []

        # Extract common tools from results
        all_tools = set()
        for result in results:
            all_tools.update(result.get("mentioned_tools", []))

        # Generate tool-specific suggestions
        for tool in list(all_tools)[:3]:
            if tool.lower() not in query.lower():
                suggestions.append(f"How to integrate {tool} with other tools?")
                suggestions.append(f"Best practices for {tool} automation")

        # Generate related queries
        if "setup" in query.lower():
            suggestions.append("Configuration best practices")
            suggestions.append("Common setup issues and solutions")

        if any(word in query.lower() for word in ["compare", "vs", "versus"]):
            suggestions.append("Pricing comparison of automation tools")
            suggestions.append("Feature comparison matrix")

        return suggestions[:5]  # Limit to 5 suggestions

    async def get_related_content(self, chunk_id: int, limit: int = 5) -> list[QueryResult]:
        """Get content related to a specific chunk."""
        async with self.db.get_connection() as conn:
            # Get the source chunk
            source_chunk = await conn.fetchrow("SELECT * FROM chunks WHERE id = $1", chunk_id)

            if not source_chunk:
                return []

            # Find similar chunks
            results = await conn.fetch(
                """
                SELECT c.*, s.id as source_id, s.title, s.channel_name, s.url, s.published_date,
                       c.embedding <-> $1 as similarity
                FROM chunks c
                JOIN sources s ON c.source_id = s.id
                WHERE c.id != $2
                  AND s.processing_status = 'completed'
                ORDER BY c.embedding <-> $1
                LIMIT $3
            """,
                source_chunk["embedding"],
                chunk_id,
                limit,
            )

            return self._post_process_results([dict(row) for row in results], [], self.config)

    async def get_video_summary(self, source_id: int) -> dict[str, Any]:
        """Get a summary of a video's content."""
        async with self.db.get_connection() as conn:
            # Get source info
            source = await conn.fetchrow("SELECT * FROM sources WHERE id = $1", source_id)

            if not source:
                return {}

            # Get chunks for this video
            chunks = await conn.fetch(
                """
                SELECT * FROM chunks
                WHERE source_id = $1
                ORDER BY chunk_index
            """,
                source_id,
            )

            # Extract key information
            all_tools = set()
            total_quality = 0

            for chunk in chunks:
                all_tools.update(chunk.get("mentioned_tools", []))
                total_quality += chunk.get("quality_score", 5.0)

            return {
                "title": source["title"],
                "channel_name": source["channel_name"],
                "url": source["url"],
                "duration_seconds": source["duration_seconds"],
                "total_chunks": len(chunks),
                "average_quality": total_quality / len(chunks) if chunks else 0,
                "mentioned_tools": list(all_tools),
                "key_topics": self._extract_key_topics(chunks),
            }

    def _extract_key_topics(self, chunks: list[dict[str, Any]]) -> list[str]:
        """Extract key topics from chunks."""
        # Simple topic extraction based on common patterns
        topics = set()

        for chunk in chunks:
            content = chunk.get("content", "").lower()

            # Look for topic indicators
            if "setup" in content or "configure" in content:
                topics.add("setup_configuration")
            if "integration" in content or "connect" in content:
                topics.add("integration")
            if "automation" in content or "workflow" in content:
                topics.add("automation")
            if "api" in content or "webhook" in content:
                topics.add("api_integration")
            if "database" in content or "data" in content:
                topics.add("data_management")

        return list(topics)


async def main():
    """Test the query system."""
    query_system = AIKnowledgeQuery()

    # Test queries
    test_queries = [
        "How do I set up n8n with a database?",
        "What's the best automation tool for beginners?",
        "Compare n8n vs Make.com for API integrations",
        "How to configure webhooks in automation tools?",
        "Best practices for workflow automation",
    ]

    print("🔍 Testing AI Knowledge Query System")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")

        try:
            response = await query_system.search(query)

            print(f"   ✅ Found {response.total_found} results in {response.search_time_ms:.1f}ms")
            print(f"   📊 Strategy: {response.search_strategy}")
            print(f"   🔧 Detected entities: {response.detected_entities}")

            if response.results:
                top_result = response.results[0]
                print(f"   📄 Top result: {top_result.source_title}")
                print(f"   🎯 Similarity: {top_result.similarity_score:.3f}")
                print(f"   💎 Quality: {top_result.quality_score:.1f}")
                print(f"   🔗 Tools: {top_result.mentioned_tools}")

            if response.suggestions:
                print(f"   💡 Suggestions: {response.suggestions[:2]}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("✅ Query system testing completed")


if __name__ == "__main__":
    asyncio.run(main())
