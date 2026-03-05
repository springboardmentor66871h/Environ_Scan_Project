import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# Load Dataset
# -----------------------------
file_path = "../data/processed/final_labeled_dataset.csv"
df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)

# -----------------------------
# Validate Dataset
# -----------------------------
print("\nMissing Values:\n", df.isnull().sum())
print("\nClass Distribution:\n", df['pollution_source'].value_counts())

# Drop missing values if any
df = df.dropna()

# -----------------------------
# Define Features & Target
# -----------------------------
features = [
    'pm2_5', 'pm10', 'no2', 'co', 'so2', 'o3',
    'temperature', 'humidity', 'wind_speed', 'wind_direction',
    'nearest_feature_distance_m'
]

X = df[features]
y = df['pollution_source']

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Size:", X_train.shape)
print("Testing Size:", X_test.shape)

# -----------------------------
# Model 1: Decision Tree
# -----------------------------
dt = DecisionTreeClassifier(random_state=42)

dt_params = {
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

dt_grid = GridSearchCV(dt, dt_params, cv=5, scoring='f1_weighted')
dt_grid.fit(X_train, y_train)

best_dt = dt_grid.best_estimator_

# -----------------------------
# Model 2: Random Forest
# -----------------------------
rf = RandomForestClassifier(random_state=42)

rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}

rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring='f1_weighted')
rf_grid.fit(X_train, y_train)

best_rf = rf_grid.best_estimator_

# -----------------------------
# Evaluate Models
# -----------------------------
def evaluate_model(model, name):
    print(f"\n===== {name} Evaluation =====")
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    print("Train Accuracy:", accuracy_score(y_train, y_train_pred))
    print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
    
    print("\nClassification Report (Test):")
    print(classification_report(y_test, y_test_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_test_pred))

evaluate_model(best_dt, "Decision Tree")
evaluate_model(best_rf, "Random Forest")

# -----------------------------
# Select Best Model (Based on Test Accuracy)
# -----------------------------
dt_test_acc = accuracy_score(y_test, best_dt.predict(X_test))
rf_test_acc = accuracy_score(y_test, best_rf.predict(X_test))

if rf_test_acc >= dt_test_acc:
    final_model = best_rf
    model_name = "random_forest_model.joblib"
else:
    final_model = best_dt
    model_name = "decision_tree_model.joblib"

# -----------------------------
# Save Final Model
# -----------------------------
os.makedirs("../models", exist_ok=True)
model_path = f"../models/{model_name}"
joblib.dump(final_model, model_path)

print(f"\nFinal model saved at: {model_path}")

# -----------------------------
# Feature Importance
# -----------------------------
importances = final_model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importance:\n", importance_df)

# Plot Feature Importance
os.makedirs("../outputs", exist_ok=True)

plt.figure()
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.gca().invert_yaxis()
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig("../outputs/feature_importance.png")

print("\nFeature importance plot saved in outputs folder.")