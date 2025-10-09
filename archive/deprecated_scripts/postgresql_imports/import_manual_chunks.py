#!/usr/bin/env python3
"""
Import manual chunks from JSON files into the PostgreSQL database.
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
        'Claude Code': [r'\bClaude Code\b', r'\bclawed code\b'],
        'Claude': [r'\bClaude\b', r'\bClaude Desktop\b', r'\bClaude 4\b'],
        'Cursor': [r'\bCursor\b', r'\bcurser\b', r'\bCursor AI\b'],
        'v0': [r'\bv0\b', r'\bzero\b', r'\bthe zero\b'],
        'Make.com': [r'\bMake\.com\b', r'\bmake dot com\b'],
        'MCP': [r'\bMCP\b', r'\bMCP servers?\b', r'\bModel Context Protocol\b'],
        'OpenAI': [r'\bOpenAI\b', r'\bopen ai\b'],
        'Deepseek': [r'\bDeepseek\b', r'\bdeep seek\b'],
        'Sonnet': [r'\bSonnet\b', r'\bsonnet\b'],
        'GPT-4': [r'\bGPT-4\b', r'\bgpt4\b'],
        'Windsurf': [r'\bWindsurf\b', r'\bWindsurf AI\b'],
        'Zapier': [r'\bZapier\b'],
        'Anthropic': [r'\bAnthropic\b', r'\banropic\b'],
        'Mem0': [r'\bMem0\b', r'\bmem0\b'],
        'OpenMemory': [r'\bOpenMemory\b', r'\bOpen Memory\b'],
        'Docker': [r'\bDocker\b'],
        'React': [r'\bReact\b'],
        'Next.js': [r'\bNext\.js\b', r'\bNextJS\b'],
        'TypeScript': [r'\bTypeScript\b'],
        'MERN': [r'\bMERN\b']
    }
    
    text_lower = text.lower()
    for tool, patterns in tool_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if tool not in tools:
                    tools.append(tool)
                break
    
    return tools

async def import_chunks(source_id: int, chunks_file: str):
    """Import manual chunks from JSON file."""
    
    # Load chunks
    chunks_path = Path(f'processed/manual_chunks/{chunks_file}')
    if not chunks_path.exists():
        print(f"Error: File {chunks_path} not found")
        return
    
    with open(chunks_path, 'r') as f:
        data = json.load(f)
    
    print(f"Loading {len(data['chunks'])} chunks from {chunks_file}")
    
    # Connect to database
    conn = psycopg2.connect(
        host="85.25.172.47",
        port=5433,
        database="aidb",
        user="ai_admin",
        password="AIKnowledgeBase2025SecurePassword"
    )
    
    # Register pgvector type
    register_vector(conn)
    cur = conn.cursor()
    cur.execute('SET search_path TO ai_kb, public;')
    
    try:
        # Delete existing chunks if any
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
            
            # Insert chunk
            cur.execute("""
                INSERT INTO chunks (
                    source_id, content, cleaned_content, embedding,
                    start_time, end_time, chunk_index, 
                    mentioned_tools, quality_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                source_id,
                chunk['text'],
                chunk['text'],  # Already cleaned
                embedding,
                chunk['start_time'],
                chunk['end_time'],
                chunk['chunk_index'],
                mentioned_tools,
                0.9  # High quality for manual chunks
            )
            imported += 1
            
            if imported % 5 == 0:
                print(f"  Imported {imported}/{len(data['chunks'])} chunks...")
        
        conn.commit()
        print(f"Successfully imported {imported} chunks for source {source_id}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error importing chunks: {e}")
        raise
    finally:
        cur.close()
        conn.close()

async def main():
    """Main function to import all pending chunks."""
    
    # Define chunks to import with their source IDs
    imports = [
        (7, "manual_chunks_vibe_code_arWg7gYVD_0.json"),
        (8, "manual_chunks_n8n_agents_u2NluvotA80.json"),
        (9, "manual_chunks_claude_commands.json"),
        (10, "manual_chunks_3_folders.json"),
        (11, "manual_chunks_openmemory_Y2XI2nk44WE.json")
    ]
    
    print("Starting manual chunk imports...")
    print("=" * 50)
    
    for source_id, chunk_file in imports:
        print(f"\nImporting {chunk_file} for source ID {source_id}")
        try:
            await import_chunks(source_id, chunk_file)
        except Exception as e:
            print(f"Failed to import {chunk_file}: {e}")
            continue
    
    print("\n" + "=" * 50)
    print("Import process completed!")
    
    # Verify imports
    conn = psycopg2.connect(
        host="85.25.172.47",
        port=5433,
        database="aidb",
        user="ai_admin",
        password="AIKnowledgeBase2025SecurePassword"
    )
    cur = conn.cursor()
    cur.execute('SET search_path TO ai_kb, public;')
    
    print("\nVerifying imports:")
    cur.execute("""
        SELECT s.id, s.title, COUNT(c.id) as chunk_count
        FROM sources s
        LEFT JOIN chunks c ON s.id = c.source_id
        WHERE s.id IN (7, 8, 9, 10, 11)
        GROUP BY s.id, s.title
        ORDER BY s.id
    """)
    
    for row in cur.fetchall():
        print(f"  Source {row[0]}: {row[1][:50]}... - {row[2]} chunks")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())