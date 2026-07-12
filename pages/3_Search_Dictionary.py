import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"

st.set_page_config(
    page_title="Search Dictionary",
    page_icon="🔍",
    layout="wide"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


st.title("📚 Dictionary Search & Manager")

conn = get_connection()

# -------------------------------
# Add New Word
# -------------------------------
with st.expander("➕ Add New Word"):

    new_korean = st.text_input("Korean Word")
    new_bangla = st.text_input("Bangla Meaning")

    if st.button("Add Word"):

        if new_korean.strip() == "" or new_bangla.strip() == "":
            st.warning("সব ঘর পূরণ করুন।")

        else:

            try:

                conn.execute(
                    """
                    INSERT INTO dictionary
                    (korean,bangla)
                    VALUES (?,?)
                    """,
                    (
                        new_korean.strip(),
                        new_bangla.strip()
                    )
                )

                conn.commit()

                st.success("Word Added Successfully")

            except sqlite3.IntegrityError:

                st.error("এই Word আগে থেকেই আছে।")

# -------------------------------
# Search
# -------------------------------

search = st.text_input(
    "🔍 Search Korean / Bangla"
)

query = """
SELECT rowid,korean,bangla
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

st.write(f"### Total Result : {len(df)}")

# -------------------------------
# Edit / Delete
# -------------------------------

for _, row in df.iterrows():

    with st.expander(f"🇰🇷 {row['korean']}"):

        bangla = st.text_input(
            "Bangla",
            value=row["bangla"],
            key=f"bangla_{row['rowid']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save",
                key=f"save_{row['rowid']}"
            ):

                conn.execute(
                    """
                    UPDATE dictionary
                    SET bangla=?
                    WHERE rowid=?
                    """,
                    (
                        bangla,
                        row["rowid"]
                    )
                )

                conn.commit()

                st.success("Updated Successfully")

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{row['rowid']}"
            ):

                conn.execute(
                    """
                    DELETE FROM dictionary
                    WHERE rowid=?
                    """,
                    (
                        row["rowid"],
                    )
                )

                conn.commit()

                st.success("Deleted Successfully")
                st.rerun()

conn.close()
    conn.close()

    st.success(f"{len(df)} টি Word পাওয়া গেছে")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
