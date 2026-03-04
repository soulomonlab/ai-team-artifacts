from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import time

app = FastAPI(title="Healthcheck")

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float

START_TIME = time.time()

@app.get("/health", response_model=HealthResponse, tags=["health"])
def health():
    """Simple health endpoint.

    Returns status, UTC timestamp and process uptime in seconds.
    p99 target: <200ms (keeps logic minimal and sync).
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat() + "Z",
        uptime_seconds=round(time.time() - START_TIME, 3),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)
