# Forensic Audit Prompt 03: Report Telemetry & Usage Triage

> **What these files are.** Refined prompt templates as they stand *after* the
> assessment. They are **not** transcripts of the runs that produced the
> deliverables. The prompts actually issued are quoted verbatim in
> `AI_WORKFLOW.md` §2, and where a template here differs from the §2 text, the
> difference is a correction made in response to a failure documented in §3 —
> not a record of what was asked at the time.
>
> This matters most for template 04. It now carries a peak-trading blackout and
> a first-business-day-of-month rule. `AI_WORKFLOW.md` §3.5 records that the
> **absence** of exactly those two constraints is why the model returned 30
> November, a date that split the accounting month and landed the cutover on
> Black Friday. Reading this file as evidence of what was asked would invert
> that finding.

---

## Objective
Apply Pareto triage across the legacy reporting catalogue to distinguish business-critical reports from ghost/dormant reports, identify source architecture vulnerabilities (e.g. shadow IT Excel extracts), and audit telemetry data integrity.

## Target Artifacts
- `artifacts/report-usage.csv`

## System Prompt / Instructions
```text
Write and run a Python script over report-usage.csv.
Tier reports by usage:
- Zero views in the last 12 months
- Active reports viewed in 2026
- Dormant reports (viewed before 2026)

Calculate:
1. Cumulative share of views captured by the active 2026 tier.
2. Number and percentage of zero-view ghost reports.
3. Reports sourced from shadow IT Excel extracts versus the enterprise data warehouse.
4. Data integrity check: flag any reports where views_last_12m > 0 but last_viewed is older than 12 months.
```

## Deterministic Guardrail Check
Verified by `src/mythril/domain/telemetry.py`:
- `Total reports == 120 | Total views == 2,309`
- `Zero-view reports == 56 (46.67% of catalogue)`
- `Active 2026 reports == 38 (holding 2,270 views, 98.31% of all usage)`
- `Dormant reports == 26 (holding 39 views, max 2 views)`
- `Telemetry contradiction == 19 reports with views > 0 but last_viewed < 2025-08-31`
- `Excel-sourced active reports == 10 of the 38 Day-One scope reports`
- `Studio scorecards == 6 in catalogue, 0 viewed in 2026, 6 total lifetime views`
