from fastapi import FastAPI
from .db import init_db
from .routers.feed import router as feed_router

app = FastAPI(title="Feed Service")

app.include_router(feed_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    init_db()

# For running with: uvicorn output.code.backend.main:app --reload
