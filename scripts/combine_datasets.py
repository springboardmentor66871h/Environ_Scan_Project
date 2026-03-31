import pandas as pd



pollution_df = pd.read_csv("data/raw/india_air_pollution_cleaned.csv")
weather_df = pd.read_csv("data/raw/india_weather_dataset_new.csv")
location_df = pd.read_csv("data/raw/location.csv")

print("Datasets Loaded Successfully")

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

final_df = pd.merge(
    merged_df,
    weather_df,
    on=["city", "latitude", "longitude"],
    how="left"
)

print("Weather merged")


final_df.to_csv("final_environment_dataset.csv", index=False)

print("FINAL DATASET CREATED")
print("Total Rows:", len(final_df))
print("Columns:", final_df.columns.tolist())
