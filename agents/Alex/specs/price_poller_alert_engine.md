# Feature: Price Poller & Alert Engine
**Goal:** Continuously poll ticker prices, compute percent change vs last close, trigger alerts when thresholds are exceeded, and expose delivery channels (websocket/webhook) with low-latency access to recent timeseries.

**Users:** Downstream delivery services, trading/risk engines, ops monitoring, end-users receiving alerts.

**Acceptance Criteria:**
- [ ] Service polls price data for configured tickers every 1 minute (configurable per-deployment).
- [ ] Computes percent change vs last-close for each tick and records the computed value.
- [ ] Triggers an alert when percent change exceeds the per-ticker (or global) threshold.
- [ ] Recent price timeseries (last N minutes/hours) stored in Redis for fast reads; configurable retention.
- [ ] Expose low-latency delivery: a) Websocket endpoint for push subscribers; b) Webhook delivery for third-party endpoints, with retries/backoff and DLQ on repeated failures.
- [ ] API to query latest percent change and recent timeseries for a ticker.
- [ ] Idempotent alert delivery (dedupe by alert id + tick timestamp).
- [ ] Robustness: automatic backoff on upstream provider errors, circuit-breaker, and health/metrics endpoints (Prometheus).
- [ ] Tests: unit tests for computation, integration tests mocking price source and Redis, and e2e smoke test hitting websocket/webhook.

**Edge cases / Requirements:**
- Missing last-close: fallback behavior (skip alert or use previous close stored in DB) — configurable.
- Late/duplicate ticks: dedupe and only keep the latest per timestamp.
- Scale: design to handle Xk tickers (TBD with #ai-tech-lead) and horizontal scaling.
- Security: webhook signing + rate-limiting; secrets stored in secrets manager.

**Out of Scope:**
- Long-term historical storage for analytics (use existing data warehouse).
- Complex alert rules (patterns, aggregations) — future iteration.

**Key decisions (proposed):**
- Poll interval: 1 minute default, configurable.
- In-memory cache: Redis (time-series via lists/streams or RedisTimeSeries module) for recent data and TTL-based retention.
- Alerts: stateless engine that reads Redis timeseries + last close; delivery via websocket channel + webhook with retry/DLQ.
- Language & infra: implement as a containerized microservice (Go or Python). Final choice with #ai-tech-lead.

**Spec file:** output/specs/price_poller_alert_engine.md
**GitHub Issue:** TBD
