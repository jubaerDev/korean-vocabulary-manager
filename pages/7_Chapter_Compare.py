import io
import pandas as pd
import streamlit as st

from utils.chapter_compare import (
    get_chapters,
    compare_chapters
)

st.set_page_config(
    page_title="Chapter Compare",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Chapter Compare")

st.write(
    "Compare two chapters and extract only the new words."
)

chapters = get_chapters()

col1, col2 = st.columns(2)

with col1:

    chapter_a = st.selectbox(
        "Chapter A",
        chapters,
        index=0
    )

with col2:

    chapter_b = st.selectbox(
        "Chapter B",
        chapters,
        index=1 if len(chapters) > 1
        else 0
    )
# ==========================================
# Compare Button
# ==========================================

if st.button(
    "🔍 Compare Chapters",
    use_container_width=True
):

    if chapter_a == chapter_b:

        st.warning(
            "Please select two different chapters."
        )

        st.stop()

    result = compare_chapters(
        chapter_a,
        chapter_b
    )

    st.success(
        f"Found {len(result)} unique words."
    )

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Unique Words",
        len(result)
    )

    st.session_state["compare_result"] = result

    st.session_state["chapter_b"] = chapter_b
# ==========================================
# Download Section
# ==========================================

if "compare_result" in st.session_state:

    result = st.session_state["compare_result"]

    chapter_b = st.session_state["chapter_b"]

    st.divider()

    st.subheader("⬇ Download")

    col1, col2 = st.columns(2)

    with col1:

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            result.to_excel(
                writer,
                index=False
            )

        st.download_button(
            label="📥 Download Excel",
            data=excel_buffer.getvalue(),
            file_name=f"{chapter_b}_Unique.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:

        csv = result.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{chapter_b}_Unique.csv",
            mime="text/csv",
            use_container_width=True
        )