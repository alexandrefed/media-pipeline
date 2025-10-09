# AI Knowledge Base Database Guide

## Overview

This guide documents the AI Knowledge Base PostgreSQL database with pgvector, rebuilt on 2025-07-14 with a 384-dimensional hybrid schema. The database is designed to analyze YouTube videos about AI tools, handling transcription errors and tracking tool relationships through a knowledge graph architecture.

## Quick Connection Info

```bash
Host: 85.25.172.47
Port: 5433
Database: aidb
Admin User: ai_admin
Admin Password: AIKnowledgeBase2025SecurePassword
Read-Only User: ai_user
Schema: ai_kb
```

---

## Architecture

### Technology Stack
- **PostgreSQL 16** with **pgvector 0.8.0**
- **Docker Container**: `vecia_aidb` (pgvector/pgvector:pg16)
- **Memory**: 2GB allocated (~50MB used)
- **Port**: 5433 (to avoid conflict with main PostgreSQL on 5432)
- **Network**: Docker network `vecia_network` (172.20.0.0/16)
- **Vector Model**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Architecture**: Knowledge graph + vector search + full-text search

### Database Schema (11-Table Hybrid Architecture)

```sql
-- Core Tables
ai_kb.sources                       -- YouTube videos/content sources
├── id, url, title, channel_name, published_date
├── quality_score, technical_level, content_type
└── transcript_available, processing_status

ai_kb.chunks                        -- Transcript chunks with embeddings
├── id, source_id, content, cleaned_content
├── embedding (vector(384))         -- sentence-transformers compatible
├── start_time, end_time, chunk_index
└── mentioned_tools[], mentioned_prices[]

ai_kb.entities                      -- AI tools with transcription aliases
├── id, canonical_name, entity_type, aliases[]
├── description, official_url, category
├── pricing_model, pricing_tiers (JSONB)
└── key_features[], platforms[]

-- Knowledge Graph Tables
ai_kb.relationship_types            -- Predefined relationships
ai_kb.entity_relationships          -- Tool connections
ai_kb.chunk_entities                -- Content-to-entity mappings
ai_kb.entity_capabilities           -- Tool capabilities
ai_kb.migration_paths               -- Tool migration guidance

-- Analysis Tables
ai_kb.use_case_patterns             -- Implementation patterns
ai_kb.comments                      -- Insights and corrections
ai_kb.quality_metrics               -- Content quality scoring
```

---

## Connection Methods

### 1. Direct PostgreSQL Connection

#### From Host Machine
```bash
# Using psql
PGPASSWORD='AIKnowledgeBase2025SecurePassword' psql -h localhost -p 5433 -U ai_admin -d aidb

# Using environment variable
export PGPASSWORD='AIKnowledgeBase2025SecurePassword'
psql -h localhost -p 5433 -U ai_admin -d aidb
```

#### From Docker Container
```bash
# Execute psql inside the container
docker exec -it -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb \
  psql -U ai_admin -d aidb -p 5433
```

#### Connection String
```
postgresql://ai_admin:AIKnowledgeBase2025SecurePassword@85.25.172.47:5433/aidb
```

### 2. Python Connection

```python
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector

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

# Example: Insert data with embedding
cur = conn.cursor()
embedding = np.random.rand(384).tolist()  # Replace with actual embedding

cur.execute("""
    INSERT INTO ai_kb.chunks 
    (source_id, content, cleaned_content, embedding, start_time, end_time, chunk_index, mentioned_tools)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (
    1,  # source_id
    "Original transcript text...",
    "Cleaned transcript with n8n instead of mate and...",
    embedding,  # 384-dimensional
    120.5,  # start_time
    145.3,  # end_time
    5,  # chunk_index
    ["n8n", "cursor", "claude"]  # mentioned_tools
))

conn.commit()
cur.close()
conn.close()
```

### 3. Node.js Connection

```javascript
const { Client } = require('pg');
const pgvector = require('pgvector/pg');

const client = new Client({
  host: '85.25.172.47',
  port: 5433,
  database: 'aidb',
  user: 'ai_admin',
  password: 'AIKnowledgeBase2025SecurePassword'
});

async function connect() {
  await client.connect();
  await pgvector.registerType(client);
  
  // Example: Query similar documents
  const embedding = Array(384).fill(0).map(() => Math.random());
  
  const result = await client.query(`
    SELECT c.id, c.content, c.embedding <-> $1 AS distance,
           s.title as video_title, s.channel_name
    FROM ai_kb.chunks c
    JOIN ai_kb.sources s ON c.source_id = s.id
    ORDER BY c.embedding <-> $1
    LIMIT 5
  `, [pgvector.toSql(embedding)]);
  
  console.log(result.rows);
  await client.end();
}

connect();
```

---

## Common Operations

### 1. Insert YouTube Video Source

```sql
-- Connect to the database first
SET search_path TO ai_kb, public;

-- Insert a YouTube video source
INSERT INTO sources (
    url, title, channel_name, channel_id,
    published_date, duration_seconds, view_count,
    quality_score, technical_level, content_type,
    domain_tags
) VALUES (
    'https://youtube.com/watch?v=example',
    'Complete n8n Tutorial for Beginners',
    'AI Automation Channel',
    'UC_channel_id',
    '2025-07-01'::timestamp,
    1850,  -- 30 min 50 sec
    125000,
    0.85,
    'beginner',
    'tutorial',
    ARRAY['automation', 'ai_tools', 'workflows']
) RETURNING id;
```

### 2. Search with Transcription Aliases

```sql
-- Find content mentioning "n8n" even if transcribed as "mate and"
SELECT DISTINCT
    e.canonical_name,
    e.aliases,
    c.content,
    s.title as video_title
FROM entities e
JOIN chunk_entities ce ON e.id = ce.entity_id
JOIN chunks c ON ce.chunk_id = c.id
JOIN sources s ON c.source_id = s.id
WHERE 
    e.canonical_name = 'n8n' 
    OR 'mate and' = ANY(e.aliases)
    OR 'n8nn' = ANY(e.aliases)
LIMIT 10;
```

### 3. Knowledge Graph Queries

```sql
-- Find tools that integrate with n8n
SELECT 
    e1.canonical_name as tool,
    rt.relationship_name,
    e2.canonical_name as integrates_with,
    er.properties->>'api' as api_type
FROM entities e1
JOIN entity_relationships er ON e1.id = er.source_entity_id
JOIN relationship_types rt ON er.relationship_type_id = rt.id
JOIN entities e2 ON er.target_entity_id = e2.id
WHERE 
    e1.canonical_name = 'n8n'
    AND rt.relationship_name = 'integrates_with'
ORDER BY er.strength DESC;
```

### 4. Vector Similarity Search (384-dim)

```sql
-- Find similar content using 384-dimensional embeddings
WITH query_embedding AS (
    SELECT '[0.1, 0.2, ...]'::vector(384) as vec  -- Your 384-dim embedding
)
SELECT 
    c.id,
    c.content,
    c.cleaned_content,
    c.embedding <-> (SELECT vec FROM query_embedding) AS cosine_distance,
    s.title as video_title,
    s.channel_name,
    CONCAT(s.url, '&t=', FLOOR(c.start_time)::text) as direct_link
FROM chunks c
JOIN sources s ON c.source_id = s.id
ORDER BY c.embedding <-> (SELECT vec FROM query_embedding)
LIMIT 5;
```

### 5. Migration Path Analysis

```sql
-- Find migration paths from one tool to another
SELECT 
    e1.canonical_name as from_tool,
    e2.canonical_name as to_tool,
    mp.migration_type,
    mp.difficulty_score,
    mp.feature_parity_percentage || '%' as feature_parity,
    mp.advantages,
    mp.limitations
FROM migration_paths mp
JOIN entities e1 ON mp.from_entity_id = e1.id
JOIN entities e2 ON mp.to_entity_id = e2.id
WHERE e1.canonical_name = 'Zapier'
ORDER BY mp.feature_parity_percentage DESC;
```

### 6. Use Case Pattern Matching

```sql
-- Find tools recommended for specific use cases
SELECT 
    ucp.pattern_name,
    ucp.description,
    array_agg(e.canonical_name) as recommended_tools,
    ucp.average_cost_monthly,
    ucp.complexity_score
FROM use_case_patterns ucp
JOIN unnest(ucp.recommended_tools) tool_id ON true
JOIN entities e ON e.id = tool_id
WHERE ucp.domain = 'e-commerce'
GROUP BY ucp.id, ucp.pattern_name, ucp.description, 
         ucp.average_cost_monthly, ucp.complexity_score
ORDER BY ucp.success_rate DESC;
```

---

## Manual Chunk Import Process

### Overview
The project uses a manual chunking workflow that creates high-quality, semantically coherent chunks. These chunks are stored as JSON files and need to be imported into the PostgreSQL database.

### Import Workflow

1. **Check if Source Exists**
```sql
-- Check if video is already in sources table
SELECT id, title, url FROM ai_kb.sources 
WHERE url LIKE '%VIDEO_ID%';
```

2. **Add New Source (if needed)**
```sql
INSERT INTO ai_kb.sources (
    url, title, channel_name, channel_id,
    published_date, duration_seconds,
    quality_score, technical_level, content_type,
    processing_status, transcript_available
) VALUES (
    'https://youtube.com/watch?v=VIDEO_ID',
    'Video Title',
    'Channel Name',
    'UC_channel_id',
    '2025-01-19'::timestamp,
    635,  -- duration in seconds
    0.85, -- quality score
    'intermediate',
    'tutorial',
    'completed',
    true
) RETURNING id;
```

3. **Import Manual Chunks Script**
```python
# Use this command to import all manual chunks:
PYTHONPATH=. uv run python scripts/import_all_chunks.py

# The script imports chunks using the correct database connection pattern:
import asyncio
import json
from src.database.connection import DatabaseConnection, get_database

async def import_manual_chunks(db: DatabaseConnection, source_id: int, chunks_file: str):
    """Import manual chunks from JSON file."""
    
    # Load chunks from file
    with open(f'processed/manual_chunks/{chunks_file}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    imported = 0
    
    async with db.get_connection() as conn:
        # Delete existing chunks if any
        await conn.execute(
            "DELETE FROM ai_kb.chunks WHERE source_id = $1",
            source_id
        )
        
        for chunk in chunks:
            # Extract mentioned tools
            mentioned_tools = extract_tools_from_content(chunk['text'])
            
            # Generate embedding using database connection
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
                0.9  # High quality for manual chunks
            )
            imported += 1
    
    return imported
```

### Current Videos Status

| Video ID | Source ID | Manual Chunks File | Status |
|----------|-----------|-------------------|---------|
| mKEq_YaJjPI | 3 | manual_chunks_mKEq_YaJjPI.json | In DB ✓ |
| arWg7gYVD_0 | 7 | manual_chunks_vibe_code_arWg7gYVD_0.json | In DB ✓ |
| u2NluvotA80 | 8 | manual_chunks_n8n_agents_u2NluvotA80.json | In DB ✓ |
| eM_Tg8_BGx4 | 9 | manual_chunks_claude_commands.json | In DB ✓ |
| hGg3nWp7afg | 10 | manual_chunks_3_folders.json | In DB ✓ |
| Y2XI2nk44WE | 11 | manual_chunks_openmemory_Y2XI2nk44WE.json | In DB ✓ |
| LEMLntjfihA | ? | manual_chunks_LEMLntjfihA.json | Add Source First |

### Tool Extraction

Common tools to detect in chunks:
- n8n (and aliases: "mate and", "n8nn")
- Claude Code, Claude 4
- Cursor, v0, Make.com
- MCP servers
- Deepseek, GPT-4, Sonnet
- Windsurf, Aider, Zapier

## Bulk Data Loading

### 1. Process YouTube Transcripts with Embeddings

```python
import pandas as pd
from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

# Initialize embedding model (384 dimensions)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to database
conn = psycopg2.connect(
    "postgresql://ai_admin:AIKnowledgeBase2025SecurePassword@85.25.172.47:5433/aidb"
)
register_vector(conn)
cur = conn.cursor()

# Example: Process transcript chunks
transcript_chunks = [
    {
        "content": "Today we'll look at mate and which is a powerful automation tool",
        "cleaned": "Today we'll look at n8n which is a powerful automation tool",
        "start_time": 0.0,
        "end_time": 5.5
    }
]

for i, chunk in enumerate(transcript_chunks):
    # Generate 384-dimensional embedding
    embedding = model.encode(chunk['cleaned']).tolist()
    
    # Insert chunk with embedding
    cur.execute("""
        INSERT INTO ai_kb.chunks 
        (source_id, content, cleaned_content, embedding, 
         start_time, end_time, chunk_index, mentioned_tools)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        1,  # source_id
        chunk['content'],
        chunk['cleaned'],
        embedding,
        chunk['start_time'],
        chunk['end_time'],
        i,
        ['n8n']  # detected tools
    ))

conn.commit()
```

### 2. Entity Recognition with Aliases

```python
# Detect and link entities in transcript chunks
def detect_entities(text, entities_dict):
    """Detect entities considering their aliases"""
    found_entities = []
    text_lower = text.lower()
    
    for entity_id, (name, aliases) in entities_dict.items():
        # Check canonical name
        if name.lower() in text_lower:
            found_entities.append(entity_id)
            continue
            
        # Check aliases
        for alias in aliases:
            if alias.lower() in text_lower:
                found_entities.append(entity_id)
                break
                
    return found_entities

# Load entities with aliases
cur.execute("""
    SELECT id, canonical_name, aliases 
    FROM ai_kb.entities 
    WHERE entity_type = 'tool'
""")
entities = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

# Process chunks and link entities
chunk_id = 1
text = "I use mate and for automation and curser for coding"
found_entity_ids = detect_entities(text, entities)

# Insert chunk-entity relationships
for entity_id in found_entity_ids:
    cur.execute("""
        INSERT INTO ai_kb.chunk_entities 
        (chunk_id, entity_id, confidence, original_text)
        VALUES (%s, %s, %s, %s)
    """, (chunk_id, entity_id, 0.95, text))
```

---

## Index Management

### HNSW Index for 384-Dimensional Vectors
```sql
-- The index is already created in the schema, but if you need to recreate:
SET maintenance_work_mem = '1GB';
SET max_parallel_maintenance_workers = 4;

-- HNSW index optimized for 384-dim sentence-transformers
-- Uses cosine similarity (best for normalized embeddings)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding 
ON ai_kb.chunks 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

-- Additional indexes for hybrid search
CREATE INDEX IF NOT EXISTS idx_entities_aliases ON ai_kb.entities USING gin(aliases);
CREATE INDEX IF NOT EXISTS idx_chunks_content_search ON ai_kb.chunks USING gin(to_tsvector('english', cleaned_content));
```

### Index Maintenance
```sql
-- Check all index sizes in the hybrid schema
SELECT 
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(schemaname||'.'||indexname)) as size
FROM pg_indexes 
WHERE schemaname = 'ai_kb'
ORDER BY pg_relation_size(schemaname||'.'||indexname) DESC;

-- Reindex vector index if needed
REINDEX INDEX ai_kb.idx_chunks_embedding;

-- Vacuum and analyze all tables
VACUUM ANALYZE ai_kb.chunks;
VACUUM ANALYZE ai_kb.entities;
VACUUM ANALYZE ai_kb.entity_relationships;
```

---

## Monitoring and Maintenance

### Check Database Status
```bash
# Container status
docker ps | grep vecia_aidb

# Database logs
docker logs vecia_aidb --tail 50

# Connect and check table sizes
docker exec -it -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb \
  psql -U ai_admin -d aidb -p 5433 -c "
SELECT tablename, pg_size_pretty(pg_total_relation_size('ai_kb.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'ai_kb' ORDER BY tablename;"
```

### Performance Monitoring
```sql
-- Check slow queries on vector operations
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time
FROM pg_stat_statements 
WHERE query LIKE '%chunks%' 
   OR query LIKE '%entities%'
   OR query LIKE '%vector%'
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'ai_kb'
ORDER BY idx_scan DESC;
```

### Backup and Restore

#### Manual Backup
```bash
# Run backup script
/root/vecia/scripts/backup-aidb.sh

# Or manually
docker exec -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb \
  pg_dump -U ai_admin -d aidb -p 5433 > aidb_backup_$(date +%Y%m%d).sql
```

#### Restore from Backup
```bash
# Create new database if needed
docker exec -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb \
  psql -U ai_admin -p 5433 -c "CREATE DATABASE aidb_restore;"

# Restore backup
docker exec -i -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb \
  psql -U ai_admin -d aidb_restore -p 5433 < aidb_backup_20250714.sql
```

---

## Transcription Error Handling

### Understanding the Alias System
The database handles common speech-to-text errors in AI tool names:

```sql
-- View all entities with their transcription aliases
SELECT 
    canonical_name,
    entity_type,
    aliases,
    array_length(aliases, 1) as alias_count
FROM ai_kb.entities
WHERE entity_type = 'tool'
ORDER BY canonical_name;

-- Examples:
-- n8n: ['mate and', 'n8nn', 'n 8 n', 'innate in', 'inn ate inn']
-- Cursor: ['curser', 'cursor ai', 'kursor', 'cursor IDE']
-- Claude: ['claud', 'cloud', 'claude ai', 'claude anthropic']
```

### Adding New Aliases
```sql
-- Add a new transcription alias to an existing tool
UPDATE ai_kb.entities
SET aliases = array_append(aliases, 'new transcription error')
WHERE canonical_name = 'n8n';

-- Or use array concatenation for multiple aliases
UPDATE ai_kb.entities
SET aliases = aliases || ARRAY['mate n', 'maten']
WHERE canonical_name = 'n8n';
```

---

## Security Best Practices

### 1. User Management
```sql
-- Create application-specific user with limited permissions
CREATE USER app_user WITH PASSWORD 'SecureAppPassword';
GRANT CONNECT ON DATABASE aidb TO app_user;
GRANT USAGE ON SCHEMA ai_kb TO app_user;
GRANT SELECT, INSERT ON ai_kb.ai_market_data TO app_user;
GRANT SELECT ON ai_kb.ai_users TO app_user;
```

### 2. SSL Connection
Always use SSL for remote connections:
```bash
psql "postgresql://ai_admin:password@85.25.172.47:5433/aidb?sslmode=require"
```

### 3. API Key Management
Store API keys in the ai_users table:
```sql
INSERT INTO ai_kb.ai_users (user_id, api_key, name, email, role, rate_limit)
VALUES ('app_1', 'sk-your-secure-api-key', 'Application 1', 'app1@vecia.fr', 'user', 100);
```

---

## Troubleshooting

### Connection Issues
```bash
# Test connection from host
nc -zv localhost 5433

# Check firewall
sudo ufw status | grep 5433

# Check Docker port mapping
docker port vecia_aidb
```

### Performance Issues
```sql
-- Increase work memory for current session
SET work_mem = '256MB';

-- Check query plan for vector search
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.*, s.title 
FROM ai_kb.chunks c
JOIN ai_kb.sources s ON c.source_id = s.id
ORDER BY c.embedding <-> '[...]'::vector(384) 
LIMIT 5;
```

### Container Issues
```bash
# Restart container
docker restart vecia_aidb

# Rebuild if needed
cd /root/vecia
docker compose up -d --force-recreate vecia_aidb
```

---

## Quick Reference Commands

```bash
# Connect to database
docker exec -it -e PGPASSWORD='AIKnowledgeBase2025SecurePassword' vecia_aidb psql -U ai_admin -d aidb -p 5433

# View logs
docker logs vecia_aidb --tail 100 -f

# Backup database
/root/vecia/scripts/backup-aidb.sh

# Check status
docker compose ps vecia_aidb

# Resource usage
docker stats vecia_aidb --no-stream
```

## Manual Chunking Workflow Reference

```bash
# Step 1: Extract transcript
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"

# Step 2: Enhance manually in Claude Code
# - Apply corrections from learning/processing_knowledge_base.json
# - Save as enhanced_transcript_VIDEO_ID_manual.txt

# Step 3: Create manual chunks
uv run python scripts/manual_chunker.py

# Step 4: Import to database
uv run python scripts/import_chunks.py --source-id ID --chunks-file manual_chunks_VIDEO_ID.json

# Step 5: Update learning system
# - Add new patterns to processing_knowledge_base.json
# - Update processing_history.md
```

---

*Updated: 2025-01-20*
*Architecture: 384-dimensional hybrid schema (Knowledge Graph + Vector Search)*
*Database: PostgreSQL 16 with pgvector 0.8.0*
*Container: vecia_aidb on port 5433*
*Embedding Model: sentence-transformers/all-MiniLM-L6-v2*