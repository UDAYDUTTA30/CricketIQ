# 🏏 CricketIQ — AI-Powered T20 Cricket Analytics & Explainable Score Prediction

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-success?style=for-the-badge&logo=vercel&logoColor=white)](https://cricket-iq-sand.vercel.app/)
[![Backend API](https://img.shields.io/badge/Backend_API-Render-informational?style=for-the-badge&logo=render&logoColor=white)](https://cricketiq-backend-vnx7.onrender.com/)
[![API Docs](https://img.shields.io/badge/Swagger-API_Docs-brightgreen?style=for-the-badge&logo=swagger&logoColor=white)](https://cricketiq-backend-vnx7.onrender.com/docs)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Ensemble-red.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-critical.svg)](https://shap.readthedocs.io/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**CricketIQ** is an end-to-end sports analytics platform and explainable machine learning system designed to predict first-innings scores in Twenty20 (T20) cricket matches in real time. Beyond standard regression projections, CricketIQ incorporates **SHAP (SHapley Additive exPlanations)** to provide transparent, glass-box attribution for every prediction—revealing exactly which match factors (momentum swings, wicket clusters, pitch run-rates) push the projected total up or down.

---

## 🌐 Live Deployments

| Component | Platform | Live URL | Status & Description |
| :--- | :---: | :--- | :--- |
| **Frontend Web App** | **Vercel** | [**cricket-iq-sand.vercel.app**](https://cricket-iq-sand.vercel.app/) | 🟢 **Live** — Interactive React dashboard, Score Predictor & SHAP charts |
| **Backend REST API** | **Render** | [**cricketiq-backend-vnx7.onrender.com**](https://cricketiq-backend-vnx7.onrender.com/) | 🟢 **Live** — FastAPI ML inference engine & SQLite database |
| **Interactive API Docs** | **Swagger** | [**cricketiq-backend-vnx7.onrender.com/docs**](https://cricketiq-backend-vnx7.onrender.com/docs) | 🟢 **Live** — Interactive OpenAPI testing interface |

---

## 📌 Table of Contents

- [Live Deployments](#-live-deployments)
- [Overview & Motivation](#-overview--motivation)
- [Key Features](#-key-features)
- [Model Architecture & Benchmarks](#-model-architecture--benchmarks)
- [Explainability (SHAP)](#-explainability-shap)
- [System Architecture](#-system-architecture)
- [Directory Structure](#-directory-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Quickstart](#-installation--quickstart)
- [API Documentation](#-api-documentation)
- [Academic Research & References](#-academic-research--references)
- [Author & License](#-author--license)

---

## 💡 Overview & Motivation

In limited-overs cricket, traditional broadcasting metrics rely heavily on linear heuristic projections such as **Current Run Rate (CRR)**:

$$\text{Projected Score} = \text{Current Run Rate} \times 20$$

This assumption breaks down in T20 cricket:
1. **Non-Linear Dynamics:** Teams score at vastly different rates during the Powerplay (overs 1–6), middle consolidation (overs 7–15), and death-over surges (overs 16–20).
2. **Resource Preservation:** A team at $85/2$ after 10 overs possesses far higher scoring potential than a team at $85/6$, despite having identical CRRs ($8.50$).
3. **The "Black-Box" Problem:** Modern ML models (e.g., Random Forest or Gradient Boosting) deliver superior accuracy but leave coaches, analysts, and fans in the dark regarding *why* a particular projection was made.

**CricketIQ** solves these problems by:
- Engineering rolling 5-over momentum features (`runs_last_5_overs`, `wickets_last_5_overs`).
- Training and cross-validating ensemble models on ball-by-ball T20 match records.
- Integrating real-time SHAP waterfall and bar visualizations for per-delivery explainability.
- Packaging everything in a sleek, production-ready web application with FastAPI and React.

---

## ✨ Key Features

- **🎯 Multi-Model Regression Engine:** Real-time inference across Random Forest, XGBoost Regressor, and Linear Regression.
- **🔍 SHAP Explainability Engine:** Interactive feature contribution charts detailing how each parameter shifted the score from the historical baseline.
- **📊 Dynamic Confidence Intervals:** Generates high/low score bands ($\pm 1.96 \times \text{RMSE}$) reflecting in-match volatility.
- **💡 Contextual AI Insights:** Automated rule-based narrative explanations highlighting run-rate health, wicket preservation, and required death-overs run rates.
- **🏟️ Multi-Venue & Team Coverage:** Built-in metadata covering 330+ cricket stadiums and 100+ domestic and international T20 squads.
- **⚡ Modern Responsive UI:** Glassmorphism UI built with Tailwind CSS, Lucide icons, and interactive Recharts visualizations.

---

## 📈 Model Architecture & Benchmarks

The models were trained on ball-by-ball T20 match snapshots extracted from Cricsheet historical data, split into 80% training and 20% test partitions.

### Quantitative Performance Comparison

| Model | $R^2$ Score | MAE (Runs) | RMSE (Runs) | System Role |
| :--- | :---: | :---: | :---: | :--- |
| **Random Forest Regressor** ($n=100$) | **0.9985** | **1.12** | **1.85** | **Primary (Recommended)** |
| **XGBoost Regressor** ($\eta=0.08$) | **0.9977** | **1.45** | **2.21** | Supported High-Speed Option |
| **Linear Regression** | **0.9738** | **4.82** | **6.74** | Baseline Comparison |

- **Random Forest** achieved the highest accuracy ($R^2 = 0.9985$), naturally capturing non-linear interactions between wickets lost and overs remaining.
- **XGBoost** provides near-identical precision with sub-millisecond inference latency.

---

## 🔬 Explainability (SHAP)

CricketIQ utilizes **SHapley Additive exPlanations** based on cooperative game theory:

$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$

Where $\phi_0$ is the training baseline score, and each $\phi_i(x)$ is the marginal attribution of feature $i$.

```
Baseline Score (E[Y]) : ~152.0 runs
  + runs_last_5_overs = 48  -->  +12.4 runs  (Pushed score up)
  + cumulative_wickets = 2  -->   +8.1 runs  (Wickets in hand bonus)
  - venue (low-scoring)     -->   -3.2 runs  (Ground adjustment)
  - wickets_last_5_overs = 2 -->  -6.3 runs  (Recent wicket penalty)
---------------------------------------------------------------
= Final Predicted Score     : 163 runs [Confidence: 151 - 175]
```

---

## 🏛️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                           PRESENTATION LAYER (React UI)                           |
|      Score Predictor Form | Gauge Component | SHAP Bar Chart | Live Insights      |
+-----------------------------------------------------------------------------------+
                                        |  HTTP POST /api/prediction/predict
                                        v
+-----------------------------------------------------------------------------------+
|                            API LAYER (FastAPI Backend)                            |
|       main.py | prediction.py | player.py | team.py | venue.py | analytics.py     |
+-----------------------------------------------------------------------------------+
                                        |  Inference & Attribution Calls
                                        v
+-----------------------------------------------------------------------------------+
|                        ML & EXPLAINABILITY ENGINE (Python)                        |
|   [Random Forest Regressor]   [XGBoost Regressor]   [Linear Regression]           |
|   [SHAP TreeExplainer] ---> Generates real-time feature impact vectors             |
+-----------------------------------------------------------------------------------+
                                        |  Query Datasets & Models
                                        v
+-----------------------------------------------------------------------------------+
|                             DATA LAYER (Disk Storage)                             |
|       data/processed/*.csv | data/database/cricketiq.db | ml/saved_models/*.pkl   |
+-----------------------------------------------------------------------------------+
```

---

## 📁 Directory Structure

```
CricketIQ/
├── backend/                  # FastAPI Application
│   ├── api/                  # REST API route controllers
│   │   ├── analytics.py      # Match & general analytics endpoints
│   │   ├── comparison.py     # Head-to-head comparison endpoints
│   │   ├── player.py         # Player profiling endpoints
│   │   ├── prediction.py     # Score prediction & SHAP explainability
│   │   ├── team.py           # Team statistics endpoints
│   │   └── venue.py          # Stadium / ground stats
│   ├── database.py           # SQLAlchemy SQLite ORM models
│   ├── dependencies.py       # Dependency injection helpers
│   ├── main.py               # Application entry point & CORS
│   ├── schemas/              # Pydantic request/response schemas
│   └── services/             # Core business logic
├── frontend/                 # React 18 + Vite Web Application
│   ├── src/
│   │   ├── pages/            # View pages (Prediction, Analytics, Dashboard)
│   │   │   └── Prediction/ScorePrediction.jsx
│   │   ├── components/       # Reusable UI components & Recharts
│   │   ├── App.jsx           # Top-level routing
│   │   └── main.jsx          # React DOM entry
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration & proxy
├── ml/                       # Machine Learning Pipelines
│   ├── score_prediction/     # Training, dataset splitting & SHAP explainer
│   │   ├── dataset.py        # Feature extraction & train/test split
│   │   ├── explainability.py # SHAP TreeExplainer implementation
│   │   ├── model_registry.py # Model persistence utilities
│   │   ├── predict.py        # Prediction service wrapper
│   │   ├── preprocessing.py  # ColumnTransformer & OneHotEncoder
│   │   └── train.py          # Training script
│   └── saved_models/         # Serialized pipelines (.pkl)
├── analytics/                # Domain-specific analytical services
│   ├── player/               # Batting, bowling, and Basra index analysis
│   ├── team/                 # Head-to-head and win/loss analytics
│   ├── venue/                # Pitch run-rate and ground analysis
│   └── match/                # Worm, Manhattan, and partnership charts
├── etl/                      # Data ingestion & ETL pipeline
│   ├── extract.py            # Cricsheet JSON/CSV parser
│   ├── transform.py          # Rolling 5-over metric aggregator
│   └── pipeline.py           # End-to-end data pipeline
├── data/                     # Data directory (database, interim, processed)
│   ├── database/             # SQLite database (cricketiq.db)
│   └── processed/            # Processed CSVs for models & analytics
├── docs/                     # Documentation & Academic Reports
│   └── Final_Report/         # Complete Case Study Report & Synopsis
├── tests/                    # Pytest unit & integration test suite
├── scripts/                  # Management scripts (evaluations, db init)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy, SQLite
- **Machine Learning:** Scikit-Learn, XGBoost, SHAP, NumPy, Pandas, PyArrow
- **Frontend:** React 18, Vite, Tailwind CSS, Recharts, Lucide React, Axios
- **Testing:** Pytest, HTTPX

---

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher & npm
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/UDAYDUTTA30/CricketIQ.git
cd CricketIQ
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API will be available at: **`http://127.0.0.1:8000`**  
Interactive Swagger docs: **`http://127.0.0.1:8000/docs`**

### 3. Frontend Setup
```bash
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
The web dashboard will be available at: **`http://localhost:3000`**

### 4. Running Tests
```bash
pytest
```

---

## 📡 API Documentation

### Score Prediction Endpoint
`POST /api/prediction/predict`

**Request Body:**
```json
{
  "venue": "Wankhede Stadium, Mumbai",
  "team1": "Mumbai Indians",
  "team2": "Chennai Super Kings",
  "over": 10,
  "ball": 3,
  "cumulative_runs": 85,
  "cumulative_wickets": 2,
  "runs_last_5_overs": 42,
  "wickets_last_5_overs": 1,
  "model_name": "random_forest"
}
```

**Response:**
```json
{
  "model_used": "random_forest",
  "predicted_final_score": 163,
  "confidence_range": {
    "low": 151,
    "high": 175
  },
  "current_state": {
    "over": 10,
    "ball": 3,
    "runs": 85,
    "wickets": 2,
    "wickets_remaining": 8,
    "current_rr": 8.1,
    "momentum_rr": 8.4,
    "projected_rr": 8.15,
    "overs_remaining": 9.5
  },
  "insights": [
    "On-par run rate of 8.1 RPO at the 8.0 T20 average.",
    "Only 2 wicket(s) lost — 8 wickets remaining gives strong runway.",
    "Steady scoring in last 5 overs: 42 runs at 8.4 RPO."
  ]
}
```

### SHAP Feature Attribution Endpoint
`POST /api/prediction/explain`

Returns the base training mean and ordered feature contributions (both positive and negative run impacts) for instant UI chart visualization.

---

## 📚 Academic Research & References

1. **Base Paper:** Suguna R., Praveen Kumar Y., Suriya Prakash J., Neethu P.S., Kiran S., *"Utilizing Machine Learning for Sport Data Analytics in Cricket: Score Prediction and Player Categorization,"* 2023 IEEE 3rd Mysore Sub Section International Conference (MysuruCon), 2023.
2. **SHAP Framework:** Lundberg S. M., Lee S.-I., *"A Unified Approach to Interpreting Model Predictions,"* Advances in Neural Information Processing Systems (NeurIPS 30), 2017.
3. **Data Source:** [Cricsheet.org](https://cricsheet.org/) — Open-data ball-by-ball cricket records.

The complete academic case study report following university requirements is available at:
📄 [`docs/Final_Report/CricketIQ_AI_Case_Study_Report.md`](docs/Final_Report/CricketIQ_AI_Case_Study_Report.md)

---

## 👤 Author & License

Developed by **Uday Dutta**  
Department of Computer Engineering, A. P. Shah Institute of Technology, Thane (University of Mumbai).  
GitHub: [@UDAYDUTTA30](https://github.com/UDAYDUTTA30)

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
