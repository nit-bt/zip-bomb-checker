"""Test files the tests use.

pytest runs these automatically. Each one builds a SMALL zip in a
temporary folder that is deleted after the test. You don't need to
change anything here.
"""

import io
import zipfile

import pytest


@pytest.fixture
def normal_zip(tmp_path):
    """A normal zip: two small text files."""
    path = tmp_path / "normal.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hello.txt", "Hello! This is a normal file.\n")
        z.writestr("notes.txt", "Some notes about the project.\n")
    return path


@pytest.fixture
def docx_file(tmp_path):
    """A small zip named .docx, laid out like a Word file."""
    path = tmp_path / "resume.docx"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", "<w:document><w:t>My resume</w:t></w:document>")
    return path


@pytest.fixture
def ratio_zip(tmp_path):
    """2 MB of zeros. Shrinks about 1,000x, so the ratio check should fire."""
    path = tmp_path / "ratio.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("zeros.bin", b"\x00" * 2_000_000)
    return path


@pytest.fixture
def many_files_zip(tmp_path):
    """10,001 empty files: one more than the limit."""
    path = tmp_path / "many.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        for i in range(10_001):
            z.writestr(f"file_{i}.txt", "")
    return path


def _zip_bytes(name, data):
    """Helper: make a zip in memory and return its bytes."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(name, data)
    return buffer.getvalue()


@pytest.fixture
def nested_zip(tmp_path):
    """A zip inside a zip inside a zip inside a zip (4 levels)."""
    inner = _zip_bytes("deepest.txt", "bottom")
    for level in range(3):
        inner = _zip_bytes(f"level_{level}.zip", inner)
    path = tmp_path / "nested.zip"
    path.write_bytes(inner)
    return path


@pytest.fixture
def not_a_zip(tmp_path):
    """A text file pretending to be a zip."""
    path = tmp_path / "fake.zip"
    path.write_text("I am not really a zip file")
    return path
