import streamlit as st
import pandas as pd

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
    type=["xlsx", "csv"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, header=None)
        else:
            df = pd.read_excel(uploaded_file, header=None)

        st.subheader("Preview")
        st.dataframe(df, use_container_width=True)
        st.write(f"📄 Total Rows : {len(df)}")

        if st.button("📥 Import Dictionary"):

            added, updated, skipped = import_dictionary(df)

            st.success("✅ Dictionary Imported Successfully!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Added", added)
            col2.metric("Updated", updated)
            col3.metric("Skipped", skipped)

    except Exception as e:

        st.error(f"❌ Error: {e}")
