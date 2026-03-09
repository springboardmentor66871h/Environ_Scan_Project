import pandas as pd
import os
import matplotlib.pyplot as plt

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

# Load pollution dataset
df = pd.read_csv("data/processed/pollution_with_levels.csv")

# Rule-based labeling function
def assign_source(row):

    # Vehicular pollution
    if row["NO2"] > 80 and row["Distance_to_Nearest_Road"] < 0.5:
        return "Vehicular"

    # Industrial pollution
    elif row["SO2"] > 50:
        return "Industrial"

    # Agricultural pollution
    elif row["PM2.5"] > 100 and row["PM10"] > 150:
        return "Agricultural"

    # Burning pollution
    elif row["PM2.5"] > 120:
        return "Burning"

    # Natural pollution
    else:
        return "Natural"

# Apply labeling
df["pollution_source"] = df.apply(assign_source, axis=1)

# Save labeled dataset
df.to_csv("data/processed/final_labeled_dataset.csv", index=False)

print("Labeled dataset created!")

# Plot label distribution
distribution = df["pollution_source"].value_counts()

plt.figure()
distribution.plot(kind="bar")
plt.title("Pollution Source Distribution")
plt.xlabel("Source Type")
plt.ylabel("Count")

plt.savefig("data/processed/label_distribution.png")

print("Label distribution chart saved!")