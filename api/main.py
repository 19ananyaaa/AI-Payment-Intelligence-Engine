from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import shap
import math
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


# -----------------------------
# Request Model
# -----------------------------

class TransactionRequest(BaseModel):
    transaction_id: str
    amount: float
    time: float
    advanced_features: dict = {}


# -----------------------------
# Project Root
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title="AI Payment Risk & Fraud Intelligence API",
    description="AI-powered payment fraud detection and risk scoring system",
    version="1.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Load Model
# -----------------------------

model = joblib.load(
    BASE_DIR / "models" / "fraud_model.pkl"
)


# -----------------------------
# Load Feature Columns
# -----------------------------

feature_columns = joblib.load(
    BASE_DIR / "models" / "feature_columns.pkl"
)


# -----------------------------
# SHAP Explainer
# -----------------------------

explainer = shap.TreeExplainer(model)


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "AI Payment Risk & Fraud Intelligence API is running",
        "status": "active"
    }


# -----------------------------
# Prediction
# -----------------------------

@app.post("/predict")
def predict(transaction: TransactionRequest):

    amount = transaction.amount
    time_value = transaction.time

    # --------------------------------
    # Calculate derived features
    # --------------------------------

    hour = int((time_value / 3600) % 24)

    amount_log = math.log1p(amount)


    # --------------------------------
    # Create V1 - V28
    # --------------------------------

    features = {}

    for i in range(1, 29):

        feature_name = f"V{i}"

        features[feature_name] = float(
            transaction.advanced_features.get(
                feature_name,
                0
            )
        )


    # --------------------------------
    # Add basic + derived features
    # --------------------------------

    features["Time"] = time_value
    features["Amount"] = amount
    features["Hour"] = hour
    features["Amount_Log"] = amount_log


    # --------------------------------
    # Arrange features in exact
    # model column order
    # --------------------------------

    input_data = pd.DataFrame(
        [[features[column] for column in feature_columns]],
        columns=feature_columns
    )


    # --------------------------------
    # Fraud Probability
    # --------------------------------

    fraud_probability = float(
        model.predict_proba(input_data)[0][1]
    )


    # --------------------------------
    # Risk Score
    # --------------------------------

    risk_score = float(
        round(fraud_probability * 100, 2)
    )


    # --------------------------------
    # Risk Classification
    # --------------------------------

    if risk_score < 30:

        risk_level = "LOW"
        recommendation = "APPROVE"

    elif risk_score < 70:

        risk_level = "MEDIUM"
        recommendation = "REVIEW"

    else:

        risk_level = "HIGH"
        recommendation = "BLOCK / MANUAL REVIEW"


    # --------------------------------
    # SHAP Explanation
    # --------------------------------

    shap_values = explainer.shap_values(input_data)

    local_shap = pd.Series(
        shap_values[0],
        index=feature_columns
    )


    # --------------------------------
    # Top 5 Risk Factors
    # --------------------------------

    top_factors = (
        local_shap
        .abs()
        .sort_values(ascending=False)
        .head(5)
    )


    risk_factors = []


    for feature in top_factors.index:

        impact = float(local_shap[feature])

        if impact > 0:

            direction = "increased fraud risk"

        else:

            direction = "reduced fraud risk"


        risk_factors.append({

            "feature": feature,

            "impact": round(
                abs(impact),
                4
            ),

            "direction": direction
        })


    # --------------------------------
    # Response
    # --------------------------------

    return {

        "transaction_id":
            transaction.transaction_id,

        "fraud_probability":
            round(
                fraud_probability,
                4
            ),

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "recommendation":
            recommendation,

        "top_risk_factors":
            risk_factors
    }