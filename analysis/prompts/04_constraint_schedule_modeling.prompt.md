# Forensic Audit Prompt 04: Constraint-Driven Schedule Modeling

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
Model a revised, defensible delivery schedule from 1 September 2026 respecting hard physical constraints, contractor capacity limits, retail peak-trading blackout windows, and statutory accounting boundaries.

## Target Artifacts
- `artifacts/project-plan.csv`
- `artifacts/resource-allocation.csv`
- `artifacts/vendor-notice.md`
- `artifacts/team-notes.md`

## System Prompt / Instructions
```text
Model a revised delivery schedule starting from 1 September 2026 under the following physical constraints:
- D. Whitlock approved PTO: 9–20 October 2026 inclusive (8 business days).
- Aggregator vendor freeze: 5–19 October 2026 inclusive (11 business days).
- Vendor storefront onboarding requirement: minimum 9 full working days without exceptions.
- Backfill task T03 effort is 12 working days and must cleanly split around Whitlock's PTO.
- Parallel run task T04 requires 10 working days; sign-off task T05 requires 2 working days.
- D. Whitlock cannot be double-allocated beyond 100% capacity.
- Peak trading window: Thanksgiving through Cyber Monday (26–30 November 2026) is strict operational blackout.
- Go-live boundary rule: Business go-live MUST land on the FIRST business day of an accounting month to avoid splitting the financial ledger.

Identify the earliest defensible go-live dates for both funded scenarios (Scenario A: November technical cutover / December business go-live; Scenario B: Year-end technical cutover / January business go-live).
```

## Deterministic Guardrail Check
Verified by `analysis/mythril/domain/revised_plan.py`:
- `Scenario A Go-Live: Tuesday 1 December 2026 (7.1 weeks slip from committed 12 Oct)`
- `Scenario B Go-Live: Monday 4 January 2027 (12.0 weeks slip from committed 12 Oct)`
- `Peak trading window derived dynamically: 2026-11-26 to 2026-11-30 (cleared by cutovers)`
- `All revised tasks maintain non-negative float (win - eff >= 0)`
- `T13 starts after freeze end (s > 2026-10-19) with 9 full working days`
