import streamlit as st
import re
import pandas as pd
from collections import Counter

st.title("📄 Korean Word Extractor")

paragraph = st.text_area(
    "Paste Korean Paragraph",
    height=250
)

if st.button("Extract"):

    words = re.findall(r"[가-힣]+", paragraph)

    if len(words) == 0:
        st.warning("No Korean words found.")
        st.stop()

    counter = Counter(words)

    unique_words = sorted(counter.keys())

    data = []

    for word in unique_words:
        data.append(
            {
                "Word": word,
                "Frequency": counter[word]
            }
        )

    df = pd.DataFrame(data)

    st.success(f"Total Words : {len(words)}")
    st.success(f"Unique Words : {len(unique_words)}")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode("utf-8-sig"),
        "korean_words.csv",
        "text/csv"
    )