import os
import pandas as pd
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point


def merge_and_clean():

    # =============================
    # Project Root Path
    # =============================
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pollution_path = os.path.join(base_dir, "data", "raw", "pollution_data.csv")
    weather_path = os.path.join(base_dir, "data", "raw", "weather_data.csv")
    output_path = os.path.join(base_dir, "data", "processed", "cleaned_data.csv")

    print("Loading datasets...")

    pollution = pd.read_csv(pollution_path)
    weather = pd.read_csv(weather_path)

    # =============================
    # Timestamp Alignment
    # =============================
    print("Aligning timestamps...")

    pollution = pollution.rename(columns={"last_updated_utc": "datetime"})
    weather = weather.rename(columns={"timestamp": "datetime"})

    pollution["datetime"] = pd.to_datetime(pollution["datetime"], errors="coerce")
    weather["datetime"] = pd.to_datetime(weather["datetime"], errors="coerce")

    # Remove timezone if exists
    if pollution["datetime"].dt.tz is not None:
        pollution["datetime"] = pollution["datetime"].dt.tz_convert(None)

    if weather["datetime"].dt.tz is not None:
        weather["datetime"] = weather["datetime"].dt.tz_convert(None)

    df = pd.merge(pollution, weather, on="datetime", how="inner")

    df = df.drop_duplicates()

    # =============================
    # Timestamp Features
    # =============================
    print("Extracting time features...")

    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day
    df["month"] = df["datetime"].dt.month
    df["weekday"] = df["datetime"].dt.weekday

    # =============================
    # Spatial Feature
    # Distance to Nearest Road
    # =============================
    print("Calculating spatial distance to nearest road...")

    # Detect correct latitude/longitude columns
    lat_col = None
    lon_col = None

    for col in df.columns:
        if "lat" in col.lower():
            lat_col = col
        if "lon" in col.lower() or "long" in col.lower():
            lon_col = col

    if lat_col and lon_col:

        place = "Chennai, India"

        G = ox.graph_from_place(place, network_type="drive")
        roads = ox.graph_to_gdfs(G, nodes=False, edges=True)

        roads = roads.to_crs(epsg=3857)

        distances = []

        for _, row in df.iterrows():

            if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):

                point = Point(row[lon_col], row[lat_col])
                point_gdf = gpd.GeoSeries([point], crs="EPSG:4326").to_crs(epsg=3857)

                dist = roads.geometry.distance(point_gdf.iloc[0]).min()
                distances.append(dist)

            else:
                distances.append(None)

        df["Distance_to_Nearest_Road"] = distances

        print("Spatial feature added ✅")

    else:
        print("No latitude/longitude columns detected — skipping spatial feature")

    # =============================
    # Save Processed File
    # =============================
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    print("✅ Merge + Cleaning + Feature Engineering Completed Successfully!")


if __name__ == "__main__":
    merge_and_clean()