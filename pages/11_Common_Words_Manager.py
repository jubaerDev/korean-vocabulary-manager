import os
import pandas as pd
import streamlit as st

from utils.database import (
    import_common_word,
    total_common_words,
    get_all_common_words
)

st.set_page_config(
    page_title="Common Words Manager",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Common Words Manager")

st.write(
    "Manage your Common Words Database."
)

st.divider()

st.metric(
    "Total Common Words",
    total_common_words()
)

st.divider()

uploaded_file = st.file_uploader(
    "Choose Excel or CSV File",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:

    if uploaded_file.name.lower().endswith(".csv"):

        try:

            df = pd.read_csv(
                uploaded_file,
                header=None,
                encoding="utf-8"
            )

        except:

            uploaded_file.seek(0)

            df = pd.read_csv(
                uploaded_file,
                header=None,
                encoding="utf-8-sig"
            )

    else:

        df = pd.read_excel(
            uploaded_file,
            header=None
        )

    st.success(
        f"{len(df)} rows loaded."
    )
# ==========================================
# Search Common Word
# ==========================================

st.divider()

st.subheader("🔍 Search Common Word")

search = st.text_input(
    "Search Korean Word"
)

if search:

    preview = preview[
        preview["korean"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        df.head(10),
        use_container_width=True
    )
# ==========================================
# Export
# ==========================================

st.divider()

st.subheader("⬇ Export")

col1, col2 = st.columns(2)

with col1:

    csv = preview[
        ["korean", "bangla"]
    ].to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "📄 Export CSV (Flashcard)",
        data=csv,
        file_name="Common_Words.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:

    import io

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        preview.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "📘 Export Excel",
        data=excel_buffer.getvalue(),
        file_name="Common_Words.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    if st.button(
        "📥 Import Common Words",
        use_container_width=True
    ):

        added = 0

        for _, row in df.iterrows():

            korean = ""

            bangla = ""

            if len(row) > 0:

                korean = str(row.iloc[0]).strip()

            if len(row) > 1:

                bangla = str(row.iloc[1]).strip()

            if korean == "" or korean.lower() == "korean":

                continue

            import_common_word(
                korean,
                bangla
            )

            added += 1

        st.success(
            f"✅ {added} Common Words Imported."
        )

st.divider()

st.subheader("Database Preview")

preview = get_all_common_words()

st.dataframe(
    preview,
    use_container_width=True,
    height=500
)