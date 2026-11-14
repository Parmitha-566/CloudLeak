# Shared image with separate frontend and backend build targets.
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM base AS frontend
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]

FROM base AS backend
EXPOSE 8000
# Member 3 must provide backend/main.py with a FastAPI instance named `app`.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
