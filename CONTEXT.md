# media-pipeline — Current Context

## What this is
A personal knowledge ingestion pipeline. URLs (YouTube, Instagram) are sent via Telegram or CLI, processed through LLM analysis, and stored across 5 targets for retrieval by any agent.

## Current state
- **66+ videos processed** in `workspace/videos/` with human-readable folder names
- **Telegram pipeline**: Hermes gateway on gaming-PC (v0.14.0), needs config (Telegram disabled, bot token commented out, SOUL.md dispatch rules reference dead OpenClaw tools)
- **Mac CLI working**: `uv run python main.py streamlined "URL"` + Sonnet agent analysis
- **Summary generation**: Now LLM-written by the agent from analysis.json (replaced broken regex script `generate_detailed_summary.py`, archived 2026-05-24)
- **Unified-memory**: 40+ video memories stored, searchable via `memory_search`
- **QMD**: Full-text search over transcripts on gaming-PC (`media-pipeline` collection)
- **Neo4j graph extraction**: Disabled per V2 vision (will use neo4j-brain deterministic indexer)
- **Dead code cleanup done**: 5 deprecated scripts + 7 unused modules archived, n8n/OpenClaw refs removed

## What's blocked
- **Hermes media agent not configured** — Telegram disabled, no unified-memory plugin, SOUL.md needs media pipeline instructions (see plan Phase 3)
- Python scripts (`youtube_processor.py`, `auto_enhancer.py`) still write to project root instead of `workspace/videos/{folder}/` — agent moves files after extraction
- Instagram image posts (no audio) not supported yet
- faster-whisper upgrade pending: large-v3 → large-v3-turbo with VAD (see plan Phase 4)
- Phase 2 (spaced repetition) and Phase 3 (channel watching) not started

## What to read first
1. `.claude/agents/media-ingestion-agent.md` — the pipeline spec (canonical)
2. `workspace/index.json` — master registry of all processed videos
3. `.planning/ROADMAP.md` — 5-phase plan

## Inputs
- Reference (L3): `docs/DUAL_PIPELINE_GUIDE.md`
- Working (L4): `.planning/ROADMAP.md`, `.planning/PROJECT.md`
- Memory: `memory_search("media pipeline", tags=["project:youtube-kb"])`

## Process
1. URL arrives (Telegram bot via Hermes, or Mac CLI)
2. Agent detects platform, routes to correct pipeline (AI Tools vs Sports)
3. Extract: yt-dlp captions (YouTube) or faster-whisper transcription (other platforms)
4. Enhance: auto_enhancer.py applies 174+ domain corrections
5. Analyze: LLM agent (Claude Code @youtube-transcript-analyzer or Hermes in-context) → analysis.json
6. Summarize: LLM agent writes summary.md from analysis.json (no Python script)
7. Store: `store_in_mcp_kb.py` → unified-memory API (auto-embeds in pgvector)
8. Output: `workspace/videos/{YYYYMMDD}--{ID}--{platform}--{channel}--{title}/`

## Key decisions (recent)
- 2026-05-24: Summary generation switched from regex script to LLM-written — `generate_detailed_summary.py` archived
- 2026-05-24: Dead code cleanup — 5 deprecated scripts, 7 unused modules archived, n8n/OpenClaw refs removed
- 2026-05-16: OpenClaw → Hermes migration on gaming-PC (Hermes v0.14.0, media agent config pending)
- 2026-04-14: Neo4j graph extraction OFF — V2 uses deterministic neo4j-brain indexer
- 2026-04-12: Workspace reorganized to per-video folders with human-readable names
- 2026-03-29: n8n removed
- 2026-03-29: Telegram chosen over WhatsApp for bidirectional intake + delivery
