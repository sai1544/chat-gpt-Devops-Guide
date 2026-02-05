from fastapi import FastAPI
from app.utils.logger import get_logger
from app.routes.health import router as health_router
from app.db.database import get_db_connection

logger = get_logger("main")

app = FastAPI(title="DevOps Python App")

# Register routes
app.include_router(health_router)

@app.on_event("startup")
def startup_event():
    logger.info("Application starting...")
    conn = get_db_connection()
    conn.close()
    logger.info("Startup DB check completed")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application stopped")

@app.get("/")
def root():
    return {"message": "DevOps Python App Running"}

@app.get("/version")
def version_info():
    return {"version": "v2.0"}

