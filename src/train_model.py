import math
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
)

from xgboost import XGBClassifier


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "creditcard.csv"
MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "feature_columns.pkl"


# ============================================================
# Load dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# Feature engineering
# ============================================================

df["Hour"] = (df["Time"] // 3600) % 24
df["Amount_Log"] = np.log1p(df["Amount"])


# ============================================================
# Prepare features and target
# ============================================================

X = df.drop("Class", axis=1)
y = df["Class"]

feature_columns = X.columns.tolist()


# ============================================================
# Train-test split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)
print("Fraud in training:", y_train.sum())
print("Fraud in testing:", y_test.sum())


# ============================================================
# Handle class imbalance
# ============================================================

scale_pos_weight = (
    y_train.value_counts()[0] /
    y_train.value_counts()[1]
)

print(
    "\nScale Pos Weight:",
    scale_pos_weight
)


# ============================================================
# Create XGBoost model
# ============================================================

xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    objective="binary:logistic",
    eval_metric="aucpr",
    random_state=42,
    n_jobs=-1
)


# ============================================================
# Train model
# ============================================================

print("\nTraining XGBoost model...")

xgb_model.fit(
    X_train,
    y_train
)

print("XGBoost model trained successfully!")


# ============================================================
# Predictions
# ============================================================

xgb_pred = xgb_model.predict(X_test)
xgb_prob = xgb_model.predict_proba(X_test)[:, 1]


# ============================================================
# Classification metrics
# ============================================================

print("\n" + "=" * 60)
print("XGBoost Classification Report")
print("=" * 60)

print(
    classification_report(
        y_test,
        xgb_pred
    )
)

roc_auc = roc_auc_score(
    y_test,
    xgb_prob
)

pr_auc = average_precision_score(
    y_test,
    xgb_prob
)

print("ROC-AUC:", round(roc_auc, 6))
print("PR-AUC:", round(pr_auc, 6))


# ============================================================
# Confusion Matrix
# ============================================================

cm = confusion_matrix(
    y_test,
    xgb_pred
)

TN, FP, FN, TP = cm.ravel()

print("\nConfusion Matrix:")
print(cm)

print("\nTN:", TN)
print("FP:", FP)
print("FN:", FN)
print("TP:", TP)


# ============================================================
# False Positive Analysis
# ============================================================

false_positive_rate = FP / (FP + TN)

# Assumed evaluation cost per false positive
false_positive_cost_per_transaction = 100

total_false_positive_cost = (
    FP * false_positive_cost_per_transaction
)

print("\n" + "=" * 60)
print("False Positive Analysis")
print("=" * 60)

print(
    "False Positive Rate (FPR):",
    round(false_positive_rate * 100, 4),
    "%"
)

print(
    "False Positives:",
    FP
)

print(
    "Assumed Cost per False Positive: ₹",
    false_positive_cost_per_transaction
)

print(
    "Estimated False Positive Cost: ₹",
    total_false_positive_cost
)


# ============================================================
# Save model
# ============================================================

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    xgb_model,
    MODEL_PATH
)

joblib.dump(
    feature_columns,
    FEATURES_PATH
)

print("\n" + "=" * 60)
print("Model saved successfully!")
print("Model:", MODEL_PATH)
print("Features:", FEATURES_PATH)
print("=" * 60)