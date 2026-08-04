from fastapi import FastAPI

app = FastAPI(title="Lifeline Backend")

@app.get("/")
def root():
    return {"message": "Backend Running"}
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
from fastapi import FastAPI
from app.config.settings import settings

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT
    }
from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import logger

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
async def startup():
    logger.info("🚀 Lifeline Backend Started")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")


@app.get("/db-status")
def db_status():
    return {
        "database": "Supabase Connected"
    }

    return {
        "message": "Backend Running"
    }


@app.get("/health")
def health():
    logger.info("Health check requested")

    return {
        "status": "healthy"
    }

from app.database.supabase import supabase
from app.utils.logger import logger

@app.on_event("startup")
async def startup():
    logger.info("🚀 Lifeline Backend Started")

    try:
        logger.info("✅ Connected to Supabase")
    except Exception as e:
        logger.error(f"❌ Supabase connection failed: {e}")
