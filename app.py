"""The web page.

Run it in the terminal:
    streamlit run app.py
It opens in your browser.
"""

import tempfile
from pathlib import Path

import streamlit as st

from scanner import list_files, scan

MAX_ROWS = 100  # a zip can hold thousands of files; show only the top ones

# How each verdict is shown: (Streamlit box, message)
DISPLAY = {
    "safe": (st.success, "Safe: no danger signs found."),
    "suspicious": (st.warning, "Suspicious: be careful with this file."),
    "bomb": (st.error, "Zip bomb: do not open this file."),
}

def readable_size(num_bytes):
    """Turn a number of bytes into text like '9.7 KB' or '10.0 MB'."""
    if num_bytes < 1024:
        return f"{num_bytes} bytes"

    for unit in ["KB", "MB", "GB"]:
        num_bytes /= 1024
        if num_bytes < 1024 or unit == "GB":
            return f"{num_bytes:,.1f} {unit}"


st.set_page_config(page_title="Zip Bomb Checker")
st.title("Zip Bomb Checker")
st.write("Upload a file to check it **before** anything opens it.")

uploaded = st.file_uploader(
    "Choose a file", type=["zip", "docx", "xlsx", "pptx"]
)

if uploaded is not None:
    # scan() needs a file on disk, so save the upload to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded.getvalue())
        temp_path = Path(tmp.name)

    try:
        result = scan(temp_path)
        files = list_files(temp_path)
    finally:
        temp_path.unlink()  # always delete the temporary file

    show_box, message = DISPLAY[result["verdict"]]
    show_box(message)
    st.metric("Risk score", f"{result['score']} / 100")

    if result["reasons"]:
        st.subheader("Why")
        for reason in result["reasons"]:
            st.write(f"- {reason}")

    # What the zip says about each file inside (read from its headers,
    # nothing is unzipped).
    if files:
        st.subheader(f"Files inside ({len(files):,})")
        rows = []
        for f in files[:MAX_ROWS]:
            rows.append({
                "File inside": f["name"],
                "Zipped": readable_size(f["zipped"]),
                "Unzipped": readable_size(f["unzipped"]),
                "Ratio": f"{f['ratio']:,.0f}x" if f["zipped"] > 0 else "–",
            })
        st.table(rows)
        if len(files) > MAX_ROWS:
            st.caption(f"Showing the {MAX_ROWS} files with the highest ratio.")
