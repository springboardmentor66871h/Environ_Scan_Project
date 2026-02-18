import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

# Your OpenWeatherMap API key
API_KEY = "faae25ac6d3734bffccd229b2066b1cd"

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
CITIES_FILE = BASE_DIR / "data" / "config" / "cities.csv"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "weather"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cities with areas
cities_df = pd.read_csv(CITIES_FILE)
print("="*70)
print("WEATHER DATA COLLECTOR - AREA LEVEL (WITH FALLBACK)")
print("="*70)
print(f"Loaded {len(cities_df)} city-areas")

def get_coordinates_for_location(query):
    """Get coordinates for any location query"""
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        'q': query,
        'limit': 1,
        'appid': API_KEY
    }
    
    try:
        response = requests.get(geo_url, params=geo_params, timeout=10)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return data['lat'], data['lon']
    except:
        pass
    return None, None

def get_weather_for_area(city, area, state):
    """Get weather for specific area with fallback to city"""
    
    # Try 1: Area, City, State format
    queries = [
        f"{area}, {city}, {state}, IN",  # Most specific
        f"{area}, {city}, IN",            # Without state
        f"{city}, {state}, IN",           # City level
        f"{city}, IN"                      # Just city
    ]
    
    lat, lon = None, None
    used_query = None
    
    for query in queries:
        lat, lon = get_coordinates_for_location(query)
        if lat and lon:
            used_query = query
            break
        time.sleep(0.5)
    
    if not lat or not lon:
        print(f"  ✗ Could not get coordinates for any format")
        return None
    
    # Get weather
    try:
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        if weather_response.status_code != 200:
            return None
        
        data = weather_response.json()
        
        # Add location_method to track which query worked
        location_method = "area" if area in used_query else "city_fallback"
        
        return {
            'city': city,
            'area': area,
            'state': state,
            'area_lat': lat,
            'area_lon': lon,
            'location_method': location_method,
            'query_used': used_query,
            'timestamp': datetime.now().isoformat(),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'wind_gust': data['wind'].get('gust', 0),
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 0),
            'country': data['sys']['country'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat()
        }
        
    except Exception as e:
        print(f"  ✗ Weather API error: {e}")
        return None

# Collect weather data
all_data = []
successful = []
failed = []
fallback_count = 0

print("\nCollecting weather data for each area...")
print("-" * 70)

for idx, row in cities_df.iterrows():
    city = row['city']
    area = row['area']
    state = row['state']
    
    print(f"[{idx+1}/{len(cities_df)}] {city} - {area}...")
    
    weather_data = get_weather_for_area(city, area, state)
    
    if weather_data:
        all_data.append(weather_data)
        successful.append(f"{city}-{area}")
        
        if weather_data['location_method'] == 'city_fallback':
            fallback_count += 1
            print(f"  ✓ (city fallback) {weather_data['temperature']}°C, {weather_data['humidity']}% humidity")
        else:
            print(f"  ✓ (area level) {weather_data['temperature']}°C, {weather_data['humidity']}% humidity")
    else:
        failed.append(f"{city}-{area}")
        print(f"  ✗ Failed")
    
    time.sleep(1)

# Save to CSV
if all_data:
    df = pd.DataFrame(all_data)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = OUTPUT_DIR / f"weather_areas_{timestamp}.csv"
    df.to_csv(filename, index=False)
    
    print("\n" + "="*70)
    print("COLLECTION COMPLETE")
    print("="*70)
    print(f"Successful areas: {len(successful)}")
    print(f"Failed areas: {len(failed)}")
    print(f"Area-level success: {len(successful) - fallback_count}")
    print(f"City fallback used: {fallback_count}")
    print(f"\nFile saved: {filename}")
    
    # Show areas that used city fallback
    if fallback_count > 0:
        print("\n⚠ Areas using city fallback (no area-level coordinates):")
        fallback_areas = df[df['location_method'] == 'city_fallback']
        for _, row in fallback_areas.iterrows():
            print(f"  {row['city']} - {row['area']}")
    
    print("\nSample data (first 10 areas):")
    print(df[['city', 'area', 'temperature', 'humidity', 'wind_speed', 'weather_main']].head(10).to_string())
    
    # Summary by city
    print("\n📊 Summary by city:")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        print(f"  {city}: {len(city_data)} areas, {city_data['temperature'].mean():.1f}°C avg")
else:
    print("\nNo data collected")