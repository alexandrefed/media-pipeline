"""
Import the vibe coding manual chunks to the database.
"""

import asyncio
import json
from src.database.connection import get_database

async def import_vibe_coding_chunks():
    """Import Bootoshi's vibe coding manual chunks."""
    db = get_database()
    await db.initialize()
    
    # Load chunks from file
    chunks_file = 'processed/manual_chunks/manual_chunks_vibe_coding_combo_Nvm9hv38z2o.json'
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    source_id = 12  # From the source we just added
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
                'OpenAI': ['openai', 'open ai', 'deep research', 'o3'],
                'Claude Code': ['claude code', 'clawed code'],
                'Claude': ['claude', 'anthropic'],
                'Cursor': ['cursor', 'curser'],
                'Assembly AI': ['assembly ai', 'assemblyai'],
                '11 Labs': ['11 labs', 'eleven labs'],
                'Open Router': ['open router', 'openrouter'],
                'Context7': ['context7', 'context 7'],
                'MCP': ['mcp', 'model context protocol'],
                'React': ['react'],
                'Next.js': ['next.js', 'nextjs'],
                'TypeScript': ['typescript'],
                'NPM': ['npm'],
                'GitHub': ['github'],
                'XML': ['xml'],
                'JSON': ['json'],
                'Repo Prompt': ['repo prompt'],
                'Raycast': ['raycast'],
                'Discord': ['discord'],
                'Agency42': ['agency42', 'agency 42'],
                'Gemini': ['gemini'],
                'Vibe Coding': ['vibe coding', 'vibe code']
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
    
    # Update source status
    async with db.get_connection() as conn:
        await conn.execute("""
            UPDATE ai_kb.sources 
            SET processing_status = 'completed',
                quality_score = 0.9
            WHERE id = $1
        """, source_id)
    
    await db.close()
    return imported

async def main():
    imported = await import_vibe_coding_chunks()
    print(f"✅ Successfully imported {imported} chunks for Bootoshi's vibe coding video")

if __name__ == "__main__":
    asyncio.run(main())