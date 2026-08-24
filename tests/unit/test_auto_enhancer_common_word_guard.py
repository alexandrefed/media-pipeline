"""Regression tests for the auto-enhancer's ordinary-English-word guard.

Background: `learning/processing_knowledge_base.json` is an untracked, live data
file, so nothing in review sees a new correction being added to it. Two rules of
the same shape have already reached production and silently corrupted the corpus:

  * "file"/"value" -> "FAL"  — 39 of 100 enhanced transcripts, caught May 2026.
  * "zero" -> "v0"           — 21 files, ran three months longer; the raw corpus
    has 58 legitimate uses of "zero" and zero uses of "v0".

Removing the offending entries does not stop the next one, so the *shape* is
refused: a single-token correction whose left-hand side is a dictionary word is
skipped unless explicitly allow-listed. These tests pin that behaviour.
"""

import json

import pytest

from src.processing.auto_enhancer import AutoEnhancer


def _kb(common_errors: dict, allow: list | None = None) -> dict:
    return {
        "transcription_corrections": {
            "common_errors": common_errors,
            "allow_common_words": allow or [],
            "contextual_corrections": {},
        }
    }


def _enhancer(tmp_path, common_errors, allow=None) -> AutoEnhancer:
    path = tmp_path / "kb.json"
    path.write_text(json.dumps(_kb(common_errors, allow)), encoding="utf-8")
    return AutoEnhancer(str(path))


@pytest.mark.skipif(
    not AutoEnhancer._english_words(),
    reason="no system dictionary available; the guard fails open by design",
)
class TestCommonWordGuard:
    def test_historical_fal_bug_cannot_be_reintroduced(self, tmp_path):
        e = _enhancer(tmp_path, {"file": "FAL", "value": "FAL"})

        assert sorted(e.skipped_common_words) == ["file", "value"]
        text = "create a file named dashboard.py and read the value"
        assert e.enhance_transcript(text).enhanced_text == text

    def test_zero_to_v0_is_refused(self, tmp_path):
        e = _enhancer(tmp_path, {"zero": "v0"})

        assert e.skipped_common_words == ["zero"]
        assert e.enhance_transcript("costs zero tokens").enhanced_text == (
            "costs zero tokens"
        )

    def test_nonsense_asr_tokens_still_corrected(self, tmp_path):
        """The guard must not disarm the enhancer's actual job."""
        e = _enhancer(tmp_path, {"aent": "agent", "clawed.md": "CLAUDE.md"})

        assert e.skipped_common_words == []
        assert e.enhance_transcript("one aent").enhanced_text == "one agent"

    def test_multi_word_rules_are_never_guarded(self, tmp_path):
        """"clawed code" -> "Claude Code" is unambiguous; only single tokens rewrite prose."""
        e = _enhancer(tmp_path, {"cloud code": "Claude Code"})

        assert e.skipped_common_words == []
        assert e.enhance_transcript("open cloud code").enhanced_text == (
            "open Claude Code"
        )

    def test_allow_list_is_the_deliberate_escape_hatch(self, tmp_path):
        """'clawed' -> 'Claude' is a real ASR artefact here (37 raw hits), so it opts in."""
        e = _enhancer(tmp_path, {"clawed": "Claude"}, allow=["clawed"])

        assert e.skipped_common_words == []
        assert e.enhance_transcript("ask clawed").enhanced_text == "ask Claude"

    def test_case_only_normalisation_is_not_a_rewrite(self, tmp_path):
        """'anthropic' -> 'Anthropic' changes no word, so the guard leaves it alone."""
        e = _enhancer(tmp_path, {"anthropic": "Anthropic"})

        assert e.skipped_common_words == []
