
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize CLOUDLEAK API
app = FastAPI(
    title="CLOUDLEAK API",
    description="Backend API for the Intelligent Cloud Cost Optimization Platform",
    version="1.0.0"
)

# Allow the Streamlit dashboard to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CLOUDLEAK API",
        "documentation": "/docs"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": "CLOUDLEAK",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
