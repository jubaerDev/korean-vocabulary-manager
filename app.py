import streamlit as st

st.set_page_config(
    page_title="Korean Vocabulary Manager",
    page_icon="🇰🇷",
    layout="wide"
)

st.title("🇰🇷 Korean Vocabulary Manager")

st.markdown("""
### Welcome

This application helps you:

- Extract Korean words
- Remove duplicate words
- Count word frequency
- Export Excel
- Export CSV
- Export TXT

---
""")

st.info("Choose a page from the sidebar.")