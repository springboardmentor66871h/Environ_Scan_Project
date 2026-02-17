import pandas as pd
from math import radians, sin, cos, sqrt, atan2

print("Creating distance-based location features...")

# =========================
# 1️⃣ Station coordinates (CPCB stations)
# =========================
stations = {
    "Delhi_ChandniChowk": (28.6560, 77.2300),
    "Delhi_AnandVihar": (28.6469, 77.3153),  # ✅ ADD THIS
    "Bhopal_TTNagar": (23.2336, 77.4009),
    "Mumbai_Sion": (19.0470, 72.8746),
    "Kolkata_RabindraBharati": (22.6270, 88.3800),
    "Bengaluru_Peenya": (13.0280, 77.5180),
    "Chennai_Manali": (13.1660, 80.2580),
    "Lucknow_Talkatora": (26.8467, 80.9462),
    "Hyderabad_Bollaram": (17.5416, 78.4840),
    "Ahmedabad_SAC_ISRO_IITM": (23.0300, 72.5400)
}



# =========================
# 2️⃣ Feature coordinates
# (representative nearby sources)
# =========================
features = {
    "major_road": [
        (28.6448, 77.2167),
        (19.0760, 72.8777),
        (13.0827, 80.2707)
    ],

    "industrial_zone": [
        (13.0310, 77.5150),   # Peenya
        (17.5400, 78.4700),   # Bollaram
        (13.1663, 80.2630)    # Manali
    ],

    "dump_site": [
        (28.6140, 77.2510),   # Delhi landfill region
        (19.0500, 72.8700),   # Mumbai dumping zone
        (22.5700, 88.3600)    # Kolkata waste region
    ],

    "farmland": [
        (26.8800, 80.9000),
        (23.2500, 77.4200),
        (22.7000, 88.3000)
    ]
}

# =========================
# 3️⃣ Distance function
# =========================
def geo_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# =========================
# 4️⃣ Compute minimum distance to each feature type
# =========================
rows = []

for station, (slat, slon) in stations.items():
    row = {"station": station}

    for feature_name, coords_list in features.items():
        distances = [
            geo_distance(slat, slon, flat, flon)
            for flat, flon in coords_list
        ]
        row[f"distance_to_{feature_name}_km"] = min(distances)

    rows.append(row)

df = pd.DataFrame(rows)

# =========================
# 5️⃣ Save dataset
# =========================
output_file = "location_features.csv"
df.to_csv(output_file, index=False)

print("\n✅ Location features created successfully")
print("Saved to:", output_file)
print("\nPreview:")
print(df)
