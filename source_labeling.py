import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 

print("Loading Combined Dataset...")
df = pd.read_csv("data/Combined_Dataset.csv")

print("Calculating Dynamic Percentiles to Balance Classes (>1500 Target)...")

# RULE 1: NATURAL DUST
cond_dust = (df['pm10'] > (df['pm25'] * 1.3)) & (df['pm10'] > df['pm10'].quantile(0.60))

# RULE 2: WASTE BURNING
cond_waste = (df['co'] > df['co'].quantile(0.85)) & (df['dist_to_waste_m'] < 4500)

# RULE 3: AGRICULTURAL BURNING
cond_agri = (df['pm25'] > df['pm25'].quantile(0.65)) & (df['dist_to_farm_m'] < 5000)

# RULE 4: INDUSTRIAL
cond_ind = (df['so2'] > df['so2'].quantile(0.60)) & (df['dist_to_industry_m'] < 4000)

# RULE 5: VEHICULAR (OPTIMIZED: Using range instead of manual list)
cond_veh = df['hour'].isin(range(5, 24)) & (df['no2'] > df['no2'].quantile(0.25))

print("Applying Labels in Priority Order...")
conditions = [cond_dust, cond_waste, cond_agri, cond_ind, cond_veh]
choices = [
    'Natural_Dust', 
    'Waste_Burning', 
    'Agricultural_Burning', 
    'Industrial', 
    'Vehicular'
]

df['pollution_source'] = np.select(conditions, choices, default='Background_Mixed')

print("\nFinal Balanced Distribution:")
counts = df['pollution_source'].value_counts()
print(counts)

# Save the final labeled dataset as CSV
csv_output_path = "data/Labeled_Master_Dataset.csv"
df.to_csv(csv_output_path, index=False)
print(f" SUCCESS! Master Answer Key (CSV) generated at: {csv_output_path}")

# Save the final labeled dataset as Excel
excel_output_path = "data/Labeled_Master_Dataset.xlsx"
df.to_excel(excel_output_path, index=False)
print(f" SUCCESS! Master Answer Key (Excel) generated at: {excel_output_path}")

# ==========================================
# 📈 GRAPH GENERATION
# ==========================================
print("\nGenerating Distribution Graph...")

plt.figure(figsize=(10, 6))
colors = ['#A8ADC1', '#D48694', '#99B898', '#FECEAB', '#FF847C', '#E84A5F']
bars = plt.bar(counts.index, counts.values, color=colors[:len(counts)])

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (counts.max() * 0.02), int(yval), ha='center', va='bottom', fontsize=10, fontweight='bold')

# OPTIMIZED: Give the graph a 15% headroom at the top so text never gets cut off
plt.ylim(0, counts.max() * 1.15)

plt.title('Distribution of Pollution Sources', fontsize=14, fontweight='bold')
plt.ylabel('Number of Hourly Records', fontsize=12)
plt.xlabel('Pollution Source', fontsize=12)
plt.xticks(rotation=45, ha='right')

# FIXED: Removed plt.legend() since it was empty
plt.tight_layout()

os.makedirs("visualisation", exist_ok=True) 
graph_path = "visualisation/pollution_source_distribution.png"
plt.savefig(graph_path, dpi=300)

print(f"SUCCESS! Graph visually saved as: {graph_path}")