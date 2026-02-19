import os
import pandas as pd

BASE_PATH = r"D:\ENVIRON-SCAN"
RAW_PATH = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "data", "processed")

os.makedirs(PROCESSED_PATH, exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

pollution = pd.read_csv(os.path.join(RAW_PATH, "pollution.csv"))
weather = pd.read_csv(os.path.join(RAW_PATH, "weather.csv"))
location = pd.read_csv(os.path.join(RAW_PATH, "location_features.csv"))

# ==========================================
# STANDARDIZE TIMESTAMP
# ==========================================

pollution["timestamp"] = pd.to_datetime(pollution["timestamp"])
weather["timestamp"] = pd.to_datetime(weather["timestamp"])

# ==========================================
# MERGE POLLUTION + WEATHER
# ==========================================

merged = pd.merge(
    pollution,
    weather,
    on=["city", "timestamp"],
    how="inner",
    suffixes=("_poll", "_weather")
)

print("After pollution + weather merge:", len(merged))

# ==========================================
# CLEAN DUPLICATE LAT/LON FROM WEATHER
# ==========================================

merged["latitude"] = merged["latitude_poll"]
merged["longitude"] = merged["longitude_poll"]

merged.drop(columns=[
    "latitude_poll",
    "longitude_poll",
    "latitude_weather",
    "longitude_weather"
], inplace=True)

# ==========================================
# ASSIGN SPATIAL PROFILE PER CITY
# ==========================================

final_list = []

for city in merged["city"].unique():

    city_data = merged[merged["city"] == city].copy()
    city_locations = location[location["city"] == city].reset_index(drop=True)

    if len(city_locations) == 0:
        print(f"No spatial data for {city}")
        continue

    # Repeat spatial rows cyclically
    city_data = city_data.reset_index(drop=True)

    spatial_indices = city_data.index % len(city_locations)
    spatial_data = city_locations.loc[spatial_indices].reset_index(drop=True)

    city_data["distance_to_road"] = spatial_data["distance_to_road"]
    city_data["distance_to_industry"] = spatial_data["distance_to_industry"]
    city_data["distance_to_dump"] = spatial_data["distance_to_dump"]
    city_data["distance_to_farmland"] = spatial_data["distance_to_farmland"]

    final_list.append(city_data)

final_df = pd.concat(final_list, ignore_index=True)

print("Final merged rows:", len(final_df))

# ==========================================
# FINAL COLUMN ORDER
# ==========================================

final_columns = [
    "timestamp", "city",
    "latitude", "longitude",
    "pm25", "pm10", "co", "no2", "so2", "o3",
    "temperature", "humidity",
    "wind_speed", "wind_direction",
    "distance_to_road",
    "distance_to_industry",
    "distance_to_dump",
    "distance_to_farmland"
]

final_df = final_df[final_columns]

# ==========================================
# SAVE FINAL DATASET
# ==========================================

file_path = os.path.join(PROCESSED_PATH, "final_dataset.csv")
final_df.to_csv(file_path, index=False)

print("\nFinal dataset saved successfully.")
print("Location:", file_path)
print("Total rows:", len(final_df))
