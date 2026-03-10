import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("--- Step 1: Loading Dataset ---")
df = pd.read_csv("data/processed/labeled_environment_dataset.csv")

# We need to convert the text-based 'pollutant' column (e.g., 'pm25') into numbers for the AI
le_pollutant = LabelEncoder()
df['pollutant_encoded'] = le_pollutant.fit_transform(df['pollutant'])

# We also need to convert our target labels (Vehicular, Industrial, etc.) into numbers
le_target = LabelEncoder()
df['target_encoded'] = le_target.fit_transform(df['pollution_source'])

print("--- Step 2: Defining Features (X) and Target (y) ---")
# These are the exact features requested by the mentor
features = [
    'pollutant_encoded', 'value', # The specific pollutant and its concentration level
    'temperature', 'humidity', 'wind_speed', 'wind_direction', # Weather
    'distance_to_road_m', 'distance_to_industry_m', 'distance_to_dump_m', 'distance_to_farmland_m' # Proximity
]

X = df[features]
y = df['target_encoded']

print("--- Step 3: Train-Test Split ---")
# 80% Training data, 20% Testing data with a fixed random_state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
print(f"Training on {len(X_train)} rows, Testing on {len(X_test)} rows.")

print("\n--- Step 4 & 5: Training & Tuning Models ---")
print("Training Model 1: XGBoost (Baseline)...")
xgb_model = XGBClassifier(random_state=42, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)
print(f"XGBoost Baseline Accuracy: {xgb_acc * 100:.2f}%")

print("\nTraining Model 2: Random Forest (with GridSearchCV)...")
# We use GridSearchCV to find the absolute best settings (hyperparameters) for the Random Forest
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [10, 20, None]
}
rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)

best_rf = grid_search.best_estimator_
rf_pred = best_rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

print(f"Random Forest Best Parameters: {grid_search.best_params_}")
print(f"Random Forest Tuned Accuracy: {rf_acc * 100:.2f}%")

# Select the best model (Usually Random Forest wins on this type of rule-based data)
final_model = best_rf if rf_acc >= xgb_acc else xgb_model
print(f"\nSelected Best Model: {type(final_model).__name__}")

print("\n--- Step 6: Model Evaluation ---")
y_pred = final_model.predict(X_test)

# Mentor requested Accuracy, Precision, Recall, and F1-Score (classification_report does all of this!)
target_names = le_target.classes_
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_names))

# Create Confusion Matrix Plot
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.title('Confusion Matrix - Pollution Source Prediction')
plt.ylabel('Actual Source')
plt.xlabel('Predicted Source')
plt.tight_layout()
os.makedirs("data/processed", exist_ok=True)
plt.savefig("data/processed/confusion_matrix.png")
print("Saved Confusion Matrix to data/processed/confusion_matrix.png")

print("\n--- Step 7: Feature Importance Analysis ---")
# Extract feature importance to see what the AI thinks is most important
importances = final_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center", color='teal')
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=45, ha='right')
plt.tight_layout()
plt.savefig("data/processed/feature_importance.png")
print("Saved Feature Importance Chart to data/processed/feature_importance.png")

print("\n--- Step 8: Export the Final Model ---")
os.makedirs("models", exist_ok=True)
# We must save the model AND the encoders so the dashboard knows how to read the text later!
joblib.dump(final_model, "models/pollution_source_model.pkl")
joblib.dump(le_pollutant, "models/pollutant_encoder.pkl")
joblib.dump(le_target, "models/target_encoder.pkl")

print("SUCCESS: Model and Encoders saved to the 'models/' folder.") 
print("Week 4 (Model Training) is 100% COMPLETE!")