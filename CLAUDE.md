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
| **How code runs, lints and builds here** (uv, lint, .mjs, library docs) | `~/Desktop/ClaudeMCP/dev/platform/unified-memory/docs/code-housekeeping.md` | `uv run ruff check src/` (the CI scope; the whole tree has 2010 findings) |
| Process a video (Mac) | Use @media-ingestion-agent | `.claude/agents/media-ingestion-agent.md` |
| Going deeper on an already processed video (full transcript, check each claim against a primary source, one dated verdict note) | the `video-deeper` skill | ~/.claude/skills/video-deeper/SKILL.md |
| Process via Telegram | Send URL to @vecia_media_pipeline_bot | Gaming-PC Hermes handles automatically |
| Pipeline architecture | `.claude/agents/` | `media-ingestion-agent.md` (the spec) |
| Extraction fallbacks (IG/X/Loom) | `.claude/agents/references/` | `*-fallback.md` |
| Dual pipeline routing | `docs/` | `DUAL_PIPELINE_GUIDE.md` |
| Research + decisions | `docs/research/` + `docs/decisions/` | `INDEX.md` first |
| Planning / roadmap | `.planning/` | `ROADMAP.md`, `PROJECT.md` |
| Source code / scripts | `src/`, `scripts/` | `streamlined_process.py`, `store_in_mcp_kb.py` |
| Database setup SQL | `deployment/sql/` | the file you need |
| Usage examples | `examples/` | `basic_usage.py` |
| Enhancer corrections dictionary + processing history | `learning/` | `processing_knowledge_base.json` |
| Old guides and session notes (parked) | `archive/` | the file you need |
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
Filesystem (`workspace/videos/`: canonical copy on the gaming-PC at `/home/alexandre/projects/workflows/media-pipeline/workspace/videos/`, the ledger `workspace/index.json` lives there too; the Mac copy is partial and NOT synced, no Mutagen session covers it, so copy a Mac-built folder over with `rsync`) · unified-memory pgvector (gaming-PC `100.112.33.86:8085`) · QMD full-text (`media-pipeline` collection) · Notion (via unified-memory) · Neo4j brain graph (extraction ON since 2026-07-13; per-writer split and duplicates being fixed in unified-memory task 46b4c5d8).

## Conventions
- Package manager: uv (never pip). No n8n — Hermes gateway handles Telegram intake.
- Two copies on the gaming-PC, neither synced from the Mac: `~/projects/media-pipeline/` is a git clone of this repo (pull to update; it holds `.claude/agents/`), and `~/projects/workflows/media-pipeline/` is the NON-git working copy Hermes runs (code, `.env`, `workspace/`), so a code change reaches it only by copying the changed files over with `rsync`/`scp` after a `diff`. Hermes follows its own instructions in `~/.hermes/skills/media/media-pipeline/`, not `.claude/agents/`.
- Memory writes on the Mac need no key by hand: the client reads the keychain item `mcp-api/gateway-token` and sends it as `claude-main`; the box uses `~/.config/unified-memory/token`. Sections over 5,000 characters are stored in parts, and the memory service then adds facts it derives from them under the same `video:<id>` tag, so a tag count is several times the sections written.
