#!/usr/bin/env python3
"""Add IndyDevDan's AI Engineering 2025 PLAN video as a new source."""

import asyncio
from datetime import datetime
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def add_ai_engineering_2025_source():
    """Add the AI Engineering 2025 PLAN video as a new source."""
    db = get_database()
    await db.initialize()
    
    try:
        # Check if source already exists
        async with db.get_connection() as conn:
            existing = await conn.fetchrow(
                "SELECT id FROM ai_kb.sources WHERE url = $1",
                'https://www.youtube.com/watch?v=4SnvMieJiuw'
            )
            
            if existing:
                print(f"⚠️  Source already exists with ID: {existing['id']}")
                return existing['id']
        
        # Add the video as a new source
        source_data = {
            'channel_name': 'IndyDevDan',
            'title': 'AI Engineering 2025 PLAN: Max out AI COMPUTE for o1 Preview, Realtime API, and AI Assistants',
            'url': 'https://www.youtube.com/watch?v=4SnvMieJiuw',
            'duration_seconds': 1147,
            'description': 'The plan for 2025 is simple. MAX OUT your AI COMPUTE for Prompts, AI Agents, and AI Assistants!',
            'published_date': datetime(2024, 12, 26),  # Approximate date
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
            
        print(f"✅ Added AI Engineering 2025 PLAN video as source ID: {source_id}")
        return source_id
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_ai_engineering_2025_source())