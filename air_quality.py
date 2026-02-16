import requests
import pandas as pd
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# Credentials
OPENAQ_KEY = os.getenv("OPENAQ_API_KEY").strip()
OWM_KEY = os.getenv("OPENWEATHER_API_KEY").strip()

# Target Date Window
START_DATE = "2025-12-01T00:00:00Z"
END_DATE = "2026-02-15T23:59:59Z"

# Convert to UNIX timestamps for OpenWeatherMap
start_unix = int(datetime.strptime(START_DATE, "%Y-%m-%dT%H:%M:%SZ").timestamp())
end_unix = int(datetime.strptime(END_DATE, "%Y-%m-%dT%H:%M:%SZ").timestamp())

# Master Location Dictionary (Expanded for Delhi's Top Stations)
locations = {
    "Delhi": {
        "Anand_Vihar": {"keyword": "anand vihar", "lat": 28.6508, "lon": 77.3152},
        "RK_Puram": {"keyword": "r k puram", "lat": 28.5632, "lon": 77.1869},
        "ITO": {"keyword": "ito", "lat": 28.6284, "lon": 77.2410},
        "Punjabi_Bagh": {"keyword": "punjabi bagh", "lat": 28.6683, "lon": 77.1167},
        "Bawana": {"keyword": "bawana", "lat": 28.7955, "lon": 77.0324}
    },
    "Mumbai": {
        "Colaba": {"keyword": "colaba", "lat": 18.9067, "lon": 72.8147},
        "Worli": {"keyword": "worli", "lat": 19.0163, "lon": 72.8166}
    },
    "Bengaluru": {
        "Peenya_Industrial": {"keyword": "peenya", "lat": 13.0285, "lon": 77.5197},
        "Silk_Board": {"keyword": "btm layout", "lat": 12.9172, "lon": 77.6228}
    }
}

allowed_params = ['pm25', 'pm10', 'no2', 'co', 'so2', 'o3']
all_hybrid_records = []

print(" Starting Hybrid API Data Fusion (OpenAQ + OpenWeatherMap)...")

for city, loc_data in locations.items():
    print(f"\n========== {city} ==========")
    
    # 1. Fetch OpenAQ City Base
    openaq_headers = {"X-API-Key": OPENAQ_KEY, "Accept": "application/json"}
    loc_res = requests.get("https://api.openaq.org/v3/locations", headers=openaq_headers, params={"iso": "IN", "locality": city, "limit": 1000}, verify=False)
    available_locs = loc_res.json().get('results', []) if loc_res.status_code == 200 else []

    for loc_name, meta in loc_data.items():
        print(f"\n Processing {loc_name}...")
        
        # Dictionary to temporarily hold hourly data for this specific location
        hourly_data = {}

        # ==========================================
        # SOURCE 1: OPENWEATHERMAP (The Flawless Baseline)
        # ==========================================
        owm_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={meta['lat']}&lon={meta['lon']}&start={start_unix}&end={end_unix}&appid={OWM_KEY}"
        owm_res = requests.get(owm_url)
        
        if owm_res.status_code == 200:
            for item in owm_res.json().get('list', []):
                dt = pd.to_datetime(item['dt'], unit='s', utc=True).floor('h')
                comps = item['components']
                
                hourly_data[dt] = {
                    "city": city,
                    "location": loc_name,
                    "timestamp": dt,
                    "pm25": comps.get('pm2_5'),
                    "pm10": comps.get('pm10'),
                    "no2": comps.get('no2'),
                    "co": comps.get('co'),
                    "so2": comps.get('so2'),
                    "o3": comps.get('o3')
                }
            print(f" OWM Data: Captured {len(hourly_data)} flawless hours.")
        else:
            print(f" OWM Data: Failed to fetch.")

        # ==========================================
        # SOURCE 2: OPENAQ (The Ground-Truth Override)
        # ==========================================
        match = next((l for l in available_locs if meta['keyword'] in l['name'].lower()), None)
        
        if match:
            openaq_points = 0
            for sensor in match.get('sensors', []):
                p_name = sensor['parameter']['name'].lower().replace('pm2.5', 'pm25')
                
                if p_name in allowed_params:
                    meas_url = f"https://api.openaq.org/v3/sensors/{sensor['id']}/measurements"
                    m_params = {"limit": 1000, "datetime_from": START_DATE, "datetime_to": END_DATE}
                    
                    m_res = requests.get(meas_url, headers=openaq_headers, params=m_params, verify=False)
                    if m_res.status_code == 200:
                        for item in m_res.json().get('results', []):
                            dt = pd.to_datetime(item['period']['datetimeTo']['utc']).floor('h')
                            val = item['value']
                            
                            # If this hour exists in our OWM baseline, override it with the real OpenAQ ground truth!
                            if dt in hourly_data:
                                hourly_data[dt][p_name] = val
                                openaq_points += 1
            print(f" OpenAQ Data: Injected {openaq_points} physical sensor readings.")
        else:
            print(f" OpenAQ Data: Sensor offline/missing. Relying entirely on OWM satellite data.")

        # Add all processed hours for this location into the master list
        all_hybrid_records.extend(list(hourly_data.values()))

# ==========================================
# FINAL COMPILATION & EXPORT
# ==========================================
print("\n Fusion complete. Formatting final dataset...")
df_hybrid = pd.DataFrame(all_hybrid_records)

if not df_hybrid.empty:
    # 1. Strip the timezone
    df_hybrid['timestamp'] = df_hybrid['timestamp'].dt.tz_localize(None)
    
    # 2. Convert to a string so the time doesn't get hidden
    df_hybrid['timestamp'] = df_hybrid['timestamp'].astype(str)
    
    # Save directly to CSV (Changed from Excel to CSV)
    os.makedirs("data", exist_ok=True)
    output_path = "data/India_Air_Quality.csv"
    df_hybrid.to_csv(output_path, index=False)
    
    print(f"SUCCESS! Saved {len(df_hybrid)} gap-free rows to {output_path}.")
else:
    print("\nProcess failed. No data collected.")