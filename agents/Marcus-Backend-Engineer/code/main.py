from fastapi import FastAPI
from .routers import auth as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/health")
def health():
    return {"status": "ok"}
