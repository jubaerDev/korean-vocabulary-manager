import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"

st.set_page_config(
    page_title="Search Dictionary",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Search Dictionary")

search = st.text_input(
    "Search Korean or Bangla",
    placeholder="যেমন: 학교 অথবা স্কুল"
)

if search:

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT korean, bangla
    FROM dictionary
    WHERE korean LIKE ?
       OR bangla LIKE ?
    ORDER BY korean
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(f"%{search}%", f"%{search}%")
    )

    conn.close()

    st.success(f"{len(df)} টি Word পাওয়া গেছে")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
