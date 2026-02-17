import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

START = "20250101"
END = "20260217"

STATIONS = {
    "Delhi_ChandniChowk": (28.6560, 77.2300),
    "Delhi_AnandVihar": (28.6469, 77.3153),  # ✅ ADD THIS
    "Bhopal_TTNagar": (23.2336, 77.4009),
    "Mumbai_Sion": (19.0470, 72.8746),
    "Kolkata_RabindraBharati": (22.6270, 88.3800),
    "Bengaluru_Peenya": (13.0280, 77.5180),
    "Chennai_Manali": (13.1660, 80.2580),
    "Lucknow_Talkatora": (26.8467, 80.9462),
    "Hyderabad_Bollaram": (17.5416, 78.4840),
    "Ahmedabad_SAC_ISRO_IITM": (23.0300, 72.5400)
}


all_data = []

for name, (lat, lon) in STATIONS.items():
    print(f"\nFetching NASA weather for {name}...")

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=T2M,WS2M,RH2M"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={START}"
        f"&end={END}"
        f"&format=JSON"
    )

    response = requests.get(url)
    data = response.json()

    if "properties" not in data:
        print("No data returned")
        continue

    weather = data["properties"]["parameter"]

    df = pd.DataFrame({
        "date": weather["T2M"].keys(),
        "temperature": weather["T2M"].values(),
        "wind_speed": weather["WS2M"].values(),
        "humidity": weather["RH2M"].values()
    })

    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["station"] = name
    df["latitude"] = lat
    df["longitude"] = lon

    all_data.append(df)
    print(name, "records:", len(df))

    time.sleep(1)

final_df = pd.concat(all_data, ignore_index=True)

os.makedirs("data/raw", exist_ok=True)
final_df.to_csv("data/raw/weather_daily_all_stations.csv", index=False)

print("\n✅ NASA weather dataset created")
print("Total records:", len(final_df))
