import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv
import urllib3

# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY").strip()
headers = {"X-API-Key": API_KEY, "Accept": "application/json"}

location_mapping = {
    "Delhi": {
        "Anand_Vihar": "anand vihar",
        "RK_Puram": "r k puram", 
        "ITO": "ito"
    },
   "Mumbai": {
        "Bandra_Kurla_Complex": "bandra kurla complex", 
        "Colaba": "colaba",                           
        "Worli": "worli"                              
    },
    "Bengaluru": {
        "City_Railway_Station": "city railway station",
        "Silk_Board": "btm layout",
        "Peenya_Industrial_Area": "peenya"
    }
}

allowed_params = {'pm25', 'pm10', 'no2', 'co', 'so2', 'o3'}
all_records = []

for city, locations in location_mapping.items():
    print(f"\n========== Searching for stations in {city} ==========")
    
    loc_params = {"iso": "IN", "locality": city, "limit": 1000}
    loc_res = None
    
    for attempt in range(3):
        try:
            loc_res = requests.get("https://api.openaq.org/v3/locations", headers=headers, params=loc_params, verify=False, timeout=15)
            break 
        except Exception as e:
            print(f" City fetch glitch (Attempt {attempt+1}/3). Retrying...")
            time.sleep(2)
            
    if not loc_res or loc_res.status_code != 200:
        print(f" Failed to fetch {city} after 3 attempts.")
        continue

    available_locs = loc_res.json().get('results', [])

    for osmnx_name, search_keyword in locations.items():
        match = next((l for l in available_locs if search_keyword in l['name'].lower()), None)

        if match:
            print(f" Found {osmnx_name} -> {match['name']}")
            
            for sensor in match.get('sensors', []):
                p_name = sensor['parameter']['name'].lower()
                
                if p_name in allowed_params:
                    meas_url = f"https://api.openaq.org/v3/sensors/{sensor['id']}/measurements"
                    m_res = None
                    
                    # FIX: Force the API to pull recent data matching your weather dates exactly
                   # FIX: Correct parameter names according to OpenAQ v3 docs
                    meas_params = {
                        "limit": 500,
                        "datetime_from": "2026-01-15T00:00:00Z",
                        "datetime_to": "2026-02-15T23:59:59Z"
                    }
                    for attempt in range(3):
                        try:
                            m_res = requests.get(meas_url, headers=headers, params=meas_params, verify=False, timeout=10)
                            break
                        except Exception as e:
                            time.sleep(1) 
                            
                    if m_res and m_res.status_code == 200:
                        data = m_res.json().get('results', [])
                        print(f"    - {p_name}: {len(data)} rows")
                        
                        for item in data:
                            all_records.append({
                                "city": city,
                                "location": osmnx_name, 
                                "parameter": p_name.replace('pm2.5', 'pm25'), 
                                "value": item['value'],
                                "unit": sensor['parameter']['units'],
                                "timestamp": item.get('period', {}).get('datetimeTo', {}).get('utc')
                            })
                    else:
                        print(f" Failed to fetch {p_name} after retries.")
        else:
            print(f" No match found for {osmnx_name}")

df = pd.DataFrame(all_records)

if not df.empty:
    df_clean = df.groupby(['city', 'location', 'parameter', 'unit', 'timestamp'], as_index=False)['value'].mean()
    os.makedirs("data", exist_ok=True)
    output_path = "data/India_3city_air_quality.csv"
    df_clean.to_csv(output_path, index=False)
    print(f"\n Saved {len(df_clean)} rows to {output_path}.")
else:
    print("\nNo data collected.")