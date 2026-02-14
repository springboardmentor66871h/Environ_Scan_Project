import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WAQI_API_KEY")

cities = ["Hyderabad", "Delhi", "Mumbai", "Chennai", "Bangalore",
          "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]

all_data = []

# Repeat multiple times to collect more rows
for iteration in range(50):   # 50 runs × 10 cities × pollutants
    print(f"Iteration {iteration + 1}")

    for city in cities:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error {response.status_code} for {city}")
            continue

        data = response.json()

        if data["status"] != "ok":
            print(f"No data for {city}")
            continue

        iaqi = data["data"]["iaqi"]
        geo = data["data"]["city"]["geo"]
        time_stamp = data["data"]["time"]["iso"]

        pollutants = ["pm25", "pm10", "no2", "so2", "co", "o3"]

        for pollutant in pollutants:
            if pollutant in iaqi:
                all_data.append({
                    "city": city.capitalize(),
                    "latitude": geo[0],
                    "longitude": geo[1],
                    "timestamp": time_stamp,
                    "pollutant": pollutant,
                    "value": iaqi[pollutant]["v"]
                })

    time.sleep(2)  # small delay to avoid rate limit

df = pd.DataFrame(all_data)

df.to_csv("../data/raw/pollution/pollution_data.csv", index=False)

print("Total rows collected:", df.shape[0])
print("Pollution Data Saved Successfully")
