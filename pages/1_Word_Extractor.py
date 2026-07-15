import streamlit as st
import pandas as pd

from utils.grammar import extract_words
from utils.search import (
    search_word,
    search_root,
    increase_search_count
)

st.set_page_config(
    page_title="Word Extractor",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Korean Word Extractor")

text = st.text_area(
    "Paste Korean Text",
    height=250
)

if st.button("🔍 Extract Words"):

    if not text.strip():
        st.warning("Please enter Korean text.")
        st.stop()

    words = extract_words(text)

    results = []

    for item in words:

        original = item["original"]
        root = item["root"]

        # ----------------------------------
        # Step 1 : Search Original Word
        # ----------------------------------

        result = search_word(original)

        found_by = ""

        # ----------------------------------
        # Step 2 : If not found search Root
        # ----------------------------------

        if result is None:

            result = search_root(root)

            if result:
                found_by = "Root"

        else:
            found_by = "Original"

        # ----------------------------------
        # Found
        # ----------------------------------

        if result:

            increase_search_count(result["korean"])

            results.append(
                {
                    "Original": original,
                    "Root": root,
                    "Bangla": result["bangla"],
                    "Matched": result["korean"],
                    "Found By": found_by,
                    "Status": "✅ Found"
                }
            )

        # ----------------------------------
        # Not Found
        # ----------------------------------

        else:

            results.append(
                {
                    "Original": original,
                    "Root": root,
                    "Bangla": "",
                    "Matched": "",
                    "Found By": "",
                    "Status": "❌ Not Found"
                }
            )

    df = pd.DataFrame(results)

    st.success(f"Extracted {len(df)} unique words.")

    st.dataframe(
        df,
        use_container_width=True
    )