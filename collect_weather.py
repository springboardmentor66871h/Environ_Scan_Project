import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

# 1. Load the secret keys
load_dotenv()
WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

if not WEATHER_KEY:
    print("Error: Could not find OPENWEATHER_API_KEY in .env file!")
    exit()

print("Loading pollution dataset to find locations...")
# Read the dataset we just created
pollution_df = pd.read_csv("data/raw/india_air_pollution_cleaned.csv")

# Get unique locations (latitude, longitude, city) to minimize API calls
locations = pollution_df[['city', 'latitude', 'longitude']].drop_duplicates()
print(f"Found {len(locations)} unique locations. Fetching real weather data...")

weather_records = []
url = "https://api.openweathermap.org/data/2.5/weather"

# 2. Fetch real weather for each unique location
for index, row in locations.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    city = row['city']
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_KEY,
        "units": "metric"  # This gets temperature in Celsius
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data.get("main", {})
        wind = data.get("wind", {})
        
        weather_records.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "temperature": main.get("temp"),
            "humidity": main.get("humidity"),
            "wind_speed": wind.get("speed"),
            "wind_direction": wind.get("deg")
        })
    elif response.status_code == 401:
        print(f"\nError 401: Unauthorized. Your OpenWeather API key is invalid or not activated yet.")
        break
    elif response.status_code == 429:
        print(f"\nError 429: Too Many Requests. We hit the API speed limit!")
        break
    else:
        print(f"Failed to fetch weather for {city}. Error: {response.status_code}")
        
    # Sleep for 1 second to respect API limits (60 calls per minute)
    time.sleep(1)

# 3. Save the results
weather_df = pd.DataFrame(weather_records)

if len(weather_df) > 0:
    print(f"\nSuccessfully collected weather for {len(weather_df)} locations!")
    output_file = "data/raw/india_weather_dataset_new.csv"
    weather_df.to_csv(output_file, index=False)
    print(f"Saved real weather dataset to {output_file}")
    print("Module 1 (Weather) Completed!")
else:
    print("\nNo weather data collected.")