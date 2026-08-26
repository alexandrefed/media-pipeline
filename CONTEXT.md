# media-pipeline — Current Context

## What this is
A personal knowledge ingestion pipeline. URLs (YouTube, Instagram) are sent via Telegram or CLI, processed through LLM analysis, and stored across 5 targets for retrieval by any agent.

## Current state
- **128 videos on the gaming-PC corpus** (`~/projects/workflows/media-pipeline/workspace/videos/`
  — the LIVE one; the Mac repo's `workspace/videos/` is a stale fork, do not read a count from it).
  Reconciled 2026-08-23: **102 retrievable from the memory store** — the only number that answers
  what the pipeline is for — 108 with analysis, 98 with a summary, 84 complete on every stage.
  Regenerate with `python3 scripts/reconcile_ledger.py` (add `--write` to rewrite the ledger).
- **`processed_at` means every stage finished**, and is written LAST by
  `src/pipeline/completion.py`. It used to be stamped by step 1 of 4, which is how videos with a
  transcript and nothing else looked processed. The early stamp is now `transcript_extracted_at`;
  incomplete videos carry `incomplete_stages` instead of silence.
- **Hermes gateway running** on gaming-PC (v0.14.0): Telegram enabled, SOUL.md with media dispatch, unified-memory plugin built, media-pipeline SKILL.md seeded for self-improvement
- **Hermes self-improvement CONFIRMED in production**: Curator auto-crystallized fallback skills at `~/.hermes/skills/media/media-pipeline/references/` (now 8 files incl. per-case ones). The 5 general ones are now ALSO ported into the repo at `.claude/agents/references/` (2026-08-02) so the Mac/Claude Code path benefits.
- **yt-dlp updated** 2026.3.17 → 2026.7.4 on gaming-PC (uv tool + venv library); pyproject floor bumped to `>=2026.7.4`
- **Hermes CLI (`hermes -z`) verified E2E**: extract → enhance → analyze → summarize → store (5 videos processed successfully)
- **Mac CLI working**: `uv run python main.py streamlined "URL"` with fallback to yt-dlp+vtt_to_text.py
- **Summary generation**: LLM-written by agent from analysis.json (no regex script)
- **Auto-enhancer fixed**: word-boundary regex matching, 4 bad corrections removed (file→FAL, etc.)
- **Extraction fixed**: text_reconstructor.py duration filter removed (YouTube VTT format change), div-by-zero guarded
- **Video folder dedup**: reuses existing folder by video ID instead of creating duplicates
- **Unified-memory**: video memories stored. API runs on gaming-PC — tailnet `http://100.112.33.86:8085` or `http://127.0.0.1:8085` (NOT the old VPS `85.25.172.47`). `unified_memory_client.py` default is now the tailnet address.
- **QMD**: Vector + full-text search over transcripts, 150 collections, embeddings via embeddinggemma (Ollama)
- **Instagram image carousels supported** (2026-08-26): pictures-with-text posts. Each slide is read with the **vision model** — navigate `?img_index=N`, screenshot every slide, read verbatim. Do NOT scrape `<img alt>`: IG's alt is auto-OCR belonging to *other* images on the page (this silently stored a wrong 19→6-slide fabrication before it was caught and corrected). Assembled by `scripts/ig_carousel_to_transcript.py` (`content_type: image-carousel`, no auto_enhancer — clean typed text). Doc: `.claude/agents/references/instagram-image-carousel.md`. Verified E2E on `Db6qLt_CJdq` (19 slides, matched to rendered images, stored + retrievable).
- **Neo4j graph extraction**: Disabled per V2 vision

## What's blocked
- **Telegram E2E not yet tested** — Hermes gateway running, CLI path verified, awaiting first Telegram message test
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
- 2026-08-26: Added Instagram image-carousel capability. **Method = vision per slide** (navigate `?img_index=N`, screenshot, read). First attempt used an `<img alt>` browser probe and it silently stored a fabrication — a 19-slide Meta-ads carousel came out as 6 unrelated "AI + ecommerce" slides because the alt selector grabbed *other* posts' auto-OCR'd images. Caught when Alex sent the real slide 1-2. Rewrote the doc/script/spec around vision + a mandatory "match extracted text to the rendered slides before claiming success" verify step; deleted the 2 wrong memories and re-stored the correct 19 slides. New `scripts/ig_carousel_to_transcript.py` + `references/instagram-image-carousel.md`; agent §3b carousel gate. Carousels skip auto_enhancer (typed text, not ASR).
- 2026-08-23: `/clief update` — refreshed CLAUDE.md (added Research+decisions + Extraction-fallbacks routing rows, trimmed to 48 lines), created `docs/research/` + `docs/decisions/` with INDEX stubs, refreshed video count (127), noted unified-memory tailnet default, flagged stale `/alex/openclaw/videos/` namespace (kept as-is to avoid fragmentation)
- 2026-08-02: Ported Hermes' 5 learned fallback skills into repo `.claude/agents/references/`; added exit-0 verification guard + browser/CDN fallback pointers to `media-ingestion-agent.md` §3b + new §7; fixed `streamlined_process.py` youtu.be ID parsing (urlparse-based `extract_youtube_video_id`) + made failure paths exit non-zero; updated yt-dlp 2026.3.17→2026.7.4
- 2026-07-14: Confirmed Hermes self-improvement working — Instagram reel (DavtYgRReBW) recovered from yt-dlp empty-media/auth failure via crystallized browser/CDN audio fallback skill (learned from prior reel DYz5-rtovGj on 2026-05-26). 5 fallback skills now exist in Hermes skill library. Curator refusal-guard also observed working (won't blind-patch skills).
- 2026-06-01: CONTEXT.md updated — unified-memory on gaming-PC localhost:8085, all 5 videos stored, blocked items cleared
- 2026-05-25: Unified-memory API confirmed on gaming-PC localhost:8085 (not VPS) — fixed Hermes .env, pushed all 5 pending videos
- 2026-05-24: Auto-enhancer fixed — word-boundary regex, removed file→FAL/cat→Cat bad corrections
- 2026-05-24: VTT extraction fixed — removed broken `duration < 0.1` filter in text_reconstructor.py, added `vtt_to_text.py` utility, streamlined_process.py fallback path
- 2026-05-24: Video folder dedup — both youtube_processor.py and streamlined_process.py check `*--{VIDEO_ID}--*` before creating folders
- 2026-05-24: Hermes media agent configured — SOUL.md, AGENTS.md, unified-memory plugin, media-pipeline SKILL.md, Telegram enabled, gateway running
- 2026-05-24: Summary generation switched from regex script to LLM-written — `generate_detailed_summary.py` archived
- 2026-05-24: Dead code cleanup — 5 deprecated scripts, 7 unused modules archived, n8n/OpenClaw refs removed
- 2026-05-16: OpenClaw → Hermes migration on gaming-PC (Hermes v0.14.0)
- 2026-04-14: Neo4j graph extraction OFF — V2 uses deterministic neo4j-brain indexer
- 2026-04-12: Workspace reorganized to per-video folders with human-readable names
- 2026-03-29: n8n removed
- 2026-03-29: Telegram chosen over WhatsApp for bidirectional intake + delivery

---

## Direction (Alexandre, 2026-08-22)

Part of agentic-platform, per his own read — not a separate cockpit tab.

- **Cadence:** folded into agentic-platform
- **Next concrete step:** fold; no standalone session

_Captured from Alexandre's own per-project review. Full portfolio view:_ `dev/platform/unified-memory/docs/SESSION-DISPOSITION.md`
