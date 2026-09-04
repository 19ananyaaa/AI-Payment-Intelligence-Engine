# AI Payment Intelligence Engine

An AI-powered fintech risk intelligence system for detecting potentially fraudulent payment transactions, calculating transaction risk, and providing explainable risk factors using Machine Learning, XGBoost, and SHAP.

## 🚀 Live Demo

**Dashboard:**  
https://ai-payment-intelligence-engine-1.onrender.com

**API Documentation:**  
https://ai-payment-intelligence-api.onrender.com/docs

---

## 📌 Project Overview

The AI Payment Intelligence Engine is an end-to-end machine learning system designed to assess payment transaction risk.

For each analyzed transaction, the system generates:

- Fraud probability
- Risk score
- Risk level
- Recommended action
- Top contributing risk factors
- SHAP-based explainable AI insights
- Audit trail of the risk decision

The project focuses on **defensive fraud detection and payment risk assessment**.

---

## ⚙️ How It Works

1. User enters a demo Transaction ID.
2. The FastAPI backend validates the Transaction ID.
3. The ID is mapped to a transaction in the reference dataset.
4. The real transaction features are retrieved from the dataset.
5. Derived features such as `Hour` and `Amount_Log` are calculated.
6. The trained XGBoost model predicts the probability of fraud.
7. The probability is converted into a 0–100 risk score.
8. The transaction is classified as LOW, MEDIUM, or HIGH risk.
9. SHAP identifies the most influential features behind the prediction.
10. The decision and explanation are recorded in an audit log.
11. The final risk assessment is returned to the frontend dashboard.

---

## 🧠 Machine Learning

The project uses an **XGBoost Classifier** for binary fraud detection.

### Model Features

The model uses 32 features:

- `Time`
- `V1` to `V28`
- `Amount`
- `Hour`
- `Amount_Log`

`Hour` and `Amount_Log` are derived during feature engineering.

### Dataset

The original dataset contains:

- **284,807 transactions**
- **492 fraudulent transactions**
- **30 original transaction features**
- Highly imbalanced fraud distribution

The project uses stratified train-test splitting to preserve the fraud distribution in both training and testing data.

---

## 📊 Model Performance

The model was evaluated on a **held-out test set** that was not used during training.

| Metric | Score |
|--------|-------|
| Accuracy | 99.95% |
| Precision | 85.26% |
| Recall | 82.65% |
| F1-Score | 83.94% |
| ROC-AUC | 0.983 |
| PR-AUC | 0.880 |

### Confusion Matrix

```text
                    Predicted
                 Normal   Fraud

Actual Normal     56850      14
Actual Fraud         17      81
```

The model detected **81 of 98 fraudulent transactions** in the held-out test set while producing **14 false positives**.

---

## 💰 False Positive Analysis

False positives are important in payment risk systems because incorrectly flagging legitimate transactions can create unnecessary review or customer friction.

The model produced:

- **False Positives:** 14
- **False Positive Rate:** 0.0246%
- **Assumed evaluation cost per false positive:** ₹100
- **Estimated false-positive cost:** ₹1,400

> The ₹100 cost is an evaluation assumption used to quantify operational impact. It is not a claim about an actual Razorpay or business cost.

---

## 🎯 Risk Classification

The model's fraud probability is converted into a risk score from 0 to 100.

| Risk Score | Risk Level | Recommendation |
|------------|------------|----------------|
| < 30 | LOW | APPROVE |
| 30–69.99 | MEDIUM | REVIEW |
| ≥ 70 | HIGH | BLOCK / MANUAL REVIEW |

These thresholds are application-level decision thresholds used by the demo risk engine.

---

## 🔍 Explainable AI

**SHAP (SHapley Additive exPlanations)** is used to explain individual model predictions.

For every analyzed transaction, the system identifies the **top 5 most influential features**.

Each factor is classified as:

- Increased fraud risk
- Reduced fraud risk

This provides visibility into the model's reasoning instead of returning only a fraud probability.

---

## 🧾 Audit Trail

The backend records each completed risk assessment in a local JSON Lines audit log.

Each audit record contains:

- Timestamp
- Transaction ID
- Fraud probability
- Risk score
- Risk level
- Recommendation
- Top SHAP risk factors

Example:

```text
{
  "timestamp": "...",
  "transaction_id": "TXN-000542",
  "fraud_probability": 0.998,
  "risk_score": 99.8,
  "risk_level": "HIGH",
  "recommendation": "BLOCK / MANUAL REVIEW",
  "top_risk_factors": [...]
}
```

The generated `audit_log.jsonl` file is intentionally excluded from version control.

> The current audit trail is designed for portfolio/demo use. It uses local runtime storage and is not a persistent production audit database.

---

## 🖥️ Features

- AI-based fraud detection
- Transaction risk scoring
- Fraud probability estimation
- LOW / MEDIUM / HIGH risk classification
- Automated risk recommendation
- SHAP-based explainability
- Top 5 risk factors
- False-positive analysis
- Decision audit trail
- FastAPI REST API
- Responsive fintech dashboard
- Cloud deployment using Render
- Reproducible model training pipeline

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Frontend Dashboard
  │
  │ Transaction ID
  ▼
FastAPI Backend
  │
  ├── Transaction Validation
  │
  ├── Demo Transaction Dataset
  │
  └── Feature Preparation
  │
  ▼
XGBoost Fraud Detection Model
  │
  ├── Fraud Probability
  ├── Risk Score
  └── Risk Level
  │
  ▼
SHAP Explainability
  │
  ▼
Top Risk Factors
  │
  ▼
Risk Recommendation
  │
  ├── Audit Trail
  │
  ▼
Frontend Dashboard
```

---

## 📊 Dataset

The project is based on a credit card fraud detection dataset containing:

- 284,807 transactions
- 492 fraudulent transactions
- 30 original transaction features
- Highly imbalanced fraud distribution

The full dataset is used for model development and training.

The complete `creditcard.csv` file is **not stored in the GitHub repository** because of its large size.

For the deployed application, an authentic subset of the original dataset is included:

```text
data/demo_transactions.csv
```

This allows the deployed API to perform genuine model inference without storing the complete training dataset in the repository.

---

## 🧪 Demo Transaction IDs

The deployed application uses demo/reference transaction IDs such as:

```text
TXN-000001
TXN-000542
```

These IDs are created for this portfolio project.

They map to rows in the reference dataset and **are not real banking transaction identifiers**.

For example:

- `TXN-000001` can be used to test a low-risk transaction.
- `TXN-000542` can be used to test a high-risk transaction.

The Transaction ID is only used to locate the corresponding reference transaction. The ML model performs inference using the actual transaction features.

---

## 🔗 API Endpoints

The backend is built using FastAPI.

### Health Check

```text
GET /
```

Checks whether the API service is running.

### Fraud Prediction

```text
POST /predict
```

Example request:

```json
{
  "transaction_id": "TXN-000542"
}
```

Example response:

```json
{
  "transaction_id": "TXN-000542",
  "fraud_probability": 0.998,
  "risk_score": 99.8,
  "risk_level": "HIGH",
  "recommendation": "BLOCK / MANUAL REVIEW",
  "top_risk_factors": [
    {
      "feature": "V17",
      "impact": 0.1234,
      "direction": "increased fraud risk"
    }
  ]
}
```

The `top_risk_factors` field contains the most influential SHAP features for the analyzed transaction.

---

## 📂 Project Structure

```text
AI-Payment-Intelligence-Engine/
│
├── api/
│   └── main.py
│
├── data/
│   └── demo_transactions.csv
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── models/
│   ├── fraud_model.pkl
│   └── feature_columns.pkl
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   └── train_model.py
│
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Pandas
- Joblib
- Uvicorn

### Machine Learning

- XGBoost
- Scikit-learn
- NumPy
- SHAP

### Frontend

- HTML
- CSS
- JavaScript

### Deployment & Version Control

- Git
- GitHub
- Render

---

## 🔁 Reproducible Training

The model training process is available in:

```text
src/train_model.py
```

The script:

1. Loads the original dataset.
2. Creates derived features.
3. Performs a stratified train-test split.
4. Handles class imbalance using `scale_pos_weight`.
5. Trains the XGBoost classifier.
6. Evaluates the model using classification metrics.
7. Calculates ROC-AUC and PR-AUC.
8. Generates confusion matrix and false-positive analysis.
9. Saves the trained model and feature column list.

Saved model artifacts:

```text
models/fraud_model.pkl
models/feature_columns.pkl
```

---

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/19ananyaaa/AI-Payment-Intelligence-Engine.git
cd AI-Payment-Intelligence-Engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI server

```bash
uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Example

Use:

```text
TXN-000542
```

to test a high-risk transaction.

Example result:

```text
Fraud Probability: ~99.8%
Risk Score: ~99.8
Risk Level: HIGH
Recommendation: BLOCK / MANUAL REVIEW
```

Use:

```text
TXN-000001
```

to test a low-risk transaction.

---

## 🎯 Objective

The objective of this project is to build an intelligent payment risk assessment system that can identify potentially fraudulent transactions and provide explainable reasons behind each prediction.

The project combines:

- Machine Learning
- XGBoost
- Imbalanced classification
- SHAP Explainable AI
- FastAPI
- Risk scoring
- False-positive analysis
- Audit trail
- Web-based dashboard
- Cloud deployment

into an end-to-end fraud detection and payment risk intelligence system.

---

## 🔐 Project Scope

This project is designed as a **defensive payment fraud detection and risk assessment system**.

It does not attempt to generate fraudulent transactions, bypass payment controls, or provide offense-capable functionality.

---

## 👩‍💻 Author

Ananya Agarwal