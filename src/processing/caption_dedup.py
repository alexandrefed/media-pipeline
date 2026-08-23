"""Collapse rolling-caption repetition in auto-generated transcripts.

YouTube auto-captions scroll: each cue repeats the tail of the previous cue so
the viewer sees continuous text. Flattened to a transcript that becomes
duplication or triplication —

    "It's time to focus. This is going to be. It's time to focus. This is going
     to be. It's time to focus. This is going to be a big video and a lot of
     engineers are a big video and a lot of engineers are a big video and a lo…"

— which is how `SEI_qIW4o2c` ended up as 135 KB carrying maybe 45 KB of content.

Why this is a repo module and not another ad-hoc pass
----------------------------------------------------
Every video that got a `transcript_cleaned_for_analysis.txt` was deduped by an
agent doing it by hand that day; the ones whose analysis step failed were never
deduped at all. So failure and unreadability compounded exactly where the
material mattered most. A deterministic function that runs every time removes
both the handwork and the inconsistency.

The method
----------
Walk the token stream. At each position, if the next *k* tokens are identical to
the *k* tokens immediately preceding, they are an echo — skip them. Longest
window first, so a long repeated span collapses as one unit rather than being
chewed up by short accidental matches.

Deliberately conservative: it only removes text that is *immediately adjacent*
to an identical span. Legitimate repetition separated by any other words is
left alone, because losing real content is far worse than leaving an echo in.
"""

from __future__ import annotations

import re

# Below this a "repeat" is ordinary English ("that that", "had had", a repeated
# short phrase for emphasis). Four tokens is where echo becomes unambiguous.
MIN_WINDOW = 4
# Caption cues are short; beyond this we are matching paragraphs, not echoes.
MAX_WINDOW = 40

_TOKEN = re.compile(r"\S+")


def _norm(token: str) -> str:
    """Compare on lowercased alphanumerics so punctuation drift does not hide an echo."""
    return re.sub(r"[^a-z0-9]", "", token.lower())


def dedup_tokens(tokens: list[str]) -> list[str]:
    out: list[str] = []
    norm_out: list[str] = []
    i = 0
    n = len(tokens)
    while i < n:
        skipped = False
        upper = min(MAX_WINDOW, n - i, len(out))
        for k in range(upper, MIN_WINDOW - 1, -1):
            ahead = [_norm(t) for t in tokens[i : i + k]]
            if any(not a for a in ahead):
                continue
            if norm_out[-k:] == ahead:
                i += k
                skipped = True
                break
        if skipped:
            continue
        out.append(tokens[i])
        norm_out.append(_norm(tokens[i]))
        i += 1
    return out


def dedup_text(text: str) -> str:
    """Return ``text`` with adjacent echoed spans removed, layout preserved.

    Lines are processed as one stream (captions wrap mid-sentence, so an echo
    routinely straddles a line break) and the result is re-wrapped to a
    comparable width rather than emitted as one enormous line.
    """
    tokens = _TOKEN.findall(text)
    kept = dedup_tokens(tokens)

    lines: list[str] = []
    current: list[str] = []
    width = 0
    for token in kept:
        if width + len(token) + 1 > 100 and current:
            lines.append(" ".join(current))
            current, width = [], 0
        current.append(token)
        width += len(token) + 1
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines) + "\n"


def dedup_report(original: str, cleaned: str) -> str:
    before, after = len(original), len(cleaned)
    pct = (100.0 * (before - after) / before) if before else 0.0
    return f"{before} -> {after} chars ({pct:.1f}% removed as caption echo)"


def main() -> int:
    import argparse
    from pathlib import Path

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()

    raw = args.input.read_text(encoding="utf-8", errors="replace")
    cleaned = dedup_text(raw)
    dest = args.output or args.input.with_name("transcript_cleaned_for_analysis.txt")
    dest.write_text(cleaned, encoding="utf-8")
    print(f"{dest}: {dedup_report(raw, cleaned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
