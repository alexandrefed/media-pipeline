"""
Add the Cursor CodeRabbit video as a new source in the database.
"""

import asyncio
from src.database.connection import get_database

async def add_cursor_coderabbit_source():
    """Add AI LABS Cursor CodeRabbit video as a new source."""
    db = get_database()
    await db.initialize()
    
    async with db.get_connection() as conn:
        # Check if source already exists
        existing = await conn.fetchrow(
            "SELECT id FROM ai_kb.sources WHERE url = $1",
            "https://www.youtube.com/watch?app=desktop&v=LXk8nWwOPuY&t=123s"
        )
        
        if existing:
            print(f"✅ Source already exists with ID: {existing['id']}")
            return existing['id']
        
        # Insert new source
        source_id = await conn.fetchval("""
            INSERT INTO ai_kb.sources (
                url, title, channel_name, duration_seconds,
                description, processing_status, quality_score, ingestion_date
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
            RETURNING id
        """,
            "https://www.youtube.com/watch?app=desktop&v=LXk8nWwOPuY&t=123s",
            "How to Use Cursor in the Smartest Way Possible",
            "AI LABS", 
            615,
            "Learn how to streamline your workflow with this Cursor AI tutorial that shows real-time code reviews using CodeRabbit. This guide covers everything from setting up the AI code editor to resolving comm...",
            "processing",
            0.0
        )
        
        print(f"✅ Added new source with ID: {source_id}")
        return source_id
    
    await db.close()

async def main():
    source_id = await add_cursor_coderabbit_source()
    print(f"Source ID: {source_id}")

if __name__ == "__main__":
    asyncio.run(main())