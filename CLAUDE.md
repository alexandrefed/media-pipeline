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
| Process via Telegram | Send URL to @vecia_media_pipeline_bot | Gaming-PC handles automatically |
| Pipeline architecture | `.claude/agents/` | `media-ingestion-agent.md` (the spec) |
| Dual pipeline routing | `docs/` | `DUAL_PIPELINE_GUIDE.md` |
| Planning / roadmap | `.planning/` | `ROADMAP.md`, `PROJECT.md` |
| BMAD artifacts | `_bmad-output/planning-artifacts/` | `prd.md`, `epics.md` |
| Legacy / old workflows | `archive/` | Don't read unless investigating history |
| Source code | `src/` | `pipeline/`, `processing/` |
| Scripts | `scripts/` | `streamlined_process.py`, `store_in_mcp_kb.py` |

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
1. **Filesystem**: `workspace/videos/{folder}/` (Mac + gaming-PC via Mutagen)
2. **Unified-memory**: pgvector semantic search (`/shared/projects/youtube-kb/`)
3. **QMD**: Full-text search on gaming-PC (`media-pipeline` collection)
4. **Notion**: Notes synced via unified-memory heartbeat
5. **Neo4j**: Graph extraction (currently disabled per V2 vision)

## Conventions
- Package manager: uv (never pip)
- No n8n — Hermes gateway on gaming-PC handles Telegram intake
- `.claude/` not synced via Mutagen — push agent updates via `scp` to gaming-PC
- Gaming-PC SSH: `ssh gaming-pc`
