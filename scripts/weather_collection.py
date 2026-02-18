import pandas as pd
import requests
import time

# Cities you want (lowercase for matching)
selected_cities = ["pune", "delhi", "mumbai", "nagpur", "ahmedabad", "srinagar"]

# Load merged pollution dataset
pollution_df = pd.read_csv("Main_Pollution_Dataset.csv")

# Convert datetimeUtc to proper datetime
pollution_df['datetimeUtc'] = pd.to_datetime(pollution_df['datetimeUtc'], utc=True)

# Extract date
pollution_df['date'] = pollution_df['datetimeUtc'].dt.date

# Convert city names to lowercase for matching
pollution_df["city"] = pollution_df["city"].str.lower()

# Filter dataset for only selected cities using partial match
pollution_df = pollution_df[
    pollution_df["city"].apply(lambda x: any(city in x for city in selected_cities))
]

# Check if any city matched
if pollution_df.empty:
    print("❌ No matching city data found. Please check city names in your CSV.")
    exit()

# Show filtered cities
print("✅ Filtered Cities:")
for city_name in pollution_df["city"].unique():
    print("  -", city_name)

# Unique location-date combinations
unique_locations = pollution_df[['city', 'latitude', 'longitude', 'date']].drop_duplicates()

weather_data = []

print("\n⏳ Fetching weather data for selected cities...\n")

# Fetch Weather Data
for _, row in unique_locations.iterrows():
    city_full = row['city']                # full name from dataset
    city_short = [c for c in selected_cities if c in city_full][0].title()  # main city name
    lat = row['latitude']
    lon = row['longitude']
    date = row['date']

    print(f"Fetching weather for {city_short} ({city_full}) on {date}...")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={date}&end_date={date}"
        f"&hourly=temperature_2m,relative_humidity_2m,"
        f"wind_speed_10m,wind_direction_10m"
        f"&timezone=UTC"
    )

    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            data = response.json()
            hourly = data.get("hourly", {})

            if "time" in hourly:
                for i in range(len(hourly["time"])):
                    weather_data.append({
                        "city": city_short,
                        "latitude": lat,
                        "longitude": lon,
                        "datetimeUtc": hourly["time"][i],
                        "Temperature": hourly["temperature_2m"][i],
                        "Humidity": hourly["relative_humidity_2m"][i],
                        "Wind Speed": hourly["wind_speed_10m"][i],
                        "Wind Direction": hourly["wind_direction_10m"][i]
                    })
        else:
            print(f"⚠ Failed for {city_short} on {date} (Status: {response.status_code})")

        # Delay to avoid overloading server
        time.sleep(0.3)

    except Exception as e:
        print(f"⚠ Skipped {city_short} on {date} due to error: {e}")
        continue

# Save Weather Dataset
weather_df = pd.DataFrame(weather_data)
weather_df.to_csv("Weather_Dataset_6Cities.csv", index=False)

print("\n✅ Weather dataset created successfully for all matched cities!")
print("📁 Saved File: Weather_Dataset_6Cities.csv")
