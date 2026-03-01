import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Load Dataset
# -----------------------------
file_path = "../data/processed/final_dataset.csv"
df = pd.read_csv(file_path)

print("Columns:", df.columns)

# -----------------------------
# Column Names
# -----------------------------
PM25 = 'pm2_5'
NO2 = 'no2'
SO2 = 'so2'
WIND = 'wind_speed'
DIST = 'nearest_feature_distance_m'

# -----------------------------
# Improved Data-Driven Thresholds
# -----------------------------
PM25_MOD = df[PM25].quantile(0.70)
PM25_HIGH = df[PM25].quantile(0.85)

NO2_HIGH = df[NO2].quantile(0.70)
SO2_HIGH = df[SO2].quantile(0.70)

NEAR = df[DIST].quantile(0.35)        # More inclusive
VERY_NEAR = df[DIST].quantile(0.20)   # Strong proximity

LOW_WIND = df[WIND].quantile(0.40)
HIGH_WIND = df[WIND].quantile(0.75)

print("\nThresholds Used:")
print("PM25_MOD:", PM25_MOD)
print("PM25_HIGH:", PM25_HIGH)
print("NO2_HIGH:", NO2_HIGH)
print("SO2_HIGH:", SO2_HIGH)
print("NEAR distance:", NEAR)
print("VERY_NEAR distance:", VERY_NEAR)

# -----------------------------
# Realistic Multi-Priority Logic
# -----------------------------
def assign_source(row):

    # 1️⃣ Burning (extreme PM + very near + low wind)
    if (
        row[PM25] > PM25_HIGH and
        row[DIST] < VERY_NEAR and
        row[WIND] < LOW_WIND
    ):
        return "Burning"

    # 2️⃣ Industrial (high SO2 + near)
    elif (
        row[SO2] > SO2_HIGH and
        row[DIST] < NEAR
    ):
        return "Industrial"

    # 3️⃣ Vehicular (high NO2 + near + moderate wind)
    elif (
        row[NO2] > NO2_HIGH and
        row[DIST] < NEAR
    ):
        return "Vehicular"

    # 4️⃣ Agricultural (moderate PM + moderate distance)
    elif (
        row[PM25] > PM25_MOD and
        row[DIST] >= NEAR
    ):
        return "Agricultural"

    # 5️⃣ Natural (background pollution + high wind dust)
    else:
        return "Natural"


# Apply labeling
df['pollution_source'] = df.apply(assign_source, axis=1)

print("\nLabeling Completed ✅")

# -----------------------------
# Save Labeled Dataset
# -----------------------------
output_csv = "../data/processed/final_labeled_dataset.csv"
df.to_csv(output_csv, index=False)

# -----------------------------
# Plot Distribution
# -----------------------------
os.makedirs("../outputs", exist_ok=True)

plt.figure()
df['pollution_source'].value_counts().plot(kind='bar')
plt.title("Pollution Source Distribution")
plt.xlabel("Source")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../outputs/label_distribution.png")

print("\nFinal Distribution:")
print(df['pollution_source'].value_counts())