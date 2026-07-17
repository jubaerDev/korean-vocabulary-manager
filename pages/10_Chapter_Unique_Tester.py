import streamlit as st
import pandas as pd
import io


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Chapter Unique Tester",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 Chapter Unique Tester")

st.write(
    "Generate unique vocabulary using Common Words and Chapters."
)


st.divider()


# ==========================================
# FILE UPLOAD
# ==========================================

common_file = st.file_uploader(
    "📂 Upload Common Words",
    type=["xlsx", "csv"],
    key="common"
)


chapter1_file = st.file_uploader(
    "📂 Upload Chapter 1",
    type=["xlsx", "csv"],
    key="chapter1"
)


chapter2_file = st.file_uploader(
    "📂 Upload Chapter 2",
    type=["xlsx", "csv"],
    key="chapter2"
)


generate = st.button(
    "🚀 Generate",
    use_container_width=True
)



# ==========================================
# LOAD FILE FUNCTION
# ==========================================

def load_file(uploaded_file):

    if uploaded_file.name.lower().endswith(".csv"):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp949",
            "latin1"
        ]


        for enc in encodings:

            try:

                uploaded_file.seek(0)

                return pd.read_csv(
                    uploaded_file,
                    header=None,
                    encoding=enc
                )

            except:

                continue


        raise Exception(
            "CSV file encoding error"
        )


    else:

        return pd.read_excel(
            uploaded_file,
            header=None
        )



# ==========================================
# CLEAN WORD FUNCTION
# ==========================================

def clean_words(df):

    # Keep first two columns

    df = df.iloc[:, :2].copy()


    df.columns = [
        "korean",
        "bangla"
    ]


    # Convert string

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


    # Remove empty

    df = df[
        df["korean"] != ""
    ]


    # Remove headers

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


    # Remove duplicate

    df = df.drop_duplicates(
        subset=["korean"]
    )


    return df.reset_index(
        drop=True
    )
# ==========================================
# GENERATE PROCESS
# ==========================================

if generate:


    # Check files

    if (
        common_file is None
        or chapter1_file is None
        or chapter2_file is None
    ):

        st.warning(
            "⚠️ Please upload all three files."
        )

        st.stop()



    # ======================================
    # LOAD FILES
    # ======================================

    common_df = load_file(
        common_file
    )


    chapter1_df = load_file(
        chapter1_file
    )


    chapter2_df = load_file(
        chapter2_file
    )



    st.success(
        "✅ Files loaded successfully."
    )



    # ======================================
    # CLEAN DATA
    # ======================================

    common_df = clean_words(
        common_df
    )


    chapter1_df = clean_words(
        chapter1_df
    )


    chapter2_df = clean_words(
        chapter2_df
    )



    st.success(
        "✅ Data cleaned successfully."
    )



    # Show count

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Common Words",
            len(common_df)
        )


    with col2:

        st.metric(
            "Chapter 1",
            len(chapter1_df)
        )


    with col3:

        st.metric(
            "Chapter 2",
            len(chapter2_df)
        )



    st.divider()



    # ======================================
    # CREATE UNIQUE WORDS
    # ======================================


    # Common word set

    common_set = set(
        common_df["korean"]
    )



    # ======================================
    # CHAPTER 1 UNIQUE
    # ======================================


    chapter1_unique = chapter1_df[
        ~chapter1_df["korean"]
        .isin(common_set)
    ].copy()



    # Master set

    master_set = set(
        chapter1_unique["korean"]
    )



    # ======================================
    # CHAPTER 2 UNIQUE
    # ======================================


    chapter2_unique = chapter2_df[
        ~chapter2_df["korean"]
        .isin(common_set)
    ].copy()



    chapter2_unique = chapter2_unique[
        ~chapter2_unique["korean"]
        .isin(master_set)
    ].copy()



    st.success(
        "✅ Unique vocabulary created."
    )
# ==========================================
# RESULT DISPLAY
# ==========================================


    st.subheader(
        "📊 Unique Vocabulary Result"
    )


    result_col1, result_col2 = st.columns(2)



    # ======================================
    # CHAPTER 1 RESULT
    # ======================================

    with result_col1:


        st.metric(
            "Chapter 1 Unique Words",
            len(chapter1_unique)
        )


        st.dataframe(
            chapter1_unique,
            use_container_width=True,
            hide_index=True,
            height=400
        )



    # ======================================
    # CHAPTER 2 RESULT
    # ======================================

    with result_col2:


        st.metric(
            "Chapter 2 Unique Words",
            len(chapter2_unique)
        )


        st.dataframe(
            chapter2_unique,
            use_container_width=True,
            hide_index=True,
            height=400
        )



    st.divider()



    # ======================================
    # PREVIEW INFORMATION
    # ======================================


    st.subheader(
        "🔎 Preview Information"
    )


    preview_col1, preview_col2 = st.columns(2)



    with preview_col1:

        st.write(
            "Chapter 1 Preview (First 10 words)"
        )

        st.dataframe(
            chapter1_unique.head(10),
            use_container_width=True,
            hide_index=True
        )



    with preview_col2:

        st.write(
            "Chapter 2 Preview (First 10 words)"
        )

        st.dataframe(
            chapter2_unique.head(10),
            use_container_width=True,
            hide_index=True
        )
# ==========================================
# DOWNLOAD SECTION
# ==========================================


    st.subheader(
        "⬇ Download Unique Vocabulary"
    )


    download_col1, download_col2 = st.columns(2)



    # ======================================
    # CHAPTER 1 DOWNLOAD
    # ======================================

    with download_col1:


        st.write(
            "📘 Chapter 1 Unique"
        )


        # Excel

        excel_buffer1 = io.BytesIO()


        with pd.ExcelWriter(
            excel_buffer1,
            engine="openpyxl"
        ) as writer:


            chapter1_unique.to_excel(
                writer,
                index=False,
                sheet_name="Chapter1"
            )


        st.download_button(

            label="📥 Download Chapter1 Excel",

            data=excel_buffer1.getvalue(),

            file_name="Chapter1_Unique.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )



        # CSV

        csv1 = chapter1_unique.to_csv(
            index=False,
            encoding="utf-8-sig"
        )


        st.download_button(

            label="📄 Download Chapter1 CSV",

            data=csv1,

            file_name="Chapter1_Unique.csv",

            mime="text/csv",

            use_container_width=True

        )





    # ======================================
    # CHAPTER 2 DOWNLOAD
    # ======================================

    with download_col2:


        st.write(
            "📗 Chapter 2 Unique"
        )


        # Excel

        excel_buffer2 = io.BytesIO()


        with pd.ExcelWriter(
            excel_buffer2,
            engine="openpyxl"
        ) as writer:


            chapter2_unique.to_excel(
                writer,
                index=False,
                sheet_name="Chapter2"
            )


        st.download_button(

            label="📥 Download Chapter2 Excel",

            data=excel_buffer2.getvalue(),

            file_name="Chapter2_Unique.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )



        # CSV

        csv2 = chapter2_unique.to_csv(
            index=False,
            encoding="utf-8-sig"
        )


        st.download_button(

            label="📄 Download Chapter2 CSV",

            data=csv2,

            file_name="Chapter2_Unique.csv",

            mime="text/csv",

            use_container_width=True

        )# ==========================================
# DOWNLOAD SECTION
# ==========================================


    st.subheader(
        "⬇ Download Unique Vocabulary"
    )


    download_col1, download_col2 = st.columns(2)



    # ======================================
    # CHAPTER 1 DOWNLOAD
    # ======================================

    with download_col1:


        st.write(
            "📘 Chapter 1 Unique"
        )


        # Excel

        excel_buffer1 = io.BytesIO()


        with pd.ExcelWriter(
            excel_buffer1,
            engine="openpyxl"
        ) as writer:


            chapter1_unique.to_excel(
                writer,
                index=False,
                sheet_name="Chapter1"
            )


        st.download_button(

            label="📥 Download Chapter1 Excel",

            data=excel_buffer1.getvalue(),

            file_name="Chapter1_Unique.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )



        # CSV

        csv1 = chapter1_unique.to_csv(
            index=False,
            encoding="utf-8-sig"
        )


        st.download_button(

            label="📄 Download Chapter1 CSV",

            data=csv1,

            file_name="Chapter1_Unique.csv",

            mime="text/csv",

            use_container_width=True

        )





    # ======================================
    # CHAPTER 2 DOWNLOAD
    # ======================================

    with download_col2:


        st.write(
            "📗 Chapter 2 Unique"
        )


        # Excel

        excel_buffer2 = io.BytesIO()


        with pd.ExcelWriter(
            excel_buffer2,
            engine="openpyxl"
        ) as writer:


            chapter2_unique.to_excel(
                writer,
                index=False,
                sheet_name="Chapter2"
            )


        st.download_button(

            label="📥 Download Chapter2 Excel",

            data=excel_buffer2.getvalue(),

            file_name="Chapter2_Unique.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )



        # CSV

        csv2 = chapter2_unique.to_csv(
            index=False,
            encoding="utf-8-sig"
        )


        st.download_button(

            label="📄 Download Chapter2 CSV",

            data=csv2,

            file_name="Chapter2_Unique.csv",

            mime="text/csv",

            use_container_width=True

        )