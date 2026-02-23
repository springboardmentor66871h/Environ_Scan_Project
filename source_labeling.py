import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Load Dataset (use your correct path)
# ----------------------------------------------------
df = pd.read_csv(r"Dataset/Final_Dataset_Environ.csv")

# ----------------------------------------------------
# Updated Thresholds (More Balanced)
# ----------------------------------------------------
PM25_HIGH = 55
PM10_HIGH = 90
NO2_HIGH = 35
SO2_HIGH = 25
CO_HIGH  = 0.8

# Distances in meters (Expanded)
ROAD_NEAR     = 6000
INDUSTRY_NEAR = 7000
FARMLAND_NEAR = 5000
DUMP_NEAR     = 7000

# ----------------------------------------------------
# Rule-Based Label Assignment
# ----------------------------------------------------
def assign_source(row):

    # 1. Vehicular
    if (row["no2"] > NO2_HIGH or row["co"] > CO_HIGH) and row["dist_road"] < ROAD_NEAR:
        return "Vehicular"

    # 2. Burning (Dump Waste)
    elif (row["pm25"] > PM25_HIGH or row["pm10"] > PM10_HIGH) and row["dist_dump"] < DUMP_NEAR:
        return "Burning"

    # 3. Industrial
    elif row["so2"] > SO2_HIGH and row["dist_industry"] < INDUSTRY_NEAR:
        return "Industrial"

    # 4. Agricultural
    elif (row["pm25"] > PM25_HIGH or row["pm10"] > PM10_HIGH) and row["dist_farmland"] < FARMLAND_NEAR:
        return "Agricultural"

    # 5. Natural
    else:
        return "Natural"


# ----------------------------------------------------
# Apply Labels
# ----------------------------------------------------
df["pollution_source"] = df.apply(assign_source, axis=1)

# ----------------------------------------------------
# Print Distribution
# ----------------------------------------------------
print("\nPollution Source Distribution:\n")
print(df["pollution_source"].value_counts())

# ----------------------------------------------------
# Save Updated Dataset
# ----------------------------------------------------
df.to_csv("Final_Labeled_Pollution_Dataset_Updated.csv", index=False)

print("\nUpdated dataset saved as:")
print("Final_Labeled_Pollution_Dataset_Updated.csv")

# ----------------------------------------------------
# Bar Chart Visualization
# ----------------------------------------------------
df["pollution_source"].value_counts().plot(kind="bar")

plt.title("Pollution Source Label Distribution")
plt.xlabel("Pollution Source")
plt.ylabel("Number of Records")

plt.show()
