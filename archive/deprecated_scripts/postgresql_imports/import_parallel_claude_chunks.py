#!/usr/bin/env python3
"""Import IndyDevDan's Parallel Claude Code manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_parallel_claude_chunks():
    """Import Parallel Claude Code manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_parallel_claude_f8RnRuaxee8.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 23  # From the database insertion
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
                
                # Parallel Claude specific tools and concepts
                tool_checks = {
                    'Claude Code': 'Claude Code',
                    'Claude 4': 'Claude 4',
                    'Opus 4': 'Opus 4',
                    'Sonnet 4': 'Sonnet 4',
                    'git worktree': 'git worktrees',
                    'git worktrees': 'git worktrees',
                    'parallel agentic': 'parallel agentic coding',
                    'multiple agents': 'multiple agents',
                    'ThoughtBench': 'ThoughtBench',
                    'Beni': 'Beni codebase',
                    '.claude/commands': '.claude/commands',
                    'slash commands': 'slash commands',
                    '/simple-init-parallel': '/simple-init-parallel',
                    '/exe-parallel': '/exe-parallel',
                    'ADW': 'AI Developer Workflows',
                    'ADWs': 'AI Developer Workflows',
                    'Principled AI Coding': 'Principled AI Coding',
                    'non-deterministic': 'non-deterministic LLMs',
                    'great planning is great prompting': 'great planning is great prompting',
                    'long-running': 'long-running agentic workflows',
                    'multiple futures': 'multiple futures',
                    'merge the best': 'merge the best',
                    'best of n': 'best of n possibilities',
                    'UI revamp': 'UI revamp',
                    'vite config': 'vite config',
                    'bun': 'bun',
                    'Cursor': 'Cursor IDE',
                    'auto-edit mode': 'auto-edit mode',
                    'tool calls': 'tool calls',
                    'Opus tokens': 'Opus tokens',
                    'git merge': 'git merge',
                    'git branch': 'git branch',
                    'git status': 'git status',
                    'git diff': 'git diff',
                    'gcm': 'git commit shortcut',
                    'git push': 'git push',
                    '3x compute': '3x compute',
                    'hedge against model failures': 'hedge against model failures',
                    'end-state ambiguous': 'end-state ambiguous tasks',
                    'clear plan': 'clear plan requirement',
                    'spec': 'specification',
                    'AI drafting': 'AI drafting',
                    'terminal-like style': 'terminal UI style',
                    'overlay setup': 'overlay UI setup',
                    '630 lines changed': '630 lines changed agentically',
                    'three essential directories': 'three essential directories for agentic coding'
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
                    0.95  # High quality for parallel agentic coding tutorial
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Parallel Claude Code video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_parallel_claude_chunks())