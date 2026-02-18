import pandas as pd
import os

# Folder containing city pollution CSV files
input_folder = "city_pollution"

# Output file
output_file = "Main_Pollution_Dataset_Cleaned.csv"

# Pollutants needed
required_params = ['pm25', 'pm10', 'no2', 'co', 'so2', 'o3']

main_df = pd.DataFrame()

# ✅ Check folder exists
if not os.path.exists(input_folder):
    print(f"❌ Folder '{input_folder}' not found!")
    print("Please create the folder and put city CSV files inside it.")
    exit()

print("⏳ Merging pollution datasets...")

for file in os.listdir(input_folder):

    if file.endswith(".csv"):

        file_path = os.path.join(input_folder, file)
        print("Reading:", file)

        df = pd.read_csv(file_path)

        # Keep only required columns
        df = df[['location_name', 'latitude', 'longitude',
                 'parameter', 'value', 'datetimeUtc']]

        # Filter pollutants
        df = df[df['parameter'].isin(required_params)]

        # Pivot table (convert rows into columns)
        df_pivot = df.pivot_table(
            index=['location_name', 'latitude', 'longitude', 'datetimeUtc'],
            columns='parameter',
            values='value',
            aggfunc='mean'
        ).reset_index()

        # Rename city column
        df_pivot.rename(columns={'location_name': 'city'}, inplace=True)

        # Append into main dataset
        main_df = pd.concat([main_df, df_pivot], ignore_index=True)


print("✅ Merge complete!")

# -------------------------------------------------
# ✅ CLEANING STEP: Replace 0 and Fill Missing Values
# -------------------------------------------------

print("🧹 Cleaning dataset...")

# Replace 0 values with NaN (pollution cannot realistically be exactly 0)
main_df[required_params] = main_df[required_params].replace(0, pd.NA)

# Sort properly before filling
main_df = main_df.sort_values(by=["city", "datetimeUtc"])

# Fill missing values city-wise
for param in required_params:

    # Forward fill (use previous value)
    main_df[param] = main_df.groupby("city")[param].ffill()

    # Backward fill (use next value)
    main_df[param] = main_df.groupby("city")[param].bfill()

    # Final fallback: replace remaining NaN with city mean
    main_df[param] = main_df.groupby("city")[param].transform(
        lambda x: x.fillna(x.mean())
    )

print("✅ Missing values and zeros handled successfully!")

# Save final cleaned dataset
main_df.to_csv(output_file, index=False)

print("✅ Cleaned Pollution Dataset created successfully!")
print("📁 Saved as:", output_file)
