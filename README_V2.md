# Construction Project Analytics & Predictive Modelling — Version 2

Version 2 is an additive upgrade. The original Version 1 notebook is preserved byte-for-byte in `archive_v1/` and is not overwritten.

## Version 2 scope

- 30 synthetic projects
- 10 work categories per project
- 24 monthly reporting periods
- 7,200 project × work-category × month observations
- Explicit separation of monthly expenditure and cumulative expenditure
- Explicit separation of monthly progress increments and cumulative physical progress
- Construction-control drivers: labour shortage, procurement delay, design changes, material-price index and rainfall
- EVM measures calculated from cumulative planned value, earned value and actual cost
- Data-quality checks for grain, progress monotonicity, cost reconciliation and package-budget reconciliation

## Repository layout

```text
Construction_Project_Analytics_V2/
├── README_V2.md
├── requirements.txt
├── archive_v1/
│   └── Ananth_RB_Construction_Project_Analytics_FINAL.ipynb
├── data_v2/
│   └── construction_project_monthly_v2.csv
├── notebooks/
│   └── Construction_Project_Analytics_V2.ipynb
├── outputs_v2/
│   ├── data_dictionary_v2.csv
│   ├── data_quality_report_v2.csv
│   └── visualizations/
└── src/
    └── synthetic_data.py
```

## Run locally (macOS / VS Code)

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/Construction_Project_Analytics_V2.ipynb` and run all cells.

## Important modelling guardrails

1. The dataset is synthetic. Metrics are demonstrations on simulated data, not evidence of real-world construction performance.
2. `actual_cost_month_cr` is monthly expenditure. `cumulative_actual_cost_cr` is the running total. Do not use these interchangeably.
3. `actual_progress_increment_pct` is monthly progress added. `actual_progress_pct` is cumulative physical progress.
4. `risk_state_simulated` and `productivity_factor_simulated` are simulator-only diagnostic fields. They must be excluded from model features because they would not be observable in a real project.
5. A 12-day next-month delay threshold is a modelling convention for this portfolio exercise, not an industry-wide contractual definition.
6. Next-month baseline progress and cost are assumed to be available from the approved baseline schedule/budget at the forecast origin. They may be used as known-future plan features, but not as actual future outcomes.
7. Version 2 modelling will use chronological training, validation and test windows. No random row split will be used for the forecasting use cases.

## Version 1 preservation

The archived Version 1 notebook is an exact copy of the original source file. Its SHA-256 is recorded in `V1_PRESERVATION_SHA256.txt`.
