"""The scanner: runs every check and decides the verdict.

scan(path) returns a dictionary, for example:
    {"verdict": "bomb", "score": 90,
     "reasons": ["zeros.bin grows 1000x (limit 100x)", ...]}
"""

import zipfile

import checks

# How many points each danger sign adds to the score (0 to 100).
# Strong signs (70) make a file a "bomb" on their own.
# Weaker signs (40) make it "suspicious", or a "bomb" when two add up.
POINTS = {
    "ratio": 40,
    "extreme_ratio": 40,  # comes on top of "ratio", so 80 in total
    "file_count": 40,
    "total_size": 70,
    "nested": 70,
    "refused": 40,        # Python could not open the file as a zip
}

# Every check, with the name used in POINTS.
CHECKS = [
    ("ratio", checks.check_ratio),
    ("extreme_ratio", checks.check_extreme_ratio),
    ("file_count", checks.check_file_count),
    ("total_size", checks.check_total_size),
    ("nested", checks.check_nested),
]

BOMB_SCORE = 70        # 70 or more -> "bomb"
SUSPICIOUS_SCORE = 30  # 30 to 69   -> "suspicious"


def scan(path):
    """Check one file and return its verdict, score and reasons."""
    reasons = []
    score = 0

    try:
        with zipfile.ZipFile(path) as z:
            for name, check in CHECKS:
                reason = check(z)
                if reason is not None:
                    reasons.append(reason)
                    score += POINTS[name]
    except zipfile.BadZipFile:
        reasons.append("Python refused to open it (broken or not a zip)")
        score += POINTS["refused"]

    score = min(score, 100)
    return {"verdict": get_verdict(score), "score": score, "reasons": reasons}


def list_files(path):
    """Return what the zip says about each file inside, biggest ratio first.

    Each item is a dictionary: name, zipped size, unzipped size, ratio.
    Returns an empty list if Python can't open the file as a zip.
    """
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
    except zipfile.BadZipFile:
        return []

    files = []
    for info in infos:
        if info.compress_size == 0:
            ratio = 0
        else:
            ratio = info.file_size / info.compress_size

        files.append({
            "name": info.filename,
            "zipped": info.compress_size,
            "unzipped": info.file_size,
            "ratio": ratio,
        })

    # Most suspicious files (highest ratio) at the top.
    files.sort(key=lambda f: f["ratio"], reverse=True)
    return files


def get_verdict(score):
    """Turn a score into "safe", "suspicious" or "bomb"."""
    if score >= BOMB_SCORE:
        return "bomb"
    if score >= SUSPICIOUS_SCORE:
        return "suspicious"
    return "safe"
