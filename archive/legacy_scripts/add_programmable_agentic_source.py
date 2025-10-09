#!/usr/bin/env python3
"""Add IndyDevDan's Programmable Agentic Coding video as a new source."""

import asyncio
from datetime import datetime
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def add_programmable_agentic_source():
    """Add the Programmable Agentic Coding video as a new source."""
    db = get_database()
    await db.initialize()
    
    try:
        # Check if source already exists
        async with db.get_connection() as conn:
            existing = await conn.fetchrow(
                "SELECT id FROM ai_kb.sources WHERE url = $1",
                'https://www.youtube.com/watch?v=2TIXl2rlA6Q'
            )
            
            if existing:
                print(f"⚠️  Source already exists with ID: {existing['id']}")
                return existing['id']
        
        # Add the video as a new source
        source_data = {
            'channel_name': 'IndyDevDan',
            'title': 'AI Coding is NOT ENOUGH: Claude Code\'s NEXT LEVEL Agentic Coding FEATURE',
            'url': 'https://www.youtube.com/watch?v=2TIXl2rlA6Q',
            'duration_seconds': 1575,
            'description': 'Look, AI coding is DEAD weight IF you\'re still stuck in single-prompt mode. Claude Code just unlocked PROGRAMMABLE agentic coding and the gap is widening fast.',
            'published_date': datetime(2025, 1, 13),  # Approximate date
            'processing_status': 'manual_enhancement',
            'quality_score': 0.95,
            'technical_level': 'advanced',
            'content_type': 'tutorial'
        }
        
        # Add the source using direct INSERT
        async with db.get_connection() as conn:
            source_id = await conn.fetchval("""
                INSERT INTO ai_kb.sources (
                    url, title, channel_name, published_date,
                    duration_seconds, description,
                    quality_score, technical_level, content_type,
                    processing_status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id
            """, 
                source_data['url'],
                source_data['title'],
                source_data['channel_name'],
                source_data['published_date'],
                source_data['duration_seconds'],
                source_data['description'],
                source_data['quality_score'],
                source_data['technical_level'],
                source_data['content_type'],
                source_data['processing_status']
            )
            
        print(f"✅ Added Programmable Agentic Coding video as source ID: {source_id}")
        return source_id
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_programmable_agentic_source())