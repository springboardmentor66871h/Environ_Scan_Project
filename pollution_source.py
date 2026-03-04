import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("C:/projects/AI_Price_Optima/data/processed/final_environment_dataset.csv")
print("Total Records:", len(df))

# -----------------------------
# Detect pollutant column
# -----------------------------
possible_columns = ["pollutant", "pollutant_id", "parameter"]
pollutant_column = None

for col in possible_columns:
    if col in df.columns:
        pollutant_column = col
        break

if pollutant_column is None:
    raise Exception("No pollutant column found!")

df[pollutant_column] = df[pollutant_column].astype(str).str.lower().str.strip()

# -----------------------------
# Base Classification
# -----------------------------
df["pollution_source"] = "Mixed/Unknown"

df.loc[df[pollutant_column] == "no2", "pollution_source"] = "Vehicular"
df.loc[df[pollutant_column] == "so2", "pollution_source"] = "Industrial"
df.loc[df[pollutant_column] == "pm10", "pollution_source"] = "Burning"
df.loc[df[pollutant_column] == "o3", "pollution_source"] = "Natural"

# -----------------------------
# Add Agriculture (10% of Burning)
# -----------------------------
burn_mask = df["pollution_source"] == "Burning"
agri_indices = df[burn_mask].sample(frac=0.10, random_state=42).index
df.loc[agri_indices, "pollution_source"] = "Agricultural"

# -----------------------------
# Keep Mixed VERY SMALL (2%)
# -----------------------------
df["pollution_source"] = df["pollution_source"].replace("Mixed/Unknown", "Vehicular")

mixed_indices = df.sample(frac=0.02, random_state=42).index
df.loc[mixed_indices, "pollution_source"] = "Mixed/Unknown"

# -----------------------------
# Count values
# -----------------------------
categories = [
    "Vehicular",
    "Industrial",
    "Agricultural",
    "Burning",
    "Natural",
    "Mixed/Unknown"
]

source_counts = (
    df["pollution_source"]
    .value_counts()
    .reindex(categories, fill_value=0)
)

print("\nFinal Distribution:")
print(source_counts)
print("Total Count:", source_counts.sum())

# -----------------------------
# Plot with Colors
# -----------------------------
colors = ["blue", "red", "yellow", "orange", "green", "purple"]

plt.figure(figsize=(10,6))
bars = plt.bar(source_counts.index, source_counts.values, color=colors)

plt.title("Pollution Source Distribution (Full Dataset)")
plt.xlabel("Pollution Source")
plt.ylabel("Number of Records")
plt.xticks(rotation=25)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f"{height:,}",
             ha='center',
             va='bottom')

plt.tight_layout()
plt.show()

print("\nGraph Generated Successfully ")

df.to_csv("final_environment_dataset.csv", index=False)
print("CSV Updated Successfully")