"""
News ingestion and summarization pipeline
- Fetch from NewsAPI and RSS feeds
- Normalize, deduplicate, preprocess
- Summarize using HuggingFace transformers (facebook/bart-large-cnn)
- Store daily summaries as JSONL
- Log run info to MLflow

Usage:
    python news_ingest_and_summarize.py --date 2026-03-09

Environment variables:
    NEWSAPI_KEY, FEED_URLS (comma-separated), STORAGE_ROOT, MLFLOW_TRACKING_URI, MODEL_NAME

Note: This script is a production-ready starting point but requires proper secrets and infra (S3, DB, scheduler).
"""
import os
import sys
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import List, Dict

import feedparser
import requests
from tqdm import tqdm

# ML
import mlflow
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# NLP
import re


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def fetch_newsapi(api_key: str, query: str = 'economy OR market OR finance', page_size: int = 100, max_pages: int = 5) -> List[Dict]:
    articles = []
    base = 'https://newsapi.org/v2/everything'
    headers = {'Authorization': api_key}
    for page in range(1, max_pages + 1):
        params = {'q': query, 'pageSize': page_size, 'page': page, 'language': 'en', 'sortBy': 'publishedAt'}
        r = requests.get(base, params=params, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"NewsAPI error: {r.status_code} {r.text}", file=sys.stderr)
            break
        data = r.json()
        articles.extend(data.get('articles', []))
        if len(data.get('articles', [])) < page_size:
            break
    return articles


def fetch_rss(feed_urls: List[str]) -> List[Dict]:
    entries = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for e in feed.entries:
            entries.append({'title': e.get('title'), 'link': e.get('link'), 'published': e.get('published', ''), 'summary': e.get('summary', ''), 'source': feed.feed.get('title', url)})
    return entries


def normalize_newsapi_article(a: Dict) -> Dict:
    content = a.get('content') or a.get('description') or ''
    published = a.get('publishedAt')
    return {
        'id': a.get('url') or fingerprint(a.get('title', '') + (published or '')),
        'title': a.get('title'),
        'url': a.get('url'),
        'source': a.get('source', {}).get('name'),
        'published_at': published,
        'author': a.get('author'),
        'content': content,
        'fetched_at': now_iso(),
    }


def normalize_rss_entry(e: Dict) -> Dict:
    published = e.get('published')
    return {
        'id': e.get('link') or fingerprint(e.get('title', '') + (published or '')),
        'title': e.get('title'),
        'url': e.get('link'),
        'source': e.get('source'),
        'published_at': published,
        'author': None,
        'content': e.get('summary') or '',
        'fetched_at': now_iso(),
    }


def dedupe(articles: List[Dict]) -> List[Dict]:
    seen = set()
    out = []
    for a in articles:
        key = a.get('url') or (a.get('title') or '')
        fp = fingerprint(key)
        if fp in seen:
            continue
        seen.add(fp)
        out.append(a)
    return out


def clean_html(text: str) -> str:
    if not text:
        return ''
    # very simple cleaning
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r"\s+", ' ', text).strip()
    return text


def split_into_sentences(text: str) -> List[str]:
    # naive sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def ensure_three_sentences(summary_text: str, summarizer, max_attempts: int = 2) -> str:
    sents = split_into_sentences(summary_text)
    if len(sents) >= 3:
        return ' '.join(sents[:3])
    # If fewer than 3, try re-summarize with smaller max_length or summarize concatenated chunk outputs
    for attempt in range(max_attempts):
        out = summarizer(summary_text, max_length=75, min_length=30, do_sample=False)
        text = out[0].get('summary_text') if isinstance(out, list) else out
        sents = split_into_sentences(text)
        if len(sents) >= 3:
            return ' '.join(sents[:3])
    # fallback: return whatever we have, pad by splitting original text
    if sents:
        return ' '.join(sents + split_into_sentences(summary_text))[:300]
    return summary_text[:300]


def summarize_articles(articles: List[Dict], model_name: str, device: int = -1) -> List[Dict]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline('summarization', model=model, tokenizer=tokenizer, device=device)

    results = []
    for a in tqdm(articles, desc='Summarizing'):
        text = clean_html(a.get('content') or '')
        if not text:
            a['summary'] = ''
            results.append(a)
            continue
        # chunk if too long (naive by chars)
        if len(text) > 4000:
            chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
            chunk_summaries = []
            for c in chunks:
                out = summarizer(c, max_length=60, min_length=25, do_sample=False)
                chunk_summaries.append(out[0]['summary_text'])
            combined = ' '.join(chunk_summaries)
            summary = ensure_three_sentences(combined, summarizer)
        else:
            out = summarizer(text, max_length=60, min_length=25, do_sample=False)
            summary = ensure_three_sentences(out[0]['summary_text'], summarizer)
        a['summary'] = summary
        results.append(a)
    return results


def write_jsonl(path: str, items: List[Dict]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + '\n')


def main(date_str: str, newsapi_key: str, feed_urls: List[str], storage_root: str, model_name: str, mlflow_uri: str = None):
    start = time.time()
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)

    run = mlflow.start_run(run_name=f'news_summarizer_{date_str}')
    mlflow.log_param('date', date_str)
    mlflow.log_param('model_name', model_name)

    articles = []
    # NewsAPI
    if newsapi_key:
        try:
            n_articles = fetch_newsapi(newsapi_key)
            for a in n_articles:
                articles.append(normalize_newsapi_article(a))
        except Exception as e:
            print('NewsAPI fetch error', e, file=sys.stderr)

    # RSS
    if feed_urls:
        try:
            r_entries = fetch_rss(feed_urls)
            for e in r_entries:
                articles.append(normalize_rss_entry(e))
        except Exception as e:
            print('RSS fetch error', e, file=sys.stderr)

    before_dedupe = len(articles)
    articles = dedupe(articles)
    after_dedupe = len(articles)

    mlflow.log_metric('num_raw_articles', before_dedupe)
    mlflow.log_metric('num_deduped_articles', after_dedupe)

    # Summarize
    summarized = summarize_articles(articles, model_name)

    # attach model/run info
    run_id = run.info.run_id
    for s in summarized:
        s['model'] = model_name
        s['mlflow_run_id'] = run_id

    # write raw and summaries
    raw_path = os.path.join(storage_root, 'raw', date_str + '.jsonl')
    summary_path = os.path.join(storage_root, 'summaries', date_str + '.jsonl')
    write_jsonl(raw_path, articles)
    write_jsonl(summary_path, summarized)

    mlflow.log_artifact(summary_path)
    mlflow.log_metric('num_summaries', len(summarized))

    elapsed = time.time() - start
    mlflow.log_metric('run_time_seconds', elapsed)

    mlflow.end_run()
    print(f"Wrote {len(summarized)} summaries to {summary_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=False, default=datetime.utcnow().strftime('%Y-%m-%d'))
    parser.add_argument('--storage-root', default=os.getenv('STORAGE_ROOT', 'output/data'))
    parser.add_argument('--model-name', default=os.getenv('MODEL_NAME', 'facebook/bart-large-cnn'))
    parser.add_argument('--mlflow-uri', default=os.getenv('MLFLOW_TRACKING_URI'))
    parser.add_argument('--feed-urls', default=os.getenv('FEED_URLS', 'https://www.reuters.com/tools/rss,https://www.ft.com/?format=rss'))
    parser.add_argument('--newsapi-key', default=os.getenv('NEWSAPI_KEY'))
    args = parser.parse_args()

    feed_urls = [u.strip() for u in args.feed_urls.split(',') if u.strip()]

    main(args.date, args.newsapi_key, feed_urls, args.storage_root, args.model_name, args.mlflow_uri)
