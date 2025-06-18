import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(layout="wide")
st.title("Forging Plant Digital Twin - Advanced KPI & Analytics Dashboard")

API_URL = "http://localhost:8000/full-analytics"  # Update to deployed backend if needed

def generate_synthetic_kpi_data():
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
            "furnace_temp": np.random.uniform(1150, 1250),
        },
        "alerts": [],
        "energy_optimization": {"inefficiency_score": np.random.randint(0,4), "electricity_forecast": elec/output},
        "emissions": {
            "scope_1": gas*2, 
            "scope_2": elec*0.82, 
            "water": water*0.344, 
            "total_ghg": gas*2+elec*0.82+water*0.344, 
            "flue_CO2": np.random.uniform(8, 10), 
            "flue_NOx": np.random.uniform(0.02, 0.07), 
            "flue_SOx": np.random.uniform(0.01, 0.03)
        },
        "predictive_maintenance": {"die_rul_cycles": np.random.choice([None, 10, 50])},
        "whatif_simulation": None,
    }

def fetch_analytics():
    try:
        resp = requests.get(API_URL, timeout=2)
        if resp.status_code == 200:
            st.info("Fetched data from backend API.")
            return resp.json()
        else:
            st.warning("Backend error, using synthetic data.")
            return generate_synthetic_kpi_data()
    except Exception:
        st.info("Backend not reachable, using synthetic KPIs.")
        return generate_synthetic_kpi_data()

analytics = fetch_analytics()
kpis = analytics["kpis"]
alerts = analytics["alerts"]
energy_opt = analytics["energy_optimization"]
emissions = analytics["emissions"]
maintenance = analytics["predictive_maintenance"]
whatif = analytics.get("whatif_simulation")

# --- KPI Display Section ---
st.subheader("Key KPIs")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("OEE (%)", f"{kpis['oee']*100:.1f}")
    st.metric("First Pass Yield (%)", f"{kpis['first_pass_yield']:.1f}")
    st.metric("Scrap Rate (%)", f"{kpis['scrap_rate']:.2f}")
    st.metric("Cycle Time (min)", f"{kpis['cycle_time']:.2f}")
with col2:
    st.metric("Electricity per Unit (kWh/unit)", f"{kpis['electricity_per_unit']:.3f}")
    st.metric("Furnace Thermal Efficiency (%)", f"{kpis['furnace_thermal_efficiency']*100:.1f}")
    st.metric("Idle Energy (kWh)", f"{kpis['idle_energy']:.1f}")
    st.metric("Peak Demand (kW)", f"{kpis['peak_demand']:.1f}")
with col3:
    st.metric("Gas per Unit (Nm³/unit)", f"{kpis['gas_per_unit']:.3f}")
    st.metric("Water per Unit (m³/unit)", f"{kpis['water_per_unit']:.3f}")
    st.metric("Cooling ΔT (°C)", f"{kpis['cooling_water_deltaT']:.2f}")
    st.metric("Throughput Rate (units/hr)", f"{kpis['throughput_rate']:.2f}")
with col4:
    st.metric("Flue Gas Temp (°C)", f"{kpis['flue_gas_temperature']:.1f}")
    st.metric("Die Temp (°C)", f"{kpis['die_temp']:.1f}")
    st.metric("Die Wear Rate", f"{kpis['die_wear_rate']:.2f}")
    st.metric("Water Discharge Temp (°C)", f"{kpis['water_discharge_temp']:.1f}")

# --- Alerts Section ---
st.subheader("⚠️ Real-Time Alerts")
if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No critical alerts at this time.")

with st.expander("Energy & Emissions Analytics", expanded=True):
    st.write(f"**Energy Inefficiency Score:** {energy_opt['inefficiency_score']}")
    if energy_opt["electricity_forecast"]:
        st.write(f"**Forecasted Electricity per Unit:** {energy_opt['electricity_forecast']:.3f} kWh/unit")
    st.write(f"**GHG Scope 1:** {emissions['scope_1']:.2f} kgCO₂e")
    st.write(f"**GHG Scope 2:** {emissions['scope_2']:.2f} kgCO₂e")
    st.write(f"**GHG Water:** {emissions['water']:.2f} kgCO₂e")
    st.write(f"**Total GHG:** {emissions['total_ghg']:.2f} kgCO₂e")
    st.write(f"**Flue Gas [CO₂]:** {emissions['flue_CO2']:.2f}% | [NOₓ]: {emissions['flue_NOx']:.3f}% | [SOₓ]: {emissions['flue_SOx']:.3f}%")

with st.expander("Predictive Maintenance"):
    st.write(f"**Estimated Die Remaining Useful Life:** {maintenance['die_rul_cycles']} cycles" if maintenance['die_rul_cycles'] is not None else "No RUL anomaly detected.")

with st.expander("What-if Simulation (10% Less Gas Consumption)"):
    if whatif:
        st.write("KPIs under scenario:")
        st.json(whatif)
    else:
        st.info("No scenario data available.")

# --- Closed-loop optimization ---
st.subheader("🔄 Closed-Loop Furnace Optimization (ML Feedback Loop)")
try:
    cl_opt = requests.get("http://localhost:8000/closed-loop-optimization", timeout=2).json()
    st.write(f"**Recommended Furnace Temp Setpoint:** {cl_opt['furnace_temp_setpoint']} °C")
    st.info(cl_opt["reason"])
except Exception:
    st.warning("Closed-loop optimization not available (backend offline).")

# --- AI-Driven SOP Recommendations ---
st.subheader("🤖 AI-Driven SOP Recommendation")
try:
    sop = requests.get("http://localhost:8000/ai-sop-recommendation", timeout=2).json()
    st.success(sop["recommendation"])
except Exception:
    st.info("SOP recommendation not available (backend offline).")

# --- Digital Worker Assistant ---
st.subheader("👷 Digital Worker Assistant (NLP Q&A)")
user_query = st.text_input("Ask a question about alerts, KPIs, or trends:")
if user_query:
    try:
        resp = requests.post("http://localhost:8000/digital-worker-assistant", json={"query": user_query}, timeout=2).json()
        st.write(resp["response"])
    except Exception:
        st.info("NLP assistant not available (backend offline).")

# --- Example Visualizations (Synthetic Time Series) ---
np.random.seed(0)
timestamps = pd.date_range("2025-06-01", periods=24, freq="H")
df = pd.DataFrame({
    "timestamp": timestamps,
    "power_usage": np.random.normal(kpis["electricity_per_unit"]*100, 5, 24),
    "gas_per_unit": np.random.normal(kpis["gas_per_unit"]*100, 2, 24),
    "water_per_unit": np.random.normal(kpis["water_per_unit"]*100, 1, 24)
})
st.subheader("Resource Usage Over Time (Synthetic Example)")
st.line_chart(df.set_index("timestamp"))

st.caption("Digital Twin Dashboard | Developed for Advanced Industrial KPI Monitoring and Analytics")
