import streamlit as st

from utils.extractor import extract_korean_words
from utils.exporter import (
    export_excel,
    export_csv,
    export_txt
)

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

    search = st.text_input("🔍 Search Word")

    if search:
        df = df[df["Word"].str.contains(search)]

    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "📥 Excel",
            export_excel(df),
            "korean_words.xlsx"
        )

    with col2:
        st.download_button(
            "📥 CSV",
            export_csv(df),
            "korean_words.csv"
        )

    with col3:
        st.download_button(
            "📥 TXT",
            export_txt(df),
            "korean_words.txt"
        )