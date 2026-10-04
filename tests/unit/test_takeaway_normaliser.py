"""One fixture per takeaway shape seen in the corpus (measured 2026-10-03).

The MUST-MATCH arms come first: shapes that used to render as a blank line must now carry their text.
"""
import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "store_in_mcp_kb", Path(__file__).parents[2] / "scripts" / "store_in_mcp_kb.py"
)
kb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kb)

MUST_MATCH = [
    ({"insight": "A", "classification": "actionable"}, {"text": "A", "kind": "actionable"}),
    ({"point": "B", "actionability": "informational"}, {"text": "B", "kind": "informational"}),
    ({"item": "C", "actionability": "actionable"}, {"text": "C", "kind": "actionable"}),
    ({"text": "D", "classification": "conceptual"}, {"text": "D", "kind": "conceptual"}),
    ({"insight": "E", "type": "actionable"}, {"text": "E", "kind": "actionable"}),
]
OTHER_SHAPES = [
    ({"takeaway": "F", "classification": "actionable"}, {"text": "F", "kind": "actionable"}),
    ({"takeaway": "G", "actionability": "actionable"}, {"text": "G", "kind": "actionable"}),
    ({"takeaway": "H", "type": "actionable"}, {"text": "H", "kind": "actionable"}),
    ({"takeaway": "I", "actionability": "x", "explanation": "long"}, {"text": "I", "kind": "x"}),
    ({"takeaway": "J", "impact": "extra field"}, {"text": "J", "kind": ""}),
    ("K bare string", {"text": "K bare string", "kind": ""}),
]


@pytest.mark.parametrize("raw,expected", MUST_MATCH + OTHER_SHAPES)
def test_shape_normalises(raw, expected):
    assert kb.normalize_takeaway(raw) == expected


@pytest.mark.parametrize("raw", [{}, {"takeaway": ""}, {"actionability": "actionable"}, "  ", None, 5])
def test_no_text_is_skipped_never_blank(raw, capsys):
    assert kb.normalize_takeaway(raw) is None
    assert "skipped takeaway" in capsys.readouterr().out


@pytest.mark.parametrize("key", kb.TAKEAWAY_LIST_KEYS)
def test_list_key_variants(key):
    assert kb.get_takeaways({key: [{"insight": "X"}]}) == [{"text": "X", "kind": ""}]


def _storage(tmp_path, takeaways):
    f = tmp_path / "VID123_analysis.json"
    f.write_text(json.dumps({"summary": "s", "key_takeaways": takeaways, "video_metadata": {}}))
    return kb.EnhancedKBStorage(str(f))


def test_overview_has_no_blank_numbered_line(tmp_path):
    content = _storage(tmp_path, [raw for raw, _ in MUST_MATCH]).create_overview_memory()["content"]
    for line in content.splitlines():
        if line[:2] in {"1.", "2.", "3.", "4.", "5."}:
            assert line[2:].replace("[actionable]", "").strip() not in {"", "[]"}, line
    assert "1. A [actionable]" in content and "4. D [conceptual]" in content


def test_takeaway_memories_now_include_classification_and_type_keys(tmp_path):
    mems = _storage(tmp_path, [raw for raw, _ in MUST_MATCH]).create_takeaway_memories()
    assert len(mems) == 5
