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
- 5 checks:
  1. A file that grows more than 100x
  2. More than 10,000 files inside
  3. Total size over 1 GB
  4. Zips inside zips, more than 2 levels deep
  5. Python refuses to open it
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
| `checks.py` | The 4 danger checks (ratio, file count, total size, nested zips) |
| `scanner.py` | Runs the checks, adds up a score, gives the verdict |
| `app.py` | Web page: upload a file, see the result |
| `make_samples.py` | Makes small sample files for the demo |
| `tests/` | Automatic tests. Red = not done yet, green = works |
| `docs/bug_journal.md` | Every bug: problem, cause, fix |
| `docs/decisions.md` | Why we chose each limit and tool |

## Getting started (VS Code)

1. `Ctrl+Shift+P` → **Python: Create Environment** → **Venv**
2. Terminal (`` Ctrl+` ``): `pip install -r requirements.txt`
3. Run the tests: Testing panel (flask icon) → play button, or `pytest`

## Steps

1. Setup ✅
2. `check_ratio` in `checks.py`
3. `check_file_count`
4. `check_total_size`
5. `check_nested`
6. `scan` in `scanner.py`
7. Web page in `app.py`
8. Demo samples in `make_samples.py`

Each step has hints in the file. When a step is done, its tests turn green.
