import pandas as pd
import os
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from time import sleep

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/processed/final_environment_dataset.csv")

print("Original Shape:", df.shape)

extra_cols = df[[
    "latitude", "longitude", "timestamp",
    "distance_to_road_m",
    "distance_to_industry_m",
    "distance_to_farmland_m",
    "distance_to_dump_m",
    "temperature", "humidity", "wind_speed"
]].drop_duplicates()

df_pivot = df.pivot_table(
    index=["latitude", "longitude", "timestamp"],
    columns="pollutant_id",
    values="pollutant_avg"
).reset_index()

df_pivot.columns.name = None

df = pd.merge(
    df_pivot,
    extra_cols,
    on=["latitude", "longitude", "timestamp"],
    how="left"
)

print("After Pivot Shape:", df.shape)

df = df.fillna(0)

# -------------------------------
# Reverse Geocoding (City Mapping)
# -------------------------------
geolocator = Nominatim(user_agent="enviro_app")

def get_city(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        address = location.raw.get("address", {})
        return address.get("city") or address.get("town") or address.get("state") or "Unknown"
    except:
        return "Unknown"

cities = []

for i, row in df.iterrows():
    city = get_city(row["latitude"], row["longitude"])
    cities.append(city)

    if i % 50 == 0:
        print(f"Processed {i} rows...")
        sleep(1)

df["location"] = cities

# -------------------------------
# Labeling Logic (4 classes)
# -------------------------------
def assign_source(row):

    no2 = row.get("NO2", 0)
    so2 = row.get("SO2", 0)
    pm10 = row.get("PM10", 0)

    road = row.get("distance_to_road_m", 999999)
    industry = row.get("distance_to_industry_m", 999999)
    dump = row.get("distance_to_dump_m", 999999)

    if no2 > 30 and road < 3000:
        return "Vehicular"

    elif so2 > 15 or industry < 5000:
        return "Industrial"

    elif pm10 > 90:
        return "Agricultural"

    elif pm10 > 50 or dump < 5000:
        return "Burning"

    else:
        return "Burning"

df["pollution_source"] = df.apply(assign_source, axis=1)

output_path = "data/processed/final_labeled_with_weather.csv"
df.to_csv(output_path, index=False)

print(f"✅ Labeled dataset created at: {output_path}")

distribution = df["pollution_source"].value_counts()

print("\nLabel Distribution:")
print(distribution)

plt.figure()
distribution.plot(kind="bar")
plt.title("Pollution Source Distribution")
plt.xlabel("Source Type")
plt.ylabel("Count")

plt.tight_layout()
plt.savefig("data/processed/label_distribution.png")

print("✅ Label distribution chart saved!")

print("\nFinal Columns:")
print(df.columns)

print("\nSample Data:")
print(df.head())