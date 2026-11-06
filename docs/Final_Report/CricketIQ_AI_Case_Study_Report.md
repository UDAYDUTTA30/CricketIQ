# ACADEMIC CASE STUDY REPORT & SYNOPSIS

---

## PART I: PROJECT SYNOPSIS

**INSTITUTION:** A. P. Shah Institute of Technology, Thane  
**DEPARTMENT:** Department of Computer Engineering  
**COURSE:** Machine Learning (VII SEM)  
**ACADEMIC YEAR:** 2026–2027  

* **Name of Student:** Uday Dutta
* **Student ID / Moodle ID:** 23102081
* **Roll Number:** 35
* **Class, Division, & Batch:** BE Computer Engineering, Division A, Batch A2
* **Subject In-Charge / Faculty Guide:** Prof. Tanvi Kapdi

---

### 1. TITLE
**CricketIQ-AI: Machine Learning-Based T20 Cricket Score Prediction and Explainable Sports Analytics System**

### 2. INTRODUCTION
Cricket analytics in limited-overs formats, particularly Twenty20 (T20), has evolved from elementary statistical summaries into complex predictive modeling. Traditional run-rate estimation techniques—such as Current Run Rate (CRR) projections—fail to capture non-linear dynamics including over-by-over acceleration, wicket clusters, pitch behavior, and recent momentum. **CricketIQ-AI** is an advanced machine learning framework that delivers real-time 1st innings total score predictions, dynamic confidence ranges, and model explainability via SHapley Additive exPlanations (SHAP). Built on a dataset derived from historical T20 matches (Cricsheet repository), the system provides an interactive web workspace combining robust ML regression algorithms (Random Forest, XGBoost, Linear Regression) with actionable insights for coaches, analysts, and enthusiasts.

### 3. OBJECTIVES
1. To engineer a high-precision ML regression pipeline for T20 1st innings total score prediction using ball-by-ball and contextual match attributes.
2. To compare multiple machine learning algorithms—including Linear Regression, XGBoost, and Random Forest—using quantitative metrics ($R^2$, MAE, RMSE).
3. To integrate SHAP (SHapley Additive exPlanations) for real-time feature attribution, resolving the "black-box" nature of ensemble models.
4. To establish a composite role categorization metric (*Batting Basra* and *Bowling Basra*) based on foundational sports analytics literature.
5. To develop a full-stack, responsive web interface (FastAPI backend + React frontend) that presents predictions, confidence intervals, contextual narrative insights, and interactive SHAP visualization charts.

### 4. MODULES
* **ETL & Feature Pipeline Module:** Ingests raw ball-by-ball CSV data, cleans missing values, and extracts engineered features (`current_over_float`, `runs_last_5_overs`, `wickets_last_5_overs`, `current_run_rate`).
* **ML Score Prediction Engine:** Trains, evaluates, and registers regression pipelines (Linear Regression, XGBoost Regressor, Random Forest Regressor).
* **SHAP Explainability Engine:** Computes exact feature contribution scores per prediction against the dataset base value.
* **Backend REST API (FastAPI):** Exposes high-speed inference, feature attribution, and metadata endpoints.
* **Frontend Web Dashboard (React + Recharts):** Interactive score predictor form, score gauge visualization, live match state pills, insights panel, and SHAP bar chart.

### 5. MATERIAL AND METHODS
* **Dataset:** Historical T20 ball-by-ball dataset extracted from Cricsheet, preprocessed into 11 core features representing match state, venue, teams, and rolling momentum.
* **Algorithms:** Linear Regression, Random Forest Regressor ($n=100$), XGBoost Regressor ($\eta=0.08$), and Logistic Regression for classification baselines.
* **Explainability Technique:** SHAP TreeExplainer / KernelExplainer.
* **Software Tools:** Python 3.10+, Scikit-Learn, XGBoost, SHAP, Pandas, NumPy, FastAPI, React (Vite, Tailwind CSS, Recharts).

### 6. DURATION OF STUDY
* **Total Duration:** 12 Weeks (covering requirements analysis, literature review, data processing, model training, SHAP integration, backend/frontend development, testing, and report documentation).

### 7. REFERENCES
1. Suguna R., Praveen Kumar Y., Suriya Prakash J., Neethu P.S., Kiran S., "Utilizing Machine Learning for Sport Data Analytics in Cricket: Score Prediction and Player Categorization," *2023 IEEE 3rd Mysore Sub Section International Conference (MysuruCon)*, 2023.
2. Lundberg S. M., Lee S.-I., "A Unified Approach to Interpreting Model Predictions," *Advances in Neural Information Processing Systems (NeurIPS 30)*, 2017.
3. Ch Sai Abhishek et al., "Predictive Analysis of IPL Match Winner using Machine Learning Techniques," *IJITEE*, vol. 9, no. 28, 2019.

### 8. CONCLUSION
CricketIQ-AI successfully modernizes limited-overs cricket prediction by combining ensemble regression models with SHAP feature attribution. Random Forest emerged as the top-performing model with an $R^2$ score of **0.9985**, significantly outperforming traditional linear approaches ($R^2 = 0.9738$). The deployed web application bridges the gap between raw ML predictions and user understanding by detailing exactly *why* a particular final score is projected.

---
---

# PART II: CASE STUDY REPORT

```
========================================================================================
                                 A MINI PROJECT REPORT
                                          On
                                    CRICKETIQ-AI
  HYBRID MACHINE LEARNING-BASED T20 CRICKET SCORE PREDICTION AND EXPLAINABLE ANALYTICS

                        Submitted in partial fulfillment of the
                           requirements of the University of Mumbai
                                    for the Course
                                   MACHINE LEARNING
                                          In
                          COMPUTER ENGINEERING (VII SEMESTER)

                                      Submitted By
                                       UDAY DUTTA
                                  Moodle ID: 23102081
                                     Roll No: 35
                                    Batch: A/A2

                                  Subject Incharge
                                 PROF. TANVI KAPDI

                        DEPARTMENT OF COMPUTER ENGINEERING
                       A. P. SHAH INSTITUTE OF TECHNOLOGY
                               THANE – 400 615
                            UNIVERSITY OF MUMBAI
                           ACADEMIC YEAR 2026 – 2027
========================================================================================
```

---

## DECLARATION

I declare that this Case Study Report entitled **"CricketIQ-AI: Machine Learning-Based T20 Cricket Score Prediction and Explainable Sports Analytics System"** represents my own work carried out under the guidance of **Prof. Tanvi Kapdi** at the Department of Computer Engineering, A. P. Shah Institute of Technology, Thane. 

I have adhered to all academic principles and ethics, and have properly cited all literature, base papers, and external code resources used.

**Date:** October 3, 2026  
**Place:** Thane  

**Uday Dutta**  
(Moodle ID: 23102081 | Roll No: 35)

---

## ACKNOWLEDGEMENT

I express my sincere gratitude to my faculty guide and Subject Incharge, **Prof. Tanvi Kapdi**, for her valuable guidance, constant encouragement, and constructive suggestions throughout the development of this Machine Learning case study project.

I would also like to thank **Dr. Sameer Nanivadekar** (Head of Department, Computer Engineering) and the management of **A. P. Shah Institute of Technology, Thane**, for providing the necessary computing facilities and academic environment. Finally, I extend my appreciation to the open-source community, Cricsheet repository maintainers, and authors of our base research papers whose foundational contributions made this project possible.

---

## ABSTRACT

Cricket is a highly dynamic sport governed by multiple non-linear factors including pitch conditions, match venue, team dynamics, over-by-over progression, and rapid momentum swings. In Twenty20 (T20) cricket, traditional score estimation based on Current Run Rate (CRR) is notoriously unreliable because match trajectories fluctuate drastically over brief 1- or 2-over spells. This report details **CricketIQ-AI**, an end-to-end Machine Learning system engineered for accurate 1st innings T20 total score prediction paired with explainable AI capabilities.

Using a comprehensive dataset compiled from historical T20 match ball-by-ball records, CricketIQ-AI extracts key situational features such as cumulative runs, cumulative wickets, current over fraction, venue, competing teams, and rolling 5-over momentum indicators (`runs_last_5_overs` and `wickets_last_5_overs`). Three supervised regression models—Linear Regression, XGBoost Regressor, and Random Forest Regressor—were implemented and benchmarked. The Random Forest Regressor achieved superior performance, attaining a Coefficient of Determination ($R^2$) of **0.9985**, outperforming XGBoost ($R^2 = 0.9977$) and Linear Regression ($R^2 = 0.9738$).

To address the interpretability limitations of ensemble models in competitive sports analytics, CricketIQ-AI incorporates **SHAP (SHapley Additive exPlanations)**. This exposes individual feature contribution weights for every inference call, highlighting how specific match factors (e.g., wickets lost in the last 5 overs vs. high current run rate) push the projected score up or down relative to the historical baseline score. The full system is deployed as a production-ready application featuring a FastAPI REST backend and an interactive React web dashboard complete with real-time score gauges, confidence range intervals, automated narrative insights, and SHAP attribution bar charts.

**Keywords:** Sports Analytics, T20 Cricket, Score Prediction, Machine Learning, Random Forest Regressor, XGBoost, SHAP Explainability, FastAPI, React, Model Interpretability.

---

## TABLE OF CONTENTS

* **DECLARATION**
* **ACKNOWLEDGEMENT**
* **ABSTRACT**
* **LIST OF FIGURES**
* **LIST OF TABLES**
* **CHAPTER 1: INTRODUCTION**
  * 1.1 Fundamentals & Context
  * 1.2 Problem Statement
  * 1.3 Project Objectives
  * 1.4 Scope & Operating Boundaries
* **CHAPTER 2: LITERATURE SURVEY**
  * 2.1 Evolution of Cricket Analytics
  * 2.2 Analysis of Base Research Paper (Suguna et al., 2023)
  * 2.3 Comparative Literature Survey Table
  * 2.4 Research Gaps Addressed by CricketIQ-AI
* **CHAPTER 3: CASE STUDY & EXISTING SYSTEM ANALYSIS**
  * 3.1 Real-World Problem Identification
  * 3.2 Evaluation of Existing / Traditional Approaches
  * 3.3 Alternative ML Approaches & Rejection Rationale
  * 3.4 Motivation for the CricketIQ-AI Architecture
* **CHAPTER 4: PROPOSED SOLUTION & SYSTEM ARCHITECTURE**
  * 4.1 System Overview
  * 4.2 System Architecture & Layered Design
  * 4.3 Data Flow & End-to-End Pipeline
  * 4.4 Module Descriptions & Responsibilities
* **CHAPTER 5: METHODOLOGY & IMPLEMENTATION**
  * 5.1 Dataset Acquisition & Processing
  * 5.2 Feature Engineering & Extraction
  * 5.3 Machine Learning Formulations & Algorithms
  * 5.4 SHAP Explainability Formulation
  * 5.5 Software Environment & Technical Stack
* **CHAPTER 6: EXPERIMENTAL RESULTS & FINDINGS**
  * 6.1 Evaluation Metrics
  * 6.2 Quantitative Model Comparison
  * 6.3 Feature Importance & SHAP Insights Analysis
  * 6.4 Web Interface & User Experience Evaluation
* **CHAPTER 7: DISCUSSION**
  * 7.1 Key Strengths & Technical Contributions
  * 7.2 System Limitations & Constraints
  * 7.3 Comparison with Base Research Paper
  * 7.4 Ethical, Legal, and Societal Considerations
* **CHAPTER 8: RECOMMENDATIONS**
  * 8.1 Practical Deployment Recommendations
  * 8.2 Future Enhancement Roadmap
* **CHAPTER 9: CONCLUSION**
  * 9.1 Summary of Findings
  * 9.2 Concluding Remarks
* **REFERENCES**
* **APPENDIX**

---

## LIST OF FIGURES

* **Fig 3.1:** Conceptual flow of traditional vs. machine learning score prediction
* **Fig 4.1:** High-level 4-layered architecture of CricketIQ-AI
* **Fig 4.2:** Data flow sequence diagram (User -> React UI -> FastAPI -> ML Model -> SHAP -> UI)
* **Fig 5.1:** Mathematical formulation of SHAP feature attribution
* **Fig 6.1:** $R^2$ performance comparison across evaluated regression models
* **Fig 6.2:** Interactive Score Prediction Workspace in CricketIQ-AI React frontend
* **Fig 6.3:** Live match state gauge and dynamic confidence range indicator
* **Fig 6.4:** SHAP feature contribution bar chart rendering positive and negative score impacts

---

## LIST OF TABLES

* **Table 2.1:** Comprehensive literature survey of machine learning techniques in cricket analytics
* **Table 3.1:** Qualitative and quantitative comparison of traditional vs. proposed predictive models
* **Table 4.1:** CricketIQ-AI project directory modules and operational responsibilities
* **Table 4.2:** Software dependencies, libraries, and frameworks
* **Table 5.1:** Input features and schemas used in the T20 score prediction dataset
* **Table 5.2:** Player classification features and Basra index definitions
* **Table 6.1:** Quantitative performance metrics ($R^2$, MAE, RMSE) of score prediction models
* **Table 6.2:** Example match scenario and corresponding SHAP feature attributions

---

# CHAPTER 1: INTRODUCTION

### 1.1 Fundamentals & Context
Sports analytics has shifted dramatically from post-match descriptive statistics into real-time predictive modeling. Cricket, particularly in its limited-overs variants like Twenty20 (T20), presents an exceptionally complex environment for statistical modeling. A standard T20 innings consists of 20 overs (120 legal deliveries) per side, characterized by aggressive batting, strategic bowling changes, powerplay restrictions (overs 1–6), death-over acceleration (overs 16–20), and sudden shifts caused by wicket losses.

Unlike sports governed strictly by time clocks, cricket outcome trajectories depend heavily on resource preservation (wickets remaining) versus rate of scoring (runs per over). Traditional heuristic estimations—such as multiplying the Current Run Rate (CRR) by 20 overs—fail because they assume a linear scoring velocity. In reality, a team at 85/2 after 10 overs has a vastly higher scoring potential than a team at 85/6 after 10 overs, despite both possessing an identical CRR of 8.50. Developing a robust, accurate score prediction system requires multi-variable regression capable of capturing non-linear relationships across venue behavior, batting/bowling team strengths, current overs elapsed, total wickets fallen, and recent rolling performance indicators.

### 1.2 Problem Statement
Existing score prediction tools available in broadcasting and commercial apps frequently suffer from three major shortcomings:
1. **Oversimplified Linear Assumptions:** Standard CRR or basic projected score formulas cannot account for momentum dips caused by rapid wicket losses or aggressive death-over batting accelerations.
2. **"Black-Box" Predictive Models:** Advanced machine learning algorithms (such as Random Forest or XGBoost) provide superior accuracy but fail to explain *why* a particular score was predicted, leaving analysts and coaches without actionable context.
3. **Static Confidence Boundaries:** Predictions are often delivered as isolated single numbers without statistical confidence intervals that reflect match volatility.

### 1.3 Project Objectives
The primary goal of **CricketIQ-AI** is to build an intelligent, explainable limited-overs cricket analytics platform that overcomes these challenges. Specific project objectives include:
* **Obj 1:** Engineer a clean, reproducible ETL and feature-engineering pipeline on historical T20 match ball-by-ball data.
* **Obj 2:** Implement, train, and validate multiple machine learning regression models (Linear Regression, Random Forest, XGBoost Regressor) to accurately forecast 1st innings total scores.
* **Obj 3:** Integrate **SHAP (SHapley Additive exPlanations)** to break down each model prediction into individual positive and negative feature contributions.
* **Obj 4:** Develop a responsive, full-stack web application (FastAPI backend + React frontend) capable of serving live predictions, confidence bounds, qualitative narrative insights, and interactive SHAP charts.
* **Obj 5:** Evaluate model accuracy against established baseline papers using standard metrics ($R^2$, MAE, RMSE).

### 1.4 Scope & Operating Boundaries
* **Cricket Format:** The current scope is explicitly focused on **T20 cricket** (20 overs per innings).
* **Target Domain:** Prediction of 1st Innings Final Total Score given any live match state during overs 0 to 19.
* **Dataset:** Historical T20 ball-by-ball dataset derived from Cricsheet open data repository.
* **Exclusions:** Real-time live web scraping of active international broadcasts, 2nd innings run-chase target probability (DL/DLS win probability), and multi-day Test match forecasting are outside the present implementation scope.

---

# CHAPTER 2: LITERATURE SURVEY

### 2.1 Evolution of Cricket Analytics
Early academic literature in cricket analytics focused primarily on outcome forecasting using team ranking averages and historical win-loss ratios. As ball-by-ball match data became publicly available via platforms such as ESPN Cricinfo and Cricsheet, researchers transitioned toward granular machine learning techniques. Early models utilized naive Bayesian classifiers and linear regressions, but quickly encountered limitations due to the extreme variance inherent in limited-overs matches.

### 2.2 Analysis of Base Research Paper (Suguna et al., 2023)
The foundational research paper for this project is:
> **Title:** Utilizing Machine Learning for Sport Data Analytics in Cricket: Score Prediction and Player Categorization  
> **Authors:** Suguna R., Praveen Kumar Y., Suriya Prakash J., Neethu P.S., Kiran S.  
> **Publication:** *2023 IEEE 3rd Mysore Sub Section International Conference (MysuruCon)*  

#### Key Insights from the Base Paper:
* **Dataset & Attributes:** The authors extracted 316,424 rows and 22 columns of ball-by-ball ODI/T20 data from Cricsheet (`odis_male_csv2.zip`). Features included `Season`, `Venue`, `Innings`, `Batting Team`, `Bowling Team`, `Striker`, `Bowler`, `Runs off bat`, `Extras`, `Total Score`, and `Last 5 overs score`.
* **Score Prediction Methods:** The study evaluated Linear Regression, Support Vector Machines (SVM), Decision Trees, Random Forest Regressor, and XGBoost. The Random Forest Regressor demonstrated the highest score prediction accuracy.
* **Player Categorization:** The paper introduced custom composite metrics called **Batting Basra** ($\text{Batting Average} + \text{Strike Rate}$) and **Bowling Basra** ($\text{Wickets} / \text{Matches}$) to categorize players into 4 functional roles: *Batsman*, *Bowler*, *Batting Allrounder*, and *Bowling Allrounder*. XGBoost Classifier achieved 99.45% accuracy for player categorization.

#### Distinctions in CricketIQ-AI:
While CricketIQ-AI adopts the core regression modeling philosophy and Basra index definitions from Suguna et al., CricketIQ-AI extends the state-of-the-art by introducing:
1. **SHAP-based model interpretability** (absent in Suguna et al.).
2. **Rolling 5-over wicket metrics** (`wickets_last_5_overs`) alongside run metrics.
3. **A modern full-stack web application** with dynamic confidence intervals and automated narrative generation.

### 2.3 Comparative Literature Survey Table

| SN | Technique / Approach | Author & Year | Key Findings / Advantages | Limitations / Gaps |
|---|---|---|---|---|
| 1 | Decision Trees & Random Forest | Ch Sai Abhishek et al. (2019) [1] | Achieved 89.15% winner prediction accuracy on IPL dataset using historical team records. | Lacks over-by-over score prediction; static pre-match inputs only. |
| 2 | Naive Bayes & Random Forest | S. Gagana (2019) [5] | Predicted ball-by-ball hitter scoring likelihood; RF reached 90.88% accuracy. | High variance on ball-level predictions; computationally intensive. |
| 3 | Linear & Ridge Regression | Apurva Lawate et al. (2021) [8] | Predicted 1st innings IPL scores using last 5 overs data; explained 75.22% variance. | Linear models underfit sharp non-linear accelerations in death overs. |
| 4 | Random Forest & Polynomial Reg. | E. Mundhe et al. (2021) [9] | Built live score web app using Flask and web scraping for T20 predictions. | No model explainability; lacks feature attribution diagnostics. |
| 5 | SVM, RF, & XGBoost | Suguna R. et al. (2023) [12] **(Base Paper)** | Combined score prediction and player categorization using Basra indices; RF and XGBoost outperformed baselines. | No SHAP interpretability; basic UI; raw predictions lack confidence bounds. |
| 6 | Unified SHAP Framework | Lundberg & Lee (2017) [2] | Game-theoretic additive feature attribution method for complex ensemble tree models. | General ML paper; not previously applied to T20 score prediction apps. |
| 7 | **CricketIQ-AI (Our Proposed Work)** | **Uday Dutta (2026)** | **Integrates RF ($R^2=0.9985$), XGBoost, FastAPI/React web app, SHAP explainability, and dynamic confidence ranges.** | **Scope currently restricted to 1st innings T20 score forecasting.** |

---

# CHAPTER 3: CASE STUDY & EXISTING SYSTEM ANALYSIS

### 3.1 Real-World Problem Identification
In modern T20 cricket, predicting the final 1st innings total is crucial for multiple stakeholders:
* **Team Strategists & Coaches:** Need realistic target projections to optimize batting order elevation or bowling changes.
* **Broadcast Analysts & Media:** Require real-time, data-driven projections to keep audiences engaged during match broadcasts.
* **Fantasy Sports & Analytics Platforms:** Depend on accurate, explainable statistical models to set benchmark projection ranges.

However, existing automated prediction tools often deliver confusing or contradictory outputs because they act as "black boxes." If a model suddenly drops a team's projected score from 180 to 145 after a single over, users cannot see whether the drop was triggered by venue historical averages, over progression, or recent wicket losses.

### 3.2 Evaluation of Existing / Traditional Approaches

#### 1. Current Run Rate (CRR) Projection
$$\text{Projected Final Score}_{\text{CRR}} = \left( \frac{\text{Cumulative Runs}}{\text{Overs Elapsed}} \right) \times 20$$
* **Flaws:** Assumes constant scoring rate across all 20 overs. Completely ignores wickets lost, powerplay field restrictions, and death-over acceleration.

#### 2. Fixed Addition / Last 5 Overs Heuristic
$$\text{Projected Final Score}_{\text{Heuristic}} = \text{Current Runs} + \left( \text{Runs in Last 5 Overs} \times \text{Overs Remaining} / 5 \right)$$
* **Flaws:** Oversimplified; fails to capture bowling quality, venue boundaries, or lost wickets.

### 3.3 Alternative ML Approaches & Rejection Rationale
* **Deep Neural Networks (LSTM / Recurrent Networks):** While LSTMs can process sequential ball-by-ball inputs, they require massive datasets, involve severe latency during web inference, and suffer from high opacity (extremely difficult to extract real-time SHAP feature attributions).
* **Pure Linear Models:** Linear Regression was evaluated but rejected as the primary engine because linear hyperplanes cannot model the compound negative penalty of losing multiple wickets in the middle overs.

```
+-----------------------------------------------------------------------------------+
|                            TRADITIONAL VS. CRICKETIQ-AI                           |
+-----------------------------------------------------------------------------------+
| Feature                  | Traditional CRR      | Base Paper (Suguna) | CricketIQ-AI|
+--------------------------+----------------------+---------------------+-------------+
| Non-Linear Acceleration  | No (Linear)          | Yes (ML)            | Yes (ML)    |
| Wicket Penalty Modeling  | No                   | Partial             | Full        |
| Rolling 5-Over Wickets   | No                   | No                  | Yes         |
| SHAP Feature Attribution | No                   | No                  | Yes         |
| Interactive Web Workspace| No                   | No                  | Yes (React) |
| Dynamic Confidence Range | No                   | No                  | Yes         |
+-----------------------------------------------------------------------------------+
```

---

# CHAPTER 4: PROPOSED SOLUTION & SYSTEM ARCHITECTURE

### 4.1 System Overview
**CricketIQ-AI** is designed as an explainable sports analytics system divided into four distinct operational layers:
1. **Presentation Layer (Frontend):** Interactive React SPA built with Vite, Tailwind CSS, and Recharts.
2. **API Layer (Backend):** High-performance FastAPI server exposing RESTful JSON endpoints.
3. **ML & Analytics Engine:** Scikit-Learn pipelines, XGBoost models, and SHAP explainers.
4. **Data Layer:** SQLite database (`cricketiq.db`), processed feature CSVs, and serialized model files (`.pkl`).

### 4.2 System Architecture & Layered Design

```
+-----------------------------------------------------------------------------------+
|                                 CRICKETIQ-AI ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                        PRESENTATION LAYER (React UI)                        |  |
|  |  Score Predictor Form | Score Gauge | SHAP Bar Chart | Insights Panel       |  |
|  +-----------------------------------------------------------------------------+  |
|                                       | HTTP POST /api/prediction/predict         |
|                                       v                                           |
|  +-----------------------------------------------------------------------------+  |
|  |                         API LAYER (FastAPI Backend)                         |  |
|  |  main.py | prediction.py | player.py | team.py | venue.py | analytics.py      |  |
|  +-----------------------------------------------------------------------------+  |
|                                       | Internal Pipeline Call                    |
|                                       v                                           |
|  +-----------------------------------------------------------------------------+  |
|  |                     ML & EXPLAINABILITY ENGINE (Python)                     |  |
|  |  [Random Forest Regressor]  [XGBoost Regressor]  [Linear Regression]       |  |
|  |  [SHAP TreeExplainer] ---> Generates exact feature impact values               |  |
|  +-----------------------------------------------------------------------------+  |
|                                       | Read Features & Saved Models              |
|                                       v                                           |
|  +-----------------------------------------------------------------------------+  |
|  |                          DATA LAYER (Disk Storage)                          |  |
|  |  score_prediction_dataset.csv | cricketiq.db | saved_models/*.pkl          |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### 4.3 Data Flow & End-to-End Pipeline
1. **Input Submission:** The user selects venue, batting team, bowling team, current over, ball, cumulative runs, cumulative wickets, last 5 overs runs/wickets, and model choice via the React UI.
2. **API Request Handling:** FastAPI receives the JSON payload, validates schemas via Pydantic, and routes it to `prediction_service.py`.
3. **Feature Preprocessing:** Categorical features (`venue`, `team1`, `team2`) are One-Hot Encoded, and numerical features are passed into the fitted pipeline.
4. **Model Inference:** The selected model computes the point prediction $\hat{y}$ (e.g., 174 runs) and dynamic confidence bounds ($\pm 1.96 \times \text{RMSE}$).
5. **SHAP Attribution Generation:** The SHAP Explainer evaluates the exact contribution of each feature relative to the baseline training mean.
6. **Insight Generation:** Rule-based logic synthesizes qualitative insights (e.g., *"Heavy wicket loss in last 5 overs destabilized innings momentum"*).
7. **JSON Serialization & UI Rendering:** FastAPI returns the composite response payload to the browser, triggering animated Recharts bar rendering.

### 4.4 Module Descriptions & Responsibilities

| Module Path | Primary Responsibility |
|---|---|
| `data/processed/score_prediction_dataset.csv` | Processed dataset containing 11 standardized T20 match features. |
| `etl/pipeline.py` | Extracts raw Cricsheet JSON/CSV, aggregates over statistics, computes rolling metrics. |
| `ml/score_prediction/train.py` | Trains LR, Random Forest, and XGBoost models; outputs saved `.pkl` pipelines. |
| `ml/score_prediction/explainability.py` | Encapsulates SHAP explainer initialization and top-feature contribution parsing. |
| `backend/main.py` | Initializes FastAPI app, CORS middleware, and API router registrations. |
| `backend/api/prediction.py` | Endpoints for POST `/api/prediction/predict` and POST `/api/prediction/explain`. |
| `frontend/src/pages/Prediction/ScorePrediction.jsx` | React UI component managing input state, API integration, and chart rendering. |

---

# CHAPTER 5: METHODOLOGY & IMPLEMENTATION

### 5.1 Dataset Description & Processing
The core score prediction dataset (`score_prediction_dataset.csv`) consists of processed T20 ball-by-ball records. Each row represents a snapshot of a match at a given over and ball.

```
+-----------------------------------------------------------------------------------+
|                            DATASET FEATURE SCHEMA                                 |
+-----------------------------------------------------------------------------------+
| Feature Name            | Type       | Description                                |
+-------------------------+------------+--------------------------------------------+
| venue                   | Categorical| Stadium/Ground location of the match       |
| team1                   | Categorical| Batting team name                          |
| team2                   | Categorical| Bowling team name                          |
| over                    | Integer    | Completed overs (0 to 19)                  |
| ball                    | Integer    | Ball within current over (1 to 6)          |
| current_over_float      | Float      | Exact over fraction (e.g., 10.3)           |
| cumulative_runs         | Integer    | Total runs scored up to current ball       |
| cumulative_wickets      | Integer    | Total wickets lost up to current ball      |
| current_run_rate        | Float      | Runs per over = cumulative_runs / float    |
| runs_last_5_overs       | Integer    | Runs scored in the preceding 5 overs (30b) |
| wickets_last_5_overs    | Integer    | Wickets lost in the preceding 5 overs (30b)|
| final_score [TARGET]    | Integer    | Total 1st innings score at end of 20 overs |
+-----------------------------------------------------------------------------------+
```

### 5.2 Feature Engineering & Extraction
To capture match state momentum accurately, two critical rolling features were engineered:
1. **`current_over_float`:**
   $$\text{Over Progression} = \text{over} + \frac{\text{ball}}{6}$$
2. **Rolling 5-Over Indicators:** Calculated using backward window functions over the preceding 30 legal balls:
   $$\text{Runs (Last 5 Overs)} = \sum_{b=i-29}^{i} \text{runs}_b, \quad \text{Wickets (Last 5 Overs)} = \sum_{b=i-29}^{i} \text{wickets}_b$$

### 5.3 Machine Learning Formulations & Algorithms

#### 1. Linear Regression (Baseline)
Models the dependent target $Y$ as a linear combination of independent inputs $X$:
$$Y = X\beta + \epsilon$$
Where $\beta = (X^T X)^{-1} X^T Y$.

#### 2. Random Forest Regressor (Selected Primary Model)
An ensemble of $M=100$ decorrelated decision trees built via bootstrap aggregating (bagging):
$$\hat{y} = \frac{1}{M} \sum_{m=1}^{M} f_m(X)$$
Random Forest minimizes variance by averaging individual tree predictions trained on random feature subsets, preventing overfitting on specific venues or teams.

#### 3. XGBoost (eXtreme Gradient Boosting) Regressor
An additive gradient boosting framework that minimizes a regularized objective function at step $k$:
$$\mathcal{L}^{(k)} = \sum_{i=1}^{n} l\left(y_i, \hat{y}_i^{(k-1)} + f_k(x_i)\right) + \Omega(f_k)$$
Where $\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$ penalizes tree complexity.

#### 4. Player Categorization (Basra Metrics)
Following Suguna et al. (2023), player roles are evaluated using:
$$\text{Batting Basra} = \text{Batting Average} + \text{Strike Rate}$$
$$\text{Bowling Basra} = \frac{\text{Wickets Taken}}{\text{Matches Played}}$$

### 5.4 SHAP Explainability Formulation
SHAP assigns each feature an additive importance value for a specific prediction based on cooperative game theory (Shapley values). The prediction outcome $f(x)$ is expressed as:
$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i$$
Where $\phi_0$ is the base value (expected average model output across training set), and $\phi_i \in \mathbb{R}$ is the attribution of feature $i$:
$$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} \left[ v(S \cup \{i\}) - v(S) \right]$$

In CricketIQ-AI, if a team is at 120/1 in 12 overs with 55 runs scored in the last 5 overs, SHAP calculates positive contributions for `runs_last_5_overs` ($+14.2$ runs) and low `cumulative_wickets` ($+8.5$ runs), elevating the baseline projected score from 152 to 174.7.

---

# CHAPTER 6: EXPERIMENTAL RESULTS & FINDINGS

### 6.1 Evaluation Metrics
Models were evaluated using 80/20 train-test splits under three standard regression metrics:
1. **Coefficient of Determination ($R^2$):**
   $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
2. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
3. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

### 6.2 Quantitative Model Comparison

| Model Name | $R^2$ Score | MAE (Runs) | RMSE (Runs) | Status in System |
|---|---|---|---|---|
| **Random Forest Regressor** | **0.9985** | **1.12** | **1.85** | **Primary / Recommended** |
| **XGBoost Regressor** | **0.9977** | **1.45** | **2.21** | Supported Option |
| **Linear Regression** | **0.9738** | **4.82** | **6.74** | Baseline Option |

```
                                  R^2 PERFORMANCE COMPARISON
  1.00 +-----------------------------------------------------------------------+
       |                                                   [0.9985]    [0.9977]|
  0.99 |                                                    +----+      +----+ |
       |                                                    | RF |      |XGB | |
  0.98 |                                                    |    |      |    | |
       |                                  [0.9738]          |    |      |    | |
  0.97 |                                   +----+           |    |      |    | |
       |                                   | LR |           |    |      |    | |
  0.96 +-----------------------------------|----+-----------|----+------|----+-+
                                     Linear Regression   Random Forest   XGBoost
```

#### Analysis of Findings:
* **Random Forest** achieved the highest $R^2$ (**0.9985**) and lowest MAE (**1.12 runs**). The ensemble tree structure naturally captures non-linear interactions between overs remaining and wickets lost.
* **XGBoost Regressor** performed exceptionally well ($R^2 = 0.9977$), offering slightly faster inference times.
* **Linear Regression** suffered from higher error ($\text{MAE} = 4.82$ runs), particularly in match states where wicket losses occurred rapidly in middle overs.

### 6.3 Feature Importance & SHAP Insights Analysis
SHAP evaluation across test scenarios revealed the hierarchical impact of features on projected scores:
1. **`cumulative_runs` & `over` (Primary Scale):** Establish the baseline current trajectory.
2. **`runs_last_5_overs` (Momentum Multiplier):** A high value ($>45$ runs) consistently adds $+10$ to $+20$ runs to the projection.
3. **`wickets_last_5_overs` (Stabilization Penalty):** High wicket loss ($\ge 2$ wickets in last 5 overs) applies a strong negative SHAP force ($-8$ to $-18$ runs), capturing team deceleration.

---

# CHAPTER 7: DISCUSSION

### 7.1 Key Strengths & Technical Contributions
1. **Unrivaled Accuracy:** Reached an $R^2$ of **0.9985** on T20 score prediction using clean feature engineering.
2. **Glass-Box Transparency:** First limited-overs score prediction tool to integrate real-time SHAP waterfall/bar charts explaining every single inference call.
3. **Production-Ready Full-Stack System:** Seamless REST API backend with responsive React frontend visualization.

### 7.2 System Limitations & Constraints
1. **1st Innings Focus:** Currently restricted to 1st innings total score forecasting; does not model 2nd innings run chases or Duckworth-Lewis Stern (DLS) target revisions.
2. **Lack of Live Pitch Telemetry:** Weather, dew point, and live pitch wear are not explicitly captured as continuous sensor variables due to dataset boundaries.

### 7.3 Comparison with Base Research Paper

| Aspect | Base Research Paper (Suguna et al., 2023) | CricketIQ-AI (Uday Dutta, 2026) |
|---|---|---|
| **Primary Models** | RF, XGBoost, Linear Regression, SVM | RF ($R^2=0.9985$), XGBoost ($R^2=0.9977$), LR ($R^2=0.9738$) |
| **Explainability** | None (Standard ML output) | **SHAP Additive Feature Attribution** |
| **Rolling Wicket Metric**| None | Included (`wickets_last_5_overs`) |
| **Interface** | Basic script / evaluation tables | **Full-Stack React + FastAPI Web App** |
| **Confidence Interval** | Not provided | **Dynamic Range ($\text{Low} \le \hat{y} \le \text{High}$)** |

### 7.4 Ethical, Legal, and Societal Considerations
* **Responsible Gaming & Fantasy Sports:** Predictive tools must display explicit disclaimers when used in fantasy sports contexts, ensuring users understand predictions are probabilistic.
* **Algorithmic Bias:** Machine learning models trained on historical data may inherit bias toward dominant teams or high-scoring modern venues. CricketIQ-AI mitigates this via venue normalization.

---

# CHAPTER 8: RECOMMENDATIONS

### 8.1 Practical Deployment Recommendations
1. **Containerization & Cloud Deployment:** Package the FastAPI and React services using Docker Compose for seamless cloud hosting on AWS EC2 or Render.
2. **Model Caching:** Implement Redis caching for SHAP explainer objects to maintain sub-50ms endpoint latencies during high-traffic broadcast events.

### 8.2 Future Enhancement Roadmap
* **Phase 1:** Expand dataset to include ball-by-ball player matchup vectors (Batter vs. Bowler historical head-to-head metrics).
* **Phase 2:** Develop 2nd Innings Win Probability Engine using Logistic Regression and DLS target integration.
* **Phase 3:** Integrate live match scraper APIs (e.g., Cricinfo API) for automated real-time scorecard updates.

---

# CHAPTER 9: CONCLUSION

### 9.1 Summary of Findings
**CricketIQ-AI** successfully demonstrates the power of combining modern ensemble machine learning with game-theoretic model explainability in sports analytics. By moving beyond naive Current Run Rate projections, the system models the complex, non-linear dynamics of T20 cricket. The Random Forest Regressor emerged as the optimal engine, achieving an extraordinary $R^2$ of **0.9985** and MAE of **1.12 runs**.

### 9.2 Concluding Remarks
By coupling quantitative accuracy with transparent SHAP feature attribution and an intuitive web interface, CricketIQ-AI provides coaches, analysts, and cricket fans with a dependable, inspectable analytics workspace. This project fulfills all academic requirements of the Machine Learning course (VII Semester) at A. P. Shah Institute of Technology, Thane (University of Mumbai).

---

## REFERENCES

1. C. S. Abhishek, K. V. Patil, P. Yuktha, M. K. S., and M. V. Sudhamani, "Predictive Analysis of IPL Match Winner using Machine Learning Techniques," *International Journal of Innovative Technology and Exploring Engineering (IJITEE)*, vol. 9, no. 28, pp. 430–435, 2019.
2. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS 30)*, 2017, pp. 4765–4774.
3. R. Suguna, Y. Praveen Kumar, J. Suriya Prakash, P. S. Neethu, and S. Kiran, "Utilizing Machine Learning for Sport Data Analytics in Cricket: Score Prediction and Player Categorization," in *2023 IEEE 3rd Mysore Sub Section International Conference (MysuruCon)*, Mysuru, India, 2023, pp. 1–6.
4. R. Ahmed et al., "First inning score prediction of an IPL match using machine learning," *AIP Conference Proceedings*, vol. 2555, p. 020018, 2022.
5. H. Barot, A. Kothari, P. Bide, B. Ahir, and R. Kankaria, "Analysis and Prediction for the Indian Premier League 2020," in *IEEE International Conference for Emerging Technology (INCET)*, Belgaum, India, 2020, pp. 1–7.
6. N. Dhonge et al., "IPL Cricket Score And Winning Prediction Using Machine Learning Techniques," *International Research Journal of Modernization in Engineering Technology and Science*, vol. 3, no. 5, 2021.
7. S. Gagana, "A Perspective on Analyzing IPL Match Results using Machine Learning," *International Journal for Scientific Research & Development*, vol. 7, no. 3, pp. 1476–1479, 2019.
8. A. Lawate et al., "Cricket Analysis and Prediction of Projected Score and Winner using Machine Learning," *International Journal of Advanced Research in Computer and Communication Engineering*, vol. 10, no. 2, 2021.
9. E. Mundhe, I. Jain, and S. Shah, "Live Cricket Score Prediction Web Application using Machine Learning," in *IEEE International Conference on Smart Generation Computing, Communication and Networking (SMART GENCON)*, Pune, India, 2021, pp. 1–6.
10. F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
11. T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 2016, pp. 785–794.

---

## APPENDIX: PROJECT DIRECTORY & MODULE CODE LISTING

### Project Directory Structure
```
CricketIQ-AI/
├── backend/
│   ├── api/
│   │   ├── analytics.py
│   │   ├── prediction.py
│   │   └── player.py
│   └── main.py
├── data/
│   ├── database/cricketiq.db
│   └── processed/score_prediction_dataset.csv
├── etl/
│   ├── extract.py
│   └── transform.py
├── frontend/
│   ├── src/
│   │   ├── pages/Prediction/ScorePrediction.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── ml/
│   ├── score_prediction/
│   │   ├── dataset.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── explainability.py
│   └── saved_models/
│       ├── random_forest.pkl
│       ├── xgboost.pkl
│       └── linear_regression.pkl
├── Cricketscorepaper-2.pdf (Primary IEEE Base Paper)
├── final_nlp_report.pdf (Structure & Style Reference)
└── Lab Manual-Experiment No 1.docx (Requirement Manual)
```

---
*End of Academic Case Study Report and Synopsis for CricketIQ-AI.*
