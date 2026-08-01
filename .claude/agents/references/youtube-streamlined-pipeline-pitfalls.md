# YouTube Streamlined Pipeline Pitfalls

Session-derived notes for processing YouTube URLs through `scripts/streamlined_process.py`.

> **Origin**: Crystallized by the Hermes self-improvement Curator (2026-06-02). Ported into the repo 2026-08-02. Note: the `youtu.be` parsing regression below was fixed in the repo on 2026-08-02.

## Step 3 pause is intentional unless automation is added

`scripts/streamlined_process.py` may stop after transcript enhancement with:

```text
⏸️  Workflow paused at Step 3
Run the command above to continue with agent analysis
```

This is not necessarily a crash. The script historically printed a `claude "Use @youtube-transcript-analyzer ..."` command and expected a manual Claude Code/specialized-agent handoff. If `analysis.json` does not already exist, storage will not run automatically.

Agent handling pattern:
1. Treat the pause as a handoff point, not a failed extraction.
2. Read `transcript_enhanced.txt` yourself or invoke the configured analysis agent if available.
3. Write `analysis.json` and `summary.md` in the same video folder.
4. Run `uv run python scripts/store_in_mcp_kb.py <video_folder>/analysis.json`.
5. Report that Step 3 was completed manually/in-context if the script did not automate it.

## youtu.be URL parsing regression (FIXED 2026-08-02)

A prior version extracted video IDs with:

```python
youtube_url.split("v=")[-1].split("&")[0]
```

That works for `youtube.com/watch?v=...` but fails for `youtu.be/VIDEO_ID?...`, producing malformed folders such as `YYYYMMDD--https:/youtu.be/...`.

Durable fix (now in `scripts/streamlined_process.py` as `extract_youtube_video_id`):
- Uses `urllib.parse.urlparse` + `parse_qs`.
- Supports `youtube.com/watch?v=ID`, `youtu.be/ID`, `youtube.com/shorts/ID`, `youtube.com/embed/ID`, and `youtube.com/live/ID`.

Regression test cases:

```python
def test_extract_youtube_video_id_from_watch_url():
    assert extract_youtube_video_id("https://www.youtube.com/watch?v=0teZqotpqT8&feature=share") == "0teZqotpqT8"

def test_extract_youtube_video_id_from_short_url_with_query():
    assert extract_youtube_video_id("https://youtu.be/0teZqotpqT8?is=e0NhQkPASHhd9NUw") == "0teZqotpqT8"

def test_extract_youtube_video_id_from_shorts_url():
    assert extract_youtube_video_id("https://www.youtube.com/shorts/0teZqotpqT8?si=abc123") == "0teZqotpqT8"
```

## Cleanup when malformed duplicate folders exist

If both a correct `*--VIDEO_ID--*` folder and a malformed URL-derived folder exist:
1. Move/copy generated artifacts (`analysis.json`, `summary.md`, `transcript_enhanced.txt`, captions) into the correct folder.
2. Preserve correct `metadata.json` and `transcript_raw.txt` if already present.
3. Remove the malformed folder tree after verifying the correct folder contains all expected files.

Expected correct folder files after cleanup:

```text
metadata.json
transcript_raw.txt
transcript_enhanced.txt
analysis.json
summary.md
subs.en.vtt  # if caption fallback was used
```
