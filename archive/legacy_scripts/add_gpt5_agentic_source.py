#!/usr/bin/env python3
"""Add GPT-5 Agentic Coding video source to database."""

import asyncio
import sys
sys.path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database

async def add_gpt5_agentic_source():
    """Add the GPT-5 Agentic Coding video source."""
    db = get_database()
    await db.initialize()
    
    async with db.get_connection() as conn:
        # Check if source already exists
        existing = await conn.fetchrow(
            'SELECT id FROM ai_kb.sources WHERE url = $1',
            'https://www.youtube.com/watch?v=tcZ3W8QYirQ'
        )
        
        if existing:
            print(f'✅ Source already exists with ID: {existing["id"]}')
            return existing['id']
        
        # Insert new source
        source_id = await conn.fetchval('''
            INSERT INTO ai_kb.sources (
                title, url, channel_name, duration_seconds,
                description, processing_status, quality_score, ingestion_date
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
            RETURNING id
        ''',
            'GPT-5 Agentic Coding with Claude Code',
            'https://www.youtube.com/watch?v=tcZ3W8QYirQ',
            'IndyDevDan',
            2274,
            'Did GPT-5 prove there\'s a wall? I don\'t care at all and neither should you. There are more important things to focus on like agentic coding, gpt-5, gpt-oss, opus 4.1, and COMPOSABLE compute.',
            'processing',
            0.0
        )
        
        print(f'✅ Added new source with ID: {source_id}')
        return source_id
    
    await db.close()

if __name__ == "__main__":
    result = asyncio.run(add_gpt5_agentic_source())
    print(f'Source ID: {result}')