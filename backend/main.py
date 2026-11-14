from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CloudLeak Backend API"}

@app.get("/api/summary")
def get_summary():
    return {
        "currency": "USD",
        "total_monthly_expenditure": 1250.00,
        "total_resources": 6,
        "average_cpu_utilization": 33.0,
        "estimated_potential_savings": 115.00
    }
