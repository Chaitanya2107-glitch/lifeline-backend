from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import logger
from app.database.supabase import supabase
from app.upload.routes import router as upload_router

# NEW IMPORT
from app.auth.routes import router as auth_router

app = FastAPI(title="Lifeline Backend")

# REGISTER ROUTER
app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(upload_router)

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
