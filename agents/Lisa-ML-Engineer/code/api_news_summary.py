"""
FastAPI app exposing /api/v1/news/summary
- GET /api/v1/news/summary?date=YYYY-MM-DD returns the daily aggregate summary if exists
- GET /api/v1/news/articles?date=YYYY-MM-DD returns list of article summaries for that day

Usage:
    uvicorn api_news_summary:app --reload --port 8000

Dependencies: fastapi, uvicorn, pydantic
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
import os
from typing import Optional, List

DB_PATH = os.environ.get('NEWS_DB_PATH', 'news_data.db')
app = FastAPI(title='News Summary API')

class DailySummary(BaseModel):
    date: str
    summary: str
    model: str
    created_at: str

class ArticleSummary(BaseModel):
    article_id: int
    title: Optional[str]
    url: Optional[str]
    summary: str
    model: str
    created_at: str


def _connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get('/api/v1/news/summary', response_model=DailySummary)
def get_daily_summary(date: str = Query(..., description='YYYY-MM-DD')):
    conn = _connect_db()
    cur = conn.cursor()
    cur.execute('SELECT date, summary, model, created_at FROM daily_aggregate WHERE date = ?', (date,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail='Summary not found for date')
    return DailySummary(date=row['date'], summary=row['summary'], model=row['model'], created_at=row['created_at'])

@app.get('/api/v1/news/articles', response_model=List[ArticleSummary])
def get_article_summaries(date: str = Query(..., description='YYYY-MM-DD')):
    conn = _connect_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT s.article_id, a.title, a.url, s.summary, s.model, s.created_at
        FROM summaries s
        JOIN raw_articles a ON a.id = s.article_id
        WHERE DATE(a.published_at) = ?
    ''', (date,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail='No article summaries for date')
    results = []
    for r in rows:
        results.append(ArticleSummary(article_id=r[0], title=r[1], url=r[2], summary=r[3], model=r[4], created_at=r[5]))
    return results

