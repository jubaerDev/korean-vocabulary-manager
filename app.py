import streamlit as st
import re
from collections import Counter
import pandas as pd

st.set_page_config(
    page_title="Korean Vocabulary Manager",
    page_icon="🇰🇷",
    layout="wide"
)

st.title("🇰🇷 Korean Vocabulary Manager")

st.write("Extract Korean words from any paragraph.")

paragraph = st.text_area(
    "Paste Korean Paragraph",
    height=250
)

if st.button("Extract Words"):

    # শুধুমাত্র Korean শব্দ বের করবে
    words = re.findall(r"[가-힣]+", paragraph)

    if not words:
        st.warning("No Korean words found.")
        st.stop()

    total_words = len(words)

    counter = Counter(words)

    unique_words = sorted(counter.keys())

    st.success(f"Total Words : {total_words}")
    st.success(f"Unique Words : {len(unique_words)}")

    data = []

    for word in unique_words:
        data.append({
            "Word": word,
            "Frequency": counter[word]
        })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    st.subheader("Word List")

    st.code("\n".join(unique_words))