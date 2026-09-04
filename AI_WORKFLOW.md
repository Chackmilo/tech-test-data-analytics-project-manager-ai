# Mythril Programme — AI Workflow & Verification Audit

**Author:** Incoming Data & Analytics Project Manager
**Date:** 31 August 2026
**Document:** How AI was used, what it got wrong, and how that was caught

---

## 1. Tooling and Why

An AI coding agent with repository access was paired with **local Python execution over the artifacts**. The division of labour was deliberate:

1. **Cross-referencing eight fragmented artifacts.** Status notes, meeting minutes, a vendor notice and three CSVs that disagree with each other. Synthesising qualitative claims against quantitative records is what a language model is genuinely good at.
2. **Never trusting it with arithmetic.** Language models are unreliable at summing columns and counting working days, and — worse — they are *fluent* while being wrong. Every number in this submission is produced by a script, not by generation.
3. **Executive translation.** Turning ETL constraints into ledger consequences the CFO can act on.

**What the AI was never allowed to do:** state a number that a script had not computed. That rule was broken repeatedly in drafting — six times, including once by the script itself. All six are documented in §3.

---

## 2. Prompts and What Came Back

### Prompt 1 — Reconciliation forensics
```text
"Inspect artifacts/reconciliation-2026-08-28.md. Compare the summary table against the
detail appendix. Calculate exact dollar and percentage deltas by quarter and month. Is
the 5% tolerance check sound from an audit perspective?"
```
**Returned:** the annual variance was +4.05% (`+$59,724.92`), while Q1, Q3, January and February were all at 0.00% delta and March 2026 was at **+49.82% (+$59,724.92)**. The model correctly identified that the annual figure and the March figure are *the same dollar amount* — one defect, 100% of the error — and that a gate evaluated on annual aggregates would pass data that fails any monthly audit.

### Prompt 2 — Resource and calendar collision mapping
```text
"Cross-reference project-plan.csv, resource-allocation.csv, team-notes.md and
vendor-notice.md. Map D. Whitlock's weekly allocations, PTO and assigned tasks across
October 2026. What physical conflicts exist?"
```
**Returned:** Whitlock planned at **160%** in the weeks of 5 and 12 October (70% + 50% + 40%), holding approved PTO 9–20 October, while owning cutover, hypercare, parallel run and the vendor migration inside that window — and `T13` scheduled entirely inside the vendor's change freeze.

### Prompt 3 — Report telemetry triage
```text
"Write and run a Python script over report-usage.csv. Tier reports by usage (zero views,
viewed in 2026, viewed before 2026). Compute the cumulative share of views captured by
the 2026 tier. Audit the source column and flag anomalies in last_viewed."
```
**Returned, via script:** 120 reports, 2,309 views. 56 with zero views (46.67%). 38 viewed in 2026 holding 2,270 views (**98.31%**). 26 dormant holding 39. Ten of the 38 sourced from Excel extracts rather than the EDW. And an anomaly nobody was looking for: **19 reports report `views_last_12m > 0` with a `last_viewed` older than 12 months** — the telemetry contradicts itself.

### Prompt 4 — Constraint-driven schedule modelling
```text
"Model a revised schedule from 1 September 2026. Constraints: Whitlock PTO 9-20 Oct
inclusive; vendor freeze 5-19 Oct inclusive; vendor needs 9 working days; T03 is 12 days
and must split around the PTO; T04 needs 10 days; T05 needs 2. Whitlock cannot be
double-allocated. Find the earliest cutover that lands on a clean accounting boundary."
```
**Returned, via script:** backfill splits 1–8 October (6 working days) and 21–28 October (6), vendor migration follows, then parallel run, sign-off, gate, cutover. It produced Monday 30 November as the earliest "clean boundary" date. **That answer was wrong, and §3.5 explains why the constraint list was the reason.**

### Prompt 5 — Adversarial review of the finished submission
```text
"You are grading this submission against README.md. Re-derive every number yourself from
artifacts/. Do not trust verify.py - it was written by the author it validates, so audit
it for tautologies and hardcoded expectations. Find what the submission missed."
```
**Returned:** four material defects and four missed findings, including both halves of the error in §3.5. This prompt was worth more than the previous four combined, and it is the reason the recommended date changed. A second run of the same prompt, narrowed to hunt unsupported claims and to attack the harness directly, produced §3.6.

---

## 3. Where the AI Was Confidently Wrong

Six failures, all caught by code or by adversarial review. Five share a signature: sound reasoning, correct-looking shape, invented number. The sixth is worse than that, and it is the one worth reading.

### 3.1 — "24 of the 42 rebuilt reports are ghosts"
An early draft asserted that of the 42 reports Okonkwo had rebuilt, 24 were zero-view ghosts.

**Why it was seductive:** it is *almost* true. Of the first 42 rows of `report-usage.csv`, exactly 24 do carry zero views. The number is real.

**How it was caught:** searching for the evidence to cite. `report-usage.csv` contains **no build order and no completion flag**. The claim silently assumed Okonkwo worked in ID order.

**Fixed:** withdrawn and replaced with the defensible statement — expected value ~20 of 42 if the rebuild was not usage-prioritised, and establishing which 42 were built is question one for Okonkwo.

### 3.2 — "8 working days before the PTO"
The model proposed starting backfill on 1 October and claimed 8 of its 12 days would complete before the PTO.

**How it was caught:** counting them. `Oct 1 (Thu), 2 (Fri), 5 (Mon), 6 (Tue), 7 (Wed), 8 (Thu)` = **6 working days, not 8**.

**Fixed:** all date arithmetic moved to `datetime` and asserted in `verify.py`.

### 3.3 — "17 core report families"
The model claimed the 38 active reports condensed into 17 families.

**How it was caught:** normalising the titles programmatically produced **24**. The 17 was a plausible-sounding estimate with nothing behind it.

**Fixed:** replaced with the computed 24.

### 3.4 — A fabricated Total Float column
A draft of `PLAN.md` published float for every task: `T02 0d`, `T06 +15d`, `T12 +5d`, `T09 +5d`, `T10 +2d`, `T14 +10d`.

**How it was caught:** recomputing `window − effort` for every row. **Six of fifteen disagreed**, and `T02` came back at **−2 days** — 58 effort days in a 56-day window. The head of the critical path was over-committed while the table read `0d`.

**Why this one was dangerous:** `ASSESSMENT.md` Finding 6 attacks the inherited plan *precisely* for zero float. Publishing an invented float column while making that argument would have handed the committee the one rebuttal that discredits everything else.

**Fixed:** dates corrected, the method stated in the table header, and `verify.py` now parses the table out of `PLAN.md` rather than holding its own copy.

### 3.5 — The recommended date was wrong twice, and the harness could not see it
The most instructive failure. `PLAN.md` recommended **Monday 30 November 2026** and told the CFO, in writing, that it meant *"no accounting month is ever split across two systems."*

**Both halves were wrong:**

1. **30 November is the last business day of November,** not the first of December. Going live that morning puts 30 November's transactions on the new platform and the rest of the month's on legacy. It splits the exact month it claimed to protect.
2. **26–30 November 2026 is Thanksgiving through Cyber Monday** — the highest-volume trading weekend of the year for a publisher settling through five digital storefronts. The plan scheduled a feed freeze and a connection repoint straight through it.

**Why the AI produced it:** it answered the question it was given. Prompt 4 listed the PTO, the freeze, the fiscal close and the task durations. It did not mention the retail calendar, and it did not ask the model to distinguish a month's *last* business day from the next month's *first*. **The model was not hallucinating; it was optimising against an incomplete constraint set.** That is a harder failure mode than invention, because the output is internally consistent and confidently argued.

**Why the harness missed it:** `verify.py` at that point contained a literal `check("FY2027 Q1 contains December 2026", True, True)` — an assertion that cannot fail. It also hardcoded the reconciliation figures without opening the artifact, hardcoded the revised schedule without reading `PLAN.md`, and never read five of the eight artifacts at all. It reported 109 passing checks and manufactured confidence in a wrong date.

**Fixed:** the date became two dates contingent on a funding decision (1 December or 4 January, `PLAN.md` §1), the peak-trading calendar is now both a scheduling constraint and a Go criterion, and the harness was rebuilt from scratch (§4).

**The lesson worth carrying:** the AI's answer was only as good as the constraint list it was given, and the test meant to catch it had been written by the same process that produced the error. Neither is a reason to stop using AI. Both are reasons to have something attack the output that did not write it.

### 3.6 — The test written to prevent §3.5 was empty

After the Black Friday error, the harness was rebuilt and this document was updated to say the
lesson had been learned. A second external audit then ran three mutations nobody had thought to try.

```text
MISSED  move the technical cutover ONTO the Black Friday weekend
MISSED  change the recommended go-live to a mid-month date that splits December
MISSED  under-staff security in the budget table while the WBS still says 65%
```

**All three passed silently.** Three separate mechanisms, each invisible on reading:

1. **A guard loop over an empty list.** The peak-trading check ran
   `re.findall(r"\*\*(\d{4}-\d{2}-\d{2})\*\* \| \*\*(\d{4}-\d{2}-\d{2})\*\*", plan_md)`, which
   matches **zero lines** in `PLAN.md`. The loop body never executed. The check reported nothing,
   failed nothing, and looked exactly like a passing test.
2. **A parser that skipped the rows that mattered.** WBS rows were matched on
   `^(T\d+[ab]?|GATE)$`. The cutover, soak and ledger-flip rows carry an **em-dash** in the id
   column, so the four rows carrying the actual cutover dates were invisible to the harness.
3. **Whole sections never parsed.** Neither the recommended-date header, the scenario table, nor the
   section 6 budget table was read at all. That last gap was hiding a live defect: the budget table
   still said Bekele at **60%** while the WBS said **65%**, and 5 effort days over an 8-day window
   needs 62.5%.

**Why this is the worst of the six.** Section 3.5 above identifies the previous harness's fatal flaw
as *"assertions that could not fail"* and presents the rebuild as the correction. The rebuilt harness
contained an assertion that could not fail (`date(2026, 10, 12) < date(2026, 10, 14)` — two
literals) and a loop that never ran. **And the loop that never ran was the one guarding the exact
constraint whose absence caused the error in 3.5.** A test was written to prevent a specific mistake,
that test was empty, and 246 green checks reported otherwise.

The failure did not recur because the lesson was wrong. It recurred because the fix was verified by
the same process that needed fixing.

**Fixed:** the guard now iterates over rows parsed from the document (2 cutover windows found, both
tested); milestone rows are parsed regardless of their id column; go-live dates are read from the
header *and* the scenario table and cross-checked against each other, the calendar and `MBR.md`; the
budget table is parsed and reconciled against the WBS; the tautology is replaced by a comparison of
two dates parsed from the status report. Imported calendar facts — the peak window, the 1 January
holiday — now sit in one clearly labelled `DECLARED OUTSIDE KNOWLEDGE` block, so a reader can see
exactly which non-artifact facts the plan leans on. The three audit mutations are permanent cases in
`mutation_test.py`, which now runs **8 of 8 caught**.

**The lesson, restated properly.** A green test suite is a claim, not evidence. The evidence is a
failing one. If you cannot show the moment your harness said no, you have not tested anything — and
"I already fixed that class of bug" is precisely the belief that lets it back in.

---

## 4. How the CSVs Were Analysed, and How the Output Was Checked

**Rule 1: never ask the model for arithmetic.** Questions like *"how many reports have zero views?"* were never answered by generation. The model wrote a script; the script answered.

**Rule 2: the harness must parse, not restate.** `verify.py` was rebuilt after the audit in §3.5. It now:

- parses the markdown tables in `reconciliation-2026-08-28.md` and recomputes **the artifact's own published percentages**;
- extracts the freeze window from `vendor-notice.md`, the PTO from `team-notes.md`, the milestone table and budget line from `status-report-2026-08.md`, and the commitments from `steering-notes-2026-08.md` — **all eight artifacts are read**, where the previous version read three;
- parses the WBS tables out of `PLAN.md` and recomputes every float from the dates published there;
- opens each citation in `ASSESSMENT.md` and confirms the file and the line range exist;
- derives constraints rather than asserting them — the peak-trading window is computed from the calendar (fourth Thursday of November), not typed in.

**Rule 3: prove the test can fail.** A passing suite is not evidence unless it fails when the truth changes. `mutation_test.py` corrupts one source of truth at a time and confirms the harness notices:

```text
CAUGHT  shorten a critical-path task window in PLAN.md by 3 days
CAUGHT  alter the March revenue figure in the artifact
CAUGHT  extend the vendor freeze so T13 now starts inside it
CAUGHT  rename a scorecard so Finding 12's count drops to 5
CAUGHT  under-staff T12b below what its effort needs
CAUGHT  move the technical cutover ONTO the Black Friday weekend
CAUGHT  change the recommended go-live to a mid-month date that splits December
CAUGHT  under-staff security in the budget table while the WBS still says 65%

All 8 mutations caught. The harness can fail.
```

The last three came from an external audit and **all three passed silently before the fix in
§3.6**. They are permanent cases now: a mutation suite that omits the attack you have already
suffered is decoration.

The rebuilt harness runs **276 checks across all eight artifacts and all six deliverables**. During its own construction it caught four further defects in documents that had already been reviewed twice: a task window that could not satisfy its own published float, a security task staffed at 60% when its effort needed 62.5%, a task spanning the PTO it was supposed to avoid, and a citation count that had gone stale.

**The test of everything above is one command.** Run `python verify.py`. If a number in any deliverable is not in its output, that number should not be believed — including by the person who wrote it.
