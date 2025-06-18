from fastapi import FastAPI, Query
from scada_client import fetch_scada_data
from sample_data import generate_sample_data
from ml.optimizer import recommend_optimizations, simulate_optimized_usage
from ghg_projection import project_ghg_emissions

app = FastAPI()

@app.get("/resource-usage")
def get_resource_usage(use_sample: bool = Query(False)):
    try:
        data = fetch_scada_data() if not use_sample else generate_sample_data()
    except Exception:
        data = generate_sample_data()
    return data

@app.post("/optimize-and-project")
def optimize_and_project(current_data: dict = None, use_sample: bool = Query(False)):
    if current_data is None:
        try:
            current_data = fetch_scada_data() if not use_sample else generate_sample_data()
        except Exception:
            current_data = generate_sample_data()
    recommendations = recommend_optimizations(current_data)
    optimized_data = simulate_optimized_usage(current_data, recommendations)
    baseline_ghg = project_ghg_emissions(current_data)
    optimized_ghg = project_ghg_emissions(optimized_data)
    return {
        "current_usage": current_data,
        "recommendations": recommendations,
        "optimized_usage": optimized_data,
        "current_ghg": baseline_ghg,
        "optimized_ghg": optimized_ghg,
        "ghg_reduction": baseline_ghg["total_ghg"] - optimized_ghg["total_ghg"]
    }
