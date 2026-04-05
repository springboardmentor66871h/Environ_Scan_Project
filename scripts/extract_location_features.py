import pandas as pd
import geopandas as gpd
import osmnx as ox
import numpy as np


df = pd.read_csv("india_air_pollution_cleaned.csv")
df.columns = df.columns.str.lower()
df = df.dropna(subset=["latitude", "longitude"])
df = df.head(1000)

print(f" Using {len(df)} rows")

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs="EPSG:4326"
)


center_lat = gdf.latitude.mean()
center_lon = gdf.longitude.mean()

bbox = ox.utils_geo.bbox_from_point(
    (center_lat, center_lon),
    dist=20000   # 20 km radius
)


def safe_download(tags):
    try:
        data = ox.features_from_bbox(bbox=bbox, tags=tags)
        print(f" Downloaded {len(data)} features for {tags}")
        return data
    except Exception as e:
        print(f" Error downloading {tags}: {e}")
        return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

print(" Downloading OSM features...")

# Broader tags for better coverage
roads = safe_download({"highway": True})

industrial = safe_download({
    "landuse": ["industrial", "commercial"]
})

farmland = safe_download({
    "landuse": ["farmland", "meadow", "farm"]
})

dumps = safe_download({
    "landuse": ["landfill", "waste_transfer_station"]
})

gdf = gdf.to_crs(epsg=3857)
roads = roads.to_crs(epsg=3857)
industrial = industrial.to_crs(epsg=3857)
farmland = farmland.to_crs(epsg=3857)
dumps = dumps.to_crs(epsg=3857)

def compute_distance(points, target, col_name):
    if not target.empty:
        join = gpd.sjoin_nearest(
            points,
            target,
            how="left",
            distance_col=col_name
        )
        return join[col_name]
    else:
        print(f" No data found for {col_name}, assigning 20000m")
        return pd.Series(20000, index=points.index)

print(" Calculating distances...")

gdf["distance_to_road_m"] = compute_distance(gdf, roads, "distance_to_road_m")
gdf["distance_to_industry_m"] = compute_distance(gdf, industrial, "distance_to_industry_m")
gdf["distance_to_farmland_m"] = compute_distance(gdf, farmland, "distance_to_farmland_m")
gdf["distance_to_dump_m"] = compute_distance(gdf, dumps, "distance_to_dump_m")

gdf.drop(columns="geometry").to_csv(
    "location.csv",
    index=False
)

print(" DONE! File saved as location.csv")








