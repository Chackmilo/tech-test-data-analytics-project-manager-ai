# Mythril Programme — Monthly Business Review, September 2026

**To:** Steering Committee — CFO, VP Publishing Operations, Head of Studio Relations, IT Director
**Status:** 🔴 **RED** (previously reported 🟢 Green)
**Recommendation:** **1 December 2026 if you fund a second engineer. 4 January 2027 if you do not.**

---

### The date

**12 October cannot be met.** Not compressed, not de-scoped, not worked around. Four hard stops sit inside one fortnight:

| | Evidence |
|---|---|
| **Revenue data is wrong.** March 2026 overstated by **+49.82% ($59,724.92)** — **100% of the annual variance in one month.** August passed only because the gate tested annual totals. The variance divided by the 2,998 phantom orders averages **$19.92** — a single price point, consistent with one duplicated ingestion batch rather than drift. Root cause is not yet confirmed. | `reconciliation-2026-08-28.md` |
| **The vendor is closed.** Aggregator change freeze **5–19 October**, no exceptions. The feed migration was scheduled entirely inside it and needs 9 working days. | `vendor-notice.md` |
| **The engineer is away.** D. Whitlock — sole loader operator, no runbook — on approved, non-refundable PTO **9–20 October**, while planned at **160%** across cutover week. | `team-notes.md`, `resource-allocation.csv` |
| **Finance is closed.** Controller at **90% on year-end close 5–16 October** — 4 hours a week for Mythril, and must sign off before cutover. | `steering-notes-2026-08.md` |

None of this was new in August. The vendor notice arrived 21 August, logged *Low* risk five days before this committee was told nothing threatened the date — in a status report that listed cutover on 12 October **above** parallel-run completion on 14 October.

### Two dates, one decision

FY2027 Q1 is October–December, so any date after 1 October splits that quarter. That is lost. What remains recoverable depends on one funding call:

| | **Fund a second engineer** | **Don't** |
|---|---|---|
| **Go-live** | **Tue 1 December 2026** | **Mon 4 January 2027** |
| Slip from 12 Oct | 7 weeks | 12 weeks |
| Boundary protected | November closes on legacy, December opens clean — **no month split** | **No quarter split** — Q1 all legacy, Q2 all new |
| Cost | ~9 engineer-days + ~220 contractor hours | ~284 contractor hours |

Both go live clear of the Thanksgiving–Cyber Monday weekend. In each, the new platform processes that peak while **legacy is still the book of record** — the year's busiest trading days become validation evidence instead of exposure. We are not asking you to accept a date. We are asking you to choose one.

### Three decisions we need this month

| # | Decision | Owner | If it is not taken |
|---|---|---|---|
| **1** | Re-baseline off 12 October and pick the date by funding — or declining — the second engineer. | CFO / IT Director | We attempt cutover during a vendor freeze, with no engineer rostered, on revenue we know is wrong, across the peak trading weekend. Restatement becomes a live risk. |
| **2** | Approve a Day-One scope of **38 reports**, cutting 82, with a 5-day reactivation SLA. | VP Pub Ops | 27 developer-days go into rebuilding reports **56 of which nobody opened all year**. |
| **3** | Fund the extension and take the legacy loader off Whitlock (~220–284 contractor hours). | CFO / IT Director | Whitlock stays at 160%, the runbook is never written, and one person's absence can still stop the programme. |

### What each of you gets

- **CFO** — audited, zero-variance historicals and an unsplit ledger instead of a restatement. August's *"71% consumed against 74% elapsed"* was measured against a date that was never real; against 12 October, elapsed was **68.4%**. We were spending ahead of schedule, not behind it.
- **VP Publishing Operations** — every report anyone opened in 2026 live on day one: **98.31% of all usage**. Anything cut returns in 5 working days on request.
- **Head of Studio Relations** — capacity is reserved for your scorecard, but one honest finding first: **six already exist and drew 6 views between them in twelve months.** We want two days with you to learn why those died before we build a seventh.
- **IT Director** — single point of failure closed: loader runbook written and IT Ops cross-trained by 18 September, before Whitlock's leave. Security funded through cutover at the level the work needs, not the 10% it carried.

**The decision that matters most: re-baseline off 12 October now, while it is still a plan and not an incident.**
