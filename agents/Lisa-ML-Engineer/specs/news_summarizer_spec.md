Title: News Ingestion & LLM Summarizer — Spec

Objective
- Collect global market and economic news (NewsAPI + RSS: FT, WSJ, Reuters) and produce a 3-sentence abstractive summary per article/day.
- Expose summaries via API endpoint /api/v1/news/summary (backend owner: Marcus).
- Store daily summaries (per source + per day) for retrieval, audits, and monitoring.

Acceptance Criteria
- Pipeline ingests stories from NewsAPI and specified RSS feeds, deduplicates, and normalizes metadata.
- For each story produce a 3-sentence abstractive summary (coherent, factual, concise).
- Summaries stored daily (YYYY-MM-DD) as JSON lines + optional DB table.
- MLflow logging for runs: model name, model version, run_id, dataset counts, avg summary length, runtime.
- Latency: pipeline can process a day's ingestion within 4 hours (training limit note). Real-time endpoint (<100ms) is backend's responsibility.
- Monitoring: daily job emits counts and a simple quality metric (ROUGE-L on a small held-out dataset or heuristics) and drift detection.

Data Sources
- NewsAPI: newsapi.org — use everything endpoint, API key in env NEWSAPI_KEY.
- RSS: FT, WSJ, Reuters — fetch via feedparser. Keep feed URL list configurable.
- Deduplication: use URL + title fingerprint (hash) and fuzzy dedupe on normalized titles.

Design & Architecture
1) Ingest layer
   - NewsAPI fetch (paginated). RSS fetch via feedparser.
   - Normalize fields: id, title, url, source, published_at (UTC ISO), author, content, summary_placeholder.
   - Store raw fetch to a raw storage folder (S3 or local path) for audit: RAW_ROOT/{date}/{source}.jsonl

2) Preprocessing
   - Clean HTML, remove boilerplate, join description + content where needed.
   - If article content too long for summarizer, chunk (approx 800 tokens per chunk) and summarize each chunk, then combine.

3) Summarization
   - Use HuggingFace summarization pipeline (default: facebook/bart-large-cnn) for on-premise. Alternatives: pegusus or OpenAI if using API.
   - Generation config: max_length=60, min_length=25, num_beams=4, do_sample=False. Post-process to exactly 3 sentences:
       * Split output into sentences using a simple splitter (nlkt.sent_tokenize or regex). If fewer than 3 sentences, run a compress-with-length step or join multiple chunk summaries and re-summarize with target 3 sentences.
   - Log model name, tokenizer, and hyperparams to MLflow.

4) Storage
   - Primary: JSONL files per day: STORAGE_ROOT/summaries/YYYY-MM-DD.jsonl (each line = JSON with: id, title, url, source, published_at, summary, model, model_version, run_id).
   - Optional DB table (for Marcus): news_summaries(date DATE, id TEXT, title TEXT, url TEXT, source TEXT, published_at TIMESTAMP, summary TEXT, model TEXT, run_id TEXT) with index on date and source.

5) API contract (for backend)
   - GET /api/v1/news/summary?date=YYYY-MM-DD&source=Reuters|FT|WSJ|all&limit=50&offset=0
   - Response: {date:..., summaries: [{id, title, url, source, published_at, summary, model, run_id}], total}
   - Pagination: offset/limit. Cache recommended (Redis) for hot days.

Operational Details
- Scheduling: daily cron (e.g., 04:00 UTC) or run-on-demand. Use Airflow/Ray for scaling if needed.
- Config via environment variables / YAML config: NEWSAPI_KEY, FEED_URLS, STORAGE_ROOT, MLFLOW_TRACKING_URI, MODEL_NAME.
- MLflow: log per run metrics: num_articles, num_summaries, avg_summary_len, run_time_seconds.
- Monitoring: produce daily report with counts; drift detector script compares token distribution vs baseline and alerts if JS divergence > threshold.

Security & Compliance
- API keys in secrets manager (don't commit keys).
- Respect robots.txt and publisher terms. For paywalled FT/WSJ, RSS may only contain headlines — don't scrape paywalled content.

Trade-offs & Decisions
- Chosen model: facebook/bart-large-cnn — good tradeoff between quality and cost; runs offline on CPU with reasonable latency. If higher factuality is required, move to instruction-tuned LLM (OpenAI/gpt-4o-mini) or RAG with source attribution.
- Storage: JSONL chosen for simplicity and auditability. DB support included for easier API querying and indexing.

Next Steps for Backend (Marcus)
- Implement GET /api/v1/news/summary per API contract reading summaries from STORAGE_ROOT (or DB). Ensure caching and <100ms p95 for typical queries.
- Add auth and rate-limits as required.

Files created by ML/AI Engineer:
- output/code/ml/news_ingest_and_summarize.py
- output/specs/news_summarizer_spec.md

