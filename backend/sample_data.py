import random

def generate_sample_data():
    # Synthetic data for all relevant KPIs
    output = random.uniform(480, 590)
    input_ = random.uniform(500, 600)
    scrap = input_ - output
    elec = random.uniform(100, 150)
    gas = random.uniform(50, 80)
    water = random.uniform(0.8, 1.2)
    cooling_in = random.uniform(25, 30)
    cooling_out = cooling_in + random.uniform(6, 12)
    flue_gas_temp = random.uniform(300, 400)
    flue_gas_comp = {
        "CO2": random.uniform(8, 10),
        "NOx": random.uniform(0.02, 0.07),
        "SOx": random.uniform(0.01, 0.03),
        "O2": random.uniform(2, 7)
    }
    die_temp = random.uniform(200, 400)
    die_wear_rate = random.uniform(0, 1)
    downtime = random.uniform(0, 0.2)
    runtime = 1 - downtime
    return {
        "furnace_temp": random.uniform(1150, 1250),
        "power_usage": elec,
        "idle_power_usage": random.uniform(0, 10),
        "peak_power": random.uniform(120, 180),
        "gas_consumption": gas,
        "water_usage": water,
        "material_input": input_,
        "production_output": output,
        "ambient_temp": random.uniform(30, 40),
        "downtime": downtime,
        "runtime": runtime,
        "target_output": 575,
        "cycle_time": random.uniform(1, 4),
        "die_temp": die_temp,
        "die_wear_rate": die_wear_rate,
        "maintenance_count": random.randint(0, 2),
        "mtbf": random.uniform(300, 1000),
        "cooling_water_in": cooling_in,
        "cooling_water_out": cooling_out,
        "water_discharge_temp": random.uniform(30, 40),
        "water_discharge_pH": random.uniform(6.5, 8.5),
        "flue_gas_temp": flue_gas_temp,
        "flue_gas_comp": flue_gas_comp
    }
