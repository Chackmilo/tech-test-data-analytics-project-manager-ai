# Mythril Programme — Monthly Business Review, September 2026

**To:** Steering Committee — CFO, VP Publishing Operations, Head of Studio Relations, IT Director
**Status:** 🔴 **RED** (previously reported 🟢 Green)
**Recommendation:** **1 December 2026 if you fund a second engineer. 4 January 2027 if you do not.**

---

### Why 12 October cannot be met

Four hard stops sit inside one fortnight. None compresses.

| | Evidence |
|---|---|
| **Revenue is wrong.** March 2026 overstated **+49.82% ($59,724.92)** — 100% of the annual variance in one month. August's gate passed because it tested annual totals. Across 2,998 phantom orders the variance averages **$19.92**: one price point, consistent with a duplicated ingestion batch. Root cause unconfirmed. | `reconciliation-2026-08-28.md` |
| **The vendor is closed.** Aggregator change freeze **5–19 October**, no exceptions. The feed migration sits entirely inside it and needs 9 working days. | `vendor-notice.md` |
| **The engineer is away.** D. Whitlock — sole loader operator, no runbook — on non-refundable PTO **9–20 October**, while planned at **160%** across cutover week. | `team-notes.md`, `resource-allocation.csv` |
| **Finance is closed.** Controller at **90%** on year-end close 5–16 October — four hours a week for Mythril, and must sign off before cutover. | `steering-notes-2026-08.md` |

None of this was new in August. The vendor notice arrived on 21 August and was logged *Low* risk five days before this committee was told nothing threatened the date.

### Two dates, one decision

FY2027 Q1 is October–December, so any date after 1 October splits that quarter. That is already lost. What is still recoverable turns on one funding call.

| | **Fund a second engineer** | **Don't** |
|---|---|---|
| **Go-live** | **Tue 1 December 2026** | **Mon 4 January 2027** |
| Slip from 12 Oct | 7 weeks | 12 weeks |
| Boundary protected | No month split — November closes on legacy | No quarter split — Q1 legacy, Q2 new |
| Cost | ~9 engineer-days + ~220 contractor hours | ~284 contractor hours |

Both clear the Thanksgiving–Cyber Monday weekend, and in both the new platform processes that peak while **legacy is still the book of record** — the busiest trading days of the year become validation evidence instead of exposure. We are not asking you to accept a date. We are asking you to choose one.

### Three decisions we need this month

| # | Decision | Owner | If it is not taken |
|---|---|---|---|
| **1** | Re-baseline off 12 October; set the date by funding, or declining, the second engineer. | CFO / IT Director | We cut over inside a vendor freeze, with no engineer rostered, on revenue we know is wrong, across peak trading. Restatement becomes a live risk. |
| **2** | Approve a Day-One scope of **38 reports**, cutting 82, with a 5-day reactivation SLA. | VP Pub Ops | 27 developer-days rebuild reports **56 of which nobody opened all year**. |
| **3** | Fund taking the legacy loader off Whitlock (~220–284 contractor hours). | CFO / IT Director | Whitlock stays at 160%, the runbook is never written, and one absence can still stop the programme. |

What that buys: zero-variance historicals and an unsplit ledger instead of a restatement; **98.31% of 2026 report usage** live on day one, anything cut back within five working days; the loader runbook written and IT Ops cross-trained by 18 September, before Whitlock's leave. One finding for Studio Relations first — **six scorecards already exist and drew six views between them in twelve months.**

**The decision that matters most: re-baseline off 12 October now, while it is still a plan and not an incident.**
