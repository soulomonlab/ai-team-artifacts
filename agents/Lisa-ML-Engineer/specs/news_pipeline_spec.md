# News Ingestion & LLM Summarizer Spec

Summary
- Ingest global market/economic news via NewsAPI + RSS (FT, Reuters, WSJ-ish). Use NewsAPI key if provided; RSS always attempted.
- Generate 3-sentence abstractive summaries per article and a daily aggregate summary.
- Expose API endpoints: /api/v1/news/summary and /api/v1/news/articles
- Store in SQLite (dev). For prod, migrate to Postgres/Cloud DB.

Requirements
- Daily summaries stored per date (YYYY-MM-DD)
- Summaries should be deduplicated and not re-generated if already present
- LLM choice: OpenAI (preferred) else local transformer model
- Acceptance: API returns daily summary (200) for existing date; list of article summaries; system logs errors

Files created
- output/code/news_ingest.py
- output/code/llm_summarizer.py
- output/code/api_news_summary.py

Operational notes
- Environment variables: NEWSAPI_KEY, OPENAI_API_KEY, NEWS_DB_PATH
- Cron: run news_ingest daily (e.g., 00:10 UTC) then run llm_summarizer with the same date
- Monitoring: log counts; track summarization failures; ML monitoring to be added later

Next steps
- #ai-data -> Samantha: provide historical news dump (3 months) for backfill and test
- #ai-backend -> Marcus: integrate API file into backend service, add auth and caching
- #ai-devops -> Noah: add cron/airflow jobs, secure secrets, and staging DB

