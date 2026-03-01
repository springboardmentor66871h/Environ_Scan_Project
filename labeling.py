import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = r"D:\ENVIRON-SCAN\data\processed\final_dataset.csv"
PLOT_PATH = r"D:\ENVIRON-SCAN\data\processed\label_distribution.png"

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv(FILE_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["month"] = df["timestamp"].dt.month

# ----------------------------
# Season Feature (Temporary)
# ----------------------------
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["season"] = df["month"].apply(get_season)

# ----------------------------
# Labeling Logic
# ----------------------------
def assign_source(row):

    # Burning
    if (
        row["pm25"] > 170 and
        row["distance_to_dump"] < 4500
    ):
        return "Burning"

    # Industrial (stricter threshold)
    elif (
        row["so2"] > 35 and
        row["distance_to_industry"] < 2500 and
        row["pm25"] > 80
    ):
        return "Industrial"

    # Vehicular
    elif (
        (row["no2"] > 45 and row["distance_to_road"] < 3500) or
        (row["no2"] > 40 and row["distance_to_road"] < 4000 and row["hour"] in range(7,10)) or
        (row["no2"] > 40 and row["distance_to_road"] < 4000 and row["hour"] in range(17,21))
    ):
        return "Vehicular"

    # Agricultural
    elif (
        row["pm25"] > 100 and
        row["distance_to_farmland"] < 7000 and
        row["season"] in ["Winter", "Post-Monsoon"]
    ):
        return "Agricultural"

    # Natural
    else:
        return "Natural"


# Apply labels
df["pollution_source"] = df.apply(assign_source, axis=1)

# ----------------------------
# Remove Temporary Columns
# ----------------------------
for col in ["hour", "month", "season"]:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

# ----------------------------
# Save Final Dataset
# ----------------------------
df.to_csv(FILE_PATH, index=False)

# ----------------------------
# Generate Distribution Plot
# ----------------------------
counts = df["pollution_source"].value_counts()

plt.figure(figsize=(8, 5))
counts.plot(kind="bar")
plt.title("Pollution Source Distribution")
plt.xlabel("Source")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.close()

print("Labeling complete.")
print("Final dataset updated.")
print("Distribution plot saved.")