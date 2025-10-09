#!/usr/bin/env python3
"""Import IndyDevDan's MCP Prompts manual chunks."""

import asyncio
import json
from pathlib import Path
from sys import path
path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

from database.connection import get_database


async def import_mcp_prompts_chunks():
    """Import MCP Prompts manual chunks."""
    db = get_database()
    await db.initialize()
    
    try:
        # Load manual chunks
        chunks_file = Path('/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_mcp_prompts_mKEq_YaJjPI.json')
        with open(chunks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        source_id = 3  # From the database check
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
                
                # MCP Prompts specific tools and concepts
                tool_checks = {
                    'MCP servers': 'MCP servers',
                    'MCP server': 'MCP servers',
                    'Claude Code': 'Claude Code',
                    'Claude 4': 'Claude 4',
                    'Sonnet 4': 'Sonnet 4',
                    'Deepseek R1': 'Deepseek R1',
                    'prompts': 'MCP prompts',
                    'tools': 'MCP tools',
                    'resources': 'MCP resources',
                    'tier list': 'tier list hierarchy',
                    'quick data': 'Quick Data MCP server',
                    'JSON': 'JSON data',
                    'CSV': 'CSV data',
                    'Cursor': 'Cursor IDE',
                    'load data set': 'load data set tool',
                    'e-commerce': 'e-commerce dataset',
                    'correlation investigation': 'correlation investigation prompt',
                    'find data sources': 'find data sources prompt',
                    'agentic workflows': 'agentic workflows',
                    'AI developer workflows': 'AI developer workflows',
                    'ADW': 'AI developer workflows',
                    'context, model, prompt': 'context, model, prompt principle',
                    'Principled AI Coding': 'Principled AI Coding',
                    'information dense keyword': 'information dense keyword',
                    'recipes for repeat solutions': 'recipes for repeat solutions',
                    'Gen AI': 'Gen AI',
                    'East Coast': 'regional analysis',
                    'West Coast': 'regional analysis',
                    'Midwest': 'regional analysis',
                    'pie chart': 'data visualization',
                    'satisfaction score': 'correlation analysis',
                    'tenure years': 'correlation analysis',
                    'multi-agent': 'multi-agent'
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
                    0.9  # High quality for MCP prompts tutorial
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
        
        print(f"\n📊 Successfully imported {imported} manual chunks for MCP Prompts video")
        print(f"✅ Updated source status to completed")
        
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(import_mcp_prompts_chunks())