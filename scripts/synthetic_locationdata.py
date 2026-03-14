import pandas as pd
import numpy as np
import math

print("📍 Generating synthetic location features...")

# -------------------------------
# 1️⃣ Station coordinates
# -------------------------------
stations = {
    "DELHI_CHANDINI_CHOWK": (28.6560, 77.2300),
    "DELHI_ANANT_VIHAR": (28.6469, 77.3153),
    "DELHI_ITO": (28.6280, 77.2410),

    "BHOPAL": (23.2336, 77.4009),
    "BHOPAL_PARYAVARAN_PARK": (23.2500, 77.4200),
    "BHOPAL_IDGAH_HILLS": (23.2550, 77.4100),

    "MUMBAI": (19.0470, 72.8746),
    "MUMBAI_BYCULLA": (18.9767, 72.8331),
    "MUMBAI_CHAKALA_ANDHERI": (19.1100, 72.8620),

    "KOLKATA": (22.6270, 88.3800),
    "KOLKATA_BALLYGUNGE": (22.5250, 88.3630),
    "KOLKATA_JADAVPUR": (22.4993, 88.3710),

    "BENGELURU": (13.0280, 77.5180),
    "BENGALURU_HEBBAL": (13.0358, 77.5970),
    "BENGALURU_RAILWAY_STATION": (12.9784, 77.5686),

    "CHENNAI": (13.1660, 80.2580),
    "CHENNAI_ALANDUR_BUS_DEPOT": (13.0046, 80.2017),
    "CHENNAI_VELACHERY": (12.9750, 80.2212),

    "LUCKNOW": (26.8467, 80.9462),
    "LUCKNOW_TALKATORA": (26.8350, 80.9000),
    "LUCKNOW_LALBAGH": (26.8485, 80.9416),

    "HYDERABAD": (17.5416, 78.4840),
    "HYDERABAD_PATENCHERU": (17.5330, 78.2600),
    "HYDERABAD_SOMAJIGUDA": (17.4240, 78.4595),

    "AHEMEDABAD": (23.0300, 72.5400),
    "AHMEDABAD_SOMAJIGUDA": (23.0370, 72.5666),
    "AHMEDABAD_SVPT": (23.0350, 72.5800),
}

# -------------------------------
# 2️⃣ Haversine distance
# -------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

# -------------------------------
# 3️⃣ Generate synthetic nearby points
# -------------------------------
def generate_nearby(lat, lon, radius_km):
    """Create a random nearby coordinate within radius"""
    delta = radius_km / 111  # approx degree conversion
    return (
        lat + np.random.uniform(-delta, delta),
        lon + np.random.uniform(-delta, delta)
    )

np.random.seed(42)

rows = []

for station, (lat, lon) in stations.items():

    # synthetic feature anchors
    road = generate_nearby(lat, lon, np.random.uniform(0.2, 2))
    industry = generate_nearby(lat, lon, np.random.uniform(1, 6))
    dump = generate_nearby(lat, lon, np.random.uniform(2, 8))
    farmland = generate_nearby(lat, lon, np.random.uniform(3, 15))

    rows.append({
        "station": station,
        "distance_to_major_road_km": round(haversine(lat, lon, *road), 3),
        "distance_to_industrial_zone_km": round(haversine(lat, lon, *industry), 3),
        "distance_to_dump_site_km": round(haversine(lat, lon, *dump), 3),
        "distance_to_farmland_km": round(haversine(lat, lon, *farmland), 3),
    })

df = pd.DataFrame(rows)

# -------------------------------
# 4️⃣ Save file
# -------------------------------
df.to_csv("data/raw/location_features_data.csv", index=False)

print("✅ Synthetic location features created successfully")
print(df.head())
print("Total stations:", len(df))