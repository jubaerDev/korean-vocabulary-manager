import streamlit as st
import pandas as pd

from utils.grammar import extract_words
from utils.search import search_word, increase_search_count

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

    if text.strip() == "":
        st.warning("Please enter Korean text.")
        st.stop()

    words = extract_words(text)

    results = []

    for item in words:

        original = item["original"]
        root = item["root"]

        result = search_word(root)

        if result:

            increase_search_count(root)

            results.append({
                "Original": original,
                "Root": root,
                "Bangla": result["bangla"],
                "Status": "✅ Found"
            })

        else:

            results.append({
                "Original": original,
                "Root": root,
                "Bangla": "",
                "Status": "❌ Not Found"
            })

    df = pd.DataFrame(results)

    st.success(f"Extracted {len(df)} unique words.")

    st.dataframe(
        df,
        use_container_width=True
    )