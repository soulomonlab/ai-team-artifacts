"""
News ingestion and summarization pipeline.
- Ingest from NewsAPI + RSS (feedparser)
- Summarize with HuggingFace BART (3-sentence abstractive)
- Save to SQLite summaries.db

Run: python news_summarizer.py --newsapi_key $NEWSAPI_KEY
"""
import os
import argparse
import sqlite3
import logging
from datetime import datetime, date
import requests
import feedparser
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HF imports deferred to avoid heavy deps if not used
try:
    from transformers import BartForConditionalGeneration, BartTokenizerFast
except Exception as e:
    BartForConditionalGeneration = None
    BartTokenizerFast = None

DB_PATH = os.environ.get("NEWS_DB_PATH", "summaries.db")
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
RSS_FEEDS = [
    "https://www.reuters.com/tools/rss",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    source TEXT,
    title TEXT,
    url TEXT UNIQUE,
    summary TEXT,
    created_at TEXT
);
"""


def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executescript(SCHEMA)
    conn.commit()
    conn.close()


def fetch_newsapi(api_key: str, query: str = "global market economy", page_size: int = 50) -> List[Dict]:
    headers = {"Authorization": api_key}
    params = {"q": query, "pageSize": page_size, "language": "en", "sortBy": "publishedAt"}
    r = requests.get(NEWSAPI_ENDPOINT, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "source": a.get("source", {}).get("name"),
            "title": a.get("title"),
            "url": a.get("url"),
            "content": a.get("content") or a.get("description") or "",
            "publishedAt": a.get("publishedAt")
        })
    return articles


def fetch_rss(feeds=RSS_FEEDS) -> List[Dict]:
    items = []
    for feed in feeds:
        d = feedparser.parse(feed)
        for e in d.entries:
            items.append({
                "source": d.feed.get("title"),
                "title": e.get("title"),
                "url": e.get("link"),
                "content": e.get("summary", ""),
                "publishedAt": e.get("published", "")
            })
    return items


class Summarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: str = "cpu"):
        if BartForConditionalGeneration is None:
            raise RuntimeError("transformers not installed")
        self.tokenizer = BartTokenizerFast.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
        self.device = device

    def summarize(self, texts: List[str], max_length: int = 130, min_length: int = 30, num_sentences: int = 3) -> List[str]:
        summaries = []
        for t in texts:
            input_ids = self.tokenizer([t], truncation=True, padding=True, return_tensors="pt").input_ids.to(self.device)
            summary_ids = self.model.generate(input_ids, num_beams=4, length_penalty=2.0, max_length=max_length, min_length=min_length, early_stopping=True)
            s = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            # heuristic: ensure ~num_sentences by splitting and trimming
            sentences = s.split('. ')
            s_short = '. '.join(sentences[:num_sentences]).strip()
            if not s_short.endswith('.'):
                s_short += '.'
            summaries.append(s_short)
        return summaries


def upsert_summary(conn: sqlite3.Connection, item: Dict, summary: str):
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        c.execute("INSERT INTO summaries (date, source, title, url, summary, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (date.today().isoformat(), item.get('source'), item.get('title'), item.get('url'), summary, now))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.debug("Duplicate URL, skipping: %s", item.get('url'))


def run_pipeline(newsapi_key: str = None, dry_run: bool = False):
    init_db()
    articles = []
    if newsapi_key:
        try:
            articles += fetch_newsapi(newsapi_key)
            logger.info("Fetched %d articles from NewsAPI", len(articles))
        except Exception as e:
            logger.warning("NewsAPI fetch failed: %s", e)
    try:
        rss_items = fetch_rss()
        articles += rss_items
        logger.info("Fetched %d articles from RSS", len(rss_items))
    except Exception as e:
        logger.warning("RSS fetch failed: %s", e)

    # filter and prepare text
    prepared = []
    for a in articles:
        text = (a.get('content') or '')
        if not text:
            continue
        if len(text.split()) < 30:
            continue
        prepared.append({'source': a.get('source'), 'title': a.get('title'), 'url': a.get('url'), 'text': text})

    logger.info("Prepared %d articles for summarization", len(prepared))
    if not prepared:
        return

    # load summarizer
    device = 'cuda' if os.environ.get('USE_CUDA') == '1' else 'cpu'
    summarizer = Summarizer(device=device)
    texts = [p['text'] for p in prepared]
    summaries = summarizer.summarize(texts)

    if dry_run:
        for p, s in zip(prepared, summaries):
            print(p['title'])
            print(s)
            print('---')
        return

    conn = sqlite3.connect(DB_PATH)
    for p, s in zip(prepared, summaries):
        upsert_summary(conn, p, s)
    conn.close()
    logger.info("Upserted %d summaries", len(summaries))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--newsapi_key', default=os.environ.get('NEWSAPI_KEY'))
    parser.add_argument('--dry_run', action='store_true')
    args = parser.parse_args()
    run_pipeline(args.newsapi_key, dry_run=args.dry_run)
