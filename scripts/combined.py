import pandas as pd

print("📦 Loading datasets...")

weather = pd.read_csv("data/raw/weather_data.csv")
pollution = pd.read_csv("data/raw/pollution_data.csv")
location = pd.read_csv("data/raw/location_features_data.csv")

# ---------- clean column names ----------
def clean(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

weather = clean(weather)
pollution = clean(pollution)
location = clean(location)

# ---------- FIX COLUMN NAME DIFFERENCES ----------
# (prevents KeyError: date)
if "timestamp" in weather.columns:
    weather = weather.rename(columns={"timestamp": "date"})
if "from_date" in pollution.columns:
    pollution = pollution.rename(columns={"from_date": "date"})

# ---------- ensure consistent keys ----------
weather["station"] = weather["station"].str.upper().str.strip()
pollution["station"] = pollution["station"].str.upper().str.strip()
location["station"] = location["station"].str.upper().str.strip()

# ---------- convert to datetime safely ----------
weather["date"] = pd.to_datetime(weather["date"], errors="coerce")
pollution["date"] = pd.to_datetime(pollution["date"], errors="coerce")

# remove time part → avoids mismatch
weather["date"] = weather["date"].dt.date
pollution["date"] = pollution["date"].dt.date

# ---------- REMOVE UNUSED COLUMN ----------
if "to_date" in pollution.columns:
    pollution = pollution.drop(columns=["to_date"])

# ---------- MERGE (KEEP ALL WEATHER ROWS) ----------
print("🔗 Merging weather + pollution...")
merged = pd.merge(
    weather,
    pollution,
    on=["station", "date"],
    how="left"   # ⭐ IMPORTANT: prevents row loss
)

# ---------- ADD LOCATION FEATURES ----------
print("🌍 Adding location features...")
merged = pd.merge(
    merged,
    location,
    on="station",
    how="left"
)

# ---------- OPTIONAL: fill pollution gaps ----------
pollution_cols = ["pm2_5", "pm10", "no2", "so2", "co", "ozone"]

for col in pollution_cols:
    if col in merged.columns:
        merged[col] = merged.groupby("station")[col].transform(
            lambda x: x.interpolate(method="linear").fillna(method="bfill").fillna(method="ffill")
        )

# ---------- FINAL SORT ----------
merged = merged.sort_values(["station", "date"])

# ---------- SAVE ----------
merged.to_csv("data/processed/enviro_merged_dataset.csv", index=False)

print("\n✅ FINAL DATASET READY!")
print("Shape:", merged.shape)
print("Stations:", merged["station"].nunique())
print("Columns:", list(merged.columns))