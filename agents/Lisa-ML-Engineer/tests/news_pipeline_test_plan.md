# News Pipeline Test Plan

Scope
- Validate ingestion from NewsAPI and RSS
- Validate per-article summarization (3-sentence) and deduplication
- Validate daily aggregate summary creation and API endpoints

Test cases
1) Ingestion with NEWSAPI_KEY set
   - Run news_ingest.py with date=2026-03-08 -> expect >0 articles from NewsAPI
2) Ingestion without NEWSAPI_KEY
   - Unset NEWSAPI_KEY, run -> only RSS articles ingested, no failures
3) Deduplication
   - Run ingestion twice for same feeds -> raw_articles count should not increase
4) Summarization success
   - Run llm_summarizer.py with OPENAI_API_KEY set -> summaries table filled with non-empty summaries
5) Summarization fallback
   - Unset OPENAI_API_KEY and ensure local transformer summarizer produces summaries
6) API endpoints
   - Start FastAPI app and call /api/v1/news/summary?date=YYYY-MM-DD -> 200 or 404 as appropriate
   - Call /api/v1/news/articles?date=YYYY-MM-DD -> list of article summaries

Acceptance criteria
- End-to-end: ingestion -> summarization -> daily aggregate -> API returns 200 and valid JSON
- Summaries are ~3 sentences (manual spot check)

