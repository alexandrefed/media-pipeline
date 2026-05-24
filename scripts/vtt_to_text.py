#!/usr/bin/env python3
"""Convert a WebVTT subtitle file to clean plain text.

Usage:
    uv run python scripts/vtt_to_text.py <vtt_file> [-o output_file]

If no output file is specified, prints to stdout.
"""

import argparse
import re
import sys


def vtt_to_text(vtt_content: str) -> str:
    """Convert VTT content to clean plain text."""
    lines = []
    for line in vtt_content.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}", line):
            continue
        if re.match(r"^[\d\s]+$", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"align:start position:\d+%", "", line)
        line = line.strip()
        if line:
            lines.append(line)

    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    text = " ".join(deduped)
    return re.sub(r"\s+", " ", text).strip()


def main():
    parser = argparse.ArgumentParser(description="Convert VTT subtitles to plain text")
    parser.add_argument("vtt_file", help="Path to .vtt file")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.vtt_file, encoding="utf-8") as f:
        content = f.read()

    text = vtt_to_text(content)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {len(text)} chars (~{len(text.split())} words) to {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
