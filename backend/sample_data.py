import random

def generate_sample_data():
    # Synthetic but realistic resource values for a forging furnace
    return {
        "furnace_temp": random.uniform(1150, 1250),
        "power_usage": random.uniform(100, 150),        # kWh
        "gas_consumption": random.uniform(50, 80),      # Nm3/hr
        "water_usage": random.uniform(0.8, 1.2),        # m3/hr
        "material_input": random.uniform(500, 600),     # kg/hr
        "production_output": random.uniform(480, 590),  # kg/hr
        "ambient_temp": random.uniform(30, 40),         # °C
        "downtime": random.uniform(0, 0.2),             # hr/hr
    }
