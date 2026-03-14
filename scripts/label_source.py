import pandas as pd
import os
import matplotlib.pyplot as plt

print("EnviroScan Week-3 Source Labeling Started...")

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "enviro_merged_dataset.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "enviro_labeled_dataset.csv")

print("Reading dataset from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)
print("Rows loaded:", len(df))


# =========================
# STATION TYPE MAPPING (SCIENTIFIC CONTEXT)
# =========================
STATION_TYPE = {

    # Delhi
    "DELHI_CHANDINI_CHOWK": "Vehicular",
    "DELHI_ANANT_VIHAR": "Industrial",
    "DELHI_ITO": "Vehicular",

    # Bhopal
    "BHOPAL": "Residential",
    "BHOPAL_PARYAVARAN_PARK": "Natural",
    "BHOPAL_IDGAH_HILLS": "Residential",

    # Mumbai
    "MUMBAI": "Vehicular",
    "MUMBAI_BYCULLA": "Vehicular",
    "MUMBAI_CHAKALA_ANDHERI": "Industrial",

    # Kolkata
    "KOLKATA": "Residential",
    "KOLKATA_BALLYGUNGE": "Residential",
    "KOLKATA_JADAVPUR": "Industrial",

    # Bengaluru
    "BENGELURU": "Residential",
    "BENGALURU_HEBBAL": "Vehicular",
    "BENGALURU_RAILWAY_STATION": "Vehicular",

    # Chennai
    "CHENNAI": "Residential",
    "CHENNAI_ALANDUR_BUS_DEPOT": "Vehicular",
    "CHENNAI_VELACHERY": "Residential",

    # Lucknow
    "LUCKNOW": "Residential",
    "LUCKNOW_TALKATORA": "Industrial",
    "LUCKNOW_LALBAGH": "Vehicular",

    # Hyderabad
    "HYDERABAD": "Residential",
    "HYDERABAD_PATENCHERU": "Industrial",
    "HYDERABAD_SOMAJIGUDA": "Vehicular",

    # Ahmedabad
    "AHEMEDABAD": "Residential",
    "AHMEDABAD_SOMAJIGUDA": "Vehicular",
    "AHMEDABAD_SVPT": "Vehicular"
}


# =========================
# HELPER
# =========================
def get_pm25(row):
    if "pm25" in row:
        return row["pm25"]
    if "pm2_5" in row:
        return row["pm2_5"]
    if "pm2.5" in row:
        return row["pm2.5"]
    return 0


# =========================
# SOURCE LABELING ENGINE
# =========================
def assign_source(row):

    pm25 = get_pm25(row)
    pm10 = row.get("pm10", 0)
    no2 = row.get("no2", 0)
    so2 = row.get("so2", 0)
    co = row.get("co", 0)

    station = row["station"]
    station_type = STATION_TYPE.get(station, "Unknown")

    scores = {
        "Vehicular": 0,
        "Industrial": 0,
        "Agricultural": 0,
        "Burning": 0,
        "Natural": 0
    }

    # ===== STRONG STATION PRIOR =====
    if station_type == "Vehicular":
        scores["Vehicular"] += 3

    elif station_type == "Industrial":
        scores["Industrial"] += 3

    elif station_type == "Residential":
        scores["Vehicular"] += 1
        scores["Natural"] += 1

    elif station_type == "Natural":
        scores["Natural"] += 3


    # ===== POLLUTANT SIGNATURE =====

    # Vehicular pattern
    if no2 >= 40:
        scores["Vehicular"] += 2
    if co >= 1:
        scores["Vehicular"] += 1

    # Industrial pattern
    if so2 >= 20:
        scores["Industrial"] += 2
    if pm10 >= 120:
        scores["Industrial"] += 1

    # Waste burning
    if pm25 >= 100 and pm10 >= 180:
        scores["Burning"] += 3

    # Agricultural
    if pm25 >= 80 and so2 < 10:
        scores["Agricultural"] += 2

    # Natural background
    if pm25 < 35 and pm10 < 70:
        scores["Natural"] += 2


    # ===== FINAL DECISION =====
    best = max(scores, key=scores.get)
    best_score = scores[best]
    sorted_scores = sorted(scores.values(), reverse=True)

    if best_score == 0:
        return "Unknown / Mixed"

    if sorted_scores[0] - sorted_scores[1] < 2:
        return "Unknown / Mixed"

    return best


# =========================
# APPLY LABELING
# =========================
df["pollution_source"] = df.apply(assign_source, axis=1)

print("\nLabel Distribution:")
print(df["pollution_source"].value_counts())


# =========================
# SAVE DATASET
# =========================
df.to_csv(OUTPUT_PATH, index=False)
print("\nSaved labeled dataset to:", OUTPUT_PATH)


# =========================
# PLOT DISTRIBUTION
# =========================
plt.figure(figsize=(8,5))
df["pollution_source"].value_counts().plot(kind="bar")
plt.title("Pollution Source Distribution")
plt.xlabel("Source")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nWeek-3 Source Labeling Completed Successfully 🚀")