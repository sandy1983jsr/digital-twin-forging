import numpy as np
from typing import Dict, Any, List, Tuple

def ingest_kpis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ingests raw process data and calculates all key KPIs.
    Input: data dictionary with raw measurements.
    Output: dictionary with all relevant KPIs.
    """
    # Energy KPIs
    electricity_per_unit = data.get("power_usage", 0) / max(data.get("production_output", 1), 1e-3)
    furnace_thermal_eff = (data.get("production_output", 1) * data.get("furnace_temp", 1)) / (
        data.get("power_usage", 1) + data.get("gas_consumption", 1) * 8.5)  # Simple proxy
    idle_energy = data.get("idle_power_usage", 0)
    peak_demand = data.get("peak_power", data.get("power_usage", 0))
    # Utilities
    water_per_unit = data.get("water_usage", 0) / max(data.get("production_output", 1), 1e-3)
    gas_per_unit = data.get("gas_consumption", 0) / max(data.get("production_output", 1), 1e-3)
    cooling_deltaT = data.get("cooling_water_out", 0) - data.get("cooling_water_in", 0)
    # Process
    scrap = max(data.get("material_input", 0) - data.get("production_output", 0), 0)
    scrap_rate = scrap / max(data.get("material_input", 1), 1e-3) * 100
    first_pass_yield = data.get("production_output", 0) / max(data.get("material_input", 1), 1e-3) * 100
    # Environmental
    ghg = emissions_calc(data)
    # OEE
    availability = max(1 - data.get("downtime", 0) / (data.get("runtime", 1) + 1e-3), 0)
    performance = min(data.get("production_output", 0) / max(data.get("target_output", 1), 1e-3), 1)
    oee = availability * performance * (first_pass_yield / 100)
    return {
        "electricity_per_unit": electricity_per_unit,
        "furnace_thermal_efficiency": furnace_thermal_eff,
        "idle_energy": idle_energy,
        "peak_demand": peak_demand,
        "water_per_unit": water_per_unit,
        "gas_per_unit": gas_per_unit,
        "cooling_water_deltaT": cooling_deltaT,
        "scrap_rate": scrap_rate,
        "first_pass_yield": first_pass_yield,
        "oee": oee,
        "flue_gas_temperature": data.get("flue_gas_temp", None),
        "flue_gas_composition": data.get("flue_gas_comp", {}),
        "ghg_scope_1_2": ghg,
        "unplanned_downtime": data.get("downtime", 0),
        "maintenance_frequency": data.get("maintenance_count", 0),
        "mtbf": data.get("mtbf", None),
        "throughput_rate": data.get("production_output", 0) / max(data.get("runtime", 1), 1e-3),
        "cycle_time": data.get("cycle_time", None),
        "die_temp": data.get("die_temp", None),
        "die_wear_rate": data.get("die_wear_rate", None),
        "water_discharge_temp": data.get("water_discharge_temp", None),
        "water_discharge_pH": data.get("water_discharge_pH", None),
    }

def analytic_alerts(kpis: Dict[str, Any]) -> List[str]:
    """
    Rule/anomaly/threshold-based alerts.
    """
    alerts = []
    if kpis.get("scrap_rate", 0) > 3:
        alerts.append("Scrap rate > 3% for 2 hrs: Send maintenance alert.")
    if kpis.get("flue_gas_temperature", 0) > 350:
        alerts.append("High flue gas temperature: Check for heat loss or burner issue.")
    if kpis.get("water_per_unit", 0) > 2:
        alerts.append("High water usage per unit: Inspect for leaks or cooling inefficiency.")
    if kpis.get("electricity_per_unit", 0) > 0.5:
        alerts.append("High electricity consumption per unit: Check for idle running or inefficiency.")
    if kpis.get("unplanned_downtime", 0) > 2:
        alerts.append("Unplanned downtime exceeds 2 hrs/month: Investigate root cause.")
    if kpis.get("oee", 1) < 0.7:
        alerts.append("OEE below 70%: Investigate production bottlenecks.")
    return alerts

def analytic_energy_optimization(kpis: Dict[str, Any], history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Energy inefficiency scoring and simple trend forecasting.
    """
    inefficiency_score = 0
    if kpis["electricity_per_unit"] > 0.5:
        inefficiency_score += 1
    if kpis["furnace_thermal_efficiency"] < 0.2:
        inefficiency_score += 2
    if kpis["idle_energy"] > 5:
        inefficiency_score += 1
    forecast = None
    if history:
        try:
            y = np.array([h["electricity_per_unit"] for h in history])
            forecast = float(np.mean(y[-5:]))  # naive mean-of-last-5 as stub
        except Exception:
            forecast = None
    return {"inefficiency_score": inefficiency_score, "electricity_forecast": forecast}

def emissions_calc(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculates GHG emissions Scope 1 & 2, and flue gas if available.
    """
    # Emission factors
    EF = {
        "power_usage": 0.82,        # kg CO₂e per kWh (Scope 2)
        "gas_consumption": 2.0,     # kg CO₂e per Nm³ (Scope 1)
        "water_usage": 0.344,       # kg CO₂e per m³  (water supply)
    }
    scope_1 = data.get("gas_consumption", 0) * EF["gas_consumption"]
    scope_2 = data.get("power_usage", 0) * EF["power_usage"]
    water = data.get("water_usage", 0) * EF["water_usage"]
    # Flue gas
    flue = data.get("flue_gas_comp", {})
    co2 = flue.get("CO2", 0)
    nox = flue.get("NOx", 0)
    sox = flue.get("SOx", 0)
    return {
        "scope_1": scope_1,
        "scope_2": scope_2,
        "water": water,
        "flue_CO2": co2,
        "flue_NOx": nox,
        "flue_SOx": sox,
        "total_ghg": scope_1 + scope_2 + water
    }

def analytic_predictive_maintenance(data: Dict[str, Any], history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Stub for RUL and anomaly detection.
    """
    # Very basic: if die_wear_rate > threshold, predict short RUL
    die_rul = None
    if data.get("die_wear_rate", 0) > 0.8:
        die_rul = 10  # cycles left
    elif data.get("die_wear_rate", 0) > 0:
        die_rul = 50
    # For motors or other assets, extend as needed
    return {"die_rul_cycles": die_rul}

def analytic_process_simulation(data: Dict[str, Any], scenario: Dict[str, float]) -> Dict[str, Any]:
    """
    Simple "what-if" simulator: perturbs selected process parameters and returns new KPIs.
    """
    simulated = data.copy()
    simulated.update(scenario)
    return ingest_kpis(simulated)

def full_analytics(data: Dict[str, Any], history: List[Dict[str, Any]] = None, scenario: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Runs full analytics suite: all KPIs, alerts, optimization, emissions, maintenance, scenario analysis.
    """
    kpis = ingest_kpis(data)
    alerts = analytic_alerts(kpis)
    energy_opt = analytic_energy_optimization(kpis, history)
    emissions = kpis["ghg_scope_1_2"]
    maintenance = analytic_predictive_maintenance(data, history)
    simulation = None
    if scenario:
        simulation = analytic_process_simulation(data, scenario)
    return {
        "kpis": kpis,
        "alerts": alerts,
        "energy_optimization": energy_opt,
        "emissions": emissions,
        "predictive_maintenance": maintenance,
        "whatif_simulation": simulation
    }
