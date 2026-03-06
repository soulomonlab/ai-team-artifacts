from fastapi import FastAPI

app = FastAPI(title="Instagram Clone API - MVP")

@app.get("/health")
def health():
    return {"status": "ok"}
