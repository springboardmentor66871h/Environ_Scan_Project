import pandas as pd

print("Loading datasets...")

# -----------------------------
# Load RAW datasets
# -----------------------------
pollution = pd.read_csv("data/raw/pollution_data.csv")

weather = pd.read_csv("data/raw/weather_data.csv")

location = pd.read_csv("data/raw/location_features.csv")


# -----------------------------
# CHECK Columns (Debug)
# -----------------------------
print("\nPollution Columns:", pollution.columns)
print("Weather Columns:", weather.columns)
print("Location Columns:", location.columns)


# -----------------------------
# Rename Columns Properly
# -----------------------------
pollution.rename(columns={
    "city":"City",
    "latitude":"Latitude",
    "longitude":"Longitude"
}, inplace=True)


weather.rename(columns={
    "location_name":"City",
    "latitude":"Latitude",
    "longitude":"Longitude"
}, inplace=True)


# -----------------------------
# Merge Pollution + Weather
# -----------------------------
print("\nMerging pollution + weather...")

merged = pd.merge(
    pollution,
    weather,
    on=["City","Latitude","Longitude"],   # safer merge
    how="left"
)


# -----------------------------
# Merge Location Features
# -----------------------------
print("Adding location features...")

final_dataset = pd.merge(
    merged,
    location,
    on=["City","Latitude","Longitude"],
    how="left"
)


# -----------------------------
# Save Final Dataset
# -----------------------------
output_path = "data/processed/final_dataset.csv"

final_dataset.to_csv(
    output_path,
    index=False
)

print("\nFinal dataset created successfully!")
print("Saved at:", output_path)