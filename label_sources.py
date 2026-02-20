import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import zipfile

# --- CONFIGURATION ---
INPUT_FILE_1 = "data/processed/india_part1.zip"
INPUT_FILE_2 = "data/processed/india_part2.zip"
OUTPUT_DIR = "data/processed"

print("⏳ Loading data parts...")
df1 = pd.read_csv(INPUT_FILE_1)
df2 = pd.read_csv(INPUT_FILE_2)
df = pd.concat([df1, df2], ignore_index=True)
print(f"✅ Loaded {len(df)} rows.")

print("🧠 Calculating sensitive dynamic thresholds for labeling...")
# lowered from 60th percentile to 35th/40th to capture more data
no2_high = df['no2'].quantile(0.35)  
so2_high = df['so2'].quantile(0.35)  
pm10_high = df['pm10'].quantile(0.40) 
pm25_high = df['pm25'].quantile(0.40) 

# Raised the "low" thresholds so more data passes the check
pm25_low = df['pm25'].quantile(0.60)  
no2_low = df['no2'].quantile(0.60)    

print("🏷️ Applying Expanded Rule-Based Heuristics...")
df['pollution_source'] = 'Mixed/Unknown'

# 1. Vehicular: Moderate/High NO2 + Wider road radius (< 700m)
cond_vehicular = (df['no2'] >= no2_high) & (df['distance_to_road'] <= 700)

# 2. Industrial: Moderate/High SO2 + Wider industry radius (< 4500m)
cond_industrial = (df['so2'] >= so2_high) & (df['distance_to_industry'] <= 4500)

# 3. Agricultural: Moderate/High PM10 + Low NO2 + Wider farm radius (< 3500m)
cond_agri = (df['pm10'] >= pm10_high) & (df['no2'] <= no2_low) & (df['distance_to_farmland'] <= 3500)

# 4. Burning: Moderate/High PM25 + Wider dump radius (< 8000m)
cond_burning = (df['pm25'] >= pm25_high) & (df['distance_to_dump'] <= 8000)

# 5. Natural: Moderate PM10 + Lower PM25
cond_natural = (df['pm10'] >= pm10_high) & (df['pm25'] <= pm25_low)

# Apply labels (Priority matters - Natural gets overwritten by more specific sources if they overlap)
df.loc[cond_natural, 'pollution_source'] = 'Natural'
df.loc[cond_agri, 'pollution_source'] = 'Agricultural'
df.loc[cond_burning, 'pollution_source'] = 'Burning'
df.loc[cond_industrial, 'pollution_source'] = 'Industrial'
df.loc[cond_vehicular, 'pollution_source'] = 'Vehicular'

# Validation: Check Distribution
dist = df['pollution_source'].value_counts()
percentages = (dist / len(df)) * 100

print("\n📊 Final Label Distribution (Counts & Percentages):")
for idx, val in dist.items():
    print(f"{idx}: {val} ({percentages[idx]:.1f}%)")

# Plot and Save Bar Chart
plt.figure(figsize=(10,6))
ax = dist.plot(kind='bar', color=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6', '#95a5a6'])
plt.title('Simulated Pollution Source Distribution (EnviroScan)')
plt.ylabel('Number of Records')

# Add percentage labels on top of each bar
for p in ax.patches:
    height = p.get_height()
    percentage = f'{(height/len(df))*100:.1f}%'
    ax.annotate(percentage, 
                (p.get_x() + p.get_width() / 2., height), 
                ha='center', va='bottom', 
                fontsize=10, color='black', xytext=(0, 2), 
                textcoords='offset points')

plt.xticks(rotation=45)
plt.tight_layout()
chart_path = os.path.join(OUTPUT_DIR, 'source_distribution.png')
plt.savefig(chart_path)
print(f"✅ Bar chart saved to: {chart_path}")

# Split and Save Labeled Data
print("\n✂️ Splitting labeled data to fit GitHub limits...")
chunk_size = int(len(df) / 2) + 1
df_part1 = df.iloc[:chunk_size]
df_part2 = df.iloc[chunk_size:]

file1 = os.path.join(OUTPUT_DIR, "labeled_india_part1.csv")
file2 = os.path.join(OUTPUT_DIR, "labeled_india_part2.csv")

df_part1.to_csv(file1, index=False)
df_part2.to_csv(file2, index=False)

def zip_file(csv_path):
    zip_name = csv_path.replace(".csv", ".zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=os.path.basename(csv_path))
    os.remove(csv_path)

zip_file(file1)
zip_file(file2)

print("✅ SUCCESS! Labeled datasets saved as zipped files.")