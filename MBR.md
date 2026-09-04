# Mythril Programme — Monthly Business Review, September 2026

**To:** Steering Committee — CFO, VP Publishing Operations, Head of Studio Relations, IT Director
**Status:** 🔴 **RED** (previously reported 🟢 Green)
**Recommendation:** Re-baseline production cutover to **Monday, 30 November 2026**

---

### The date

**12 October cannot be met.** Not compressed, not de-scoped, not worked around. Four independent hard stops sit inside the same fortnight:

| | Evidence |
|---|---|
| **Revenue data is wrong.** March 2026 is overstated by **+49.82% ($59,724.92)**. The August reconciliation passed only because the gate was tested on annual totals. **That one month is 100% of the annual variance.** | `reconciliation-2026-08-28.md` |
| **The vendor is closed.** Storefront aggregator change freeze, **5–19 October**, no exceptions. The settlement feed migration was scheduled entirely inside it and needs 9 working days. | `vendor-notice.md` |
| **The engineer is away.** D. Whitlock — sole operator of the legacy loader, no runbook — has approved, non-refundable PTO **9–20 October**, while planned at **160%** allocation across cutover week. | `team-notes.md`, `resource-allocation.csv` |
| **Finance is closed.** Controller at **90% on fiscal year-end close, 5–16 October** — 4 hours a week for Mythril, and Finance must sign off before cutover. | `steering-notes-2026-08.md` |

None of this was new information in August. The vendor notice arrived on 21 August and was logged as a *Low* risk five days before this committee was told nothing threatened the date.

### Why 30 November, and not sooner

FY2027 Q1 runs October–December, so **any** date after 1 October splits that quarter — that is not recoverable. What is recoverable is the month. **30 November means November closes entirely on legacy and December opens entirely on the new platform: no accounting month is ever split across two systems.** That is the property the audit tests.

We priced going faster. A second engineer running the vendor migration in parallel buys **one week** and lands go-live mid-month, forfeiting the clean boundary. We do not recommend it.

### Three decisions we need this month

| # | Decision | Owner | If it is not taken |
|---|---|---|---|
| **1** | Re-baseline cutover to **30 November** and notify the board. | CFO | We cut over during a vendor freeze, with no engineer, on corrupted revenue — then restate. |
| **2** | Approve a Day-One scope of **38 reports**, cutting 82, with a 5-day reactivation SLA. | VP Pub Ops | The BI developer spends 27 days rebuilding reports **56 of which nobody opened all year**, and the FY2027 Studio Scorecard is not built at all. |
| **3** | Fund the extension: **7 weeks** of team burn plus **~220 contractor hours** to take the legacy loader off Whitlock. | CFO / IT Director | Whitlock stays at 160%, the runbook is never written, and one person's absence remains able to stop the programme. |

### What each of you gets

- **CFO** — audited, zero-variance historicals and a clean December ledger, instead of a restatement.
- **VP Publishing Operations** — every report anyone opened in 2026 live on day one; that is **98.31% of all usage**. Anything cut comes back in 5 working days on request.
- **Head of Studio Relations** — the FY2027 Studio Scorecard, unfunded and unbuilt until now, **delivered 30 September** out of the capacity descoping frees.
- **IT Director** — the single-point-of-failure closed: legacy loader runbook written and IT Ops cross-trained by 18 September, before Whitlock's leave.

**The one decision that matters most: approve the 30 November re-baseline now, while it is still a plan and not an incident.**
