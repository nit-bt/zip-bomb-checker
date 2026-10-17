"""The web page (Step 7).

Run it in the terminal:
    streamlit run app.py
It opens in your browser.

What the page does:
    1. Show a title.
    2. Let the user upload a .zip, .docx, .xlsx or .pptx file.
    3. Save it to a temporary file and call scanner.scan() on it.
    4. Show the verdict in color and list the reasons.

Useful Streamlit commands:
    st.title("text")
    uploaded = st.file_uploader("label", type=["zip", "docx", "xlsx", "pptx"])
    uploaded.getvalue()      # the file's bytes
    st.success("text")       # green box
    st.warning("text")       # orange box
    st.error("text")         # red box
    st.write("text")

Saving the upload so scan() can read it:
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded.getvalue())
        path = tmp.name
"""

import streamlit as st

import scanner

st.title("Zip Bomb Checker")
st.write("Upload a file to check it before opening it.")

# Step 7: write the rest here.
