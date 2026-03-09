# Postgres & Migration Plan (MVP)

## Decision
- Database: Postgres (managed) on Railway for MVP.
- Migrations: Alembic for schema migrations; SQLAlchemy ORM in backend.

## Rationale
- Postgres: reliable, transactional, mature ecosystem, strong support in SQLAlchemy and Alembic.
- Railway: fast setup for MVP, integrates with GitHub, supports managed Postgres and environment variables.

## Migration Strategy
1. Start with single Postgres instance for MVP. Backups enabled (Railway backups).
2. Schema definition via SQLAlchemy models in backend/modules/*/models.py
3. Alembic config in backend/migrations/. Keep migration scripts under version control.
4. Migration workflow:
   - Developers add model changes + generate alembic revision locally (alembic revision --autogenerate -m "msg")
   - Run migrations locally against a dev DB to validate
   - Open PR including migration file; CI runs a smoke migration against a test DB (docker or ephemeral)
   - On merge to main, deployment pipeline runs alembic upgrade head against staging/prod DB

## Rollback
- Use alembic downgrade <rev> for quick rollbacks. For complex destructive operations, prefer additive migrations + backfill before swapping.

## Acceptance criteria
- Alembic present and configured (backend/migrations/)
- Migration run documented in docs/RUNBOOK.md
