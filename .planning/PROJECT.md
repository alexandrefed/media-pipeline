# media-pipeline

## What This Is

A continuous knowledge ingestion system for a single power user (Alexandre). Watches 15+ creator accounts across Instagram and YouTube, accepts on-demand URL submissions via a dedicated Telegram bot, processes content through domain-specific LLM agents, and stores LLM-post-processed knowledge across 5 targets (unified-memory, Obsidian, Notion, Neo4j, pgvector). OpenClaw on gaming-PC is the sole orchestrator — handling Telegram intake, processing dispatch, persistent cron scheduling, and notification delivery. No external orchestration layer required.

## Core Value

**Forward a URL from your phone → it becomes searchable, reviewable knowledge that any AI agent can surface at the right moment.** Zero friction in, zero effort out.

## Requirements

### Validated

- ✓ YouTube long-form transcript extraction via yt-dlp — existing
- ✓ Auto-enhancement with 174+ transcription corrections — existing
- ✓ AI Tools analysis via @youtube-transcript-analyzer — existing
- ✓ Sports analysis via @sports-transcript-analyzer — existing
- ✓ Unified-memory API storage (memories + notes) — existing, verified
- ✓ Neo4j entity extraction via GraphExtractionPipeline — existing, automatic
- ✓ pgvector embedding storage (768-dim nomic-embed-text) — existing
- ✓ Notion note sync via unified-memory heartbeat — existing
- ✓ Obsidian .md visibility via Mutagen sync (gaming-PC → Mac) — existing
- ✓ CLI intake via `uv run python main.py streamlined <URL>` — existing

### Active

- [ ] Telegram intake via OpenClaw (enable stock plugin, configure routing)
- [ ] Instagram Reel extraction via yt-dlp + Whisper on gaming-PC
- [ ] Short-form processing mode (1 note vs 5-7 memories for <2 min content)
- [ ] Actionability tagging (actionable/reference/awareness classification)
- [ ] Telegram confirmation reply with summary after processing
- [ ] Daily spaced repetition via OpenClaw Gateway persistent cron (9 AM)
- [ ] Weekly synthesis digest via Gateway cron (Sunday 8 PM)
- [ ] Spaced repetition feedback via Telegram inline buttons (Done/Not Relevant/Remind Later)
- [ ] YouTube channel RSS polling (6 channels, every 4h, Gateway cron)
- [ ] Instagram account polling via instaloader (9 accounts, every 6h, burner account)
- [ ] Deduplication (check unified-memory before processing)
- [ ] Watchlist management via Telegram commands (watch/unwatch/watchlist)
- [ ] Cookie pre-flight health check (every 12h, proactive Telegram alert)
- [ ] Processing observability logging in unified-memory
- [ ] Telegram security whitelisting
- [ ] Pipeline config externalization (pipeline-config.yaml)
- [ ] Workflow template documentation (Inputs → Pipe → Outputs pattern)

### Out of Scope

- Multi-user support — single user system, no auth/tenancy needed
- Podcast/RSS ingestion — future vision, not MVP
- Article/thread ingestion (Twitter, blogs) — future vision
- Voice query via Telegram — future vision
- n8n orchestration — replaced by OpenClaw Gateway crons (researched and confirmed: persistent, disk-backed, survives restarts)
- Accountability workflow — separate project at workflows/accountability/ (seed doc created)
- Project cross-referencing in spaced repetition — belongs to accountability workflow

## Context

**Infrastructure (3 machines):**
- **Mac**: Development, Obsidian vault (iCloud + Mutagen sync), Claude Code sessions
- **Gaming-PC**: OpenClaw gateway (systemd, auto-restart), media processing, GPU (Whisper), yt-dlp, Firefox cookies for Instagram/Vimeo
- **VPS**: unified-memory API (port 8085), Neo4j (bolt://vecia_neo4j:7687), PostgreSQL 16 + pgvector, CouchDB LiveSync

**Sync architecture:**
- Mutagen: `workflows/` bidirectional real-time sync (Mac ↔ gaming-PC), ignores `.git` and `.claude/`
- CouchDB LiveSync: Obsidian vaults (Mac ↔ iPhone via VPS)
- Git: code transport, `.claude/` directory updates require push/pull

**OpenClaw capabilities (verified via research):**
- Telegram stock plugin: exists, supports inline keyboards + callback_query forwarding
- Gateway cron: persistent (jobs.json on disk), survives restarts, standard cron expressions + intervals
- 9 agents configured, media agent needs bootstrap (TOOLS.md/IDENTITY.md empty)

**Gaming-PC environment issues (from SSH research 2026-03-28):**
- Media agent path stale: points to `~/ai-knowledge-base/AI-Knowledge-Base-PRD` (should be `~/projects/workflows/media-pipeline/`)
- `.env` missing at new path
- yt-dlp outdated (v2024.04.09)
- Whisper not installed (no local-whisper, no faster-whisper, no openai-whisper)
- `.claude/` not synced via Mutagen — agent updates need git

**Instagram polling (from research 2026-03-28):**
- yt-dlp cannot list Instagram profiles (broken since 2022, confirmed by maintainers)
- instaloader v4.15 works with login, 200 req/hour limit, burner account recommended
- Apify free tier ($5/mo) as commercial fallback
- Post URL format: `https://instagram.com/reel/{shortcode}/`

**BMAD artifacts:**
- PRD: `_bmad-output/planning-artifacts/prd.md`
- Epics: `_bmad-output/planning-artifacts/epics.md` (5 epics, 16 stories, validated)
- Downstream: `workflows/accountability/PRODUCT-SEED.md`

## Constraints

- **Platform**: OpenClaw orchestrates everything — no n8n for scheduling (Gateway crons are persistent and sufficient)
- **Single machine processing**: All extraction + Whisper runs on gaming-PC (GPU). VPS is storage only.
- **Instagram auth**: Requires burner account for instaloader. Cookie refresh is manual (Firefox on gaming-PC).
- **Mutagen ignores .claude/**: Agent definition updates require explicit git push/pull between Mac and gaming-PC.
- **Content volume**: ~70-80 pieces/week at full capacity (9-12 reels/day + YouTube every other day)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| OpenClaw as sole orchestrator (no n8n) | Gateway crons are persistent (jobs.json, systemd). Telegram plugin native. Eliminates external dependency. | — Pending |
| Telegram for intake + delivery (not WhatsApp) | Bidirectional: URLs in, summaries + reminders out. WhatsApp was overloading orchestrator with inline transcription. | — Pending |
| Instaloader for Instagram polling (not yt-dlp) | yt-dlp instagram:user extractor broken since 2022. Instaloader maintained (v4.15), works with login. | — Pending |
| Short-form = 1 note, long-form = 5-7 memories | Proportional processing. A 60s reel doesn't need the same extraction depth as a 45min tutorial. | — Pending |
| Actionability tagging (not project cross-referencing) | Media pipeline tags content. Accountability workflow (separate) cross-references with projects. Clean separation. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-29 after GSD initialization*
