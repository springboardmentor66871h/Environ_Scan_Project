import pandas as pd
from math import radians, sin, cos, sqrt, atan2

print("Creating distance-based location features...")

# =========================
# 1️⃣ Station coordinates (CPCB stations)
# =========================
stations = {
    "DELHI_CHANDINI_CHOWK": (28.6560, 77.2300),
    "DELHI_ANANT_VIHAR": (28.6469, 77.3153),
    "BHOPAL": (23.2336, 77.4009),
    "MUMBAI": (19.0470, 72.8746),
    "KOLKATA": (22.6270, 88.3800),
    "BENGELURU": (13.0280, 77.5180),
    "CHENNAI": (13.1660, 80.2580),
    "LUCKNOW": (26.8467, 80.9462),
    "HYDERABAD": (17.5416, 78.4840),
    "AHEMEDABAD": (23.0300, 72.5400)
}

# =========================
# 2️⃣ City-specific feature anchors
# =========================
features = {
    "major_road": {
        "DELHI_CHANDINI_CHOWK": (28.6448, 77.2167),
        "DELHI_ANANT_VIHAR": (28.6505, 77.3150),
        "BHOPAL": (23.2599, 77.4126),
        "MUMBAI": (19.0760, 72.8777),
        "KOLKATA": (22.5726, 88.3639),
        "BENGELURU": (13.0285, 77.5460),
        "CHENNAI": (13.0827, 80.2707),
        "LUCKNOW": (26.8467, 80.9462),
        "HYDERABAD": (17.3850, 78.4867),
        "AHEMEDABAD": (23.0225, 72.5714)
    },

    "industrial_zone": {
        "DELHI_CHANDINI_CHOWK": (28.6700, 77.2600),
        "DELHI_ANANT_VIHAR": (28.6600, 77.3300),
        "BHOPAL": (23.2500, 77.4500),
        "MUMBAI": (19.0600, 72.8800),
        "KOLKATA": (22.5600, 88.3900),
        "BENGELURU": (13.0310, 77.5150),
        "CHENNAI": (13.1663, 80.2630),
        "LUCKNOW": (26.9000, 80.9500),
        "HYDERABAD": (17.5400, 78.4700),
        "AHEMEDABAD": (23.0300, 72.5400)
    },

    "dump_site": {
        "DELHI_CHANDINI_CHOWK": (28.6140, 77.2510),
        "DELHI_ANANT_VIHAR": (28.6300, 77.3000),
        "BHOPAL": (23.2300, 77.4200),
        "MUMBAI": (19.0500, 72.8700),
        "KOLKATA": (22.5700, 88.3600),
        "BENGELURU": (13.0000, 77.5200),
        "CHENNAI": (13.1500, 80.2500),
        "LUCKNOW": (26.8500, 80.9300),
        "HYDERABAD": (17.5200, 78.4800),
        "AHEMEDABAD": (23.0200, 72.5500)
    },

    "farmland": {
        "DELHI_CHANDINI_CHOWK": (28.7500, 77.2000),
        "DELHI_ANANT_VIHAR": (28.7200, 77.3500),
        "BHOPAL": (23.2500, 77.4200),
        "MUMBAI": (19.2000, 72.9000),
        "KOLKATA": (22.7000, 88.3000),
        "BENGELURU": (13.2000, 77.6000),
        "CHENNAI": (13.3000, 80.2000),
        "LUCKNOW": (26.8800, 80.9000),
        "HYDERABAD": (17.6000, 78.5000),
        "AHEMEDABAD": (23.1000, 72.6000)
    }
}

# =========================
# 3️⃣ Distance function
# =========================
def geo_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# =========================
# 4️⃣ Compute distances
# =========================
rows = []

for station, (slat, slon) in stations.items():
    row = {"station": station}

    for feature_name, station_map in features.items():
        flat, flon = station_map[station]   # ✅ use full station name
        row[f"distance_to_{feature_name}_km"] = geo_distance(slat, slon, flat, flon)

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("location_features.csv", index=False)

print("\n✅ Location features created successfully")
print(df)