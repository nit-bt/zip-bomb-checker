"""Tests for scanner.py.

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


def test_ratio_bomb_is_bomb(ratio_zip):
    result = scanner.scan(ratio_zip)
    assert result["verdict"] == "bomb"
    assert len(result["reasons"]) == 2  # ratio + extreme ratio


def test_nested_zip_is_bomb(nested_zip):
    assert scanner.scan(nested_zip)["verdict"] == "bomb"


def test_many_files_is_suspicious(many_files_zip):
    assert scanner.scan(many_files_zip)["verdict"] == "suspicious"


def test_fake_zip_is_flagged(not_a_zip):
    result = scanner.scan(not_a_zip)
    assert result["verdict"] in ("suspicious", "bomb")
    assert result["score"] > 0


def test_score_never_above_100(many_files_zip, monkeypatch):
    import checks
    monkeypatch.setattr(checks, "MAX_TOTAL_SIZE", 0)
    monkeypatch.setattr(checks, "MAX_RATIO", 0)
    assert scanner.scan(many_files_zip)["score"] <= 100


# ---------- list_files ----------

def test_list_files_shows_sizes(ratio_zip):
    files = scanner.list_files(ratio_zip)
    assert len(files) == 1
    assert files[0]["name"] == "zeros.bin"
    assert files[0]["unzipped"] == 2_000_000
    assert files[0]["ratio"] > 100


def test_list_files_highest_ratio_first(normal_zip):
    files = scanner.list_files(normal_zip)
    assert files[0]["ratio"] >= files[-1]["ratio"]


def test_list_files_fake_zip_is_empty(not_a_zip):
    assert scanner.list_files(not_a_zip) == []
