import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Forging Plant Digital Twin Dashboard Suite")

API_URL = "http://localhost:8000/full-analytics"
CLOSED_LOOP_URL = "http://localhost:8000/closed-loop-optimization"
SOP_URL = "http://localhost:8000/ai-sop-recommendation"
ASSISTANT_URL = "http://localhost:8000/digital-worker-assistant"

# --- Synthetic Data Generator ---
def generate_synthetic_kpi_data():
    now = datetime.now()
    output = np.random.uniform(480, 590)
    input_ = np.random.uniform(500, 600)
    scrap = input_ - output
    elec = np.random.uniform(100, 150)
    gas = np.random.uniform(50, 80)
    water = np.random.uniform(0.8, 1.2)
    cooling_in = np.random.uniform(25, 30)
    cooling_out = cooling_in + np.random.uniform(6, 12)
    oee = np.random.uniform(0.7, 0.98)
    return {
        "kpis": {
            "oee": oee,
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
            "setpoints": {
                "furnace_temp": np.random.uniform(1150, 1250),
                "cycle_time": np.random.uniform(1, 4)
            }
        },
        "alerts": ["Sample alert: Die wear rate high!"] if np.random.rand() > 0.7 else [],
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
        "timestamp": now
    }

def fetch_analytics():
    try:
        resp = requests.get(API_URL, timeout=2)
        if resp.status_code == 200:
            return resp.json()
        else:
            return generate_synthetic_kpi_data()
    except Exception:
        return generate_synthetic_kpi_data()

def fetch_closed_loop():
    try:
        resp = requests.get(CLOSED_LOOP_URL, timeout=2)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception:
        return None

def fetch_sop():
    try:
        resp = requests.get(SOP_URL, timeout=2)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception:
        return None

def ask_assistant(query):
    try:
        resp = requests.post(ASSISTANT_URL, json={"query": query}, timeout=2)
        if resp.status_code == 200:
            return resp.json()["response"]
        else:
            return "Assistant not available (backend error)."
    except Exception:
        return "Assistant not available (backend offline)."

def generate_monthly_synthetic_data(months=6):
    base = datetime(2025, 1, 1)
    dates = [base.replace(month=((base.month + i - 1) % 12 + 1)) for i in range(months)]
    data = {
        "Month": [d.strftime("%Y-%m") for d in dates],
        "Electricity (MWh)": np.random.uniform(125, 175, months),
        "Gas (Nm³)": np.random.uniform(6500, 8000, months),
        "Water (m³)": np.random.uniform(400, 600, months),
        "GHG total (tCO₂e)": np.random.uniform(210, 350, months)
    }
    return pd.DataFrame(data)

# --- Main App ---
DASHBOARD = st.sidebar.radio(
    "Choose dashboard:",
    (
        "Executive (GHG, Energy, Productivity)",
        "Operator (Alerts, Setpoints, Tracking)",
        "Sustainability Scorecard",
        "AI/Assistant & Optimization"
    )
)

analytics = fetch_analytics()
kpis = analytics["kpis"]
alerts = analytics["alerts"]
emissions = analytics["emissions"]

# --- Executive Dashboard ---
if DASHBOARD == "Executive (GHG, Energy, Productivity)":
    st.header("Executive Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("GHG Emissions")
        st.metric("Scope 1 (kgCO₂e)", f"{emissions['scope_1']:.1f}")
        st.metric("Scope 2 (kgCO₂e)", f"{emissions['scope_2']:.1f}")
        st.metric("Total GHG (kgCO₂e)", f"{emissions['total_ghg']:.1f}")
    with col2:
        st.subheader("Energy Intensity")
        st.metric("Electricity per Unit (kWh/unit)", f"{kpis['electricity_per_unit']:.3f}")
        st.metric("Gas per Unit (Nm³/unit)", f"{kpis['gas_per_unit']:.3f}")
        st.metric("Water per Unit (m³/unit)", f"{kpis['water_per_unit']:.3f}")
    with col3:
        st.subheader("Productivity")
        st.metric("OEE (%)", f"{kpis['oee']*100:.1f}")
        st.metric("Throughput Rate (units/hr)", f"{kpis['throughput_rate']:.2f}")
        st.metric("First Pass Yield (%)", f"{kpis['first_pass_yield']:.1f}")
    st.subheader("Resource Usage Over Time (Synthetic Example)")
    dates = pd.date_range("2025-01-01", periods=30)
    df = pd.DataFrame({
        "Date": dates,
        "Electricity (kWh/unit)": np.random.normal(kpis["electricity_per_unit"], 0.05, 30),
        "Gas (Nm³/unit)": np.random.normal(kpis["gas_per_unit"], 0.02, 30),
        "Water (m³/unit)": np.random.normal(kpis["water_per_unit"], 0.01, 30),
    })
    st.line_chart(df.set_index("Date"))

# --- Operator Dashboard ---
elif DASHBOARD == "Operator (Alerts, Setpoints, Tracking)":
    st.header("Operator Dashboard")
    st.subheader("Real-Time Alerts")
    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("No critical alerts at this time.")
    st.subheader("Current Setpoints")
    sp = kpis.get("setpoints", {})
    st.write(f"**Furnace Temp Setpoint:** {sp.get('furnace_temp', 'N/A'):.1f} °C")
    st.write(f"**Cycle Time Setpoint:** {sp.get('cycle_time', 'N/A'):.2f} min")
    st.subheader("Key Process Tracking")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Current Furnace Temp (°C)", f"{kpis['furnace_temp']:.1f}")
    with col2: st.metric("Die Temp (°C)", f"{kpis['die_temp']:.1f}")
    with col3: st.metric("Die Wear Rate", f"{kpis['die_wear_rate']:.2f}")
    st.subheader("Utility Usage (last 24h, synthetic)")
    df = pd.DataFrame({
        "Hour": [f"{h}:00" for h in range(24)],
        "Electricity (kWh/unit)": np.random.normal(kpis["electricity_per_unit"], 0.05, 24),
        "Gas (Nm³/unit)": np.random.normal(kpis["gas_per_unit"], 0.02, 24),
        "Water (m³/unit)": np.random.normal(kpis["water_per_unit"], 0.01, 24),
    })
    st.line_chart(df.set_index("Hour"))

# --- Sustainability Scorecard ---
elif DASHBOARD == "Sustainability Scorecard":
    st.header("Sustainability Scorecard")
    st.subheader("Resource and Emissions Footprint (Monthly)")
    df = generate_monthly_synthetic_data()
    st.dataframe(df, hide_index=True)
    st.subheader("Resource Trends")
    st.line_chart(df.set_index("Month")[["Electricity (MWh)", "Gas (Nm³)", "Water (m³)"]])
    st.subheader("GHG Emissions Trend")
    st.line_chart(df.set_index("Month")[["GHG total (tCO₂e)"]])
    st.markdown("#### Sustainability Score")
    latest = df.iloc[-1]
    score = max(0, 100 - (latest["GHG total (tCO₂e)"]-200)/2)
    st.metric("Sustainability Score (demo)", f"{score:.1f} / 100")

# --- AI/Assistant & Optimization Dashboard ---
elif DASHBOARD == "AI/Assistant & Optimization":
    st.header("AI/ML Optimization & Digital Worker Assistant")

    # Closed-loop optimization
    st.subheader("🔄 Closed-Loop Furnace Optimization (ML Feedback Loop)")
    cl_opt = fetch_closed_loop()
    if cl_opt:
        st.write(f"**Recommended Furnace Temp Setpoint:** {cl_opt['furnace_temp_setpoint']} °C")
        st.info(cl_opt["reason"])
    else:
        st.warning("Closed-loop optimization not available (backend offline).")

    # AI-driven SOP
    st.subheader("🤖 AI-Driven SOP Recommendation")
    sop = fetch_sop()
    if sop:
        st.success(sop["recommendation"])
    else:
        st.info("SOP recommendation not available (backend offline).")

    # Digital Worker Assistant (NLP)
    st.subheader("👷 Digital Worker Assistant (NLP Q&A)")
    user_query = st.text_input("Ask a question about alerts, KPIs, or trends:")
    if user_query:
        resp = ask_assistant(user_query)
        st.write(resp)

st.caption("Digital Twin Dashboard | Executive, Operator, Sustainability, and AI/Assistant Views")
