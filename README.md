# Construction Project Analytics

A Python-based construction project analytics and performance monitoring project using simulated project-control data.

The project combines construction project management concepts with data analytics to evaluate schedule performance, cost performance, work-package delays, contractor performance, and Earned Value Management (EVM).

---

## Project Overview

Construction projects generate large amounts of schedule, cost, progress, and contractor-performance data. Converting this information into actionable management insights is essential for identifying emerging delays, cost pressures, and underperforming work packages.

This project demonstrates how Python, Pandas, NumPy, and Matplotlib can be used to transform project-control data into structured KPIs, EVM metrics, and management-oriented visualizations.

The analytical approach is based on construction project-control concepts and uses simulated data designed to reflect realistic project conditions.

---

## Key Business Questions

The analysis addresses five core project-management questions:

1. How closely does actual progress track planned progress?
2. Which work categories experience the highest delays?
3. Where are the largest cost variances occurring?
4. How does project performance change over time?
5. Which contractors demonstrate stronger schedule and cost performance?

---

## Analysis Approach

The project follows a project-control analytics workflow:

1. Generate realistic project and work-package data
2. Establish planned progress and cost baselines
3. Model actual progress, cost, and delays
4. Calculate project and work-package KPIs
5. Aggregate performance to project-month level
6. Apply Earned Value Management (EVM)
7. Compare contractor performance
8. Identify high-risk work packages and projects
9. Visualize performance trends and relationships

---

## Key Performance Indicators

### Progress Performance

- Planned progress (%)
- Actual progress (%)
- Progress variance (percentage points)

### Cost Performance

- Planned cost
- Actual cost
- Cost variance (₹ Cr)
- Cost variance (%)

### Schedule Performance

- Delay days
- Schedule variance

### Earned Value Management

- Planned Value (PV)
- Earned Value (EV)
- Actual Cost (AC)
- Schedule Variance (SV)
- Cost Variance (CV)
- Schedule Performance Index (SPI)
- Cost Performance Index (CPI)

---

## Earned Value Management

The project uses standard EVM concepts to evaluate schedule and cost efficiency.

### Planned Value (PV)

Budgeted value of work planned to be completed.

### Earned Value (EV)

Budgeted value of work actually completed.

### Actual Cost (AC)

Actual expenditure incurred.

### Schedule Performance Index

```text
SPI = EV / PV
```
