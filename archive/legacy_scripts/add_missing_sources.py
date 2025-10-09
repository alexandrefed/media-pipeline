#!/usr/bin/env python3
"""
Add missing video sources to the database before importing chunks.
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from src.database.connection import DatabaseConnection, get_database


# Map chunk files to video metadata
VIDEO_METADATA = {
    "manual_chunks_LEMLntjfihA.json": {
        "url": "https://www.youtube.com/watch?v=LEMLntjfihA",
        "title": "AI Automation Video - LEMLntjfihA",  # Will be updated from chunks
        "channel_name": "Unknown Channel",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_ai_engineering_2025_4SnvMieJiuw.json": {
        "url": "https://www.youtube.com/watch?v=4SnvMieJiuw",
        "title": "AI Engineering 2025 PLAN: Max out AI COMPUTE for o1 Preview, Realtime API, and AI Assistants",
        "channel_name": "AI Engineering Channel",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_ai_labs_n8n_mcp_xf2i6Acs1mI.json": {
        "url": "https://www.youtube.com/watch?v=xf2i6Acs1mI",
        "title": "AI Labs n8n MCP Integration",
        "channel_name": "AI Labs",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_ai_labs_superclaude_6Rg5M69bMgQ.json": {
        "url": "https://www.youtube.com/watch?v=6Rg5M69bMgQ",
        "title": "AI Labs SuperClaude",
        "channel_name": "AI Labs",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_claude_engineering_forever_6fCqj4xFCZI.json": {
        "url": "https://www.youtube.com/watch?v=6fCqj4xFCZI",
        "title": "Claude Engineering Forever",
        "channel_name": "Claude Engineering",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_liam_ottley_9_tools_Tw9HButMNu8.json": {
        "url": "https://www.youtube.com/watch?v=Tw9HButMNu8",
        "title": "9 AI Automation Tools That Print Money",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_liam_ottley_comprehensive_5TxSqvPbnWw.json": {
        "url": "https://www.youtube.com/watch?v=5TxSqvPbnWw",
        "title": "AI Automation Agency Comprehensive Guide",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_liam_ottley_entrepreneur_rOUs76wtv60.json": {
        "url": "https://www.youtube.com/watch?v=rOUs76wtv60",
        "title": "From Developer to AI Entrepreneur",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_nick_saraev_comprehensive_L4Qbx8OM9l4.json": {
        "url": "https://www.youtube.com/watch?v=L4Qbx8OM9l4",
        "title": "$1,000,000 AI Automation & Agents Advice for 5 Hours Straight",
        "channel_name": "Nick Saraev",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_sean_kochel_claude_features_eIUYSC6SilA.json": {
        "url": "https://www.youtube.com/watch?v=eIUYSC6SilA",
        "title": "Claude Features Deep Dive",
        "channel_name": "Sean Kochel",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_voice_claude_LvkZuY7rJOM.json": {
        "url": "https://www.youtube.com/watch?v=LvkZuY7rJOM",
        "title": "Voice Claude Integration",
        "channel_name": "Voice AI Channel",
        "published_date": "2025-01-01T00:00:00Z"
    },
    "manual_chunks_openmemory.json": {
        "url": "https://www.youtube.com/watch?v=UNKNOWN",
        "title": "OpenMemory System Overview",
        "channel_name": "AI Memory Channel",
        "published_date": "2025-01-01T00:00:00Z"
    }
}


async def get_existing_videos(db: DatabaseConnection):
    """Get list of existing video URLs to avoid duplicates."""
    async with db.get_connection() as conn:
        rows = await conn.fetch("SELECT url, id, title FROM ai_kb.sources")
        return {row['url']: {'id': row['id'], 'title': row['title']} for row in rows}


async def extract_metadata_from_chunks(chunk_file: str):
    """Extract additional metadata from chunk file if available."""
    chunk_path = Path(f"processed/manual_chunks/{chunk_file}")
    if chunk_path.exists():
        with open(chunk_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Try to extract metadata from the chunks
            if 'metadata' in data:
                return data['metadata']
            
            # Calculate total duration from chunks
            if 'chunks' in data and len(data['chunks']) > 0:
                last_chunk = max(data['chunks'], key=lambda x: x.get('end_time', 0))
                duration = int(last_chunk.get('end_time', 0))
                return {'duration_seconds': duration}
    
    return {}


async def add_missing_sources(db: DatabaseConnection):
    """Add missing video sources to database."""
    existing_videos = await get_existing_videos(db)
    added_count = 0
    
    print("🔍 Checking for missing video sources...")
    print(f"📊 Currently {len(existing_videos)} videos in database")
    
    for chunk_file, metadata in VIDEO_METADATA.items():
        url = metadata['url']
        
        # Skip if already exists
        if url in existing_videos:
            print(f"✓ Already exists: {metadata['title'][:60]}...")
            continue
        
        # Extract additional metadata from chunks
        chunk_metadata = await extract_metadata_from_chunks(chunk_file)
        
        # Prepare source data
        source_data = {
            'url': url,
            'title': metadata['title'],
            'channel_name': metadata['channel_name'],
            'channel_id': '',  # Will be updated later
            'published_date': metadata['published_date'],
            'duration_seconds': chunk_metadata.get('duration_seconds', 0),
            'view_count': 0,
            'like_count': 0,
            'description': '',
            'thumbnail_url': '',
            'quality_score': 0.85,
            'technical_level': 'intermediate',
            'content_type': 'tutorial',
            'transcript_available': True,
            'processing_status': 'pending'
        }
        
        async with db.get_connection() as conn:
            source_id = await conn.fetchval("""
                INSERT INTO ai_kb.sources (
                    url, title, channel_name, channel_id, published_date,
                    duration_seconds, view_count, like_count, description,
                    thumbnail_url, quality_score, technical_level, content_type,
                    transcript_available, processing_status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                RETURNING id
            """, 
                source_data['url'],
                source_data['title'],
                source_data['channel_name'],
                source_data['channel_id'],
                source_data['published_date'],
                source_data['duration_seconds'],
                source_data['view_count'],
                source_data['like_count'],
                source_data['description'],
                source_data['thumbnail_url'],
                source_data['quality_score'],
                source_data['technical_level'],
                source_data['content_type'],
                source_data['transcript_available'],
                source_data['processing_status']
            )
            
            print(f"✅ Added source {source_id}: {source_data['title'][:60]}...")
            added_count += 1
    
    return added_count


async def main():
    """Main function to add missing sources."""
    db = get_database()
    await db.initialize()
    
    try:
        added = await add_missing_sources(db)
        
        print(f"\n📊 Summary:")
        print(f"   Added {added} new video sources")
        
        # Show final count
        async with db.get_connection() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM ai_kb.sources")
            print(f"   Total sources in database: {total}")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())