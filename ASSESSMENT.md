# Mythril Programme — Technical Assessment: What Was Inherited

**Author:** Incoming Data & Analytics Project Manager  
**Date:** 31 August 2026  
**Target:** Steering Committee / Twin Hearth Studios Leadership  
**Evaluation Scope:** Forensic audit of project repository artifacts (`artifacts/`)  

---

## 1. Executive Declaration: Programme Colour

### **Current Programme Status: 🔴 RED**

The previous Monthly Status Report (August 2026) declared the Mythril programme **🟢 GREEN** across Schedule, Budget, Scope, Quality, and **🟡 AMBER** on Resources. 

**That assessment is completely false.** It represents a governance breakdown where risks were actively downgraded, financial data corruption was masked by aggregate thresholds, mathematical impossibilities were scheduled as facts, and critical dependencies were inverted. 

The committed production cutover date of **12 October 2026 is an operational, technical, and mathematical impossibility**. The programme cannot proceed to cutover on 12 October without inflicting catastrophic reporting outages, corrupting financial reporting, and attempting execution with an empty engineering chair.

---

## 2. Forensic Findings (Ranked by Impact on Programme)

Every finding below is substantiated with specific artifact references, table rows, and line numbers. Verified empirical facts are strictly separated from reasonable operational inferences. **Every number in this document is reproducible by running `python verify.py` at the repository root.**

```
IMPACT RANKING OVERVIEW:
1. Critical Data Integrity: Reconciliation Conceals +49.82% Revenue Overstatement in March 2026
2. Critical Execution Void: Sole Analytics Engineer on Approved PTO During Cutover Week
3. Critical External Blocker: Storefront Aggregator Imposes Unnegotiable Change Freeze (5–19 Oct)
4. Critical Governance Breach: Vendor Freeze Known on 21 Aug, Downgraded in Status, Concealed from SteerCo
5. Structural Schedule Infeasibility: Four Impossible Dependency Inversions in Published Plan
6. Structural Schedule Infeasibility: Zero Contingency / Zero Float Across 9 of 13 Tasks
7. Mathematical Capacity Infeasibility: T06 Reporting Rebuild Unviable at 90% Allocation in Isolation
8. Resource Availability Conflict: Finance Controller 90% Occupied by Fiscal Year-End Close
9. Resource Fiction: Outgoing PM Allocated 60% Capacity for 5 Weeks Post-Departure
10. Scope Waste & Telemetry Debt: 46.7% Ghost Reports (56/120) and Corrupted Telemetry
11. Architectural / Pipeline Debt: 10 Active Day-One Reports Depend on Ad-Hoc Excel Extracts
12. Security & Compliance Void: IT Security Allocation Drops to 0% During Cutover & Hypercare
13. Uncontrolled Scope Creep: Unbaselined FY2027 Studio Scorecard Promised Without Sizing
14. Financial Reality: Schedule Realignment Adds ~7 Weeks of Operational Team Burn
```

---

### Finding 1: Reconciliation Conceals +49.82% Revenue Overstatement in March 2026
* **Impact:** **Critical — Data Integrity & Financial Reporting.** Cutover would publish corrupt financial figures to executive and accounting ledgers.
* **Evidence:**
  - `artifacts/reconciliation-2026-08-28.md` (lines 10–16, 20–37)
  - `artifacts/status-report-2026-08.md` (lines 14, 22–24)
* **Empirical Facts:**
  - Status report claims: *"First reconciliation run completed on 28 August and passed... Quality: 🟢 Green."*
  - Kick-off tolerance was agreed at **±5%** evaluated on annual totals. Net revenue for FY2026 total was reported as: Legacy `$1,476,035.13` vs New Platform `$1,535,760.05` (**+4.05% / +$59,724.92**), triggering an automated `PASS`.
  - The hidden Detail Appendix (explicitly marked *"not reviewed in the status meeting"*, line 18) reveals:
    - Q1 FY2026 (Oct–Dec 2025): **0.00% delta** (`$311,739.28` vs `$311,739.28`).
    - Q3 FY2026 (Apr–Jun 2026): **0.00% delta** (`$401,395.79` vs `$401,395.79`).
    - Jan 2026: **0.00% delta** (`$105,245.87` vs `$105,245.87`).
    - Feb 2026: **0.00% delta** (`$101,633.14` vs `$101,633.14`).
    - **March 2026: Legacy `$119,882.64` vs New Platform `$179,607.56` — an error of +49.82% (+$59,724.92).**
  - **The entire annual variance of `$59,724.92` is identically and exclusively the March variance.** It is not one discrepancy distributed among several; a single systemic defect accounts for 100% of the annual error.
  - Total `fact_order` rows: Legacy `105,440` vs New Platform `108,438` (**+2,998 rows / +2.84%**).
* **Operational Inferences:**
  - While row count delta is reported only at the FY total level in the artifact, the exact correspondence between the revenue overstatement in March and the annual total strongly indicates that the +2,998 phantom orders originated in the March ingestion/transformation run.
  - Root cause is uninvestigated: possibilities include duplicate ingestion of a batch file, missing refund deduplication, or currency conversion error.
  - Controller J. Reyes cannot and will not sign off on financial reconciliations containing a 50% monthly variance. Historical backfill (`T03`) cannot proceed while transformation logic remains corrupt.

---

### Finding 2: Sole Analytics Engineer on Approved PTO During Cutover Week
* **Impact:** **Critical — Complete Technical Execution Void.** Zero engineering capability during committed cutover.
* **Evidence:**
  - `artifacts/team-notes.md` (line 7)
  - `artifacts/project-plan.csv` (lines 5, 8, 9, 10, 14)
  - `artifacts/resource-allocation.csv` (lines 6–7, 15–16, 20–21)
* **Empirical Facts:**
  - D. Whitlock is the sole analytics engineer, sole author of the legacy SSIS packages, and the only person who can operate the legacy loader. No runbook exists (`team-notes.md:7`).
  - Whitlock has approved, non-refundable PTO from **9–20 October 2026** (booked in March 2026; 8 business days).
  - `project-plan.csv` assigns Whitlock to execute:
    - `T08 Production cutover`: Monday, **12 October 2026** (middle of PTO).
    - `T09 Hypercare and stabilisation`: Starts **13 October 2026** (middle of PTO).
    - `T04 Parallel run`: Runs through **14 October 2026** (middle of PTO).
    - `T13 Storefront feed migration`: Scheduled **5–16 October 2026** (middle of PTO).
  - In `resource-allocation.csv`, Whitlock is planned at **160% allocation** during cutover week (12 Oct) and the preceding week (5 Oct): 70% Warehouse Migration + 50% Legacy Loader Support + 40% Storefront Feed Migration.
* **Operational Inferences:**
  - The schedule relied on a team member working at 160% capacity while physically on vacation in another country. Cutover on 12 October literally has no engineer to push the button.

---

### Finding 3: Storefront Aggregator Imposes Unnegotiable Change Freeze (5–19 Oct)
* **Impact:** **Critical — External Pipeline Dependency Blocked.** Target warehouse cannot ingest primary storefront revenue.
* **Evidence:**
  - `artifacts/vendor-notice.md` (lines 10–23)
  - `artifacts/project-plan.csv` (line 14)
* **Empirical Facts:**
  - Vendor formal notice dated 21 August 2026 mandates a platform change freeze from **Monday 5 October through Monday 19 October 2026 inclusive**.
  - During this window: *"No new integrations can be provisioned, and no credentials can be issued or rotated. Migrations from v2 to v3 cannot be started or completed. We are unable to make exceptions to the freeze window; it applies to all partners."*
  - Vendor onboarding requires **9 working days** from credential issue to verified first full settlement file.
  - `project-plan.csv` scheduled `T13 Storefront settlement feed migration` for **2026-10-05 to 2026-10-16** (effort: 9 days) — directly inside the freeze window.
* **Operational Inferences:**
  - Even if Whitlock were not on PTO, the vendor will reject any credential provisioning or migration request between 5 and 19 October. `T04 Parallel run` depends on `T13`; without settlement feeds, parallel run cannot validate revenue.

---

### Finding 4: Active Risk Degradation and Governance Failure
* **Impact:** **Critical — Governance & Executive Visibility.** Programme risks were deliberately sanitized.
* **Evidence:**
  - `artifacts/vendor-notice.md` (dated 21 August 2026)
  - `artifacts/status-report-2026-08.md` (line 42)
  - `artifacts/steering-notes-2026-08.md` (line 9)
* **Empirical Facts:**
  - The vendor notice with strict freeze dates was delivered on **21 August 2026**.
  - In the August status report, this risk was downgraded to `R-03`: Severity **Low**, Owner **D. Whitlock**, Mitigation *"Vendor notified, awaiting confirmation"* (`status-report-2026-08.md:42`).
  - Five days later, at the Steering Committee on **26 August 2026**, the CFO asked whether anything threatened the 12 October date and was told **"No"** (`steering-notes-2026-08.md:9`).
* **Operational Inferences:**
  - Leadership was misinformed. The outgoing PM possessed written notice of an immovable freeze that invalidated the cutover date, yet reported the risk as "Low" and verbally assured the CFO that schedule integrity was intact.

---

### Finding 5: Four Fatal Dependency Inversions in Published Schedule
* **Impact:** **Critical — Structural Schedule Infeasibility.** Tasks are arranged in physical contradiction to their prerequisites.
* **Evidence:**
  - `artifacts/project-plan.csv` (lines 4, 5, 6, 7, 8, 9, 14)
* **Empirical Facts:**
  1. **Cutover before Sign-off:** `T08 Production cutover` is scheduled for **12 October**, but its predecessor `T05 Reconciliation sign-off` is scheduled for **15–16 October**. The cutover is scheduled 4 days before Finance signs off.
  2. **Parallel Run before Predecessor Feed Finishes:** `T04 Parallel run` is scheduled for **1–14 October**, but its explicit predecessor `T13 Storefront feed migration` is scheduled to finish on **16 October**. The validation finishes before the feed is built.
  3. **UAT before Build Completes:** `T07 User acceptance testing` starts on **5 October**, but its predecessor `T06 Rebuild reporting layer` does not finish until **9 October**. Business users are scheduled to test reports 4 business days before they exist.
  4. **Historical Backfill before Schema Complete:** `T03 Historical backfill` starts **14 September**, but its predecessor `T02 Build curated tables` does not finish until **25 September** (11 business days later).
* **Operational Inferences:**
  - The schedule was reverse-engineered from the CFO's target date of 12 October without network logic. Dates were typed into cells to look compliant rather than to establish a viable sequence.

---

### Finding 6: Zero Contingency / Zero Float Across 9 of 13 Tasks
* **Impact:** **High — Fragile Critical Path.** A single day's delay anywhere in the chain collapses the entire schedule.
* **Evidence:**
  - `artifacts/project-plan.csv` (lines 2–14)
* **Empirical Facts:**
  - Calculating total float (Working Days in Window minus Planned Effort Days):
    - `T02`: 55 days effort in 55-day window → **Float = 0 days**
    - `T04`: 10 days effort in 10-day window → **Float = 0 days**
    - `T05`: 2 days effort in 2-day window → **Float = 0 days**
    - `T06`: 40 days effort in 40-day window → **Float = 0 days**
    - `T07`: 5 days effort in 5-day window → **Float = 0 days**
    - `T08`: 1 day effort in 1-day window → **Float = 0 days**
    - `T09`: 14 days effort in 14-day window → **Float = 0 days**
    - `T10`: 10 days effort in 10-day window → **Float = 0 days**
    - `T11`: 10 days effort in 10-day window → **Float = 0 days**
  - Only four non-critical tasks contain minimal float: `T01` (+2d), `T03` (+1d), `T12` (+2d), `T13` (+1d).
* **Operational Inferences:**
  - In data warehouse migrations involving complex ETL, zero buffer is negligence. Any defect, unexpected data type mismatch, or query timeout triggers immediate delay.

---

### Finding 7: T06 Reporting Rebuild is Mathematically Impossible in Isolation
* **Impact:** **High — Schedule Slippage.** Reporting workstream slips even if no other dependencies failed.
* **Evidence:**
  - `artifacts/project-plan.csv` (line 7)
  - `artifacts/resource-allocation.csv` (lines 24–29)
* **Empirical Facts:**
  - `T06` specifies **40 working days of effort** between 17 August and 9 October 2026 (an elapsed window of exactly 40 working days).
  - BI Developer M. Okonkwo is allocated to Warehouse Migration at **90% capacity (0.9 FTE)** across all weeks (`resource-allocation.csv:24-29`).
  - Required elapsed time: 40 ÷ 0.9 = **44.4 working days**.
* **Operational Inferences:**
  - At 0.9 FTE, `T06` slips by approximately 4.4 working days into mid-October, automatically pushing `T07 UAT` and `T08 Cutover` past 12 October, entirely independent of Whitlock's PTO or the vendor freeze.

---

### Finding 8: Finance Controller 90% Occupied by Fiscal Year-End Close
* **Impact:** **High — Sign-off & Governance Block.** Key gatekeeper cannot participate during cutover window.
* **Evidence:**
  - `artifacts/steering-notes-2026-08.md` (lines 21–23)
  - `artifacts/team-notes.md` (line 9)
  - `artifacts/resource-allocation.csv` (lines 37–38, 42–43)
* **Empirical Facts:**
  - Controller J. Reyes owns reconciliation sign-off (`T05`).
  - Reyes is allocated **90% to Fiscal Year-End Close** for the weeks starting 5 October and 12 October, leaving only **10% capacity (4 hours/week)** for Mythril.
  - In Steering Committee notes, the CFO confirmed: *"Finance is in fiscal year-end close for the first two weeks of October and will have limited availability. Expects the programme to 'work around it' and confirmed Finance still needs to sign off the reconciliation before cutover."*
* **Operational Inferences:**
  - Attempting to conduct UAT, reconciliation deep-dives, and cutover sign-off during Finance's most demanding annual audit window is fundamentally flawed.

---

### Finding 9: Outgoing PM Allocated 60% Capacity for 5 Weeks Post-Departure
* **Impact:** **Medium — Resource Planning Fiction.** Critical project tasks left unowned.
* **Evidence:**
  - `artifacts/team-notes.md` (line 10)
  - `artifacts/resource-allocation.csv` (lines 49–53)
  - `artifacts/project-plan.csv` (line 11)
* **Empirical Facts:**
  - S. Alvear leaves the company on **30 September 2026** (`team-notes.md:10`).
  - `resource-allocation.csv` allocates Alvear at **60% capacity across 5 weeks after departure**: weeks starting 5 Oct, 12 Oct, 19 Oct, 26 Oct, and 2 Nov.
  - Alvear is listed as sole owner of `T10 Training and organisational comms` (effort: 10 days, running through 9 October).
* **Operational Inferences:**
  - Handover planning was neglected. Unless the incoming PM immediately takes ownership of governance, training, and communications, these streams will halt on 1 October.

---

### Finding 10: Scope Waste & Telemetry Debt (46.7% Ghost Reports)
* **Impact:** **Medium — Engineering Resource Misdirection.** Burning developer capacity on unused assets.
* **Evidence:**
  - `artifacts/report-usage.csv` (lines 2–121)
  - `artifacts/status-report-2026-08.md` (line 13)
* **Empirical Facts:**
  - Catalogue size: **120 legacy reports**.
  - **56 reports (46.67%) have exactly 0 views** in the last 12 months and `last_viewed` is null/empty.
  - Only **38 reports (31.67%) have been viewed in 2026**.
  - These 38 active reports account for **2,270 out of 2,309 total views (98.31%)**.
  - Telemetry is self-contradictory: **19 reports** show `views_last_12m > 0` but record `last_viewed` dates prior to September 2025 (e.g., `RPT-012` last viewed 2024-03-14 with 1 view; `RPT-070` last viewed 2024-03-24 with 2 views). These 19 reports account for only 28 total views.
* **Operational Inferences & Corrections:**
  - *Correction of prior assumption:* `report-usage.csv` does not record which 42 reports (35%) Okonkwo rebuilt. There is no artifact evidence proving whether Okonkwo rebuilt 24 ghost reports. However, if the rebuild was conducted sequentially or without usage filtering, the expected statistical value is that **~20 of the 42 rebuilt reports (46.7%) are zero-use ghosts**. Establishing which reports were rebuilt is Question #1 for Okonkwo.
  - The telemetry corruption indicates that dormant reports are even more obsolete than reported.

---

### Finding 11: 10 Active Day-One Reports Depend on Ad-Hoc Excel Extracts
* **Impact:** **Medium — Data Architecture Debt & Unowned Work.**
* **Evidence:**
  - `artifacts/report-usage.csv` (lines 2–121)
* **Empirical Facts:**
  - Across the 120-report catalogue, 30 reports source from `Excel extract`.
  - Among the **38 active day-one reports**, exactly **10 source from Excel extracts** rather than the Legacy EDW:
    - `RPT-035` Fiscal quarter close pack EMEA (140 views)
    - `RPT-041` Platform fee analysis 2024 (5 views)
    - `RPT-062` Paying player cohorts - copy (11 views)
    - `RPT-071` Acquisition channel mix FINAL (140 views)
    - `RPT-072` Acquisition channel mix detail (14 views)
    - `RPT-079` Refund reason breakdown FINAL (11 views)
    - `RPT-101` Wishlist funnel 2024 (140 views)
    - `RPT-109` Board summary old (220 views)
    - `RPT-112` Board summary weekly (19 views)
    - `RPT-117` Weekly flash FINAL (19 views)
* **Operational Inferences:**
  - These reports cannot simply be pointed to the new warehouse; they rely on manual upstream Excel files. Migrating them requires engineering new ingestion pipelines or accepting that they remain manual processes post-cutover. This work is completely unowned in `project-plan.csv`.

---

### Finding 12: IT Security Allocation Drops to 0% During Cutover & Hypercare
* **Impact:** **Medium — Security & Compliance Vulnerability.**
* **Evidence:**
  - `artifacts/resource-allocation.csv` (lines 54–58)
* **Empirical Facts:**
  - R. Bekele (IT Security) is allocated: 30% (Sep 7, Sep 14), 20% (Sep 21), 10% (Sep 28), 10% (Oct 5).
  - From the week of **12 October onward, Bekele's allocation drops to 0%**.
* **Operational Inferences:**
  - There is zero planned security support during production cutover, role-based access provisioning, or hypercare stabilization. Any access or permission failure during go-live will have no security owner.

---

### Finding 13: Unbaselined Scope Demand: Studio Relations Scorecard
* **Impact:** **Medium — Uncontrolled Scope Creep.**
* **Evidence:**
  - `artifacts/steering-notes-2026-08.md` (lines 15–16)
* **Empirical Facts:**
  - Head of Studio Relations stated in Steering Committee: *"Studio leads have been promised their own scorecard by the start of FY2027. This is the first the programme team has heard of that commitment."*
  - FY2027 begins on **1 October 2026**.
* **Operational Inferences:**
  - A major new business capability was promised to studio leadership with zero sizing, no project plan task, no developer allocation, landing directly in the middle of cutover preparations.

---

### Finding 14: Schedule Realignment Adds ~7 Weeks of Team Burn
* **Impact:** **Medium — Budgetary Reality.**
* **Evidence:**
  - `artifacts/status-report-2026-08.md` (line 12)
* **Empirical Facts:**
  - August status report stated: *"Budget: 🟢 Green | 71% consumed against 74% elapsed."*
  - However, this burn rate was measured against an artificial schedule terminating on 12 October.
* **Operational Inferences:**
  - Realignment of cutover from 12 October to **30 November 2026** extends project duration by **7 calendar weeks (49 days)**. Cloud infrastructure cost modelling is out of scope, but operational labour burn is not: internal team time across those 7 weeks, plus contractor backfill for the legacy loader derived from the RTB lines of `resource-allocation.csv` (40% for the weeks of 7/14/21 Sep, 50% for 28 Sep and 5/12 Oct, 40% for 19 Oct/26 Oct/2 Nov, plus an assumed 40% across the four November weeks to go-live) = **5.5 FTE-weeks, roughly 220 contractor hours**. The CFO will ask for this number; the derivation is in `PLAN.md` section 6.

---

## 3. Side-by-Side Reality Matrix

| Dimension | August Status Report | Ground Truth (Artifact Evidence) | Variance / Impact |
|---|---|---|---|
| **Overall Status** | 🟢 **GREEN** | 🔴 **RED** | Total disconnect between reporting and reality. |
| **Schedule** | 🟢 On track for 12 Oct | 🔴 Cutover 12 Oct impossible | Whitlock PTO (9–20 Oct), vendor freeze (5–19 Oct), 4 dependency inversions. |
| **Data Quality** | 🟢 Recon passed (±5%) | 🔴 March revenue +49.82% error | FY variance ($59,724.92) is 100% in March. +2,998 extra orders. |
| **Vendor Feed** | 🟢 Risk R-03: Low | 🔴 Hard freeze 5–19 Oct | Vendor will not provision or migrate. Requires 9 workdays. |
| **Reporting Scope** | 🟢 All 120 on track | 🟡 46.7% zero-use ghosts | 56 reports unused; 38 active reports account for 98.31% of views. |
| **Staffing** | 🟡 Capacity tight | 🔴 160% allocation / PTO | Whitlock allocated 160% while on PTO. Alvear allocated 5 wks post-exit. |
| **Governance** | 🟢 Asks: None | 🔴 Decisions Suppressed | SteerCo misinformed on 26 Aug; critical blockers hidden from minutes. |

---

## 4. Assessment Summary

The Mythril programme cannot be rescued by working overtime or "pushing harder" in September. The foundation is compromised by a 50% revenue flaw in March 2026, an absent technical lead during cutover, an unnegotiable vendor freeze, and an unprioritized reporting rebuild.

A complete re-baselining of scope, critical path, cutover sequencing, and governance is required immediately. The revised plan is detailed in `PLAN.md`.
