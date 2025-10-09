"""
Import the Cursor CodeRabbit manual chunks to the database.
"""

import asyncio
import json
from src.database.connection import get_database

async def import_cursor_coderabbit_chunks():
    """Import AI LABS Cursor CodeRabbit manual chunks."""
    db = get_database()
    await db.initialize()
    
    # Load chunks from file
    chunks_file = 'processed/manual_chunks/manual_chunks_cursor_coderabbit_LXk8nWwOPuY.json'
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    source_id = 13  # From the source we just added
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
                'Cursor': ['cursor', 'cursor ai'],
                'CodeRabbit': ['coderabbit', 'code rabbit'],
                'VS Code': ['vs code', 'vscode'],
                'Windsurf': ['windsurf'],
                'GitHub': ['github'],
                'Git': ['git init', 'git add', 'git commit'],
                'Next.js': ['next.js', 'nextjs'],
                'FastAPI': ['fastapi', 'fast api'],
                'Shadcn': ['shadcn', 'shaden'],
                'Gemini': ['gemini 2.5 pro', 'gemini'],
                'Discord': ['discord'],
                'AI Agent': ['ai agent', 'ai models'],
                'Extensions': ['extensions', 'extension'],
                'Pull Requests': ['pull requests', 'commits'],
                'Security': ['security', 'vulnerabilities'],
                'Authentication': ['authentication', 'sign in'],
                'E-commerce': ['e-commerce', 'admin panel'],
                'Implementation': ['implementation plan', 'phase'],
                'Review': ['review process', 'suggestions']
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
    imported = await import_cursor_coderabbit_chunks()
    print(f"✅ Successfully imported {imported} chunks for AI LABS Cursor CodeRabbit video")

if __name__ == "__main__":
    asyncio.run(main())