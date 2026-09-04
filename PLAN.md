# Mythril Programme — Revised Master Plan & Cutover Strategy

**Author:** Incoming Data & Analytics Project Manager
**Date:** 31 August 2026
**Baseline Revision:** v3.0 (supersedes the August 2026 baseline)
**Recommended cutover:** **Tuesday 1 December 2026** if a second engineer is funded — **Monday 4 January 2027** if not.

---

## 1. The Date Is a Decision, Not an Estimate

12 October 2026 is unreachable. Four hard stops sit inside one fortnight: the vendor API freeze (5–19 Oct), the sole engineer's approved PTO (9–20 Oct), Finance year-end close (5–16 Oct), and an undiagnosed +49.82% revenue defect in March 2026.

Rather than hand the Steering Committee one date and ask them to accept it, this plan presents **two fully-costed baselines that differ by exactly one decision: whether to fund a second engineer for the vendor migration.**

| | **Scenario A** | **Scenario B** |
|---|---|---|
| **Business go-live** | **Tue 1 December 2026** | **Mon 4 January 2027** |
| Slip from 12 October | 50 days (7.1 weeks) | 84 days (12 weeks) |
| Requires | **One additional engineer** (or vendor-led migration) for `T13`, ~9 working days | No new headcount |
| Technical cutover window | Fri 20 – Sun 22 Nov, then an 8-day soak with legacy authoritative | Mon 28 – Thu 31 Dec, inside the year-end shutdown |
| Ledger boundary | Month: November closes on legacy, December opens on the new platform | **Quarter: FY2027 Q1 entirely on legacy, FY2027 Q2 entirely on the new platform** |
| Peak-season validation | The Black Friday weekend runs on the new platform in soak, legacy still the book of record | The Black Friday weekend runs inside an extended 18-day parallel run |
| Contractor backfill | ~220 hours | ~284 hours |

**Both are defensible. Neither splits an accounting period. Neither puts a cutover on top of the year's biggest sales weekend.** The Steering Committee chooses by deciding whether to fund the engineer.

### Why the fiscal argument had to change

The CFO chose 12 October because it was a clean break for the new fiscal year (`steering-notes-2026-08.md:7-8`). Be exact about what survives:

FY2026 Q1 was Oct–Dec 2025 (`reconciliation-2026-08-28.md:24`), so **FY2027 Q1 is October–December 2026**. Any date after 1 October splits that quarter. The quarter is already gone.

What remains recoverable is the boundary below it. **Scenario A guarantees no accounting *month* is split.** Scenario B goes further and recovers the quarter itself — FY2027 Q1 closes wholly on legacy, FY2027 Q2 opens wholly on the new warehouse. That is a cleaner break than 12 October would ever have produced, because 12 October was itself eleven days into Q1.

### Why not 30 November

An earlier draft of this plan recommended Monday 30 November. It was wrong twice, and both errors are worth stating because they are the two questions the committee will ask:

1. **30 November is the last business day of November,** not the first of December. Going live that morning puts 30 November's orders on the new platform and 1–27 November's on legacy. That splits November — the exact failure the date was chosen to avoid.
2. **26–30 November 2026 is Thanksgiving through Cyber Monday.** For a publisher settling through five digital storefronts, that is the highest-volume revenue weekend of the year. Freezing feeds and repointing connections across it is not a scheduling inconvenience; it is a commercial outage at peak.

Both scenarios below turn that weekend from a hazard into an asset: the new platform processes the peak under observation while legacy remains the system of record. **No synthetic test data we could construct is worth as much as a verified Black Friday.**

---

## 2. Critical Path

```
T02 (curated tables + March bug fix)
  -> T03 Part 1 (backfill, pre-PTO)
  -> [PTO + vendor freeze + FY close: planned pause]
  -> T03 Part 2 (backfill, post-PTO)
  -> T13 (vendor settlement feed)   A: parallel, 2nd engineer | B: sequential on Whitlock
  -> T04 (parallel run)
  -> T05 (Finance sign-off)
  -> GATE -> cutover -> go-live
```

`T13` is on the critical path **only because Whitlock is a single resource**, not because of logical precedence. That is the entire difference between the two scenarios, and it is why the date is a funding decision.

**Descoping the report catalogue does not shorten this path** — reporting runs in parallel with float. Descoping still matters: it de-risks UAT and is the only source of capacity for the Studio Relations commitment (see `SCOPE.md`).

```
SCENARIO A - go-live Tue 1 December 2026

[Sep 1  - Sep 30] ===== T02 Curated tables + March bug fix (Whitlock) =====
[Sep 1  - Sep 18] ----- Legacy loader runbook + knowledge transfer (Whitlock 20% / IT Ops) -----
[Aug 17 - Sep 11] ..... T06 Day-One reports, 38 active (Okonkwo) .....
[Sep 14 - Sep 30] ..... T14 Studio scorecard: audit then build (Okonkwo) .....
[Oct 1  - Oct 8 ] ===== T03 Backfill Part 1 (6 of 12 workdays) =====
[Oct 5  - Oct 19] XXXXX VENDOR API FREEZE XXXXX
[Oct 5  - Oct 16] ##### FINANCE YEAR-END CLOSE #####
[Oct 9  - Oct 20] ***** WHITLOCK PTO (8 working days) *****
[Oct 19 - Nov 6 ] ..... T07 UAT (post-close, so Finance can attend) .....
[Oct 21 - Oct 28] ===== T03 Backfill Part 2 (Whitlock) =====
[Oct 21 - Nov 2 ] ===== T13 Vendor feed migration (SECOND ENGINEER, in parallel) =====
[Nov 3  - Nov 16] ===== T04 Parallel run =====
[Nov 9  - Nov 24] ..... T10 Training & comms (Incoming PM) .....
[Nov 9  - Nov 18] ..... T12b Cutover security & RBAC (Bekele) .....
[Nov 17 - Nov 18] ===== T05 Finance sign-off =====
[Nov 19         ] ||||| GO/NO-GO GATE |||||
[Nov 20 - Nov 22] >>>>> TECHNICAL CUTOVER (Fri eve - Sun) >>>>>
[Nov 23 - Nov 30] ~~~~~ SOAK: new platform live, LEGACY IS BOOK OF RECORD ~~~~~
                        (Thanksgiving 26th, Black Friday 27th, Cyber Monday 30th)
[Dec 1          ] ***** LEDGER FLIP - BUSINESS GO-LIVE *****
[Dec 1  - Dec 18] ..... T09 Hypercare .....
[Jan 11 - Jan 22] ..... T11 Legacy decommission (after 30-day dual run) .....


SCENARIO B - go-live Mon 4 January 2027   (September and October identical to A)

[Oct 29 - Nov 10] ===== T13 Vendor feed migration (Whitlock, sequential) =====
[Nov 11 - Dec 4 ] ===== T04 Parallel run, EXTENDED to 18 workdays =====
                        (covers Thanksgiving/Black Friday as shadow validation)
[Nov 9  - Dec 11] ..... T10 Training & comms .....
[Nov 30 - Dec 8 ] ..... T12b Cutover security & RBAC .....
[Dec 7  - Dec 8 ] ===== T05 Finance sign-off =====
[Dec 11         ] ||||| GO/NO-GO GATE |||||
[Dec 28 - Dec 31] >>>>> CUTOVER inside the year-end shutdown (4 workdays) >>>>>
[Jan 1          ] ----- public holiday: buffer before go-live -----
[Jan 4          ] ***** GO-LIVE - FY2027 Q2 opens on the new platform *****
[Jan 4  - Jan 22] ..... T09 Hypercare (lowest-volume month) .....
[Feb 8  - Feb 19] ..... T11 Legacy decommission .....
```

---

## 3. Work Breakdown Structure

**Float method:** `Total Float = working days in window − effort days`, computed identically for every row — the same method used against the inherited plan in `ASSESSMENT.md` Finding 6. Where a resource sits below 1.0 FTE the adjusted figure is in the notes. Every row is recomputed by `verify.py`, which parses this table directly: if a date here is wrong, the harness fails.

### Common to both scenarios (September – 28 October)

| ID | Task | Owner | Start | End | Effort | Window | Depends | Float | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T01 | Source system inventory | D. Whitlock | 2026-06-01 | 2026-07-10 | 28 | 30 | — | +2d | Complete. |
| T02 | Curated tables + March bug fix | D. Whitlock | 2026-07-13 | 2026-09-30 | 58 | 58 | T01 | 0d | 70% done. Extended from 25 to 30 Sep to absorb a 3-day fix. **Critical path.** |
| T06 | Reporting layer, 38 active reports | M. Okonkwo | 2026-08-17 | 2026-09-11 | 13 | 20 | — | +7d | Descope cuts 40d to 13d. At 0.9 FTE needs 14.4 elapsed: adjusted float +5.6d. |
| T12a | Security & access review, phase 1 | R. Bekele | 2026-09-07 | 2026-09-18 | 8 | 10 | — | +2d | 60% done. |
| T14 | Studio scorecard: audit, then build | M. Okonkwo | 2026-09-14 | 2026-09-30 | 10 | 13 | T06 | +3d | **First 2 days are an audit, not a build** — six scorecards already exist and all six are dead (`SCOPE.md` §6). Delivers on the FY2027 open. |
| T03a | Historical backfill, part 1 | D. Whitlock | 2026-10-01 | 2026-10-08 | 6 | 6 | T02 | 0d | Last 6 working days before PTO. **Critical path.** |
| T03b | Historical backfill, part 2 | D. Whitlock | 2026-10-21 | 2026-10-28 | 6 | 6 | T03a | 0d | Resumes the day after PTO ends. 12 effort days total. **Critical path.** |
| T07 | UAT, 38-report scope | M. Okonkwo / business leads | 2026-10-19 | 2026-11-06 | 10 | 15 | T06; T14 | +5d | Starts after Finance close ends 16 Oct so Finance-area reports get a real reviewer. |

### Scenario A — second engineer funded, go-live 1 December

| ID | Task | Owner | Start | End | Effort | Window | Depends | Float | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T13 | Vendor settlement feed migration | **2nd engineer** / Vendor | 2026-10-21 | 2026-11-02 | 9 | 9 | freeze ends 19 Oct | 0d | Runs **parallel** to T03 Part 2. This is what the funding buys. **Critical path.** |
| T04 | Parallel run | D. Whitlock | 2026-11-03 | 2026-11-16 | 10 | 10 | T03; T13 | 0d | **Critical path.** |
| T10 | Training & comms | Incoming PM | 2026-11-09 | 2026-11-24 | 10 | 12 | T07 | +2d | Reassigned from S. Alvear. |
| T12b | Cutover security & RBAC | R. Bekele **at 65%** | 2026-11-09 | 2026-11-18 | 5 | 8 | T04 | +3d | 5d over an 8-day window needs 62.5% FTE; 65% delivers 5.2d. Closes the 0%-security gap. |
| T05 | Finance sign-off | J. Reyes | 2026-11-17 | 2026-11-18 | 2 | 2 | T04 | 0d | **Critical path.** |
| GATE | Go/No-Go | Steering Committee | 2026-11-19 | 2026-11-19 | 1 | 1 | T05; T07; T12b | 0d | Thursday, one day before the window. |
| — | Technical cutover | Whitlock / IT Ops | 2026-11-20 | 2026-11-22 | — | — | GATE | n/a | Weekend window: 1 working day plus 2 non-working. |
| — | **Soak, legacy authoritative** | All | 2026-11-23 | 2026-11-30 | — | — | cutover | n/a | New platform processes the peak; legacy remains the book of record. Rollback is a config flip, not a restore. |
| — | **Ledger flip / go-live** | CFO | 2026-12-01 | 2026-12-01 | — | — | soak | n/a | November closed on legacy. December opens on the new platform. |
| T09 | Hypercare | Whitlock / team | 2026-12-01 | 2026-12-18 | 14 | 14 | go-live | 0d | |
| T11 | Legacy decommission | D. Whitlock | 2027-01-11 | 2027-01-22 | 10 | 10 | T09 | 0d | After the 30-day dual run. |

### Scenario B — no new headcount, go-live 4 January

| ID | Task | Owner | Start | End | Effort | Window | Depends | Float | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T13 | Vendor settlement feed migration | D. Whitlock / Vendor | 2026-10-29 | 2026-11-10 | 9 | 9 | T03 *(resource-sequential)* | 0d | **Critical path.** |
| T04 | Parallel run, extended | D. Whitlock | 2026-11-11 | 2026-12-04 | 18 | 18 | T03; T13 | 0d | 18 days rather than 10: the slack buys shadow validation across the peak weekend. **Critical path.** |
| T10 | Training & comms | Incoming PM | 2026-11-09 | 2026-12-11 | 10 | 25 | T07 | +15d | |
| T12b | Cutover security & RBAC | R. Bekele **at 75%** | 2026-11-30 | 2026-12-08 | 5 | 7 | T04 | +2d | 75% over 7 wd delivers 5.25d against 5d effort. |
| T05 | Finance sign-off | J. Reyes | 2026-12-07 | 2026-12-08 | 2 | 2 | T04 | 0d | **Critical path.** |
| GATE | Go/No-Go | Steering Committee | 2026-12-11 | 2026-12-11 | 1 | 1 | T05; T07; T12b | 0d | Two weeks before the window, so a No leaves room to act. |
| — | Cutover, year-end shutdown | Whitlock / IT Ops | 2026-12-28 | 2026-12-31 | — | 4 | GATE | n/a | Four working days at the lowest transaction volume of the year. |
| T09 | Hypercare | Whitlock / team | 2027-01-04 | 2027-01-22 | 14 | 15 | go-live | +1d | |
| T11 | Legacy decommission | D. Whitlock | 2027-02-08 | 2027-02-19 | 10 | 10 | T09 | 0d | After the 30-day dual run. |

---

## 4. Staffing Changes Required

**1. D. Whitlock — break the single point of failure.** Planned at 120–160% across conflicting workstreams, peaking at 160% in the weeks of 5 and 12 October. Offload **100% of run-the-business legacy loader support** to IT Ops or a contractor.

*Honest September split:* Whitlock cannot be at 100% on T02 while also transferring the loader. Through 18 September: **80% T02 / 20% knowledge transfer** (about 3 days — recorded walkthroughs plus review of a runbook the receiving engineer writes). From 21 September: 100% T02.

*The arithmetic:* T02 remaining = 30% × 58 = **17.4 effort days**. September capacity = (14 wd × 0.8) + (8 wd × 1.0) = **19.2 days**. Margin **+1.8 days** — thin, which is why the offload is a committee decision and not a preference.

**2. M. Okonkwo — descope and redeploy.** At 90% attempting 120 reports (40 effort days = 44.4 elapsed at 0.9 FTE, which slips past 9 October unaided). Descope to the **38 active reports, 13 effort days**, freeing **27 effort days**: 10 to the studio scorecard (`T14`, audit first), 5 to source remediation for the 10 active reports fed by Excel extracts, the balance to UAT support.

**3. J. Reyes — protect, don't negotiate.** Zero programme demands during close (5–16 Oct). UAT from 19 October, sign-off after the close in both scenarios.

**4. R. Bekele — fund the level, not just the extension.** The inherited plan drops security to **0% from the week of 12 October**, through cutover and hypercare. `T12b` needs 5 effort days. Over its 8-day window in Scenario A that is **65% FTE**; over its 7-day window in Scenario B, **75%**. Not the 10% Bekele has been carrying — an extension at 10% would deliver 0.9 days against a 5-day task.

**5. Incoming PM.** S. Alvear departs 30 September while allocated 60% across five later weeks. Incoming PM takes `T10`, governance and SteerCo reporting from 1 October.

**6. Scenario A only — the second engineer.** One engineer (or a vendor-led migration) for `T13`, roughly 9 working days from 21 October. No such person exists anywhere in `resource-allocation.csv`. This is the single line item that separates 1 December from 4 January.

> **Planning assumption.** `resource-allocation.csv` ends at the week of 2 November 2026. Every allocation from 9 November onward is an assumption requiring committee ratification, not an inherited fact.

> **Estimating assumption.** The **3 engineering days** inside T02 for the March defect is an estimate made before root cause is known; no artifact supports it. **Decision trigger: if diagnosis is not complete by 18 September, the fix no longer fits and the date moves.** Reported to the committee, not managed silently. `ASSESSMENT.md` Finding 2 narrows the likely cause to a single ingestion batch, which is what makes 3 days plausible rather than arbitrary.

---

## 5. Cutover Execution

### Sequence — Scenario A (20–22 November, then soak)

| Phase | When | Actions | Lead |
|---|---|---|---|
| 1 Freeze | Fri 20 Nov 17:00 | Code freeze. Final delta load on legacy. Freeze reporting changes. | D. Whitlock |
| 2 Ingest & reconcile | Fri 20 Nov 20:00 – Sat 21 Nov 04:00 | Final sync from aggregator (v3) and platforms. Automated reconciliation. | Whitlock / Vendor |
| 3 Verification gate | Sat 21 Nov 08:00–12:00 | Row counts, order totals, revenue across 5 storefronts and 5 titles. **March 2026 verified at 0.00%.** | J. Reyes / PM |
| 4 Traffic cutover | Sat 21 Nov 14:00–18:00 | Repoint the BI alias to the cloud warehouse. Deploy the portal against new endpoints. | IT Ops / Whitlock |
| 5 Smoke tests | Sun 22 Nov 09:00–15:00 | Synthetic queries; all 38 Day-One reports; role permissions. | Okonkwo / Bekele |
| 6 **Soak** | Mon 23 – Mon 30 Nov | New platform serves reporting and processes the peak. **Legacy remains the book of record.** Daily delta reconciliation, including a full Black Friday comparison. | Whitlock / Reyes |
| 7 **Ledger flip** | Tue 1 Dec 09:00 | New warehouse becomes the system of record. November's books close on legacy, unsplit. | CFO |

The soak is the point. For eight days, including the peak weekend, a rollback costs a configuration flip rather than a data restore, and Finance can compare a real high-volume period side by side before signing the ledger over.

### Sequence — Scenario B (28–31 December)

Same seven-step shape, compressed into the year-end shutdown: freeze Mon 28 Dec, ingest and reconcile Mon–Tue, verification gate Wed 30 Dec, traffic cutover Wed afternoon, smoke tests Thu 31 Dec, holiday buffer Fri 1 Jan, go-live Mon 4 Jan. The peak weekend was already validated inside the 18-day parallel run, so there is no soak; the quarter boundary does the work the soak does in Scenario A.

### Go/No-Go

- **Authority:** unanimous consent among **CFO** (financial), **IT Director** (technical), **VP Publishing Operations** (operational), **Incoming PM** (execution).
- **A single No stops the cutover.** No override. Fallback from Scenario A is Scenario B; fallback from Scenario B is Monday 1 February 2027. There is no "push through the weekend".

**Go criteria — all six, no partial credit:**
1. Legacy-to-new delta on core financials across FY2026 and FY2027-to-date is **0.00%**, evaluated **monthly, not annually**. March 2026 verified fixed.
2. The v3 settlement feed has produced **5 consecutive days** of verified error-free ingestion.
3. All 38 Day-One reports validated and passing UAT smoke tests.
4. RBAC matrix signed off by R. Bekele (`T12b`); no critical access findings open.
5. Rollback runbook **tested in staging**, with a timed rehearsal on record.
6. **Scenario A only:** the soak has completed a full peak-weekend reconciliation at 0.00% before the ledger flips.

### Rollback

**1. Dual ingestion, 30 days.** The legacy SSIS loader is **not** decommissioned at cutover. Raw ingestion is dual-written to the cloud landing zone and to legacy staging (or replayed daily from the bronze layer) for 30 days after go-live. `T11` is scheduled accordingly — January in A, February in B. This is the cost of a real rollback and it is deliberate.

*Vendor caveat:* the settlement feed migrates v2 → v3. Dual ingestion therefore requires either that the legacy loader can consume the v3 schema, or that the vendor maintains the v2 endpoint through the dual-run window. **Confirming which is a precondition of the gate**, and it is the one dependency in this plan that Twin Hearth does not control.

**2. Connection reversion, RTO under 2 hours.** Reporting and BI connect through an abstraction alias (`edw-bi.twinhearth.internal`), never a direct host. Rollback repoints the alias to the on-premise cluster. **RTO 2 hours, RPO under 4 hours** via delta replay. During the Scenario A soak, RTO is minutes: legacy never stopped being authoritative.

**3. Authority and triggers.** Incident Commander is the IT Director, with CFO concurrence for anything touching financial reporting. Non-negotiable triggers: revenue divergence **above 0.1%** not root-caused within 4 hours; settlement ingestion failure beyond **12 hours** with no hot fix; warehouse outage beyond **4 business hours** at peak. **Rollback is pre-authorised at the gate** so nobody seeks permission at 03:00.

---

## 6. Budget Impact

| | Scenario A | Scenario B |
|---|---|---|
| Added duration vs 12 Oct | 50 days (7.1 weeks) | 84 days (12 weeks) |
| Contractor backfill, legacy loader | **~220 hours** (5.5 FTE-weeks) | **~284 hours** (7.1 FTE-weeks) |
| Additional engineer | ~9 working days for `T13` | none |
| Security uplift | Bekele 10% → 60% for 8 working days | Bekele 10% → 75% for 7 working days |

Contractor hours are derived from the run-the-business lines of `resource-allocation.csv` (390 percentage-weeks present in the artifact from 7 Sep to 2 Nov) plus assumed 40% weeks to go-live, not estimated freehand.

**On the inherited budget figure.** August reported *"71% consumed against 74% elapsed"*. Against the committed 12 October cutover, elapsed on 31 August was **68.4%** (91 of 133 calendar days; 68.8% by working days). The 74% only reconciles against a 30 September end date, which was never the committed date. Corrected, the programme was **spending ahead of schedule, not behind it** — the budget green was the same artefact of a fictional baseline as the schedule green. Cloud cost modelling is out of scope; this is staffing burn, which the CFO will ask about.

---

## 7. Defensibility Summary

| Challenge | The 12 October plan | This plan |
|---|---|---|
| March revenue defect | Hidden behind an annual ±5% gate. | 3 days inside T02 with an 18 Sep decision trigger. Gate criterion moves to **monthly** 0.00%. |
| Whitlock PTO 9–20 Oct | Cutover scheduled mid-PTO at 160% allocation. | Planned pause. Backfill splits 6d + 6d. No task assumes he is present. |
| Vendor freeze 5–19 Oct | `T13` scheduled wholly inside it. | A: 21 Oct – 2 Nov. B: 29 Oct – 10 Nov. Both after the freeze, both with the full 9 days. |
| Finance close 5–16 Oct | Assumed Finance would "work around it". | Zero demands during close; sign-off well after it in both scenarios. |
| Dependency inversions | Four (T08/T05, T04/T13, T07/T06, T03/T02). | Strict precedence restored; every predecessor finishes first. |
| Zero float | 9 of 13 tasks at zero float. | Declared per task by a reproducible method; non-critical work carries +2 to +15 days. |
| Security coverage | 0% from 12 Oct, through cutover and hypercare. | `T12b` at the FTE the task actually needs; RBAC sign-off is a Go criterion. |
| Fiscal boundary | Claimed a clean break it could not deliver. | A: no month split. B: no quarter split. Both state plainly what is already lost. |
| **Peak trading season** | **Not considered at all.** | Cutover moved off it; the peak becomes validation evidence in both scenarios. |
| Rollback | None, and decommission two weeks after go-live. | 30-day dual run, RTO under 2h, pre-authorised triggers, decommission deferred, vendor v2/v3 dependency named as a gate precondition. |
