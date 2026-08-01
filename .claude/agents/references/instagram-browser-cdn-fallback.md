# Instagram browser CDN audio fallback

Use when `uv run python main.py streamlined <instagram-url>` or direct `yt-dlp` metadata/caption extraction fails with Instagram API/auth/empty-media errors, but the public reel is visible in a browser.

> **Origin**: Crystallized by the Hermes self-improvement Curator on gaming-PC from repeated Instagram reel processing (first learned from reel `DYz5-rtovGj`, 2026-05-26; confirmed in production on `DavtYgRReBW`, 2026-07-14). Ported into the repo 2026-08-02 so the Mac/Claude Code path benefits too.

## Trigger signal

yt-dlp fails with:
```
WARNING: [Instagram] <id>: No csrf token set by Instagram API
ERROR: [Instagram] <id>: Instagram sent an empty media response...
```

**Critical:** a failed streamlined run may exit `0` while still printing this error and creating no video folder. Never assume success from exit code alone — verify with a targeted folder search:
```bash
find workspace/videos/ -maxdepth 1 -name "*--${VIDEO_ID}--*" -type d
```
If no folder/artifacts exist, continue with this fallback.

## Pattern

1. Open the Instagram reel in the browser and accept cookies if prompted.
2. Capture metadata from the page:
   - creator/channel from visible profile link and `og:title`
   - caption from visible post text and `og:description`
   - publish date from the visible date link
   - engagement from visible buttons if needed
3. Inspect browser resources for `.mp4` entries:
   ```js
   performance.getEntriesByType('resource')
     .map(e => e.name)
     .filter(n => n.includes('.mp4'))
   ```
4. Normalize candidate URLs by removing range-only params so the whole resource can be downloaded:
   ```js
   [...new Set(urls.map(u => {
     const url = new URL(u);
     url.searchParams.delete('bytestart');
     url.searchParams.delete('byteend');
     url.searchParams.delete('efg');
     return url.toString();
   }))]
   ```
5. Download candidates with `curl -L --fail -A 'Mozilla/5.0' '<url>' -o <file>.mp4`.
6. Probe each candidate with `ffprobe`:
   ```bash
   ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name -of compact <file>.mp4
   ```
   Instagram often exposes separate video-only and audio-only MP4 resources. For transcript extraction, use the `aac` / audio-only candidate.
7. Transcribe the audio-only candidate with faster-whisper and write `transcript_raw.txt`:
   ```python
   from faster_whisper import WhisperModel
   model = WhisperModel('large-v3-turbo', device='cuda', compute_type='int8')
   segments, info = model.transcribe(str(audio_file), vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
   text = '\n'.join(f'[{seg.start:0.2f} - {seg.end:0.2f}] {seg.text.strip()}' for seg in segments)
   ```
8. Continue the normal pipeline: auto-enhance, write `analysis.json`, write `summary.md`, run `scripts/store_in_mcp_kb.py`, and update `workspace/index.json`.

## One-pass browser probe (metadata + resources)

```js
(() => {
  const metas = [...document.querySelectorAll('meta')]
    .map(m => ({p: m.getAttribute('property') || m.getAttribute('name'), c: m.getAttribute('content')}))
    .filter(x => x.p && /title|description|image|video|url|site/.test(x.p));
  const mp4 = [...new Set(performance.getEntriesByType('resource')
    .map(e => e.name)
    .filter(n => n.includes('.mp4'))
    .map(u => { const url = new URL(u); ['bytestart','byteend','efg'].forEach(p => url.searchParams.delete(p)); return url.toString(); }))];
  return {title: document.title, metas, mp4, text: document.body.innerText.slice(0, 3000)};
})()
```

## Notes & gotchas

- The public page can still provide usable metadata even behind a sign-up/login prompt. After accepting cookies and closing/ignoring the prompt, inspect `og:title`, `og:description`, the visible profile link, caption text, likes/comments, and the canonical URL. Use the caption as metadata/context but still transcribe audio — the spoken reel may contain framing beyond the caption.
- If terminal `yt-dlp --cookies-from-browser firefox` still returns empty media, don't keep retrying cookies; use browser resources instead.
- Don't preserve `bytestart`/`byteend` params when downloading the whole file; those fetch ranges only.
- Use `ffprobe` to distinguish audio-only from video-only before transcription. Observed reels expose multiple H.264 video-only MP4s plus a smaller AAC audio-only MP4 — transcribe the AAC candidate (`codec_type=audio`, `codec_name=aac`), often the smallest/last.
- Download all normalized resources to `workspace/tmp/ig_<VIDEO_ID>/candidate_N.mp4`, probe, then pick the AAC candidate. Build the manual folder + `metadata.json` from browser metadata; don't wait for yt-dlp to create the folder after empty-media.
- When saving CDN URLs to `urls.txt`, ensure a trailing newline or use a Python downloader — a POSIX `while read` loop skips the final line without one. Verify candidate count matches discovered URL count before probing.
- Keep the standard folder naming: `{upload_date}--{video_id}--ig--{channel_slug}--{title_slug}`. Keep temporary candidates under `workspace/tmp/...` unless preserving media is intentional.
- `auto_enhancer` appends an `AUTO-ENHANCEMENT REPORT` footer. During in-context analysis, treat lines after that divider as processing metadata, not spoken content.
- Use the browser caption/metadata to correct obvious Whisper/domain-term errors (e.g. `Ake Accelerator` → `EIC Accelerator`, `red type` → `red tape`). Preserve the raw transcript but note corrections in `implementation_details.configuration` or `evidence_notes`.
- Instagram dates can disagree between fields (visible time vs `og:description`). Prefer explicit ISO dates; otherwise keep the best observed date and use the compact `upload_date` consistently for folder/index.
- For sports/fitness creators or captions, set `area: mutora` even on the manual fallback path.
- If a delegated ingestion times out, first search `workspace/videos/` and `workspace/index.json` for the video ID before re-dispatching; if no artifacts exist, continue manually from the browser/CDN fallback.
- `scripts/store_in_mcp_kb.py` expects `analysis.json.implementation_details` to be an **object/dict** (keys like `setup_steps`, `configuration`, `troubleshooting`, `evidence_notes`, `code_snippets`) — NOT a list of `{title, details}`. A list causes `AttributeError: 'list' object has no attribute 'get'` during storage.
