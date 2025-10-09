#!/usr/bin/env python3
"""Add IndyDevDan's Infinite Agentic Coding GLITCH video as a new source."""

import asyncio
from datetime import datetime
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def add_infinite_agentic_source():
    """Add the Infinite Agentic Coding GLITCH video as a new source."""
    db = get_database()
    await db.initialize()
    
    try:
        # Check if source already exists
        async with db.get_connection() as conn:
            existing = await conn.fetchrow(
                "SELECT id FROM ai_kb.sources WHERE url = $1",
                'https://www.youtube.com/watch?v=9ipM_vDwflI'
            )
            
            if existing:
                print(f"⚠️  Source already exists with ID: {existing['id']}")
                return existing['id']
        
        # Add the video as a new source
        source_data = {
            'channel_name': 'IndyDevDan',
            'title': 'I just BROKE Claude Code: Infinite Agentic Coding GLITCH (Don\'t try this at work)',
            'url': 'https://www.youtube.com/watch?v=9ipM_vDwflI',
            'duration_seconds': 1060,
            'description': 'Engineers, I just ran an Infinite Agenic Loop in Claude Code. Seriously, don\'t try this at work. This Infinite Agentic Loop will break Claude Code by churning through ALL OF YOUR OPUS TOKENS.',
            'published_date': datetime(2024, 12, 30),  # Approximate date
            'processing_status': 'manual_enhancement',
            'quality_score': 0.9,
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
            
        print(f"✅ Added Infinite Agentic Coding GLITCH video as source ID: {source_id}")
        return source_id
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_infinite_agentic_source())