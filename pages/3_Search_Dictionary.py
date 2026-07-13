import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "database/dictionary.db"

st.set_page_config(
    page_title="Search Dictionary",
    page_icon="🔍",
    layout="wide"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


conn = get_connection()

st.title("🔍 Dictionary Search & Manager")

# ============================
# Statistics
# ============================

total = conn.execute(
    "SELECT COUNT(*) FROM dictionary"
).fetchone()[0]

st.metric("📚 Total Words", total)

st.divider()

# ============================
# Add New Word
# ============================

with st.expander("➕ Add New Word"):

    korean = st.text_input("Korean Word")

    bangla = st.text_input("Bangla Meaning")

    chapter = st.text_input("Chapter (Optional)")

    if st.button("Add Word"):

        if korean.strip() == "" or bangla.strip() == "":

            st.warning("Please fill all required fields.")

        else:

            try:

                conn.execute(
                    """
                    INSERT INTO dictionary
                    (
                        korean,
                        root,
                        bangla,
                        english,
                        pos,
                        topik,
                        chapter,
                        frequency,
                        source,
                        created_at
                    )
                    VALUES
                    (
                        ?, ?, ?, '', '', '', ?, 0,
                        'Manual',
                        datetime('now')
                    )
                    """,
                    (
                        korean.strip(),
                        korean.strip(),
                        bangla.strip(),
                        chapter.strip()
                    )
                )

                conn.commit()

                st.success("✅ Word Added Successfully")

                st.rerun()

            except sqlite3.IntegrityError:

                st.error("❌ Word already exists.")

st.divider()

# ============================
# Search
# ============================

search = st.text_input(
    "Search Korean or Bangla"
)

query = """
SELECT
    id,
    korean,
    bangla,
    chapter
FROM dictionary
"""

params = ()

if search:

    query += """
    WHERE korean LIKE ?
       OR bangla LIKE ?
    """

    params = (
        f"%{search}%",
        f"%{search}%"
    )

query += " ORDER BY korean"

df = pd.read_sql_query(
    query,
    conn,
    params=params
)

st.success(f"Found {len(df)} word(s)")

# ============================
# Result
# ============================

for _, row in df.iterrows():

    with st.expander(f"🇰🇷 {row['korean']}"):

        bangla = st.text_input(
            "Bangla Meaning",
            value=row["bangla"],
            key=f"bangla_{row['id']}"
        )

        chapter = st.text_input(
            "Chapter",
            value=row["chapter"] if row["chapter"] else "",
            key=f"chapter_{row['id']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save",
                key=f"save_{row['id']}"
            ):

                conn.execute(
                    """
                    UPDATE dictionary
                    SET
                        bangla=?,
                        chapter=?
                    WHERE id=?
                    """,
                    (
                        bangla,
                        chapter,
                        row["id"]
                    )
                )

                conn.commit()

                st.success("Updated Successfully")

                st.rerun()

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{row['id']}"
            ):

                conn.execute(
                    """
                    DELETE FROM dictionary
                    WHERE id=?
                    """,
                    (
                        row["id"],
                    )
                )

                conn.commit()

                st.success("Deleted Successfully")

                st.rerun()

conn.close()