# Mythril Programme — AI Workflow & Verification Audit

**Author:** Incoming Data & Analytics Project Manager  
**Date:** 31 August 2026  
**Document:** Methodological audit of AI utilization, prompt logs, and validation controls  

---

## 1. Tooling Architecture & Rationale

To assess and re-baseline the Mythril programme under a tight time constraint, an **integrated AI pair-programming agent (Google Antigravity with Advanced Reasoning)** was combined with **local Python/pandas script execution** via the CLI.

### Why this combination:
1. **Multi-Artifact Cross-Referencing:** Project documentation was fragmented across Markdown status notes, meeting minutes, vendor notices, and three tabular CSV files. LLMs excel at synthesizing qualitative sentiment against quantitative records.
2. **Eliminating LLM Arithmetic Hallucinations:** Large language models are notorious for making calculation errors when summing CSV columns or calculating working-day date math. To prevent this, the AI was strictly directed to write and execute deterministic Python scripts for all tabular aggregations, calendar math, and network dependency calculations.
3. **Rapid Executive Drafting:** High-level executive synthesis (MBR, CFO memo) requires translating complex data engineering constraints into commercial and governance impacts.

---

## 2. Concrete Prompts & Outputs

Below are four representative prompts executed during the assessment, showing the model's analytical progression.

### Prompt 1: Forensic Audit of Financial Reconciliation
```text
PROMPT:
"Inspect artifacts/reconciliation-2026-08-28.md and compare the summary table against 
the detail appendix. Calculate the exact dollar and percentage deltas across quarters and 
months. Is the 5% tolerance check mathematically sound from an audit perspective?"
```
* **Output Synthesized:**
  The AI highlighted that while the annual net revenue variance was +4.05% (`+$59,724.92`), Q1, Q3, January, and February had **0.00% delta**. Exactly 100% of the annual error was concentrated in **March 2026 (+49.82% / +$59,724.92)**. The AI concluded that evaluating pass/fail exclusively on annual aggregates masked a catastrophic monthly defect that would fail any standard financial audit.

---

### Prompt 2: Resource Allocation vs. Project Plan Collision Analysis
```text
PROMPT:
"Cross-reference artifacts/project-plan.csv with artifacts/resource-allocation.csv, 
team-notes.md, and vendor-notice.md. Map out D. Whitlock's weekly allocations, PTO, 
and assigned tasks during October 2026. What physical conflicts exist?"
```
* **Output Synthesized:**
  The AI revealed that Whitlock was allocated at **160% capacity** during the weeks of 5 October and 12 October (70% migration + 50% legacy support + 40% vendor migration). It cross-referenced `team-notes.md` to identify that Whitlock had approved, non-refundable PTO from 9–20 October, meaning Whitlock was assigned to execute `T08 Production Cutover` on 12 October while physically out of the office. It also flagged that `T13 Storefront feed migration` was scheduled directly inside the vendor's change freeze (5–19 October).

---

### Prompt 3: Telemetry & Scope Triage of 120 Reports
```text
PROMPT:
"Write and run a Python script over artifacts/report-usage.csv. Group reports into 
usage tiers (zero views in 12m, viewed in 2026, viewed prior to 2026). Calculate the 
cumulative percentage of total views captured by reports viewed in 2026. Audit the 
source column and flag any anomalies in the last_viewed timestamps."
```
* **Output Synthesized (via script execution):**
  - Total reports: 120. Total annual views: 2,309.
  - Zero views: 56 reports (46.67%).
  - Viewed in 2026: 38 reports (31.67%), accounting for 2,270 views (**98.31% of total consumption**).
  - Dormant (viewed before 2026): 26 reports (1.69% of views).
  - Data anomaly discovered: 19 reports recorded `views_last_12m > 0` but had `last_viewed` dates in 2024 or early 2025, indicating stale/corrupted telemetry counters.
  - Architecture debt: 10 of the 38 active reports sourced from `Excel extract`, not the EDW.

---

### Prompt 4: Sequential Critical Path Modeling for 30 November Cutover
```text
PROMPT:
"Simulate a revised project schedule starting 1 September 2026. Constraints:
- Whitlock cannot be double-allocated post-PTO; T03 (12d) and T13 (9d) must be sequential.
- Whitlock PTO is 9–20 October inclusive (8 working days).
- Vendor freeze is 5–19 October inclusive.
- Oct 1–8 has 6 working days.
- Parallel run T04 requires 10 working days; Finance sign-off T05 requires 2 working days.
Determine the earliest viable cutover date that provides a clean monthly accounting boundary."
```
* **Output Synthesized (via script execution):**
  - T03 Part 1: Oct 1–8 (6 workdays).
  - T03 Part 2: Oct 21–28 (6 workdays).
  - T13: Oct 29 – Nov 10 (9 workdays).
  - T04: Nov 11 – Nov 24 (10 workdays).
  - T05: Nov 25 – Nov 26 (2 workdays).
  - Go/No-Go Gate: Friday 27 November. Cutover execution window: 27–29 November.
  - Production Go-Live: **Monday, 30 November 2026**.
  - Outcome: Solves the CFO's fiscal ledger requirement by allowing November to close on legacy and December to start 100% on the cloud platform.

---

## 3. The "Confidently Wrong" AI Moments (Hallucinations Caught)

During the forensic investigation, code verification caught **four** confidently-wrong AI outputs. All four shared a signature: the reasoning was sound, the *shape* of the answer was right, and the number was invented. Each is documented below with the check that caught it.

### Hallucination 1: The "24 Rebuilt Ghost Reports" Assumption
* **The AI's Plausible Finding:** In an initial draft, the AI confidently stated: *"In the 42 reports already rebuilt by M. Okonkwo (35%), 24 of them were zero-view ghost reports, proving engineering effort is being actively wasted."*
* **Why it seemed plausible:** In `report-usage.csv`, if one inspects the first 42 rows numerically (`RPT-001` to `RPT-042`), exactly 24 of those reports have zero views.
* **How it was caught:** When auditing the proof for `ASSESSMENT.md`, we searched for the artifact evidence confirming build sequence. `report-usage.csv` contains *no build order or completion flag*. The assumption that Okonkwo worked strictly in numerical order was an unsubstantiated inference.
* **Correction Applied:** Per the assessment rules (*"a finding with no evidence is an opinion"*), the text was surgically corrected to state: *"There is no artifact evidence recording the build sequence. If Okonkwo rebuilt reports without usage prioritization, the statistical expected value is that ~20 of the 42 rebuilt reports are zero-use ghosts. Determining which reports were rebuilt is Question #1 for Okonkwo."*

---

### Hallucination 2: Calendar Arithmetic Error (The "8 Working Days in October" Error)
* **The AI's Plausible Finding:** The AI proposed starting `T03 Historical Backfill` on 1 October and claimed that *"all 8 days prior to Whitlock's PTO (1–8 October) would be completed, leaving only 4 days post-PTO."*
* **How it was caught:** When running a verification script over the calendar dates, the script counted the business days between Thursday 1 October and Thursday 8 October:
  `Oct 1 (Thu), Oct 2 (Fri), Oct 5 (Mon), Oct 6 (Tue), Oct 7 (Wed), Oct 8 (Thu)` = **6 working days, not 8**.
* **Impact of Error:** Overlooking this would have pushed `T03` completion 2 business days later post-PTO, causing an unbudgeted cascade that would have collapsed the revised 23 November date.
* **Correction Applied:** The schedule was completely recalculated using deterministic Python datetime logic, advancing the cutover recommendation to **Monday, 30 November 2026**, which also solved the CFO's financial ledger problem.

---

### Hallucination 3: Grouping into "17 Core Families"
* **The AI's Plausible Finding:** The AI claimed the 38 active reports condensed into *"17 core report families."*
* **How it was caught:** Normalizing the report titles and entities programmatically revealed **24 distinct functional families** (or ~19 under aggressive grouping). The number 17 was a rounded LLM estimation without mathematical backing.
* **Correction Applied:** Replaced with the audited count of 24 base families.

---

### Hallucination 4: The Fabricated Total Float Column (the most dangerous one)

* **The AI's Plausible Finding:** The first draft of `PLAN.md` shipped a Total Float column for every task
  in the revised schedule: `T02 0d`, `T06 +15d`, `T12 +5d`, `T09 +5d`, `T10 +2d`, `T14 +10d`.
* **Why it seemed plausible:** The numbers were the right order of magnitude, monotonically sensible, and
  sat in a table that looked audited. Nothing about them read as invented.
* **How it was caught:** `verify.py` recomputes float for every row as
  `working days in window - effort days`. Six of fifteen rows disagreed with the draft. Worse, **T02 came
  back at -2 days**: 13 Jul to 28 Sep is 56 working days and the task carried 58 effort days after the
  3-day bug fix was added. The head of the critical path was over-committed, and the table said `0d`.
* **Why this was the most dangerous of the four:** `ASSESSMENT.md` Finding 6 attacks the inherited plan
  precisely for zero float. Presenting a fabricated float column while making that argument would have
  handed the Steering Committee the one rebuttal that discredits the whole submission.
* **Correction Applied:** T02 end date moved from 25 to 30 September (window 58 working days, effort 58,
  float 0), backfill Part 1 shifted to 1-8 October, every float recomputed by script, and the float method
  is now stated in the table header so anyone can re-derive it. `T08` no longer carries a float number at
  all: it is a weekend window of 1 working day plus 2 non-working days, where float is not a meaningful
  measure.
* **Process change:** no derived number ships in any deliverable unless `verify.py` computes it. The
  script is committed alongside the documents for exactly this reason.

---

## 4. Methodology for CSV Analysis and Data Integrity Verification

To ensure 100% data integrity, all conclusions drawn from the CSV files adhered to a three-tier verification protocol:

```
DATA VERIFICATION PROTOCOL:

1. Never Prompt LLMs for Direct Math:
   - Queries like "What is the total views of reports where platform=Excel?" were NEVER
     evaluated via generative text.
   - The AI was instructed to generate an explicit Python script utilizing the pandas library.

2. Deterministic Local Execution:
   - Scripts were executed in the workspace using the local Python 3 environment.
   - Outputs were dumped as raw text and inspected.
   - The consolidated script is committed as `verify.py` at the repository root. Running
     `python verify.py` regenerates every number quoted in ASSESSMENT.md, PLAN.md, SCOPE.md,
     MBR.md and CFO_MESSAGE.md, and exits non-zero if any assertion fails.

3. Cross-Check Against Edge Cases:
   - Date formats were validated using `pd.to_datetime(..., errors='coerce')`.
   - String matching was verified using regular expressions and exact lowercase stripping.
   - Resource allocations were summed by person and by week to verify total capacity burdens.
```

By enforcing strict code-level verification, every metric in this submission is reproducible rather than asserted. The test of that claim is simple: run `python verify.py`. If a number in any deliverable is not in its output, the number should not be believed — including by the person who wrote it.
