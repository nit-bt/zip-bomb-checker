"""The scanner: runs every check and decides the verdict.

scan(path) returns a dictionary:
    {"verdict": "safe" / "suspicious" / "bomb",
     "score": 0 to 100,
     "reasons": ["...", "..."]}

Python concepts: try/except, lists, dictionaries, if/elif/else.
"""

import zipfile

import checks

# How many points each danger sign adds to the score.
POINTS = {
    "ratio": 40,
    "file_count": 30,
    "total_size": 50,
    "nested": 50,
    "refused": 60,   # Python could not open it
}


def scan(path):
    """Step 6: check one file and return the verdict.

    Hints:
        1. Start with: reasons = [] and score = 0
        2. Open the file inside try:
               with zipfile.ZipFile(path) as z:
        3. Inside the with, run each check from checks.py.
           For each one that returns a reason:
               reasons.append(reason)
               score += POINTS["ratio"]   (use the matching key)
        4. except zipfile.BadZipFile:
               reasons.append("Python refused to open it (broken or not a zip)")
               score += POINTS["refused"]
        5. Cap the score: score = min(score, 100)
        6. Verdict: 70 or more -> "bomb", 30 or more -> "suspicious",
           otherwise -> "safe"
        7. return {"verdict": verdict, "score": score, "reasons": reasons}
    """
    raise NotImplementedError("Step 6: write scan")
