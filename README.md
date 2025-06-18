# Digital Twin for Forging Company – ESG Resource & GHG Optimization

## Features
- Real-time and synthetic data support (SCADA integration-ready)
- ML-based resource optimization and scenario simulation
- GHG emissions projection for current and optimized scenarios
- Interactive dashboard:
    - Time series (resource use)
    - Yield distribution
    - Scenario comparison (GHG/resource bar charts)

## Structure
- `backend/`: FastAPI API, ML, GHG, sample data
- `dashboard/`: Dash/Plotly dashboard for visualization

## Quick Start

### 1. Start Backend API
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Start Dashboard
```
cd ../dashboard
pip install dash plotly pandas requests
python app.py
```

## Notes
- SCADA integration can be added in `backend/scada_client.py`
- Dashboard expects backend at `http://localhost:8000`
