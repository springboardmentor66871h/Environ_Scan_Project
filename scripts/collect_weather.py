import requests
import pandas as pd
from datetime import datetime
import os
import time

# -----------------------------
# CONFIG
# -----------------------------
START = "20250101"
END = "20260217"

STATIONS = {
    "DELHI_CHANDINI_CHOWK": (28.6560, 77.2300),
    "DELHI_ANANT_VIHAR": (28.6469, 77.3153),
    "DELHI_ITO": (28.6280, 77.2410),
    "BHOPAL": (23.2336, 77.4009),
    "BHOPAL_PARYAVARAN_PARK": (23.2500, 77.4200),
    "BHOPAL_IDGAH_HILLS": (23.2550, 77.4100),
    "MUMBAI": (19.0470, 72.8746),
    "MUMBAI_BYCULLA": (18.9767, 72.8331),
    "MUMBAI_CHAKALA_ANDHERI": (19.1100, 72.8620),
    "KOLKATA": (22.6270, 88.3800),
    "KOLKATA_BALLYGUNGE": (22.5250, 88.3630),
    "KOLKATA_JADAVPUR": (22.4993, 88.3710),
    "BENGELURU": (13.0280, 77.5180),
    "BENGALURU_HEBBAL": (13.0358, 77.5970),
    "BENGALURU_RAILWAY_STATION": (12.9784, 77.5686),
    "CHENNAI": (13.1660, 80.2580),
    "CHENNAI_ALANDUR_BUS_DEPOT": (13.0046, 80.2017),
    "CHENNAI_VELACHERY": (12.9750, 80.2212),
    "LUCKNOW": (26.8467, 80.9462),
    "LUCKNOW_TALKATORA": (26.8350, 80.9000),
    "LUCKNOW_LALBAGH": (26.8485, 80.9416),
    "HYDERABAD": (17.5416, 78.4840),
    "HYDERABAD_PATENCHERU": (17.5330, 78.2600),
    "HYDERABAD_SOMAJIGUDA": (17.4240, 78.4595),
    "AHEMEDABAD": (23.0300, 72.5400),
    "AHMEDABAD_SOMAJIGUDA": (23.0370, 72.5666),
    "AHMEDABAD_SVPT": (23.0350, 72.5800),
}

all_data = []

# -----------------------------
# DATA FETCH
# -----------------------------
for name, (lat, lon) in STATIONS.items():
    city = name.split("_")[0]   # Extract city name

    print(f"\n📡 Fetching NASA weather for {name}...")

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=T2M,WS2M,RH2M,WD2M"
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
        print(f"⚠ No data returned for {name}")
        continue

    weather = data["properties"]["parameter"]

    df = pd.DataFrame({
        "timestamp": weather["T2M"].keys(),
        "temperature": weather["T2M"].values(),
        "humidity": weather["RH2M"].values(),
        "wind_speed": weather["WS2M"].values(),
        "wind_direction": weather["WD2M"].values()
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d")
    df["city"] = city
    df["station"] = name
    df["latitude"] = lat
    df["longitude"] = lon

    all_data.append(df)
    print(f"✅ {name} records: {len(df)}")

    time.sleep(1)

# -----------------------------
# SAVE DATASET
# -----------------------------
final_df = pd.concat(all_data, ignore_index=True)

os.makedirs("data/raw", exist_ok=True)
final_df.to_csv("data/raw/weather_daily_all_stations.csv", index=False)

print("\n🎉 NASA Weather Dataset Created Successfully")
print("📊 Total records:", len(final_df))
