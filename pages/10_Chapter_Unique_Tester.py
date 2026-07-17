import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Chapter Unique Tester",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Chapter Unique Tester")

st.write(
    "Generate unique vocabulary using Common Words and two Chapters."
)

st.divider()

common_file = st.file_uploader(
    "📂 Common Words File",
    type=["xlsx", "csv"],
    key="common"
)

chapter1_file = st.file_uploader(
    "📂 Chapter 1",
    type=["xlsx", "csv"],
    key="chapter1"
)

chapter2_file = st.file_uploader(
    "📂 Chapter 2",
    type=["xlsx", "csv"],
    key="chapter2"
)

generate = st.button(
    "🚀 Generate",
    use_container_width=True
)
# ==========================================
# Read File
# ==========================================

def load_file(uploaded_file):

    if uploaded_file.name.lower().endswith(".csv"):

        try:
            df = pd.read_csv(
                uploaded_file,
                header=None,
                encoding="utf-8"
            )

        except:

            uploaded_file.seek(0)

            try:
                df = pd.read_csv(
                    uploaded_file,
                    header=None,
                    encoding="utf-8-sig"
                )

            except:

                uploaded_file.seek(0)

                try:
                    df = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="cp949"
                    )

                except:

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

    return df


# ==========================================
# Generate
# ==========================================

if generate:

    if (
        common_file is None
        or
        chapter1_file is None
        or
        chapter2_file is None
    ):

        st.warning(
            "Please select all three files."
        )

        st.stop()

    common_df = load_file(common_file)

    chapter1_df = load_file(chapter1_file)

    chapter2_df = load_file(chapter2_file)

    st.success("✅ Files loaded successfully.")

    st.write("Common Words :", len(common_df))
    st.write("Chapter 1 :", len(chapter1_df))
    st.write("Chapter 2 :", len(chapter2_df))
# ==========================================
# Clean Data
# ==========================================

def clean_words(df):

    # Keep only first two columns
    df = df.iloc[:, :2].copy()

    df.columns = [
        "korean",
        "bangla"
    ]

    # Convert to string
    df["korean"] = (
        df["korean"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["bangla"] = (
        df["bangla"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Remove empty rows
    df = df[
        df["korean"] != ""
    ]

    # Remove common header rows
    headers = [
        "korean",
        "bangla",
        "korean word",
        "serial",
        "번호",
        "단어",
        "뜻"
    ]

    df = df[
        ~df["korean"]
        .str.lower()
        .isin(headers)
    ]

    # Remove duplicate Korean words
    df = df.drop_duplicates(
        subset=["korean"]
    )

    df = df.reset_index(
        drop=True
    )

    return df


# Clean all files
common_df = clean_words(common_df)

chapter1_df = clean_words(chapter1_df)

chapter2_df = clean_words(chapter2_df)

st.success("✅ Data cleaned successfully.")

st.write("Common Words :", len(common_df))
st.write("Chapter 1 :", len(chapter1_df))
st.write("Chapter 2 :", len(chapter2_df))
# ==========================================
# Create Unique Chapters
# ==========================================

# Common word set
common_set = set(common_df["korean"])

# ----------------------------
# Chapter 1 Unique
# ----------------------------

chapter1_unique = chapter1_df[
    ~chapter1_df["korean"].isin(common_set)
].copy()

master_set = set(
    chapter1_unique["korean"]
)

# ----------------------------
# Chapter 2 Unique
# ----------------------------

chapter2_unique = chapter2_df[
    ~chapter2_df["korean"].isin(common_set)
].copy()

chapter2_unique = chapter2_unique[
    ~chapter2_unique["korean"].isin(master_set)
].copy()

# Update Master Set
master_set.update(
    chapter2_unique["korean"]
)

st.success("✅ Unique chapters created successfully.")

st.subheader("Result")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Chapter 1 Unique",
        len(chapter1_unique)
    )

    st.dataframe(
        chapter1_unique,
        use_container_width=True,
        hide_index=True,
        height=350
    )

with col2:

    st.metric(
        "Chapter 2 Unique",
        len(chapter2_unique)
    )

    st.dataframe(
        chapter2_unique,
        use_container_width=True,
        hide_index=True,
        height=350
    )
# ==========================================
# Download Files
# ==========================================

import io

st.divider()

st.subheader("⬇ Download Unique Chapters")

col1, col2 = st.columns(2)

# ==========================================
# Chapter 1
# ==========================================

with col1:

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        chapter1_unique.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "📥 Chapter1_Unique.xlsx",
        data=excel_buffer.getvalue(),
        file_name="Chapter1_Unique.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    csv = chapter1_unique.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "📄 Chapter1_Unique.csv",
        data=csv,
        file_name="Chapter1_Unique.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==========================================
# Chapter 2
# ==========================================

with col2:

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        chapter2_unique.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "📥 Chapter2_Unique.xlsx",
        data=excel_buffer.getvalue(),
        file_name="Chapter2_Unique.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    csv = chapter2_unique.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "📄 Chapter2_Unique.csv",
        data=csv,
        file_name="Chapter2_Unique.csv",
        mime="text/csv",
        use_container_width=True
    )