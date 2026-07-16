import streamlit as st

from utils.practice import (
    get_chapters,
    get_words_by_chapter
)

st.set_page_config(
    page_title="Vocabulary Practice",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Korean Vocabulary Practice")

st.write("Practice Korean vocabulary chapter by chapter.")

# ==========================================
# Session State
# ==========================================

if "practice_started" not in st.session_state:
    st.session_state.practice_started = False

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "wrong" not in st.session_state:
    st.session_state.wrong = 0

# ==========================================
# Chapter Selection
# ==========================================

chapters = get_chapters()

chapter = st.selectbox(
    "📂 Select Chapter",
    chapters
)

if st.button("🚀 Start Practice"):

    st.session_state.practice_started = True
    st.session_state.current_index = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.show_meaning = False

# ==========================================
# Load Words
# ==========================================

if st.session_state.practice_started:

    words = get_words_by_chapter(chapter)

    total = len(words)

    st.info(f"Total Words : {total}")

    if total == 0:

        st.warning("No words found.")

        st.stop()

    if st.session_state.current_index >= total:

        st.success("🎉 Chapter Finished")

        st.metric("Correct", st.session_state.correct)
        st.metric("Wrong", st.session_state.wrong)

        st.stop()

    row = words.iloc[
        st.session_state.current_index
    ]

    st.divider()

    st.subheader(row["korean"])

    if st.session_state.show_meaning:

        st.success(row["bangla"])

    else:

        st.info("Meaning Hidden")
# ==========================================
# Show Meaning
# ==========================================

col1, col2, col3 = st.columns(3)

with col2:

    if not st.session_state.show_meaning:

        if st.button(
            "👁 Show Meaning",
            use_container_width=True
        ):

            st.session_state.show_meaning = True
            st.rerun()

# ==========================================
# Correct / Wrong Buttons
# ==========================================

if st.session_state.show_meaning:

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "✅ I Know",
            use_container_width=True
        ):

            st.session_state.correct += 1

            st.session_state.current_index += 1

            st.session_state.show_meaning = False

            st.rerun()

    with c2:

        if st.button(
            "❌ I Don't Know",
            use_container_width=True
        ):

            st.session_state.wrong += 1

            st.session_state.current_index += 1

            st.session_state.show_meaning = False

            st.rerun()

# ==========================================
# Progress
# ==========================================

st.divider()

remaining = total - (
    st.session_state.correct +
    st.session_state.wrong
)

a, b, c = st.columns(3)

with a:

    st.metric(
        "✅ Correct",
        st.session_state.correct
    )

with b:

    st.metric(
        "❌ Wrong",
        st.session_state.wrong
    )

with c:

    st.metric(
        "📚 Remaining",
        remaining
    )

progress = (
    st.session_state.correct +
    st.session_state.wrong
) / total

st.progress(progress)
# ==========================================
# Wrong Word List
# ==========================================

if "wrong_words" not in st.session_state:

    st.session_state.wrong_words = []


# ==========================================
# Save Wrong Word
# ==========================================

if st.session_state.show_meaning:

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "✅ I Know",
            key="know_button",
            use_container_width=True
        ):

            st.session_state.correct += 1

            st.session_state.current_index += 1

            st.session_state.show_meaning = False

            st.rerun()

    with c2:

        if st.button(
            "❌ I Don't Know",
            key="dontknow_button",
            use_container_width=True
        ):

            st.session_state.wrong += 1

            st.session_state.wrong_words.append(
                row.to_dict()
            )

            st.session_state.current_index += 1

            st.session_state.show_meaning = False

            st.rerun()


# ==========================================
# Finish Screen
# ==========================================

if (
    st.session_state.practice_started
    and
    st.session_state.current_index >= total
):

    st.balloons()

    st.header("🎉 Practice Completed")

    total_answered = (
        st.session_state.correct
        +
        st.session_state.wrong
    )

    accuracy = 0

    if total_answered > 0:

        accuracy = round(
            st.session_state.correct
            /
            total_answered
            * 100,
            2
        )

    a, b, c = st.columns(3)

    with a:

        st.metric(
            "✅ Correct",
            st.session_state.correct
        )

    with b:

        st.metric(
            "❌ Wrong",
            st.session_state.wrong
        )

    with c:

        st.metric(
            "🎯 Accuracy",
            f"{accuracy}%"
        )

    # ======================================
    # Review Wrong Words
    # ======================================

    if len(st.session_state.wrong_words) > 0:

        st.divider()

        st.subheader("❌ Wrong Words")

        import pandas as pd

        wrong_df = pd.DataFrame(
            st.session_state.wrong_words
        )

        st.dataframe(
            wrong_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("🥳 Excellent! No wrong words.")

    st.stop()