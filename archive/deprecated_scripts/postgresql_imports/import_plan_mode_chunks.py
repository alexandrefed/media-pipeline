#!/usr/bin/env python3
"""Import IndyDevDan's Plan Mode manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_plan_mode_chunks():
    """Import Plan Mode manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_plan_mode_7LWl3EbcFTc.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 17  # From the previous step
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
                
                # Plan mode specific tools and concepts
                tool_checks = {
                    'Claude Code': 'Claude Code',
                    'plan mode': 'plan mode',
                    'shift tab': 'plan mode activation',
                    'system prompt': 'system prompt',
                    'Anthropic': 'Anthropic',
                    'context window': 'context window',
                    'sycophancy': 'model bias',
                    'senior engineer': 'senior engineer workflow',
                    'Cursor': 'Cursor',
                    'infinite agentic loop': 'infinite agentic loop',
                    'Opus': 'Claude 4 Opus',
                    'CLAUDE.md': 'CLAUDE.md',
                    'meta-prompting': 'meta-prompting',
                    'spec file': 'spec file',
                    'HTML': 'HTML',
                    'CSS': 'CSS',
                    'JavaScript': 'JavaScript',
                    'ephemeral': 'agent ephemeralness',
                    'think hard': 'reasoning model trigger',
                    'higher order prompts': 'higher order prompts',
                    'prompt engineering': 'prompt engineering',
                    'parallel agents': 'parallel execution',
                    'YOLO mode': 'auto-accept mode',
                    'Principal AI coding': 'Principal AI coding course'
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
                    0.9  # Very high quality for plan mode tutorial
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Plan Mode video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_plan_mode_chunks())