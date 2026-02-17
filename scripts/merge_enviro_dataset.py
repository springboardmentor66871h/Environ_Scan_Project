import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

print("Loading datasets...")

pollution = pd.read_csv(os.path.join(BASE_DIR, "data/raw/pollution_cleaned.csv"))
weather = pd.read_csv(os.path.join(BASE_DIR, "data/raw/weather_data.csv"))
location = pd.read_csv(os.path.join(BASE_DIR, "data/raw/location_features.csv"))

print("Files loaded successfully\n")

# ---------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------
def clean_columns(df):
    df.columns = df.columns.str.lower().str.strip()
    return df

pollution = clean_columns(pollution)
weather = clean_columns(weather)
location = clean_columns(location)

# ---------------------------------------------------
# ENSURE STATION COLUMN EXISTS
# ---------------------------------------------------
def ensure_station(df):
    if "station" in df.columns:
        col = "station"
    elif "city" in df.columns:
        col = "city"
    elif "location" in df.columns:
        col = "location"
    else:
        raise ValueError("❌ No station/city column found")

    df["station"] = df[col].astype(str)
    return df

pollution = ensure_station(pollution)
weather = ensure_station(weather)
location = ensure_station(location)

# ---------------------------------------------------
# NORMALIZE STATION TEXT
# ---------------------------------------------------
def normalize_station(df):
    df["station"] = (
        df["station"]
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace("-", " ", regex=False)
    )
    return df

pollution = normalize_station(pollution)
weather = normalize_station(weather)
location = normalize_station(location)

# ---------------------------------------------------
# EXTRACT CITY FROM STATION
# Works for:
# "bhopal"
# "delhi anand vihar"
# "delhi_chandnichowk"
# ---------------------------------------------------
def extract_city(df):
    df["city"] = (
        df["station"]
        .str.replace("_", " ", regex=False)
        .str.split()
        .str[0]
    )
    return df

pollution = extract_city(pollution)
weather = extract_city(weather)
location = extract_city(location)

# ---------------------------------------------------
# STANDARDIZE DATE IF PRESENT
# ---------------------------------------------------
def ensure_date(df):
    for col in ["date", "timestamp", "from date"]:
        if col in df.columns:
            df["date"] = pd.to_datetime(df[col], errors="coerce").dt.date
            return df
    return df

pollution = ensure_date(pollution)
weather = ensure_date(weather)

# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------
for df in [pollution, weather, location]:
    df.replace(["None", "none", ""], pd.NA, inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)

# ---------------------------------------------------
# DEBUG CHECK
# ---------------------------------------------------
print("Rows before merge:")
print("Pollution:", len(pollution))
print("Weather:", len(weather))
print("Location:", len(location))

print("\nCities detected:")
print("Pollution:", pollution["city"].unique())
print("Weather:", weather["city"].unique())
print("Location:", location["city"].unique())

# ---------------------------------------------------
# MERGE DATASETS (CITY LEVEL)
# ---------------------------------------------------
print("\nMerging pollution + weather...")
merged = pd.merge(
    pollution,
    weather,
    on="city",
    how="left",
    suffixes=("_pollution", "_weather")
)

print("Adding location features...")
merged = pd.merge(
    merged,
    location,
    on="city",
    how="left"
)

# ---------------------------------------------------
# FINAL CLEAN
# ---------------------------------------------------
merged.fillna(merged.mean(numeric_only=True), inplace=True)
merged.drop_duplicates(inplace=True)

print("\nNon-null values per column:")
print(merged.notna().sum())

# ---------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------
output_dir = os.path.join(BASE_DIR, "data/processed")
os.makedirs(output_dir, exist_ok=True)

csv_path = os.path.join(output_dir, "enviro_final_dataset.csv")
json_path = os.path.join(output_dir, "enviro_final_dataset.json")

merged.to_csv(csv_path, index=False)
merged.to_json(json_path, orient="records")

print("\n✅ FINAL DATASET CREATED SUCCESSFULLY")
print("Saved to:", csv_path)
print("Final shape:", merged.shape)
print(merged.head())
