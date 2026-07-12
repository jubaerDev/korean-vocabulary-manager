import sqlite3
from datetime import datetime

from utils.database import create_database

DB_PATH = "database/dictionary.db"


def import_dictionary(df):

    create_database()

    # কমপক্ষে ২টি কলাম থাকতে হবে
    if len(df.columns) < 2:
        raise Exception("Excel/CSV ফাইলে কমপক্ষে ২টি কলাম থাকতে হবে।")

    # প্রথম দুইটি কলাম নিন
    df = df.iloc[:, :2].copy()

    df.columns = ["Korean", "Bangla"]

    # Header Detect
    korean_headers = [
        "korean",
        "word",
        "korean word",
        "한국어",
        "단어"
    ]

    bangla_headers = [
        "bangla",
        "বাংলা",
        "বাংলা অর্থ",
        "meaning",
        "bengali"
    ]

    if len(df) > 0:

        first_korean = str(df.iloc[0]["Korean"]).strip().lower()
        first_bangla = str(df.iloc[0]["Bangla"]).strip().lower()

        if first_korean in korean_headers or first_bangla in bangla_headers:
            df = df.iloc[1:].reset_index(drop=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    added = 0
    updated = 0
    skipped = 0

    for _, row in df.iterrows():

        korean = str(row["Korean"]).strip()
        bangla = str(row["Bangla"]).strip()

        if korean == "" or korean.lower() == "nan":
            skipped += 1
            continue

        if bangla == "" or bangla.lower() == "nan":
            skipped += 1
            continue

        cursor.execute(
            """
            SELECT id
            FROM dictionary
            WHERE korean=?
            """,
            (korean,)
        )

        result = cursor.fetchone()

        if result:

            cursor.execute(
                """
                UPDATE dictionary
                SET
                    bangla=?,
                    chapter=?
                WHERE korean=?
                """,
                (
                    bangla,
                    chapter,
                    korean
                )
            )

            updated += 1

        else:

            cursor.execute(
                """
                INSERT INTO dictionary
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
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    korean,               # korean
                    korean,               # root
                    bangla,               # bangla
                    "",                   # english
                    "",                   # pos
                    "",                   # topik
                    chapter,              # chapter
                    0,                    # frequency
                    "Manual Import",      # source
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            added += 1

    conn.commit()
    conn.close()

    return added, updated, skipped