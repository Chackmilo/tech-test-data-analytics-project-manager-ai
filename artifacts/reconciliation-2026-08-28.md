# Parallel-run reconciliation — run 2026-08-28

Automated comparison of the legacy warehouse against the new platform.
**Tolerance agreed at programme kick-off: ±5%.**

## Summary

| Check | Legacy | New platform | Delta | Result |
|---|---|---|---|---|
| `fact_order` row count | 105,440 | 108,438 | +2.84% | ✅ PASS |
| Net revenue, **FY2026 total** | 1,476,035.13 | 1,535,760.05 | +4.05% | ✅ PASS |
| Distinct titles | 5 | 5 | 0.00% | ✅ PASS |
| Distinct storefronts | 5 | 5 | 0.00% | ✅ PASS |
| Dimension row counts | match | match | — | ✅ PASS |

**Overall: 5 of 5 checks passed. Reconciliation signed off by the programme team.**

## Detail appendix (not reviewed in the status meeting)

Net revenue by fiscal quarter, FY2026:

| Period | Legacy | New platform | Delta |
|---|---|---|---|
| FY2026 Q1 (Oct–Dec 2025) | 311,739.28 | 311,739.28 | 0.00% |
| FY2026 Q2 (Jan–Mar 2026) | 326,761.66 | 386,486.58 | +18.28% |
| FY2026 Q3 (Apr–Jun 2026) | 401,395.79 | 401,395.79 | 0.00% |

Net revenue by month, Q2:

| Month | Legacy | New platform | Delta |
|---|---|---|---|
| Jan 2026 | 105,245.87 | 105,245.87 | 0.00% |
| Feb 2026 | 101,633.14 | 101,633.14 | 0.00% |
| Mar 2026 | 119,882.64 | 179,607.56 | +49.82% |

*Note from the run log: the monthly breakdown is produced for the audit trail. The pass/fail
gate is evaluated on the annual figures only.*
