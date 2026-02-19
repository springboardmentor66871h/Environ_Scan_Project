import matplotlib.pyplot as plt
import pandas as pd

file_path = r"D:\ENVIRON-SCAN\data\processed\final_dataset.csv"
df = pd.read_csv(file_path)

counts = df["pollution_source"].value_counts()

plt.figure(figsize=(8,5))
counts.plot(kind="bar")
plt.title("Pollution Source Distribution")
plt.xlabel("Source")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(r"D:\ENVIRON-SCAN\data\processed\label_distribution.png")
plt.show()

print("Label distribution plot saved.")
