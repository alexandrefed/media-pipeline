#!/usr/bin/env python3
"""Import IndyDevDan's Codex vs Claude Code manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_codex_claude_chunks():
    """Import Codex vs Claude Code manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_codex_claude_y-_xknNOapo.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 25  # From the database insertion
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
                
                # Codex vs Claude Code specific tools and concepts
                tool_checks = {
                    'Codex': 'OpenAI Codex',
                    'Claude Code': 'Claude Code',
                    'ChatGPT': 'ChatGPT',
                    'Devon': 'Devon',
                    'Replit': 'Replit',
                    'Cursor': 'Cursor IDE',
                    'VS Code': 'VS Code',
                    'Windsurf': 'Windsurf',
                    'v0': 'v0',
                    'terminal': 'terminal coding',
                    'web app': 'web applications',
                    'desktop app': 'desktop applications',
                    'AI coding spectrum': 'AI coding spectrum',
                    'control vs ease': 'control vs ease of use',
                    'primitive': 'engineering primitive',
                    'do the simple thing first': 'do the simple thing first',
                    'KISS principle': 'KISS principle',
                    'Aider': 'Aider',
                    'Clyde': 'Clyde (Anthropic internal)',
                    'Boris': 'Boris (Claude Code creator)',
                    'Cat': 'Cat (Claude Code PM)',
                    'Paul': 'Paul (Aider creator)',
                    '$6 per day': '$6 per day cost',
                    'ROI': 'ROI vs cost',
                    '80%': '80% AI-generated code',
                    'ADW': 'AI Developer Workflows',
                    'agentic workflows': 'agentic workflows',
                    'linting': 'semantic linting',
                    'code review': 'AI code review',
                    'parallel': 'parallel execution',
                    'parallelism': 'parallelism',
                    'context window': 'context window',
                    'compact': 'compacting context',
                    '200k': '200k context limit',
                    '500k': '500k context prediction',
                    'scale your compute': 'scale your compute',
                    'north star': 'north star',
                    'living software': 'living software',
                    'background tasks': 'background tasks',
                    'great planning': 'great planning is great prompting',
                    'prototype': 'rapid prototyping',
                    'spec-first': 'spec-first approach',
                    'PRD': 'PRD/design doc',
                    'multiple versions': 'multiple versions approach',
                    'engineers using AI': 'engineers using AI',
                    'AI replacing engineers': 'AI not replacing engineers',
                    'review process': 'human review process',
                    'taste and judgment': 'taste and judgment',
                    'IDK': 'IDK keyword',
                    'sub agent': 'sub agents',
                    'effective context': 'effective context window'
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
                    0.95  # High quality for comparison tutorial
                )
                imported += 1
                
                print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk['chapter_title'][:60]}...")
        
        # Update source status
        async with db.get_connection() as conn:
            await conn.execute("""
                UPDATE ai_kb.sources 
                SET processing_status = 'completed',
                    quality_score = 0.95
                WHERE id = $1
            """, source_id)
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Codex vs Claude Code video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_codex_claude_chunks())