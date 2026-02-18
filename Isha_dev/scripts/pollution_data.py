import requests
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path

# 🔴 YOUR OPENAQ API KEY
OPENAQ_API_KEY = "365f11bdd62574e3c01af1c76402a5109a1d54a7cfafc5d1be9054fef3077742"

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
CITIES_FILE = BASE_DIR / "data" / "config" / "cities.csv"  # New format with area
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "pollution"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cities with areas
cities_df = pd.read_csv(CITIES_FILE)
print("="*70)
print("POLLUTION DATA COLLECTOR - AREA LEVEL")
print("="*70)
print(f"Loaded {len(cities_df)} city-areas from {CITIES_FILE}")
print("\nFirst few entries:")
print(cities_df.head(10).to_string())
print()

# Pollutants we want
POLLUTANT_IDS = {
    "pm25": 2,
    "pm10": 1, 
    "no2": 8,
    "co": 10005,
    "so2": 7,
    "o3": 3
}

def get_area_coordinates(city, area, state):
    """Get coordinates for specific area within city"""
    query = f"{area}, {city}, {state}, India"
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'AirQualityDataCollection/1.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon, query
    except:
        pass
    return None, None, query

def get_locations_near_coordinates(lat, lon, radius=10000):  # 10km radius for area-level
    """Find monitoring locations near coordinates"""
    url = "https://api.openaq.org/v3/locations"
    params = {
        'coordinates': f"{lat},{lon}",
        'radius': radius,
        'limit': 10
    }
    headers = {'X-API-Key': OPENAQ_API_KEY}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
    except:
        pass
    return []

def get_sensors_for_location(location_id):
    """Get sensors for a specific location"""
    url = f"https://api.openaq.org/v3/locations/{location_id}/sensors"
    headers = {'X-API-Key': OPENAQ_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
    except:
        pass
    return []

def get_measurements_for_sensor(sensor_id, limit=10):
    """Get latest measurements for a specific sensor"""
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
    params = {'limit': limit}
    headers = {'X-API-Key': OPENAQ_API_KEY}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
    except:
        pass
    return []

# TRACKING
area_status = []
all_measurements = []

for idx, row in cities_df.iterrows():
    city = row['city']
    area = row['area']
    state = row['state']
    
    print(f"\n[{idx+1}/{len(cities_df)}] {city} - {area}...")
    
    # Get coordinates for this specific area
    lat, lon, query = get_area_coordinates(city, area, state)
    
    if lat is None or lon is None:
        print(f"  ✗ Could not get coordinates for: {query}")
        area_status.append({
            'city': city,
            'area': area,
            'status': 'NO_COORDINATES',
            'locations_found': 0,
            'measurements_found': 0
        })
        continue
    
    print(f"  ✓ Coordinates: {lat:.4f}, {lon:.4f}")
    
    # Find monitoring locations near this area
    locations = get_locations_near_coordinates(lat, lon)
    
    if not locations:
        print(f"  ✗ No monitoring stations found near {area}")
        area_status.append({
            'city': city,
            'area': area,
            'status': 'NO_LOCATIONS',
            'locations_found': 0,
            'measurements_found': 0
        })
        continue
    
    print(f"  ✓ Found {len(locations)} monitoring stations")
    
    area_measurements = 0
    area_locations_with_data = 0
    
    # Check each location
    for location in locations:
        loc_id = location['id']
        loc_name = location.get('name', 'Unknown')
        loc_distance = "unknown"  # Could calculate if needed
        
        # Get sensors
        sensors = get_sensors_for_location(loc_id)
        
        location_has_data = False
        
        if sensors:
            for sensor in sensors:
                sensor_id = sensor['id']
                sensor_param = sensor.get('parameter', {})
                
                if isinstance(sensor_param, dict):
                    param_name = sensor_param.get('name', '').lower()
                else:
                    param_name = str(sensor_param).lower()
                
                # Check if target pollutant
                if param_name in POLLUTANT_IDS:
                    measurements = get_measurements_for_sensor(sensor_id, limit=5)
                    
                    if measurements:
                        location_has_data = True
                        for m in measurements:
                            all_measurements.append({
                                'city': city,
                                'area': area,
                                'state': state,
                                'area_lat': lat,
                                'area_lon': lon,
                                'location_id': loc_id,
                                'location_name': loc_name,
                                'location_lat': location.get('coordinates', {}).get('latitude'),
                                'location_lon': location.get('coordinates', {}).get('longitude'),
                                'sensor_id': sensor_id,
                                'pollutant': param_name,
                                'value': m.get('value'),
                                'unit': m.get('unit'),
                                'timestamp': m.get('datetime', {}).get('utc')
                            })
                            area_measurements += 1
                    
                    time.sleep(0.2)
        
        if location_has_data:
            area_locations_with_data += 1
        
        time.sleep(0.5)
    
    # Record area status
    if area_measurements > 0:
        status = 'HAS_DATA'
        print(f"  ✓ COLLECTED: {area_measurements} measurements from {area_locations_with_data} locations")
    else:
        status = 'NO_MEASUREMENTS'
        print(f"  ✗ No measurements found for {area}")
    
    area_status.append({
        'city': city,
        'area': area,
        'status': status,
        'locations_found': len(locations),
        'locations_with_data': area_locations_with_data,
        'measurements_found': area_measurements
    })
    
    time.sleep(1)

# =============================================
# SAVE DATA
# =============================================
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save measurements
if all_measurements:
    df = pd.DataFrame(all_measurements)
    
    # Create pivot table for easier analysis
    pivot_df = df.pivot_table(
        index=['city', 'area', 'state', 'area_lat', 'area_lon'],
        columns='pollutant',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    # Flatten column names
    pivot_df.columns.name = None
    
    # Save both formats
    raw_file = OUTPUT_DIR / f"pollution_raw_{timestamp}.csv"
    df.to_csv(raw_file, index=False)
    
    pivot_file = OUTPUT_DIR / f"pollution_by_area_{timestamp}.csv"
    pivot_df.to_csv(pivot_file, index=False)
    
    print(f"\n✅ Saved {len(df)} measurements to {raw_file}")
    print(f"✅ Saved {len(pivot_df)} area summaries to {pivot_file}")
else:
    print("\n⚠ No measurements collected")
    # Create empty files with headers
    empty_raw = pd.DataFrame(columns=['city', 'area', 'state', 'area_lat', 'area_lon', 
                                       'location_id', 'location_name', 'pollutant', 'value'])
    empty_raw.to_csv(OUTPUT_DIR / f"pollution_raw_{timestamp}.csv", index=False)

# Save area status report
status_df = pd.DataFrame(area_status)
status_file = OUTPUT_DIR / f"area_pollution_status.csv"
status_df.to_csv(status_file, index=False)
print(f"✅ Saved area status report to {status_file}")

# =============================================
# DISPLAY AREA SUMMARY
# =============================================
print("\n" + "="*70)
print("AREA-LEVEL COLLECTION SUMMARY")
print("="*70)

# Summary statistics
total_areas = len(area_status)
areas_with_data = sum(1 for a in area_status if a['status'] == 'HAS_DATA')
areas_no_locations = sum(1 for a in area_status if a['status'] == 'NO_LOCATIONS')
areas_no_coords = sum(1 for a in area_status if a['status'] == 'NO_COORDINATES')
areas_no_measurements = sum(1 for a in area_status if a['status'] == 'NO_MEASUREMENTS')

print(f"\n📊 OVERALL STATISTICS:")
print(f"  Total areas processed: {total_areas}")
print(f"  ✅ Areas WITH pollution data: {areas_with_data}")
print(f"  ⚠ Areas with locations but no measurements: {areas_no_measurements}")
print(f"  ⚠ Areas with no monitoring locations: {areas_no_locations}")
print(f"  ⚠ Areas with no coordinates: {areas_no_coords}")

# Show areas with data by city
if areas_with_data > 0:
    print(f"\n✅ AREAS WITH POLLUTION DATA:")
    areas_df = pd.DataFrame(area_status)
    for city in areas_df[areas_df['status'] == 'HAS_DATA']['city'].unique():
        city_areas = areas_df[(areas_df['city'] == city) & (areas_df['status'] == 'HAS_DATA')]
        print(f"\n  {city}:")
        for _, row in city_areas.iterrows():
            print(f"    - {row['area']}: {row['measurements_found']} measurements")

print("\n" + "="*70)