import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# --------------------------------------------------
# Paths
# --------------------------------------------------
DATA_PATH = r"D:\ENVIRON-SCAN\data\processed\final_dataset.csv"
MODEL_DIR = r"D:\ENVIRON-SCAN\models"
CONF_MATRIX_PATH = r"D:\ENVIRON-SCAN\data\processed\confusion_matrix.png"
FEATURE_IMPORTANCE_PATH = r"D:\ENVIRON-SCAN\data\processed\feature_importance.png"

os.makedirs(MODEL_DIR, exist_ok=True)

# --------------------------------------------------
# Step 1: Load Dataset
# --------------------------------------------------
df = pd.read_csv(DATA_PATH)
print("Initial dataset shape:", df.shape)

# Drop missing values (safe – only 2 rows)
if df.isnull().sum().sum() > 0:
    print("Missing values detected. Dropping rows...")
    df = df.dropna()

print("Final dataset shape:", df.shape)

if "pollution_source" not in df.columns:
    raise ValueError("Target column 'pollution_source' not found!")

# --------------------------------------------------
# Step 2: Define Features and Target
# --------------------------------------------------
X = df.drop(columns=["pollution_source", "timestamp", "city"])
y = df["pollution_source"]

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# --------------------------------------------------
# Step 3: Train-Test Split
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("Train size:", X_train.shape[0])
print("Test size:", X_test.shape[0])

# --------------------------------------------------
# Step 4: Train Models
# --------------------------------------------------

# 1️⃣ Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt_params = {
    "max_depth": [5, 10, 15, None],
    "min_samples_split": [2, 5, 10]
}
dt_grid = GridSearchCV(dt, dt_params, cv=5, scoring="f1_weighted")
dt_grid.fit(X_train, y_train)

# 2️⃣ Random Forest
rf = RandomForestClassifier(random_state=42)
rf_params = {
    "n_estimators": [100, 200],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5]
}
rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring="f1_weighted")
rf_grid.fit(X_train, y_train)

# 3️⃣ XGBoost
xgb = XGBClassifier(
    random_state=42,
    eval_metric="mlogloss"
)
xgb_params = {
    "n_estimators": [100, 200],
    "max_depth": [3, 6, 10],
    "learning_rate": [0.01, 0.1]
}
xgb_grid = GridSearchCV(xgb, xgb_params, cv=5, scoring="f1_weighted")
xgb_grid.fit(X_train, y_train)

# --------------------------------------------------
# Step 5: Select Best Model
# --------------------------------------------------
models = {
    "Decision Tree": dt_grid,
    "Random Forest": rf_grid,
    "XGBoost": xgb_grid
}

best_model_name = max(models, key=lambda k: models[k].best_score_)
best_model = models[best_model_name].best_estimator_

print("\nBest Model Selected:", best_model_name)

# --------------------------------------------------
# Step 6: Evaluate on Test Set
# --------------------------------------------------
y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nTest Accuracy:", round(accuracy, 4))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d",
            xticklabels=le.classes_,
            yticklabels=le.classes_,
            cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig(CONF_MATRIX_PATH)
plt.close()

print("Confusion matrix saved.")

# --------------------------------------------------
# Step 7: Feature Importance
# --------------------------------------------------
if hasattr(best_model, "feature_importances_"):
    importances = best_model.feature_importances_
    features = X.columns

    imp_df = pd.DataFrame({
        "Feature": features,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10,6))
    plt.barh(imp_df["Feature"], imp_df["Importance"])
    plt.gca().invert_yaxis()
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_PATH)
    plt.close()

    print("Feature importance plot saved.")

# --------------------------------------------------
# Step 8: Save Model
# --------------------------------------------------
joblib.dump({
    "model": best_model,
    "label_encoder": le
}, os.path.join(MODEL_DIR, "best_model.joblib"))

print("\nModel saved successfully in models folder.")
print("Week 4 Model Training Complete.")