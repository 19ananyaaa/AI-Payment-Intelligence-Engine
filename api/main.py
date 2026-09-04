from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import shap
import math
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


class TransactionRequest(BaseModel):
    transaction_id: str = Field(
        description="Demo transaction ID, e.g. TXN-000001"
    )


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "feature_columns.pkl"
DATA_PATH = BASE_DIR / "data" / "creditcard.csv"


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Payment Risk & Fraud Intelligence API",
    description="AI-powered payment fraud detection and risk scoring system",
    version="1.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# LOAD MODEL AND DATA
# =========================================================

model = joblib.load(MODEL_PATH)

feature_columns = joblib.load(FEATURES_PATH)

dataset = pd.read_csv(DATA_PATH)

explainer = shap.TreeExplainer(model)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI Payment Risk & Fraud Intelligence API is running",
        "status": "active",
        "model_features": len(feature_columns),
        "dataset_transactions": len(dataset)
    }


# =========================================================
# PREDICT
# =========================================================

@app.post("/predict")
def predict(transaction: TransactionRequest):

    transaction_id = transaction.transaction_id.strip()

    # -----------------------------------------------------
    # Validate transaction ID
    # -----------------------------------------------------

    if not transaction_id:

        raise HTTPException(
            status_code=400,
            detail="Transaction ID is required."
        )


    if not transaction_id.upper().startswith("TXN-"):

        raise HTTPException(
            status_code=400,
            detail="Transaction ID must be in format TXN-000001."
        )


    try:

        row_number = int(
            transaction_id.upper().replace("TXN-", "")
        ) - 1

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Invalid Transaction ID. Example: TXN-000001."
        )


    # -----------------------------------------------------
    # Check transaction exists
    # -----------------------------------------------------

    if row_number < 0 or row_number >= len(dataset):

        raise HTTPException(
            status_code=404,
            detail=(
                f"Transaction not found. "
                f"Valid range: TXN-000001 to TXN-{len(dataset):06d}."
            )
        )


    # -----------------------------------------------------
    # Get REAL transaction from CSV
    # -----------------------------------------------------

    transaction_row = dataset.iloc[row_number]


    # -----------------------------------------------------
    # Build model features
    # -----------------------------------------------------

    features = {}

    for column in feature_columns:

        if column == "Hour":

            features[column] = int(
                (float(transaction_row["Time"]) / 3600) % 24
            )

        elif column == "Amount_Log":

            features[column] = math.log1p(
                float(transaction_row["Amount"])
            )

        else:

            features[column] = float(
                transaction_row[column]
            )


    # -----------------------------------------------------
    # Create model input
    # -----------------------------------------------------

    input_data = pd.DataFrame(
        [[
            features[column]
            for column in feature_columns
        ]],
        columns=feature_columns
    )


    # -----------------------------------------------------
    # Fraud probability
    # -----------------------------------------------------

    fraud_probability = float(
        model.predict_proba(input_data)[0][1]
    )


    # -----------------------------------------------------
    # Risk score
    # -----------------------------------------------------

    risk_score = float(
        round(
            fraud_probability * 100,
            2
        )
    )


    # -----------------------------------------------------
    # Risk level
    # -----------------------------------------------------

    if risk_score < 30:

        risk_level = "LOW"
        recommendation = "APPROVE"

    elif risk_score < 70:

        risk_level = "MEDIUM"
        recommendation = "REVIEW"

    else:

        risk_level = "HIGH"
        recommendation = "BLOCK / MANUAL REVIEW"


    # -----------------------------------------------------
    # SHAP explanation
    # -----------------------------------------------------

    shap_values = explainer.shap_values(input_data)

    local_shap = pd.Series(
        shap_values[0],
        index=feature_columns
    )


    top_factors = (
        local_shap
        .abs()
        .sort_values(ascending=False)
        .head(5)
    )


    # -----------------------------------------------------
    # Risk factors
    # -----------------------------------------------------

    risk_factors = []

    for feature in top_factors.index:

        impact = float(
            local_shap[feature]
        )

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


    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------

    return {

        "transaction_id":
            transaction_id,

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