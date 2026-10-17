"""Tests for checks.py.

Run them: Testing panel (flask icon) -> click the play button,
or type `pytest` in the terminal.

Red = not done yet (or a bug). Green = your check works.
"""

import zipfile

import checks


# ---------- Step 2: check_ratio ----------

def test_ratio_normal_zip_is_fine(normal_zip):
    with zipfile.ZipFile(normal_zip) as z:
        assert checks.check_ratio(z) is None


def test_ratio_catches_zeros(ratio_zip):
    with zipfile.ZipFile(ratio_zip) as z:
        reason = checks.check_ratio(z)
    assert reason is not None
    assert "zeros.bin" in reason


# ---------- Step 3: check_file_count ----------

def test_file_count_normal_zip_is_fine(normal_zip):
    with zipfile.ZipFile(normal_zip) as z:
        assert checks.check_file_count(z) is None


def test_file_count_catches_too_many(many_files_zip):
    with zipfile.ZipFile(many_files_zip) as z:
        reason = checks.check_file_count(z)
    assert reason is not None
    assert "10001" in reason.replace(",", "")


# ---------- Step 4: check_total_size ----------

def test_total_size_normal_zip_is_fine(normal_zip):
    with zipfile.ZipFile(normal_zip) as z:
        assert checks.check_total_size(z) is None


def test_total_size_catches_big(ratio_zip, monkeypatch):
    # Pretend the limit is 1 MB so a small test file can go over it.
    monkeypatch.setattr(checks, "MAX_TOTAL_SIZE", 1_000_000)
    with zipfile.ZipFile(ratio_zip) as z:
        assert checks.check_total_size(z) is not None


# ---------- Step 5: check_nested ----------

def test_nested_normal_zip_is_fine(normal_zip):
    with zipfile.ZipFile(normal_zip) as z:
        assert checks.check_nested(z) is None


def test_nested_catches_deep(nested_zip):
    with zipfile.ZipFile(nested_zip) as z:
        assert checks.check_nested(z) is not None
