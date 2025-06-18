import streamlit as st
import pandas as pd
import numpy as np
import requests

def generate_synthetic_kpi_data():
    # Example: Generate synthetic KPI data similar to your backend
    output = np.random.uniform(480, 590)
    input_ = np.random.uniform(500, 600)
    scrap = input_ - output
    elec = np.random.uniform(100, 150)
    gas = np.random.uniform(50, 80)
    water = np.random.uniform(0.8, 1.2)
    cooling_in = np.random.uniform(25, 30)
    cooling_out = cooling_in + np.random.uniform(6, 12)
    return {
        "kpis": {
            "oee": np.random.uniform(0.7, 0.98),
            "first_pass_yield": output/input_*100,
            "scrap_rate": scrap/input_*100,
            "cycle_time": np.random.uniform(1, 4),
            "electricity_per_unit": elec/output,
            "furnace_thermal_efficiency": np.random.uniform(0.2, 0.4),
            "idle_energy": np.random.uniform(0, 10),
            "peak_demand": np.random.uniform(120, 180),
            "gas_per_unit": gas/output,
            "water_per_unit": water/output,
            "cooling_water_deltaT": cooling_out-cooling_in,
            "throughput_rate": output/1,
            "flue_gas_temperature": np.random.uniform(300, 400),
            "die_temp": np.random.uniform(200, 400),
            "die_wear_rate": np.random.uniform(0, 1),
            "water_discharge_temp": np.random.uniform(30, 40),
        },
        "alerts": [],
        "energy_optimization": {"inefficiency_score": np.random.randint(0,4), "electricity_forecast": elec/output},
        "emissions": {"scope_1": gas*2, "scope_2": elec*0.82, "water": water*0.344, "total_ghg": gas*2+elec*0.82+water*0.344, "flue_CO2": np.random.uniform(8, 10), "flue_NOx": np.random.uniform(0.02, 0.07), "flue_SOx": np.random.uniform(0.01, 0.03)},
        "predictive_maintenance": {"die_rul_cycles": np.random.choice([None, 10, 50])},
        "whatif_simulation": None,
    }

API_URL = "http://localhost:8000/full-analytics"  # Or your public API if available

def fetch_analytics():
    try:
        resp = requests.get(API_URL, timeout=2)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.warning("Backend error, using synthetic data.")
            return generate_synthetic_kpi_data()
    except Exception:
        st.info("Backend not reachable, using synthetic KPIs.")
        return generate_synthetic_kpi_data()

analytics = fetch_analytics()
# ...rest of your dashboard visualization...
