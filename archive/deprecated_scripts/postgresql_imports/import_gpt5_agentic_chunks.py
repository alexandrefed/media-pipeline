#!/usr/bin/env python3
"""Import IndyDevDan's GPT-5 Agentic Coding manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_gpt5_agentic_chunks():
    """Import GPT-5 Agentic Coding manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_gpt5_agentic_tcZ3W8QYirQ.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 43  # From the database insertion
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
                
                # GPT-5 Agentic Coding specific tools and concepts
                tool_checks = {
                    'GPT-5': ['gpt-5', 'gpt5'],
                    'GPT OSS': ['gpt oss', 'gpt open-source', 'gpt open source'],
                    'Opus 4.1': ['opus 4.1', 'opus 41'],
                    'Opus 4': ['opus 4', 'opus'],
                    'Sonnet 4': ['sonnet 4', 'claude 4 sonnet'],
                    'Haiku': ['haiku', 'claude 3 haiku'],
                    'Claude Code': ['claude code', 'clawed code'],
                    'Claude': ['claude', 'anthropic'],
                    'nano agent': ['nano agent', 'nano agents'],
                    'MCP server': ['mcp server', 'mcp servers', 'model context protocol'],
                    'OpenAI Agent SDK': ['openai agent sdk', 'agent sdk'],
                    'multi-model evaluation': ['multi-model evaluation', 'multi model evaluation'],
                    'on-device models': ['on-device', 'on device', 'local models'],
                    'M4 Max': ['m4 max', '128gb'],
                    'agentic architecture': ['agentic architecture', 'agent architecture'],
                    'tool chains': ['tool chains', 'tool chaining', 'tool calls'],
                    'higher order prompt': ['higher order prompt', 'hop'],
                    'lower order prompt': ['lower order prompt', 'lop'],
                    'LLM as judge': ['llm as judge', 'llm as a judge'],
                    'performance speed cost': ['performance speed cost', 'performance, speed, and cost'],
                    'fair playing field': ['fair playing field', 'even playing field'],
                    'sub-agents': ['sub-agents', 'sub agents', 'subagents'],
                    'primitives': ['primitive', 'primitives', 'engineering primitive'],
                    'benchmarks': ['benchmark', 'benchmarks', 'benchmark regurgitation'],
                    'The big three': ['context, model, and prompt', 'context model prompt'],
                    'Principled AI Coding': ['principled ai coding', 'principled ai'],
                    'agentic engineering': ['agentic engineering', 'agentic coding'],
                    'nano': ['gpt-5 nano', 'gpt5 nano'],
                    'mini': ['gpt-5 mini', 'gpt5 mini'],
                    '120 billion': ['120 billion', '120b'],
                    '20 billion': ['20 billion', '20b'],
                    'Ollama': ['ollama'],
                    'compute scaling': ['scale your compute', 'scaling compute'],
                    'trade-offs': ['trade-off', 'tradeoffs', 'trade off'],
                    'context window': ['context window', 'context windows'],
                    'embeddings': ['embedding', 'embeddings', '384-dim'],
                    'prompt orchestration': ['prompt orchestration', 'prompt engineering'],
                    'atomized compute': ['atomized compute', 'atomize compute'],
                    'breakthrough week': ['breakthrough week'],
                    'S-tier performance': ['s-tier', 's tier'],
                    'instruction following': ['instruction following'],
                    'file operations': ['file operations', 'read write files'],
                    'JSON structure': ['json structure', 'json format'],
                    'directory listing': ['directory listing', 'list directory']
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
                chunk_id = await conn.fetchval('''
                    INSERT INTO ai_kb.chunks (
                        source_id, content, cleaned_content, embedding,
                        start_time, end_time, chunk_index, mentioned_tools,
                        quality_score, tokens_count
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    RETURNING id
                ''',
                    source_id,
                    chunk['text'],
                    chunk['text'],  # Already cleaned
                    embedding,
                    chunk['start_time'],
                    chunk['end_time'],
                    chunk['chunk_index'],
                    mentioned_tools,
                    0.9,  # High quality score for manual chunks
                    chunk['token_count']
                )
                
                imported += 1
                print(f"✅ Imported chunk {chunk['chunk_index']}: {chunk['chapter_title']} (ID: {chunk_id})")
        
        print(f"📊 Imported {imported} manual chunks for source {source_id}")
        
        # Update source status
        async with db.get_connection() as conn:
            await conn.execute('''
                UPDATE ai_kb.sources 
                SET processing_status = 'completed',
                    quality_score = 0.9,
                    processed_at = NOW()
                WHERE id = $1
            ''', source_id)
        
        print(f"🎉 Successfully completed import of '{data['title']}'")
        
        # Print statistics
        stats = data.get('statistics', {})
        if stats:
            print(f"📊 Total chunks: {stats.get('total_chunks', 0)}")
            print(f"📊 Total tokens: {stats.get('total_tokens', 0)}")
            print(f"📊 Average tokens per chunk: {stats.get('average_tokens_per_chunk', 0)}")
    
    except Exception as e:
        print(f"❌ Error importing chunks: {e}")
        raise
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_gpt5_agentic_chunks())