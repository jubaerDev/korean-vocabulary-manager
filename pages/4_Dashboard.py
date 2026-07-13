import streamlit as st
import pandas as pd

from utils.dashboard import (
    get_total_words,
    get_total_chapters,
    get_favorite_words,
    get_recent_words,
    get_chapter_statistics
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Korean Vocabulary Dashboard")

# ===========================
# Statistics
# ===========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📚 Total Words",
        get_total_words()
    )

with col2:
    st.metric(
        "📖 Total Chapters",
        get_total_chapters()
    )

with col3:
    st.metric(
        "⭐ Favorite Words",
        get_favorite_words()
    )

st.divider()

# ===========================
# Chapter Statistics
# ===========================

st.subheader("📖 Words per Chapter")

chapter_df = get_chapter_statistics()

if len(chapter_df) > 0:

    st.bar_chart(
        chapter_df.set_index("chapter")["total"]
    )

    st.dataframe(
        chapter_df,
        use_container_width=True
    )

else:

    st.info("No chapter data found.")

st.divider()

# ===========================
# Recent Imported Words
# ===========================

st.subheader("🆕 Recently Added Words")

recent_df = get_recent_words(20)

if len(recent_df) > 0:

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("Dictionary is empty.")

st.divider()

st.success("✅ Dashboard Loaded Successfully")