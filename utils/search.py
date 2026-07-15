import sqlite3
from datetime import datetime

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )


# ==========================
# Search Original Word
# ==========================

def search_word(word):

    with get_connection() as conn:

        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM dictionary
            WHERE korean = ?
            """,
            (word,)
        )

        row = cur.fetchone()

    if row:
        return dict(row)

    return None


# ==========================
# Search Root Word
# ==========================

def search_root(root):

    with get_connection() as conn:

        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM dictionary
            WHERE root = ?
            """,
            (root,)
        )

        row = cur.fetchone()

    if row:
        return dict(row)

    return None


# ==========================
# Increase Search Count
# ==========================

def increase_search_count(word):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE dictionary
            SET search_count = search_count + 1
            WHERE korean = ?
            """,
            (word,)
        )

        conn.commit()


# ==========================
# Add New Word
# ==========================

def add_word(
    korean,
    bangla,
    root="",
    chapter="Manual",
    source="Word Extractor"
):

    if root == "":
        root = korean

    with get_connection() as conn:

        conn.execute(
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
                created_at,
                updated_at
            )

            VALUES
            (
                ?, ?, ?, '', '', '', ?, 0, ?, ?, ?
            )
            """,
            (
                korean,
                root,
                bangla,
                chapter,
                source,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()


# ==========================
# Update Existing Word
# ==========================

def update_word(
    korean,
    bangla
):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE dictionary
            SET
                bangla=?,
                updated_at=?
            WHERE korean=?
            """,
            (
                bangla,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                korean
            )
        )

        conn.commit()