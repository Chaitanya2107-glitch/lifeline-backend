from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import logger
from app.database.supabase import supabase
from app.api.upload import router as upload_router
from app.timeline.routes import router as timeline_router
from app.summary.routes import router as summary_router
from app.vitalis.routes import router as vitalis_router

# NEW IMPORT
from app.auth.routes import router as auth_router

app = FastAPI(title="Lifeline Backend")
app.include_router(upload_router)

# REGISTER ROUTER
app.include_router(auth_router)

app.include_router(timeline_router)
app.include_router(summary_router)
app.include_router(vitalis_router)

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
