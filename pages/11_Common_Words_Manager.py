import io
import pandas as pd
import streamlit as st

from utils.database import (
    import_common_word,
    total_common_words,
    get_all_common_words,
    delete_all_common_words,
    common_duplicate_count,
)

st.set_page_config(
    page_title="Common Words Manager",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Common Words Manager")
st.caption("Manage your Common Words Database")

# ==========================================
# DATABASE INFO
# ==========================================

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.metric(
        "Total Common Words",
        total_common_words()
    )

with info_col2:
    st.metric(
        "Duplicate Words",
        common_duplicate_count()
    )

st.divider()

# ==========================================
# LOAD DATABASE
# ==========================================

preview = get_all_common_words()

if preview.empty:
    preview = pd.DataFrame(
        columns=[
            "korean",
            "bangla",
            "english",
            "category"
        ]
    )
# ==========================================
# FILE UPLOAD
# ==========================================

st.divider()

st.subheader("📤 Import Common Words")

uploaded_file = st.file_uploader(
    "Choose Excel or CSV File",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            try:

                df = pd.read_csv(
                    uploaded_file,
                    header=None,
                    encoding="utf-8"
                )

            except UnicodeDecodeError:

                uploaded_file.seek(0)

                try:

                    df = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="utf-8-sig"
                    )

                except UnicodeDecodeError:

                    uploaded_file.seek(0)

                    df = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="cp949"
                    )

        else:

            df = pd.read_excel(
                uploaded_file,
                header=None
            )

        st.success(
            f"✅ {len(df)} rows loaded successfully."
        )

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(
            f"❌ Failed to read file.\n\n{e}"
        )

        df = None

else:

    df = None
# ==========================================
# IMPORT BUTTON
# ==========================================

if df is not None:

    st.divider()

    if st.button(
        "📥 Import Common Words",
        use_container_width=True
    ):

        progress = st.progress(0)

        status = st.empty()

        added = 0

        skipped = 0

        total_rows = len(df)

        for index, row in df.iterrows():

            korean = ""

            bangla = ""

            english = ""

            category = ""

            if len(row) > 0:
                korean = str(row.iloc[0]).strip()

            if len(row) > 1:
                bangla = str(row.iloc[1]).strip()

            if len(row) > 2:
                english = str(row.iloc[2]).strip()

            if len(row) > 3:
                category = str(row.iloc[3]).strip()

            if (
                korean == ""
                or
                korean.lower() in [
                    "korean",
                    "word",
                    "단어"
                ]
            ):
                skipped += 1
                continue

            import_common_word(
                korean=korean,
                bangla=bangla,
                english=english,
                category=category
            )

            added += 1

            progress.progress(
                (index + 1) / total_rows
            )

            status.text(
                f"Importing... {index + 1}/{total_rows}"
            )

        progress.empty()

        status.empty()

        st.success("✅ Import Completed")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Imported",
                added
            )

        with col2:
            st.metric(
                "Skipped",
                skipped
            )

        st.rerun()
# ==========================================
# SEARCH
# ==========================================

st.divider()

st.subheader("🔍 Search")

search = st.text_input(
    "Search Korean Word",
    placeholder="Type Korean word..."
)

preview = get_all_common_words()

if not preview.empty:

    if search.strip():

        preview = preview[
            preview["korean"]
            .astype(str)
            .str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

# ==========================================
# DATABASE PREVIEW
# ==========================================

st.divider()

left, right = st.columns([1, 1])

with left:

    st.subheader("📋 Database Preview")

with right:

    st.metric(
        "Showing",
        len(preview)
    )

# ==========================================
# EXPORT & DATABASE TOOLS
# ==========================================

st.divider()

st.subheader("⬇ Export & Database Tools")

tool_col1, tool_col2 = st.columns(2)

with tool_col1:

    if not preview.empty:

        csv_data = preview[
            ["korean", "bangla"]
        ].to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="📄 Export CSV (Flashcard)",
            data=csv_data,
            file_name="Common_Words.csv",
            mime="text/csv",
            use_container_width=True
        )

with tool_col2:
  
    if not preview.empty:

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
            label="📘 Export Excel",
            data=excel_buffer.getvalue(),
            file_name="Common_Words.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

st.divider()

danger_col1, danger_col2 = st.columns(2)

with danger_col1:

    if st.button(
        "🔄 Refresh Database",
        use_container_width=True
    ):

        st.rerun()

with danger_col2:

    if st.checkbox(
        "I understand this will delete ALL common words."
    ):

        if st.button(
            "🗑 Delete All Common Words",
            type="primary",
            use_container_width=True
        ):

            delete_all_common_words()

            st.success(
                "✅ All Common Words Deleted Successfully."
            )

            st.rerun()
# ==========================================
# MOBILE CARD VIEW
# ==========================================

st.divider()

st.subheader("📖 Common Words")

if preview.empty:

    st.info("No Common Words Found.")

else:

    for index, row in preview.iterrows():

        with st.container(border=True):

            top_left, top_right = st.columns([4, 1])

            with top_left:

                st.markdown(
                    f"### 🇰🇷 {row['korean']}"
                )

                bangla = row.get("bangla", "")

                if bangla:
                    st.write(f"🇧🇩 {bangla}")

                english = row.get("english", "")

                if english:
                    st.caption(english)

            with top_right:

                if st.button(
                    "✏",
                    key=f"edit_{index}",
                    use_container_width=True
                ):
                    st.info(
                        "Edit feature coming in Version 2."
                    )

                if st.button(
                    "🗑",
                    key=f"delete_{index}",
                    use_container_width=True
                ):
                    st.warning(
                        "Delete feature coming in Version 2."
                    )