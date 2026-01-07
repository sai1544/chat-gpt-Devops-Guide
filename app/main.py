from fastapi import FastAPI
from app.utils.logger import get_logger
from app.core.config import settings
from app.db.database import get_db_connection

# Initialize logger
logger = get_logger("app")

# Create FastAPI app
app = FastAPI()

@app.on_event("startup")
def startup_event():
    logger.info("FastAPI application started")

    # Only attempt DB connection if not in dev environment
    if settings.APP_ENV != "dev":
        try:
            conn = get_db_connection()
            conn.close()
            logger.info("Database connection verified and closed")
        except Exception as e:
            logger.error(f"Database connection failed on startup: {e}")
            # Fail fast: stop app if DB is critical
            raise

@app.on_event("shutdown")
def shutdown_event():
    logger.info("FastAPI application stopped")

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

