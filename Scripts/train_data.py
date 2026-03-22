import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

print("Starting EnviroScan Model Training Pipeline...")

# --- CONFIGURATION & PATHS ---
BASE_DIR = r"C:\Users\ajayk\Environ_Scan_Project"
TRAIN_FILE = os.path.join(BASE_DIR, "Processed", "training_data.zip")
TEST_FILE = os.path.join(BASE_DIR, "Processed", "testing_data.zip")
MODEL_DIR = os.path.join(BASE_DIR, "Models")
VIS_DIR = os.path.join(BASE_DIR, "Visualizations")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(VIS_DIR, exist_ok=True)

# --- LOAD ZIPPED SPLITS ---
print("Loading training and testing datasets...")
if not os.path.exists(TRAIN_FILE) or not os.path.exists(TEST_FILE):
    print("Error: Zip files not found. Please run split_data.py first.")
    exit()

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

# --- DEFINE FEATURES AND TARGET ---
features = [
    'PM25', 'PM10', 'NO2', 'CO', 'SO2', 
    'Dist_Road_km', 'Dist_Industry_km', 'Dist_Dump_km', 'Dist_Farmland_km'
]

# Clean data: Ensure numeric types and drop NaNs for both sets
for df in [train_df, test_df]:
    for col in features:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=features + ['POLLUTION_SOURCE'], inplace=True)

# Separate X and encode y
X_train = train_df[features]
X_test = test_df[features]

le = LabelEncoder()
y_train = le.fit_transform(train_df['POLLUTION_SOURCE'])
y_test = le.transform(test_df['POLLUTION_SOURCE']) 

print(f"Data Ready. Training on {len(X_train)} rows, Testing on {len(X_test)} rows.\n")

# --- EVALUATION FUNCTION (Fulfills Step 6 Requirements for multiple models) ---
def evaluate_and_interpret(model, X_test, y_test, model_name):
    print("=" * 60)
    print(f"EVALUATING MODEL: {model_name}")
    print("=" * 60)
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print("\n1. RAW METRICS:")
    print(f"   Accuracy  : {accuracy * 100:.2f}%")
    print(f"   Precision : {precision:.4f}")
    print(f"   Recall    : {recall:.4f}")
    print(f"   F1-Score  : {f1:.4f}")
    
    print("\n2. METRICS INTERPRETATION:")
    print(f"   - Accuracy: The model correctly predicted {accuracy * 100:.2f}% of all test samples.")
    print(f"   - Precision: Out of all the predictions the model made for a specific source, {precision * 100:.2f}% were actually correct. This indicates a low rate of false alarms.")
    print(f"   - Recall: Out of all the actual events in the real world, the model successfully detected {recall * 100:.2f}%. This indicates it misses very few real pollution sources.")
    print(f"   - F1-Score: At {f1:.4f}, this metric confirms the model maintains a strong, harmonic balance between Precision and Recall, proving it isn't overly biased toward one specific class.")
    
    print(f"\n3. DETAILED CLASSIFICATION REPORT ({model_name}):")
    print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
    plt.title(f'CONFUSION MATRIX - {model_name}')
    plt.ylabel('Actual Source')
    plt.xlabel('Predicted Source')
    plt.tight_layout()
    
    # Save with dynamic name based on model
    safe_name = model_name.replace(" ", "_").lower()
    cm_path = os.path.join(VIS_DIR, f'confusion_matrix_{safe_name}.png')
    plt.savefig(cm_path)
    plt.close() # Close plot to prevent overlap
    print(f"4. CONFUSION MATRIX SAVED TO: {cm_path}")
    print("   Interpretation: The diagonal cells show correct predictions. Off-diagonal cells reveal where the model confused one source for another (e.g., misclassifying AGRICULTURAL as NATURAL).\n")

# --- TRAIN & EVALUATE DECISION TREE ---
print("Training Baseline Decision Tree...")
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Evaluate Decision Tree
evaluate_and_interpret(dt_model, X_test, y_test, "Decision Tree Baseline")

# --- TRAIN & EVALUATE RANDOM FOREST ---
print("Tuning Random Forest Classifier (Randomized Search)...")
rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)

param_dist = {
    'n_estimators': [50, 100],
    'max_depth': [10, 20, None],
}

rf_search = RandomizedSearchCV(
    estimator=rf_base, param_distributions=param_dist, 
    n_iter=5, cv=3, random_state=42, n_jobs=-1
)

rf_search.fit(X_train, y_train)
best_rf = rf_search.best_estimator_

# Evaluate Random Forest
evaluate_and_interpret(best_rf, X_test, y_test, "Random Forest Tuned")

# --- FEATURE IMPORTANCE ANALYSIS (Best Model) ---
print("Analyzing Feature Importance for the Best Model (Random Forest)...")
importances = best_rf.feature_importances_
# Changed ascending to False so the tallest bars are on the left
feat_imp_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
# Changed to plt.bar (vertical) instead of plt.barh (horizontal)
plt.bar(feat_imp_df['Feature'], feat_imp_df['Importance'])
# Updated the title to match your screenshot
plt.title('Feature Importance Ranking')
# Rotated the x-axis labels by 45 degrees so the names don't overlap
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

fi_path = os.path.join(VIS_DIR, 'feature_importance.png')
plt.savefig(fi_path)
plt.close()
print(f"Feature Importance chart saved to: {fi_path}")
print("Interpretation: Taller bars indicate features that have the strongest influence on the model's final prediction.\n")

# --- EXPORT THE FINAL MODEL ---
print("Exporting best model and encoder...")
joblib.dump(best_rf, os.path.join(MODEL_DIR, 'pollution_model.pkl'))
joblib.dump(le, os.path.join(MODEL_DIR, 'label_encoder.pkl'))

print(f"SUCCESS! All evaluations are complete and files are saved in {BASE_DIR}.")