Price Poller & Alert Engine

Endpoints:
- GET /health
- WebSocket /ws (receives alerts)

Env vars (see .env.example):
- REDIS_URL
- TICKERS
- POLL_INTERVAL
- ALERT_THRESHOLD_PCT
- ALERT_WEBHOOKS
- PRICE_API_URL

Run locally:
  docker-compose -f output/config/docker-compose.yml up --build
