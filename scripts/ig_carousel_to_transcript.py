#!/usr/bin/env python3
"""Assemble an Instagram image-carousel into the standard video-folder layout.

Instagram image carousels (pictures with text) are read slide-by-slide with the
VISION model — navigate `?img_index=N` and screenshot each rendered slide (see
`.claude/agents/references/instagram-image-carousel.md`). Do NOT scrape `<img alt>`:
Instagram's alt is auto-OCR that belongs to other images on the page and silently
ingests the wrong post. This script takes the vision-extracted slides + caption +
metadata as JSON and writes the standard `workspace/videos/{folder}/` with
`metadata.json` and `transcript_raw.txt`, so the rest of the pipeline
(analyze → summarize → store) is unchanged.

Unlike audio/video, carousel slide text is clean typed text, NOT an ASR
transcription — so it is deliberately NOT run through `auto_enhancer` (whose
corrections only fix speech-to-text mis-hearings).

Input JSON shape (stdin or --input FILE):
    {
      "video_id": "Db6qLt_CJdq",       # shortcode
      "platform": "ig",
      "creator": "markbuildsbrands",
      "title": "short human title",
      "url": "https://www.instagram.com/p/Db6qLt_CJdq/",
      "upload_date": "20260811",        # YYYYMMDD; falls back to today
      "caption": "post caption text",
      "likes": "2373", "comments": "109",
      "slides": ["slide 1 text", "slide 2 text", ...]
    }

Usage:
    uv run python scripts/ig_carousel_to_transcript.py --input carousel.json
    cat carousel.json | uv run python scripts/ig_carousel_to_transcript.py
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _slug(text: str, maxwords: int = 8, maxlen: int = 25) -> str:
    s = re.sub(r"[^a-z0-9 -]", "", (text or "").lower())
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return "-".join(s.split("-")[:maxwords])[:maxlen].strip("-") or "untitled"


def build_transcript(slides: list[str], caption: str) -> str:
    """Render slides + caption into the canonical transcript_raw.txt body."""
    parts = []
    for i, slide in enumerate(slides, 1):
        text = (slide or "").strip()
        if text:
            parts.append(f"[Slide {i}]\n{text}")
    if caption and caption.strip():
        parts.append(f"[Caption]\n{caption.strip()}")
    return "\n\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble IG image carousel into a video folder")
    ap.add_argument("--input", help="JSON file (default: stdin)")
    ap.add_argument(
        "--videos-dir",
        default="workspace/videos",
        help="Base videos directory (default: workspace/videos)",
    )
    args = ap.parse_args()

    raw = Path(args.input).read_text() if args.input else sys.stdin.read()
    data = json.loads(raw)

    video_id = data["video_id"]
    slides = data.get("slides", [])
    if not slides:
        print("❌ No slides provided", file=sys.stderr)
        return 1

    platform = data.get("platform", "ig")
    creator = data.get("creator", "unknown")
    title = data.get("title") or (slides[0][:60] if slides else video_id)
    upload_date = data.get("upload_date") or datetime.now().strftime("%Y%m%d")

    videos_dir = Path(args.videos_dir)
    # Reuse an existing folder for this video ID (dedup), else create one.
    existing = list(videos_dir.glob(f"*--{video_id}--*"))
    if existing:
        vdir = existing[0]
    else:
        folder = f"{upload_date}--{video_id}--{platform}--{_slug(creator)}--{_slug(title)}"
        vdir = videos_dir / folder
        vdir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "video_id": video_id,
        "title": title,
        "channel": creator,
        "creator": creator,
        "platform": platform,
        "content_type": "image-carousel",
        "url": data.get("url", f"https://www.instagram.com/p/{video_id}/"),
        "upload_date": upload_date,
        "caption": data.get("caption", ""),
        "likes": data.get("likes", ""),
        "comments": data.get("comments", ""),
        "slide_count": len(slides),
        "source": "instagram browser vision carousel extraction (per-slide screenshot read)",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
    (vdir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    transcript = build_transcript(slides, data.get("caption", ""))
    (vdir / "transcript_raw.txt").write_text(transcript, encoding="utf-8")
    # Carousel text is clean typed text (no ASR) — enhanced == raw, no auto_enhancer pass.
    (vdir / "transcript_enhanced.txt").write_text(transcript, encoding="utf-8")

    print(f"✅ Carousel assembled: {vdir}")
    print(f"   Slides: {len(slides)} | transcript: {len(transcript)} chars")
    print(str(vdir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
