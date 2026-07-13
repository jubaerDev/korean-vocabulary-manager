import os
import pandas as pd
import streamlit as st

from utils.importer import import_dictionary

st.set_page_config(
    page_title="Dictionary Manager",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Korean Dictionary Manager")

st.write("Upload one or more Excel / CSV files")

uploaded_files = st.file_uploader(
    "Choose Excel or CSV Files",
    type=["xlsx", "xls", "csv"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} file(s) selected")

    for file in uploaded_files:
        st.write("📄", file.name)

    if st.button("📥 Import All Files"):

        total_added = 0
        total_updated = 0
        total_skipped = 0

        progress = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):

            try:

                # Read File
                if uploaded_file.name.lower().endswith(".csv"):

                    try:
                        df = pd.read_csv(uploaded_file, header=None, encoding="utf-8")

                    except UnicodeDecodeError:

                        uploaded_file.seek(0)

                        try:
                            df = pd.read_csv(uploaded_file, header=None, encoding="utf-8-sig")

                        except UnicodeDecodeError:

                            uploaded_file.seek(0)

                            try:
                                df = pd.read_csv(uploaded_file, header=None, encoding="cp949")

                            except UnicodeDecodeError:

                                uploaded_file.seek(0)

                                df = pd.read_csv(uploaded_file, header=None, encoding="latin1")

                else:

                    df = pd.read_excel(uploaded_file, header=None)

                chapter = os.path.splitext(uploaded_file.name)[0]

                added, updated, skipped = import_dictionary(
                    df,
                    chapter
                )

                total_added += added
                total_updated += updated
                total_skipped += skipped

            except Exception as e:

                st.error(f"❌ {uploaded_file.name} : {e}")

            progress.progress((index + 1) / len(uploaded_files))

        st.success("✅ Import Finished")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Added", total_added)

        with col2:
            st.metric("Updated", total_updated)

        with col3:
            st.metric("Skipped", total_skipped)

else:

    st.info("⬆️ Select one or more Excel / CSV files.")