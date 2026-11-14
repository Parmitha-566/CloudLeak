
FROM python:3.13-slim

WORKDIR /app

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the integrated project modules
COPY backend/ ./backend/
COPY Member1/ ./Member1/
COPY analyzer/ ./analyzer/

# Backend API port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
