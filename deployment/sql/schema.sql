-- Complete Database Schema Update for AI Knowledge Base with Transcript Processing
-- This includes all columns needed for the enhanced processing pipeline
-- Run this on the VPS database: psql -h 85.25.172.47 -p 5433 -U ai_admin -d aidb

-- Set the schema
SET search_path TO ai_kb;

-- ============================================
-- UPDATE CHUNKS TABLE
-- ============================================

-- Add quality_score column (normalized 0-1 for information density)
ALTER TABLE chunks 
ADD COLUMN IF NOT EXISTS quality_score FLOAT DEFAULT 0.5 
    CHECK (quality_score >= 0 AND quality_score <= 1);

-- Add context columns for better search and understanding
ALTER TABLE chunks 
ADD COLUMN IF NOT EXISTS context_before TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS context_after TEXT DEFAULT '';

-- Optional: Add processing metadata columns for tracking
ALTER TABLE chunks
ADD COLUMN IF NOT EXISTS processing_metadata JSONB DEFAULT '{}';
-- This can store: segment_type, action_taken, was_summarized, etc.

COMMENT ON COLUMN chunks.quality_score IS 'Information density score (0-1) based on content type and value';
COMMENT ON COLUMN chunks.context_before IS 'Text from preceding segments for context';
COMMENT ON COLUMN chunks.context_after IS 'Text from following segments for context';
COMMENT ON COLUMN chunks.processing_metadata IS 'Metadata from transcript processing (segment types, actions, etc)';

-- ============================================
-- UPDATE SOURCES TABLE
-- ============================================

-- Add processed_at timestamp
ALTER TABLE sources 
ADD COLUMN IF NOT EXISTS processed_at TIMESTAMP;

-- Add processing statistics column
ALTER TABLE sources
ADD COLUMN IF NOT EXISTS processing_stats JSONB DEFAULT '{}';
-- This stores: segments_removed, segments_summarized, original_duration, etc.

-- Add transcript quality metadata
ALTER TABLE sources
ADD COLUMN IF NOT EXISTS transcript_quality TEXT DEFAULT 'auto'
    CHECK (transcript_quality IN ('auto', 'manual', 'professional', 'unknown'));

COMMENT ON COLUMN sources.processed_at IS 'When the video was processed through the pipeline';
COMMENT ON COLUMN sources.processing_stats IS 'Statistics from transcript processing';
COMMENT ON COLUMN sources.transcript_quality IS 'Quality of the source transcript';

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================

-- Index for quality-based queries
CREATE INDEX IF NOT EXISTS idx_chunks_quality_score ON chunks(quality_score DESC);

-- Index for searching by mentioned tools
CREATE INDEX IF NOT EXISTS idx_chunks_mentioned_tools ON chunks USING gin(mentioned_tools);

-- Index for full-text search on cleaned content
CREATE INDEX IF NOT EXISTS idx_chunks_cleaned_content_fts 
    ON chunks USING gin(to_tsvector('english', cleaned_content));

-- Index for processed videos
CREATE INDEX IF NOT EXISTS idx_sources_processed_at ON sources(processed_at);
CREATE INDEX IF NOT EXISTS idx_sources_processing_status ON sources(processing_status);

-- Composite index for common query patterns
CREATE INDEX IF NOT EXISTS idx_chunks_source_quality 
    ON chunks(source_id, quality_score DESC);

-- ============================================
-- UPDATE EXISTING DATA (if any)
-- ============================================

-- Set default quality scores for existing chunks
UPDATE chunks 
SET quality_score = CASE 
    WHEN array_length(mentioned_tools, 1) > 2 THEN 0.8
    WHEN array_length(mentioned_tools, 1) > 0 THEN 0.6
    ELSE 0.5
END
WHERE quality_score IS NULL;

-- Set processed_at for existing completed sources
UPDATE sources 
SET processed_at = ingestion_date 
WHERE processing_status = 'completed' AND processed_at IS NULL;

-- Initialize empty processing stats for existing sources
UPDATE sources 
SET processing_stats = '{}'::jsonb 
WHERE processing_stats IS NULL;

-- ============================================
-- OPTIONAL: PROCESSING HISTORY TABLE
-- ============================================

-- Create a table to track processing history and improvements
CREATE TABLE IF NOT EXISTS processing_history (
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

COMMENT ON TABLE processing_history IS 'Track processing runs for continuous improvement';

-- ============================================
-- VERIFY FINAL SCHEMA
-- ============================================

-- Check chunks table structure
SELECT 
    column_name, 
    data_type, 
    column_default,
    is_nullable,
    character_maximum_length
FROM information_schema.columns 
WHERE table_schema = 'ai_kb' 
AND table_name = 'chunks'
ORDER BY ordinal_position;

-- Check sources table structure
SELECT 
    column_name, 
    data_type, 
    column_default,
    is_nullable,
    character_maximum_length
FROM information_schema.columns 
WHERE table_schema = 'ai_kb' 
AND table_name = 'sources'
ORDER BY ordinal_position;

-- Show all indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'ai_kb'
ORDER BY tablename, indexname;

-- ============================================
-- USEFUL QUERIES FOR TESTING
-- ============================================

-- Check processing statistics
SELECT 
    processing_status,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (processed_at - ingestion_date))) as avg_processing_time_seconds
FROM sources
GROUP BY processing_status;

-- Check chunk quality distribution
SELECT 
    CASE 
        WHEN quality_score >= 0.8 THEN 'High (0.8-1.0)'
        WHEN quality_score >= 0.6 THEN 'Medium (0.6-0.8)'
        WHEN quality_score >= 0.4 THEN 'Low (0.4-0.6)'
        ELSE 'Very Low (0-0.4)'
    END as quality_range,
    COUNT(*) as chunk_count,
    AVG(array_length(mentioned_tools, 1)) as avg_tools_mentioned
FROM chunks
GROUP BY quality_range
ORDER BY quality_range DESC;