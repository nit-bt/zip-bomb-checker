"""Make sample files for the demo (Step 8).

Run it:  python make_samples.py
It creates small files in the samples/ folder.

SAFETY:
    - Keep every sample small (a few MB at most when unzipped).
    - Never double-click or unzip the samples. Only scan them.
    - samples/ is in .gitignore, so they never go to GitHub.

Files to make:
    samples/normal.zip       two small text files       -> should be safe
    samples/resume.docx      looks like a Word file     -> should be safe
    samples/ratio_bomb.zip   10 MB of zeros             -> ratio check fires
    samples/many_files.zip   10,001 empty files         -> file count fires
    samples/nested.zip       zip in zip in zip          -> nested check fires

How to write a zip:
    import zipfile
    with zipfile.ZipFile("samples/normal.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hello.txt", "hello")        # name inside, content

10 MB of zeros:  b"\\x00" * 10_000_000

Tip: tests/conftest.py builds the same kinds of files. Read it for ideas.
"""

from pathlib import Path

SAMPLES = Path("samples")
SAMPLES.mkdir(exist_ok=True)

# Step 8: write the code that creates each sample here.
