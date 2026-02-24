import pandas as pd

pollution = pd.read_csv("data/raw/pollution_data.csv")
weather = pd.read_csv("data/raw/weather_data.csv")
location = pd.read_csv("data/raw/location_features.csv")

# Merge pollution + weather
merged = pd.merge(
    pollution,
    weather,
    on=["city", "latitude", "longitude", "timestamp"],
    how="inner"
)

# Merge location features
final = pd.merge(
    merged,
    location,
    on=["city", "latitude", "longitude"],
    how="left"
)

final.to_csv("data/processed/final_dataset.csv", index=False)

print("Final dataset created successfully.")