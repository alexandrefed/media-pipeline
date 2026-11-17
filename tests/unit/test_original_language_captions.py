"""A video with dubbed audio tracks is transcribed from its ORIGINAL language. No network."""

from types import SimpleNamespace

import src.pipeline.raw_transcript_extractor as rte


def _vtt(tag):
    return f"WEBVTT\n\n00:00:01.000 --> 00:00:02.500\n{tag}\n"


class FakeYDL:
    """urlopen echoes the track url, so the chosen track is visible in the text."""

    def __init__(self, info):
        self.info = info

    def __call__(self, opts):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def extract_info(self, url, download=False):
        return self.info

    def urlopen(self, url):
        return SimpleNamespace(read=lambda: _vtt(url).encode())


def _chosen(monkeypatch, info):
    monkeypatch.setattr(rte.yt_dlp, "YoutubeDL", FakeYDL(info))
    ex = rte.RawTranscriptExtractor()
    ex._transcribe_audio = lambda url: [{"raw_text": "from audio"}]
    return ex.extract_raw_segments("https://youtu.be/x")[0]["raw_text"]


def _auto(*langs):
    return {lang: [{"ext": "vtt", "url": lang}] for lang in langs}


def test_en_orig_beats_ar_orig_when_language_is_en(monkeypatch):
    info = {"language": "en", "subtitles": {}, "automatic_captions": _auto("ar-orig", "en-orig")}
    assert _chosen(monkeypatch, info) == "en-orig"


def test_regional_language_code_is_normalised(monkeypatch):
    info = {"language": "en-US", "subtitles": {}, "automatic_captions": _auto("ar-orig", "en-orig")}
    assert _chosen(monkeypatch, info) == "en-orig"


def test_en_orig_beats_ar_orig_when_language_unknown(monkeypatch):
    info = {"subtitles": {}, "automatic_captions": _auto("ar-orig", "en-orig")}
    assert _chosen(monkeypatch, info) == "en-orig"


def test_video_language_wins_over_en_orig(monkeypatch):
    info = {"language": "fr", "subtitles": {}, "automatic_captions": _auto("en-orig", "fr-orig")}
    assert _chosen(monkeypatch, info) == "fr-orig"


def test_manual_en_still_wins(monkeypatch):
    info = {
        "language": "fr",
        "subtitles": _auto("en"),
        "automatic_captions": _auto("fr-orig", "en-orig"),
    }
    assert _chosen(monkeypatch, info) == "en"
