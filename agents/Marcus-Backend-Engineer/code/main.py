from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts
from .db import Base, engine

app = FastAPI(title="Posts Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables at startup for local dev (Alembic should be used in prod)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(posts.router, prefix="/api/v1")
