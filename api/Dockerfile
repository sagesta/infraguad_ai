FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
# python-multipart is required for Starlette/FastAPI `request.form()` (e.g. POST /login).
# Install explicitly so image builds do not pass without it if requirements drift.
RUN pip install --no-cache-dir -r requirements.txt "python-multipart>=0.0.9" \
    && python -c "import multipart"

COPY agent ./agent
COPY api ./api
COPY dashboard ./dashboard

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
