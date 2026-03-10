import pandas as pd
import os

print("Loading datasets...")
pollution_df = pd.read_csv("data/raw/india_air_pollution_cleaned.csv")
weather_df = pd.read_csv("data/raw/india_weather_dataset_new.csv")
location_df = pd.read_csv("data/raw/location.csv")

print("Merging Pollution and Location data...")
# Merge pollution and location based on the city and coordinates
merged_df = pd.merge(pollution_df, location_df, on=["city", "latitude", "longitude"], how="left")

print("Merging Weather data...")
# Merge with weather data
final_df = pd.merge(merged_df, weather_df, on=["city", "latitude", "longitude"], how="left")

print("Extracting Temporal Features (Hour, Month, Day of Week)...")
# Convert timestamp to a format Python understands, then extract specific time features
final_df['last_updated'] = pd.to_datetime(final_df['last_updated'])
final_df['hour'] = final_df['last_updated'].dt.hour
final_df['month'] = final_df['last_updated'].dt.month
final_df['day_of_week'] = final_df['last_updated'].dt.dayofweek

print("Cleaning up missing values...")
# If any map features failed to download, default them to 5000 meters (far away)
distance_cols = ['distance_to_road_m', 'distance_to_industry_m', 'distance_to_farmland_m', 'distance_to_dump_m']
final_df[distance_cols] = final_df[distance_cols].fillna(5000.0)

# If any weather data is missing, fill it with the median value so the ML model doesn't crash
weather_cols = ['temperature', 'humidity', 'wind_speed', 'wind_direction']
for col in weather_cols:
    final_df[col] = final_df[col].fillna(final_df[col].median())

# Create the final processed folder
os.makedirs("data/processed", exist_ok=True)

# Save the final masterpiece
output_path = "data/processed/final_environment_dataset.csv"
final_df.to_csv(output_path, index=False)

print(f"\nSUCCESS: Unified dataset created with {len(final_df)} rows and {len(final_df.columns)} columns!")
print(f"Saved to: {output_path}")
print("Module 2 (Data Cleaning and Feature Engineering) is 100% COMPLETE!")