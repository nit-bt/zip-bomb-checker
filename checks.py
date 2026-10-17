"""The danger checks.

Each check is one function. It gets an open zip file (z) and returns:
    - a short reason (text) if it finds danger
    - None if everything looks fine

How to look inside a zip without unzipping it:
    for info in z.infolist():
        info.filename       # name of the file inside, e.g. "word/document.xml"
        info.compress_size  # size INSIDE the zip (bytes)
        info.file_size      # size AFTER unzipping (bytes)

Python concepts: functions, for loops, if, sum(), len(), recursion.
"""

import io
import zipfile

# Limits. Change them here, not inside the functions.
MAX_RATIO = 100                 # a file may grow at most 100x
MAX_FILES = 10_000              # at most 10,000 files inside
MAX_TOTAL_SIZE = 1_000_000_000  # everything together at most 1 GB
MAX_DEPTH = 2                   # a zip inside a zip is OK, deeper is not


def check_ratio(z):
    """Step 2: does any file grow more than MAX_RATIO times?

    Hints:
        1. Loop over z.infolist().
        2. Skip files whose compress_size is 0 (you can't divide by 0).
        3. ratio = file_size / compress_size
        4. If ratio > MAX_RATIO, return a reason that includes the file name,
           e.g. f"{info.filename} grows {ratio:.0f}x (limit {MAX_RATIO}x)"
        5. After the loop, return None.
    """
    raise NotImplementedError("Step 2: write check_ratio")


def check_file_count(z):
    """Step 3: are there more than MAX_FILES files inside?

    Hints:
        1. count = len(z.infolist())
        2. If count > MAX_FILES, return a reason with the count in it.
        3. Otherwise return None.
    """
    raise NotImplementedError("Step 3: write check_file_count")


def check_total_size(z):
    """Step 4: do all files together unzip to more than MAX_TOTAL_SIZE?

    Hints:
        1. Add up info.file_size for every file (a loop, or sum()).
        2. If total > MAX_TOTAL_SIZE, return a reason with the total in it.
        3. Otherwise return None.
    """
    raise NotImplementedError("Step 4: write check_total_size")


def check_nested(z, depth=1):
    """Step 5: are there zips inside zips, deeper than MAX_DEPTH?

    This one uses recursion: the function calls itself on the inner zip.

    Hints:
        1. Loop over z.infolist().
        2. If info.filename ends with ".zip":
             a. If depth + 1 > MAX_DEPTH, return a reason (too deep).
             b. Safety: if info.file_size > 50_000_000, return a reason
                (don't load a huge inner zip into memory).
             c. Open the inner zip from memory:
                    inner = zipfile.ZipFile(io.BytesIO(z.read(info)))
             d. Call check_nested(inner, depth + 1).
                If it returns a reason, return that reason.
        3. After the loop, return None.
    """
    raise NotImplementedError("Step 5: write check_nested")
