#!/usr/bin/env python3
"""Add IndyDevDan's Parallel Claude Code video as a new source."""

import asyncio
from datetime import datetime
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def add_parallel_claude_source():
    """Add the Parallel Claude Code video as a new source."""
    db = get_database()
    await db.initialize()
    
    try:
        # Check if source already exists
        async with db.get_connection() as conn:
            existing = await conn.fetchrow(
                "SELECT id FROM ai_kb.sources WHERE url = $1",
                'https://www.youtube.com/watch?v=f8RnRuaxee8'
            )
            
            if existing:
                print(f"⚠️  Source already exists with ID: {existing['id']}")
                return existing['id']
        
        # Add the video as a new source
        source_data = {
            'channel_name': 'IndyDevDan',
            'title': 'Claude 4 ADVANCED AI Coding: How I PARALLELIZE Claude Code with Git Worktrees',
            'url': 'https://www.youtube.com/watch?v=f8RnRuaxee8',
            'duration_seconds': 1698,
            'description': 'Look, MOST developers have NO IDEA how to truly unlock Claude 4\'s INSANE power... They\'re leaving MASSIVE productivity gains on the table! IndyDevDan just dropped the DIRTIEST agentic coding trick th...',
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
            
        print(f"✅ Added Parallel Claude Code video as source ID: {source_id}")
        return source_id
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(add_parallel_claude_source())