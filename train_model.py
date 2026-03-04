import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

# ===============================
# 1. Load Dataset
# ===============================
print("Loading dataset...")

data_path = os.path.join("data", "processed", "final_dataset.csv")
df = pd.read_csv(data_path)

print("Dataset Shape:", df.shape)
print("\nColumns:\n", df.columns)

# ===============================
# 2. Create Target Column
# ===============================
print("\nCreating pollution_source column...")

def assign_source(row):
    if row["Nearest_Industry_km"] < 2:
        return "Industrial"
    elif row["Nearest_Farm_km"] < 2:
        return "Agricultural"
    elif row["Nearest_Dump_km"] < 2:
        return "Dump"
    elif row["Nearest_Road_km"] < 2:
        return "Vehicular"
    else:
        return "Natural"

df["pollution_source"] = df.apply(assign_source, axis=1)

print("\nClass Distribution:")
print(df["pollution_source"].value_counts())

# ===============================
# 3. Feature Selection
# ===============================
features = [
    'pollutant_min',
    'pollutant_max',
    'pollutant_avg',
    'Nearest_Road_km',
    'Nearest_Industry_km',
    'Nearest_Dump_km',
    'Nearest_Farm_km'
]

X = df[features]
y = df['pollution_source']

# Remove missing values
# Fill missing values instead of dropping rows
df[features] = df[features].fillna(df[features].median())

X = df[features]
y = df["pollution_source"]


# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ===============================
# 4. Train-Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ===============================
# 5. Train Model
# ===============================
print("\nTraining model...")

model = RandomForestClassifier(
    n_estimators=300,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

# ===============================
# 6. Evaluation
# ===============================
y_pred = model.predict(X_test)

print("\nTesting Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    target_names=le.classes_,
    zero_division=0
))
# ===============================
# 7. Confusion Matrix
# ===============================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=le.classes_,
    yticklabels=le.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

os.makedirs("models", exist_ok=True)
plt.savefig("models/confusion_matrix.png")
plt.close()

print("Confusion matrix saved in models folder!")

# ===============================
# 8. Feature Importance
# ===============================
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:\n")
print(importance_df)

plt.figure(figsize=(6, 4))
sns.barplot(
    x="Importance",
    y="Feature",
    data=importance_df
)

plt.title("Feature Importance")
plt.tight_layout()
plt.savefig("models/feature_importance.png")
plt.close()

print("Feature importance plot saved!")

# ===============================
# 9. Save Model
# ===============================
joblib.dump(model, "models/pollution_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("Model saved successfully!")