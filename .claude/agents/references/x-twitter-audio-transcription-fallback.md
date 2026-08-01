# X/Twitter audio transcription fallback

Use when `uv run python main.py streamlined <x-url>` exits successfully but produces no usable captions/transcript for an X/Twitter video.

> **Origin**: Crystallized by the Hermes self-improvement Curator (2026-07-08). Ported into the repo 2026-08-02.

## Signal

- Streamlined output says captions are unavailable, but exits `0`.
- A video folder exists, but `transcript_raw.txt` only contains metadata/header lines and no spoken transcript.
- The generated folder or metadata may incorrectly use platform `yt`; correct final artifacts to platform `x` / `X/Twitter`.

## Fallback workflow

From `~/projects/workflows/media-pipeline` with `.env` sourced:

```bash
yt-dlp --dump-single-json --skip-download "$URL" > /tmp/xmeta.json
mkdir -p workspace/audio
yt-dlp -x --audio-format mp3 -o "workspace/audio/%(id)s.%(ext)s" "$URL"
```

Then transcribe the downloaded MP3:

```bash
uv run python - <<'PY'
from pathlib import Path
from faster_whisper import WhisperModel

video_id = "REPLACE_WITH_RESOLVED_MEDIA_ID"
vdir = Path("workspace/videos/REPLACE_WITH_VIDEO_FOLDER")
audio = f"workspace/audio/{video_id}.mp3"

try:
    model = WhisperModel("large-v3-turbo", device="cuda", compute_type="int8")
except Exception:
    model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    audio,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
)
lines = [seg.text.strip() for seg in segments if seg.text.strip()]
vdir.mkdir(parents=True, exist_ok=True)
(vdir / "transcript_raw.txt").write_text("\n".join(lines), encoding="utf-8")
print(info.language, len(lines), sum(map(len, lines)))
PY
```

Run auto-enhancement and continue normal analysis/storage:

```bash
uv run python -m src.processing.auto_enhancer "$VDIR/transcript_raw.txt"
mv "$VDIR/transcript_raw_auto_enhanced.txt" "$VDIR/transcript_enhanced.txt"
```

## Analysis notes

- Base analysis on `transcript_enhanced.txt`, not the header-only raw file from the failed caption attempt.
- Set `pipeline_type` to `X/Twitter yt-dlp audio transcription fallback`.
- Keep `platform` as `x` in `metadata.json`, `analysis.json`, and `workspace/index.json` even if the initial folder was created as `--yt--`.
- Include extraction notes that captions were unavailable, audio was downloaded with `yt-dlp`, transcribed with `faster-whisper`, and auto-enhanced.
