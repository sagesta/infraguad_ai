FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# python-multipart is required for Starlette/FastAPI `request.form()` (e.g. POST /login).
# The validation import below tests the exact path modern Starlette uses at runtime.
RUN pip install --no-cache-dir -r requirements.txt \
    && python -c "from python_multipart.multipart import parse_options_header; print('multipart OK')"

COPY agent ./agent
COPY api ./api
COPY dashboard ./dashboard

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
