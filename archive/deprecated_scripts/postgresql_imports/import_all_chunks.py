"""
Import all pending manual chunks using the correct database connection system.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
from src.database.connection import DatabaseConnection, get_database


async def import_manual_chunks(db: DatabaseConnection, source_id: int, chunks_file: str) -> int:
    """Import manual chunks from JSON file."""
    # Load chunks from file
    with open(f'processed/manual_chunks/{chunks_file}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    imported = 0
    
    async with db.get_connection() as conn:
        # First delete any existing chunks for this source
        await conn.execute(
            "DELETE FROM ai_kb.chunks WHERE source_id = $1",
            source_id
        )
        
        for chunk in chunks:
            # Extract mentioned tools from the content
            mentioned_tools = []
            content_lower = chunk['text'].lower()
            
            # Common tools to detect
            tool_checks = {
                'n8n': ['n8n', 'mate and'],
                'Claude Code': ['claude code', 'clawed code'],
                'Claude': ['claude desktop', 'claude 4', 'claude anthropic'],
                'Cursor': ['cursor', 'curser', 'cursor ai'],
                'v0': ['v0', 'zero', 'the zero'],
                'Make.com': ['make.com', 'make dot com'],
                'MCP': ['mcp', 'mcp servers', 'model context protocol'],
                'OpenAI': ['openai', 'open ai'],
                'Deepseek': ['deepseek', 'deep seek'],
                'Sonnet': ['sonnet', 'claude sonnet'],
                'GPT-4': ['gpt-4', 'gpt4'],
                'Windsurf': ['windsurf', 'windsurf ai'],
                'Zapier': ['zapier'],
                'Anthropic': ['anthropic', 'anropic'],
                'Mem0': ['mem0', 'mem zero'],
                'OpenMemory': ['openmemory', 'open memory'],
                'Docker': ['docker'],
                'React': ['react'],
                'Next.js': ['next.js', 'nextjs'],
                'TypeScript': ['typescript'],
                'MERN': ['mern'],
                'JSON': ['json'],
                'CSV': ['csv']
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
                0.9  # High quality score for manual chunks
            )
            imported += 1
            
            print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk.get('chapter_title', 'Chunk')[:50]}...")
    
    print(f"📊 Imported {imported} manual chunks for source {source_id}")
    return imported


async def main():
    """Main import function."""
    print("🔄 Importing all pending manual chunks...")
    
    db = get_database()
    await db.initialize()
    
    # Define all chunks to import
    imports = [
        (7, "manual_chunks_vibe_code_arWg7gYVD_0.json"),
        (8, "manual_chunks_n8n_agents_u2NluvotA80.json"), 
        (9, "manual_chunks_claude_commands.json"),
        (10, "manual_chunks_3_folders.json"),
        (11, "manual_chunks_openmemory_Y2XI2nk44WE.json")
    ]
    
    total_imported = 0
    
    try:
        for source_id, chunks_file in imports:
            print(f"\n📹 Processing source {source_id}: {chunks_file}")
            
            # Get source info
            async with db.get_connection() as conn:
                source = await conn.fetchrow(
                    "SELECT id, title FROM ai_kb.sources WHERE id = $1",
                    source_id
                )
                
                if not source:
                    print(f"❌ Source {source_id} not found in database")
                    continue
                    
                print(f"   Title: {source['title'][:60]}...")
            
            # Import chunks
            imported = await import_manual_chunks(db, source_id, chunks_file)
            total_imported += imported
            
            # Update source status
            async with db.get_connection() as conn:
                await conn.execute("""
                    UPDATE ai_kb.sources 
                    SET processing_status = 'completed',
                        quality_score = 0.9
                    WHERE id = $1
                """, source_id)
        
        print("\n" + "="*70)
        print("✅ ALL IMPORTS COMPLETE!")
        print(f"   Total chunks imported: {total_imported}")
        print(f"   Sources processed: {len(imports)}")
        
        # Verify all imports
        print(f"\n📊 Final verification:")
        async with db.get_connection() as conn:
            for source_id, chunks_file in imports:
                count = await conn.fetchval(
                    "SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = $1",
                    source_id
                )
                print(f"   Source {source_id}: {count} chunks")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())