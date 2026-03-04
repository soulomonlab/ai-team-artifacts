# Multi-stage Python image
FROM python:3.11-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential gcc libssl-dev && rm -rf /var/lib/apt/lists/*
COPY output/code/price_poller/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip wheel -r requirements.txt -w /wheels

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /wheels /wheels
COPY output/code/price_poller/ /app/
RUN pip install --upgrade pip && pip install --no-index --find-links=/wheels -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "price_poller.app:app", "--host", "0.0.0.0", "--port", "8000"]
