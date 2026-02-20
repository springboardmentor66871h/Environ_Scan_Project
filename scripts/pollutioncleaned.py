import pandas as pd
import os

INPUT_FOLDER = "data/raw/pollution_excels"
OUTPUT_FILE = "data/processed/pollution_all_stations.csv"

all_data = []

print("📦 Combining pollution station datasets...")

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".csv"):
        path = os.path.join(INPUT_FOLDER, file)
        print("Processing:", file)

        df = pd.read_csv(path)

        # clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(".", "")
        )

        # rename date column
        if "from_date" in df.columns:
            df = df.rename(columns={"from_date": "date"})

        # convert date column
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # add station column
        station_name = file.replace(".csv", "")
        station_name = station_name.upper().replace(" ", "_")
        df["station"] = station_name

        # sort by date for proper interpolation
        df = df.sort_values("date")

        # interpolate numeric columns only
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].interpolate(method="linear")

        # handle edge NaNs (start/end) using nearest available value
        df[numeric_cols] = df[numeric_cols].bfill().ffill()

        all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

cols = ["station", "date"] + [c for c in combined_df.columns if c not in ["station", "date"]]
combined_df = combined_df[cols]

os.makedirs("data/processed", exist_ok=True)
combined_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ All stations combined successfully!")
print("Saved to:", OUTPUT_FILE)
print("Stations:", combined_df["station"].unique())
print("Total rows:", len(combined_df))