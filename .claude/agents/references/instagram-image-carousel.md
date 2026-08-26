# Instagram image carousel (pictures with text)

Use when the URL is an Instagram **image** post or carousel (`instagram.com/p/<shortcode>`)
made of picture slides — often text-graphics — with **no video/audio to transcribe**. This is
the counterpart to `instagram-browser-cdn-fallback.md`, which handles *reels* (video → audio →
Whisper). Added 2026-08-26 to close the "Instagram image posts not supported yet" gap.

## Key insight (validated on `Db6qLt_CJdq`)

Instagram renders each carousel slide as an `<img>` whose **`alt` attribute contains the
slide's full text** (the accessibility text). For text-graphic carousels this IS the creator's
per-slide copy — complete, in order, no OCR needed. The public post page loads this without a
login wall. So the primary extraction is a browser JS probe of `img alt`, NOT an image
download.

**When alt is not enough** — a slide that is a photo (not a text graphic) gets an
auto-generated alt like *"may be an image of one person"* / *"photo of"*. Detect these and fall
back to **vision** on that slide (screenshot in the browser, or download → `~/.claude/scripts/safe-image.sh`
→ read). Never `Read` a raw downloaded image without `safe-image.sh` first — a bad image Read
poisons the session.

## Procedure

### 1. Detect: carousel vs reel

Open the URL in the browser. If the page has a `<video>` element or `.mp4` resources, it's a
video — use `instagram-browser-cdn-fallback.md` instead. Otherwise it's an image post/carousel —
continue here.

### 2. Probe slides + metadata (one JS call, no download)

```js
(() => {
  const slides = [...document.querySelectorAll('img')]
    .filter(i => i.src && i.src.includes('cdninstagram') && i.naturalWidth > 300)
    .map(i => ({
      alt: i.alt,
      auto: /may be an image|no photo description|photo of|image of/i.test(i.alt || ''),
      w: i.naturalWidth, h: i.naturalHeight,
    }));
  const m = p => (document.querySelector(`meta[property="${p}"]`) || {}).content || '';
  return {
    title: m('og:title'),
    caption: m('og:description'),   // "N likes, M comments - creator on DATE: \"caption\""
    url: m('og:url'),
    slideCount: slides.length,
    slides,
  };
})()
```

The browser tool truncates a very long `alt` for display — if a slide reports `[TRUNCATED]`,
re-read just that one: `[...document.querySelectorAll('img')].filter(i=>i.src.includes('cdninstagram')&&i.naturalWidth>300)[N].alt`.

Skip the profile-avatar `<img>` (square, ~<300px, or the creator's handle as alt).

### 3. Vision fallback for photo slides (only if `auto` is true)

For any slide flagged `auto`, capture its image (browser screenshot of the slide, or fetch the
blob) and read it with the vision model to extract on-image text / a description. Merge that in
place of the generic alt.

### 4. Assemble the standard folder

Parse creator, date, likes/comments from the caption string, then:

```bash
cat > /tmp/carousel.json <<'JSON'
{ "video_id": "<shortcode>", "platform": "ig", "creator": "<handle>",
  "title": "<short title>", "url": "<post url>", "upload_date": "YYYYMMDD",
  "caption": "<caption>", "likes": "<n>", "comments": "<n>",
  "slides": ["<slide 1 text>", "<slide 2 text>", "..."] }
JSON
uv run python scripts/ig_carousel_to_transcript.py --input /tmp/carousel.json
```

This writes `workspace/videos/{date}--{shortcode}--ig--{creator}--{title}/` with
`metadata.json` (`content_type: image-carousel`), `transcript_raw.txt`, and
`transcript_enhanced.txt`.

**Do NOT run `auto_enhancer`** on a carousel. Its corrections fix speech-to-text mis-hearings;
slide text is clean typed text and has no ASR errors to fix. (The script writes
`transcript_enhanced.txt == transcript_raw.txt` for pipeline compatibility.)

### 5. Analyze → summarize → store (unchanged)

Read `transcript_enhanced.txt` in-context and write `analysis.json` using the normal schema,
with `content_type: "image-carousel"`. Then write `summary.md`, run
`uv run python scripts/store_in_mcp_kb.py <folder>/analysis.json`, and update
`workspace/index.json`. For sports/fitness carousels set `area: mutora`.

## Notes

- Platform code stays `ig`; the distinguishing field is `content_type: image-carousel`. No new
  platform code needed.
- The caption often carries the real hook + CTA ("DM me X", "link in bio") — keep it as the
  final `[Caption]` block; it's context, and analysis should treat CTAs as `awareness`, not
  `actionable`, takeaways.
- `store_in_mcp_kb.py` expects `analysis.json.implementation_details` to be a **dict**
  (keys like `setup_steps`, `configuration`, `evidence_notes`), never a list — same gotcha as
  the reel fallback.
