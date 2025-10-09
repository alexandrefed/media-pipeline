#!/usr/bin/env python3
"""Import IndyDevDan's Infinite Agentic Coding GLITCH manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_infinite_agentic_chunks():
    """Import Infinite Agentic Coding GLITCH manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_infinite_agentic_9ipM_vDwflI.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 22  # From the previous step
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
                
                # Infinite Agentic Coding specific tools and concepts
                tool_checks = {
                    'Claude Code': 'Claude Code',
                    'infinite agentic loop': 'infinite agentic loop',
                    'infinite prompt': 'infinite prompt',
                    'sub-agents': 'sub-agents',
                    'parallel agents': 'parallel agents',
                    'Opus': 'Opus model',
                    'custom slash command': 'custom slash commands',
                    'slash infinite': '/infinite command',
                    'spec': 'spec/PRD',
                    'PRD': 'Product Requirements Document',
                    'two-prompt system': 'two-prompt system',
                    'prompts as first class citizens': 'prompts as first class citizens',
                    'git work trees': 'git work trees',
                    'context window': 'context window limits',
                    'UI generation': 'UI generation',
                    'self-improving': 'self-improving agentic workflow',
                    'reinforcement learning': 'reinforcement learning',
                    'Principled AI Coding': 'Principled AI Coding',
                    'great planning is great prompting': 'great planning is great prompting',
                    'scale your compute': 'scale your compute',
                    'compute equals success': 'compute equals success',
                    'Claude 4 series': 'Claude 4 series',
                    'multiple solutions': 'multiple potential solutions',
                    'information dense keyword': 'information dense keyword',
                    'agentic coding': 'agentic coding',
                    'Q3 launch': 'Q3 launch',
                    'infinite.md': 'infinite.md prompt',
                    'source_infinite': 'source_infinite directory',
                    'neural implant registry': 'neural implant registry UI',
                    'adaptive flow': 'adaptive flow UI',
                    'liquid metal': 'liquid metal UI theme'
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
                    0.9  # High quality for infinite agentic coding pattern
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Infinite Agentic Coding GLITCH video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_infinite_agentic_chunks())