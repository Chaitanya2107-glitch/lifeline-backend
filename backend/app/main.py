from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import logger
from app.database.supabase import supabase

app = FastAPI(title="Lifeline Backend")

@app.get("/")
def root():
    return {"message": "Backend Running"}
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.get("/db-status")
def db_status():
    try:
        return {
            "status": "connected",
            "database": "Supabase"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
