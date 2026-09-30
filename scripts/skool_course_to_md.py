#!/usr/bin/env python3
"""Turn a Skool course extracted by scripts/skool_extract.js into markdown.

Input is the JSON the browser script downloads (lesson bodies as Skool "[v2]"
ProseMirror JSON, captions of Skool-hosted videos, ids of YouTube videos).
Output, in the course folder:

    raw.md                     the whole course, in order
    lessons/M1-03-<slug>.md    one file per lesson: lesson text + transcript
    captions/<youtube-id>.json3  cached YouTube captions, so re-runs stay offline

Transcripts keep a [mm:ss] stamp at the start of each paragraph so a passage
can be found in the video again.

Usage:
    uv run python scripts/skool_course_to_md.py <course.json> [-o <out_dir>]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yt_dlp

# --- lesson body: Skool [v2] ProseMirror JSON -> markdown -------------------


def strip_tracking(url: str) -> str:
    """Drop the utm_* parameters Skool appends to its own links."""
    base, _, query = url.partition("?")
    kept = [p for p in query.split("&") if p and not p.startswith("utm_")]
    return base + ("?" + "&".join(kept) if kept else "")


def render_inline(nodes: list[dict]) -> str:
    out = []
    for n in nodes or []:
        if n["type"] == "hardBreak":
            out.append("<br>")
            continue
        text = n.get("text", "")
        for m in n.get("marks", []) or []:
            t = m["type"]
            if t == "code":
                text = f"`{text}`"
            elif t == "bold":
                text = f"**{text}**"
            elif t == "italic":
                text = f"*{text}*"
            elif t == "link":
                text = f"[{text}]({strip_tracking(m['attrs']['href'])})"
            elif t == "videoTimestamp":
                text = f"[{m['attrs']['timestamp']}]"
        out.append(text)
    s = "".join(out).replace("****", "")
    # A paragraph stays on one line; line breaks inside it become <br>.
    return s.replace("\n", " ").strip()


def render_blocks(nodes: list[dict], heading_offset: int, indent: str = "") -> list[str]:
    blocks = []
    for n in nodes or []:
        t = n["type"]
        if t == "paragraph":
            text = render_inline(n.get("content"))
            if text:
                blocks.append(indent + text)
        elif t == "heading":
            level = min(6, n["attrs"]["level"] + heading_offset)
            blocks.append(indent + "#" * level + " " + render_inline(n.get("content")))
        elif t in ("unorderedList", "orderedList"):
            start = (n.get("attrs") or {}).get("start") or 1
            items = []
            for i, item in enumerate(n.get("content", [])):
                marker = f"{start + i}. " if t == "orderedList" else "- "
                inner = render_blocks(
                    item.get("content"), heading_offset, indent + " " * len(marker)
                )
                first, rest = (inner[0].lstrip(), inner[1:]) if inner else ("", [])
                items.append("\n".join([indent + marker + first, *rest]))
            blocks.append("\n".join(items))
        elif t == "codeBlock":
            lang = (n.get("attrs") or {}).get("language") or ""
            code = "".join(c.get("text", "") for c in n.get("content", []) or [])
            fenced = f"```{lang}\n{code}\n```"
            blocks.append("\n".join(indent + line for line in fenced.split("\n")))
        elif t == "blockquote":
            inner = render_blocks(n.get("content"), heading_offset)
            blocks.append(
                "\n".join(
                    indent + "> " + line if line else indent + ">"
                    for b in inner
                    for line in b.split("\n")
                )
            )
        else:
            print(f"warning: unhandled node type {t}", file=sys.stderr)
    return blocks


def body_to_md(body: str, heading_offset: int) -> str:
    if not body:
        return ""
    if body.startswith("[v2]"):
        return "\n\n".join(render_blocks(json.loads(body[4:]), heading_offset))
    return body.strip()


# --- transcripts -------------------------------------------------------------

CUE = re.compile(r"(\d+):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d+):(\d{2}):(\d{2})\.(\d{3})")


def mux_vtt_cues(vtt: str) -> list[tuple[float, float, str]]:
    """Cues from Skool's (Mux) captions. Segments overlap, so a cue can repeat."""
    cues, seen = [], set()
    lines = vtt.split("\n")
    for i, line in enumerate(lines):
        m = CUE.search(line)
        if not m:
            continue
        g = list(map(int, m.groups()))
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = []
        for nxt in lines[i + 1 :]:
            if not nxt.strip() or CUE.search(nxt):
                break
            text.append(re.sub(r"<[^>]+>", "", nxt).strip())
        text = " ".join(text).strip()
        if text and (start, text) not in seen:
            seen.add((start, text))
            cues.append((start, end, text))
    return sorted(cues)


def youtube_cues(video_id: str, cache_dir: Path) -> list[tuple[float, float, str]]:
    """YouTube automatic English captions, in json3 (no rolling-line duplicates)."""
    cache = cache_dir / f"{video_id}.json3"
    if not cache.exists():
        opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            tracks = (
                info.get("subtitles", {}).get("en")
                or info.get("automatic_captions", {}).get("en-orig")
                or info.get("automatic_captions", {}).get("en")
                or []
            )
            track = next((t for t in tracks if t.get("ext") == "json3"), None)
            if not track:
                raise RuntimeError(f"no English json3 captions for {video_id}")
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(ydl.urlopen(track["url"]).read())
    data = json.loads(cache.read_text())
    cues = []
    for ev in data.get("events", []):
        if ev.get("aAppend") or "segs" not in ev:
            continue
        text = "".join(s.get("utf8", "") for s in ev["segs"]).replace("\n", " ").strip()
        if text:
            start = ev["tStartMs"] / 1000
            cues.append((start, start + ev.get("dDurationMs", 0) / 1000, text))
    return cues


def stamp(seconds: float) -> str:
    s = int(seconds)
    return (
        f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
        if s >= 3600
        else f"{s // 60:02d}:{s % 60:02d}"
    )


def cues_to_paragraphs(cues: list[tuple[float, float, str]], max_words: int = 110) -> str:
    """Group cues into paragraphs: break on a pause or once a paragraph is long and a sentence ends."""
    paras, cur, cur_start, words, prev_end = [], [], None, 0, None
    for start, end, text in cues:
        pause = prev_end is not None and start - prev_end > 1.5
        sentence_done = bool(cur) and re.search(r"[.!?][\"')\]]?$", cur[-1])
        if cur and (
            (pause and sentence_done)
            or (words >= max_words and sentence_done)
            or words >= max_words * 2
        ):
            paras.append(f"**[{stamp(cur_start)}]** " + " ".join(cur))
            cur, words = [], 0
        if not cur:
            cur_start = start
        cur.append(text)
        words += len(text.split())
        prev_end = end
    if cur:
        paras.append(f"**[{stamp(cur_start)}]** " + " ".join(cur))
    return "\n\n".join(re.sub(r"\s+", " ", p) for p in paras)


# --- assembly ----------------------------------------------------------------


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60].rstrip("-")


def lesson_filename(lesson: dict, index_in_section: int) -> str:
    title = lesson["title"]
    num = re.match(r"(\d+)\.(\d+)\s+(.*)", title)
    if num:
        return f"M{num.group(1)}-{int(num.group(2)):02d}-{slugify(num.group(3))}.md"
    mod = re.match(r"Module (\d+)", lesson.get("section") or "")
    return f"M{mod.group(1) if mod else 0}-{index_in_section:02d}-{slugify(title)}.md"


def minutes(ms) -> str:
    return f"{round(ms / 60000)} min" if ms else "unknown length"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("course_json")
    ap.add_argument("-o", "--out", help="output folder (default: folder of course_json)")
    args = ap.parse_args()

    src = Path(args.course_json)
    out = Path(args.out) if args.out else src.parent
    course = json.loads(src.read_text())
    (out / "lessons").mkdir(parents=True, exist_ok=True)

    raw = [f"# {course['course']}", "", course.get("courseDescription", ""), ""]
    report, per_section, last_section = [], {}, object()
    for lesson in course["lessons"]:
        section = lesson.get("section")
        per_section[section] = per_section.get(section, 0) + 1
        fname = lesson_filename(lesson, per_section[section])
        video = lesson.get("video")

        transcript, video_line = "", "Video: none (text-only lesson)"
        if video:
            try:
                if video["kind"] == "skool":
                    cues = mux_vtt_cues(video.get("captionsVtt") or "")
                    video_line = f"Video: hosted on Skool, {minutes(video.get('durationMs'))}"
                elif video["kind"] == "youtube":
                    cues = youtube_cues(video["id"], out / "captions")
                    video_line = f"Video: YouTube https://www.youtube.com/watch?v={video['id']}, {minutes(video.get('durationMs'))}"
                else:
                    cues, video_line = [], f"Video: {video.get('link')} (no captions fetched)"
            except Exception as e:  # one bad video must not sink the course
                cues = []
                print(f"warning: {lesson['title']}: {e}", file=sys.stderr)
            transcript = cues_to_paragraphs(cues)
        words = len(transcript.split())
        report.append(
            (fname, video["kind"] if video else "text", (video or {}).get("durationMs"), words)
        )

        header = [
            f"# {lesson['title']}",
            "",
            f"- Course: {course['course']}" + (f" — {section}" if section else ""),
            f"- Source: {lesson['url']}",
            f"- {video_line}",
            "",
        ]
        text_md = body_to_md(lesson["body"], heading_offset=1)
        parts = ["## Lesson text", "", text_md or "_(no written text)_", ""]
        if video:
            parts += ["## Transcript", "", transcript or "_(no captions available)_", ""]
        (out / "lessons" / fname).write_text("\n".join(header + parts))

        if section != last_section and section:
            raw += [f"# {section}", ""]
        last_section = section
        raw += [
            f"## {lesson['title']}",
            "",
            f"_{video_line} · lesson file: lessons/{fname}_",
            "",
            body_to_md(lesson["body"], heading_offset=2),
            "",
        ]
        if transcript:
            raw += ["### Transcript", "", transcript, ""]
    (out / "raw.md").write_text("\n".join(raw))

    for fname, kind, ms, words in report:
        rate = f"{words / (ms / 60000):.0f} w/min" if ms and words else ""
        print(f"{fname:70} {kind:8} {minutes(ms) if ms else '':>8} {words:6} words {rate}")


if __name__ == "__main__":
    main()
