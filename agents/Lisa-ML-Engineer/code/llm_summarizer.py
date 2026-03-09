"""
LLM summarization pipeline
- Loads raw articles from SQLite DB 'news_data.db' table raw_articles
- Generates 3-sentence abstractive summaries per article using an LLM backend
- Stores per-article summaries into summaries table and creates daily aggregate summary

Design decisions:
- Default LLM is OpenAI (via openai python package). If OPENAI_API_KEY not set, falls back to a local HuggingFace model using transformers pipeline (e.g., facebook/bart-large-cnn) if available.
- Abstractive 3-sentence summary enforced by instruction prompt; not extractive.
- Summaries deduplicated by article_id.

Usage:
    python llm_summarizer.py --date 2026-03-08

Dependencies: openai, transformers, sentencepiece (optional), sqlite3
"""

from typing import Optional, List
import os
import sqlite3
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DB_PATH = os.environ.get('NEWS_DB_PATH', 'news_data.db')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')

try:
    import openai
except Exception:
    openai = None

try:
    from transformers import pipeline
except Exception:
    pipeline = None

PROMPT_TEMPLATE = (
    "Summarize the following news article into exactly 3 concise sentences. Use abstractive summarization. Do not hallucinate facts. If information is missing, say 'insufficient information'.\n\nArticle:\n{content}\n\nSummary:")


def _connect_db(path=DB_PATH):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn


def _get_unprocessed_articles(conn: sqlite3.Connection, target_date: Optional[str] = None):
    cur = conn.cursor()
    q = 'SELECT id, title, content, url, published_at FROM raw_articles WHERE id NOT IN (SELECT article_id FROM summaries)'
    params = ()
    if target_date:
        q = 'SELECT id, title, content, url, published_at FROM raw_articles WHERE DATE(published_at) = ? AND id NOT IN (SELECT article_id FROM summaries)'
        params = (target_date,)
    cur.execute(q, params)
    rows = cur.fetchall()
    return rows


def _store_summary(conn: sqlite3.Connection, article_id: int, summary: str, model: str):
    cur = conn.cursor()
    cur.execute('INSERT INTO summaries (article_id, summary, model, created_at) VALUES (?, ?, ?, ?)',
                (article_id, summary, model, datetime.now(timezone.utc).isoformat()))
    conn.commit()


def _create_daily_aggregate(conn: sqlite3.Connection, date_str: str, summary: str, model: str):
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO daily_aggregate (date, summary, model, created_at) VALUES (?, ?, ?, ?)',
                (date_str, summary, model, datetime.now(timezone.utc).isoformat()))
    conn.commit()


def summarize_with_openai(content: str, model: str = OPENAI_MODEL) -> str:
    if not openai:
        raise RuntimeError('openai package not installed')
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = OPENAI_API_KEY
    prompt = PROMPT_TEMPLATE.format(content=content)
    # Use chat completion
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=200,
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()


def summarize_with_local(content: str) -> str:
    if not pipeline:
        raise RuntimeError('transformers not available')
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    out = summarizer(content, max_length=150, min_length=60, do_sample=False)
    return out[0]['summary_text']


def generate_daily_aggregate(summaries: List[str]) -> str:
    # Simple heuristics: join summaries and ask LLM to condense to 3 sentences
    joined = '\n'.join(summaries[:30])  # limit to first 30 to avoid token overflow
    prompt = 'Condense the following article summaries into a 3-sentence market summary:\n\n' + joined
    if OPENAI_API_KEY and openai:
        openai.api_key = OPENAI_API_KEY
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=200,
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    else:
        # fallback: naive join-first-3
        return ' '.join(summaries[:3])


def run(target_date: Optional[str] = None):
    conn = _connect_db()
    rows = _get_unprocessed_articles(conn, target_date)
    logger.info('Found %d unprocessed articles', len(rows))
    processed_summaries = []
    model_used = 'openai' if OPENAI_API_KEY and openai else 'local'
    for r in rows:
        article_id, title, content, url, published_at = r
        text = content or title or ''
        if not text.strip():
            logger.info('Skipping article %s - no content', url)
            continue
        try:
            if model_used == 'openai':
                summary = summarize_with_openai(text)
            else:
                summary = summarize_with_local(text)
            _store_summary(conn, article_id, summary, model_used)
            processed_summaries.append(summary)
            logger.info('Summarized article id=%d', article_id)
        except Exception as e:
            logger.exception('Failed summarizing article %s: %s', url, e)
    # Create daily aggregate if target_date or if we processed any today
    if target_date and processed_summaries:
        aggregate = generate_daily_aggregate(processed_summaries)
        _create_daily_aggregate(conn, target_date, aggregate, model_used)
        logger.info('Created daily aggregate for %s', target_date)
    conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='ISO date YYYY-MM-DD to summarize', required=False)
    args = parser.parse_args()
    run(args.date)
