# AI Payment Intelligence Engine

An AI-powered fintech system for detecting fraudulent payment transactions, calculating transaction risk, and providing explainable risk factors using Machine Learning and SHAP.

## 🚀 Live Demo

https://ai-payment-intelligence-engine-1.onrender.com

## 📌 Project Overview

The AI Payment Intelligence Engine is a machine learning-based fraud detection system designed to assess payment transaction risk.

The system generates:

- Fraud probability
- Risk score
- Risk level
- Recommended action
- Top contributing risk factors
- SHAP-based explainable AI insights

## ⚙️ How It Works

1. User enters a demo Transaction ID.
2. The backend maps the Transaction ID to a transaction in the reference dataset.
3. The transaction features are retrieved from the dataset.
4. Derived features such as `Hour` and `Amount_Log` are calculated.
5. The trained XGBoost model predicts the probability of fraud.
6. The probability is converted into a risk score.
7. The transaction is classified as LOW, MEDIUM, or HIGH risk.
8. SHAP identifies the most influential features behind the prediction.
9. The result is displayed on the dashboard.

## 🧠 Machine Learning

The project uses an **XGBoost classifier** for binary fraud detection.

The model uses 32 features:

- `Time`
- `V1` to `V28`
- `Amount`
- `Hour`
- `Amount_Log`

The dataset contains **284,807 transactions** and **492 fraudulent transactions**, making it a highly imbalanced classification problem.

### Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 99.95% |
| Precision | 85.26% |
| Recall | 82.65% |
| F1-Score | 83.94% |
| ROC-AUC | 0.983 |
| PR-AUC | 0.880 |

### Risk Classification

| Risk Score | Risk Level | Recommendation |
|------------|------------|----------------|
| < 30 | LOW | APPROVE |
| 30–69.99 | MEDIUM | REVIEW |
| ≥ 70 | HIGH | BLOCK / MANUAL REVIEW |

## 🔍 Explainable AI

**SHAP (SHapley Additive exPlanations)** is used to explain individual predictions.

For every analyzed transaction, the system identifies the top 5 features that have the greatest influence on the prediction.

Each feature is shown as either:

- Increased fraud risk
- Reduced fraud risk

This makes the model more interpretable and helps users understand why a transaction is considered risky.

## 🖥️ Features

- AI-based fraud detection
- Transaction risk scoring
- Fraud probability estimation
- LOW / MEDIUM / HIGH risk classification
- Automated risk recommendation
- SHAP-based explainability
- Top 5 risk factors
- FastAPI REST API
- Responsive fintech dashboard
- Cloud deployment using Render

## 🏗️ System Architecture

User
  │
  ▼
Frontend Dashboard
  │
  │ Transaction ID
  ▼
FastAPI Backend
  │
  ├── Demo Transaction Dataset
  │
  ├── Feature Preparation
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
Risk Factors + Recommendation
  │
  ▼
Frontend Dashboard


📊 Dataset

The project is based on a credit card fraud detection dataset containing:

284,807 transactions
492 fraudulent transactions
30 original transaction features
Highly imbalanced fraud distribution

The full dataset is used for model development and training.

The complete creditcard.csv file is not stored in the GitHub repository because of its large size.

For the deployed application, a small authentic subset of the original dataset is included:

data/demo_transactions.csv

This allows the deployed API to perform genuine model inference without storing the complete training dataset in the repository.

Demo Transaction IDs

Transaction IDs such as:

TXN-000001
TXN-000542

are demo/reference IDs created for this portfolio project.

They map to rows in the reference dataset and are not real banking transaction identifiers.

🔗 API Endpoints

The backend is built using FastAPI.

Health Check
GET /

Checks whether the API service is running.

Fraud Prediction
POST /predict

Example request:

{
  "transaction_id": "TXN-000542"
}

Example response:

{
  "transaction_id": "TXN-000542",
  "fraud_probability": 0.998,
  "risk_score": 99.8,
  "risk_level": "HIGH",
  "recommendation": "BLOCK / MANUAL REVIEW",
  "top_risk_factors": []
}

The top_risk_factors field contains the most influential SHAP features for the transaction.

📂 Project Structure
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


🛠️ Tech Stack

Backend
Python
FastAPI
Pydantic
Pandas
Joblib
Uvicorn
Machine Learning
XGBoost
Scikit-learn
NumPy
SHAP
Frontend
HTML
CSS
JavaScript
Deployment
GitHub
Render


💻 Local Setup

1. Clone the repository
git clone https://github.com/19ananyaaa/AI-Payment-Intelligence-Engine.git
cd AI-Payment-Intelligence-Engine
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Start the FastAPI server
uvicorn api.main:app --reload

API:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs


🧪 Example

Use:

TXN-000542

to test a high-risk transaction.

Example result:

Fraud Probability: 99.8%
Risk Score: 99.8
Risk Level: HIGH
Recommendation: BLOCK / MANUAL REVIEW
🎯 Objective

The objective of this project is to build an intelligent payment risk assessment system that can identify potentially fraudulent transactions and provide explainable reasons behind each prediction.

The project combines Machine Learning, XGBoost, imbalanced classification, FastAPI, SHAP Explainable AI, and a web-based dashboard into an end-to-end fraud detection system.

👩‍💻 Author
Ananya Agarwal