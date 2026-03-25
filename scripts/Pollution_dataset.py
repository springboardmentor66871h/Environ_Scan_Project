import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# --------------------------
# 10 Major Indian Cities
# --------------------------

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462)
}

# --------------------------
# Date Range (Last 30 Days)
# --------------------------

end_date = datetime.today()
start_date = end_date - timedelta(days=90)

start = start_date.strftime("%Y-%m-%d")
end = end_date.strftime("%Y-%m-%d")

all_data = []

# --------------------------
# Fetch Data
# --------------------------

for city, (lat, lon) in cities.items():
    print(f"Fetching data for {city}...")

    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=pm10,pm2_5,nitrogen_dioxide,carbon_monoxide,sulphur_dioxide,ozone"
        f"&start_date={start}&end_date={end}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        hourly = data["hourly"]
        timestamps = hourly["time"]

        pollutants_map = {
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "nitrogen_dioxide": "NO2",
            "carbon_monoxide": "CO",
            "sulphur_dioxide": "SO2",
            "ozone": "O3"
        }

        for key, pollutant_name in pollutants_map.items():
            values = hourly.get(key, [])

            for i in range(len(timestamps)):
                if i < len(values) and values[i] is not None:
                    all_data.append({
                        "city": city,
                        "latitude": lat,
                        "longitude": lon,
                        "timestamp": timestamps[i],
                        "pollutant": pollutant_name,
                        "value": values[i]
                    })

        time.sleep(1)

    except Exception as e:
        print(f"Error for {city}: {e}")

# --------------------------
# Save CSV
# --------------------------

df = pd.DataFrame(all_data)

df.to_csv(r"C:\Users\admin\Environ_Scan_Project\pollution.csv", index=False)

print("\n✅ Data collection completed!")
print("Total records:", len(df))
