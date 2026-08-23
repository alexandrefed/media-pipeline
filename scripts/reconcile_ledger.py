#!/usr/bin/env python3
"""Rebuild workspace/index.json from what is ACTUALLY on disk and in memory.

The ledger had drifted three ways at once and none of it was visible:

* 128 folders on disk, 103 entries in the index — 25 videos existed but were
  registered nowhere;
* 21 registered entries were missing ``analysis`` or ``summary`` and nothing
  reported it, so a fifth of the ledger was partial and read as fine;
* the index recorded *file presence* only, never whether the material was
  retrievable — which is the single thing the pipeline exists to deliver.

So this does not "sync" the index. It regenerates it from artifact truth, adds
the retrievability column, and prints the honest count. Reconciliation is a
read-and-rewrite of the ledger; it never deletes a video folder.

Usage
-----
    uv run python scripts/reconcile_ledger.py            # report only
    uv run python scripts/reconcile_ledger.py --write    # rewrite index.json + metadata stamps
    uv run python scripts/reconcile_ledger.py --json     # machine-readable

Memory lookups need the unified-memory API. Without them the retrievability
column cannot be filled, so the script REFUSES to write a ledger it cannot
tell the truth in (``--allow-no-memory`` to override for an offline audit).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline.completion import (  # noqa: E402
    Completion,
    inspect,
    stamp_if_complete,
    summarize,
    video_id_of,
)

DEFAULT_API = os.environ.get("UM_API_BASE", "http://127.0.0.1:8085")
MEMORY_NAMESPACE = "/alex/openclaw/videos/"


def _token() -> str:
    token = os.environ.get("GATEWAY_TOKEN", "")
    if token:
        return token
    env_file = Path.home() / "unified-memory-config" / ".env"
    if env_file.is_file():
        for line in env_file.read_text(errors="replace").splitlines():
            if line.startswith("GATEWAY_TOKEN="):
                return line.split("=", 1)[1].strip().strip("'\"")
    return ""


def memory_count(video_id: str, *, api: str, token: str, attempts: int = 6) -> int | None:
    """How many memories carry this video's tag. ``None`` = could not ask.

    ``None`` is deliberately distinct from ``0``: "the store did not answer" and
    "the store answered, nothing is there" must never collapse into the same
    value, or an API blip silently reports the whole corpus as unretrievable —
    which is the same lie as reporting it all fine, just in the other direction.

    The API rate-limits a burst at ~16 requests, and a 128-video sweep walks
    straight into it, so 429 is retried with backoff rather than counted as a
    failure. A sweep that gives up is how a real measurement becomes a guess.
    """
    if not video_id or not token:
        return None
    body = json.dumps(
        {"query": video_id, "tags": [f"video:{video_id}"], "page_size": 1}
    ).encode()
    delay = 1.0
    for attempt in range(attempts):
        req = urllib.request.Request(  # noqa: S310 — fixed local API base
            f"{api.rstrip('/')}/v1/memories/search/",
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                payload = json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < attempts - 1:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    wait = float(retry_after) if retry_after else delay
                except (TypeError, ValueError):
                    wait = delay
                time.sleep(max(wait, 0.25))
                delay = min(delay * 2, 10.0)
                continue
            return None
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            if attempt < attempts - 1:
                time.sleep(delay)
                delay = min(delay * 2, 10.0)
                continue
            return None

        total = payload.get("total")
        if isinstance(total, int):
            return total
        return len(payload.get("items", payload.get("results", [])))
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default="workspace", type=Path)
    ap.add_argument("--write", action="store_true", help="rewrite index.json + stamps")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--allow-no-memory", action="store_true")
    args = ap.parse_args()

    videos_dir = args.workspace / "videos"
    index_path = args.workspace / "index.json"
    if not videos_dir.is_dir():
        print(f"no such directory: {videos_dir}", file=sys.stderr)
        return 2

    try:
        old = json.loads(index_path.read_text())
    except (OSError, ValueError):
        old = {"videos": []}
    indexed_folders = {v.get("folder") for v in old.get("videos", [])}

    folders = sorted(p for p in videos_dir.iterdir() if p.is_dir())
    token = _token()

    counts: dict[str, int] = {}
    unknown_memory = 0
    for folder in folders:
        vid = video_id_of(folder)
        if not vid or vid in counts:
            continue
        n = memory_count(vid, api=args.api, token=token)
        if n is None:
            unknown_memory += 1
        else:
            counts[vid] = n

    rows: list[Completion] = [
        inspect(f, indexed_folders=indexed_folders, memory_counts=counts)
        for f in folders
    ]
    stats = summarize(rows)
    stats["unregistered_before"] = sum(
        1 for f in folders if f.name not in indexed_folders
    )
    stats["memory_lookups_failed"] = unknown_memory

    if args.as_json:
        print(json.dumps({"counts": stats, "videos": [r.as_dict() for r in rows]}, indent=2))
    else:
        print(f"folders on disk .......... {stats['total']}")
        print(f"  transcript ............. {stats['transcript']}")
        print(f"  analysis ............... {stats['analysis']}")
        print(f"  summary ................ {stats['summary']}")
        print(f"  in the ledger .......... {stats['indexed']}")
        print(f"  RETRIEVABLE from memory  {stats['retrievable']}   <- the real number")
        print(f"  complete (all stages) .. {stats['complete']}")
        print(f"unregistered before this run: {stats['unregistered_before']}")
        if unknown_memory:
            print(f"!! memory lookups that FAILED: {unknown_memory} (not counted as 0)")
        worst = [r for r in rows if r.transcript and not r.retrievable]
        if worst:
            print(f"\n{len(worst)} video(s) have a transcript but reach NO memory:")
            for r in sorted(worst, key=lambda r: r.folder)[:40]:
                print(f"  {r.folder}  missing={','.join(r.missing)}")

    if not args.write:
        return 0

    if unknown_memory and not args.allow_no_memory:
        print(
            f"\nREFUSING to write: {unknown_memory} memory lookup(s) failed, so the "
            "retrievable column would be a guess. Fix the API or pass "
            "--allow-no-memory for an explicitly incomplete audit.",
            file=sys.stderr,
        )
        return 1

    # LEDGER FIRST, STAMPS SECOND. Order matters and getting it wrong is this
    # tool committing the very bug it audits: `indexed` is derived from the
    # ledger, so stamping before the rewrite records every video as unindexed
    # — a stamp computed from state that is about to change is exactly the
    # premature `processed_at`, one layer up.
    every_folder = {f.name for f in folders}
    final_rows = [
        inspect(f, indexed_folders=every_folder, memory_counts=counts) for f in folders
    ]
    final_stats = summarize(final_rows)

    index_path.write_text(
        json.dumps(
            {
                "generated": datetime.now(UTC).isoformat(),
                "convention": "{YYYYMMDD}--{VIDEO_ID}--{PLATFORM}--{CHANNEL}--{TITLE}",
                "total": len(final_rows),
                # Recorded so a future reader sees the honest number without
                # recomputing it, and so a drop shows up as a diff.
                "retrievable": final_stats["retrievable"],
                "videos": [r.as_dict() for r in final_rows],
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    stamped = 0
    for folder, row in zip(folders, final_rows, strict=True):
        if stamp_if_complete(folder, row):
            stamped += 1

    print(
        f"\nwrote {index_path} — {len(final_rows)} entries, "
        f"{final_stats['retrievable']} retrievable, "
        f"{stamped} stamped processed_at (complete on every stage)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
