import streamlit as st

from utils.practice import (
    get_chapters,
    get_words_by_chapter
)

st.set_page_config(
    page_title="Vocabulary Practice",
    page_icon="📚",
    layout="centered"
)

# ==========================================
# Session State
# ==========================================

defaults = {
    "practice_started": False,
    "current_index": 0,
    "show_meaning": False,
    "correct": 0,
    "wrong": 0,
    "wrong_words": [],
    "words": None,
    "chapter": None
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================
# Header
# ==========================================

left, middle, right = st.columns([2, 2, 1])

with left:

    chapters = get_chapters()

    chapter = st.selectbox(
        "📂 Chapter",
        chapters
    )

with middle:

    practice_mode = st.radio(
        "Practice Mode",
        [
            "Sequential",
            "Random"
        ],
        horizontal=True
    )

with right:

    st.metric(
        "Score",
        f"{st.session_state.correct}/{st.session_state.correct + st.session_state.wrong}"
    )

# ==========================================
# Start Practice
# ==========================================

if st.button(
    "🚀 Start Practice",
    use_container_width=True
):

    st.session_state.practice_started = True

    st.session_state.chapter = chapter

    st.session_state.words = get_words_by_chapter(
        chapter
    )
    if practice_mode == "Random":

    st.session_state.words = (
        st.session_state.words
        .sample(frac=1)
        .reset_index(drop=True)
    )

    st.session_state.current_index = 0

    st.session_state.correct = 0

    st.session_state.wrong = 0

    st.session_state.show_meaning = False

    st.session_state.wrong_words = []

    st.rerun()

# ==========================================
# Stop if Practice Not Started
# ==========================================

if not st.session_state.practice_started:

    st.info("Select a chapter and press Start Practice.")

    st.stop()
# ==========================================
# Load Current Word
# ==========================================

words = st.session_state.words

total = len(words)

if total == 0:

    st.warning("No words found in this chapter.")

    st.stop()

if st.session_state.current_index >= total:

    st.success("🎉 Practice Completed")

    st.stop()

row = words.iloc[
    st.session_state.current_index
]

remaining = total - (
    st.session_state.correct +
    st.session_state.wrong
)

# ==========================================
# Progress
# ==========================================

st.caption(
    f"Total: {total} | Remaining: {remaining}"
)

progress = (
    st.session_state.correct +
    st.session_state.wrong
) / total

st.progress(progress)

st.write("")

# ==========================================
# Main Practice Area
# ==========================================

left, right = st.columns(
    [5, 1]
)

with left:

    st.markdown(
        f"""
        <div style='
            text-align:center;
            margin-top:80px;
            margin-bottom:20px;
            font-size:48px;
            font-weight:bold;
        '>
            {row["korean"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='text-align:center;'>",
        unsafe_allow_html=True
    )

    if not st.session_state.show_meaning:

        if st.button(
            "👁 Show Meaning",
            use_container_width=False
        ):

            st.session_state.show_meaning = True

            st.rerun()

    else:

        st.markdown(
            f"""
            <div style='
                text-align:center;
                font-size:28px;
                font-weight:600;
                color:#00AA55;
                margin-top:15px;
            '>
                {row["bangla"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

with right:

    st.write("")
    st.write("")
    st.write("")

    if st.button(
        "✅",
        use_container_width=True
    ):

        st.session_state.correct += 1

        st.session_state.current_index += 1

        st.session_state.show_meaning = False

        st.rerun()

    if st.button(
        "❌",
        use_container_width=True
    ):

        st.session_state.wrong += 1

        st.session_state.wrong_words.append(
            row.to_dict()
        )

        st.session_state.current_index += 1

        st.session_state.show_meaning = False

        st.rerun()