# Instagram image carousel (pictures with text)

Use when the URL is an Instagram **image** post or carousel (`instagram.com/p/<shortcode>`)
made of picture slides — often text-graphics — with **no video/audio to transcribe**. This is
the counterpart to `instagram-browser-cdn-fallback.md`, which handles *reels*.

## ⚠️ Read the slides with VISION. Do NOT trust `img[alt]`.

The first version of this doc claimed the slide text lives in each `<img alt>` attribute. **That
is wrong and it silently produced a completely fabricated ingestion** (post `Db6qLt_CJdq`: a
19-slide carousel about the Meta ads algorithm was stored as 6 unrelated slides about "AI +
ecommerce"). Why it fails:

- A broad `img[alt]` selector grabs images from the **whole page** — the "more posts from this
  account" grid and suggested content below the post — not this post's carousel.
- Instagram's `alt` for these text-slides is **auto-generated OCR of other images**, so even the
  ones that load look like real copy but belong to different posts.
- Only the current + adjacent slides are in the DOM anyway (lazy-loaded).

**The ground truth is the rendered slide.** Read each slide with the vision model. It is a
text-on-plain-background image — vision reads it perfectly.

## Procedure

### 1. Detect: carousel vs reel

Open the URL in the browser. If the page has a `<video>` element or `.mp4` resources, it's a
video — use `instagram-browser-cdn-fallback.md`. Otherwise it's an image post/carousel.

### 2. Metadata + slide count (JS probe — metadata only, NOT slide text)

```js
(() => {
  const m = p => (document.querySelector(`meta[property="${p}"]`) || {}).content || '';
  // slide count = the dot indicator bar
  const dotBar = [...document.querySelectorAll('div')].map(d => d.children.length)
    .filter(n => n >= 2 && n <= 30);
  return { title: m('og:title'), caption: m('og:description'), url: m('og:url') };
})()
```

`og:description` reliably gives the caption + creator + date + likes/comments
(e.g. `"2,373 likes, 109 comments - markbuildsbrands on August 11, 2026: \"…\""`). Parse those.
Count the slide dots from a screenshot (the bar of little circles under the image).

### 3. Read every slide with vision (the actual extraction)

The URL takes `?img_index=N`. For each slide `1..N`:

1. Navigate to `…/p/<code>/?img_index=N` **or** click the right-arrow (`›`) on the image
   (roughly the right edge, vertical centre of the image panel).
2. Screenshot/zoom just the image region (crop out the comments column) for a clean read.
3. Vision-read the slide's text verbatim, in reading order. Some slides are screenshots or
   thumbnails (e.g. an Ads Manager grab, a video thumbnail) — capture the visible text and note
   the image in brackets, e.g. `[slide image: Ads Manager screenshot — …]`.
4. Advance until the last dot is filled (all N slides read).

Keep slides in order; that order is the narrative (hook → lessons → CTA).

### 4. Assemble the standard folder

```bash
cat > /tmp/carousel.json <<'JSON'
{ "video_id": "<shortcode>", "platform": "ig", "creator": "<handle>",
  "title": "<short title, usually slide 1>", "url": "<post url>", "upload_date": "YYYYMMDD",
  "caption": "<caption>", "likes": "<n>", "comments": "<n>",
  "slides": ["<slide 1 text>", "<slide 2 text>", "..."] }
JSON
uv run python scripts/ig_carousel_to_transcript.py --input /tmp/carousel.json
```

Writes `workspace/videos/{date}--{shortcode}--ig--{creator}--{title}/` with `metadata.json`
(`content_type: image-carousel`), `transcript_raw.txt`, and `transcript_enhanced.txt`.

**Do NOT run `auto_enhancer`** — its corrections fix speech-to-text mis-hearings; slide text is
clean typed text.

### 5. Analyze → summarize → store (unchanged)

Read `transcript_enhanced.txt` and write `analysis.json` (schema as normal, `content_type:
image-carousel`), then `summary.md`, then
`uv run python scripts/store_in_mcp_kb.py <folder>/analysis.json`, then update
`workspace/index.json`. Sports/fitness carousels → `area: mutora`.

## Verify before claiming success

Before saying it worked, **confirm the extracted slide text matches what is actually on the
slides** — re-read slide 1 and one middle slide against the screenshots. "I extracted N slides
and stored them" is not verification; matching them to the rendered images is. (The first run of
this capability skipped that and stored fiction.)

## Notes

- Platform code stays `ig`; the distinguishing field is `content_type: image-carousel`.
- The caption's CTA ("DM me X", "link in bio") is context — treat CTAs as `awareness`, not
  `actionable`, takeaways.
- `store_in_mcp_kb.py` expects `analysis.json.implementation_details` to be a **dict**, never a
  list — same gotcha as the reel fallback.
