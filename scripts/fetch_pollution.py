import requests
import pandas as pd
import os

print("Collecting Stable Pollution Location Dataset (200 Rows)...")

API_KEY = "a3c324d19264ccf59d4b30e9fc15bec9ba0fd9608c9b01dd755f3d4f270aec6b"

headers = {
    "X-API-Key": API_KEY
}

url = "https://api.openaq.org/v3/locations"

params = {
    "country_id": "IN",
    "limit": 200
}

response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print("API Error:")
    print(response.text)
    exit()

data = response.json()
locations = data.get("results", [])

print("Locations Retrieved:", len(locations))

records = []

for loc in locations:

    sensors = loc.get("sensors") or []
    pollutant_list = []

    for s in sensors:
        param = s.get("parameter") or {}
        name = param.get("name")
        if name:
            pollutant_list.append(name)

    records.append({
        "location_id": loc.get("id"),
        "name": loc.get("name"),
        "latitude": (loc.get("coordinates") or {}).get("latitude"),
        "longitude": (loc.get("coordinates") or {}).get("longitude"),
        "pollutants": ",".join(pollutant_list),
        "timezone": loc.get("timezone")
    })

df = pd.DataFrame(records)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(base_dir, "data", "raw")

os.makedirs(raw_path, exist_ok=True)

file_path = os.path.join(raw_path, "pollution_200.csv")

df.to_csv(file_path, index=False)

print("✅ Pollution dataset saved at:")
print(file_path)