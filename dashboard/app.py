import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Generate synthetic data
np.random.seed(0)
time_stamps = pd.date_range("2025-01-01", periods=100, freq="H")
data = pd.DataFrame({
    "timestamp": time_stamps,
    "power_usage": np.random.normal(120, 10, 100),
    "gas_consumption": np.random.normal(65, 8, 100),
    "water_usage": np.random.normal(1.0, 0.1, 100),
    "material_input": np.random.normal(550, 25, 100),
    "production_output": np.random.normal(530, 20, 100)
})
data["yield"] = data["production_output"] / data["material_input"]

st.title("Forging Plant Digital Twin - GHG & Resource Dashboard")

tab1, tab2, tab3 = st.tabs(["Time Series", "Yield Distribution", "Scenario Comparison"])

with tab1:
    st.subheader("Resource Usage Over Time")
    fig = px.line(data, x="timestamp", y=["power_usage", "gas_consumption", "water_usage"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Yield Distribution")
    fig = px.histogram(data, x="yield", nbins=20, title="Yield Distribution")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Scenario Comparison")
    st.info("Backend optimization and GHG calculation requires a public backend API. Using static demo for Streamlit Cloud.")
    # Simulate scenario
    resources = ["power_usage", "gas_consumption", "water_usage"]
    current = [data[res].mean() for res in resources]
    optimized = [c * 0.9 for c in current]  # Simulate 10% reduction
    ghg = [sum(current), sum(optimized)]
    comparison_df = pd.DataFrame({
        "Resource": resources + ["GHG Emissions"],
        "Current": current + [ghg[0]],
        "Optimized": optimized + [ghg[1]],
    })
    fig = px.bar(comparison_df.melt(id_vars="Resource", value_vars=["Current", "Optimized"]),
                 x="Resource", y="value", color="variable", barmode="group",
                 title="Scenario Resource & GHG Comparison")
    st.plotly_chart(fig, use_container_width=True)
    st.success(f"Estimated GHG Reduction: {ghg[0] - ghg[1]:.2f} units/hr")
