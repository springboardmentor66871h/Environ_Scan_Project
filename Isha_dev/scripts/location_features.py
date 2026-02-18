import pandas as pd
import requests
import time
from datetime import datetime
from pathlib import Path

# Setup paths
base_dir = Path(__file__).parent.parent
config_file = base_dir / "data" / "config" / "cities.csv"  # New format with area
output_dir = base_dir / "data" / "raw" / "location"
output_dir.mkdir(parents=True, exist_ok=True)

# Load cities with areas
cities_df = pd.read_csv(config_file)
print("="*70)
print("LOCATION FEATURES COLLECTOR - AREA LEVEL")
print("="*70)
print(f"Loaded {len(cities_df)} city-areas from config")
print("\nFirst few entries:")
print(cities_df.head(10).to_string())
print()

def get_area_coordinates(city, area, state):
    """Get coordinates for specific area within city"""
    query = f"{area}, {city}, {state}, India"
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'EnviroScan/1.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data['lat']), float(data['lon']), query
    except Exception as e:
        print(f"    Error getting coordinates: {e}")
    return None, None, query

def query_overpass(query):
    """Execute Overpass API query"""
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = requests.get(url, params={'data': query}, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def get_location_features(city, area, state, lat, lon):
    """Get location features for a specific area using Overpass API"""
    
    # Create bounding box (roughly 5km x 5km for area-level)
    # 0.05 degrees ≈ 5.5km
    bbox = f"{lat-0.05},{lon-0.05},{lat+0.05},{lon+0.05}"
    
    features = {
        'city': city,
        'area': area,
        'state': state,
        'latitude': lat,
        'longitude': lon,
        'timestamp': datetime.now().isoformat(),
        
        # Road network features
        'road_segments': 0,
        'road_km': 0,
        'road_density': 0,
        
        # Source identification features
        'industrial_count': 0,
        'farmland_count': 0,
        'dump_sites_count': 0,
        'power_plants_count': 0,
        'bus_stops_count': 0,
        'railway_stations_count': 0,
        'parking_lots_count': 0,
        
        # Binary flags
        'has_industrial': 0,
        'has_farmland': 0,
        'has_dump': 0,
        'has_power_plant': 0
    }
    
    # 1. Get road network (count and estimate length)
    print(f"    Querying roads...")
    road_query = f"""
    [out:json];
    (
      way["highway"~"primary|secondary|tertiary|residential"]({bbox});
    );
    out count;
    """
    result = query_overpass(road_query)
    if result and 'elements' in result:
        features['road_segments'] = len(result['elements'])
        # Rough estimate: average road segment ~200m
        features['road_km'] = round(len(result['elements']) * 0.2, 2)
        # Area in sq km: ~30 sq km for 5.5km radius
        features['road_density'] = round(features['road_km'] / 30, 2)
    
    # 2. Get industrial areas
    print(f"    Querying industrial areas...")
    industrial_query = f"""
    [out:json];
    (
      way["landuse"="industrial"]({bbox});
      relation["landuse"="industrial"]({bbox});
      way["industrial"]({bbox});
      way["man_made"="factory"]({bbox});
    );
    out count;
    """
    result = query_overpass(industrial_query)
    if result and 'elements' in result:
        features['industrial_count'] = len(result['elements'])
        features['has_industrial'] = 1 if features['industrial_count'] > 0 else 0
    
    # 3. Get farmland/agricultural areas
    print(f"    Querying farmland...")
    farmland_query = f"""
    [out:json];
    (
      way["landuse"~"farmland|farm|agricultural|orchard|meadow|vineyard"]({bbox});
      relation["landuse"~"farmland|farm|agricultural|orchard|meadow|vineyard"]({bbox});
    );
    out count;
    """
    result = query_overpass(farmland_query)
    if result and 'elements' in result:
        features['farmland_count'] = len(result['elements'])
        features['has_farmland'] = 1 if features['farmland_count'] > 0 else 0
    
    # 4. Get dump/waste sites
    print(f"    Querying dump sites...")
    dump_query = f"""
    [out:json];
    (
      way["landuse"="landfill"]({bbox});
      way["amenity"="waste_disposal"]({bbox});
      way["amenity"="dump"]({bbox});
      node["amenity"="waste_disposal"]({bbox});
      node["amenity"="dump"]({bbox});
      way["man_made"="wastewater_plant"]({bbox});
    );
    out count;
    """
    result = query_overpass(dump_query)
    if result and 'elements' in result:
        features['dump_sites_count'] = len(result['elements'])
        features['has_dump'] = 1 if features['dump_sites_count'] > 0 else 0
    
    # 5. Get power plants
    print(f"    Querying power plants...")
    power_query = f"""
    [out:json];
    (
      way["power"="plant"]({bbox});
      way["power"="generator"]({bbox});
      relation["power"="plant"]({bbox});
      way["power"="substation"]({bbox});
    );
    out count;
    """
    result = query_overpass(power_query)
    if result and 'elements' in result:
        features['power_plants_count'] = len(result['elements'])
        features['has_power_plant'] = 1 if features['power_plants_count'] > 0 else 0
    
    # 6. Get bus stops
    print(f"    Querying bus stops...")
    bus_query = f"""
    [out:json];
    (
      node["highway"="bus_stop"]({bbox});
      node["amenity"="bus_station"]({bbox});
      way["amenity"="bus_station"]({bbox});
    );
    out count;
    """
    result = query_overpass(bus_query)
    if result and 'elements' in result:
        features['bus_stops_count'] = len(result['elements'])
    
    # 7. Get railway stations
    print(f"    Querying railway stations...")
    railway_query = f"""
    [out:json];
    (
      node["railway"="station"]({bbox});
      node["railway"="halt"]({bbox});
      way["railway"="station"]({bbox});
    );
    out count;
    """
    result = query_overpass(railway_query)
    if result and 'elements' in result:
        features['railway_stations_count'] = len(result['elements'])
    
    # 8. Get parking lots
    print(f"    Querying parking lots...")
    parking_query = f"""
    [out:json];
    (
      node["amenity"="parking"]({bbox});
      way["amenity"="parking"]({bbox});
    );
    out count;
    """
    result = query_overpass(parking_query)
    if result and 'elements' in result:
        features['parking_lots_count'] = len(result['elements'])
    
    return features

# Collect features for all areas
all_features = []
successful = []
failed = []
area_status = []

print("\nCollecting location features for each area...")
print("-" * 70)

for idx, row in cities_df.iterrows():
    city = row['city']
    area = row['area']
    state = row['state']
    
    print(f"\n[{idx+1}/{len(cities_df)}] {city} - {area}...")
    
    # Get coordinates for this specific area
    lat, lon, query = get_area_coordinates(city, area, state)
    
    if lat is None or lon is None:
        print(f"  ✗ Could not get coordinates for: {query}")
        failed.append(f"{city}-{area}")
        area_status.append({
            'city': city,
            'area': area,
            'status': 'NO_COORDINATES'
        })
        continue
    
    print(f"  ✓ Coordinates: {lat:.4f}, {lon:.4f}")
    
    # Get location features
    features = get_location_features(city, area, state, lat, lon)
    
    if features:
        all_features.append(features)
        successful.append(f"{city}-{area}")
        
        # Show summary
        print(f"  ✓ Results:")
        print(f"    Roads: {features['road_segments']} segments ({features['road_km']} km)")
        print(f"    Industrial: {features['industrial_count']}")
        print(f"    Farmland: {features['farmland_count']}")
        print(f"    Dump sites: {features['dump_sites_count']}")
        print(f"    Power plants: {features['power_plants_count']}")
        print(f"    Bus stops: {features['bus_stops_count']}")
        
        area_status.append({
            'city': city,
            'area': area,
            'status': 'SUCCESS',
            'industrial': features['industrial_count'],
            'farmland': features['farmland_count'],
            'dumps': features['dump_sites_count']
        })
    else:
        failed.append(f"{city}-{area}")
        area_status.append({
            'city': city,
            'area': area,
            'status': 'FAILED'
        })
        print(f"  ✗ Failed to get features")
    
    # Rate limiting - be nice to the API
    time.sleep(2)

# Save results
if all_features:
    df = pd.DataFrame(all_features)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = output_dir / f"location_features_areas_{timestamp}.csv"
    df.to_csv(filename, index=False)
    
    # Save status report
    status_df = pd.DataFrame(area_status)
    status_file = output_dir / f"location_status_{timestamp}.csv"
    status_df.to_csv(status_file, index=False)
    
    print("\n" + "="*70)
    print("COLLECTION COMPLETE")
    print("="*70)
    print(f"Successful areas: {len(successful)}")
    print(f"Failed areas: {len(failed)}")
    print(f"\n📁 Files saved:")
    print(f"  - {filename}")
    print(f"  - {status_file}")
    
    # Show statistics by city
    print("\n📊 SUMMARY BY CITY:")
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        print(f"\n  {city}:")
        print(f"    Areas: {len(city_data)}")
        print(f"    Avg Road Segments: {city_data['road_segments'].mean():.0f}")
        print(f"    Total Industrial: {city_data['industrial_count'].sum()}")
        print(f"    Total Farmland: {city_data['farmland_count'].sum()}")
        print(f"    Total Dump Sites: {city_data['dump_sites_count'].sum()}")
    
    # Show areas with industrial activity
    print("\n🏭 AREAS WITH INDUSTRIAL ACTIVITY:")
    industrial_areas = df[df['industrial_count'] > 0]
    if not industrial_areas.empty:
        for _, row in industrial_areas.iterrows():
            print(f"  {row['city']} - {row['area']}: {row['industrial_count']} sites")
    
    # Show areas with farmland
    print("\n🌾 AREAS WITH FARMLAND:")
    farmland_areas = df[df['farmland_count'] > 0]
    if not farmland_areas.empty:
        for _, row in farmland_areas.iterrows():
            print(f"  {row['city']} - {row['area']}: {row['farmland_count']} areas")
    
    # Show areas with dump sites
    print("\n🗑️ AREAS WITH DUMP SITES:")
    dump_areas = df[df['dump_sites_count'] > 0]
    if not dump_areas.empty:
        for _, row in dump_areas.iterrows():
            print(f"  {row['city']} - {row['area']}: {row['dump_sites_count']} sites")
    
    # Sample data
    print("\n📋 SAMPLE DATA (first 10 areas):")
    display_cols = ['city', 'area', 'road_segments', 'industrial_count', 
                    'farmland_count', 'dump_sites_count', 'bus_stops_count']
    print(df[display_cols].head(10).to_string())
    
else:
    print("\nNo data collected")