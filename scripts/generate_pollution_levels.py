import pandas as pd
import numpy as np
import os

os.makedirs("data/processed", exist_ok=True)

stations = pd.read_csv("data/stations_with_spatial_features.csv")

np.random.seed(42)

stations["PM2.5"] = np.random.uniform(20,150,len(stations))
stations["PM10"] = np.random.uniform(30,200,len(stations))
stations["NO2"] = np.random.uniform(10,120,len(stations))
stations["CO"] = np.random.uniform(0.5,3,len(stations))
stations["SO2"] = np.random.uniform(5,80,len(stations))
stations["O3"] = np.random.uniform(10,100,len(stations))

stations.to_csv("data/processed/pollution_with_levels.csv",index=False)

print("Synthetic pollution dataset created!")