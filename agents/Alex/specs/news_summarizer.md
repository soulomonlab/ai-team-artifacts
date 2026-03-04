# Feature: News ingestion & LLM summarizer
**Goal:** Collect global market & economic news, produce daily 3-sentence abstractive summaries, and expose them via an API while keeping the pipeline scalable and auditable.

**Users:** Traders, PMs, research analysts, downstream ML models.

**Acceptance Criteria:**
- [ ] Daily ingestion job collects headlines & article bodies from NewsAPI + RSS feeds (FT, WSJ, Reuters).
- [ ] Deduplicate articles across sources and filter for market/economy topics (basic keyword + publisher tags).
- [ ] 3-sentence abstractive summary produced per day using LLM; include source attribution and top-3 articles referenced.
- [ ] Summaries stored in DB per-day (schema: date, summary_text, sources[], top_articles[], model_id, tokens_used, created_at).
- [ ] Public internal endpoint: GET /api/v1/news/summary?date=YYYY-MM-DD returns stored summary; POST /api/v1/news/summary/run triggers a run (auth required).
- [ ] Retry/backoff and alerting for feed failures; idempotent runs (use run_id + dedupe).
- [ ] Cost control: batch prompts, truncate long articles with extractive prefiltering, log token usage per run.
- [ ] Tests: unit tests for ingestion, E2E test for end-to-end summary generation (mock LLM), QA test plan.

**Performance & Scale:**
- Schedule daily run at 02:00 UTC; support on-demand run.
- Pipeline should horizontally scale (workers for fetch -> preprocess -> summarize -> store).

**Security & Compliance:**
- Respect publisher terms; do not store paywalled full text beyond transient processing.
- POST run endpoint requires service-to-service auth (JWT with scope news:run).

**Monitoring & Observability:**
- Emit metrics: articles_fetched, summaries_generated, tokens_used, run_duration, errors.
- Store run logs (first-line only) and link to S3 raw fetch artifacts for audits.

**Out of Scope:**
- Retrieving paywalled content via scraping or bypassing paywalls.
- Multilingual summarization (English only for now).

**Implementation notes / Decisions:**
- LLM: Use our hosted LLM endpoint (model v1) with 3-shot prompt for consistency; call batching to reduce token count.
- Storage: Postgres table news_summaries + S3 for raw fetch artifacts.
- Scheduling: Cron on Kubernetes (K8s CronJob) + manual trigger endpoint.

**GitHub Issue:** #N (created separately)
