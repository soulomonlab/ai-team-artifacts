"""
News ingestion module
- Fetches articles from NewsAPI and configured RSS feeds (FT, WSJ, Reuters)
- Stores raw articles into SQLite DB 'news_data.db' table raw_articles
- Avoids duplicates by URL

Usage:
    python news_ingest.py --date 2026-03-08

Environment variables expected:
- NEWSAPI_KEY (optional; NewsAPI requests are skipped if missing)

Dependencies: requests, feedparser, python-dateutil
"""

from typing import List, Optional
import os
import sqlite3
import requests
import feedparser
import hashlib
from datetime import datetime, timezone
from dateutil import parser as dateparser
import logging

DB_PATH = os.environ.get('NEWS_DB_PATH', 'news_data.db')
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')

RSS_FEEDS = {
    'ft': 'https://www.ft.com/?format=rss',
    'reuters': 'https://www.reutersagency.com/feed/?best-regions=global&post_type=best',
    # WSJ RSS is partly behind paywall; public feeds or site-specific feeds could be used instead
    'wsj': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml'
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _connect_db(path=DB_PATH):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS raw_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            source TEXT,
            title TEXT,
            content TEXT,
            published_at TEXT,
            fetched_at TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            summary TEXT,
            model TEXT,
            created_at TEXT,
            FOREIGN KEY(article_id) REFERENCES raw_articles(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS daily_aggregate (
            date TEXT PRIMARY KEY,
            summary TEXT,
            model TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    return conn


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _store_article(conn: sqlite3.Connection, source: str, title: str, content: str, url: str, published_at: Optional[str]):
    cur = conn.cursor()
    fetched_at = datetime.now(timezone.utc).isoformat()
    try:
        cur.execute(
            'INSERT OR IGNORE INTO raw_articles (url, source, title, content, published_at, fetched_at) VALUES (?, ?, ?, ?, ?, ?)',
            (url, source, title, content, published_at, fetched_at)
        )
        conn.commit()
        if cur.rowcount:
            logger.info('Stored article: %s', title[:120])
        else:
            logger.debug('Duplicate article skipped: %s', url)
    except Exception as e:
        logger.exception('Failed storing article: %s', e)


def fetch_newsapi(query: str = 'global markets OR economy', page_size: int = 100, from_date: Optional[str] = None) -> List[dict]:
    if not NEWSAPI_KEY:
        logger.warning('NEWSAPI_KEY not set; skipping NewsAPI fetch')
        return []
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'pageSize': page_size,
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': NEWSAPI_KEY
    }
    if from_date:
        params['from'] = from_date
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    articles = []
    for a in data.get('articles', []):
        articles.append({
            'source': a.get('source', {}).get('name'),
            'title': a.get('title'),
            'content': a.get('content') or a.get('description') or '',
            'url': a.get('url'),
            'publishedAt': a.get('publishedAt')
        })
    return articles


def fetch_rss(feeds: dict = RSS_FEEDS) -> List[dict]:
    results = []
    for name, feed_url in feeds.items():
        try:
            d = feedparser.parse(feed_url)
            for entry in d.entries:
                published = None
                if 'published' in entry:
                    try:
                        published = dateparser.parse(entry.published).isoformat()
                    except Exception:
                        published = None
                content = ''
                if 'content' in entry and entry.content:
                    content = entry.content[0].value
                elif 'summary' in entry:
                    content = entry.summary
                results.append({
                    'source': name,
                    'title': entry.get('title'),
                    'content': content,
                    'url': entry.get('link'),
                    'publishedAt': published
                })
        except Exception as e:
            logger.exception('Failed to parse RSS %s: %s', feed_url, e)
    return results


def fetch_and_store(target_date: Optional[str] = None):
    """Fetch news from sources and store into DB. target_date currently used to filter NewsAPI 'from' param.
    """
    conn = _connect_db()
    from_date = None
    if target_date:
        # ISO date
        from_date = target_date
    # Fetch
    newsapi_articles = fetch_newsapi(from_date=from_date)
    rss_articles = fetch_rss()
    total = 0
    for a in newsapi_articles + rss_articles:
        _store_article(conn, a.get('source'), a.get('title'), a.get('content') or '', a.get('url'), a.get('publishedAt'))
        total += 1
    logger.info('Fetched and stored %d articles', total)
    conn.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='ISO date YYYY-MM-DD to use as "from" filtering for NewsAPI', required=False)
    args = parser.parse_args()
    fetch_and_store(args.date)
