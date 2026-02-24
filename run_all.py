import os

os.system("python scripts/collect_pollution.py")
os.system("python scripts/collect_weather.py")
os.system("python scripts/extract_location_features.py")
os.system("python scripts/merge_datasets.py")

print("All steps completed successfully.")