"""Make sample files for the demo.

Run it:  python make_samples.py
It creates small files in the samples/ folder.

SAFETY:
    - Every sample is small (10 MB at most when unzipped).
    - Never double-click or unzip the samples. Only scan them.
    - samples/ is in .gitignore, so they never go to GitHub.
"""

import io
import zipfile
from pathlib import Path

SAMPLES = Path("samples")


def make_normal():
    """Two small text files: should be safe."""
    with zipfile.ZipFile(SAMPLES / "normal.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hello.txt", "Hello! This is a normal file.\n")
        z.writestr("notes.txt", "Some notes about the project.\n")


def make_docx():
    """A file laid out like a Word document: should be safe."""
    with zipfile.ZipFile(SAMPLES / "resume.docx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", "<w:document><w:t>My resume</w:t></w:document>")


def make_ratio_bomb():
    """10 MB of zeros that shrinks about 1,000x: the ratio check fires."""
    with zipfile.ZipFile(SAMPLES / "ratio_bomb.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("zeros.bin", b"\x00" * 10_000_000)


def make_many_files():
    """10,001 empty files: the file count check fires."""
    with zipfile.ZipFile(SAMPLES / "many_files.zip", "w", zipfile.ZIP_STORED) as z:
        for i in range(10_001):
            z.writestr(f"file_{i}.txt", "")


def make_nested():
    """A zip inside a zip inside a zip inside a zip: the nested check fires."""
    data = zip_in_memory("deepest.txt", b"bottom")
    for level in range(3):
        data = zip_in_memory(f"level_{level}.zip", data)
    (SAMPLES / "nested.zip").write_bytes(data)


def make_fake_zip():
    """A text file pretending to be a zip: Python refuses to open it."""
    (SAMPLES / "fake.zip").write_text("I am not really a zip file")


def zip_in_memory(name, data):
    """Make a zip holding one file, and return the zip's bytes."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(name, data)
    return buffer.getvalue()


def main():
    SAMPLES.mkdir(exist_ok=True)
    make_normal()
    make_docx()
    make_ratio_bomb()
    make_many_files()
    make_nested()
    make_fake_zip()
    print(f"Samples created in {SAMPLES}/")


if __name__ == "__main__":
    main()
