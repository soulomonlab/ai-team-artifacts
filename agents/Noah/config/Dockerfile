# Multi-stage Dockerfile for core-api and auth services
# Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies to a wheelhouse
COPY pyproject.toml setup.cfg requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# Final image
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Create non-root user
RUN groupadd -r app && useradd -r -g app app

# Install runtime deps
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels -r /wheels/../requirements.txt || true

# Copy application (expect repo to mount code at /app during build for CI)
COPY . /app
RUN chown -R app:app /app
USER app

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
