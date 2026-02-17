import pandas as pd
import os

# ---------- Configuration ----------
INPUT_FOLDER = "data/raw/pollution_excels"
OUTPUT_FILE = "data/processed/pollution_cleaned.csv"

print("Reading pollution files...")

all_data = []

# Standard columns to keep
standard_columns = ["date", "pm2_5", "pm10", "no2", "so2", "co", "ozone", "station"]

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        path = os.path.join(INPUT_FOLDER, file)
        print("\nProcessing:", file)

        try:
            df = pd.read_excel(path, header=0)
        except Exception as e:
            print("❌ Could not read file:", e)
            continue

        # Standardize column names
        df.columns = [str(c).strip().lower().replace(".", "_") for c in df.columns]
        print("Columns found:", df.columns.tolist())

        # Use 'from date' as the main date
        if "from date" in df.columns:
            df = df.rename(columns={"from date": "date"})
        elif "date" in df.columns:
            df = df.rename(columns={"date": "date"})
        else:
            print("⚠ Skipping file — no valid date column found")
            continue

        # Convert 'date' to datetime
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])  # drop rows with missing date

        # Rename pollution columns consistently
        column_rename = {
            "pm2_5": "pm2_5",
            "pm10": "pm10",
            "no2": "no2",
            "so2": "so2",
            "co": "co",
            "ozone": "ozone"
        }
        df = df.rename(columns=column_rename)

        # Fill missing pollution values with column mean
        for col in ["pm2_5", "pm10", "no2", "so2", "co", "ozone"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")  # convert text 'None' to NaN
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = 0  # placeholder if column missing

        # Add station name from filename
        station_name = file.replace(".xlsx", "").replace(".xls", "").replace(" ", "_")
        df["station"] = station_name

        # Keep only standard columns
        all_data.append(df[standard_columns])

if not all_data:
    print("❌ No valid pollution data found")
    exit()

# Combine all files
final_df = pd.concat(all_data, ignore_index=True)

# Sort by station and date
final_df = final_df.sort_values(["station", "date"])

# Ensure output folder exists
os.makedirs("data/processed", exist_ok=True)

# Save cleaned CSV
final_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Clean pollution dataset created")
print("Saved to:", OUTPUT_FILE)
print("Total rows:", len(final_df))
print(final_df.head())
