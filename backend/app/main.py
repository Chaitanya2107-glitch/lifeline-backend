from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import logger

app = FastAPI(title="Lifeline Backend")

@app.get("/")
def root():
    return {"message": "Backend Running"}
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
