import sqlite3
from datetime import datetime


DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )


def search_word(word):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM dictionary
        WHERE korean=?
        """,
        (word,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def increase_search_count(word):

    conn = get_connection()

    conn.execute(
        """
        UPDATE dictionary
        SET search_count = search_count + 1
        WHERE korean=?
        """,
        (word,)
    )
    conn.commit()
    conn.close()
def add_word(
    korean,
    bangla,
    root="",
    chapter="Manual",
    source="Word Extractor"
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO dictionary
        (
            korean,
            root,
            bangla,
            english,
            pos,
            topik,
            chapter,
            frequency,
            source,
            created_at
        )

        VALUES
        (
            ?, ?, ?, '', '', '', ?, 0, ?, ?
        )
        """,
        (
            korean,
            root,
            bangla,
            chapter,
            source,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )


    conn.commit()
    conn.close()