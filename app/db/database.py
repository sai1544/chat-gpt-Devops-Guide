import psycopg2
from psycopg2 import OperationalError
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger("database")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        logger.info("PostgreSQL connection successful")
        return conn
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise
