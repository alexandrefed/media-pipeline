# Loom manual fallback

Use when a user asks to process a Loom share URL (`loom.com/share/<id>`) even though the normal yt-dlp/media pipeline does not list Loom as a first-class platform.

> **Origin**: Crystallized by the Hermes self-improvement Curator (2026-06-28). Ported into the repo 2026-08-02.

## Why this works

Public Loom pages often embed enough data in the page state to retrieve transcript/caption assets without downloading the video. The page exposes `window.__APOLLO_STATE__` with a `RegularUserVideo:<id>` object and a `VideoTranscriptDetails:<id>` object. When transcript sharing is enabled, the transcript details include signed `source_url` and `captions_source_url` fields.

## Procedure

1. Treat Loom as a manual fallback, not as unsupported.
2. Open the Loom URL in the browser if direct terminal fetching truncates or masks signed URLs.
3. In page JS, inspect Apollo state:

```js
(() => {
  const st = window.__APOLLO_STATE__;
  const out = {};
  for (const [k, v] of Object.entries(st || {})) {
    if (k.startsWith('RegularUserVideo:') || k.startsWith('VideoTranscriptDetails:')) out[k] = v;
  }
  return out;
})()
```

4. Extract metadata from `RegularUserVideo:<id>`:
   - `name` as title
   - owner reference/name if available
   - `createdAt`
   - `playable_duration` or `video_properties.durationMs`
   - original Loom share URL
5. Extract transcript from `VideoTranscriptDetails:<id>.source_url`:

```js
(async () => {
  const st = window.__APOLLO_STATE__;
  const t = Object.entries(st).find(([k]) => k.startsWith('VideoTranscriptDetails:'))[1];
  const r = await fetch(t.source_url);
  const txt = await r.text();
  return { status: r.status, ct: r.headers.get('content-type'), length: txt.length, text: txt.slice(0, 5000) };
})()
```

6. Save the full JSON from `source_url` locally as `transcript_loom_raw.json`.
7. Convert `phrases[]` into timestamped transcript text:
   - timestamp: `phrase.ts`
   - text: `phrase.value`
   - format: `[MM:SS] text`
8. Create a standard video folder under `workspace/videos/` using platform `loom`:

```text
{YYYYMMDD}--{VIDEO_ID}--loom--{CHANNEL_SLUG}--{TITLE_SLUG}/
├── metadata.json
├── transcript_loom_raw.json
├── transcript_raw.txt
├── transcript_enhanced.txt
├── analysis.json
└── summary.md
```

9. Analyze the enhanced transcript in-context using the normal `analysis.json` schema, then write `summary.md`.
10. Store with:

```bash
uv run python scripts/store_in_mcp_kb.py <video_folder>/analysis.json
```

11. Update `workspace/index.json` with `platform: "loom"`, `has_analysis`, `has_summary`, and `in_unified_memory`.

## Pitfalls

- Do not stop at "unsupported platform" when the user explicitly asks for a solution. Try the browser/Apollo transcript path first.
- Direct terminal requests to signed CDN URLs may 403 if the URL was truncated or stale. Use the browser page context to fetch `source_url` — it has the current signed URL and page/referrer context.
- Loom transcript JSON can be several MB because it includes word/range metadata. Keep `transcript_loom_raw.json`, but generate a clean timestamped `transcript_raw.txt` for analysis.
- If `source_url` is absent or transcript sharing is disabled, fall back to `captions_source_url` if present, then to HLS/audio download + Whisper if needed.
