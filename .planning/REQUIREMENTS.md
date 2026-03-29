# Requirements: media-pipeline

**Defined:** 2026-03-29
**Core Value:** Forward a URL from your phone → it becomes searchable, reviewable knowledge that any AI agent can surface at the right moment.

## v1 Requirements

### Intake

- [ ] **INTAKE-01**: User can send URL to Telegram bot and system detects content platform (YouTube, Instagram, TikTok, Vimeo, X)
- [ ] **INTAKE-02**: System acknowledges URL receipt via Telegram within 5 seconds
- [ ] **INTAKE-03**: OpenClaw orchestrator routes URLs to media-ingestion-agent without inline processing
- [ ] **INTAKE-04**: System detects duplicate URLs by checking unified-memory before processing
- [ ] **INTAKE-05**: CLI intake works via `uv run python main.py streamlined <URL>` (existing, verify)

### Extraction

- [ ] **EXTRACT-01**: System extracts transcripts from YouTube videos via yt-dlp
- [ ] **EXTRACT-02**: System extracts audio from Instagram Reels via yt-dlp + Whisper (browser cookies)
- [ ] **EXTRACT-03**: System extracts audio from TikTok, X videos, YouTube Shorts via Whisper pipeline
- [ ] **EXTRACT-04**: System extracts transcripts from Vimeo via yt-dlp with Firefox cookies
- [ ] **EXTRACT-05**: System applies 174+ auto-corrections to transcripts
- [ ] **EXTRACT-06**: Cookie pre-flight health check runs every 12h with proactive Telegram alert on auth decay

### Processing

- [ ] **PROC-01**: System classifies content by duration: short-form (<2 min) vs long-form (>2 min)
- [ ] **PROC-02**: Short-form content produces 1 structured note (key insight, tools, actionable items, summary)
- [ ] **PROC-03**: Long-form AI Tools content produces 5-7 entity memories via @youtube-transcript-analyzer
- [ ] **PROC-04**: Long-form Sports content produces protocol + evidence + biomechanics analysis
- [ ] **PROC-05**: System generates clean .md summary for every processed piece of content
- [ ] **PROC-06**: System auto-detects content domain (AI Tools vs Sports) based on channel + title keywords
- [ ] **PROC-07**: Analysis agents classify each takeaway as actionable/reference/awareness

### Storage

- [ ] **STORE-01**: Memories stored in unified-memory API with required tags (source, project, type, area, video, channel, content-type)
- [ ] **STORE-02**: Notion note created per video via unified-memory note_create
- [ ] **STORE-03**: .md summary written to workspace/summaries/ (Mutagen-synced to Mac)
- [ ] **STORE-04**: Neo4j entity extraction triggered automatically via GraphExtractionPipeline
- [ ] **STORE-05**: Embedded chunks stored in VPS pgvector via unified-memory API
- [ ] **STORE-06**: Actionable items tagged with spaced-repetition metadata

### Delivery

- [ ] **DELIVER-01**: Telegram confirmation with compact summary after processing completes
- [ ] **DELIVER-02**: Daily spaced repetition reminders at 9 AM for due actionable items (Gateway cron)
- [ ] **DELIVER-03**: Weekly synthesis digest Sunday 8 PM with cross-content patterns (Gateway cron)
- [ ] **DELIVER-04**: User can mark spaced repetition items as done/not-relevant via Telegram inline buttons

### Watching

- [ ] **WATCH-01**: OpenClaw cron polls 9 Instagram accounts for new posts every 6 hours (instaloader)
- [ ] **WATCH-02**: OpenClaw cron polls 6 YouTube channels via RSS every 4 hours
- [ ] **WATCH-03**: New content queued for processing with deduplication
- [ ] **WATCH-04**: User can add/remove watched accounts via Telegram commands

### Operations

- [ ] **OPS-01**: Processing observability — every URL logged in unified-memory with status
- [ ] **OPS-02**: Processing failures generate Telegram notification with error context
- [ ] **OPS-03**: Telegram bot only accepts messages from whitelisted user ID

### Template

- [ ] **TMPL-01**: Pipeline follows Inputs → Pipe → Outputs pattern
- [ ] **TMPL-02**: Each pipeline stage independently replaceable
- [ ] **TMPL-03**: Configuration externalized in pipeline-config.yaml

## v2 Requirements

### Expanded Intake

- **V2-INTAKE-01**: Notion Video Inbox (add URL to Notion database, webhook triggers processing)
- **V2-INTAKE-02**: Podcast/RSS feed ingestion

### Enhanced Delivery

- **V2-DELIVER-01**: Adaptive spaced repetition (adjusts intervals based on feedback patterns)
- **V2-DELIVER-02**: Notion dashboard with visual overview of processed content and pipeline status

### Content Expansion

- **V2-CONTENT-01**: Article/thread ingestion (Twitter threads, blog posts, newsletters)
- **V2-CONTENT-02**: Knowledge graph queries via Telegram ("What tools does @hormozi recommend?")
- **V2-CONTENT-03**: Voice query — ask Telegram bot a question, get KB answer via voice note

## Out of Scope

| Feature | Reason |
|---------|--------|
| Multi-user support | Single user system, no auth/tenancy complexity |
| n8n orchestration | Replaced by OpenClaw Gateway crons (persistent, disk-backed, verified) |
| Project cross-referencing in spaced repetition | Belongs to accountability workflow (separate project) |
| Mobile app | Telegram + Obsidian on phone covers mobile use case |
| Workflow template marketplace | Future vision, not v1 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INTAKE-01 | Phase 1 | Pending |
| INTAKE-02 | Phase 1 | Pending |
| INTAKE-03 | Phase 1 | Pending |
| INTAKE-04 | Phase 3 | Pending |
| INTAKE-05 | Phase 4 | Pending |
| EXTRACT-01 | Phase 1 | Pending |
| EXTRACT-02 | Phase 1 | Pending |
| EXTRACT-03 | Phase 1 | Pending |
| EXTRACT-04 | Phase 1 | Pending |
| EXTRACT-05 | Phase 1 | Pending |
| EXTRACT-06 | Phase 4 | Pending |
| PROC-01 | Phase 1 | Pending |
| PROC-02 | Phase 1 | Pending |
| PROC-03 | Phase 1 | Pending |
| PROC-04 | Phase 1 | Pending |
| PROC-05 | Phase 1 | Pending |
| PROC-06 | Phase 1 | Pending |
| PROC-07 | Phase 1 | Pending |
| STORE-01 | Phase 1 | Pending |
| STORE-02 | Phase 1 | Pending |
| STORE-03 | Phase 1 | Pending |
| STORE-04 | Phase 1 | Pending |
| STORE-05 | Phase 1 | Pending |
| STORE-06 | Phase 1 | Pending |
| DELIVER-01 | Phase 1 | Pending |
| DELIVER-02 | Phase 2 | Pending |
| DELIVER-03 | Phase 2 | Pending |
| DELIVER-04 | Phase 2 | Pending |
| WATCH-01 | Phase 3 | Pending |
| WATCH-02 | Phase 3 | Pending |
| WATCH-03 | Phase 3 | Pending |
| WATCH-04 | Phase 3 | Pending |
| OPS-01 | Phase 4 | Pending |
| OPS-02 | Phase 4 | Pending |
| OPS-03 | Phase 4 | Pending |
| TMPL-01 | Phase 5 | Pending |
| TMPL-02 | Phase 5 | Pending |
| TMPL-03 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 38 total
- Mapped to phases: 38
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-29*
*Last updated: 2026-03-29 after GSD initialization*
