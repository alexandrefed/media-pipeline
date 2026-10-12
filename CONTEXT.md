# media-pipeline — Current Context

## What this is
A personal knowledge ingestion pipeline. URLs (YouTube, Instagram, X, Loom, Skool, gated webinars) arrive via Telegram or CLI, are transcribed and analysed by an LLM, and stored across five targets for retrieval by any agent.

## Direction
Folded into agentic-platform (Alexandre, 2026-08-22). Since 2026-10-04 the processed videos also feed skills: triage in `docs/research/2026-10-video-triage.md`, skills in `dev/platform/agentic-platform/skills/`.

## Where things are now
- Canonical video folders and the ledger `workspace/index.json` are on the gaming-PC (`/home/alexandre/projects/workflows/media-pipeline/workspace/`); the Mac copy is partial and not synced.
- Graph side (Neo4j brain): fix landed 8 Oct by the unified-memory session (f0ee463b); what is left on the video side (untitled Video nodes, graph_search not listing videos, stale links after edits) is with that session as its task abc5c245, report in `docs/reviews/2026-10-10-report-for-unified-memory.md`. Open here: empty YouTube twin folders for reels (ebdfe7a3).

## What to read first
1. `.claude/agents/media-ingestion-agent.md` — the pipeline spec
2. `docs/research/INDEX.md` — research, newest first
3. `.planning/ROADMAP.md` — phases and direction

## Process
URL → extract (yt-dlp captions or faster-whisper) → enhance (`src/processing/auto_enhancer.py`) → analyse (LLM → `analysis.json`) → summarise (`summary.md`) → store (`scripts/store_in_mcp_kb.py`) → stamp processed last (`src/pipeline/completion.py`).

History of this file: `docs/reviews/2026-10-08-context-before-trim.md` and git log.
