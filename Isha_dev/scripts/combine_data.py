import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import os

# =============================================
# CONFIGURATION
# =============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Input directories - FIXED: Looking directly in raw folder, not subfolders
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CONFIG_DIR = BASE_DIR / "data" / "config"

# Output directory
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# =============================================
# HELPER FUNCTIONS
# =============================================
def find_file(directory, filename):
    """Find a specific file in directory"""
    file_path = directory / filename
    if file_path.exists():
        return file_path
    
    # Try with different extensions
    file_path = directory / f"{filename}.csv"
    if file_path.exists():
        return file_path
    
    # Try pattern matching
    files = list(directory.glob(f"*{filename}*.csv"))
    if files:
        return files[0]
    
    return None

def load_dataset(file_path, dataset_name):
    """Load a dataset and print basic info"""
    if not file_path or not file_path.exists():
        print(f"   {dataset_name}: No file found")
        return None
    
    df = pd.read_csv(file_path)
    print(f"   {dataset_name}: {len(df)} rows, {df.shape[1]} columns")
    return df

def standardize_city_names(df, city_col='city'):
    """Standardize city names (strip, title case)"""
    if city_col in df.columns:
        df[city_col] = df[city_col].astype(str).str.strip().str.title()
    return df

# =============================================
# 1. FIND FILES IN RAW DIRECTORY
# =============================================
print("="*60)
print("ENVIROSCAN - DATASET COMBINER")
print("="*60)
print(f"\n Looking for datasets in:")
print(f"   Raw data folder: {RAW_DATA_DIR}")
print()

# Find files directly in raw folder
pollution_file = find_file(RAW_DATA_DIR, "pollution_by_area")
weather_file = find_file(RAW_DATA_DIR, "weather_areas")
location_file = find_file(RAW_DATA_DIR, "location_features_areas")

print(f"   Found pollution file: {pollution_file.name if pollution_file else 'Not found'}")
print(f"   Found weather file: {weather_file.name if weather_file else 'Not found'}")
print(f"   Found location file: {location_file.name if location_file else 'Not found'}")
print()

# =============================================
# 2. LOAD DATASETS
# =============================================
print("\n LOADING DATASETS")
print("-" * 40)

pollution_df = load_dataset(pollution_file, "Pollution")
weather_df = load_dataset(weather_file, "Weather")
location_df = load_dataset(location_file, "Location Features")

if pollution_df is None or weather_df is None:
    print("\n Error: Missing required datasets (pollution and weather are mandatory)")
    print("\n   Expected files in:", RAW_DATA_DIR)
    print("   - pollution_by_area.csv")
    print("   - weather_areas.csv")
    print("   - location_features_areas.csv")
    exit()

# =============================================
# 3. STANDARDIZE COLUMN NAMES
# =============================================
print("\n STANDARDIZING COLUMNS")
print("-" * 40)

# Check for area column and create city if needed
for df, name in [(pollution_df, "Pollution"), (weather_df, "Weather"), (location_df, "Location")]:
    if df is not None:
        if 'city' not in df.columns and 'area' in df.columns:
            # If there's an area but no city, use area as city
            df['city'] = df['area']
            print(f"   Created 'city' from 'area' in {name} data")
        elif 'city' not in df.columns and 'location' in df.columns:
            df['city'] = df['location']
            print(f"   Created 'city' from 'location' in {name} data")

# Standardize city names
pollution_df = standardize_city_names(pollution_df)
weather_df = standardize_city_names(weather_df)
if location_df is not None:
    location_df = standardize_city_names(location_df)

print("   City names standardized")

# =============================================
# 4. SELECT RELEVANT COLUMNS
# =============================================
print("\n SELECTING RELEVANT COLUMNS")
print("-" * 40)

# Pollution columns - keep city, area, and all pollutant measurements
pollution_cols = ['city']
if 'area' in pollution_df.columns:
    pollution_cols.append('area')

pollutant_keywords = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'pm2.5', 'aqi', 'pollutant']
for col in pollution_df.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in pollutant_keywords):
        if col not in pollution_cols:
            pollution_cols.append(col)

# Keep only selected columns
pollution_df = pollution_df[[col for col in pollution_cols if col in pollution_df.columns]].copy()
print(f"   Pollution: keeping {len(pollution_df.columns)} columns")

# Weather columns
weather_cols = ['city']
if 'area' in weather_df.columns:
    weather_cols.append('area')

weather_keywords = ['temp', 'humidity', 'pressure', 'wind', 'weather', 'description', 'feels']
for col in weather_df.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in weather_keywords):
        if col not in weather_cols:
            weather_cols.append(col)

# Keep timestamp if available
if 'timestamp' in weather_df.columns and 'timestamp' not in weather_cols:
    weather_cols.append('timestamp')
if 'last_updated' in weather_df.columns:
    weather_cols.append('last_updated')

weather_df = weather_df[[col for col in weather_cols if col in weather_df.columns]].copy()
print(f"   Weather: keeping {len(weather_df.columns)} columns")

# Location columns
if location_df is not None:
    location_cols = ['city']
    if 'area' in location_df.columns:
        location_cols.append('area')
    
    location_keywords = ['road', 'segment', 'industrial', 'farmland', 'dump', 'power', 
                         'bus', 'railway', 'parking', 'density', 'count']
    for col in location_df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in location_keywords):
            if col not in location_cols:
                location_cols.append(col)
    
    location_df = location_df[[col for col in location_cols if col in location_df.columns]].copy()
    print(f"   Location: keeping {len(location_df.columns)} columns")

# =============================================
# 5. AGGREGATE POLLUTION DATA (LATEST PER CITY/AREA)
# =============================================
print("\n AGGREGATING POLLUTION DATA")
print("-" * 40)

# Check if we have timestamp
if 'timestamp' in pollution_df.columns:
    pollution_df['timestamp'] = pd.to_datetime(pollution_df['timestamp'], errors='coerce')
    # Get latest record for each city-area combination
    if 'area' in pollution_df.columns:
        latest_idx = pollution_df.groupby(['city', 'area'])['timestamp'].idxmax()
    else:
        latest_idx = pollution_df.groupby('city')['timestamp'].idxmax()
    pollution_agg = pollution_df.loc[latest_idx].reset_index(drop=True)
    print(f"   Aggregated by latest timestamp: {len(pollution_agg)} records")
else:
    # Take first record per city-area
    if 'area' in pollution_df.columns:
        pollution_agg = pollution_df.drop_duplicates(subset=['city', 'area'], keep='first').reset_index(drop=True)
    else:
        pollution_agg = pollution_df.drop_duplicates(subset=['city'], keep='first').reset_index(drop=True)
    print(f"   Using first record per city: {len(pollution_agg)} records")

# =============================================
# 6. AGGREGATE WEATHER DATA (LATEST PER CITY/AREA)
# =============================================
print("\n AGGREGATING WEATHER DATA")
print("-" * 40)

timestamp_col = None
for col in ['timestamp', 'last_updated', 'date', 'time']:
    if col in weather_df.columns:
        timestamp_col = col
        break

if timestamp_col:
    weather_df[timestamp_col] = pd.to_datetime(weather_df[timestamp_col], errors='coerce')
    if 'area' in weather_df.columns:
        latest_weather_idx = weather_df.groupby(['city', 'area'])[timestamp_col].idxmax()
    else:
        latest_weather_idx = weather_df.groupby('city')[timestamp_col].idxmax()
    weather_agg = weather_df.loc[latest_weather_idx].reset_index(drop=True)
    print(f"  ✓ Aggregated by latest timestamp: {len(weather_agg)} records")
else:
    if 'area' in weather_df.columns:
        weather_agg = weather_df.drop_duplicates(subset=['city', 'area'], keep='first').reset_index(drop=True)
    else:
        weather_agg = weather_df.drop_duplicates(subset=['city'], keep='first').reset_index(drop=True)
    print(f"  ✓ Using first record per city: {len(weather_agg)} records")

# =============================================
# 7. MERGE DATASETS
# =============================================
print("\n MERGING DATASETS")
print("-" * 40)

# Determine merge keys
merge_keys = ['city']
if 'area' in pollution_agg.columns and 'area' in weather_agg.columns:
    merge_keys.append('area')
    print(f"  Merging on: {merge_keys}")

# Start with pollution data
combined = pollution_agg.copy()
print(f"  Starting with {len(combined)} records from pollution data")

# Merge weather
combined = combined.merge(
    weather_agg, 
    on=merge_keys, 
    how='left', 
    suffixes=('', '_weather')
)
print(f"  After weather merge: {len(combined)} records")

# Merge location if available
if location_df is not None:
    # Take first record per city-area for location features
    if 'area' in location_df.columns and 'area' in combined.columns:
        location_unique = location_df.drop_duplicates(subset=['city', 'area'], keep='first').reset_index(drop=True)
        combined = combined.merge(
            location_unique,
            on=['city', 'area'],
            how='left',
            suffixes=('', '_location')
        )
    else:
        location_unique = location_df.drop_duplicates(subset=['city'], keep='first').reset_index(drop=True)
        combined = combined.merge(
            location_unique,
            on='city',
            how='left',
            suffixes=('', '_location')
        )
    print(f"  After location merge: {len(combined)} records")

print(f"\n  Final shape: {combined.shape[0]} rows × {combined.shape[1]} columns")

# =============================================
# 8. FEATURE ENGINEERING
# =============================================
print("\n FEATURE ENGINEERING")
print("-" * 40)

# Function to categorize AQI based on PM2.5
def categorize_aqi(pm25):
    if pd.isna(pm25):
        return np.nan
    if pm25 <= 30:
        return 'Good'
    elif pm25 <= 60:
        return 'Moderate'
    elif pm25 <= 90:
        return 'Unhealthy for Sensitive'
    elif pm25 <= 120:
        return 'Unhealthy'
    elif pm25 <= 250:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

# Find PM2.5 column (could be named pm25 or pm2.5)
pm25_col = None
for col in combined.columns:
    if 'pm2.5' in col.lower() or 'pm25' in col.lower():
        pm25_col = col
        break

if pm25_col:
    combined['aqi_category'] = combined[pm25_col].apply(categorize_aqi)
    print(f"  ✓ Created AQI category from {pm25_col}")

# Create season from timestamp
timestamp_col = None
for col in ['timestamp', 'last_updated', 'date']:
    if col in combined.columns:
        timestamp_col = col
        break

if timestamp_col:
    combined[timestamp_col] = pd.to_datetime(combined[timestamp_col], errors='coerce')
    combined['month'] = combined[timestamp_col].dt.month
    
    # Map month to season in India
    season_map = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Summer', 4: 'Summer', 5: 'Summer',
        6: 'Monsoon', 7: 'Monsoon', 8: 'Monsoon',
        9: 'Post-Monsoon', 10: 'Post-Monsoon', 11: 'Post-Monsoon'
    }
    combined['season'] = combined['month'].map(season_map)
    print(f"  ✓ Created month and season features")

# Calculate pollution severity score (normalized sum of pollutants)
pollutant_cols = []
for col in combined.columns:
    col_lower = col.lower()
    if any(p in col_lower for p in ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']):
        if col not in pollutant_cols:
            pollutant_cols.append(col)

if len(pollutant_cols) >= 3:
    # Normalize each pollutant
    for col in pollutant_cols:
        if combined[col].notna().any():
            min_val = combined[col].min()
            max_val = combined[col].max()
            if max_val > min_val:
                combined[f'{col}_norm'] = (combined[col] - min_val) / (max_val - min_val)
    
    # Sum normalized values
    norm_cols = [f'{col}_norm' for col in pollutant_cols if f'{col}_norm' in combined.columns]
    if norm_cols:
        combined['pollution_severity'] = combined[norm_cols].sum(axis=1)
        print(f"   Created pollution severity score from {len(norm_cols)} pollutants")

# =============================================
# 9. HANDLE MISSING VALUES
# =============================================
print("\n HANDLING MISSING VALUES")
print("-" * 40)

missing_before = combined.isnull().sum().sum()
print(f"  Missing values before: {missing_before}")

# Fill numeric columns with median
numeric_cols = combined.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if combined[col].isnull().any():
        combined[col].fillna(combined[col].median(), inplace=True)

# Fill categorical columns with mode or 'Unknown'
categorical_cols = combined.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if combined[col].isnull().any() and col not in ['city', 'area']:
        if combined[col].mode().any():
            combined[col].fillna(combined[col].mode()[0], inplace=True)
        else:
            combined[col].fillna('Unknown', inplace=True)

missing_after = combined.isnull().sum().sum()
print(f"  Missing values after: {missing_after}")

# =============================================
# 10. SELECT FINAL COLUMNS FOR PROJECT
# =============================================
print("\n SELECTING FINAL COLUMNS")
print("-" * 40)

# Essential columns for the project
essential_cols = ['city']
if 'area' in combined.columns:
    essential_cols.append('area')

# Add pollutant columns
pollutants_found = [col for col in pollutant_cols if col in combined.columns]
essential_cols.extend(pollutants_found)

# Add weather columns
weather_found = []
for col in combined.columns:
    col_lower = col.lower()
    if any(k in col_lower for k in ['temp', 'humidity', 'wind', 'pressure']):
        if col not in essential_cols and col not in weather_found:
            weather_found.append(col)
essential_cols.extend(weather_found)

# Add location columns
location_found = []
if location_df is not None:
    for col in combined.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in ['industrial', 'farmland', 'dump', 'road', 'bus']):
            if col not in essential_cols and col not in location_found:
                location_found.append(col)
    essential_cols.extend(location_found)

# Add engineered features
engineered_found = []
for col in ['aqi_category', 'season', 'pollution_severity', 'month']:
    if col in combined.columns:
        engineered_found.append(col)
essential_cols.extend(engineered_found)

# Keep only essential columns (that actually exist)
final_cols = [col for col in essential_cols if col in combined.columns]
final_df = combined[final_cols].copy()

print(f"  Final columns ({len(final_df.columns)}):")
for col in final_df.columns:
    print(f"    • {col}")

# =============================================
# 11. SAVE PROCESSED DATASET
# =============================================
print("\n SAVING PROCESSED DATASET")
print("-" * 40)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = PROCESSED_DIR / f"enviroscan_combined_{timestamp}.csv"
final_df.to_csv(filename, index=False)

# Also save a sample for quick viewing
sample_filename = PROCESSED_DIR / f"enviroscan_sample_{timestamp}.csv"
final_df.head(20).to_csv(sample_filename, index=False)

print(f"   Full dataset: {filename}")
print(f"   Sample: {sample_filename}")

# =============================================
# 12. SUMMARY STATISTICS
# =============================================
print("\n" + "="*60)
print(" PROCESSING COMPLETE - SUMMARY")
print("="*60)
print(f"\n DATASET OVERVIEW:")
print(f"  Total rows: {len(final_df)}")
print(f"  Total columns: {len(final_df.columns)}")
print(f"  Cities covered: {final_df['city'].nunique()}")
if 'area' in final_df.columns:
    print(f"  Areas covered: {final_df['area'].nunique()}")

print(f"\n COLUMNS BY CATEGORY:")
print(f"  Pollutants: {len(pollutants_found)}")
print(f"  Weather: {len(weather_found)}")
print(f"  Location: {len(location_found)}")
print(f"  Engineered: {len(engineered_found)}")

print(f"\n DATA COMPLETENESS:")
for col in final_df.columns[:10]:  # First 10 columns
    pct = (final_df[col].notna().sum() / len(final_df)) * 100
    print(f"  {col}: {pct:.1f}% complete")

print(f"\n CITIES INCLUDED:")
cities_list = final_df['city'].unique().tolist()
print(f"  {', '.join(cities_list[:10])}")
if len(cities_list) > 10:
    print(f"  ... and {len(cities_list)-10} more")

print(f"\n Files saved in: {PROCESSED_DIR}")
print("="*60)