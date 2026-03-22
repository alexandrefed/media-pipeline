# n8n + PostgreSQL Integration - Complete Setup Summary

**Date**: 2025-10-20
**Status**: ✅ Core Infrastructure Complete

## Overview

Successfully integrated the AI Knowledge Base notification system with n8n and PostgreSQL on VPS for automated workflows and long-term data retention.

---

## ✅ Completed Tasks

### 1. PostgreSQL Connection Setup

**Connection Details**:
- **Host**: `vecia_aidb` (Docker container name)
- **Port**: `5433`
- **Database**: `aidb`
- **Schema**: `ai_kb`
- **User**: `ai_admin`
- **Status**: ✅ Connection tested successfully

**Configuration**:
- Credential Name: "Postgres account" (ID: `Lg6POD6iPiWwwFkQ`)
- Updated via Playwright automation
- Auto-tested on save

### 2. Database Schema Deployment

**Schema File**: `notifications/schema/knowledge_base.sql`

**Tables Created**:
1. **kb_videos** - Video metadata and processing status
   - Fields: video_id, title, channel_name, url, pipeline_type, processing_status, total_chunks, total_insights, etc.
   - Indexes: status, pipeline, created_at, channel, tags, notification

2. **kb_insights** - Extractable insights for spaced repetition
   - Fields: insight_text, insight_type, quality_score, priority_level, repetition_count, next_review_date, etc.
   - Spaced repetition: SM-2 algorithm support with ease_factor and interval_days
   - Indexes: video, type, next_review, quality, priority, tags

3. **kb_notifications** - Notification tracking
   - Fields: notification_type, title, message, channel, status, delivered_at, metadata (JSONB)
   - Types: video_processed, insight_reminder, weekly_digest, daily_insight, custom
   - Indexes: video, insight, type, status, scheduled, metadata

4. **kb_weekly_digests** - Weekly digest tracking
   - Fields: week_start_date, week_end_date, total_videos, total_insights, top_insights_json (JSONB)
   - Breakdown: ai_tools_count, sports_count
   - Unique constraint: (week_start_date, week_end_date)

**Views Created**:
- `v_videos_pending_notification` - Videos ready for notification
- `v_insights_due_for_review` - Insights due for spaced repetition
- `v_current_week_summary` - Current week stats with aggregations

**Triggers**:
- Auto-update `updated_at` timestamp on all tables

**Deployment**:
- Workflow: "Deploy Knowledge Base Schema" (ID: `uijV1yACzz39SS1l`)
- Status: ✅ Executed successfully
- Result: All 4 tables, 3 views, and triggers deployed

---

## 🔄 n8n Workflows Created

### Workflow 1: Store Video Insights
**ID**: `078JDpHZix14KAme`
**Trigger**: Webhook (POST `/video-processed`)
**Status**: Inactive (ready for testing)

**Flow**:
1. Receive video processing completion webhook
2. Store video metadata in `kb_videos`
3. Check for insights
4. Loop through insights and store in `kb_insights`
5. Create notification record in `kb_notifications`
6. Send Telegram notification via Python script
7. Mark video as notified
8. Update notification status to 'sent'
9. Return success response

**Webhook URL**: `https://n8n.vecia.fr/webhook/video-processed`

**Expected Payload**:
```json
{
  "video_id": "VIDEO_ID",
  "title": "Video Title",
  "channel_name": "Channel Name",
  "channel_id": "UC...",
  "url": "https://youtube.com/watch?v=...",
  "duration_seconds": 1234,
  "pipeline_type": "ai_tools",
  "tags": ["n8n", "automation"],
  "total_chunks": 17,
  "insights": [
    {
      "text": "Insight text here",
      "type": "tip",
      "context": "Additional context",
      "category": "n8n",
      "tags": ["workflow", "automation"],
      "timestamp_start": 120,
      "timestamp_end": 180,
      "quality_score": 0.85,
      "priority": "high",
      "actionable": true
    }
  ]
}
```

---

### Workflow 2: Weekly Digest Builder
**ID**: `4s7bVBIjmgMJ5D8o`
**Trigger**: Schedule (Every Sunday 8 PM)
**Status**: Inactive (ready for activation)

**Flow**:
1. Trigger every Sunday at 20:00
2. Query `v_current_week_summary` view
3. Check if videos exist
4. Get top 10 insights from the week
5. Create digest record in `kb_weekly_digests`
6. Format rich digest message with:
   - Weekly stats (videos, insights, breakdown)
   - Top 10 insights with quality scores
   - Video links with timestamps
7. Send via Telegram
8. Create notification record
9. Mark digest as sent

**Schedule**: Weekly on Sundays at 8 PM (server time)

---

### Workflow 3: Spaced Repetition System
**ID**: `ggTUxmThD47HwOzC`
**Trigger**: Schedule (Every day 9 AM)
**Status**: Inactive (ready for activation)

**Flow**:
1. Trigger daily at 09:00
2. Query `v_insights_due_for_review` view (limit 5)
3. Check if insights exist
4. Loop through each insight
5. Format reminder message with:
   - Insight text and type
   - Video title and timestamped link
   - Quality and priority metrics
   - Review count
6. Send Telegram reminder
7. Create notification record
8. Update spaced repetition metadata:
   - Increment repetition_count
   - Calculate new interval (1 → 3 → 7 → 14 → 30 → exponential)
   - Set next_review_date

**Spaced Repetition Schedule**:
- Review 1: Next day (1 day)
- Review 2: +3 days
- Review 3: +7 days
- Review 4: +14 days
- Review 5: +30 days
- Review 6+: Double interval each time

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Knowledge Base System                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
         ┌──────────────────────────────────────┐
         │   Video Processing Pipeline (Local)   │
         │  - Extract transcripts                │
         │  - Enhance with Claude Code           │
         │  - Analyze with agents                │
         │  - Generate insights                  │
         └──────────────────────────────────────┘
                                │
                                ▼ POST /webhook/video-processed
         ┌──────────────────────────────────────┐
         │    n8n: Store Video Insights         │
         │  - Store video metadata               │
         │  - Store insights                     │
         │  - Create notifications               │
         │  - Send immediate notification        │
         └──────────────────────────────────────┘
                                │
                                ▼
         ┌──────────────────────────────────────┐
         │   PostgreSQL Database (VPS)          │
         │  - kb_videos                          │
         │  - kb_insights                        │
         │  - kb_notifications                   │
         │  - kb_weekly_digests                  │
         └──────────────────────────────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         │                                              │
         ▼                                              ▼
┌─────────────────────┐                    ┌─────────────────────┐
│ n8n: Weekly Digest  │                    │ n8n: Spaced Rep     │
│ (Sundays 8 PM)      │                    │ (Daily 9 AM)        │
│ - Aggregate weekly  │                    │ - Get due insights  │
│ - Format summary    │                    │ - Send reminders    │
│ - Send digest       │                    │ - Update schedule   │
└─────────────────────┘                    └─────────────────────┘
         │                                              │
         └──────────────────────┬──────────────────────┘
                                ▼
                    ┌──────────────────────┐
                    │  Telegram Bot API     │
                    │  (notifications/)     │
                    └──────────────────────┘
                                │
                                ▼
                        [ Your Telegram ]
```

---

## 🔗 Integration Points

### From Processing Pipeline → n8n

**Option 1: Direct Webhook (Recommended)**
```bash
curl -X POST https://n8n.vecia.fr/webhook/video-processed \
  -H "Content-Type: application/json" \
  -d @analysis.json
```

**Option 2: Python Integration** (To be created)
```python
# notifications/src/core/db_logger.py
from db_logger import KnowledgeBaseLogger

logger = KnowledgeBaseLogger(webhook_url="https://n8n.vecia.fr/webhook/video-processed")
logger.store_video_insights(video_data, insights)
```

### From n8n → Telegram Notification System

**Current**: Execute Command node
```bash
cd /path/to/notifications && python3 scripts/send_notification.py \
  --video-id VIDEO_ID \
  --title "Title" \
  --url "URL"
```

**Future**: Direct Telegram node (optional)

---

## 📋 Next Steps

### Immediate (To Complete Integration)

1. **Update Notification Scripts**
   - Add database logging to `send_notification.py`
   - Track notification delivery in `kb_notifications`
   - Update status on success/failure

2. **Create Database Logger Module**
   - File: `notifications/src/core/db_logger.py`
   - Methods:
     - `store_video()` - Insert video metadata
     - `store_insights()` - Bulk insert insights
     - `log_notification()` - Track notification sends
     - `get_pending_reviews()` - Query due insights

3. **Test Workflows**
   - Activate "Store Video Insights" workflow
   - Send test webhook with sample data
   - Verify database records
   - Check Telegram notification

4. **Update Processing Scripts**
   - Modify `store_in_mcp_kb.py` or `store_in_mcp_kb_v2.py`
   - Add webhook call after processing
   - Send video + insights JSON to n8n

5. **Create Documentation**
   - Workflow usage guide
   - Webhook payload schema
   - Database query examples
   - Troubleshooting guide

### Future Enhancements

- **Analytics Dashboard**: Query database for insights analytics
- **User Feedback**: Add rating system for insights
- **Smart Scheduling**: Adjust review intervals based on user engagement
- **Multi-channel**: Support email and webhook notifications
- **Batch Processing**: Handle multiple videos in one webhook call
- **API Endpoints**: Create REST API for mobile app access

---

## 🛠️ Configuration Files

### n8n Workflows (VPS)
- Deploy Knowledge Base Schema: `uijV1yACzz39SS1l`
- Store Video Insights: `078JDpHZix14KAme`
- Weekly Digest Builder: `4s7bVBIjmgMJ5D8o`
- Spaced Repetition System: `ggTUxmThD47HwOzC`

### Database Schema (Local)
- Schema file: `notifications/schema/knowledge_base.sql`
- Deployed to: `vecia_aidb:5433/aidb` (schema: `ai_kb`)

### Notification System (Local)
- Base directory: `notifications/`
- Core modules: `notifications/src/core/`
- Scripts: `notifications/scripts/`
- Config: `notifications/config/config.yaml`

---

## 📚 Key Queries

### Get Videos Needing Notification
```sql
SELECT * FROM ai_kb.v_videos_pending_notification;
```

### Get Today's Review Insights
```sql
SELECT * FROM ai_kb.v_insights_due_for_review LIMIT 5;
```

### Get Current Week Summary
```sql
SELECT * FROM ai_kb.v_current_week_summary;
```

### Get All Notifications for a Video
```sql
SELECT * FROM ai_kb.kb_notifications
WHERE video_id = 'VIDEO_ID'
ORDER BY created_at DESC;
```

### Get Insight Review History
```sql
SELECT
  i.insight_text,
  i.repetition_count,
  i.next_review_date,
  i.interval_days,
  COUNT(n.notification_id) as times_sent
FROM ai_kb.kb_insights i
LEFT JOIN ai_kb.kb_notifications n ON i.insight_id = n.insight_id
WHERE i.insight_id = 123
GROUP BY i.insight_id;
```

---

## 🎯 Success Metrics

**Current Status**:
- ✅ Database schema deployed (4 tables, 3 views)
- ✅ PostgreSQL connection working
- ✅ 3 automated workflows created
- ✅ Spaced repetition algorithm implemented
- ✅ Multi-pipeline support (AI tools + Sports)

**Ready for Testing**:
- Webhook integration
- Telegram notifications via workflows
- Weekly digest generation
- Daily insight reminders

**Pending**:
- Database logger module
- Notification script updates
- End-to-end testing
- Documentation

---

## 💡 Tips

1. **Testing Workflows**: Use n8n's "Test workflow" button with manual data first
2. **Monitoring**: Check n8n execution logs in the Executions tab
3. **Database Access**: Use `psql` or pgAdmin to query the database directly
4. **Debugging**: Enable `saveDataErrorExecution` in workflow settings (already enabled)
5. **Activation**: Activate workflows individually as you test them

---

## 📞 Support

For issues or questions:
- Check n8n execution logs: `https://n8n.vecia.fr/executions`
- Query database: `psql -h vecia_aidb -p 5433 -U ai_admin -d aidb`
- Review workflow: Open in n8n editor and check node configurations
- Test webhook: Use curl or Postman to send test payloads

---

**Last Updated**: 2025-10-20
**Created By**: Claude Code + n8n MCP Integration
