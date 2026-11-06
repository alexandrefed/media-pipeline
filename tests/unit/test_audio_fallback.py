"""No usable subtitles -> audio transcription; usable subtitles -> no audio. No network."""

from types import SimpleNamespace

import src.pipeline.raw_transcript_extractor as rte
from src.pipeline.audio_transcriber import segments_to_raw

VTT = "WEBVTT\n\n00:00:01.000 --> 00:00:02.500\nhello there\n"


class FakeYDL:
    def __init__(self, info, subtitle_body=VTT):
        self.info, self.body = info, subtitle_body

    def __call__(self, opts):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def extract_info(self, url, download=False):
        return self.info

    def urlopen(self, url):
        body = self.body
        if isinstance(body, Exception):
            raise body
        return SimpleNamespace(read=lambda: body.encode())


def _run(monkeypatch, info, body=VTT):
    monkeypatch.setattr(rte.yt_dlp, "YoutubeDL", FakeYDL(info, body))
    ex = rte.RawTranscriptExtractor()
    calls = []
    ex._transcribe_audio = lambda url: calls.append(url) or [{"raw_text": "from audio"}]
    return ex.extract_raw_segments("https://youtu.be/x"), calls


def test_no_tracks_goes_to_audio(monkeypatch):
    segs, calls = _run(monkeypatch, {"subtitles": {}, "automatic_captions": {}})
    assert calls and segs[0]["raw_text"] == "from audio"


def test_rate_limited_track_goes_to_audio(monkeypatch):
    info = {"subtitles": {}, "automatic_captions": {"en": [{"ext": "vtt", "url": "u"}]}}
    segs, calls = _run(monkeypatch, info, Exception("HTTP Error 429"))
    assert calls


def test_empty_playlist_instead_of_vtt_goes_to_audio(monkeypatch):
    info = {"subtitles": {}, "automatic_captions": {"en": [{"ext": "vtt", "url": "u"}]}}
    _, calls = _run(monkeypatch, info, "#EXTM3U\n")
    assert calls


def test_good_subtitles_never_touch_audio(monkeypatch):
    info = {"subtitles": {"en": [{"ext": "vtt", "url": "u"}]}, "automatic_captions": {}}
    segs, calls = _run(monkeypatch, info)
    assert not calls and segs[0]["raw_text"] == "hello there"


def test_whisper_segments_have_subtitle_shape():
    seg = SimpleNamespace(start=1.0, end=2.5, text=" hi ")
    raw = segments_to_raw([seg, SimpleNamespace(start=3, end=4, text="  ")])
    assert len(raw) == 1
    assert set(raw[0]) == {
        "segment_index", "start_time", "end_time", "duration",
        "text_lines", "raw_text", "timestamp_line",
    }
    assert raw[0]["timestamp_line"] == "00:00:01.000 --> 00:00:02.500"


def test_force_audio_env_skips_good_subtitles(monkeypatch):
    monkeypatch.setenv("MEDIA_PIPELINE_FORCE_AUDIO", "1")
    info = {"subtitles": {"en": [{"ext": "vtt", "url": "u"}]}, "automatic_captions": {}}
    _, calls = _run(monkeypatch, info)
    assert calls
