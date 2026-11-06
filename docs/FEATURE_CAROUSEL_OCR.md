# Feature: Carousel Image OCR (text extraction from shared image posts)

**Status**: Queued — needs BMAD discussion before build
**Queued**: 2026-07-30
**Area**: `vecia` (or `mutora` if the shared post is sports content — inherit the same area rule as the existing INSTAGRAM pipeline)
**Targets**: BOTH ingest surfaces (a shared carousel can arrive via either)
  - `media-pipeline` (Python agent) — `~/projects/media-pipeline`
  - `instagram-processor` (Slack bot, TS/Node) — `~/projects/instagram-processor`

## Problem

Both media surfaces assume every shared post is a **video/audio** job: download → (frames) →
transcribe. When an Instagram post is a **carousel of images** (Instagram "sidecar", 2–10 slides)
with no meaningful audio track, the pipeline produces nothing useful:

- **media-pipeline**: the `§2 Link Detection` table
  (`.claude/agents/media-ingestion-agent.md`) routes purely by URL host, never by media *type*.
  The INSTAGRAM branch (`§3b`) runs `yt-dlp -x --audio-format mp3` (audio-only), which yields no
  audio for an image carousel. Carousels are silently unsupported.
- **instagram-processor**: `processVideoAsync` (`src/slack/commands.ts:301`) is a fixed linear
  video sequence, and both yt-dlp calls pass `--no-playlist`
  (`src/processors/downloader.ts:97,110`), which **actively discards** every carousel slide after
  the first. There is no `media_type` column in the schema.

Neither system has any OCR today (`grep ocr|tesseract|carousel|sidecar` → zero hits in both repos).

## Desired behavior

When a shared Instagram post is detected as a **carousel of images (not a video)**:
1. Download all image slides (not just the first).
2. Run OCR over each slide to extract any embedded text.
3. Treat a text-free slide as a first-class "no text" result (do **not** hallucinate text).
4. Fan the extracted text out to the same storage/notification sinks as a transcript.

## Chosen approach: vision-LLM OCR (reuse Claude)

Decision (2026-07-30): use a **vision LLM** for OCR rather than a dedicated OCR engine.
Rationale (from research, see `## Research summary` below): for text baked into stylized
social-media graphics (script fonts, text over photos, colored backgrounds), a vision LLM matches
or beats classic OCR, needs **no new dependency or cloud vendor**, and both surfaces already
(or easily can) call Claude. Cost at solo-dev volume is trivial (~$0.01–0.03/post at Sonnet
image-token rates; a fraction of a cent on Haiku/Gemini Flash).

**Mandatory guardrail — anti-hallucination prompt** (the one real risk of the LLM route):

> Transcribe only text that is actually visible in this image, verbatim. Do not guess, translate,
> paraphrase, or describe the image. If there is no text, output exactly `NO_TEXT`.

Emit results tagged by slide index (`slide 1..N`); treat `NO_TEXT`/empty as a valid result and
dedupe overlay text repeated across slides.

**Cost lever if volume grows**: route the OCR call to Claude Haiku or Gemini Flash (≈5× cheaper
image tokens) while the main agent stays on its normal model. Fall back to Google Cloud Vision
($1.50/1k images) or local PaddleOCR only if you ever need offline / a zero-hallucination
guarantee. Do **not** default to Tesseract for this content type (weakest on stylized text).

## Where it slots in

### media-pipeline (Python agent) — cleanest fit; agent has native vision
- Add a **carousel row** to the `§2 Link Detection` table
  (`.claude/agents/media-ingestion-agent.md`, table at `§2`) — branch on media *type*, not just host.
- Add a new **`§3c — Carousel / Image Pipeline`** section mirroring `§3b` (INSTAGRAM), but:
  - swap `yt-dlp -x` (audio) for an image download that keeps all sidecar nodes
    (drop `--no-playlist`, or use Instaloader `--slide` / gallery-dl for arbitrary shared posts);
  - swap the whisper transcription step for the vision-LLM OCR pass (the Claude Code agent can
    read the images natively — no external OCR call needed).
- Reuse **`§4 — Unified Storage Fan-out`** unchanged so OCR text lands in
  unified-memory / Notion / Neo4j / pgvector exactly like a transcript.

### instagram-processor (Slack bot) — real TS code
1. **Detect type** in `getVideoInfo` (`src/processors/downloader.ts`, `VideoInfo` interface at
   `downloader.ts:14`): yt-dlp `--dump-json` returns `_type: "playlist"` + `entries[]` for
   carousels — surface `mediaType: 'video' | 'carousel' | 'image'` on `VideoInfo`.
2. **Branch** in `processVideoAsync` right after the `getVideoInfo` call
   (`src/slack/commands.ts:314`): if `carousel`, skip the video steps (download/frames/transcribe)
   and take the image path.
3. **Add an image downloader** in `downloader.ts` that **drops `--no-playlist`**
   (`downloader.ts:97,110`) and pulls all `entries` images to `output/<requestId>/images/`.
4. **Add `src/processors/ocr.ts`** (new file, parallel to `transcriber.ts`) that sends each image
   to Claude vision with the anti-hallucination prompt above and returns per-slide text.
5. **Schema**: add `media_type` to `reels` (`src/database/schema.sql:4-20`) and an
   `ocr_text` column (or reuse `frames`/add `carousel_images`); wire helpers in `src/database/db.ts`.

## Open questions for BMAD

- **Type detection reliability**: is yt-dlp `_type: playlist` a robust carousel signal across
  instagram/tiktok/x, or do we need Instaloader/gallery-dl for the "arbitrary shared post" case
  (unauthenticated pulls get rate-limited/blocked — needs backoff + per-media-ID caching)?
- **Model routing**: OCR on Haiku/Flash vs. the agent's default model — one shared config knob?
- **Mixed posts**: a carousel that contains *both* images and a video slide — OCR images AND
  transcribe the video, or pick one?
- **Storage shape**: does downstream (search/embeddings) want per-slide records or one
  concatenated `ocr_text` blob per post? Dedupe repeated overlay text before embedding.
- **Notification**: reuse the transcript notification formatters, or a distinct "image post" format?

## Research summary (2026)

- Accuracy ranking for *text-in-graphics* input: **vision LLM ≈ Google Cloud Vision ≫ Tesseract**.
  Tesseract is strong only on clean digital-born text and falls apart on stylized/over-photo text.
- Vision LLMs' one weakness is **hallucinated text** on textless/noisy images — mitigated by the
  verbatim-only + `NO_TEXT` sentinel prompt above. Dedicated OCR models (PaddleOCR, Google Vision)
  don't hallucinate; keep one as a gate only if a hard guarantee is ever required.
- Carousel image retrieval: Meta Graph API `children` (owned accounts only); Instaloader
  (`--slide`), yt-dlp, or gallery-dl for arbitrary shared post URLs.
- Preprocessing (upscale to ~1000–1500px long edge) helps classic OCR; LLMs need little/none —
  send near-native resolution.

Full source list is in the research task output (unified-memory task for this feature).
