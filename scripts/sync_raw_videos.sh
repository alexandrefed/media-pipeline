#!/usr/bin/env bash
# sync_raw_videos.sh — copy each processed video's summary.md + analysis.json into WikiVault/raw/videos/<same folder>/.
#
# Why: the weekly wiki-ingest detector enumerates WikiVault/raw/videos/*/, so a processed video that never lands
# there is invisible to it. Measured 2026-10-03: 224 processed folders, 48 ever copied, detector reported "backlog 0".
# Idempotent: unchanged files are not rewritten. Copy only — committing the vault is a separate, explicit step.
#
# Usage: sync_raw_videos.sh [<video-folder>...]   no args = every folder under workspace/videos
# Env:   MP_ROOT (default: the repo this script lives in), WIKI_VAULT (default ~/Documents/WikiVault)
set -euo pipefail

MP_ROOT="${MP_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
WIKI="${WIKI_VAULT:-$HOME/Documents/WikiVault}"
SRC="$MP_ROOT/workspace/videos"
DST="$WIKI/raw/videos"
[ -d "$SRC" ] || { echo "sync_raw_videos: no $SRC" >&2; exit 1; }
[ -d "$WIKI/atlas" ] || { echo "sync_raw_videos: $WIKI is not a WikiVault" >&2; exit 1; }

if [ "$#" -gt 0 ]; then dirs=("$@"); else dirs=("$SRC"/*/); fi
new=0 changed=0 same=0
for d in "${dirs[@]}"; do
  d="${d%/}"; [ -d "$d" ] || continue
  [ -f "$d/summary.md" ] || continue
  name="$(basename "$d")"; mkdir -p "$DST/$name"
  for f in summary.md analysis.json; do
    [ -f "$d/$f" ] || continue
    if [ ! -f "$DST/$name/$f" ]; then cp "$d/$f" "$DST/$name/$f"; new=$((new+1))
    elif ! cmp -s "$d/$f" "$DST/$name/$f"; then cp "$d/$f" "$DST/$name/$f"; changed=$((changed+1))
    else same=$((same+1)); fi
  done
done
echo "sync_raw_videos: $new new, $changed updated, $same unchanged files (-> $DST)"
