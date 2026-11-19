# Construction Project Analytics & Predictive Modelling — V2

An end-to-end construction analytics and predictive modelling portfolio project that applies data science techniques to project controls, cost forecasting, schedule-risk detection and PMC investigation prioritisation.

Version 2 is an additive upgrade. The original Version 1 notebook is preserved byte-for-byte in `archive_v1/` and is not overwritten.

---

## 1. Business Problem

Construction project management consultants and project-control teams routinely monitor multiple projects, contractors and work packages.

Traditional project monitoring relies heavily on periodic progress reports, approved schedules, expenditure statements and manual analysis.

This creates several challenges:

- Identifying work packages likely to experience future delays.
- Estimating next-month expenditure instead of relying only on historical spending.
- Forecasting physical progress against the approved programme.
- Identifying packages with significant schedule and budget exposure.
- Prioritising limited engineering resources for risk investigation.
- Converting historical project information into actionable management insights.

### Project objective

Develop a construction analytics system that uses historical project data, execution conditions and Earned Value Management (EVM) indicators to:

1. Predict next-month delay risk.
2. Forecast next-month expenditure.
3. Forecast next-month physical progress increments.
4. Rank flagged work packages for PMC investigation.
5. Provide a structured, data-driven basis for project-control decisions.

The objective is decision support, not autonomous project management.

---

## 2. Solution Overview

The V2 workflow consists of five major components.

| Component                       | Purpose                                                       |
| ------------------------------- | ------------------------------------------------------------- |
| Synthetic construction dataset  | Simulate project, contractor and work-package performance     |
| Data quality and EVM validation | Check data integrity and construction-control calculations    |
| Delay-risk classification       | Predict whether a package will experience a significant delay |
| Cost and progress forecasting   | Estimate next-month expenditure and physical progress         |
| PMC risk prioritisation         | Rank flagged packages against investigation capacity          |

### Analytical workflow

```text
Synthetic Construction Data
          |
          v
Data Quality Validation
          |
          v
Feature Engineering
          |
          v
Chronological Data Splitting
          |
          +----------------------+
          |                      |
          v                      v
Delay Classification      Cost & Progress
          |                 Forecasting
          v                      |
Delay Probability               v
          |                Forecast Outputs
          v                      |
Risk & Impact Ranking           |
          |                      |
          v                      v
Capacity-Constrained PMC Investigation
          |
          v
Actionable Risk Register
```

---

## 3. Dataset Design

The dataset represents a simulated construction portfolio.

| Attribute           | Description                     |
| ------------------- | ------------------------------- |
| Projects            | 30                              |
| Contractors         | 6                               |
| Work categories     | 10                              |
| Reporting frequency | Monthly                         |
| Reporting period    | January 2025 – December 2026    |
| Total observations  | 7,200                           |
| Dataset columns     | 32                              |
| Observation grain   | Project × Work Category × Month |

### Work categories

- Earthwork
- RCC
- Masonry
- Plastering
- Flooring
- Electrical
- Plumbing
- HVAC
- Fire Fighting
- External Works

### Construction execution variables

The dataset includes:

- Planned and actual monthly progress increments.
- Planned and actual cumulative progress.
- Planned and actual monthly expenditure.
- Cumulative actual expenditure.
- Package budget and project contract value.
- Delay days.
- Labour shortage percentage.
- Procurement delay days.
- Design change count.
- Material price index.
- Rainfall.

The generator incorporates temporal risk behaviour, project-level characteristics, work-package budgets and execution-related productivity and cost pressures.

**Reproducibility:** The synthetic data generator uses a fixed random seed of 42.

---

## 4. Data Semantics and EVM

A key correction in V2 is the explicit distinction between monthly flows and cumulative measures.

| Variable                         | Meaning                                             |
| -------------------------------- | --------------------------------------------------- |
| `planned_progress_increment_pct` | Planned progress during the reporting month         |
| `actual_progress_increment_pct`  | Actual progress achieved during the reporting month |
| `planned_progress_pct`           | Planned cumulative physical progress                |
| `actual_progress_pct`            | Actual cumulative physical progress                 |
| `planned_cost_month_cr`          | Planned monthly expenditure                         |
| `actual_cost_month_cr`           | Actual monthly expenditure                          |
| `cumulative_actual_cost_cr`      | Cumulative actual expenditure                       |

This distinction prevents a common modelling error: forecasting cumulative expenditure or cumulative progress when the intended target is the next month's increment.

### Earned Value Management

The dataset calculates:

- PV — Planned Value
- EV — Earned Value
- AC — Actual Cost
- SV — Schedule Variance
- CV — Cost Variance
- SPI — Schedule Performance Index
- CPI — Cost Performance Index

Formulas:

- SV = EV − PV
- CV = EV − AC
- SPI = EV / PV
- CPI = EV / AC

SPI and CPI are left undefined where their denominators are zero.

---

## 5. Data Quality and Validation

The enhanced validation function in `src/synthetic_data.py` checks:

- Duplicate project/work-category/month combinations.
- Invalid reporting months.
- Unexpected missing and non-finite values.
- Negative monthly costs and progress increments.
- Negative delay values.
- Progress boundaries and cumulative monotonicity.
- Planned and actual cumulative progress reconciliation.
- Cumulative expenditure reconciliation.
- Package-budget reconciliation with project contract values.
- EVM formula reconciliation.
- SPI and CPI missingness against zero denominators.

### Validation results

| Validation measure            | Result |
| ----------------------------- | -----: |
| Total rows                    |  7,200 |
| Duplicate grain observations  |      0 |
| Unexpected missing values     |      0 |
| Invalid reporting months      |      0 |
| Negative monthly costs        |      0 |
| Negative delay values         |      0 |
| Progress-bound violations     |      0 |
| Cumulative progress decreases |      0 |
| Cumulative cost decreases     |      0 |
| Maximum reconciliation errors |      0 |

There are 896 expected missing EVM ratio values: 448 missing SPI values where PV is zero and 448 missing CPI values where AC is zero.

These values are mathematically undefined and are not replaced with zero.

---

## 6. Feature Engineering and Predictive Dataset

The supervised dataset is created using chronological next-month targets.

### Prediction targets

**Delay classification**

`target_delay_next_month`

A binary target indicating whether next-month delay reaches or exceeds 12 days.

The 12-day threshold is a modelling convention for this portfolio exercise, not a universal contractual definition.

**Cost forecasting**

`target_cost_next_month_cr`

Next-month actual monthly expenditure.

**Progress forecasting**

`target_progress_next_month_pct`

Next-month actual physical progress increment.

### Feature engineering

The feature set includes:

- Current project and package characteristics.
- Contractor and work-category identifiers.
- Current execution and EVM indicators.
- Lagged execution variables.
- Three-month rolling averages.
- Seasonal month features.
- Approved next-month planned cost and progress.

The final feature list contains 41 model features:

- 3 categorical features.
- 38 numerical features.

Simulator-only variables `risk_state_simulated` and `productivity_factor_simulated` are excluded from predictive features.

### Leakage controls

- Future actual outcomes are used only as target variables.
- Targets are generated using a one-month forward shift within each project/work-category combination.
- Final-month observations without next-month targets are excluded.
- Lag and rolling features use historical information through the forecast origin.
- Approved next-month plans are treated as known-future inputs only under the assumption that they are approved and available at forecast time.
- Chronological rather than random train/test splitting is used.

### Temporal split

| Split      | Observations | Forecast-origin period |
| ---------- | -----------: | ---------------------- |
| Training   |        4,500 | Jan 2025 – Mar 2026    |
| Validation |        1,200 | Apr 2026 – Jul 2026    |
| Test       |        1,200 | Aug 2026 – Nov 2026    |
| **Total**  |    **6,900** |                        |

The validation period is used for model and threshold selection. The held-out test period is reserved for final evaluation.

---

## 7. Delay-Risk Classification

### Objective

Predict whether a work package will experience a next-month delay of at least 12 days.

### Candidate models

- Logistic Regression
- Random Forest Classifier

The preprocessing pipeline includes:

- Median imputation for numerical features.
- Standardisation of numerical features.
- Most-frequent imputation for categorical features.
- One-hot encoding for categorical variables.

### Model selection

Average Precision is used to compare candidate models on validation data.

The selected Random Forest model uses a threshold of 0.28, selected using validation F2.

F2 gives greater importance to recall, which is relevant to an early-warning system where missing a potential delay can be costly.

### Held-out test results

| Metric             | Result |
| ------------------ | -----: |
| Accuracy           | 61.25% |
| Precision          | 49.75% |
| Recall             | 86.77% |
| F1                 |  0.632 |
| F2                 |  0.755 |
| ROC-AUC            |  0.771 |
| Average Precision  |  0.669 |
| Test positive rate | 38.42% |

### Test confusion matrix

| Actual / Predicted | No delay | Delay |
| ------------------ | -------: | ----: |
| No delay           |      335 |   404 |
| Delay              |       61 |   400 |

The model identifies 400 delayed observations and misses 61. It also produces 404 false alerts.

The model is therefore designed as a high-recall screening mechanism rather than an automatic confirmation of delay.

Threshold operating-point comparisons are generated separately using validation predictions.

---

## 8. PMC Risk Prioritisation

### Business problem

A PMC team may have more flagged work packages than it can investigate during a reporting cycle.

The risk-prioritisation component ranks flagged observations and selects a capacity-constrained investigation list.

### Impact proxy

The impact proxy combines:

- Package budget percentile: 70%
- Schedule-gap percentile: 30%

Conceptually:

`Impact Proxy = 0.70 × Budget Percentile + 0.30 × Schedule-Gap Percentile`

The priority score is:

`Priority Score = Predicted Delay Probability × Impact Proxy`

This is a transparent heuristic for ranking. It is not a calibrated financial-loss estimate, critical-path impact calculation or contractual damages estimate.

### Investigation capacity

The configured investigation capacity is 30% of monthly observations.

With 300 observations per month, this provides 90 investigation slots.

### Test-period results

| Measure                        | Result |
| ------------------------------ | -----: |
| Test observations              |  1,200 |
| Flagged observations           |    804 |
| Selected for investigation     |    360 |
| Flagged backlog                |    444 |
| Monthly investigation capacity |     90 |
| Investigation capacity share   |    30% |

| Month    | Flagged | Selected | Backlog |
| -------- | ------: | -------: | ------: |
| Aug 2026 |     177 |       90 |      87 |
| Sep 2026 |     202 |       90 |     112 |
| Oct 2026 |     205 |       90 |     115 |
| Nov 2026 |     220 |       90 |     130 |

The risk register was verified to select exactly the top 90 flagged observations by priority score in each month.

The same project/work-category combination may appear in multiple months. These are monthly forecast observations, not necessarily unique physical packages or new investigations.

### Operational limitation

The current implementation does not maintain a persistent investigation lifecycle. A production system should distinguish new alerts from unresolved risks and track assignment, corrective action, monitoring, resolution and reopening.

---

## 9. Cost and Progress Forecasting

### Objective

Forecast next-month monthly expenditure and next-month physical progress increments.

### Candidate models

- Random Forest Regressor
- Extra Trees Regressor

Model selection is based on validation MAE, separately for cost and progress.

The selected regression models are retrained using the combined training and validation datasets before final test evaluation.

### Baselines

Two conventional baselines are used:

1. **Approved-plan baseline:** Next-month planned cost or progress increment.
2. **Persistence baseline:** Current-month actual cost or progress increment carried forward.

These baselines help establish whether machine learning adds value beyond the approved plan and a simple historical assumption.

### Cost forecasting — held-out test

| Metric         | Random Forest | Approved-plan baseline | Persistence baseline |
| -------------- | ------------: | ---------------------: | -------------------: |
| MAE (₹ crore)  |      0.001778 |               0.004264 |             0.017831 |
| RMSE (₹ crore) |      0.006070 |               0.013397 |             0.039065 |
| R²             |        0.9919 |                 0.9605 |               0.6640 |
| WAPE           |         6.85% |                 16.42% |               68.66% |

Random Forest reduces MAE by approximately 58.3% compared with the approved-plan baseline.

### Progress forecasting — held-out test

| Metric                   | Random Forest | Approved-plan baseline | Persistence baseline |
| ------------------------ | ------------: | ---------------------: | -------------------: |
| MAE (percentage points)  |       0.05651 |                0.09957 |              0.32631 |
| RMSE (percentage points) |       0.15270 |                0.26756 |              0.61772 |
| R²                       |        0.9707 |                 0.9101 |               0.5207 |
| WAPE                     |        12.95% |                 22.81% |               74.76% |

Random Forest reduces MAE by approximately 43.2% compared with the approved-plan baseline.

### Interpretation

The models demonstrate the ability to estimate next-month outcomes using execution history, risk drivers and approved-plan information.

The improvements are measured on the simulated held-out test set. They should not be interpreted as demonstrated accuracy on real construction projects.

---

## 10. Forecasting Data Diagnostics and Limitations

The test dataset contains a high proportion of zero-activity observations.

| Diagnostic          |    Cost |                Progress |
| ------------------- | ------: | ----------------------: |
| Test observations   |   1,200 |                   1,200 |
| Zero observations   |     928 |                     934 |
| Zero percentage     |  77.33% |                  77.83% |
| Active observations |     272 |                     266 |
| Active-only MAE     | ₹69,310 | 0.199 percentage points |
| Inactive-only MAE   |  ₹2,680 | 0.016 percentage points |

The overall regression metrics must be interpreted in light of this zero-inflated distribution.

Across all 7,200 source observations, zero-cost and zero-progress indicators agree in 99.82% of cases.

The synthetic generator therefore couples expenditure activity and physical progress activity very closely. This is simpler than real construction execution, where procurement, labour deployment, payments and physical progress can occur at different times.

A two-stage activity-classification and conditional-regression approach may be explored as a future experiment. The existing Random Forest models are retained as the current benchmark.

### Other limitations

- All source observations are synthetic.
- Project and contractor identities occur across training, validation and test periods; unseen-project generalisation has not been established.
- The data does not contain activity-level schedules, critical-path logic or total float.
- The impact proxy is heuristic and is not validated against actual project consequences.
- The current model does not explicitly classify work-package operational states such as not started, temporarily stalled and completed.
- Approved next-month plan features assume that the relevant schedule and budget versions are available at forecast time.
- The generator couples several execution drivers and outcomes by design.

### Future enhancements

- Validate the workflow using historical project data.
- Introduce activity-level schedule and critical-path information.
- Add resource and procurement status.
- Capture baseline revisions and change orders.
- Improve cost/progress activity modelling.
- Introduce persistent risk-investigation lifecycle tracking.
- Evaluate generalisation to previously unseen projects.
- Explore two-stage forecasting and alternative model architectures.
- Validate impact prioritisation against actual project outcomes.

---

## 11. Repository Structure

```text
construction-project-analytics/
│
├── README_V2.md
├── requirements.txt
│
├── archive_v1/
│   └── Ananth_RB_Construction_Project_Analytics_FINAL.ipynb
│
├── data_v2/
│   └── construction_project_monthly_v2.csv
│
├── notebooks/
│   └── Construction_Project_Analytics_V2.ipynb
│
├── src/
│   └── synthetic_data.py
│
└── outputs_v2/
    ├── data_dictionary_v2.csv
    ├── data_quality_report_v2.csv
    ├── project_month_summary_v2.csv
    ├── supervised_next_month_dataset_v2.csv
    ├── delay_model_feature_list_v2.csv
    ├── temporal_split_summary_v2.csv
    ├── delay_classifier_validation_comparison_v2.csv
    ├── delay_classifier_threshold_selection_v2.csv
    ├── delay_classifier_test_metrics_v2.csv
    ├── delay_model_permutation_importance_v2.csv
    ├── delay_probability_calibration_v2.csv
    ├── delay_threshold_operating_points_v2.csv
    ├── risk_prioritisation_register_v2.csv
    ├── risk_prioritisation_summary_v2.csv
    ├── risk_prioritisation_capacity_summary_v2.csv
    ├── regression_validation_model_comparison_v2.csv
    ├── regression_baseline_metrics_v2.csv
    ├── regression_test_metrics_v2.csv
    ├── regression_monthly_errors_v2.csv
    ├── regression_forecasting_summary_v2.csv
    ├── cost_forecast_test_evaluation_v2.csv
    ├── progress_forecast_test_evaluation_v2.csv
    └── visualizations/
```

---

## 12. Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Git and GitHub

---

## 13. Run Locally

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook
```

Open:

```text
notebooks/Construction_Project_Analytics_V2.ipynb
```

Run the notebook cells sequentially.

The notebook generates the supervised datasets, model evaluations, risk registers, forecasting outputs and visualisations under `outputs_v2/`.

---

## 14. Portfolio Relevance

This project demonstrates an end-to-end applied data science workflow in a specialised business domain.

It combines construction and project-controls knowledge with:

- Data generation and validation.
- Exploratory data analysis.
- Feature engineering.
- Data leakage prevention.
- Classification and regression.
- Model selection and evaluation.
- Time-aware validation.
- Baseline comparisons.
- Risk prioritisation.
- Business interpretation.

It is relevant to roles involving:

- Data Scientist
- Data Analyst
- Business Analyst
- Project Controls Analyst
- Predictive Analytics
- Construction Analytics
- Cost Analytics
- Risk Analytics
- Business Intelligence

**The central value of this project is the translation of construction project-control problems into measurable analytical tasks and decision-support workflows.**
