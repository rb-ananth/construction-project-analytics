"""Reproducible synthetic construction project-control data generator.

All records are simulated. No real client, contractor, or project information is used.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

WORK_CATEGORY_WEIGHTS = {
    "Earthwork": 0.05,
    "RCC": 0.22,
    "Masonry": 0.10,
    "Plastering": 0.07,
    "Flooring": 0.06,
    "Electrical": 0.14,
    "Plumbing": 0.08,
    "HVAC": 0.11,
    "Fire Fighting": 0.06,
    "External Works": 0.11,
}


def _planned_progress_curve(duration: int) -> np.ndarray:
    """Return a smooth, normalized S-curve-like monthly progress profile."""
    x = np.linspace(0.0, 1.0, duration)
    weights = 0.30 + 4.0 * x * (1.0 - x)
    return weights / weights.sum() * 100.0


def generate_construction_dataset(
    seed: int = 42,
    n_projects: int = 30,
    n_months: int = 24,
) -> pd.DataFrame:
    """Generate monthly project × work-package observations.

    The generated dataset deliberately separates monthly expenditure from
    cumulative expenditure and monthly progress increments from cumulative
    physical progress. This makes forecast targets unambiguous.
    """
    if n_projects < 6:
        raise ValueError("Use at least 6 projects for meaningful synthetic variation.")
    if n_months < 18:
        raise ValueError("Use at least 18 months for chronological model validation.")

    rng = np.random.default_rng(seed)
    months = pd.date_range("2025-01-01", periods=n_months, freq="MS")
    contractors = [f"Contractor {letter}" for letter in "ABCDEF"]
    records: list[dict] = []

    for project_number in range(1, n_projects + 1):
        project_id = f"PRJ-{project_number:03d}"
        project_name = f"Project {project_number:02d}"
        contractor = contractors[(project_number - 1) % len(contractors)]
        contract_value = float(rng.uniform(12.0, 65.0))
        project_risk_baseline = float(rng.beta(2.0, 3.0))
        project_productivity = float(np.clip(rng.normal(1.0, 0.06), 0.82, 1.18))
        project_cost_pressure = float(rng.normal(0.025, 0.02))

        # Project-level monthly conditions have temporal persistence.
        environment = []
        risk_state = project_risk_baseline
        material_price_index = 1.0
        for month_index, month in enumerate(months, start=1):
            risk_shock = rng.normal(0.0, 0.12)
            risk_state = float(np.clip(
                0.72 * risk_state + 0.28 * project_risk_baseline + risk_shock,
                0.0, 1.0,
            ))
            material_price_index = float(max(
                0.85,
                material_price_index + rng.normal(0.008, 0.018),
            ))
            labour_shortage_pct = float(np.clip(
                7.0 + 30.0 * risk_state + rng.normal(0.0, 5.5), 0.0, 65.0
            ))
            procurement_delay_days = int(max(
                0, rng.poisson(0.8 + 5.0 * risk_state)
            ))
            design_change_count = int(rng.poisson(0.10 + 0.55 * risk_state))
            rainfall_pattern = [5, 5, 10, 25, 80, 180, 220, 200, 130, 60, 20, 5]
            rainfall_mm = float(max(
                0.0,
                rainfall_pattern[(month.month - 1) % 12] + rng.normal(0.0, 18.0),
            ))
            environment.append({
                "risk_state_simulated": risk_state,
                "material_price_index": material_price_index,
                "labour_shortage_pct": labour_shortage_pct,
                "procurement_delay_days": procurement_delay_days,
                "design_change_count": design_change_count,
                "rainfall_mm": rainfall_mm,
            })

        # Slightly vary package allocations by project, then normalize to BAC.
        category_names = list(WORK_CATEGORY_WEIGHTS)
        raw_weights = np.array([
            WORK_CATEGORY_WEIGHTS[name] * rng.uniform(0.94, 1.06)
            for name in category_names
        ])
        normalized_weights = raw_weights / raw_weights.sum()

        for category, weight in zip(category_names, normalized_weights):
            package_budget = float(contract_value * weight)
            start_month_index = int(rng.integers(1, 5))
            duration = int(rng.integers(14, min(23, n_months - start_month_index + 2)))
            end_month_index = min(n_months, start_month_index + duration - 1)
            duration = end_month_index - start_month_index + 1
            planned_curve = _planned_progress_curve(duration)

            planned_increments = np.zeros(n_months, dtype=float)
            planned_increments[start_month_index - 1:end_month_index] = planned_curve
            planned_cumulative = np.minimum(np.cumsum(planned_increments), 100.0)

            actual_cumulative = 0.0
            cumulative_actual_cost = 0.0
            package_productivity = float(np.clip(rng.normal(1.0, 0.07), 0.80, 1.20))

            for month_offset, month in enumerate(months):
                month_index = month_offset + 1
                conditions = environment[month_offset]
                planned_increment = float(planned_increments[month_offset])

                labour_fraction = conditions["labour_shortage_pct"] / 100.0
                procurement_delay = conditions["procurement_delay_days"]
                design_changes = conditions["design_change_count"]
                rainfall = conditions["rainfall_mm"]

                productivity_factor = (
                    project_productivity
                    * package_productivity
                    * (1.0 - 0.45 * labour_fraction)
                    * max(0.65, 1.0 - 0.008 * procurement_delay)
                    * max(0.75, 1.0 - 0.035 * design_changes)
                    * max(0.85, 1.0 - 0.00015 * rainfall)
                    * rng.normal(1.0, 0.09)
                )
                productivity_factor = float(np.clip(productivity_factor, 0.30, 1.25))
                actual_increment = float(max(0.0, planned_increment * productivity_factor))
                actual_increment = min(actual_increment, 100.0 - actual_cumulative)
                actual_cumulative = float(actual_cumulative + actual_increment)

                planned_cumulative_pct = float(planned_cumulative[month_offset])
                planned_monthly_cost = float(package_budget * planned_increment / 100.0)
                cost_pressure = (
                    project_cost_pressure
                    + 0.12 * (conditions["material_price_index"] - 1.0)
                    + 0.20 * labour_fraction
                    + 0.012 * procurement_delay
                    + 0.06 * design_changes
                    + 0.025 * conditions["risk_state_simulated"]
                    + rng.normal(0.0, 0.035)
                )
                actual_monthly_cost = float(max(
                    0.0, planned_monthly_cost * (1.0 + cost_pressure)
                ))
                cumulative_actual_cost += actual_monthly_cost

                delay_days = int(max(
                    0,
                    round(
                        2.0
                        + 5.0 * conditions["risk_state_simulated"]
                        + 0.90 * procurement_delay
                        + 2.0 * design_changes
                        + 8.0 * labour_fraction
                        + rng.normal(0.0, 2.5)
                    ),
                ))

                records.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "contractor": contractor,
                    "work_category": category,
                    "month": month,
                    "month_index": month_index,
                    "contract_value_cr": contract_value,
                    "package_budget_cr": package_budget,
                    "baseline_start_month": start_month_index,
                    "baseline_duration_months": duration,
                    "planned_progress_increment_pct": planned_increment,
                    "planned_progress_pct": planned_cumulative_pct,
                    "actual_progress_increment_pct": actual_increment,
                    "actual_progress_pct": actual_cumulative,
                    "planned_cost_month_cr": planned_monthly_cost,
                    "actual_cost_month_cr": actual_monthly_cost,
                    "cumulative_actual_cost_cr": cumulative_actual_cost,
                    "delay_days": delay_days,
                    "labour_shortage_pct": conditions["labour_shortage_pct"],
                    "procurement_delay_days": procurement_delay,
                    "design_change_count": design_changes,
                    "material_price_index": conditions["material_price_index"],
                    "rainfall_mm": conditions["rainfall_mm"],
                    # Retained only to explain/test the simulation; excluded from ML features.
                    "risk_state_simulated": conditions["risk_state_simulated"],
                    "productivity_factor_simulated": productivity_factor,
                })

    data = pd.DataFrame.from_records(records)
    data = data.sort_values(
        ["project_id", "work_category", "month"]
    ).reset_index(drop=True)

    # Work-package EVM values, calculated from cumulative measures.
    data["PV_cr"] = data["package_budget_cr"] * data["planned_progress_pct"] / 100.0
    data["EV_cr"] = data["package_budget_cr"] * data["actual_progress_pct"] / 100.0
    data["AC_cr"] = data["cumulative_actual_cost_cr"]
    data["SV_cr"] = data["EV_cr"] - data["PV_cr"]
    data["CV_cr"] = data["EV_cr"] - data["AC_cr"]
    data["SPI"] = np.where(data["PV_cr"] > 0, data["EV_cr"] / data["PV_cr"], np.nan)
    data["CPI"] = np.where(data["AC_cr"] > 0, data["EV_cr"] / data["AC_cr"], np.nan)

    return data


def validate_construction_dataset(data: pd.DataFrame) -> dict:
    """Run structural and domain checks; return a compact quality report."""
    required = {
        "project_id", "project_name", "contractor", "work_category", "month", "month_index",
        "planned_progress_pct", "actual_progress_pct",
        "planned_progress_increment_pct", "actual_progress_increment_pct",
        "planned_cost_month_cr", "actual_cost_month_cr",
        "cumulative_actual_cost_cr", "delay_days", "PV_cr", "EV_cr", "AC_cr",
    }
    missing_columns = sorted(required - set(data.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    key = ["project_id", "work_category", "month"]
    duplicate_grain = int(data.duplicated(key).sum())
    grouped = data.groupby(["project_id", "work_category"], sort=False)
    actual_progress_diff = grouped["actual_progress_pct"].diff().dropna()
    planned_progress_diff = grouped["planned_progress_pct"].diff().dropna()
    cumulative_cost_diff = grouped["cumulative_actual_cost_cr"].diff().dropna()
    missing_columns_with_values = set(data.columns[data.isna().any()].tolist())
    unexpected_missing_columns = sorted(missing_columns_with_values - {"SPI", "CPI"})

    # Reconcile each project's work-package budgets to its contract value.
    package_budgets = data.drop_duplicates(["project_id", "work_category"])
    budget_by_project = package_budgets.groupby("project_id")["package_budget_cr"].sum()
    contract_by_project = package_budgets.groupby("project_id")["contract_value_cr"].first()
    budget_reconciliation_error = float((budget_by_project - contract_by_project).abs().max())

    # Reconcile cumulative cost to the running total of monthly expenditure.
    expected_cumulative_cost = grouped["actual_cost_month_cr"].cumsum()
    cumulative_cost_reconciliation_error = float(
        (data["cumulative_actual_cost_cr"].to_numpy() - expected_cumulative_cost.to_numpy()).__abs__().max()
    )

    checks = {
        "rows": int(len(data)),
        "columns": int(data.shape[1]),
        "projects": int(data["project_id"].nunique()),
        "work_categories": int(data["work_category"].nunique()),
        "reporting_months": int(data["month"].nunique()),
        "duplicate_grain_rows": duplicate_grain,
        "missing_cells": int(data.isna().sum().sum()),
        "columns_with_expected_missing_values": ", ".join(sorted(missing_columns_with_values)),
        "unexpected_missing_columns": ", ".join(unexpected_missing_columns),
        "negative_monthly_cost_rows": int((data["actual_cost_month_cr"] < 0).sum()),
        "negative_delay_rows": int((data["delay_days"] < 0).sum()),
        "actual_progress_out_of_bounds_rows": int((~data["actual_progress_pct"].between(0, 100)).sum()),
        "planned_progress_out_of_bounds_rows": int((~data["planned_progress_pct"].between(0, 100)).sum()),
        "actual_progress_decreases": int((actual_progress_diff < -1e-9).sum()),
        "planned_progress_decreases": int((planned_progress_diff < -1e-9).sum()),
        "cumulative_cost_decreases": int((cumulative_cost_diff < -1e-9).sum()),
        "max_project_budget_reconciliation_error_cr": budget_reconciliation_error,
        "max_cumulative_cost_reconciliation_error_cr": cumulative_cost_reconciliation_error,
    }
    checks["passed"] = bool(
        checks["duplicate_grain_rows"] == 0
        and checks["unexpected_missing_columns"] == ""
        and checks["negative_monthly_cost_rows"] == 0
        and checks["negative_delay_rows"] == 0
        and checks["actual_progress_out_of_bounds_rows"] == 0
        and checks["planned_progress_out_of_bounds_rows"] == 0
        and checks["actual_progress_decreases"] == 0
        and checks["planned_progress_decreases"] == 0
        and checks["cumulative_cost_decreases"] == 0
        and budget_reconciliation_error < 1e-8
        and cumulative_cost_reconciliation_error < 1e-8
    )
    return checks
