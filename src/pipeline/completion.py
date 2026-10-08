"""What "processed" actually means, and when it may be written down.

The bug this module exists to kill
---------------------------------
``metadata.json`` carried ``processed_at``, and it was written by the FIRST
step — the moment ``transcript_raw.txt`` landed, inside
``youtube_processor.extract_raw_text_for_enhancement`` and again in the
``streamlined_process`` fallback. Steps 2-4 (enhance, analyse, index, store to
memory) had not run and frequently never would: step 3 is not automated at all,
it *prints a command for a human* and the script then exits **0** with
"Workflow paused at Step 3".

So the canonical failure was: transcript lands, ``processed_at`` stamped with
today's date, exit 0, and nothing downstream ever happens. Nothing errors,
because nothing ran. `20260810--SEI_qIW4o2c` — the most on-topic video of the
month — sat like that with a `processed_at` of 2026-08-23 and no analysis, no
summary, no index entry and zero memories.

The rule
--------
**The stamp is written LAST or it is a lie.** ``processed_at`` now means every
downstream stage produced a real artifact, and it is written by
:func:`stamp_if_complete` after checking, never by the step that starts the
work. The honest name for the old stamp is ``transcript_extracted_at``, which is
what it always recorded.

Retrievability is the terminal stage on purpose. The pipeline's whole reason to
exist is that an agent can later find the material; a video with a beautiful
``analysis.json`` that no search returns has not been ingested, it has been
downloaded.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

# Ordered: each stage is only meaningful once the ones before it are real.
STAGES = ("transcript", "analysis", "summary", "indexed", "retrievable")

# Below this a file is an empty shell — a 0-byte analysis.json passing an
# `exists()` check is the same vacuous-pass trap the stamp itself was.
MIN_ARTIFACT_BYTES = 32


@dataclass
class Completion:
    """Per-video stage truth, derived from artifacts rather than from claims."""

    folder: str
    video_id: str
    transcript: bool = False
    analysis: bool = False
    summary: bool = False
    indexed: bool = False
    retrievable: bool = False
    memory_count: int = 0
    missing: list[str] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.missing

    def as_dict(self) -> dict:
        return asdict(self)


def _real(path: Path) -> bool:
    """A file counts only if it exists AND carries content."""
    try:
        return path.is_file() and path.stat().st_size >= MIN_ARTIFACT_BYTES
    except OSError:
        return False


def video_id_of(folder: Path) -> str:
    """Second `--`-separated segment of the folder name, per the convention.

    Falls back to ``metadata.json`` because the four ``YYYYMMDD--https:``
    folders (the URL-parsing bug) have no usable id in their name.
    """
    parts = folder.name.split("--")
    if len(parts) >= 2 and parts[1] and parts[1] != "https:":
        return parts[1]
    meta = folder / "metadata.json"
    if _real(meta):
        try:
            return str(json.loads(meta.read_text()).get("video_id") or "")
        except (OSError, ValueError):
            return ""
    return ""


def has_analysis(folder: Path) -> bool:
    """Any analysis variant — the sports lane writes ``analysis_sports.json``."""
    return any(_real(p) for p in folder.glob("analysis*.json"))


def inspect(
    folder: Path,
    *,
    indexed_folders: set[str] | None = None,
    memory_counts: dict[str, int] | None = None,
) -> Completion:
    """Derive one video's stage truth from what is actually on disk and in the store.

    ``memory_counts`` maps video_id -> number of memories carrying its tag. It is
    passed in rather than looked up here so this stays a pure function and the
    network round-trips happen once, in the caller.
    """
    vid = video_id_of(folder)
    c = Completion(folder=folder.name, video_id=vid)

    c.transcript = _real(folder / "transcript_enhanced.txt") or _real(folder / "transcript_raw.txt")
    c.analysis = has_analysis(folder)
    c.summary = _real(folder / "summary.md")
    c.indexed = folder.name in (indexed_folders or set())
    c.memory_count = (memory_counts or {}).get(vid, 0)
    c.retrievable = c.memory_count > 0

    c.missing = [s for s in STAGES if not getattr(c, s)]
    return c


def stamp_if_complete(folder: Path, completion: Completion) -> bool:
    """Write ``processed_at`` — and ONLY if every stage really produced something.

    Returns True when the stamp was written. On an incomplete video it writes
    ``incomplete_stages`` instead, so the folder says what is missing rather than
    saying nothing (which reads identically to "fine").

    ``transcript_extracted_at`` is preserved/derived from any legacy
    ``processed_at`` found in place, because that is the only thing the old
    stamp ever truthfully recorded.
    """
    meta_path = folder / "metadata.json"
    try:
        meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    except (OSError, ValueError):
        meta = {}
    if not isinstance(meta, dict):
        meta = {}

    legacy = meta.pop("processed_at", None)
    if legacy and "transcript_extracted_at" not in meta:
        meta["transcript_extracted_at"] = legacy

    meta["stages"] = {s: bool(getattr(completion, s)) for s in STAGES}
    meta["memory_count"] = completion.memory_count

    if completion.complete:
        meta.pop("incomplete_stages", None)
        meta["processed_at"] = datetime.now(UTC).isoformat()
        written = True
    else:
        meta["incomplete_stages"] = list(completion.missing)
        written = False

    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    return written


def summarize(completions: Iterable[Completion]) -> dict[str, int]:
    """Honest counts. ``retrievable`` is the only one that answers the question
    the pipeline exists to answer."""
    rows = list(completions)
    counts = {"total": len(rows), "complete": sum(1 for c in rows if c.complete)}
    for stage in STAGES:
        counts[stage] = sum(1 for c in rows if getattr(c, stage))
    return counts
