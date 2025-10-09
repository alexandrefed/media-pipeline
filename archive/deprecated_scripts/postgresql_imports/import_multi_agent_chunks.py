#!/usr/bin/env python3
"""Import IndyDevDan's Multi-Agent Observability manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_multi_agent_chunks():
    """Import Multi-Agent Observability manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_multi_agent_observability_9ijnN985O_c.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 16  # From the previous step
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
                
                # Multi-agent observability specific tools
                tool_checks = {
                    'Claude Code': 'Claude Code',
                    'hooks': 'Claude Code hooks',
                    'multi-agent': 'multi-agent systems',
                    'observability': 'observability',
                    'SQLite': 'SQLite',
                    'websockets': 'websockets',
                    'bun server': 'bun',
                    'Vue.js': 'Vue.js',
                    'Haiku': 'Haiku',
                    'session ID': 'session tracking',
                    'MCP servers': 'MCP servers',
                    'Astral UV': 'Astral UV',
                    'Python': 'Python',
                    'JSON': 'JSON',
                    'HTTP': 'HTTP',
                    'agentic': 'agentic coding',
                    'pre-tool': 'pre-tool use hook',
                    'post tool': 'post tool use hook',
                    'notification': 'notification hook',
                    'stop event': 'stop hook',
                    'sub agent': 'sub agent',
                    'event stream': 'event streaming'
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
                    0.85  # High quality for manual chunks
                )
                imported += 1
                
                print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk['chapter_title'][:60]}...")
        
        # Update source status
        async with db.get_connection() as conn:
            await conn.execute("""
                UPDATE ai_kb.sources 
                SET processing_status = 'completed',
                    quality_score = 0.85
                WHERE id = $1
            """, source_id)
        
        print(f"\n📊 Successfully imported {imported} manual chunks for Multi-Agent Observability video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_multi_agent_chunks())