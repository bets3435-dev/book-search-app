import argparse
import csv
import os
import sqlite3
from typing import Dict

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "books.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    publisher TEXT,
    category TEXT,
    publish_date TEXT,
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_books_publisher ON books(publisher);
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category);
CREATE INDEX IF NOT EXISTS idx_books_publish_date ON books(publish_date);
"""

INSERT_SQL = (
    "INSERT INTO books (title, author, publisher, category, publish_date, description) "
    "VALUES (?, ?, ?, ?, ?, ?)"
)

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def load_csv(
    csv_path: str,
    delimiter: str,
    field_map: Dict[str, str],
    encoding: str = "utf-8-sig",
    batch_size: int = 5000,
):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("DELETE FROM books")
        conn.commit()

        with open(csv_path, "r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            missing = [src for src in field_map.values() if src not in reader.fieldnames]
            if missing:
                raise ValueError(f"CSV header missing required columns: {missing}")

            buffer = []
            total = 0
            for row in reader:
                title = (row.get(field_map["title"], "") or "").strip()
                author = (row.get(field_map["author"], "") or "").strip()
                publisher = (row.get(field_map["publisher"], "") or "").strip()
                category = (row.get(field_map["category"], "") or "").strip()
                publish_date = (row.get(field_map["publish_date"], "") or "").strip()
                description = (row.get(field_map["description"], "") or "").strip()

                buffer.append((title, author, publisher, category, publish_date, description))
                if len(buffer) >= batch_size:
                    conn.executemany(INSERT_SQL, buffer)
                    conn.commit()
                    total += len(buffer)
                    print(f"Inserted: {total}")
                    buffer.clear()

            if buffer:
                conn.executemany(INSERT_SQL, buffer)
                conn.commit()
                total += len(buffer)
                print(f"Inserted: {total}")

        print("Done.")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Load CSV into SQLite for Book Search API")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default ',')")
    parser.add_argument("--encoding", default="utf-8-sig", help="CSV encoding (default utf-8-sig)")

    # CSV 헤더명 매핑
    parser.add_argument("--title", default="title", help="CSV column name for title")
    parser.add_argument("--author", default="author", help="CSV column name for author")
    parser.add_argument("--publisher", default="publisher", help="CSV column name for publisher")
    parser.add_argument("--category", default="category", help="CSV column name for category")
    parser.add_argument("--publish_date", default="publish_date", help="CSV column name for publish_date")
    parser.add_argument("--description", default="description", help="CSV column name for description")

    args = parser.parse_args()

    ensure_db()

    field_map = {
        "title": args.title,
        "author": args.author,
        "publisher": args.publisher,
        "category": args.category,
        "publish_date": args.publish_date,
        "description": args.description,
    }

    load_csv(
        csv_path=args.csv,
        delimiter=args.delimiter,
        field_map=field_map,
        encoding=args.encoding,
    )


if __name__ == "__main__":
    main() 