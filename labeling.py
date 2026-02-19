import pandas as pd
import os

FILE_PATH = r"D:\ENVIRON-SCAN\data\processed\final_dataset.csv"

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(FILE_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["month"] = df["timestamp"].dt.month

# ==========================================
# SEASON FEATURE
# ==========================================

def get_season(month):
    if month in [12,1,2]:
        return "Winter"
    elif month in [3,4,5]:
        return "Summer"
    elif month in [6,7,8,9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["season"] = df["month"].apply(get_season)

# ==========================================
# LABELING LOGIC
# ==========================================

def assign_source(row):

    # Burning
    if row["pm25"] > 180 and row["distance_to_dump"] < 5000:
        return "Burning"

    # Industrial
    elif row["so2"] > 25 and row["distance_to_industry"] < 4000:
        return "Industrial"

    # Vehicular
    elif (
        (row["no2"] > 50 and row["distance_to_road"] < 3000) or
        (row["no2"] > 40 and row["distance_to_road"] < 4000 and row["hour"] in range(7,10)) or
        (row["no2"] > 40 and row["distance_to_road"] < 4000 and row["hour"] in range(17,21))
    ):
        return "Vehicular"

    # Agricultural
    elif (
        row["pm25"] > 120 and
        row["distance_to_farmland"] < 6000 and
        row["season"] in ["Winter", "Post-Monsoon"]
    ):
        return "Agricultural"

    else:
        return "Natural"

# Assign label
df["pollution_source"] = df.apply(assign_source, axis=1)

# ==========================================
# SAVE UPDATED FILE (VERY IMPORTANT)
# ==========================================

df.to_csv(FILE_PATH, index=False)

print("Labeling complete and file updated.")
print("\nDistribution:")
print(df["pollution_source"].value_counts())


