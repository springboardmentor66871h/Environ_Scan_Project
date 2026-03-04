import pandas as pd

# -----------------------------
# Load Raw Datasets
# -----------------------------
pollution_df = pd.read_csv("C:/projects/AI_Price_Optima/data/raw/india_air_pollution_cleaned.csv")
weather_df = pd.read_csv("C:/projects/AI_Price_Optima/data/raw/india_weather_dataset_new.csv")
location_df = pd.read_csv("C:/projects/AI_Price_Optima/data/raw/location.csv")

print("Datasets Loaded Successfully")

# -----------------------------
# Merge pollution + location
# -----------------------------
merged_df = pd.merge(
    pollution_df,
    location_df[
        [
            "city",
            "latitude",
            "longitude",
            "distance_to_road_m",
            "distance_to_industry_m",
            "distance_to_farmland_m",
            "distance_to_dump_m"
        ]
    ],
    on=["city", "latitude", "longitude"],
    how="left"
)

print("Pollution + Location merged")

# -----------------------------
# Merge weather
# -----------------------------
final_df = pd.merge(
    merged_df,
    weather_df,
    on=["city", "latitude", "longitude"],
    how="left"
)

print("Weather merged")

# -----------------------------
# Pollution Source Classification
# -----------------------------
def classify_source(row):
    pollutant = str(row["pollutant_id"]).lower()

    if pollutant in ["no2", "co"]:
        return "Vehicular"
    elif pollutant in ["so2"]:
        return "Industrial"
    elif pollutant in ["pm10", "pm2.5"]:
        return "Burning"
    elif pollutant in ["o3"]:
        return "Natural"
    else:
        return "Mixed"

# Apply classification
final_df["pollution_source"] = final_df.apply(classify_source, axis=1)

print("Pollution source classified")

# -----------------------------
# Save Final CSV
# -----------------------------
final_df.to_csv("final_environment_dataset.csv", index=False)

print("FINAL DATASET CREATED")
print("Total Rows:", len(final_df))
print("Columns:", final_df.columns.tolist())