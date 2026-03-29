# Phase 1: Telegram Intake & End-to-End Pipeline Wiring - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning
**Source:** PRD Express Path (_bmad-output/planning-artifacts/epics.md — Epic 1)

<domain>
## Phase Boundary

Wire the existing media processing pipeline to Telegram intake via OpenClaw. Most components already exist (extraction, processing, storage). The work is: enable Telegram plugin, fix media agent environment on gaming-PC, configure OpenClaw routing, add short-form processing mode, add actionability tagging, verify all 5 storage targets, and send Telegram confirmation. This is primarily a WIRING job, not a build-from-scratch job.

**What exists:** YouTube extraction (yt-dlp), Instagram extraction (yt-dlp + Whisper when working), auto-enhancement (174+ corrections), AI Tools analyzer, Sports analyzer, unified-memory storage, Notion notes, Neo4j graph extraction, pgvector embeddings, .md summary generation, Obsidian visibility via Mutagen sync.

**What's new:** Telegram plugin enable, OpenClaw URL routing, short-form processing mode (<2 min → 1 note), actionability tagging (actionable/reference/awareness), Telegram confirmation reply.

**What's broken on gaming-PC:** Agent path stale (points to ~/ai-knowledge-base/), .env missing at new path, yt-dlp outdated (v2024.04.09), Whisper not installed, workspace-media never bootstrapped (TOOLS.md/IDENTITY.md empty).

</domain>

<decisions>
## Implementation Decisions

### Telegram Plugin Setup
- Enable OpenClaw stock Telegram plugin: `openclaw channels add --channel telegram --token <BOT_TOKEN>`
- Add "telegram" to plugins.allow in openclaw.json
- Configure `telegram.capabilities.inlineButtons: "dm"` for future button callbacks
- Configure DM allowlist policy (only accept from Alexandre's Telegram user ID)

### URL Detection & Routing
- OpenClaw orchestrator detects URL patterns: youtube.com, instagram.com, vimeo.com, tiktok.com, x.com
- Dispatches to media-ingestion-agent with URL + detected platform
- Replies "Processing: [URL] ([platform detected])" within 5 seconds
- Unsupported URLs get reply: "Unsupported platform. Supported: YouTube, Instagram, TikTok, Vimeo, X"
- Non-URL messages handled normally by orchestrator

### Media Agent Environment Fix
- Update media-ingestion-agent.md default path: `~/ai-knowledge-base/AI-Knowledge-Base-PRD` → `~/projects/workflows/media-pipeline/`
- Create `.env` at new path from `.env.example` (MEMORY_BASE_URL, MEMORY_TOKEN, MEMORY_AGENT_ID)
- Update yt-dlp to latest version
- Install faster-whisper or openai-whisper for audio transcription
- Bootstrap OpenClaw workspace-media (populate TOOLS.md, IDENTITY.md)
- Note: `.claude/` not synced via Mutagen — agent updates need git push/pull

### Short-Form Processing
- Content <2 min classified as short-form
- Produces 1 structured note: key insight, tools mentioned, actionable items, 1-paragraph summary
- Tagged `content-type:short-form`
- Uses compact .md template (not the 20-section long-form template)

### Actionability Tagging
- Every takeaway classified: `actionable` | `reference` | `awareness`
- Stored as tag in unified-memory: `takeaway-type:actionable`
- Actionable items additionally tagged `spaced-repetition:pending`
- This enables downstream consumption by accountability workflow

### Storage Fan-Out (5 targets — all existing, verify wiring)
- unified-memory: memories with tags (source, project, type, area, video, channel, content-type)
- Notion: note per video via `note_create` with title format `{YEAR}-{MON}-Video-{SLUG}`
- Obsidian: .md summary in `workspace/summaries/` (Mutagen auto-syncs to Mac)
- Neo4j: automatic via GraphExtractionPipeline on memory_store
- pgvector: auto-embedded on store via unified-memory API

### Telegram Confirmation
- After processing + storage complete, send Telegram message: title, channel, pipeline type, key insight, memory count, Obsidian path
- On failure: error message + suggested fix (e.g., "cookies expired, refresh Firefox")

### Claude's Discretion
- How to structure the orchestrator's URL detection (regex vs agent prompt)
- Whether to update the media-ingestion-agent.md in-place or create a v2
- How to test the integration (manual test script vs automated)
- Error handling strategy for partial storage failures

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Agent Specs
- `.claude/agents/media-ingestion-agent.md` — Current agent spec (needs path updates)
- `.claude/agents/youtube-transcript-analyzer.md` — AI Tools analyzer
- `.claude/agents/sports-transcript-analyzer.md` — Sports analyzer

### Processing Pipeline
- `src/storage/unified_memory_client.py` — HTTP client for unified-memory API
- `scripts/store_in_mcp_kb.py` — AI Tools storage script (5-7 memories)
- `scripts/store_sports_in_mcp_kb.py` — Sports storage script
- `scripts/generate_detailed_summary.py` — Summary generation
- `src/processing/auto_enhancer.py` — 174+ corrections

### Configuration
- `.env.example` — Environment variables template
- `CLAUDE.md` — Project guide with GSD workflow

### Infrastructure
- `infrastructure/doc/sync-architecture.md` — Mutagen, git sync between Mac and gaming-PC

### BMAD Artifacts
- `_bmad-output/planning-artifacts/prd.md` — Full PRD
- `_bmad-output/planning-artifacts/epics.md` — Epic 1 stories with acceptance criteria

</canonical_refs>

<specifics>
## Specific Ideas

- The OpenClaw Telegram plugin supports inline keyboards + callback_query forwarding (verified via source code research). callback_data is forwarded to agent as synthetic user message.
- Mutagen ignores `.claude/` — agent definition changes on Mac don't auto-sync to gaming-PC
- Gaming-PC has 3 stale repo copies at `~/ai-knowledge-base/` — don't touch, just update paths to Mutagen-synced location
- Instagram extraction already works when triggered manually via OpenClaw — this is about correct wiring, not building extraction

</specifics>

<deferred>
## Deferred Ideas

- Spaced repetition delivery (Phase 2)
- Weekly digest (Phase 2)
- Creator cron watching (Phase 3)
- Cookie health checks (Phase 4)
- Config externalization (Phase 5)

</deferred>

---

*Phase: 01-telegram-intake-end-to-end-pipeline-wiring*
*Context gathered: 2026-03-29 via PRD Express Path*
