# Construction Project Analytics & Predictive Modeling

A data-driven construction project analytics portfolio project combining **Python, SQL, Statistical Analysis, Machine Learning, Earned Value Management (EVM), and Power BI** to analyze project cost, schedule, progress, and risk.

The project demonstrates how construction and project-controls data can be transformed into actionable insights for **cost control, schedule monitoring, forecasting, and management decision-making**.

---

## 📌 Project Overview

Construction projects generate large volumes of cost, schedule, quantity, billing, and progress data. However, raw project data does not automatically provide useful management insight.

This project builds an analytics workflow that answers practical project-control questions such as:

* Are projects progressing according to plan?
* Which projects and work categories experience higher delays?
* Where are the largest cost variances?
* How are schedule and cost performance changing over time?
* Which projects are showing signs of schedule or cost pressure?
* Can historical project data be used to predict future delay risk?
* Can next-month project cost and progress be forecast?
* How can project analytics be converted into a management dashboard?

---

## 🎯 Business Objectives

The analysis focuses on five major areas:

### 1. Project Performance Analysis

Analyze planned versus actual progress, cost, and delay performance.

### 2. Cost & Schedule Control

Identify projects experiencing cost overruns and schedule slippage.

### 3. Earned Value Management

Use **PV, EV, AC, SV, CV, SPI, and CPI** to evaluate project performance.

### 4. Predictive Analytics

Develop machine-learning models for:

* Next-month delay risk
* Next-month project cost
* Next-month project progress

### 5. Management Intelligence

Convert analytical results into a **Power BI project-controls dashboard** and an AI-ready project intelligence prototype.

---

## 🗂️ Dataset

The project uses a **synthetic construction-project dataset** designed to resemble realistic project-control information.

The dataset contains information related to:

* Projects
* Contractors
* Work categories
* Contract values
* Planned progress
* Actual progress
* Planned cost
* Actual cost
* Delay
* Monthly project performance
* Earned Value Management metrics

> **Note:** The dataset is simulated/synthetic and does not contain confidential project or client information.

---

## 🔎 Analytical Workflow

```text
Construction Project Data
          │
          ▼
    Data Preparation
          │
          ▼
 Exploratory Data Analysis
          │
          ├──────────────► Statistical Analysis
          │
          ├──────────────► SQL Analysis
          │
          ├──────────────► Earned Value Analysis
          │
          ▼
   Machine Learning
          │
          ├── Delay Risk Prediction
          ├── Cost Forecasting
          └── Progress Forecasting
          │
          ▼
   Project Intelligence
          │
          ▼
      Power BI
   Project Controls
     Dashboard
```

---

## 🧰 Technologies & Skills

### Programming & Data

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SciPy

### Machine Learning

* Scikit-learn
* Logistic Regression
* Random Forest
* Gradient Boosting
* Regression
* Classification
* Feature Engineering
* Model Evaluation
* Cross-validation concepts

### Analytics

* Exploratory Data Analysis
* Statistical Analysis
* Correlation Analysis
* Predictive Modeling
* Time-series / chronological modeling
* Risk Analysis
* Forecasting

### SQL

* SQLite
* Aggregation
* GROUP BY
* Filtering
* Project-level analytical queries

### Project Controls

* Planned Value (PV)
* Earned Value (EV)
* Actual Cost (AC)
* Schedule Variance (SV)
* Cost Variance (CV)
* Schedule Performance Index (SPI)
* Cost Performance Index (CPI)

### Visualization & BI

* Power BI
* DAX
* Data Visualization
* Management Dashboards

---

# 📊 Key Analysis

## 1. Project Performance

The analysis compares planned and actual project progress to identify projects performing behind, on, or ahead of plan.

Key metrics include:

* Planned Progress %
* Actual Progress %
* Progress Variance %
* Average Delay
* Schedule Status

---

## 2. Cost Analysis

Project cost performance is evaluated using planned versus actual expenditure.

Key metrics include:

* Planned Cost
* Actual Cost
* Cost Variance
* Cost Variance %
* Cost Performance Index

---

## 3. Earned Value Management

The project implements standard EVM metrics:

| Metric | Description                |
| ------ | -------------------------- |
| PV     | Planned Value              |
| EV     | Earned Value               |
| AC     | Actual Cost                |
| SV     | Schedule Variance          |
| CV     | Cost Variance              |
| SPI    | Schedule Performance Index |
| CPI    | Cost Performance Index     |

Interpretation:

* **SPI < 1** → progressing slower than planned
* **SPI > 1** → progressing faster than planned
* **CPI < 1** → cost efficiency is unfavorable
* **CPI > 1** → cost efficiency is favorable

The Power BI dashboard uses the latest available project-month values for the portfolio-level EVM view.

---

# 🤖 Machine Learning

## Project 1 — Next-Month Delay Risk Prediction

A classification problem was developed to estimate whether a project is likely to experience **high delay risk in the following month**.

### Models evaluated

* Logistic Regression
* Random Forest
* Gradient Boosting

### Evaluation metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC

The modeling workflow uses chronological project data to avoid using future observations when predicting future risk.

---

## Project 2 — Construction Cost Forecasting

A regression problem was developed to predict **next-month actual project cost**.

### Models evaluated

* Linear Regression
* Random Forest
* Gradient Boosting

### Evaluation metrics

* MAE
* RMSE
* R²

The objective is to provide an early indication of expected project expenditure and support proactive cost control.

---

## Project 3 — Project Progress Forecasting

A regression model predicts **next-month actual project progress**.

### Models evaluated

* Linear Regression
* Random Forest
* Gradient Boosting

### Evaluation metrics

* MAE
* RMSE
* R²

This provides a forward-looking view of expected project progress rather than relying only on historical reporting.

---

# 📈 Power BI Dashboard

The project includes a Power BI **Project Controls Dashboard** designed for management-level project monitoring.

### Dashboard pages

**1. Executive Overview**

* Total Contract Value
* Actual Progress
* Progress Variance
* Actual Cost
* Cost Variance
* Average Delay
* Planned vs Actual Progress
* Planned vs Actual Cost

**2. Cost & EVM**

* PV
* EV
* AC
* CV
* SV
* SPI
* CPI
* EVM trends

**3. Schedule & Risk**

* Schedule Performance Index
* Schedule Status
* Average Project Delay
* Latest Delay-Risk Probability

**4. Forecasting**

* Next-month cost prediction
* Next-month progress prediction
* Forecast bias
* Project-level forecast comparison

---

## 🧠 AI-Ready Project Intelligence

The project also contains an **AI-ready project intelligence prototype**.

It combines project-control indicators to identify:

* Schedule risk
* Cost pressure
* Delay risk
* Recommended management actions

Example logic:

```text
Low SPI + High Delay Risk
        ↓
Schedule Risk
        ↓
Review Critical Activities
        ↓
Evaluate Recovery Actions
```

This component is intentionally presented as an **AI-ready analytical prototype**, rather than a deployed Generative AI or RAG system.

---

# 📁 Repository Structure

```text
construction-project-analytics/
│
├── README.md
├── requirements.txt
│
├── notebooks/
│   ├── Construction Project Analytics & Predictive Modeling.ipynb
│   ├── random_forest_feature_importance.png
│   └── random_forest_permutation_importance.png
│
├── outputs/
│   ├── project_controls_dashboard.csv
│   ├── project_summary.csv
│   ├── category_summary.csv
│   ├── evm_project_summary.csv
│   ├── cost_forecast_output.csv
│   ├── progress_forecast_output.csv
│   └── project_intelligence_output.csv
│
├── visualizations/
│   ├── 01_project_progress_variance.png
│   ├── 02_contractor_progress_variance.png
│   ├── 03_correlation_matrix.png
│   ├── 04_evm_pv_ev_ac_trend.png
│   ├── 05_delay_model_comparison.png
│   ├── 06_delay_risk_roc_curve.png
│   ├── 07_delay_risk_pr_curve.png
│   ├── 08_cost_actual_vs_predicted.png
│   ├── 09_progress_actual_vs_predicted.png
│   ├── 10_latest_project_spi.png
│   ├── 11_project_delay_risk.png
│   └── 12_category_average_delay.png
│
├── Construction_Project_Controls.pbix
└── Construction_Project_Controls.pdf
```

---

# 📌 Key Business Findings

The analysis demonstrates several practical project-control insights:

* Planned and actual progress can be compared systematically to identify schedule slippage.
* Cost variance provides an early indicator of projects under financial pressure.
* EVM metrics provide a standardized view of schedule and cost efficiency.
* Projects can exhibit different combinations of schedule and cost performance.
* Machine-learning models can provide forward-looking risk and forecast indicators.
* Forecast bias helps identify whether predictions systematically overestimate or underestimate future performance.
* Combining predictive analytics with project-control KPIs creates a stronger management decision-support system than relying on historical reporting alone.

---

# ⚠️ Limitations

This project is a portfolio demonstration using synthetic data.

Important limitations include:

* The dataset is simulated rather than sourced from live projects.
* The dataset does not contain detailed activity-level schedules.
* Critical-path and total-float information is not available.
* Model performance on synthetic data should not be interpreted as production performance.
* External factors such as weather, procurement delays, design changes, contractor capacity, and regulatory issues are not explicitly modeled.
* The AI-ready component is a prototype and is not a deployed Generative AI/RAG application.

A production implementation would require validated historical project data and additional features such as:

* Activity-level schedules
* Baseline revisions
* Resource utilization
* Procurement status
* Material availability
* Change orders
* Weather information
* Contractor performance history
* Critical-path and float information

---

# 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/rb-ananth/construction-project-analytics.git
cd construction-project-analytics
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch Jupyter:

```bash
jupyter notebook
```

Open:

```text
notebooks/Construction Project Analytics & Predictive Modeling.ipynb
```

---

# 💼 Portfolio Relevance

This project demonstrates the combination of **data science skills and real-world construction/project-controls domain knowledge**.

It is particularly relevant to roles involving:

* Data Scientist
* Data Analyst
* Business Analyst
* Project Controls Analyst
* Project Analytics
* Predictive Analytics
* Business Intelligence
* Cost Analytics
* Risk Analytics

The project demonstrates an end-to-end workflow from **raw project data to statistical analysis, machine learning, forecasting, EVM, and management reporting**.

---

## 👤 Author

**Ananth RB**

Data Scientist | Business Analyst | Construction Analytics

Core interests:

`Python` · `SQL` · `Machine Learning` · `Data Analytics` · `Predictive Modeling` · `Power BI` · `Project Analytics`

---

⭐ If you find this project useful, feel free to explore the notebook, dashboard, and analytical outputs.
