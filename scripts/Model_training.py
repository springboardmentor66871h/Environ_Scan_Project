import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

os.environ["LOKY_MAX_CPU_COUNT"] = "2"

df = pd.read_csv(r"C:\Users\admin\Environ_Scan_Project\data\processed\final_labelled_dataset.csv")

target = "pollution_source"

X = df.drop(columns=[target])
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rf_params = {
    "n_estimators": [200, 300, 400],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2]
}

rf_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    rf_params,
    n_iter=5,
    cv=3,
    verbose=1,
    n_jobs=1
)

rf_search.fit(X_train, y_train)
rf_best = rf_search.best_estimator_


rf_preds = rf_best.predict(X_test)


print("\n===== RANDOM FOREST =====")
print("Accuracy:", accuracy_score(y_test, rf_preds))
print(classification_report(y_test, rf_preds))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_preds))

model_path = r"C:\Users\admin\Environ_Scan_Project\model\final_pollution_model.pkl"
joblib.dump(rf_best, model_path)
print(f"\n Random Forest model trained and exported to {model_path}!")
