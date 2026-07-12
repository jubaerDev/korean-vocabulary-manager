import streamlit as st
from utils.extractor import extract_korean_words

st.title("📄 Korean Word Extractor")

paragraph = st.text_area(
    "Paste Korean Paragraph",
    height=250
)

if st.button("Extract"):

    words, df = extract_korean_words(paragraph)

    if len(words) == 0:
        st.warning("No Korean words found.")
        st.stop()

    st.metric("Total Words", len(words))
    st.metric("Unique Words", len(df))

    st.dataframe(df, use_container_width=True)