"""Audio fallback: download the audio with yt-dlp, transcribe with faster-whisper.

Used when a video has no usable subtitle track (YouTube rate limits or removed
captions, or a video that never had any). Output has the same shape as the
subtitle path (``RawTranscriptExtractor._parse_raw_vtt``), so every later step
is unchanged.

GPU on the gaming-PC (large-v3-turbo, int8, the settings the Hermes
media-pipeline skill used by hand); on a machine without CUDA it falls back to
a small CPU model and says so.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def _cuda_available() -> bool:
    try:
        import ctranslate2

        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def pick_device() -> tuple[str, str, str]:
    """Return (model_name, device, compute_type)."""
    if _cuda_available():
        return "large-v3-turbo", "cuda", "int8"
    return "small", "cpu", "int8"


def download_audio(url: str, out_dir: Path) -> Path:
    """Download the best audio-only stream; return the file path."""
    import yt_dlp

    out_dir.mkdir(parents=True, exist_ok=True)
    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    node = shutil.which("node")
    if node:
        opts["js_runtimes"] = {"node": {"path": node}}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info))


def _fmt(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def segments_to_raw(whisper_segments) -> list[dict]:
    """Map faster-whisper segments to the raw-segment dicts the subtitle path makes."""
    raw = []
    for seg in whisper_segments:
        text = seg.text.strip()
        if not text:
            continue
        raw.append(
            {
                "segment_index": len(raw),
                "start_time": float(seg.start),
                "end_time": float(seg.end),
                "duration": float(seg.end) - float(seg.start),
                "text_lines": [text],
                "raw_text": text,
                "timestamp_line": f"{_fmt(seg.start)} --> {_fmt(seg.end)}",
            }
        )
    return raw


def transcribe_audio_file(path: Path) -> list[dict]:
    from faster_whisper import WhisperModel

    model_name, device, compute_type = pick_device()
    print(f"   Whisper fallback: model {model_name} on {device} ({compute_type})")
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, _info = model.transcribe(
        str(path), vad_filter=True, vad_parameters={"min_silence_duration_ms": 500}
    )
    return segments_to_raw(segments)


def transcribe_url(url: str, workspace: Path | None = None) -> list[dict]:
    """Download audio for ``url`` and return raw segments."""
    audio_dir = (workspace or Path("workspace")) / "audio"
    audio = download_audio(url, audio_dir)
    segments = transcribe_audio_file(audio)
    if not segments:
        raise Exception("Audio transcription produced no text")
    return segments
