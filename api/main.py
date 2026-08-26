from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
import shap
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
class TransactionRequest(BaseModel):
    transaction_id: str
    features: List[float]

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Create FastAPI app
app = FastAPI(
    title="AI Payment Risk & Fraud Intelligence API",
    description="AI-powered payment fraud detection and risk scoring system",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load trained model
model = joblib.load(
    BASE_DIR / "models" / "fraud_model.pkl"
)

# Load feature list
feature_columns = joblib.load(
    BASE_DIR / "models" / "feature_columns.pkl"
)
# Create SHAP explainer
explainer = shap.TreeExplainer(model)


@app.get("/")
def home():
    return {
        "message": "AI Payment Risk & Fraud Intelligence API is running",
        "status": "active"
    }


@app.post("/predict")
def predict(transaction: TransactionRequest):

    # Convert incoming features into DataFrame
    input_data = pd.DataFrame(
        [transaction.features],
        columns=feature_columns
    )

    fraud_probability = float(
        model.predict_proba(input_data)[0][1]
    )

    risk_score = float(
        round(fraud_probability * 100, 2)
    )

    if risk_score < 30:
        risk_level = "LOW"
        recommendation = "APPROVE"

    elif risk_score < 70:
        risk_level = "MEDIUM"
        recommendation = "REVIEW"

    else:
        risk_level = "HIGH"
        recommendation = "BLOCK / MANUAL REVIEW"

    shap_values = explainer.shap_values(input_data)

    # SHAP values for this transaction
    local_shap = pd.Series(
        shap_values[0],
        index=feature_columns
    )

    # Top 5 most influential features
    top_factors = (
        local_shap
        .abs()
        .sort_values(ascending=False)
        .head(5)
    )

    # Create readable explanations
    risk_factors = []

    for feature in top_factors.index:

        impact = float(local_shap[feature])

        if impact > 0:
            direction = "increased fraud risk"
        else:
            direction = "reduced fraud risk"

        risk_factors.append({
            "feature": feature,
            "impact": round(abs(impact), 4),
            "direction": direction
        })

    return {
    "transaction_id": transaction.transaction_id,
    "fraud_probability": round(fraud_probability, 4),
    "risk_score": risk_score,
    "risk_level": risk_level,
    "recommendation": recommendation,
    "top_risk_factors": risk_factors
}