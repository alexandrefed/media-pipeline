# media-pipeline

Continuous knowledge ingestion system. Forward a URL from your phone → it becomes searchable knowledge any agent can surface. Processes YouTube, Instagram, Vimeo, TikTok via Telegram bot or CLI.

## Area
Vecia

## Tech Stack
Python 3.11+ / uv, yt-dlp, faster-whisper (GPU on gaming-PC), unified-memory API, QMD, Neo4j, pgvector

## Commands
```bash
uv sync                                    # Install dependencies
uv run python main.py streamlined "URL"    # Process a YouTube video (Mac)
uv run python main.py extract "URL"        # Extract transcript only
```

## Routing Table

| Task | Go to | Read first |
|------|-------|-----------|
| Process a video (Mac) | Use @media-ingestion-agent | `.claude/agents/media-ingestion-agent.md` |
| Going deeper on an already processed video (full transcript, check each claim against a primary source, one dated verdict note) | the `video-deeper` skill | ~/.claude/skills/video-deeper/SKILL.md |
| Process via Telegram | Send URL to @vecia_media_pipeline_bot | Gaming-PC Hermes handles automatically |
| Pipeline architecture | `.claude/agents/` | `media-ingestion-agent.md` (the spec) |
| Extraction fallbacks (IG/X/Loom) | `.claude/agents/references/` | `*-fallback.md` |
| Dual pipeline routing | `docs/` | `DUAL_PIPELINE_GUIDE.md` |
| Research + decisions | `docs/research/` + `docs/decisions/` | `INDEX.md` first |
| Planning / roadmap | `.planning/` | `ROADMAP.md`, `PROJECT.md` |
| Source code / scripts | `src/`, `scripts/` | `streamlined_process.py`, `store_in_mcp_kb.py` |
| Ledger truth / "is it actually retrievable?" | `scripts/reconcile_ledger.py` | run it — file presence is not ingestion |
| What "processed" means (stage gate) | `src/pipeline/completion.py` | full docstring — the stamp is written LAST or it is a lie |

## Video Folder Convention

All processed content lives in `workspace/videos/` with this naming:
```
{YYYYMMDD}--{VIDEO_ID}--{PLATFORM}--{CHANNEL_SLUG}--{TITLE_SLUG}/
├── metadata.json, transcript_raw.txt, transcript_enhanced.txt
├── analysis.json (or analysis_sports.json), summary.md
```
- Platform: `yt`, `ig`, `vm`, `tt`, `x`, `local`
- Lookup: `find workspace/videos/ -maxdepth 1 -name "*--{ID}--*"`
- Index: `workspace/index.json`

## Storage Targets (per video)
Filesystem (`workspace/videos/`, Mutagen-synced) · unified-memory pgvector (gaming-PC `100.112.33.86:8085`) · QMD full-text (`media-pipeline` collection) · Notion (via unified-memory) · Neo4j (disabled per V2).

## Conventions
- Package manager: uv (never pip). No n8n — Hermes gateway handles Telegram intake.
- `.claude/` not synced via Mutagen — push agent updates via `scp` to gaming-PC (`ssh gaming-pc`).
