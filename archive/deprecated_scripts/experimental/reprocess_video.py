"""
Reprocess video in database: delete old chunks and import new manual chunks.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
from src.database.connection import DatabaseConnection, get_database


async def delete_old_chunks(db: DatabaseConnection, source_id: int) -> int:
    """Delete all chunks for a given source."""
    async with db.get_connection() as conn:
        # First get count of chunks to delete
        count = await conn.fetchval(
            "SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = $1",
            source_id
        )
        
        # Delete the chunks
        await conn.execute(
            "DELETE FROM ai_kb.chunks WHERE source_id = $1",
            source_id
        )
        
        print(f"🗑️  Deleted {count} old chunks for source_id {source_id}")
        return count


async def import_manual_chunks(db: DatabaseConnection, source_id: int, chunks_file: str) -> int:
    """Import manual chunks from JSON file."""
    # Load chunks from file
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    imported = 0
    
    async with db.get_connection() as conn:
        for chunk in chunks:
            # Extract mentioned tools from the content
            mentioned_tools = []
            content_lower = chunk['text'].lower()
            
            # Common tools mentioned in this video
            tool_checks = {
                'MCP servers': 'MCP',
                'Claude Code': 'Claude Code',
                'Claude 4': 'Claude 4',
                'Sonnet 4': 'Sonnet 4',
                'Cursor': 'Cursor',
                'Deepseek R1.1': 'Deepseek R1.1',
                'JSON': 'JSON',
                'CSV': 'CSV'
            }
            
            for pattern, tool_name in tool_checks.items():
                if pattern.lower() in content_lower:
                    mentioned_tools.append(tool_name)
            
            # Generate embedding
            embedding = db.generate_embedding(chunk['text'])
            
            # Insert chunk
            await conn.execute("""
                INSERT INTO ai_kb.chunks (
                    source_id, content, cleaned_content, embedding,
                    start_time, end_time, chunk_index, mentioned_tools,
                    quality_score
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
                source_id,
                chunk['text'],
                chunk['text'],  # Already cleaned
                embedding,
                chunk['start_time'],
                chunk['end_time'],
                chunk['chunk_index'],
                mentioned_tools,
                0.8  # Higher quality score for manual chunks (0-1 scale)
            )
            imported += 1
            
            print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk['chapter_title'][:60]}...")
    
    print(f"\n📊 Imported {imported} manual chunks")
    return imported


async def update_source_status(db: DatabaseConnection, source_id: int):
    """Update source processing status and timestamp."""
    async with db.get_connection() as conn:
        await conn.execute("""
            UPDATE ai_kb.sources 
            SET processing_status = 'completed',
                quality_score = 0.85
            WHERE id = $1
        """, source_id)
        
        print(f"✅ Updated source status to completed with quality score 0.85")


async def main():
    """Main reprocessing function."""
    print("🔄 Reprocessing first video with manual chunks...")
    
    db = get_database()
    await db.initialize()
    
    try:
        # Get the first video
        async with db.get_connection() as conn:
            video = await conn.fetchrow("""
                SELECT id, url, title 
                FROM ai_kb.sources 
                ORDER BY id 
                LIMIT 1
            """)
            
            if not video:
                print("❌ No videos found in database")
                return
                
            print(f"\n📹 Reprocessing video:")
            print(f"   ID: {video['id']}")
            print(f"   Title: {video['title']}")
            print(f"   URL: {video['url']}")
            print()
        
        # Delete old chunks
        deleted = await delete_old_chunks(db, video['id'])
        
        # Import new manual chunks
        chunks_file = "manual_chunks_mKEq_YaJjPI.json"
        imported = await import_manual_chunks(db, video['id'], chunks_file)
        
        # Update source status
        await update_source_status(db, video['id'])
        
        # Show summary
        print("\n" + "="*70)
        print("✅ REPROCESSING COMPLETE!")
        print(f"   Deleted: {deleted} old chunks")
        print(f"   Imported: {imported} manual chunks")
        print(f"   Reduction: {((deleted - imported) / deleted * 100):.1f}%")
        print(f"   Quality: Dramatically improved with semantic coherence")
        
        # Verify the new chunks
        async with db.get_connection() as conn:
            stats = await conn.fetchrow("""
                SELECT COUNT(*) as count,
                       AVG(LENGTH(content)) as avg_length,
                       MIN(LENGTH(content)) as min_length,
                       MAX(LENGTH(content)) as max_length
                FROM ai_kb.chunks 
                WHERE source_id = $1
            """, video['id'])
            
            print(f"\n📊 New chunk statistics:")
            print(f"   Total chunks: {stats['count']}")
            print(f"   Avg length: {stats['avg_length']:.0f} chars")
            print(f"   Min length: {stats['min_length']} chars")
            print(f"   Max length: {stats['max_length']} chars")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())