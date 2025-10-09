#!/usr/bin/env python3
"""Import IndyDevDan's AutoGen Multi-Agent Postgres manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_autogen_chunks():
    """Import AutoGen Multi-Agent Postgres manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_autogen_JjVvYDPVrAQ.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 19  # From the previous step
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
                
                # AutoGen and multi-agent specific tools and concepts
                tool_checks = {
                    'AutoGen': 'AutoGen',
                    'multi-agent': 'multi-agent framework',
                    'Microsoft': 'Microsoft',
                    'Postgres': 'PostgreSQL',
                    'OpenAI': 'OpenAI',
                    'GPT-4': 'GPT-4',
                    'LLMs': 'Large Language Models',
                    'AI tools': 'AI tools',
                    'Aider': 'Aider',
                    'TablePlus': 'TablePlus',
                    'poetry': 'poetry',
                    'pyautogen': 'pyautogen',
                    'function map': 'function mapping',
                    'terminate message': 'terminate message',
                    'group chat': 'group chat',
                    'user proxy agent': 'user proxy agent',
                    'data engineer': 'data engineer agent',
                    'senior analyst': 'senior analyst agent',
                    'product manager': 'product manager agent',
                    'commander': 'commander agent',
                    'writer': 'writer agent',
                    'safeguard': 'safeguard agent',
                    'SQL': 'SQL',
                    'Python': 'Python',
                    'prompt engineering': 'prompt engineering',
                    'prompt orchestration': 'prompt orchestration',
                    'agent orchestration': 'agent orchestration',
                    'agentic frameworks': 'agentic frameworks',
                    'agentic software': 'agentic software',
                    'Gmail': 'Gmail example',
                    'Unix philosophy': 'Unix philosophy',
                    'FAANG': 'FAANG companies',
                    'single prompt': 'single prompt limitation',
                    'config_list_from_models': 'config_list_from_models',
                    'use_cache': 'use_cache flag'
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
                    0.9  # High quality for AutoGen multi-agent tutorial
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for AutoGen Multi-Agent Postgres video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_autogen_chunks())