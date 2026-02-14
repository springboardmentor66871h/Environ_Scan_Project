import pandas as pd
import osmnx as ox
from shapely.geometry import Point
import geopandas as gpd

pollution_df = pd.read_csv("../data/raw/pollution/pollution_data.csv")
unique_locations = pollution_df[["latitude", "longitude"]].drop_duplicates()

location_features = []

for _, row in unique_locations.iterrows():
    lat = row["latitude"]
    lon = row["longitude"]

    print(f"Processing location: {lat}, {lon}")

    point = Point(lon, lat)
    point_gdf = gpd.GeoSeries([point], crs="EPSG:4326").to_crs(epsg=3857)

    # ---------------- ROAD ----------------
    try:
        G = ox.graph_from_point((lat, lon), dist=2000, network_type="drive")
        roads = ox.graph_to_gdfs(G, nodes=False)
        roads_gdf = gpd.GeoDataFrame(roads).to_crs(epsg=3857)
        roads_gdf["distance"] = roads_gdf.geometry.distance(point_gdf.iloc[0])
        min_road_distance = roads_gdf["distance"].min()
    except Exception as e:
        print("Road extraction failed:", e)
        min_road_distance = 10000

    # ---------------- INDUSTRIAL ----------------
    try:
        industrial_tags = {"landuse": "industrial"}
        industrial = ox.features_from_point((lat, lon), tags=industrial_tags, dist=5000)

        if not industrial.empty:
            industrial = industrial.to_crs(epsg=3857)
            industrial["distance"] = industrial.geometry.distance(point_gdf.iloc[0])
            min_industrial_distance = industrial["distance"].min()
        else:
            min_industrial_distance = 10000
    except Exception as e:
        print("Industrial extraction failed:", e)
        min_industrial_distance = 10000

    # ---------------- LANDFILL ----------------
    try:
        landfill_tags = {"amenity": "landfill"}
        landfill = ox.features_from_point((lat, lon), tags=landfill_tags, dist=5000)

        if not landfill.empty:
            landfill = landfill.to_crs(epsg=3857)
            landfill["distance"] = landfill.geometry.distance(point_gdf.iloc[0])
            min_landfill_distance = landfill["distance"].min()
        else:
            min_landfill_distance = 10000
    except Exception as e:
        print("Landfill extraction failed:", e)
        min_landfill_distance = 10000

    # ---------------- FARMLAND ----------------
    try:
        farmland_tags = {"landuse": "farmland"}
        farmland = ox.features_from_point((lat, lon), tags=farmland_tags, dist=5000)

        if not farmland.empty:
            farmland = farmland.to_crs(epsg=3857)
            farmland["distance"] = farmland.geometry.distance(point_gdf.iloc[0])
            min_farmland_distance = farmland["distance"].min()
        else:
            min_farmland_distance = 10000
    except Exception as e:
        print("Farmland extraction failed:", e)
        min_farmland_distance = 10000

    # Always append row (even if some values are None)
    location_features.append({
        "latitude": lat,
        "longitude": lon,
        "distance_to_nearest_road_meters": min_road_distance,
        "distance_to_nearest_industrial_meters": min_industrial_distance,
        "distance_to_nearest_landfill_meters": min_landfill_distance,
        "distance_to_nearest_farmland_meters": min_farmland_distance
    })

df = pd.DataFrame(location_features)

if not df.empty:
    df.to_csv("../data/raw/location_features/location_features.csv", index=False)
    print("All Location Features Saved Successfully")
else:
    print("No data extracted.")
