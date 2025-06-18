EMISSIONS_FACTORS = {
    "power_usage": 0.82,        # kg CO₂e per kWh
    "gas_consumption": 2.0,     # kg CO₂e per Nm³
    "water_usage": 0.344,       # kg CO₂e per m³
    "material_input": 1.5,      # kg CO₂e per kg steel
}

def project_ghg_emissions(resource_usage: dict) -> dict:
    ghg = {}
    total = 0
    for resource, usage in resource_usage.items():
        factor = EMISSIONS_FACTORS.get(resource)
        if factor is not None:
            emission = usage * factor
            ghg[resource] = emission
            total += emission
    ghg["total_ghg"] = total
    return ghg
