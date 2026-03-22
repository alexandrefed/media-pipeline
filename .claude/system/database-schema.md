# System: PostgreSQL Database Schema

## Overview

The AI Knowledge Base uses PostgreSQL 16 with pgvector extension for storing and querying YouTube video content with vector embeddings.

**Database Details:**
- **Host**: VPS (connection details via environment variables `DATABASE_URL` in `.env`)
- **Port**: 5433
- **Database**: aidb
- **Schema**: ai_kb
- **Vector Dimensions**: 768 (nomic-embed-text via Ollama)
- **Embedding Model**: nomic-embed-text (768-dim, via Ollama)

## Tables

### 1. sources

Stores metadata about YouTube videos.

```sql
CREATE TABLE ai_kb.sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    video_id TEXT NOT NULL,
    channel_name TEXT,
    description TEXT,
    duration INTEGER,
    publish_date DATE,
    ingestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status TEXT DEFAULT 'pending'
        CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
    processed_at TIMESTAMP,
    processing_stats JSONB DEFAULT '{}',
    transcript_quality TEXT DEFAULT 'auto'
        CHECK (transcript_quality IN ('auto', 'manual', 'professional', 'unknown'))
);
```

**Key Columns:**
- `id`: Unique identifier for the video source
- `video_id`: YouTube video ID (from URL)
- `processing_status`: Current processing state
- `processed_at`: When video was fully processed
- `processing_stats`: JSON with metrics (segments removed, summarized, etc.)
- `transcript_quality`: Source transcript quality level

**Indexes:**
```sql
CREATE INDEX idx_sources_processed_at ON sources(processed_at);
CREATE INDEX idx_sources_processing_status ON sources(processing_status);
```

### 2. chunks

Stores individual content chunks from videos with embeddings.

```sql
CREATE TABLE ai_kb.chunks (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    start_time FLOAT,
    end_time FLOAT,
    original_content TEXT NOT NULL,
    cleaned_content TEXT NOT NULL,
    embedding vector(384),
    mentioned_tools TEXT[] DEFAULT '{}',
    quality_score FLOAT DEFAULT 0.5
        CHECK (quality_score >= 0 AND quality_score <= 1),
    context_before TEXT DEFAULT '',
    context_after TEXT DEFAULT '',
    processing_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Key Columns:**
- `id`: Unique identifier for the chunk
- `source_id`: Foreign key to sources table
- `chunk_index`: Position in video (0-indexed)
- `start_time/end_time`: Timestamp in video (seconds)
- `original_content`: Raw transcript text
- `cleaned_content`: Enhanced, corrected text
- `embedding`: 768-dimensional vector for semantic search
- `mentioned_tools`: Array of tools referenced
- `quality_score`: Information density (0-1)
- `context_before/after`: Surrounding context for better understanding
- `processing_metadata`: JSON with segment type, actions, etc.

**Indexes:**
```sql
-- Vector similarity search (HNSW algorithm)
CREATE INDEX idx_chunks_embedding ON chunks
    USING hnsw (embedding vector_cosine_ops);

-- Quality-based queries
CREATE INDEX idx_chunks_quality_score ON chunks(quality_score DESC);

-- Tool search
CREATE INDEX idx_chunks_mentioned_tools ON chunks
    USING gin(mentioned_tools);

-- Full-text search
CREATE INDEX idx_chunks_cleaned_content_fts ON chunks
    USING gin(to_tsvector('english', cleaned_content));

-- Common query pattern
CREATE INDEX idx_chunks_source_quality ON chunks(source_id, quality_score DESC);
```

### 3. processing_history (Optional)

Tracks processing runs for continuous improvement.

```sql
CREATE TABLE ai_kb.processing_history (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    processing_version TEXT NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    segments_original INTEGER,
    segments_processed INTEGER,
    segments_removed INTEGER,
    segments_summarized INTEGER,
    chunks_created INTEGER,
    average_quality_score FLOAT,
    processing_time_ms INTEGER,
    error_log TEXT
);
```

**Purpose:**
- Track processing improvements over time
- Compare different processing versions
- Identify bottlenecks and errors
- Monitor quality trends

## Relationships

```
sources (1) ←→ (many) chunks
  └─ One video has many chunks
  └─ CASCADE DELETE: deleting source removes all chunks

sources (1) ←→ (many) processing_history
  └─ One video can have multiple processing runs
  └─ CASCADE DELETE: deleting source removes history
```

## Common Queries

### Insert New Video Source
```sql
INSERT INTO ai_kb.sources
    (title, url, video_id, channel_name, description)
VALUES
    ('Video Title', 'https://youtube.com/watch?v=ABC', 'ABC', 'Channel', 'Description')
RETURNING id;
```

### Insert Chunk with Embedding
```sql
INSERT INTO ai_kb.chunks
    (source_id, chunk_index, start_time, end_time, original_content,
     cleaned_content, embedding, mentioned_tools, quality_score)
VALUES
    (1, 0, 0.0, 30.5, 'Original text...', 'Cleaned text...',
     '[0.1, 0.2, ...]'::vector, ARRAY['Claude Code', 'n8n'], 0.85);
```

### Vector Similarity Search
```sql
SELECT
    c.id,
    c.cleaned_content,
    c.quality_score,
    s.title,
    s.channel_name,
    c.start_time,
    1 - (c.embedding <=> '[query_embedding]'::vector) as similarity
FROM ai_kb.chunks c
JOIN ai_kb.sources s ON c.source_id = s.id
WHERE 1 - (c.embedding <=> '[query_embedding]'::vector) > 0.5
ORDER BY c.embedding <=> '[query_embedding]'::vector
LIMIT 10;
```

### Quality-Based Filtering
```sql
SELECT
    c.cleaned_content,
    c.quality_score,
    s.title
FROM ai_kb.chunks c
JOIN ai_kb.sources s ON c.source_id = s.id
WHERE c.quality_score >= 0.7
ORDER BY c.quality_score DESC
LIMIT 20;
```

### Tool-Specific Search
```sql
SELECT
    c.cleaned_content,
    c.mentioned_tools,
    s.title,
    c.start_time
FROM ai_kb.chunks c
JOIN ai_kb.sources s ON c.source_id = s.id
WHERE 'Claude Code' = ANY(c.mentioned_tools)
ORDER BY c.quality_score DESC;
```

### Processing Statistics
```sql
SELECT
    processing_status,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (processed_at - ingestion_date))) as avg_time_seconds
FROM ai_kb.sources
GROUP BY processing_status;
```

### Chunk Quality Distribution
```sql
SELECT
    CASE
        WHEN quality_score >= 0.8 THEN 'High (0.8-1.0)'
        WHEN quality_score >= 0.6 THEN 'Medium (0.6-0.8)'
        WHEN quality_score >= 0.4 THEN 'Low (0.4-0.6)'
        ELSE 'Very Low (0-0.4)'
    END as quality_range,
    COUNT(*) as chunk_count,
    AVG(array_length(mentioned_tools, 1)) as avg_tools_mentioned
FROM ai_kb.chunks
GROUP BY quality_range
ORDER BY quality_range DESC;
```

## Performance Considerations

### Vector Search Optimization
- **HNSW Index**: Fast approximate nearest neighbor search
- **Trade-off**: Slight accuracy loss for major speed gain
- **Recommended**: Use similarity threshold (e.g., > 0.5) to filter results

### Quality Score Usage
- **Pre-filter**: Filter by quality before vector search to reduce candidates
- **Post-rank**: Use quality as secondary sort after similarity
- **Threshold**: 0.7+ for high-quality content, 0.5+ for general content

### Full-Text Search
- **GIN Index**: Fast text search on cleaned_content
- **Use case**: Exact phrase matching, keyword search
- **Complement**: Use with vector search for hybrid retrieval

## Maintenance

### Vacuum and Analyze
```sql
-- After bulk inserts
VACUUM ANALYZE ai_kb.chunks;
VACUUM ANALYZE ai_kb.sources;
```

### Index Rebuild (if performance degrades)
```sql
REINDEX INDEX ai_kb.idx_chunks_embedding;
```

### Backup
```bash
# Dump schema and data
# Use connection details from DATABASE_URL env var
pg_dump -h $DB_HOST -p 5433 -U ai_admin -d aidb -n ai_kb > backup.sql

# Restore
psql -h $DB_HOST -p 5433 -U ai_admin -d aidb < backup.sql
```

## Current Statistics

**As of last check:**
- **Videos processed**: 29
- **Chunks stored**: 435
- **Average chunk quality**: 0.78
- **Average tools per chunk**: 2.3

## Schema Source

Full schema definition: `deployment/sql/schema.sql`

## Related Documents

- [API Architecture](./api-architecture.md)
- [YouTube Video Processing SOP](../SOPs/youtube-video-processing.md)

## Version History

- v1.0 (Jan 2025): Initial database schema documentation
