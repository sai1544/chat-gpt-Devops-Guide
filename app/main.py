import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/health")
def health_check():
  logging.info("Health check endpoint called")
  return {"status": "ok"}
