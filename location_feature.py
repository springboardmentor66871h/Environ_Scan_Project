import osmnx as ox
import pandas as pd
import os

locations = {
    # DELHI
    ("Delhi", "Anand_Vihar"): (28.6476, 77.3158),
    ("Delhi", "RK_Puram"): (28.5651, 77.1751),
    ("Delhi", "ITO"): (28.6286, 77.2410),
    
    # MUMBAI
    ("Mumbai", "Bandra_Kurla_Complex"): (19.0535, 72.8464),
    ("Mumbai", "Colaba"): (18.9100, 72.8200),
    ("Mumbai", "Worli"): (19.0001, 72.8140),
    
    # BENGALURU
    ("Bengaluru", "City_Railway_Station"): (12.9733, 77.5670),
    ("Bengaluru", "Silk_Board"): (12.9176, 77.6233),
    ("Bengaluru", "Peenya_Industrial_Area"): (13.0329, 77.5273)
}

radius_m = 2000  
records = []

for (city, name), (lat, lon) in locations.items():
    print(f"\n[{city}] Extracting OSM features for {name}...")

    try:
        # Added extended tags for farmland and waste dumps
        gdf = ox.features_from_point(
            (lat, lon),
            tags={
                "highway": ["motorway", "trunk", "primary", "secondary"],
                "landuse": ["industrial", "construction", "commercial", "farmland", "farmyard", "orchard", "vineyard", "plant_nursery", "landfill"],
                "amenity": ["fuel", "bus_station", "waste_disposal", "waste_transfer_station", "waste_dump_site"]
            },
            dist=radius_m
        )

        total_roads = len(gdf[gdf["highway"].notna()]) if "highway" in gdf.columns else 0
        industrial = len(gdf[gdf["landuse"] == "industrial"]) if "landuse" in gdf.columns else 0
        construction = len(gdf[gdf["landuse"] == "construction"]) if "landuse" in gdf.columns else 0
        fuel_stations = len(gdf[gdf["amenity"] == "fuel"]) if "amenity" in gdf.columns else 0
        commercial = len(gdf[gdf["landuse"] == "commercial"]) if "landuse" in gdf.columns else 0
        
        # New Feature 1: Agricultural Labels
        farmland_tags = ["farmland", "farmyard", "orchard", "vineyard", "plant_nursery"]
        farmland = len(gdf[gdf["landuse"].isin(farmland_tags)]) if "landuse" in gdf.columns else 0

        # New Feature 2: Waste and Bur  ning Labels
        waste_amenity_tags = ["waste_disposal", "waste_transfer_station", "waste_dump_site"]
        waste_dumps = (len(gdf[gdf["landuse"] == "landfill"]) if "landuse" in gdf.columns else 0) + \
                      (len(gdf[gdf["amenity"].isin(waste_amenity_tags)]) if "amenity" in gdf.columns else 0)

        records.append({
            "city": city,
            "location": name,
            "latitude": lat,
            "longitude": lon,
            "major_roads_within_2km": total_roads,
            "industrial_zones_within_2km": industrial,
            "construction_sites_within_2km": construction,
            "fuel_stations_within_2km": fuel_stations,
            "commercial_zones_within_2km": commercial,
            "farmland_within_2km": farmland,
            "waste_dumps_within_2km": waste_dumps
        })

    except Exception as e:
        print(f"  -> No features found or error for {name}: {e}")
        records.append({
            "city": city, "location": name, "latitude": lat, "longitude": lon,
            "major_roads_within_2km": 0, "industrial_zones_within_2km": 0,
            "construction_sites_within_2km": 0, "fuel_stations_within_2km": 0,
            "commercial_zones_within_2km": 0, "farmland_within_2km": 0, "waste_dumps_within_2km": 0
        })

df = pd.DataFrame(records)

os.makedirs("data", exist_ok=True)
output_path = "data/India_3city_location_features.csv"
df.to_csv(output_path, index=False)

print(f"\n Feature extraction complete. Data saved to {output_path}")