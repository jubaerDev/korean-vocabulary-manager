import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


def get_chapters():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT DISTINCT chapter
        FROM dictionary
        ORDER BY chapter
        """,
        conn
    )

    conn.close()

    return df["chapter"].tolist()


def get_words(chapter):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            korean,
            bangla
        FROM dictionary
        WHERE chapter=?
        """,
        conn,
        params=(chapter,)
    )

    conn.close()

    return df
def compare_chapters(
    chapter_a,
    chapter_b
):

    df_a = get_words(chapter_a)

    df_b = get_words(chapter_b)

    # Remove duplicate words
    df_a = df_a.drop_duplicates(
        subset=["korean"]
    )

    df_b = df_b.drop_duplicates(
        subset=["korean"]
    )

    # Find words that exist only in Chapter B
    unique_df = df_b[
        ~df_b["korean"].isin(
            df_a["korean"]
        )
    ].copy()

    # Sort alphabetically
    unique_df = unique_df.sort_values(
        by="korean"
    ).reset_index(drop=True)

    return unique_df