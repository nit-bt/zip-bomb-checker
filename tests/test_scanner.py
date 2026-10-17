"""Tests for scanner.py (Step 6).

scan() should return a dictionary like:
    {"verdict": "safe", "score": 0, "reasons": []}
"""

import scanner


def test_normal_zip_is_safe(normal_zip):
    result = scanner.scan(normal_zip)
    assert result["verdict"] == "safe"
    assert result["score"] == 0
    assert result["reasons"] == []


def test_docx_is_safe(docx_file):
    assert scanner.scan(docx_file)["verdict"] == "safe"


def test_ratio_bomb_is_not_safe(ratio_zip):
    result = scanner.scan(ratio_zip)
    assert result["verdict"] in ("suspicious", "bomb")
    assert len(result["reasons"]) >= 1


def test_nested_zip_is_not_safe(nested_zip):
    assert scanner.scan(nested_zip)["verdict"] in ("suspicious", "bomb")


def test_fake_zip_is_flagged(not_a_zip):
    result = scanner.scan(not_a_zip)
    assert result["verdict"] in ("suspicious", "bomb")
    assert result["score"] > 0


def test_score_never_above_100(many_files_zip, monkeypatch):
    import checks
    monkeypatch.setattr(checks, "MAX_TOTAL_SIZE", 0)
    monkeypatch.setattr(checks, "MAX_RATIO", 0)
    assert scanner.scan(many_files_zip)["score"] <= 100
