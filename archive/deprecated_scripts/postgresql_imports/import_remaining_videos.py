#!/usr/bin/env python3
"""
Import all remaining videos with manual chunks to complete the database.
This script handles all videos that haven't been imported yet.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import sys
sys.path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD')
from src.database.connection import DatabaseConnection, get_database


# Map chunk files to video metadata
VIDEO_METADATA = {
    "manual_chunks_ai_labs_n8n_mcp_xf2i6Acs1mI.json": {
        "url": "https://www.youtube.com/watch?v=xf2i6Acs1mI",
        "title": "This n8n mcp is INSANE... Let AI Create your Entire Automation",
        "channel_name": "AI LABS",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_ai_labs_superclaude_6Rg5M69bMgQ.json": {
        "url": "https://www.youtube.com/watch?v=6Rg5M69bMgQ",
        "title": "Claude Engineer is INSANE... Upgrade Your Claude Code Workflow",
        "channel_name": "AI LABS",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_liam_ottley_9_tools_Tw9HButMNu8.json": {
        "url": "https://www.youtube.com/watch?v=Tw9HButMNu8",
        "title": "9 AI Tools That Will Separate Winners from Losers in 2025",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_liam_ottley_comprehensive_5TxSqvPbnWw.json": {
        "url": "https://www.youtube.com/watch?v=5TxSqvPbnWw",
        "title": "How to Build & Sell AI Automations: Ultimate Beginner's Guide",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_liam_ottley_entrepreneur_rOUs76wtv60.json": {
        "url": "https://www.youtube.com/watch?v=rOUs76wtv60",
        "title": "How to Learn AI as an Entrepreneur (3 Beginner Paths)",
        "channel_name": "Liam Ottley",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_claude_engineering_forever_6fCqj4xFCZI.json": {
        "url": "https://www.youtube.com/watch?v=6fCqj4xFCZI",
        "title": "How Claude Code CHANGED Engineering Forever (and what's next)",
        "channel_name": "IndyDevDan",
        "published_date": "2025-01-21T00:00:00Z"
    },
    "manual_chunks_voice_claude_LvkZuY7rJOM.json": {
        "url": "https://www.youtube.com/watch?v=LvkZuY7rJOM",
        "title": "Voice to Claude Code: SPEAK to SHIP Agentic Coding AI Assistant",
        "channel_name": "IndyDevDan",
        "published_date": "2025-01-21T00:00:00Z"
    },
    "manual_chunks_sean_kochel_claude_features_eIUYSC6SilA.json": {
        "url": "https://www.youtube.com/watch?v=eIUYSC6SilA",
        "title": "Code 10x Better With These 5 Claude Code Features",
        "channel_name": "Sean Kochel",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_nick_saraev_comprehensive_L4Qbx8OM9l4.json": {
        "url": "https://www.youtube.com/watch?v=L4Qbx8OM9l4",
        "title": "$1,000,000 AI Automation & Agents Advice for 5 Hours Straight",
        "channel_name": "Nick Saraev",
        "published_date": "2025-01-22T00:00:00Z"
    },
    "manual_chunks_LEMLntjfihA.json": {
        "url": "https://www.youtube.com/watch?v=LEMLntjfihA",
        "title": "AI Automation Tutorial",  # Will be updated from chunks
        "channel_name": "Unknown Channel",
        "published_date": "2025-01-18T00:00:00Z"
    },
    "manual_chunks_claude_commands.json": {
        "url": "https://www.youtube.com/watch?v=UNKNOWN_1",
        "title": "Claude Commands Tutorial",
        "channel_name": "Unknown Channel",
        "published_date": "2025-01-19T00:00:00Z"
    },
    "manual_chunks_mcp_prompts_mKEq_YaJjPI.json": {
        "url": "https://www.youtube.com/watch?v=mKEq_YaJjPI",
        "title": "MCP Prompts Tutorial",
        "channel_name": "IndyDevDan",
        "published_date": "2025-01-21T00:00:00Z"
    },
    "manual_chunks_openmemory.json": {
        "url": "https://www.youtube.com/watch?v=UNKNOWN_2",
        "title": "OpenMemory System Overview",
        "channel_name": "AI Memory Channel",
        "published_date": "2025-01-19T00:00:00Z"
    }
}


async def get_existing_videos(db: DatabaseConnection) -> Dict[str, Dict]:
    """Get list of existing video URLs to avoid duplicates."""
    async with db.get_connection() as conn:
        rows = await conn.fetch("SELECT url, id, title FROM ai_kb.sources")
        return {row['url']: {'id': row['id'], 'title': row['title']} for row in rows}


async def extract_metadata_from_chunks(chunk_file: str) -> Dict:
    """Extract additional metadata from chunk file if available."""
    chunk_path = Path(f"processed/manual_chunks/{chunk_file}")
    if chunk_path.exists():
        with open(chunk_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Extract metadata
            metadata = {}
            if 'metadata' in data:
                metadata.update(data['metadata'])
            
            # Get title from chunks if available
            if 'title' in data:
                metadata['title'] = data['title']
            
            # Calculate total duration from chunks
            if 'chunks' in data and len(data['chunks']) > 0:
                last_chunk = max(data['chunks'], key=lambda x: x.get('end_time', 0))
                metadata['duration_seconds'] = int(last_chunk.get('end_time', 0))
            
            # Get total chunks
            metadata['total_chunks'] = data.get('total_chunks', len(data.get('chunks', [])))
            
            return metadata
    
    return {}


async def import_manual_chunks(db: DatabaseConnection, source_id: int, chunks_file: str) -> int:
    """Import manual chunks from JSON file."""
    # Load chunks from file
    with open(f'processed/manual_chunks/{chunks_file}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data.get('chunks', [])
    imported = 0
    
    async with db.get_connection() as conn:
        # First delete any existing chunks for this source
        existing = await conn.fetchval(
            "SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = $1",
            source_id
        )
        
        if existing > 0:
            await conn.execute(
                "DELETE FROM ai_kb.chunks WHERE source_id = $1",
                source_id
            )
            print(f"   🗑️  Deleted {existing} existing chunks")
        
        for chunk in chunks:
            # Extract mentioned tools from the content
            mentioned_tools = []
            content_lower = chunk['text'].lower()
            
            # Common tools to detect
            tool_checks = {
                'n8n': ['n8n', 'mate and'],
                'Claude Code': ['claude code', 'clawed code', 'cloud code'],
                'Claude': ['claude desktop', 'claude 4', 'claude anthropic'],
                'Cursor': ['cursor', 'curser', 'cursor ai'],
                'v0': ['v0', 'zero', 'v zero', 'the zero'],
                'Make.com': ['make.com', 'make dot com'],
                'MCP': ['mcp', 'mcp servers', 'model context protocol'],
                'OpenAI': ['openai', 'open ai', 'chatgpt', 'gpt-4'],
                'Deepseek': ['deepseek', 'deep seek'],
                'Sonnet': ['sonnet', 'claude sonnet'],
                'Windsurf': ['windsurf', 'windsurf ai'],
                'Zapier': ['zapier'],
                'Anthropic': ['anthropic', 'anropic'],
                'Mem0': ['mem0', 'mem zero'],
                'OpenMemory': ['openmemory', 'open memory'],
                'Docker': ['docker'],
                'SuperClaude': ['superclaude', 'super claude'],
                'Firecrawl': ['firecrawl', 'fire crawl'],
                'Puppeteer': ['puppeteer'],
                'Playwright': ['playwright']
            }
            
            for tool_name, patterns in tool_checks.items():
                for pattern in patterns:
                    if pattern in content_lower:
                        if tool_name not in mentioned_tools:
                            mentioned_tools.append(tool_name)
                        break
            
            # Generate embedding
            embedding = db.generate_embedding(chunk['text'])
            
            # Insert chunk
            await conn.execute("""
                INSERT INTO ai_kb.chunks (
                    source_id, content, cleaned_content, embedding,
                    start_time, end_time, chunk_index, mentioned_tools,
                    quality_score, context_before, context_after
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
                source_id,
                chunk['text'],
                chunk['text'],  # Already cleaned
                embedding,
                chunk.get('start_time', 0),
                chunk.get('end_time', 0),
                chunk.get('chunk_index', imported),
                mentioned_tools,
                0.9,  # High quality score for manual chunks
                '',  # context_before
                ''   # context_after
            )
            imported += 1
    
    print(f"   ✅ Imported {imported} chunks")
    return imported


async def main():
    """Main function to import all remaining videos."""
    print("🚀 Starting comprehensive import of remaining videos...")
    
    db = get_database()
    await db.initialize()
    
    try:
        # Get existing videos
        existing_videos = await get_existing_videos(db)
        print(f"📊 Currently {len(existing_videos)} videos in database")
        
        # Track import statistics
        total_sources_added = 0
        total_chunks_imported = 0
        skipped_duplicates = []
        
        # Process each video
        for chunk_file, base_metadata in VIDEO_METADATA.items():
            print(f"\n{'='*70}")
            print(f"📹 Processing: {chunk_file}")
            
            url = base_metadata['url']
            
            # Check if video already exists (handle MCP prompts duplicate)
            if url in existing_videos:
                if url == "https://www.youtube.com/watch?v=mKEq_YaJjPI":
                    # This is the MCP prompts video, already in DB as ID 3
                    print(f"   ⚠️  Video already exists in database (ID: {existing_videos[url]['id']})")
                    skipped_duplicates.append(chunk_file)
                    continue
                else:
                    print(f"   ⚠️  Video already exists: {existing_videos[url]['title'][:50]}...")
                    skipped_duplicates.append(chunk_file)
                    continue
            
            # Extract metadata from chunks
            chunk_metadata = await extract_metadata_from_chunks(chunk_file)
            
            # Update title if found in chunks
            if 'title' in chunk_metadata:
                base_metadata['title'] = chunk_metadata['title']
            
            # Prepare source data
            source_data = {
                'url': url,
                'title': base_metadata['title'],
                'channel_name': base_metadata['channel_name'],
                'channel_id': '',
                'published_date': datetime.fromisoformat(base_metadata['published_date'].replace('Z', '')),
                'duration_seconds': chunk_metadata.get('duration_seconds', 0),
                'view_count': 0,
                'like_count': 0,
                'description': '',
                'thumbnail_url': '',
                'quality_score': 0.9,
                'technical_level': 'intermediate',
                'content_type': 'tutorial',
                'transcript_available': True,
                'processing_status': 'pending'
            }
            
            # Insert source
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
                
                print(f"   ✅ Added source ID {source_id}: {source_data['title'][:50]}...")
                total_sources_added += 1
            
            # Import chunks
            chunks_imported = await import_manual_chunks(db, source_id, chunk_file)
            total_chunks_imported += chunks_imported
            
            # Update source status
            async with db.get_connection() as conn:
                await conn.execute("""
                    UPDATE ai_kb.sources 
                    SET processing_status = 'completed',
                        processed_at = CURRENT_TIMESTAMP
                    WHERE id = $1
                """, source_id)
                print(f"   ✅ Updated status to 'completed'")
        
        # Final summary
        print(f"\n{'='*70}")
        print("✅ IMPORT COMPLETE!")
        print(f"   New sources added: {total_sources_added}")
        print(f"   Total chunks imported: {total_chunks_imported}")
        print(f"   Skipped duplicates: {len(skipped_duplicates)}")
        
        if skipped_duplicates:
            print("\n   Skipped files:")
            for f in skipped_duplicates:
                print(f"   - {f}")
        
        # Verify final counts
        async with db.get_connection() as conn:
            total_sources = await conn.fetchval("SELECT COUNT(*) FROM ai_kb.sources")
            total_chunks = await conn.fetchval("SELECT COUNT(*) FROM ai_kb.chunks")
            
            print(f"\n📊 Final Database Status:")
            print(f"   Total videos: {total_sources}")
            print(f"   Total chunks: {total_chunks}")
            
            # Show recent imports
            recent = await conn.fetch("""
                SELECT id, title, 
                       (SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = s.id) as chunk_count
                FROM ai_kb.sources s
                WHERE processed_at > CURRENT_TIMESTAMP - INTERVAL '1 hour'
                ORDER BY id DESC
                LIMIT 10
            """)
            
            if recent:
                print(f"\n📋 Recently imported videos:")
                for r in recent:
                    print(f"   ID {r['id']:2d}: {r['title'][:50]}... ({r['chunk_count']} chunks)")
        
    except Exception as e:
        print(f"❌ Error during import: {e}")
        raise
    finally:
        await db.close()
        print("\n✅ Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())