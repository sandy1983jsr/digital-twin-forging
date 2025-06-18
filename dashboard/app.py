import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests
import numpy as np
import pandas as pd

# For demo, generate synthetic time-series
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

def fetch_optimization():
    # Simulate API call to FastAPI backend
    url = "http://localhost:8000/optimize-and-project"
    try:
        res = requests.post(url, json=data.iloc[-1].to_dict(), timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Forging Plant Digital Twin - GHG & Resource Dashboard"),
    dcc.Tabs([
        dcc.Tab(label='Time Series', children=[
            dcc.Graph(
                id='time-series',
                figure={
                    "data": [
                        go.Scatter(x=data["timestamp"], y=data["power_usage"], name="Electricity (kWh)"),
                        go.Scatter(x=data["timestamp"], y=data["gas_consumption"], name="Natural Gas (Nm³/hr)"),
                        go.Scatter(x=data["timestamp"], y=data["water_usage"], name="Water (m³/hr)"),
                    ],
                    "layout": go.Layout(title="Resource Usage Over Time", xaxis={"title": "Time"}, yaxis={"title": "Usage"})
                }
            )
        ]),
        dcc.Tab(label='Yield Distribution', children=[
            dcc.Graph(
                id='yield-dist',
                figure={
                    "data": [
                        go.Histogram(x=data["yield"], nbinsx=20, name="Yield Distribution"),
                    ],
                    "layout": go.Layout(title="Yield Distribution", xaxis={"title": "Yield (%)"}, yaxis={"title": "Count"})
                }
            )
        ]),
        dcc.Tab(label='Scenario Comparison', children=[
            html.Button("Fetch Optimization Scenario", id="fetch-btn"),
            dcc.Loading(
                id="loading",
                children=[dcc.Graph(id="scenario-bar")],
                type="default"
            ),
            html.Div(id="ghg-reduction")
        ])
    ])
])

@app.callback(
    [Output("scenario-bar", "figure"),
     Output("ghg-reduction", "children")],
    [Input("fetch-btn", "n_clicks")]
)
def update_scenario(n_clicks):
    if not n_clicks:
        return go.Figure(), ""
    result = fetch_optimization()
    if not result:
        return go.Figure(), "No data available."
    resources = ["power_usage", "gas_consumption", "water_usage"]
    current = [result["current_usage"][r] for r in resources]
    optimized = [result["optimized_usage"][r] for r in resources]
    ghg = [result["current_ghg"]["total_ghg"], result["optimized_ghg"]["total_ghg"]]
    fig = go.Figure(data=[
        go.Bar(name='Current', x=resources, y=current),
        go.Bar(name='Optimized', x=resources, y=optimized),
        go.Bar(name='Current vs Optimized GHG', x=["GHG Emissions"], y=[ghg[0]], marker_color="gray"),
        go.Bar(name='GHG After Optimization', x=["GHG Emissions"], y=[ghg[1]], marker_color="green"),
    ])
    fig.update_layout(barmode='group', title="Scenario Resource & GHG Comparison")
    reduction = result["ghg_reduction"]
    return fig, f"Estimated GHG Reduction: {reduction:.2f} kg CO₂e/hr"

if __name__ == "__main__":
    app.run_server(debug=True)
