import pandas as pd

pollution = pd.read_csv(r"C:\Users\admin\Environ_Scan_Project\pollution.csv")
weather = pd.read_csv(r"C:\Users\admin\Environ_Scan_Project\weather.csv")
location = pd.read_csv(r"C:\Users\admin\Environ_Scan_Project\location_features.csv")

for df in [pollution, weather, location]:
    df["city"] = df["city"].str.lower().str.strip()

for df in [pollution, weather, location]:
    df["latitude"] = df["latitude"].round(4)
    df["longitude"] = df["longitude"].round(4)

pollution["timestamp"] = pd.to_datetime(pollution["timestamp"])
weather["timestamp"] = pd.to_datetime(weather["timestamp"])

pollution_wide = pollution.pivot_table(
    index=["city", "latitude", "longitude", "timestamp"],
    columns="pollutant",
    values="value"
).reset_index()

pollution_wide.columns.name = None

print("Pollution wide shape:", pollution_wide.shape)

merged = pd.merge(
    pollution_wide,
    weather,
    on=["city", "latitude", "longitude", "timestamp"],
    how="inner"
)

print("After merging weather:", merged.shape)

final_dataset = pd.merge(
    merged,
    location,
    on=["city", "latitude", "longitude"],
    how="left"
)

print("After merging location features:", final_dataset.shape)
print("\nMissing values summary:")
print(final_dataset.isnull().sum())
print("\nDuplicate rows:", final_dataset.duplicated().sum())

numeric_cols = final_dataset.select_dtypes(include=["float64", "int64"]).columns
final_dataset[numeric_cols] = final_dataset[numeric_cols].fillna(
    final_dataset[numeric_cols].mean()
)

final_dataset = final_dataset.sort_values("timestamp")
final_dataset.to_csv(r"C:\Users\admin\Environ_Scan_Project\combined_dataset.csv", index=False)

print("\n Data Integration Completed Successfully!")
print("Final dataset shape:", final_dataset.shape)
print("Total columns:", len(final_dataset.columns))
