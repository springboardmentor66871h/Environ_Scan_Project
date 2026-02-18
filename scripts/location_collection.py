import os
import shutil
import requests
import pandas as pd
from time import sleep
from math import radians, sin, cos, sqrt, atan2

# ----------------------------
# Settings
# ----------------------------
CSV_FILE = "pollution_with_osm_feature.csv"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
MAX_RADIUS = 20000      # Fallback distance (20 km)
SLEEP_BETWEEN_QUERIES = 1

# ----------------------------
# Haversine formula
# ----------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius (meters)
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ----------------------------
# Query nearest feature distance
# ----------------------------
def nearest_distance(lat, lon, tag_query):
    """
    Query Overpass for nearest feature matching tag_query near (lat,lon).
    Returns the minimum distance found, or MAX_RADIUS if none.
    """
    query = f"""
    [out:json][timeout:25];
    (
      node[{tag_query}](around:{MAX_RADIUS},{lat},{lon});
      way[{tag_query}](around:{MAX_RADIUS},{lat},{lon});
      relation[{tag_query}](around:{MAX_RADIUS},{lat},{lon});
    );
    out center 1;
    """
    try:
        response = requests.get(OVERPASS_URL, params={"data": query}, timeout=60)
        data = response.json().get("elements", [])
    except Exception as e:
        print(f"  ! Overpass query error for {tag_query}: {e}")
        data = []
    if not data:
        return MAX_RADIUS
    # Compute minimum distance from results
    min_d = MAX_RADIUS
    for el in data:
        if "center" in el: 
            el_lat, el_lon = el["center"]["lat"], el["center"]["lon"]
        elif "lat" in el and "lon" in el:
            el_lat, el_lon = el["lat"], el["lon"]
        else:
            continue
        d = haversine_distance(lat, lon, el_lat, el_lon)
        if d < min_d:
            min_d = d
    return min_d

# ----------------------------
# Main processing
# ----------------------------
def main():
    if not os.path.exists(CSV_FILE):
        print(f"❌ File not found: {CSV_FILE}")
        return
    # Backup
    backup = CSV_FILE + ".bak"
    if not os.path.exists(backup):
        shutil.copyfile(CSV_FILE, backup)
    # Load CSV
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded {len(df)} rows from {CSV_FILE}")

    # Ensure all distance columns exist
    for col in ["dist_road", "dist_industry", "dist_dump", "dist_farmland"]:
        if col not in df.columns:
            df[col] = None

    # Define tag queries for each category
    tag_queries = {
        "dist_road": "highway",           # any road/path【39†L185-L189】
        "dist_industry": "landuse=industrial",  # industrial areas【35†L163-L169】
        "dist_dump": "landuse=landfill|amenity=waste_transfer_station|amenity=recycling",  # dump/recycling
        "dist_farmland": "landuse=farmland"     # farmland【37†L168-L171】
    }

    # Fill missing values per category
    for col, tag in tag_queries.items():
        mask = df[col].isna() | (df[col] == "")  # NA or blank【32†L406-L412】
        missing_rows = df[mask]
        if missing_rows.empty:
            continue
        print(f"\nUpdating {col} for {len(missing_rows)} rows...")
        for idx, row in missing_rows.iterrows():
            city, lat, lon = row["city"], row["latitude"], row["longitude"]
            print(f" {col}: {city} ({idx+1}/{len(missing_rows)})")
            dist = nearest_distance(lat, lon, tag)
            df.at[idx, col] = dist
            sleep(SLEEP_BETWEEN_QUERIES)

    # Final fill for any leftover NA
    df.fillna(MAX_RADIUS, inplace=True)

    # Save CSV with UTF-8 BOM (Excel-friendly)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    print(f"\n✅ All distances updated and saved to {CSV_FILE}")

if __name__ == "__main__":
    main()
