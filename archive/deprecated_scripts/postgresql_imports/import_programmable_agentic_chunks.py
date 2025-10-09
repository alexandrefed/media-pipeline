#!/usr/bin/env python3
"""Import IndyDevDan's Programmable Agentic Coding manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_programmable_agentic_chunks():
    """Import Programmable Agentic Coding manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_programmable_agentic_2TIXl2rlA6Q.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 18  # From the previous step
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
                
                # Programmable agentic coding specific tools and concepts
                tool_checks = {
                    'Claude Code': 'Claude Code',
                    'claude -p': 'claude -p command',
                    'programmable': 'programmable agentic coding',
                    'Aider': 'Aider',
                    'aider-message': 'aider-message',
                    'Cursor': 'Cursor',
                    'Windsurf': 'Windsurf',
                    'AI coding': 'AI coding',
                    'agentic coding': 'agentic coding',
                    'MCP servers': 'MCP servers',
                    'MCP': 'Model Context Protocol',
                    'bash tool': 'bash tool',
                    'edit tool': 'edit tool',
                    'write tool': 'write tool',
                    'glob': 'glob tool',
                    'grep': 'grep tool',
                    'ls': 'ls tool',
                    'read': 'read tool',
                    'task': 'task tool',
                    'UV': 'uv package manager',
                    'Python': 'Python',
                    'TypeScript': 'TypeScript',
                    'todo.ts': 'TypeScript file',
                    'hello.js': 'JavaScript file',
                    'git': 'git',
                    'Notion': 'Notion',
                    'Anthropic': 'Anthropic',
                    'OpenAI': 'OpenAI',
                    'Principal AI Coding': 'Principal AI Coding course',
                    'Sonnet': 'Claude 3.7 Sonnet',
                    'tool belt': 'tool belt concept',
                    'living software': 'living software',
                    'infinite programmability': 'infinite programmability',
                    'scaling compute': 'scaling compute',
                    'DevOps': 'DevOps',
                    'arbitrary tool calling': 'arbitrary tool calling'
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
                    0.95  # Very high quality for programmable agentic tutorial
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Programmable Agentic Coding video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_programmable_agentic_chunks())