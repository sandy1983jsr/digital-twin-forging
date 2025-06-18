import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Forging Plant Digital Twin - Advanced KPI & Analytics Dashboard")

# --- Fetch Data from Backend API ---
API_URL = "http://localhost:8000/full-analytics"  # Replace with public API if deployed

@st.cache_data(ttl=60)
def fetch_analytics():
    try:
        resp = requests.get(API_URL)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"Backend error: {resp.status_code}")
            return None
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
        return None

analytics = fetch_analytics()
if not analytics:
    st.stop()

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

# --- Energy & Emissions Section ---
with st.expander("Energy & Emissions Analytics", expanded=True):
    st.write(f"**Energy Inefficiency Score:** {energy_opt['inefficiency_score']}")
    if energy_opt["electricity_forecast"]:
        st.write(f"**Forecasted Electricity per Unit:** {energy_opt['electricity_forecast']:.3f} kWh/unit")
    st.write(f"**GHG Scope 1:** {emissions['scope_1']:.2f} kgCO₂e")
    st.write(f"**GHG Scope 2:** {emissions['scope_2']:.2f} kgCO₂e")
    st.write(f"**GHG Water:** {emissions['water']:.2f} kgCO₂e")
    st.write(f"**Total GHG:** {emissions['total_ghg']:.2f} kgCO₂e")
    st.write(f"**Flue Gas [CO₂]:** {emissions['flue_CO2']:.2f}% | [NOₓ]: {emissions['flue_NOx']:.3f}% | [SOₓ]: {emissions['flue_SOx']:.3f}%")

# --- Predictive Maintenance Section ---
with st.expander("Predictive Maintenance"):
    st.write(f"**Estimated Die Remaining Useful Life:** {maintenance['die_rul_cycles']} cycles" if maintenance['die_rul_cycles'] is not None else "No RUL anomaly detected.")

# --- What-If Simulation Section ---
with st.expander("What-if Simulation (10% Less Gas Consumption)"):
    if whatif:
        st.write("KPIs under scenario:")
        st.json(whatif)
    else:
        st.info("No scenario data available.")

# --- Example Visualizations (Synthetic) ---
# You could replace this with actual time series from your backend if available
data = {
    'timestamp': pd.date_range("2025-06-01", periods=24, freq="H"),
    'power_usage': [kpis['electricity_per_unit']*random for random in (1+0.05*i for i in range(24))],
    'gas_per_unit': [kpis['gas_per_unit']*random for random in (1+0.03*i for i in range(24))],
    'water_per_unit': [kpis['water_per_unit']*random for random in (1+0.02*i for i in range(24))]
}
df = pd.DataFrame(data)
st.subheader("Resource Usage Over Time (Example)")
st.line_chart(df.set_index("timestamp"))

# --- Footer ---
st.caption("Digital Twin Dashboard | Developed for Advanced Industrial KPI Monitoring and Analytics")
