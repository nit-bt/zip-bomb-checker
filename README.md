# Zip Bomb Checker

COSC 121 final project (in progress).

## What is a zip bomb?

A tiny file that becomes huge when unzipped. For example, a 45 KB file can turn into 5 GB or more, enough to fill a server's memory or disk and crash it.

It works because zip files store repeats very efficiently: "write 0, one billion times" takes almost no space. Normal files shrink 3–10x; a zip bomb shrinks 1,000x or more.

## Why it's a problem

The victims are **programs that open files automatically**: websites that preview or read uploads, email scanners, file converters. A Word file (`.docx`) is a zip too, so any site that reads uploaded Word files is unzipping them.

Most small websites only limit **upload size**. A zip bomb is tiny, so it gets through.

## Our goal

A Python program that checks a zip or Word file **before it is opened** and says **safe**, **suspicious** or **bomb**, and why.

## Scope

**We will build:**
- Support for `.zip`, `.docx`, `.xlsx`, `.pptx`
- 6 checks:
  1. A file that grows more than 100x
  2. A file that grows more than 1,000x (as much as zip can compress)
  3. More than 10,000 files inside
  4. Total size over 1 GB
  5. Zips inside zips, more than 2 levels deep
  6. Python refuses to open it
- A risk score and verdict with reasons
- A simple web page: upload a file, see the result
- Tests with small sample files

**We will not build:**
- Virus or malware scanning
- Other formats (`.rar`, `.7z`, `.tar.gz`)
- Safe extraction of files
- An API or admin dashboard

**Target:** small to medium websites that accept file uploads.

## Project files

| File | What it does |
| --- | --- |
| `checks.py` | The danger checks (ratio, extreme ratio, file count, total size, nested zips) |
| `scanner.py` | Runs the checks, adds up a score, gives the verdict |
| `app.py` | Web page: upload a file, see the result |
| `make_samples.py` | Makes small sample files for the demo |
| `tests/` | Automatic tests. Red = not done yet, green = works |
| `docs/bug_journal.md` | Every bug: problem, cause, fix |
| `docs/decisions.md` | Why we chose each limit and tool |

## How to run

In VS Code:

1. `Ctrl+Shift+P` → **Python: Create Environment** → **Venv**
2. Terminal (`` Ctrl+` ``): `pip install -r requirements.txt`
3. Make the sample files: `python make_samples.py`
4. Start the web page: `streamlit run app.py`
5. Upload a file from `samples/` and see the verdict

Run the tests: Testing panel (flask icon) → play button, or `pytest`.

## Results on the sample files

| File | Verdict | Score | Why |
| --- | --- | --- | --- |
| `normal.zip` | safe | 0 | |
| `resume.docx` | safe | 0 | |
| `many_files.zip` | suspicious | 40 | 10,001 files inside |
| `fake.zip` | suspicious | 40 | Python refused to open it |
| `nested.zip` | bomb | 70 | zips nested more than 2 levels deep |
| `ratio_bomb.zip` | bomb | 80 | grows 1,028x |

## Known limitation

The checks trust the sizes written inside the zip. A zip can lie about them. Catching that would mean unzipping in small pieces and counting the real bytes, which is outside our scope.
