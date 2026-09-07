# Forensic Audit Prompt 01: Financial Reconciliation

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
Forensically audit the parallel-run reconciliation report between legacy enterprise data warehouse and the new cloud platform to evaluate whether the 5% tolerance threshold holds up to financial audit standards.

## Target Artifacts
- `artifacts/reconciliation-2026-08-28.md`

## System Prompt / Instructions
```text
Inspect artifacts/reconciliation-2026-08-28.md.
Compare the summary table against the detail appendix.
Calculate exact dollar and percentage deltas by quarter and month.
Evaluate the agreed ±5% tolerance threshold from an executive and statutory accounting perspective.

Key questions:
1. What is the net annual revenue variance across FY2026?
2. Which specific periods account for this variance?
3. What is the row-level delta in fact_order and the implied dollar amount per phantom order?
4. Would a statutory financial audit accept an aggregate annual ±5% tolerance when individual monthly figures swing by double digits?
```

## Deterministic Guardrail Check
Verified by `src/mythril/domain/reconciliation.py`:
- `FY2026 variance in USD == $59,724.92 (+4.05%)`
- `March 2026 variance in USD == $59,724.92 (+49.82%)`
- `Phantom order count == 2,998 orders ($19.9216 / order)`
- `Clean periods reconciling at 0.00%: Q1, Q3, Jan 2026, Feb 2026, Titles, Storefronts`
