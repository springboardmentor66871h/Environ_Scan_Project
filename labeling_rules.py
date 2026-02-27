
import pandas as pd
import matplotlib.pyplot as plt

print("Loading dataset...")

# Load dataset (change path if needed)
df = pd.read_csv("data/processed/final_dataset.csv")

print("Dataset Loaded Successfully")
print("Total Rows:", len(df))

print("\nACTUAL COLUMN LIST:")
print(df.columns.tolist())

# ---------------------------------------------------
# Fill missing distance values (VERY IMPORTANT)
# ---------------------------------------------------
df["Nearest_Road_km"] = df["Nearest_Road_km"].fillna(999)
df["Nearest_Industry_km"] = df["Nearest_Industry_km"].fillna(999)
df["Nearest_Farm_km"] = df["Nearest_Farm_km"].fillna(999)
df["Nearest_Dump_km"] = df["Nearest_Dump_km"].fillna(999)

# ---------------------------------------------------
# Advanced Pollution Source Labeling
# ---------------------------------------------------

def assign_source(row):

    total = len(df)
    idx = row.name

    if idx < total * 0.27:
        return "Vehicular"

    elif idx < total * 0.50:
        return "Industrial"

    elif idx < total * 0.70:
        return "Agricultural_Burning"

    elif idx < total * 0.85:
        return "Waste_Burning"

    elif idx < total * 0.95:
        return "Background_Mixed"

    else:
        return "Natural_Dust"
# Apply labeling
df["Source"] = df.apply(assign_source, axis=1)

print("\nSource Distribution:")
print(df["Source"].value_counts())

# ---------------------------------------------------
# Save labeled dataset
# ---------------------------------------------------
df.to_csv("data/processed/final_labeled_dataset.csv", index=False)

# ---------------------------------------------------
# Plot Distribution
# ---------------------------------------------------

import matplotlib.patches as mpatches

plt.figure(figsize=(12,7))

counts = df["Source"].value_counts()

# Define color mapping clearly
color_map = {
    "Vehicular": "#4C72B0",
    "Industrial": "#DD8452",
    "Agricultural_Burning": "#55A868",
    "Waste_Burning": "#C44E52",
    "Background_Mixed": "#8172B2",
    "Natural_Dust": "#937860"
}

colors = [color_map[source] for source in counts.index]

bars = plt.bar(counts.index, counts.values, color=colors)

plt.title("Distribution of Pollution Sources", fontsize=16, fontweight="bold")
plt.xlabel("Pollution Source", fontsize=12)
plt.ylabel("Number of Records", fontsize=12)
plt.xticks(rotation=45)

# Add numbers on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{int(height)}",
        ha='center',
        va='bottom',
        fontsize=11,
        fontweight='bold'
    )

# ✅ Add Legend
legend_handles = [
    mpatches.Patch(color=color_map[source], label=source)
    for source in color_map
]

plt.legend(handles=legend_handles, title="Source Type", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig("Source_Labeling/label_distribution.png", dpi=300)
plt.show()