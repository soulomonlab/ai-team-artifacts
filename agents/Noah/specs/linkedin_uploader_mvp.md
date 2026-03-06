# LinkedIn Uploader — MVP Spec

## Objective
Enable marketing team to create and schedule LinkedIn posts (text + image) from the product dashboard with minimal friction.

## Scope (MVP)
- Auth: OAuth2 flow to obtain LinkedIn access token per org account.
- Feature: Create immediate or scheduled post (text + single image).
- Storage: Upload image to S3-compatible object store; store media reference in DB.
- API: Backend endpoints to create post, check status, list scheduled posts.
- Webhook/callback: Polling fallback + webhook for status updates.

## Acceptance Criteria
- UI can call POST /api/marketing/linkedin/posts to create a post and receive 202 + job id.
- Images uploaded and served from S3; DB stores media_url.
- OAuth tokens stored encrypted; refresh flow implemented.
- Scheduled posts execute within ±1 minute of scheduled time.
- Logs instrumented; failures generate alerts (P1 runbook).

## API (example)
- POST /api/marketing/linkedin/posts
  - Auth: Bearer (internal service token)
  - Payload: { text: string, image_url: string (S3), post_at?: ISO8601 }
  - Response: 202 { job_id }
- GET /api/marketing/linkedin/posts/{id}
  - Response: status, attempts, linkedin_post_id (if posted), error
- GET /api/marketing/linkedin/accounts
  - List connected LinkedIn accounts

## Data model (minimum)
- linkedin_accounts: id, org_id, linkedin_user_id, access_token_enc, refresh_token_enc, expires_at
- linkedin_posts: id, org_id, author_account_id, text, media_url, scheduled_at, status, attempts, linkedin_post_id, error

## Security / Secrets
- Required env vars (add to repo PR when deployment ready): LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, S3_BUCKET, S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, DATABASE_URL
- Tokens encrypted at rest (KMS/Secret Manager). Use short-lived access tokens + refresh.

## Infra & Operational notes
- Background worker (k8s CronJob or queue worker) to process scheduled posts (recommend: horizontal autoscaling with concurrency control).
- Health endpoint: /health for readiness and liveness (backend to implement).
- Metrics: job_success_rate, job_failure_count, job_latency_p99. SLO: job success rate >= 99%, p99 latency < 30s.
- Alerts: Failed jobs > 5 in 5m => P1 alert with runbook link.

## Non-goals (MVP)
- Rich media beyond single image (video/carousel)
- Content approval flows

## Next steps for Backend (Marcus)
1. Implement DB schema + migrations.
2. Implement endpoints above and background worker.
3. Add encrypted token storage and refresh logic.
4. Provide /health endpoint for LB probes.

