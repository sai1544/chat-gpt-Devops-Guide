from fastapi import APIRouter
from app.db.database import get_db_connection

router = APIRouter()

@router.get("/health")
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "ok"}
    except Exception:
        return {"status": "db_error"}

@router.get("/write")
def write_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO health_logs (status) VALUES (%s)",
        ("OK",)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Data inserted"}

@router.get("/read")
def read_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, status, checked_at FROM health_logs ORDER BY id DESC LIMIT 5"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

