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

st.write("Upload your Korean Dictionary (Excel or CSV)")

uploaded_file = st.file_uploader(
    "Choose Excel or CSV File",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:

    try:

        # ---------- Read File ----------
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

                    try:
                        df = pd.read_csv(
                            uploaded_file,
                            header=None,
                            encoding="cp949"
                        )

                    except UnicodeDecodeError:

                        uploaded_file.seek(0)

                        df = pd.read_csv(
                            uploaded_file,
                            header=None,
                            encoding="latin1"
                        )

        else:

            df = pd.read_excel(
                uploaded_file,
                header=None
            )

        # ---------- Chapter ----------
        chapter = os.path.splitext(uploaded_file.name)[0]

        st.success(f"📁 Chapter : {chapter}")

        st.subheader("Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.info(f"📄 Total Rows : {len(df)}")

        if st.button("📥 Import Dictionary"):

            added, updated, skipped = import_dictionary(
                df,
                chapter
            )

            st.success("✅ Import Completed Successfully!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Added", added)

            with col2:
                st.metric("Updated", updated)

            with col3:
                st.metric("Skipped", skipped)

    except Exception as e:

        st.error(f"❌ {e}")

else:

    st.info("⬆️ Upload an Excel or CSV file to begin.")