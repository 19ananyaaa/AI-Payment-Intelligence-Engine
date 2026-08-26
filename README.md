# AI Payment Intelligence Engine

An AI-powered fintech system for detecting fraudulent payment transactions, calculating transaction risk, and providing explainable risk factors using machine learning and SHAP.

## 🚀 Live Demo

https://ai-payment-intelligence-engine-1.onrender.com

## 📌 Project Overview

The AI Payment Intelligence Engine analyzes transaction features and predicts the probability of fraud.

The system generates:

- Fraud probability
- Risk score
- Risk level
- Recommended action
- Top contributing risk factors
- Explainable AI insights using SHAP

## ⚙️ How It Works

1. User enters a Transaction ID.
2. User provides the transaction feature values.
3. The frontend sends the data to the FastAPI backend.
4. The trained machine learning model predicts fraud probability.
5. The system calculates a risk score.
6. SHAP explains the most influential features.
7. The result is displayed on the dashboard.

## 🧠 Machine Learning

The project uses a trained fraud detection model to classify payment transactions based on transaction features.

### Risk Classification

| Risk Score | Risk Level | Recommendation |
|------------|------------|----------------|
| < 30 | LOW | APPROVE |
| 30–69.99 | MEDIUM | REVIEW |
| ≥ 70 | HIGH | BLOCK / MANUAL REVIEW |

## 🔍 Explainable AI

SHAP (SHapley Additive exPlanations) is used to identify the features that have the greatest influence on each prediction.

The dashboard displays the top 5 model contributors and explains whether each feature:

- Increased fraud risk
- Reduced fraud risk

## 🖥️ Features

- Transaction analysis dashboard
- Real-time fraud prediction
- Risk score calculation
- Fraud probability
- LOW / MEDIUM / HIGH risk classification
- Automated recommendation
- SHAP-based explainability
- FastAPI REST API
- Responsive web interface
- Cloud deployment using Render

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Pandas
- Joblib
- SHAP
- Uvicorn

### Machine Learning
- Scikit-learn
- XGBoost
- SHAP

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- GitHub
- Render

## 📂 Project Structure

```text
AI-Payment-Intelligence-Engine/
│
├── api/
│   └── main.py
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
├── .gitignore
└── README.md
## 🔗 API Endpoints

### Health Check

`GET /`

Checks whether the FastAPI service is running successfully.

### Fraud Prediction

`POST /predict`

Accepts a transaction ID and 32 transaction feature values, then returns:

- Fraud probability
- Risk score
- Risk level
- Recommended action
- Top 5 risk factors

## 🎯 Objective

The objective of this project is to build an intelligent payment risk assessment system that can identify potentially fraudulent transactions and provide explainable reasons behind each prediction.

The system combines machine learning with SHAP-based explainable AI to help users understand why a transaction is considered risky.

## 👩‍💻 Author

**Ananya Agarwal**
