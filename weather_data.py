import requests
import pandas as pd
import os
import time

# Target Date Window
START_DATE = "2025-12-01"
END_DATE = "2026-02-15"

# Master Location Dictionary
locations = {
    "Delhi": {
        "Anand_Vihar": {"lat": 28.6508, "lon": 77.3152},
        "RK_Puram": {"lat": 28.5632, "lon": 77.1869},
        "ITO": {"lat": 28.6284, "lon": 77.2410},
        "Punjabi_Bagh": {"lat": 28.6683, "lon": 77.1167},
        "Bawana": {"lat": 28.7955, "lon": 77.0324}
    },
    "Mumbai": {
        "Colaba": {"lat": 18.9067, "lon": 72.8147},
        "Worli": {"lat": 19.0163, "lon": 72.8166}
    },
    "Bengaluru": {
        "Peenya_Industrial": {"lat": 13.0285, "lon": 77.5197},
        "Silk_Board": {"lat": 12.9172, "lon": 77.6228}
    }
}

all_weather_records = []

print("Starting GPS-Localized Weather Extraction (Open-Meteo)...")

for city, loc_data in locations.items():
    print(f"\n========== Fetching Weather for {city} ==========")
    
    for loc_name, meta in loc_data.items():
        print(f"   Processing {loc_name} ({meta['lat']}, {meta['lon']})...")
        
        # Open-Meteo historical forecast endpoint
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": meta['lat'],
            "longitude": meta['lon'],
            "start_date": START_DATE,
            "end_date": END_DATE,
            "hourly": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m",
            "timezone": "UTC"
        }
        
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                data = res.json()
                hourly = data.get('hourly', {})
                
                times = hourly.get('time', [])
                temps = hourly.get('temperature_2m', [])
                hums = hourly.get('relative_humidity_2m', [])
                press = hourly.get('surface_pressure', [])
                w_speeds = hourly.get('wind_speed_10m', [])
                w_dirs = hourly.get('wind_direction_10m', [])
                
                # Combine lists into row dictionaries
                for i in range(len(times)):
                    all_weather_records.append({
                        "city": city,
                        "location": loc_name,
                        "timestamp": times[i].replace("T", " ") + ":00", # Align format with AQ dataset exactly
                        "temperature_c": temps[i],
                        "humidity_percent": hums[i],
                        "pressure_hpa": press[i],
                        "wind_speed_mps": w_speeds[i],
                        "wind_direction_deg": w_dirs[i]
                    })
                print(f"   Captured {len(times)} hourly records.")
            else:
                print(f"    Failed to fetch data: HTTP {res.status_code}")
                
            time.sleep(1) # Be polite to the free API
            
        except Exception as e:
            print(f" Connection error: {e}")

# ==========================================
# FINAL COMPILATION & EXPORT
# ==========================================
print("\n Weather extraction complete. Formatting final dataset...")
df_weather = pd.DataFrame(all_weather_records)

if not df_weather.empty:
    # Ensure timestamps are strings so Excel/CSVs don't hide the hours
    df_weather['timestamp'] = df_weather['timestamp'].astype(str)
    
    os.makedirs("data", exist_ok=True)
    output_path = "data/India_Weather.csv"
    df_weather.to_csv(output_path, index=False)
    
    print(f" SUCCESS! Saved {len(df_weather)} gap-free rows to {output_path}.")
else:
    print("\n Process failed. No data collected.")