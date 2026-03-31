import pandas as pd
import random
import os
from datetime import datetime, timedelta

# ===============================
# Load Pollution Dataset
# ===============================

pollution_df = pd.read_csv("india_air_pollution_cleaned.csv")

print("Pollution dataset loaded")
print("Total Unique Cities:", pollution_df["city"].nunique())

# ===============================
# Generate Weather Data
# ===============================

records = []

for index, row in pollution_df.iterrows():
    for i in range(7):
        records.append({
            "city": row["city"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "timestamp": datetime.now() - timedelta(days=i),
            "temperature": round(random.uniform(20, 40), 2),
            "humidity": round(random.uniform(30, 95), 2),
            "wind_speed": round(random.uniform(1, 20), 2),
            "wind_direction": round(random.uniform(0, 360), 2),
        })
weather_df = pd.DataFrame(records)

print("Total Records Generated:", len(weather_df))

print("\nEntire Dataset:\n")
print(weather_df.to_string())
# ===============================
# Safe Save (Auto Rename if Exists)
# ===============================

filename = "india_weather_dataset.csv"

if os.path.exists(filename):
    filename = "india_weather_dataset_new.csv"

weather_df.to_csv(filename, index=False)

print(f"\nWeather dataset saved successfully as {filename}")
print("Project Completed")
