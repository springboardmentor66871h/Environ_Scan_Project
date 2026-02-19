import pandas as pd
import osmnx as ox
from geopy.distance import geodesic

# ----------------------------
# Load Pollution Dataset
# ----------------------------
pollution = pd.read_csv("data/raw/pollution_data.csv")
print(pollution["city"].unique())
# exit()
# print("Pollution columns:")
# print(pollution.columns)
# exit()

# Rename columns if needed (adjust if yours are different)
pollution.rename(columns={
    "city": "city",
    "lat": "latitude",
    "lon": "longitude"
}, inplace=True)

# Get unique locations
locations = pollution[["city", "latitude", "longitude"]].drop_duplicates()
# Select only few cities (FAST)
selected_cities = [
    "Amaravati",
    "Bhopal",
    "Indore",
    "Chittoor",
    "Guntur",
    
]

locations = locations[locations["city"].isin(selected_cities)]

# ----------------------------
# Function to calculate distance
# ----------------------------
def get_nearest_distance(lat, lon, tags):

    point = (lat, lon)

    try:
        gdf = ox.features_from_point(point, tags=tags, dist=3000)

        if gdf.empty:
            return None

        # gdf["center"] = gdf.geometry.centroid
        # Convert to projected CRS
        gdf_proj = gdf.to_crs(epsg=3857)

# Calculate centroid safely
        gdf_proj["center"] = gdf_proj.geometry.centroid

# Convert back to lat lon
        gdf["center"] = gdf_proj["center"].to_crs(epsg=4326)

        distances = [
            geodesic(point, (geom.y, geom.x)).km
            for geom in gdf["center"]
        ]

        return min(distances)

    except Exception as e:
      print("OSM Error:", e)
      return None


# ----------------------------
# OSM Feature Tags
# ----------------------------
road_tags = {"highway": True}
industry_tags = {"landuse": "industrial"}
dump_tags = {"amenity": "waste_disposal"}
farm_tags = {"landuse": "farmland"}


# ----------------------------
# Extract Features
# ----------------------------
results = []

for _, row in locations.iterrows():

    city = row["city"]
    lat = row["latitude"]
    lon = row["longitude"]

    print("Processing:", city)

    road_dist = get_nearest_distance(lat, lon, road_tags)
    industry_dist = get_nearest_distance(lat, lon, industry_tags)
    dump_dist = get_nearest_distance(lat, lon, dump_tags)
    farm_dist = get_nearest_distance(lat, lon, farm_tags)

    results.append({
        "City": city,
        "Latitude": lat,
        "Longitude": lon,
        "Nearest_Road_km": road_dist,
        "Nearest_Industry_km": industry_dist,
        "Nearest_Dump_km": dump_dist,
        "Nearest_Farm_km": farm_dist
    })


# ----------------------------
# Save File
# ----------------------------
location_features = pd.DataFrame(results)

location_features.to_csv(
    "data/raw/location_features.csv",
    index=False
)

print("Location feature extraction complete!")
location_features.to_csv("data/raw/location_features.csv", index=False)
print("Location features saved successfully!")
