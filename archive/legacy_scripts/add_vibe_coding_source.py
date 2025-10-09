"""
Add the vibe coding video as a new source in the database.
"""

import asyncio
from src.database.connection import get_database

async def add_vibe_coding_source():
    """Add Bootoshi's vibe coding video as a new source."""
    db = get_database()
    await db.initialize()
    
    async with db.get_connection() as conn:
        # Check if source already exists (using url column)
        existing = await conn.fetchrow(
            "SELECT id FROM ai_kb.sources WHERE url = $1",
            "https://www.youtube.com/watch?v=Nvm9hv38z2o"
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
            "https://www.youtube.com/watch?v=Nvm9hv38z2o",
            "THE 100x VIBE CODING COMBO (Workflow Tutorial)",
            "Bootoshi", 
            1790,
            "btw this combo DOES work with Gemini 2.5 Pro (replaces o3)- which you can use for free in the AI studio",
            "processing",
            0.0
        )
        
        print(f"✅ Added new source with ID: {source_id}")
        return source_id
    
    await db.close()

async def main():
    source_id = await add_vibe_coding_source()
    print(f"Source ID: {source_id}")

if __name__ == "__main__":
    asyncio.run(main())