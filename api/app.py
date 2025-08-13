from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "books.db")

app = FastAPI(title="Book Search API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(
    q: Optional[str] = Query(default="", description="검색어"),
    category: Optional[str] = Query(default=None, description="카테고리"),
    sort: str = Query(default="relevance", pattern="^(relevance|title|author|date)$"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
):
        # category 필터링 로직 수정
    if category:
        # category = ? 대신 LIKE ? 와 %를 사용하여 '해당 숫자로 시작하는' 모든 데이터를 찾습니다.
        base_query += " AND category LIKE ?"
        params.append(f'{category}%')
    
    conn = get_connection()
    try:
        where_clauses = ["1=1"]
        params = []

        if q:
            like = f"%{q}%"
            where_clauses.append("(title LIKE ? OR author LIKE ? OR publisher LIKE ? OR description LIKE ?)")
            params.extend([like, like, like, like])

        if category:
            where_clauses.append("category = ?")
            params.append(category)

        where_sql = " AND ".join(where_clauses)

        if sort == "title":
            order_sql = "ORDER BY title COLLATE NOCASE ASC"
        elif sort == "author":
            order_sql = "ORDER BY author COLLATE NOCASE ASC"
        elif sort == "date":
            order_sql = "ORDER BY publish_date DESC"
        else:
            # relevance 대용: 최신순을 기본으로 사용
            order_sql = "ORDER BY publish_date DESC"

        # total count
        count_sql = f"SELECT COUNT(*) as cnt FROM books WHERE {where_sql}"
        cur = conn.execute(count_sql, params)
        total = cur.fetchone()[0]

        # pagination
        offset = (page - 1) * size
        query_sql = f"""
            SELECT id, title, author, publisher, category, publish_date, description
            FROM books
            WHERE {where_sql}
            {order_sql}
            LIMIT ? OFFSET ?
        """
        query_params = params + [size, offset]
        cur = conn.execute(query_sql, query_params)
        rows = [dict(r) for r in cur.fetchall()]

        return {
            "total": total,
            "page": page,
            "size": size,
            "items": rows,
        }
    finally:
        conn.close()