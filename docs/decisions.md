# Decisions

Why we chose each number and tool. Use these to answer questions in class.

| Decision | Choice | Why |
| --- | --- | --- |
| Max ratio | 100x | Normal files shrink 3-10x, logs up to ~100x. More than 100x is suspicious. |
| Max files | 10,000 | Normal zips have tens or hundreds of files. |
| Max total size | 1 GB | Bigger than normal uploads, smaller than what crashes a small server. |
| Max depth | 2 | A zip inside a zip is normal. Deeper is the "42.zip" trick. |
| Python refuses it | Red flag | Python's zipfile blocks broken files and some bomb tricks. |
| Library | zipfile (built in) | Reads the list of files without unzipping them. |
| Web page | Streamlit | Pure Python, no HTML or JavaScript needed. |
| Tests | pytest | Simple `assert` statements. |
