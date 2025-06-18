from fastapi import FastAPI, Query, Request
from sample_data import generate_sample_data
from kpis_and_analytics import (
    full_analytics, closed_loop_optimization, ai_sop_recommendation, digital_worker_assistant
)
import numpy as np

app = FastAPI()

@app.get("/full-analytics")
def get_full_analytics():
    data = generate_sample_data()
    history = [generate_sample_data() for _ in range(10)]
    scenario = {"gas_consumption": data["gas_consumption"] * 0.9}
    result = full_analytics(data, history=history, scenario=scenario)
    return result

@app.get("/closed-loop-optimization")
def get_closed_loop_optimization():
    data = generate_sample_data()
    kpis = full_analytics(data)["kpis"]
    return closed_loop_optimization(kpis)

@app.get("/ai-sop-recommendation")
def get_ai_sop_recommendation():
    history = [generate_sample_data() for _ in range(15)]
    return {"recommendation": ai_sop_recommendation(history)}

@app.post("/digital-worker-assistant")
async def digital_worker_assistant_api(request: Request):
    req = await request.json()
    query = req.get("query", "")
    data = generate_sample_data()
    history = [generate_sample_data() for _ in range(12)]
    kpis = full_analytics(data)["kpis"]
    resp = digital_worker_assistant(query, kpis, history)
    return {"response": resp}
