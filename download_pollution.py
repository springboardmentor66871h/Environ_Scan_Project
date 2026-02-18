import requests
import pandas as pd
import os

# 1. Create the folder structure required by your mentor
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# 2. Define our parameters
cities = ["Delhi", "Mumbai"]
pollutants = ["pm25", "pm10", "no2", "co", "so2", "o3"]
date_from = "2026-01-01T00:00:00Z"
date_to = "2026-01-07T23:59:59Z"
limit = 1000 # Max records per request

all_data = []

print("Starting OpenAQ data download...")

# 3. Loop through cities and fetch data
for city in cities:
    print(f"Fetching data for {city}...")
    url = "https://api.openaq.org/v2/measurements"
    
    params = {
        "city": city,
        "parameter": pollutants,
        "date_from": date_from,
        "date_to": date_to,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        
        # 4. Extract only the required columns
        for item in results:
            record = {
                "City": item.get('city'),
                "Latitude": item['coordinates']['latitude'] if 'coordinates' in item else None,
                "Longitude": item['coordinates']['longitude'] if 'coordinates' in item else None,
                "Timestamp": item['date']['utc'],
                "Pollutant": item['parameter'],
                "Value": item['value']
            }
            all_data.append(record)
    else:
        print(f"Failed to fetch data for {city}. Status code: {response.status_code}")

# 5. Save to CSV
if all_data:
    df = pd.DataFrame(all_data)
    # Drop rows without coordinates just to be safe
    df = df.dropna(subset=['Latitude', 'Longitude']) 
    
    file_path = 'data/raw/pollution_data.csv'
    df.to_csv(file_path, index=False)
    print(f"Success! Downloaded {len(df)} records.")
    print(f"Saved to: {file_path}")
else:
    print("No data found for the given parameters.")
