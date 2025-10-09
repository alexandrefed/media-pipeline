#!/usr/bin/env python3
"""Import IndyDevDan's AI Engineering 2025 PLAN manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_ai_engineering_2025_chunks():
    """Import AI Engineering 2025 PLAN manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_ai_engineering_2025_4SnvMieJiuw.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 21  # From the previous step
        imported = 0
        
        async with db.get_connection() as conn:
            # First, check for existing chunks
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = $1",
                source_id
            )
            
            if count > 0:
                # Delete existing chunks
                await conn.execute(
                    "DELETE FROM ai_kb.chunks WHERE source_id = $1",
                    source_id
                )
                print(f"🗑️  Deleted {count} existing chunks")
            
            # Import new chunks
            for chunk in chunks:
                # Extract mentioned tools
                mentioned_tools = []
                content_lower = chunk['text'].lower()
                
                # AI Engineering 2025 specific tools and concepts
                tool_checks = {
                    'ADA': 'ADA personal AI assistant',
                    'real-time API': 'real-time API',
                    'o1': 'o1 reasoning model',
                    'Sonnet 3.5': 'Sonnet 3.5',
                    'structured outputs': 'structured outputs',
                    'ChatGPT': 'ChatGPT',
                    'Claude': 'Claude',
                    'Gemini': 'Gemini',
                    'Cursor': 'Cursor',
                    'Aider': 'Aider',
                    'Continue': 'Continue',
                    'Zed': 'Zed',
                    'AI agents': 'AI agents',
                    'AI assistant': 'AI assistant',
                    'orchestration layer': 'orchestration layer',
                    'LLM': 'Large Language Models',
                    'prompt': 'prompt engineering',
                    'AGI': 'AGI',
                    'agentic': 'agentic software',
                    'knowledge work': 'knowledge work',
                    'SQL': 'SQL',
                    'Python': 'Python',
                    'bar chart': 'data visualization',
                    'CSV': 'CSV files',
                    'markdown': 'markdown documentation',
                    'meta prompting': 'meta prompting',
                    'two-way prompt': 'two-way prompt',
                    'AI coding course': 'AI coding course',
                    'North Star': 'North Star vision',
                    '2x': '2x productivity',
                    '5x': '5x productivity',
                    '10x': '10x productivity',
                    '100x': '100x productivity',
                    'ingestion': 'data ingestion',
                    'synthesis': 'data synthesis',
                    'Anthropic': 'Anthropic'
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
                    0.9  # High quality for AI Engineering 2025 vision content
                )
                imported += 1
                
                print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk['chapter_title'][:60]}...")
        
        # Update source status
        async with db.get_connection() as conn:
            await conn.execute("""
                UPDATE ai_kb.sources 
                SET processing_status = 'completed',
                    quality_score = 0.9
                WHERE id = $1
            """, source_id)
        
        print(f"\n📊 Successfully imported {imported} manual chunks for AI Engineering 2025 PLAN video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_ai_engineering_2025_chunks())