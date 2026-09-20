# PARK memo — event-driven execution of the live band (idea 1761, lane cloud, 2026-09-20)

**Not a KEEP.** It misses PROTOCOL path 4a at the binding 10 bps cost rung by 2.3e-05 of H2
Sharpe, and rule 8's IS-only chooser reaches the family but lands below the live book's OOS
Sharpe. It clears 4a outright at 25 and 50 bps. Recorded here so the Sunday review can see the
exact wording, not as a proposed rules change.

**What it is.** Keep RULES v2 clause 2 (200d +/-3% band, gated weight to cash, gross 0.75,
equal weight over priced names) exactly as live, and change ONLY the trade trigger:

> **Clause 3 (proposed wording, NOT adopted).** Rebalance on day t if and only if at least
> **k = 16** names' band state differs from their state at the last rebalance; otherwise hold and
> let weights drift. Trades execute at the next close. No calendar fallback.

**U56, band c=0.03, gross 0.75, warm-up 260 rows, next-day execution, full sample 2009-2026:**

| cost | book | CAGR | Sharpe | MaxDD | H1 / H2 | turnover | 4a |
|---|---|---|---|---|---|---|---|
| 10 bps | live RULES v2 (weekly) | 8.62% | 1.2010 | -12.05% | 1.2276 / 1.18055 | 1.77x/yr | — |
| 10 bps | event k=16 | **9.06%** | **1.2108** | **-10.75%** | **1.2550** / 1.18052 | **0.69x/yr** | fail (H2 by 2.3e-05) |
| 25 bps | event k=16 | 8.95% | 1.1964 | -10.82% | 1.2406 / 1.1661 | 0.69x/yr | **PASS** |
| 50 bps | event k=16 | 8.76% | 1.1722 | -10.93% | 1.2163 / 1.1418 | 0.69x/yr | **PASS** |

**Why it is interesting.** Against a realised-gross-matched de-gross twin the event book earns a
drawdown credit of **+6.06 pp at 0.69x/yr turnover** where the weekly calendar book earns
**+4.34 pp at 1.77x/yr** — 139.5% of the credit at 39.0% of the turnover, and +8.76 vs +2.45 of
credit per unit of turnover. The quarterly calendar book spends MORE turnover (0.84x/yr) and
earns **-4.51 pp**: same budget, opposite sign.

**Why it is not a KEEP.** 4b is out of reach (CAGR 9.06% against a 10.58% floor). 4a ties at the
protocol's own cost rung. Rule 8 (dials on 2009-2016 only): C_SHARPE does pick k=16 at g=0.75 and
reads OOS 9.94% / 1.2593 / -10.75% against the live book's 9.46% / 1.2766 / -12.05% — better CAGR
and drawdown, worse Sharpe, so 4a OOS fails. 2 of 24 choosers clear 4a OOS; neither picks k=16.

**What would settle it.** k is a single tuned dial on a 5-rung ladder and the record has never
priced it; the neighbours k=8 (+4.92 pp, 1.15x) and k=1 (+5.00 pp, 1.88x) are both worse per unit
of turnover, so k=16 is an interior argmax and needs a resolution check before anyone trades it.
Survivorship: U56 is a current-constituent panel.
