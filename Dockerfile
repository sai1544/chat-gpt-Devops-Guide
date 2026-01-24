# -------- Stage 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# -------- Stage 2: Runtime --------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

COPY --from=builder /install /usr/local
COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

