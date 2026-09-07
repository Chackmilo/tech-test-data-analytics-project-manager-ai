# Forensic Audit Prompt 02: Resource & Calendar Collision Mapping

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
Cross-reference project planning files, weekly resource allocations, personnel notes, and vendor notices to detect physical delivery impossibilities, over-allocation spikes, and holiday collisions.

## Target Artifacts
- `artifacts/project-plan.csv`
- `artifacts/resource-allocation.csv`
- `artifacts/team-notes.md`
- `artifacts/vendor-notice.md`

## System Prompt / Instructions
```text
Cross-reference project-plan.csv, resource-allocation.csv, team-notes.md, and vendor-notice.md.
Map D. Whitlock's weekly allocations, approved PTO, and assigned critical-path tasks across October 2026.
Identify physical delivery conflicts, single-operator key-person dependencies, and vendor freeze collisions.

Key questions:
1. What is D. Whitlock's planned weekly allocation across October 2026?
2. Which tasks overlap Whitlock's approved PTO (9–20 October 2026)?
3. Does task T13 collide with the storefront aggregator's vendor freeze window?
4. Who else can operate the legacy loader if Whitlock is unavailable?
```

## Deterministic Guardrail Check
Verified by `analysis/mythril/domain/inherited_plan.py` & `analysis/mythril/domain/resources.py`:
- `Whitlock peak allocation == 160% in weeks of 2026-10-05 and 2026-10-12`
- `Whitlock tasks overlapping PTO (8 business days) == ['T04', 'T08', 'T09', 'T13']`
- `T13 planned window sits wholly inside vendor freeze (2026-10-05 to 2026-10-19)`
- `Single-operator risk: 'only person who can operate the legacy loader'`
