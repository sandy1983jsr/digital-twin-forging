def recommend_optimizations(data):
    recommendations = []
    if data["power_usage"] > 130:
        recommendations.append({
            "action": "Reduce idle running of furnace",
            "suggested_value": "Lower power usage to <130 kWh",
            "expected_savings": "Up to 10% electricity"
        })
    if data["gas_consumption"] > 70:
        recommendations.append({
            "action": "Check furnace insulation and burner tuning",
            "suggested_value": "Reduce gas to <70 Nm3/hr",
            "expected_savings": "Up to 8% natural gas"
        })
    if data["water_usage"] > 1.0:
        recommendations.append({
            "action": "Inspect water leaks or cooling optimization",
            "suggested_value": "Reduce water to <1.0 m3/hr",
            "expected_savings": "Up to 5% water"
        })
    if data["production_output"] / data["material_input"] < 0.95:
        recommendations.append({
            "action": "Reduce scrap/rework",
            "suggested_value": "Increase yield to >95%",
            "expected_savings": "Up to 4% material"
        })
    return recommendations

def simulate_optimized_usage(data, recommendations):
    optimized = data.copy()
    for rec in recommendations:
        if "power" in rec["action"].lower():
            val = float(rec["suggested_value"].split("<")[-1].replace("kWh", "").strip())
            optimized["power_usage"] = min(optimized["power_usage"], val)
        if "gas" in rec["action"].lower():
            val = float(rec["suggested_value"].split("<")[-1].replace("Nm3/hr", "").strip())
            optimized["gas_consumption"] = min(optimized["gas_consumption"], val)
        if "water" in rec["action"].lower():
            val = float(rec["suggested_value"].split("<")[-1].replace("m3/hr", "").strip())
            optimized["water_usage"] = min(optimized["water_usage"], val)
        if "yield" in rec["action"].lower():
            optimized["production_output"] = optimized["material_input"] * 0.95
    return optimized
