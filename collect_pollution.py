
import pandas as pd

df = pd.read_csv("dataset.csv")

print("Dataset Loaded Successfully")
print("Total Records:", len(df))
print("Columns:", df.columns.tolist())

required_pollutants = ["pm25", "pm10", "no2", "co", "so2", "o3"]

# Detect correct column automatically
if "pollutant_id" in df.columns:
    pollutant_column = "pollutant_id"
elif "pollutant" in df.columns:
    pollutant_column = "pollutant"
else:
    raise Exception("No pollutant column found!")

df_filtered = df[df[pollutant_column].str.lower().isin(required_pollutants)]

print("Filtered Records:", len(df_filtered))

print("\nPreview:")
print(df_filtered)

df_filtered.to_csv("india_air_pollution_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully ")
print("Project Completed ")



