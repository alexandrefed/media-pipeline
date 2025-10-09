#!/usr/bin/env python3
"""
Import manual chunks for SSbqXzRsC6s video into the PostgreSQL database.
"""

import json
import asyncio
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import sys
import re

# Initialize the embedding model (384 dimensions)
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_tools(text):
    """Extract mentioned tools from chunk text."""
    tools = []
    
    # Tool patterns to search for
    tool_patterns = {
        'n8n': [r'\bn8n\b', r'\bmate and\b'],
        'Claude Code': [r'\bClaude Code\b', r'\bclawed code\b', r'\bcloud code\b'],
        'Claude': [r'\bClaude\b', r'\bClaude Desktop\b', r'\bClaude 4\b'],
        'Cursor': [r'\bCursor\b', r'\bcurser\b', r'\bCursor AI\b'],
        'v0': [r'\bv0\b', r'\bzero\b', r'\bthe zero\b'],
        'Make.com': [r'\bMake\.com\b', r'\bmake dot com\b'],
        'MCP': [r'\bMCP\b', r'\bMCP servers?\b', r'\bModel Context Protocol\b'],
        'OpenAI': [r'\bOpenAI\b', r'\bopen ai\b'],
        'Deepseek': [r'\bDeepseek\b', r'\bdeep seek\b'],
        'Sonnet': [r'\bSonnet\b', r'\bsonnet\b'],
        'GPT-4': [r'\bGPT-4\b', r'\bgpt4\b'],
        'Codex': [r'\bCodex\b'],
        'ChatGPT': [r'\bChatGPT\b', r'\bChat GPT\b'],
        'Anthropic': [r'\bAnthropic\b', r'\banropic\b'],
        'Haiku': [r'\bHaiku\b'],
        'Opus': [r'\bOpus\b'],
        'Aider': [r'\bAider\b'],
        'FastAPI': [r'\bFastAPI\b', r'\bFast API\b']
    }
    
    text_lower = text.lower()
    for tool, patterns in tool_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if tool not in tools:
                    tools.append(tool)
                break
    
    return tools

async def import_chunks():
    """Import chunks for SSbqXzRsC6s video."""
    
    source_id = 42  # The ID we just inserted
    chunk_file = "manual_chunks_SSbqXzRsC6s.json"
    chunks_dir = Path(__file__).parent.parent / "processed" / "manual_chunks"
    file_path = chunks_dir / chunk_file
    
    print(f"Importing {chunk_file} for source ID {source_id}")
    
    # Load chunks
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loading {len(data['chunks'])} chunks from {chunk_file}")
    
    # Connect to database
    conn = psycopg2.connect(
        host="85.25.172.47",
        port=5433,
        database="aidb",
        user="ai_admin",
        password="AIKnowledgeBase2025SecurePassword"
    )
    
    # Register vector type
    register_vector(conn)
    
    cur = conn.cursor()
    cur.execute('SET search_path TO ai_kb, public;')
    
    try:
        # Delete any existing chunks for this source
        cur.execute(
            "DELETE FROM chunks WHERE source_id = %s",
            (source_id,)
        )
        print(f"Deleted existing chunks for source {source_id}")
        
        # Import new chunks
        imported = 0
        for chunk in data['chunks']:
            # Generate embedding
            embedding = model.encode(chunk['text']).tolist()
            
            # Extract mentioned tools
            mentioned_tools = extract_tools(chunk['text'])
            
            # Insert chunk - Fixed the parameter passing
            cur.execute("""
                INSERT INTO chunks (
                    source_id, content, cleaned_content, embedding,
                    start_time, end_time, chunk_index, 
                    mentioned_tools, quality_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                source_id,
                chunk['text'],
                chunk['text'],  # Already cleaned
                embedding,
                chunk['start_time'],
                chunk['end_time'],
                chunk['chunk_index'],
                mentioned_tools,
                0.95  # High quality for manual chunks
            ))
            imported += 1
            
            if imported % 5 == 0:
                print(f"  Imported {imported}/{len(data['chunks'])} chunks...")
        
        conn.commit()
        print(f"Successfully imported {imported} chunks for source {source_id}")
        
        # Verify the import
        cur.execute("""
            SELECT COUNT(*) FROM chunks WHERE source_id = %s
        """, (source_id,))
        
        count = cur.fetchone()[0]
        print(f"Verification: {count} chunks in database for source {source_id}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error importing chunks: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    asyncio.run(import_chunks())