"""
Import manually created chunks to the AI Knowledge Base database.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from src.database.connection import get_database, get_sources_table, get_chunks_table


async def import_chunks_from_json(json_file: str):
    """Import chunks from JSON file to database."""
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📁 Loading chunks from: {json_file}")
    # Get channel from first chunk if available
    channel_name = data.get('video_channel') or (data['chunks'][0].get('video_channel') if data['chunks'] else 'Unknown')
    
    print(f"🎬 Video: {data['video_title']}")
    print(f"📺 Channel: {channel_name}")
    print(f"📊 Chunks: {data['chunk_count']}")
    print("="*70)
    
    # Initialize database
    db = get_database()
    await db.initialize()
    
    sources_table = get_sources_table()
    chunks_table = get_chunks_table()
    
    try:
        # First, check if source already exists
        source = await sources_table.get_source_by_url(data['video_url'])
        
        if source:
            print(f"✅ Found existing source: {source['title']}")
            source_id = source['id']
            
            # Delete existing chunks for this source
            async with db.get_connection() as conn:
                await conn.execute("DELETE FROM chunks WHERE source_id = $1", source_id)
                print(f"🗑️  Deleted existing chunks for source {source_id}")
        else:
            # Create new source record
            print("📝 Creating new source record...")
            
            # Extract video ID from URL
            video_id = data['video_id']
            
            source_data = {
                'url': data['video_url'],
                'title': data['video_title'],
                'channel_name': channel_name,
                'channel_id': '',
                'published_date': datetime.now(),
                'duration_seconds': data['chunks'][0].get('video_duration', 0) if data['chunks'] else 0,
                'view_count': 0,
                'like_count': None,
                'description': f"Processed with {data.get('processing_method', 'manual')} chunking",
                'thumbnail_url': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
                'quality_score': 0.9,  # Manual chunks are high quality (0-1 scale)
                'technical_level': 'intermediate',
                'content_type': 'tutorial',
                'transcript_available': True,
                'processing_status': 'completed'
            }
            
            source_id = await sources_table.insert_source(source_data)
            print(f"✅ Created source with ID: {source_id}")
        
        # Import chunks
        print(f"\n📦 Importing {len(data['chunks'])} chunks...")
        
        chunk_ids = []
        for i, chunk in enumerate(data['chunks']):
            chunk_data = {
                'source_id': source_id,
                'content': chunk['text'],
                'cleaned_content': chunk['text'],
                'start_time': chunk.get('start_time', 0),
                'end_time': chunk.get('end_time', 0),
                'chunk_index': chunk.get('chunk_index', i),
                'mentioned_tools': chunk.get('topics', []),  # Use topics as tools for now
                'mentioned_prices': [],
                'quality_score': 0.9 if chunk.get('importance') == 'high' else 0.8,
                'context_before': chunk.get('context', ''),
                'context_after': ''
            }
            
            chunk_id = await chunks_table.insert_chunk(chunk_data)
            chunk_ids.append(chunk_id)
            
            # Progress indicator
            if (i + 1) % 5 == 0 or i == len(data['chunks']) - 1:
                print(f"   ⏳ Imported {i + 1}/{len(data['chunks'])} chunks...")
        
        print(f"\n✅ Successfully imported {len(chunk_ids)} chunks!")
        print(f"🆔 Chunk IDs: {chunk_ids[0]} - {chunk_ids[-1]}")
        
        # Update source processing status
        async with db.get_connection() as conn:
            await conn.execute("""
                UPDATE sources 
                SET processing_status = 'completed'
                WHERE id = $1
            """, source_id)
        
        print(f"📊 Updated source {source_id} status to completed")
        
        return {
            'source_id': source_id,
            'chunk_ids': chunk_ids,
            'chunk_count': len(chunk_ids)
        }
        
    except Exception as e:
        print(f"❌ Error importing chunks: {e}")
        raise
    finally:
        await db.close()


async def verify_import(source_id: int, expected_count: int):
    """Verify the chunks were imported correctly."""
    
    db = get_database()
    await db.initialize()
    
    try:
        async with db.get_connection() as conn:
            # Count chunks
            chunk_count = await conn.fetchval(
                "SELECT COUNT(*) FROM chunks WHERE source_id = $1", source_id
            )
            
            # Get sample chunk
            sample = await conn.fetchrow("""
                SELECT content, start_time, end_time, quality_score
                FROM chunks 
                WHERE source_id = $1 
                ORDER BY chunk_index 
                LIMIT 1
            """, source_id)
            
            print(f"\n🔍 Verification:")
            print(f"   Expected chunks: {expected_count}")
            print(f"   Actual chunks: {chunk_count}")
            print(f"   Match: {'✅' if chunk_count == expected_count else '❌'}")
            
            if sample:
                print(f"   Sample chunk: {sample['content'][:100]}...")
                print(f"   Timespan: {sample['start_time']}s - {sample['end_time']}s")
                print(f"   Quality: {sample['quality_score']}/10")
            
            return chunk_count == expected_count
            
    finally:
        await db.close()


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python import_chunks.py <json_file>")
        print("Example: python import_chunks.py manual_chunks_vibe_code_arWg7gYVD_0.json")
        return
    
    json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f"❌ File not found: {json_file}")
        return
    
    # Import chunks
    result = asyncio.run(import_chunks_from_json(json_file))
    
    # Verify import
    success = asyncio.run(verify_import(result['source_id'], result['chunk_count']))
    
    print("\n" + "="*70)
    if success:
        print("🎉 Import completed successfully!")
        print(f"📊 Source ID: {result['source_id']}")
        print(f"📦 Chunks imported: {result['chunk_count']}")
    else:
        print("⚠️  Import completed with issues - verification failed")
    
    print("\n🔍 You can now query the knowledge base:")
    print(f"   uv run python main.py query 'vibe code productivity'")


if __name__ == "__main__":
    main()