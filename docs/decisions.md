# Decisions

Why we chose each number and tool. Use these to answer questions in class.

| Decision | Choice | Why |
| --- | --- | --- |
| Max ratio | 100x | Normal files shrink 3-10x, logs up to ~100x. More than 100x is suspicious. |
| Extreme ratio | 1,000x | Zip's compression can shrink a file at most ~1,032x. Past 1,000x the file is almost pure repetition, like a bomb. |
| Max files | 10,000 | Normal zips have tens or hundreds of files. |
| Max total size | 1 GB | Bigger than normal uploads, smaller than what crashes a small server. |
| Max depth | 2 | A zip inside a zip is normal. Deeper is the "42.zip" trick. |
| Python refuses it | Red flag | Python's zipfile blocks broken files and some bomb tricks. |
| Library | zipfile (built in) | Reads the list of files without unzipping them. |
| Web page | Streamlit | Pure Python, no HTML or JavaScript needed. |
| Tests | pytest | Simple `assert` statements. |
| Score | Strong signs 70, weaker signs 40 | Strong signs (total size, deep nesting) are a bomb on their own. Weaker signs (100x ratio, many files, broken file) alone are only suspicious, because some real files trigger them. |
| Verdict | 70+ bomb, 30-69 suspicious, under 30 safe | One weak sign = suspicious; two together = bomb. |
| Known limitation | We trust the sizes in the zip | Checking real sizes means unzipping in pieces; out of scope. |
