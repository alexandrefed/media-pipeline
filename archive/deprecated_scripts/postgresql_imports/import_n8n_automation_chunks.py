"""Import manual chunks for n8n automation video"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import psycopg2
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np

# Database configuration
DB_CONFIG = {
    "host": "85.25.172.47",
    "port": 5433,
    "database": "aidb",
    "user": "ai_admin",
    "password": "AIKnowledgeBase2025SecurePassword"
}

def get_or_create_source(cursor, video_id, title, channel):
    """Get or create source record"""
    # Check if source exists
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    cursor.execute("""
        SELECT id FROM ai_kb.sources 
        WHERE url = %s
    """, (video_url,))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Create new source
    cursor.execute("""
        INSERT INTO ai_kb.sources (url, title, channel_name, ingestion_date, processing_status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (video_url, title, channel, datetime.now(), 'processed'))
    
    return cursor.fetchone()[0]

def import_chunks():
    """Import manual chunks to database"""
    # Load model for embeddings
    print("Loading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Load chunks
    chunks_file = "../processed/manual_chunks/manual_chunks_QJSE1yXoDxQ.json"
    print(f"Loading chunks from {chunks_file}")
    
    with open(chunks_file, 'r') as f:
        data = json.load(f)
    
    video_meta = data['video_metadata']
    chunks = data['chunks']
    
    print(f"Found {len(chunks)} chunks")
    
    # Connect to database
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('SET search_path TO ai_kb, public;')
    
    try:
        # Get or create source
        source_id = get_or_create_source(
            cursor,
            video_meta['video_id'],
            video_meta['title'],
            video_meta['channel']
        )
        print(f"Using source ID: {source_id}")
        
        # Delete existing chunks for this source
        cursor.execute("DELETE FROM ai_kb.chunks WHERE source_id = %s", (source_id,))
        print(f"Deleted existing chunks for source {source_id}")
        
        # Import each chunk
        for idx, chunk in enumerate(chunks):
            # Generate embedding
            embedding = model.encode(chunk['text'])
            embedding_list = embedding.tolist()
            
            # Calculate quality score based on token count and importance
            base_score = min(chunk['token_count'] / 200, 1.0) * 0.7
            importance_bonus = 0.3 if chunk.get('importance') == 'high' else 0.15
            quality_score = base_score + importance_bonus
            
            # Insert chunk
            cursor.execute("""
                INSERT INTO ai_kb.chunks (
                    source_id, content, start_time, end_time,
                    embedding, quality_score, processing_metadata,
                    mentioned_tools, tokens_count, chunk_index
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                source_id,
                chunk['text'],
                chunk['start_time'],
                chunk['end_time'],
                embedding_list,
                quality_score,
                json.dumps({
                    'topics': chunk.get('topics', []),
                    'importance': chunk.get('importance', 'medium'),
                    'context': chunk.get('context', ''),
                    'chunk_id': chunk['chunk_id'],
                    'processing_method': 'manual_semantic'
                }),
                chunk.get('topics', []),  # using topics as mentioned_tools
                chunk['token_count'],
                idx  # chunk_index
            ))
        
        # Commit transaction
        conn.commit()
        print(f"Successfully imported {len(chunks)} chunks")
        
        # Verify import
        cursor.execute("""
            SELECT COUNT(*) FROM ai_kb.chunks WHERE source_id = %s
        """, (source_id,))
        count = cursor.fetchone()[0]
        print(f"Verified: {count} chunks in database for source {source_id}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error importing chunks: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import_chunks()