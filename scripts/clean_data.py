import pandas as pd

# Load dataset
df = pd.read_csv("data/station_day.csv")

# Select required columns
required_columns = [
    "StationId",
    "Date",
    "PM2.5",
    "PM10",
    "NO2",
    "CO",
    "SO2",
    "O3"
]

df = df[required_columns]

# Remove rows with missing values
df = df.dropna()

# Keep only first 10000 rows
df = df.head(10000)

print("Final Shape:", df.shape)
print(df.head())

# Save cleaned dataset
df.to_csv("data/india_pollution_cleaned_10000.csv", index=False)

print("Saved successfully!")
