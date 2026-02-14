import pandas as pd

# Load datasets
pollution_df = pd.read_csv("../data/raw/pollution/pollution_data.csv")
weather_df = pd.read_csv("../data/raw/weather/weather_data.csv")
location_df = pd.read_csv("../data/raw/location_features/location_features.csv")

# -----------------------------
# Step 1: Convert timestamps properly
# -----------------------------
pollution_df["timestamp"] = pd.to_datetime(pollution_df["timestamp"])
weather_df["timestamp"] = pd.to_datetime(weather_df["timestamp"])

# -----------------------------
# Step 2: Round latitude & longitude (avoid float mismatch)
# -----------------------------
pollution_df["latitude"] = pollution_df["latitude"].round(4)
pollution_df["longitude"] = pollution_df["longitude"].round(4)

weather_df["latitude"] = weather_df["latitude"].round(4)
weather_df["longitude"] = weather_df["longitude"].round(4)

location_df["latitude"] = location_df["latitude"].round(4)
location_df["longitude"] = location_df["longitude"].round(4)

# -----------------------------
# Step 3: Merge pollution + weather (LEFT JOIN instead of INNER)
# -----------------------------
merged_df = pd.merge(
    pollution_df,
    weather_df,
    on=["city"],   # safer to merge only on city
    how="left",
    suffixes=("", "_weather")
)

print("Pollution rows:", pollution_df.shape)
print("Weather rows:", weather_df.shape)
print("After first merge:", merged_df.shape)

# -----------------------------
# Step 4: Merge with location features
# -----------------------------
final_df = pd.merge(
    merged_df,
    location_df,
    on=["latitude", "longitude"],
    how="left"
)

print("Final rows:", final_df.shape)
# -----------------------------
# Step 5: Fill Missing Values
# -----------------------------

# Fill pollutant columns with 0
pollutant_cols = ["pm25", "pm10", "no2", "co", "so2", "o3"]

for col in pollutant_cols:
    if col in final_df.columns:
        final_df[col] = final_df[col].fillna(0)

# Fill numeric columns with mean
numeric_cols = final_df.select_dtypes(include=["float64", "int64"]).columns
final_df[numeric_cols] = final_df[numeric_cols].fillna(final_df[numeric_cols].mean())

print("Remaining Null Values:")
print(final_df.isnull().sum())

# -----------------------------
# Step 5: Save dataset
# -----------------------------
final_df.to_csv("../data/processed/final_dataset.csv", index=False)

print("Final Dataset Created Successfully")
