# Memo — idea 2399 (lane C, run 43, 2026-09-23): equity-curve de-grossing gate on CAP2
**Status: 4b passer on BOTH panels at the live gross and 10 bps, FILED AND NOT RECOMMENDED.** It is
strictly dominated by the standing candidate (CAP2) on CAGR and Sharpe and pays +0.59x / +0.55x of
annual turnover for drawdown headroom the candidate already had.

**Exact RULES wording, if a Sunday review ever wanted it (clause to insert after RULES v2 clause 3):**
> 3b. **EQUITY-CURVE DE-GROSSING GATE.** At each weekly rebalance, let `E_t` be the book's own
> cumulative net-of-nothing equity level as of the previous close and `MA100_t` the mean of that same
> equity series over the 100 trading days ending at the previous close. Set `s_t = 1.00` if
> `E_t >= MA100_t`, else `s_t = 0.75`. Multiply every risk weight from clause 3 by `s_t`; the whole
> residual `1 - sum_i w_i` goes to SHY. `s_t` is never above 1.00, so the book never levers.

**The numbers (10 bps, weekly, t+1, band 0.03, 2% name cap, gross 0.75, SHY sweep phi = 1.00):**
U56 **10.81% / 1.2625 / -12.91%**, halves 1.2555 / 1.2741, OOS 12.25% / 1.3669, turnover **4.09x/yr**,
against CAP2's 11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, 3.51x. B136 **10.63% / 1.1161 /
-15.12%**, halves 1.2235 / 1.0172, OOS 10.85% / 1.1346, 5.23x, against CAP2's 11.82% / 1.1180 /
-17.10%, OOS 11.65% / 1.0936, 4.68x. SPY 15.23% / 0.8897 / -33.72% (U56 window).

**Why NOT recommended, in one line each.** (1) It spends the margin the book cannot spare: `L_CAGR`
headroom falls from +0.96 pp / +1.24 pp to **+0.15 pp / +0.04 pp**, a hairline, to buy 1.90 pp / 1.98 pp
of `L_DD` headroom on a book that already had +5.42 pp / +3.13 pp spare. (2) Turnover — the ONLY stated
blocker on CAP2's adoption (idea 2391) — goes UP, not down. (3) Rule 8 does not endorse it: 49 of 64
IS-only picks take `d = 1.00`, i.e. NO gate, and only 14 of 64 beat the anchor's OOS Sharpe.
(4) Sharpe falls on both panels, so it fails 4a as well as failing to improve 4b.

_Research, not investment advice. Survivorship (rule 9): U56 / B136 are current constituents held from
2008; `L_CAGR` is the contaminated leg. Script:
`research/backtests/2026-09-23_equity-curve-de-grossing-gate-on-the-capped-candidate_C.py`._
