from fastapi import FastAPI, Query
from sample_data import generate_sample_data
from kpis_and_analytics import full_analytics

app = FastAPI()

@app.get("/full-analytics")
def get_full_analytics(use_sample: bool = Query(True)):
    # In real deployment, replace with actual data fetch
    data = generate_sample_data()
    # For time series/trend analytics, you could keep a history list here
    history = [generate_sample_data() for _ in range(10)]
    # Scenario: what if we reduce gas consumption by 10%
    scenario = {"gas_consumption": data["gas_consumption"] * 0.9}
    result = full_analytics(data, history=history, scenario=scenario)
    return result
