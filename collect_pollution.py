import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()
OPENAQ_KEY = os.getenv("OPENAQ_API_KEY")

print("Fetching locations in India from OpenAQ v3...")
headers = {"X-API-Key": OPENAQ_KEY}

# Let's keep it at 500. This is plenty of data to get a high-quality, clean dataset!
locations_params = {"iso": "IN", "limit": 500}  
response = requests.get("https://api.openaq.org/v3/locations", headers=headers, params=locations_params)

records = []
required_pollutants = ["pm25", "pm10", "no2", "co", "so2", "o3"]

if response.status_code == 200:
    locations = response.json().get('results', [])
    print(f"Found {len(locations)} locations. Fetching latest measurements for each...")
    
    for loc in locations:
        loc_id = loc.get('id')
        
        # FIX 1: Force empty cities to say "Unknown" instead of being completely blank
        city = loc.get('locality') or loc.get('name') or "Unknown"
        
        sensor_map = {}
        for sensor in loc.get('sensors', []):
            sensor_map[sensor.get('id')] = sensor.get('parameter', {}).get('name', '').lower()
            
        latest_url = f"https://api.openaq.org/v3/locations/{loc_id}/latest"
        latest_resp = requests.get(latest_url, headers=headers)
        
        if latest_resp.status_code == 200:
            for m in latest_resp.json().get('results', []):
                pollutant = sensor_map.get(m.get('sensorsId'))
                
                if pollutant in required_pollutants:
                    last_updated = m.get('datetime', {}).get('utc', '')
                    
                    # FIX 2: Only keep data that is actually from this year! (2026)
                    if "2026" in last_updated:
                        coords = m.get('coordinates', {})
                        lat = coords.get('latitude')
                        lon = coords.get('longitude')
                        
                        if lat and lon:
                            records.append({
                                "city": city,
                                "latitude": lat,
                                "longitude": lon,
                                "pollutant": pollutant,
                                "value": m.get('value'),
                                "last_updated": last_updated
                            })
        time.sleep(0.5)

    df = pd.DataFrame(records)
    print(f"\nSuccessfully collected {len(df)} CLEAN, RECENT pollutant records!")
    
    if len(df) > 0:
        os.makedirs("data/raw", exist_ok=True)
        df.to_csv("data/raw/india_air_pollution_cleaned.csv", index=False)
        print("Module 1 (Pollution) Completed safely!")
else:
    print(f"Failed to fetch locations. Error: {response.status_code}")