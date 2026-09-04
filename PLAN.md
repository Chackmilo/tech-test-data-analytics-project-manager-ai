# Mythril Programme — Revised Master Plan & Cutover Strategy

**Author:** Incoming Data & Analytics Project Manager
**Date:** 31 August 2026
**Baseline Revision:** v2.0 (Supersedes August 2026 Baseline)
**Target Cutover Date:** Monday, 30 November 2026 (Execution Window: 27–29 November 2026)

---

## 1. Executive Summary: The Defensible Cutover Date

### **Target Production Cutover: Monday, 30 November 2026**
*(Execution Window: Friday evening 27 November through Sunday 29 November 2026)*

The inherited date of **12 October 2026** is unviable due to the convergence of an unnegotiable vendor API freeze (5–19 Oct), the sole engineer's approved PTO (9–20 Oct), Finance fiscal year-end close (5–16 Oct), and an uninvestigated +49.82% revenue defect in March 2026.

### Why 30 November 2026 Wins the Financial & Operational Argument

1. **It answers the CFO's actual reason for 12 October.** The CFO chose 12 October because it was a clean break for the new fiscal year (`steering-notes-2026-08.md:7-8`). Be precise about what is and is not recoverable: FY2027 Q1 runs **October–December 2026**, so *any* date after 1 October splits that quarter across two systems. What is still recoverable is the **month** boundary. A 30 November go-live means November closes entirely on legacy and December opens entirely on the new warehouse — **no accounting month is ever split between two systems**, which is the property an auditor actually tests. A mid-month date (e.g. 23 November) forfeits that.
2. **Honours all physical constraints sequentially.** Whitlock is never double-allocated. Backfill completes first; vendor migration follows; parallel run runs on clean data with a live settlement feed.
3. **Respects Finance availability.** Sign-off lands 25–26 November, after the October close.
4. **Carries real float.** Every non-critical task carries declared float, and there is a formal decision gate one working day before the cutover window.

### Why Not Faster — The Option We Priced and Rejected

`T13` sits on the critical path **only because Whitlock is a single resource**, not because of logical precedence. If a second engineer (or a vendor-led migration) ran `T13` from 21 October in parallel with `T03` Part 2, the chain compresses:

| | Sequential (recommended) | With a second engineer |
|---|---|---|
| T13 Vendor migration | 29 Oct – 10 Nov | 21 Oct – 2 Nov |
| T04 Parallel run | 11–24 Nov | 3–16 Nov |
| T05 Finance sign-off | 25–26 Nov | 17–18 Nov |
| **Go-live** | **Mon 30 Nov** | Mon 23 Nov |

The option buys exactly **one week (5 working days)** and costs a second engineer who does not exist anywhere in `resource-allocation.csv`. It also lands go-live **mid-month**, forfeiting the clean ledger boundary that is the main reason the new date is defensible at all. **We do not recommend buying it.** It is documented here so the Steering Committee knows it was evaluated, not overlooked.

---

## 2. The Real Critical Path & Network Logic

### True Critical Path Sequence

```
T02 (Curated tables + March bug fix)
  -> T03 Part 1 (Backfill, pre-PTO)
  -> [PTO + vendor freeze + FY close: planned pause]
  -> T03 Part 2 (Backfill, post-PTO)
  -> T13 (Vendor settlement feed migration)
  -> T04 (Parallel run)
  -> T05 (Finance sign-off)
  -> GATE (Go/No-Go)
  -> T08 (Cutover)
```

The critical path is governed by ETL engineering, vendor onboarding and financial validation. **Descoping the reporting catalogue does not shorten it** — reporting runs in parallel and carries float. Descoping is still essential: it de-risks UAT and it is the only source of capacity for the unbudgeted FY2027 Studio Scorecard (see `SCOPE.md`).

```
CHRONOLOGICAL TIMELINE (SEPTEMBER 2026 - JANUARY 2027):

[Sep 1  - Sep 30] ===== T02 Curated Tables + March Bug Fix (Whitlock) =====
[Sep 1  - Sep 18] ----- RTB Runbook + Knowledge Transfer (Whitlock 20% / IT Ops) -----
[Aug 17 - Sep 11] ..... T06 Day-One Reports, 38 active (Okonkwo) .....
[Sep 14 - Sep 30] ..... T14 NEW: FY2027 Studio Scorecard (Okonkwo) .....
[Oct 1  - Oct 8 ] ===== T03 Historical Backfill Part 1 (6 of 12 workdays) =====

[Oct 5  - Oct 19] XXXXX VENDOR API CHANGE FREEZE (no credentials / no migrations) XXXXX
[Oct 5  - Oct 16] ##### FINANCE FISCAL YEAR-END CLOSE (Reyes 90% unavailable) #####
[Oct 9  - Oct 20] ***** D. WHITLOCK APPROVED PTO (8 working days) *****

[Oct 19 - Nov 6 ] ..... T07 User Acceptance Testing (post-FY-close) .....
[Oct 21 - Oct 28] ===== T03 Historical Backfill Part 2 (remaining 6 workdays) =====
[Oct 29 - Nov 10] ===== T13 Storefront Feed Migration (vendor: 9 workdays) =====
[Nov 9  - Nov 25] ..... T10 Training & Organisational Comms (Incoming PM) .....
[Nov 11 - Nov 24] ===== T04 Parallel Run (legacy vs new: 10 workdays) =====
[Nov 16 - Nov 26] ..... T12b Cutover Security & RBAC Review (Bekele) .....
[Nov 25 - Nov 26] ===== T05 Finance Reconciliation Sign-Off (Reyes: 2 workdays) =====
[Nov 27         ] ||||| EXECUTIVE GO/NO-GO DECISION GATE (14:00) |||||
[Nov 27 - Nov 29] >>>>> T08 Production Cutover Execution (weekend window) >>>>>
[Nov 30         ] ***** PRODUCTION GO-LIVE (clean start for the December ledger) *****
[Nov 30 - Dec 18] ..... T09 Hypercare & Stabilisation (14 workdays) .....
[Jan 11 - Jan 22] ..... T11 Legacy Decommission (rollback window preserved) .....
```

---

## 3. Revised Task Schedule & Work Breakdown Structure

**Float method:** `Total Float = working days in the planned window − effort days`, computed identically for every row (the same method used to expose the inherited plan's zero-float problem in `ASSESSMENT.md`, Finding 6). Where a resource is allocated below 1.0 FTE, the FTE-adjusted float is given in the notes. All figures are reproducible via `verify.py`.

| Task ID | Task Name | Owner | Start | End | Effort (d) | Window (wd) | Depends On | Total Float | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **T01** | Source system inventory & profiling | D. Whitlock | 2026-06-01 | 2026-07-10 | 28 | 30 | — | **+2d** | Complete (100%). |
| **T02** | Curated tables + March recon bug fix | D. Whitlock | 2026-07-13 | 2026-09-30 | 58 | 58 | T01 | **0d** | In progress (70%). End date extended from 25 to 30 Sep to absorb the 3-day bug fix. **Critical path.** |
| **T06** | Rebuild reporting layer (38 active reports) | M. Okonkwo | 2026-08-17 | 2026-09-11 | 13 | 20 | — | **+7d** | Descope cuts effort from 40d to 13d. At 0.9 FTE: 14.4 elapsed days needed, so **FTE-adjusted float +5.6d**. |
| **T12a** | Security & access review (Phase 1) | R. Bekele | 2026-09-07 | 2026-09-18 | 8 | 10 | — | **+2d** | On track (60%). |
| **T14** | *NEW:* FY2027 Studio Scorecard build | M. Okonkwo | 2026-09-14 | 2026-09-30 | 10 | 13 | T06 | **+3d** | At 0.9 FTE: 11.1 elapsed days needed, so **FTE-adjusted float +1.9d**. Delivers **on** the promised FY2027 start date. |
| **T03** | Historical backfill & load validation | D. Whitlock | 2026-10-01 | 2026-10-28 | 12 | 12 | T02 | **0d** | **Split around PTO:** Part 1 = 1–8 Oct (6 wd), Part 2 = 21–28 Oct (6 wd). **Critical path.** |
| **T07** | User acceptance testing (38-report scope) | M. Okonkwo / Business leads | 2026-10-19 | 2026-11-06 | 10 | 15 | T06; T14 | **+5d** | Deliberately scheduled **after** the 16 Oct end of Finance FY close so Finance-area reports get a real reviewer. |
| **T13** | Storefront settlement feed migration | D. Whitlock / Vendor | 2026-10-29 | 2026-11-10 | 9 | 9 | T03 *(resource-sequential on Whitlock)*; vendor freeze ends 19 Oct | **0d** | Vendor requires 9 working days from credential issue. **Critical path.** |
| **T04** | Parallel run: legacy vs new warehouse | D. Whitlock | 2026-11-11 | 2026-11-24 | 10 | 10 | T03; T13 | **0d** | Two full business weeks with a live v3 settlement feed. **Critical path.** |
| **T10** | Training & organisational comms | Incoming PM | 2026-11-09 | 2026-11-25 | 10 | 13 | T07 | **+3d** | Reassigned from S. Alvear (departs 30 Sep). |
| **T12b** | Cutover security & RBAC review | R. Bekele | 2026-11-16 | 2026-11-26 | 5 | 9 | T04 | **+4d** | **New.** Closes the security gap: the inherited plan had 0% security allocation from 12 Oct onward. |
| **T05** | Reconciliation sign-off (Finance) | J. Reyes | 2026-11-25 | 2026-11-26 | 2 | 2 | T04 | **0d** | Post-close availability. Requires 0.00% delta on audited core. **Critical path.** |
| **GATE** | **Executive Go/No-Go decision gate** | **Steering Committee** | **2026-11-27** | **2026-11-27** | **1** | **1** | **T05; T07; T12b** | **0d** | Formal sign-off: CFO, IT Director, VP Publishing Operations, Incoming PM. |
| **T08** | Production cutover execution | D. Whitlock / Team | 2026-11-27 | 2026-11-29 | — | — | GATE | *n/a* | **Weekend window: 1 working day (Fri) plus 2 non-working days.** Float is not meaningful here; the buffer sits in the GATE that same afternoon. |
| **T09** | Hypercare & stabilisation | D. Whitlock / Team | 2026-11-30 | 2026-12-18 | 14 | 15 | T08 | **+1d** | Intensive dual-run monitoring and triage. |
| **T11** | Legacy warehouse decommission | D. Whitlock | 2027-01-11 | 2027-01-22 | 10 | 10 | T09 | **0d in-window** | Deferred to January 2027 to preserve the rollback window. No downstream constraint, so in-window float of 0 carries no risk. |

---

## 4. Required Staffing & Operating Model Changes

For this date to hold, the Steering Committee must approve the following:

**1. D. Whitlock (Analytics Engineer) — break the single point of failure.**
- Current state: **120%–160%** planned allocation across conflicting workstreams (peak 160% in the weeks of 5 and 12 October).
- Mandated change: offload **100% of Run-The-Business legacy loader support** to IT Ops or a contractor.
- **Honest September split:** Whitlock is **not** available at 100% for T02 while also transferring the loader. Through **18 September** Whitlock runs **80% on T02 / 20% on knowledge transfer** (roughly 3 days total: recorded walkthrough sessions plus review of the runbook, which the receiving IT Ops engineer or contractor writes). From **21 September**, Whitlock is **100% on T02**.
- **The arithmetic:** T02 remaining = 30% × 58 = **17.4 effort days**. Available September capacity = (14 wd × 0.8) + (8 wd × 1.0) = **19.2 effective days**. Margin: **+1.8 days.** Thin — which is precisely why the RTB offload is a Steering Committee decision and not a preference.

**2. M. Okonkwo (BI Developer) — descope and redeploy.**
- Current state: 90% allocation attempting 120 reports (40 effort days, which is 44.4 elapsed days at 0.9 FTE, slipping past 9 October on its own).
- Mandated change: descope to the **38 active reports (13 effort days)**, freeing **27 effort days**.
- Freed capacity reallocated to: (a) the **FY2027 Studio Scorecard**, 10 days, delivering 30 September; (b) source remediation for the **10 active reports currently fed by Excel extracts**, 5 days during hypercare.

**3. J. Reyes (Finance Controller) — protect, don't negotiate.**
- Zero programme demands during FY close (5–16 October). UAT for Finance-area reports starts 19 October. Formal sign-off 25–26 November.

**4. R. Bekele (IT Security) — extend past cutover.**
- The inherited allocation drops to **0% from the week of 12 October**. Extend at 10% through November for `T12b` (RBAC, credential rotation, cutover access).

**5. Incoming PM — take ownership now.**
- S. Alvear departs 30 September while allocated 60% across five subsequent weeks. The incoming PM assumes `T10`, governance and SteerCo reporting from 1 October.

> **Explicit planning assumption.** `resource-allocation.csv` terminates at the week of 2 November 2026. Every allocation from 9 November onward (Whitlock, Okonkwo, Reyes, Bekele, PM) is a **planning assumption requiring Steering Committee staffing and budget ratification**, not an inherited fact.

> **Explicit estimating assumption.** The **3 engineering days** budgeted inside T02 for the March defect is an estimate made **before root cause is known**. No artifact supports it. Decision trigger: **if diagnosis is not complete by 18 September**, the fix no longer fits inside T02's window and the cutover date moves. That trigger is reported to the Steering Committee, not managed silently.

---

## 5. Cutover Execution Plan

### A. Cutover Sequence (Weekend Window: 27–29 November 2026)

| Phase | Time Window | Actions & Milestones | Responsible Lead |
|---|---|---|---|
| **1: Pre-cutover freeze** | Fri 27 Nov, 17:00 | Code freeze on the new platform. Final delta load on legacy EDW. Freeze reporting changes. | D. Whitlock |
| **2: Final ingestion & recon** | Fri 27 Nov 20:00 – Sat 28 Nov 04:00 | Final batch sync from the storefront aggregator (v3) and game platforms. Run automated reconciliation. | D. Whitlock / Vendor |
| **3: Verification gate** | Sat 28 Nov, 08:00–12:00 | Audit row counts, order totals and revenue across all 5 storefronts and 5 titles. **March 2026 verified at 0.00%.** | J. Reyes / Incoming PM |
| **4: Traffic cutover** | Sat 28 Nov, 14:00–18:00 | Repoint the BI alias to the cloud warehouse. Deploy the reporting portal against new endpoints. | IT Ops / D. Whitlock |
| **5: Smoke testing** | Sun 29 Nov, 09:00–15:00 | Synthetic queries; smoke-test all 38 Day-One reports; verify role permissions. | M. Okonkwo / R. Bekele |
| **6: Go-live broadcast** | Sun 29 Nov, 17:00 | Go-live confirmation to executive stakeholders. Open for Monday operations. | Incoming PM |

### B. Go/No-Go Decision Framework

- **Decision meeting:** Friday 27 November 2026, 14:00 — one working day before the window opens.
- **Authority:** unanimous consent among **CFO** (financial sign-off), **IT Director** (technical and infrastructure), **VP Publishing Operations** (operational and reporting), **Incoming PM** (execution).
- **A single No vote stops the cutover.** There is no override. The fallback is the next clean month boundary (Monday 4 January 2027), not "push through the weekend".

**Mandatory Go criteria — all five, no partial credit:**
1. **Financial reconciliation:** delta between legacy and new platform on core financials across FY2026 and FY2027-to-date is **0.00%**, evaluated **monthly, not annually**. March 2026 verified fixed.
2. **Storefront feed:** the v3 settlement feed has produced **5 consecutive days** of verified, error-free daily ingestion.
3. **Reporting layer:** 100% of the 38 Day-One reports validated and passing UAT smoke tests.
4. **Security:** RBAC matrix signed off by R. Bekele (`T12b`); no critical access findings outstanding.
5. **Rollback:** rollback runbook **tested in staging**, with a timed rehearsal on record.

### C. Post-Cutover Rollback Architecture

A cutover without a proven rollback is an unacceptable business risk. If critical defects emerge after the switch, Twin Hearth Studios must be able to restore legacy operations within hours.

**1. Dual-ingestion and parallel sync (retention: 30 days).**
- The legacy SSIS loader is **not** decommissioned at cutover.
- For 30 days post-cutover (through 31 December 2026), raw ingestion is dual-written to the new cloud landing zone and to legacy staging (or replayed daily from the bronze layer).
- `T11 Decommission` is therefore rescheduled to **January 2027**. This is the cost of a real rollback, and it is deliberate.

**2. Connection reversion (RTO under 2 hours).**
- Reporting portal and BI services connect through an abstraction alias (`edw-bi.twinhearth.internal`), never a direct host.
- On rollback, IT Ops repoints the alias to the on-premise legacy cluster.
- **RTO: 2 hours. RPO: under 4 hours** (delta sync replay).

**3. Invocation authority and triggers.**
- **Authority:** Incident Commander (IT Director), with CFO concurrence for any trigger touching financial reporting.
- **Non-negotiable rollback triggers:**
  - Revenue divergence **above 0.1%** discovered post-go-live and not root-caused within 4 hours.
  - Settlement ingestion failure exceeding **12 hours** that cannot be hot-fixed.
  - Cloud warehouse outage exceeding **4 business hours** during peak operations.
- **Rollback is a decision, not a failure.** It is pre-authorised at the gate so nobody has to seek permission at 03:00.

---

## 6. Budgetary Impact (Team Burn Accounting)

- Moving cutover from 12 October to 30 November adds **7 calendar weeks** (49 days) of programme execution.
- **Internal labour:** Whitlock, Okonkwo, Bekele and the incoming PM extended across those 7 weeks.
- **Contractor backfill for the legacy loader**, derived from the `resource-allocation.csv` RTB lines rather than estimated: 40% for the weeks of 7 / 14 / 21 Sep, 50% for 28 Sep and 5 / 12 Oct, 40% for 19 Oct / 26 Oct / 2 Nov, plus an assumed 40% for the four November weeks to go-live = **5.5 FTE-weeks, roughly 220 hours**.
- The August status report showed **71% budget consumed against 74% elapsed** — measured against a schedule that was never achievable. That green is not evidence of budget health; it is another artefact of a fictional baseline.
- **Trade-off:** attempting 12 October guarantees cutover failure, financial misstatement and emergency remediation. 220 contractor hours plus 7 weeks of internal burn is the cheaper of the two outcomes by a wide margin.

---

## 7. Plan Defensibility Summary

| Challenge | What the 12 Oct plan did | How the 30 Nov plan resolves it |
|---|---|---|
| **March reconciliation error** | Hid it behind an annual ±5% threshold. | 3 engineering days inside T02 to root-cause and fix, with a **declared 18 Sep decision trigger** if diagnosis runs long. Gate criterion moves to **monthly** 0.00%. |
| **Whitlock PTO (9–20 Oct)** | Scheduled cutover on 12 Oct, mid-PTO, at 160% allocation. | Planned pause. Backfill splits 6d before / 6d after. No task assumes Whitlock is present. |
| **Vendor freeze (5–19 Oct)** | Scheduled T13 (9d) entirely inside the freeze. | T13 runs 29 Oct – 10 Nov, wholly after the freeze, with the vendor's full 9 working days. |
| **Finance close (5–16 Oct)** | Assumed Finance would "work around it". | Zero demands during close. UAT from 19 Oct; sign-off 25–26 Nov. |
| **Dependency inversions** | Four inversions (T08/T05, T04/T13, T07/T06, T03/T02). | Strict network precedence restored; every predecessor finishes before its successor starts. |
| **Zero float** | 9 of 13 tasks at zero float; no contingency anywhere. | Float declared per task by an explicit, reproducible method; non-critical work carries +1 to +7 days; the critical path is protected by a formal gate. |
| **Security coverage** | Allocation dropped to 0% from 12 Oct — through cutover and hypercare. | New `T12b` extends Bekele through 26 Nov; RBAC sign-off is a Go criterion. |
| **Fiscal boundary** | Claimed a clean fiscal break it could not deliver. | Concedes Q1 FY2027 is split by any post-1-Oct date; guarantees **no month is split**, which is what the audit actually tests. |
| **Rollback** | No rollback plan, and decommission scheduled 2 weeks after go-live. | Dual-run for 30 days, RTO under 2h, pre-authorised triggers, decommission deferred to Jan 2027. |
