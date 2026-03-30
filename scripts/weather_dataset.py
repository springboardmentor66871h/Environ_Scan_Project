import requests
import pandas as pd
from datetime import datetime, timedelta
import time



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


end_date = datetime.today()
start_date = end_date - timedelta(days=90)

start = start_date.strftime("%Y-%m-%d")
end = end_date.strftime("%Y-%m-%d")

all_data = []



for city, (lat, lon) in cities.items():
    print(f"Fetching weather data for {city}...")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m"
    )

    try:
        response = requests.get(url)
        data = response.json()

        hourly = data["hourly"]
        timestamps = hourly["time"]

        for i in range(len(timestamps)):
            all_data.append({
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "timestamp": timestamps[i],
                "temperature": hourly["temperature_2m"][i],
                "humidity": hourly["relative_humidity_2m"][i],
                "wind_speed": hourly["wind_speed_10m"][i],
                "wind_direction": hourly["wind_direction_10m"][i]
            })

        time.sleep(1)

    except Exception as e:
        print(f"Error for {city}: {e}")


df = pd.DataFrame(all_data)

df.to_csv(r"C:\Users\admin\Environ_Scan_Project\weather.csv", index=False)

print("\n Weather data collection completed!")
print("Total records:", len(df))
