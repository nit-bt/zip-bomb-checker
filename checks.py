"""The danger checks.

Each check gets an open zip file and returns:
    - a short reason (text) if it finds a danger sign
    - None if everything looks fine

None of the checks unzip the files. They only read the zip's list of
files, which stores each file's name, zipped size and unzipped size.
"""

import io
import zipfile

# Limits. Change them here, not inside the functions.
MAX_RATIO = 100                 # a file may grow at most 100x
EXTREME_RATIO = 1_000           # normal compression almost never goes past ~1000x
MAX_FILES = 10_000              # at most 10,000 files inside
MAX_TOTAL_SIZE = 1_000_000_000  # everything together at most 1 GB
MAX_DEPTH = 2                   # a zip inside a zip is OK, deeper is not
MAX_INNER_ZIP = 50_000_000      # never load an inner zip bigger than 50 MB


def check_ratio(z):
    """Return a reason if any file grows more than MAX_RATIO times."""
    for info in z.infolist():
        # Skip empty files: we can't divide by zero.
        if info.compress_size == 0:
            continue

        ratio = info.file_size / info.compress_size
        if ratio > MAX_RATIO:
            return f"{info.filename} grows {ratio:.0f}x (limit {MAX_RATIO}x)"

    return None


def check_extreme_ratio(z):
    """Return a reason if any file grows more than EXTREME_RATIO times.

    Zip's normal compression (DEFLATE) can shrink a file at most about
    1,032 times. Growing more than 1,000x means the file is almost pure
    repetition, the way zip bombs are built.
    """
    for info in z.infolist():
        if info.compress_size == 0:
            continue

        ratio = info.file_size / info.compress_size
        if ratio > EXTREME_RATIO:
            return f"{info.filename} grows {ratio:.0f}x, as much as zip can compress"

    return None


def check_file_count(z):
    """Return a reason if the zip holds more than MAX_FILES files."""
    count = len(z.infolist())

    if count > MAX_FILES:
        return f"{count:,} files inside (limit {MAX_FILES:,})"
    return None


def check_total_size(z):
    """Return a reason if all files together unzip to more than MAX_TOTAL_SIZE."""
    total = 0
    for info in z.infolist():
        total += info.file_size

    if total > MAX_TOTAL_SIZE:
        return f"unzips to {total:,} bytes (limit {MAX_TOTAL_SIZE:,})"
    return None


def check_nested(z, depth=1):
    """Return a reason if zips are nested deeper than MAX_DEPTH.

    This uses recursion: when we find a zip inside the zip, the function
    calls itself on that inner zip, one level deeper.
    """
    for info in z.infolist():
        if not info.filename.lower().endswith(".zip"):
            continue

        if depth + 1 > MAX_DEPTH:
            return f"zips nested more than {MAX_DEPTH} levels deep"

        # Don't load a huge inner zip into memory just to look inside it.
        if info.file_size > MAX_INNER_ZIP:
            return f"{info.filename} is a very large zip inside the zip"

        # Open the inner zip from memory, without saving it to disk.
        try:
            inner = zipfile.ZipFile(io.BytesIO(z.read(info)))
        except zipfile.BadZipFile:
            return f"{info.filename} is a broken zip inside the zip"

        reason = check_nested(inner, depth + 1)
        if reason is not None:
            return reason

    return None
