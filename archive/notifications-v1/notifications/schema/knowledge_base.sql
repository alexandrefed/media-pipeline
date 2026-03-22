-- ============================================================================
-- AI KNOWLEDGE BASE SCHEMA
-- ============================================================================
-- Purpose: Database schema for n8n workflow integration
-- Database: aidb (PostgreSQL 16 with pgvector)
-- Schema: ai_kb
-- Created: 2025-10-20
-- ============================================================================

-- Ensure we're in the correct schema
SET search_path TO ai_kb, public;

-- ============================================================================
-- TABLE: kb_videos
-- Purpose: Store YouTube video metadata and processing status
-- ============================================================================
CREATE TABLE IF NOT EXISTS kb_videos (
    -- Primary Key
    video_id VARCHAR(20) PRIMARY KEY,  -- YouTube video ID

    -- Video Metadata
    title VARCHAR(500) NOT NULL,
    channel_name VARCHAR(200) NOT NULL,
    channel_id VARCHAR(50),
    url TEXT NOT NULL,
    duration_seconds INTEGER,
    published_at TIMESTAMPTZ,

    -- Content Classification
    pipeline_type VARCHAR(20) DEFAULT 'ai_tools' CHECK (pipeline_type IN ('ai_tools', 'sports')),
    content_tags TEXT[],  -- Array of tags (e.g., ['n8n', 'automation', 'tutorial'])

    -- Processing Status
    processing_status VARCHAR(20) DEFAULT 'pending' CHECK (
        processing_status IN ('pending', 'extracted', 'enhanced', 'chunked', 'completed', 'failed')
    ),
    processing_stage VARCHAR(50),  -- Current stage details
    error_message TEXT,  -- Error details if failed

    -- Transcript Files
    raw_transcript_path TEXT,
    enhanced_transcript_path TEXT,
    analysis_json_path TEXT,

    -- Quality Metrics
    total_chunks INTEGER DEFAULT 0,
    avg_chunk_quality DECIMAL(3,2),  -- Average quality score (0-1)
    total_insights INTEGER DEFAULT 0,  -- Count of actionable insights

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,  -- When fully processed

    -- Notification Tracking
    notification_sent BOOLEAN DEFAULT FALSE,
    notification_sent_at TIMESTAMPTZ,

    -- Indexes will be added below
    CONSTRAINT valid_duration CHECK (duration_seconds IS NULL OR duration_seconds > 0),
    CONSTRAINT valid_chunks CHECK (total_chunks >= 0),
    CONSTRAINT valid_quality CHECK (avg_chunk_quality IS NULL OR (avg_chunk_quality >= 0 AND avg_chunk_quality <= 1))
);

-- Indexes for kb_videos
CREATE INDEX IF NOT EXISTS idx_kb_videos_status ON kb_videos(processing_status);
CREATE INDEX IF NOT EXISTS idx_kb_videos_pipeline ON kb_videos(pipeline_type);
CREATE INDEX IF NOT EXISTS idx_kb_videos_created ON kb_videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_kb_videos_channel ON kb_videos(channel_id);
CREATE INDEX IF NOT EXISTS idx_kb_videos_tags ON kb_videos USING GIN(content_tags);
CREATE INDEX IF NOT EXISTS idx_kb_videos_notification ON kb_videos(notification_sent, created_at);

-- ============================================================================
-- TABLE: kb_insights
-- Purpose: Store extractable insights for spaced repetition
-- ============================================================================
CREATE TABLE IF NOT EXISTS kb_insights (
    -- Primary Key
    insight_id SERIAL PRIMARY KEY,

    -- Foreign Keys
    video_id VARCHAR(20) NOT NULL REFERENCES kb_videos(video_id) ON DELETE CASCADE,

    -- Insight Content
    insight_text TEXT NOT NULL,
    insight_type VARCHAR(30) NOT NULL CHECK (
        insight_type IN (
            'protocol',        -- Exercise protocol or workflow
            'concept',         -- Core concept or principle
            'technique',       -- Specific technique or method
            'tip',            -- Quick tip or best practice
            'warning',        -- Common mistake or warning
            'tool_usage',     -- Tool-specific usage pattern
            'strategy'        -- Strategic approach
        )
    ),

    -- Context
    context TEXT,  -- Additional context or prerequisites
    category VARCHAR(50),  -- Domain category (e.g., 'n8n', 'biomechanics')
    tags TEXT[],  -- Searchable tags

    -- Source Reference
    timestamp_start INTEGER,  -- Start timestamp in seconds
    timestamp_end INTEGER,    -- End timestamp in seconds
    source_chunk_id INTEGER,  -- Reference to original chunk if exists

    -- Quality & Priority
    quality_score DECIMAL(3,2) CHECK (quality_score >= 0 AND quality_score <= 1),
    priority_level VARCHAR(10) DEFAULT 'medium' CHECK (
        priority_level IN ('low', 'medium', 'high', 'critical')
    ),
    actionable BOOLEAN DEFAULT TRUE,

    -- Spaced Repetition Metrics
    repetition_count INTEGER DEFAULT 0,
    next_review_date DATE,
    last_reviewed_at TIMESTAMPTZ,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,  -- SM-2 algorithm factor
    interval_days INTEGER DEFAULT 1,        -- Current review interval

    -- User Interaction
    times_sent INTEGER DEFAULT 0,
    last_sent_at TIMESTAMPTZ,
    user_rating INTEGER CHECK (user_rating IS NULL OR (user_rating >= 1 AND user_rating <= 5)),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT valid_timestamps CHECK (
        timestamp_start IS NULL OR
        timestamp_end IS NULL OR
        timestamp_end >= timestamp_start
    )
);

-- Indexes for kb_insights
CREATE INDEX IF NOT EXISTS idx_kb_insights_video ON kb_insights(video_id);
CREATE INDEX IF NOT EXISTS idx_kb_insights_type ON kb_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_kb_insights_next_review ON kb_insights(next_review_date)
    WHERE next_review_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_kb_insights_quality ON kb_insights(quality_score DESC);
CREATE INDEX IF NOT EXISTS idx_kb_insights_priority ON kb_insights(priority_level);
CREATE INDEX IF NOT EXISTS idx_kb_insights_tags ON kb_insights USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_kb_insights_created ON kb_insights(created_at DESC);

-- ============================================================================
-- TABLE: kb_notifications
-- Purpose: Track all notification sends (immediate and spaced repetition)
-- ============================================================================
CREATE TABLE IF NOT EXISTS kb_notifications (
    -- Primary Key
    notification_id SERIAL PRIMARY KEY,

    -- Foreign Keys
    video_id VARCHAR(20) REFERENCES kb_videos(video_id) ON DELETE SET NULL,
    insight_id INTEGER REFERENCES kb_insights(insight_id) ON DELETE SET NULL,

    -- Notification Details
    notification_type VARCHAR(30) NOT NULL CHECK (
        notification_type IN (
            'video_processed',    -- New video completed
            'insight_reminder',   -- Spaced repetition reminder
            'weekly_digest',      -- Weekly summary
            'daily_insight',      -- Daily insight
            'custom'             -- Custom notification
        )
    ),

    -- Content
    title VARCHAR(500) NOT NULL,
    message TEXT NOT NULL,
    formatted_html TEXT,  -- Full HTML formatted message

    -- Delivery Details
    channel VARCHAR(20) DEFAULT 'telegram' CHECK (channel IN ('telegram', 'email', 'webhook')),
    recipient_id VARCHAR(100),  -- Chat ID or email

    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (
        status IN ('pending', 'sent', 'failed', 'cancelled')
    ),
    error_message TEXT,

    -- Response Tracking
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    user_responded BOOLEAN DEFAULT FALSE,
    user_response TEXT,

    -- Metadata
    metadata JSONB,  -- Additional flexible data

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    scheduled_for TIMESTAMPTZ,  -- When to send (for scheduled notifications)

    -- Constraints
    CONSTRAINT valid_delivery CHECK (
        status != 'sent' OR delivered_at IS NOT NULL
    )
);

-- Indexes for kb_notifications
CREATE INDEX IF NOT EXISTS idx_kb_notifications_video ON kb_notifications(video_id);
CREATE INDEX IF NOT EXISTS idx_kb_notifications_insight ON kb_notifications(insight_id);
CREATE INDEX IF NOT EXISTS idx_kb_notifications_type ON kb_notifications(notification_type);
CREATE INDEX IF NOT EXISTS idx_kb_notifications_status ON kb_notifications(status);
CREATE INDEX IF NOT EXISTS idx_kb_notifications_created ON kb_notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_kb_notifications_scheduled ON kb_notifications(scheduled_for)
    WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_kb_notifications_metadata ON kb_notifications USING GIN(metadata);

-- ============================================================================
-- TABLE: kb_weekly_digests
-- Purpose: Track weekly digest generation and delivery
-- ============================================================================
CREATE TABLE IF NOT EXISTS kb_weekly_digests (
    -- Primary Key
    digest_id SERIAL PRIMARY KEY,

    -- Time Period
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,

    -- Content Summary
    total_videos INTEGER DEFAULT 0,
    total_insights INTEGER DEFAULT 0,
    video_ids TEXT[],  -- Array of video IDs included

    -- Categories Breakdown
    ai_tools_count INTEGER DEFAULT 0,
    sports_count INTEGER DEFAULT 0,

    -- Top Insights
    top_insights_json JSONB,  -- Structured data of top insights

    -- Delivery
    notification_id INTEGER REFERENCES kb_notifications(notification_id) ON DELETE SET NULL,
    sent_at TIMESTAMPTZ,

    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (
        status IN ('pending', 'generating', 'completed', 'sent', 'failed')
    ),
    error_message TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT valid_week_period CHECK (week_end_date >= week_start_date),
    CONSTRAINT valid_counts CHECK (
        total_videos >= 0 AND
        total_insights >= 0 AND
        ai_tools_count >= 0 AND
        sports_count >= 0
    ),
    UNIQUE(week_start_date, week_end_date)
);

-- Indexes for kb_weekly_digests
CREATE INDEX IF NOT EXISTS idx_kb_weekly_digests_dates ON kb_weekly_digests(week_start_date, week_end_date);
CREATE INDEX IF NOT EXISTS idx_kb_weekly_digests_status ON kb_weekly_digests(status);
CREATE INDEX IF NOT EXISTS idx_kb_weekly_digests_created ON kb_weekly_digests(created_at DESC);

-- ============================================================================
-- TRIGGERS: Auto-update timestamps
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables
DROP TRIGGER IF EXISTS update_kb_videos_updated_at ON kb_videos;
CREATE TRIGGER update_kb_videos_updated_at
    BEFORE UPDATE ON kb_videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_kb_insights_updated_at ON kb_insights;
CREATE TRIGGER update_kb_insights_updated_at
    BEFORE UPDATE ON kb_insights
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_kb_notifications_updated_at ON kb_notifications;
CREATE TRIGGER update_kb_notifications_updated_at
    BEFORE UPDATE ON kb_notifications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_kb_weekly_digests_updated_at ON kb_weekly_digests;
CREATE TRIGGER update_kb_weekly_digests_updated_at
    BEFORE UPDATE ON kb_weekly_digests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS: Convenient queries for n8n workflows
-- ============================================================================

-- View: Videos ready for notification
CREATE OR REPLACE VIEW v_videos_pending_notification AS
SELECT
    video_id,
    title,
    channel_name,
    url,
    pipeline_type,
    total_chunks,
    total_insights,
    processed_at
FROM kb_videos
WHERE
    processing_status = 'completed'
    AND notification_sent = FALSE
    AND processed_at IS NOT NULL
ORDER BY processed_at DESC;

-- View: Insights due for review (spaced repetition)
CREATE OR REPLACE VIEW v_insights_due_for_review AS
SELECT
    i.insight_id,
    i.video_id,
    v.title as video_title,
    v.url as video_url,
    i.insight_text,
    i.insight_type,
    i.category,
    i.quality_score,
    i.priority_level,
    i.next_review_date,
    i.repetition_count,
    i.timestamp_start,
    i.timestamp_end
FROM kb_insights i
JOIN kb_videos v ON i.video_id = v.video_id
WHERE
    i.next_review_date IS NOT NULL
    AND i.next_review_date <= CURRENT_DATE
    AND v.processing_status = 'completed'
ORDER BY
    i.priority_level DESC,
    i.quality_score DESC,
    i.next_review_date ASC;

-- View: Weekly digest data (current week)
CREATE OR REPLACE VIEW v_current_week_summary AS
SELECT
    DATE_TRUNC('week', CURRENT_DATE)::DATE as week_start,
    (DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '6 days')::DATE as week_end,
    COUNT(*) as total_videos,
    SUM(total_insights) as total_insights,
    COUNT(*) FILTER (WHERE pipeline_type = 'ai_tools') as ai_tools_count,
    COUNT(*) FILTER (WHERE pipeline_type = 'sports') as sports_count,
    ARRAY_AGG(video_id ORDER BY processed_at DESC) as video_ids,
    ARRAY_AGG(
        JSON_BUILD_OBJECT(
            'video_id', video_id,
            'title', title,
            'url', url,
            'insights', total_insights,
            'processed_at', processed_at
        ) ORDER BY processed_at DESC
    ) as videos_json
FROM kb_videos
WHERE
    processed_at >= DATE_TRUNC('week', CURRENT_DATE)
    AND processed_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
    AND processing_status = 'completed';

-- ============================================================================
-- SAMPLE QUERIES FOR n8n WORKFLOWS
-- ============================================================================

-- Example 1: Get videos ready for notification
COMMENT ON VIEW v_videos_pending_notification IS
'Use in n8n workflow: SELECT * FROM v_videos_pending_notification LIMIT 10;';

-- Example 2: Get today''s insights for spaced repetition
COMMENT ON VIEW v_insights_due_for_review IS
'Use in n8n workflow: SELECT * FROM v_insights_due_for_review LIMIT 5;';

-- Example 3: Generate weekly digest
COMMENT ON VIEW v_current_week_summary IS
'Use in n8n workflow: SELECT * FROM v_current_week_summary;';

-- Example 4: Mark notification as sent
COMMENT ON TABLE kb_notifications IS
'After sending: UPDATE kb_notifications SET status = ''sent'', delivered_at = CURRENT_TIMESTAMP WHERE notification_id = ?';

-- Example 5: Update spaced repetition after review
COMMENT ON TABLE kb_insights IS
'After review: UPDATE kb_insights SET
  repetition_count = repetition_count + 1,
  last_reviewed_at = CURRENT_TIMESTAMP,
  next_review_date = CURRENT_DATE + interval_days,
  interval_days = interval_days * 2
WHERE insight_id = ?';

-- ============================================================================
-- GRANTS: Ensure n8n user has proper permissions
-- ============================================================================

-- Grant permissions to ai_admin (your n8n database user)
GRANT USAGE ON SCHEMA ai_kb TO ai_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ai_kb TO ai_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA ai_kb TO ai_admin;
GRANT SELECT ON ALL TABLES IN SCHEMA ai_kb TO ai_admin;

-- ============================================================================
-- COMPLETION
-- ============================================================================

-- Verification query
DO $$
BEGIN
    RAISE NOTICE '=================================================================';
    RAISE NOTICE 'AI Knowledge Base Schema Installation Complete';
    RAISE NOTICE '=================================================================';
    RAISE NOTICE 'Tables created:';
    RAISE NOTICE '  - kb_videos (video metadata & processing status)';
    RAISE NOTICE '  - kb_insights (extractable insights for spaced repetition)';
    RAISE NOTICE '  - kb_notifications (notification tracking)';
    RAISE NOTICE '  - kb_weekly_digests (weekly digest tracking)';
    RAISE NOTICE '';
    RAISE NOTICE 'Views created:';
    RAISE NOTICE '  - v_videos_pending_notification';
    RAISE NOTICE '  - v_insights_due_for_review';
    RAISE NOTICE '  - v_current_week_summary';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '  1. Test schema with: SELECT * FROM kb_videos;';
    RAISE NOTICE '  2. Build n8n workflows using these tables';
    RAISE NOTICE '  3. Integrate with notification system';
    RAISE NOTICE '=================================================================';
END $$;
