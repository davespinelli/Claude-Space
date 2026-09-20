# KEEP-CANDIDATE MEMO — VOLTGT-DRIFT on B136 (idea 2034, lane cloud, 2026-09-20). **BOTH paths: 4a AND 4b.**

1. **WHAT.** Equal-weight the broad panel, scale gross by a vol target, and refresh that gross on a
   DRIFT TRIGGER rather than a calendar. Cell: panel B136, `t = 0.10`, `h = 0.08`, trade weekly,
   10 bps, t+1, gross capped at 1.00. Reached by a LEGAL IS-only chooser (argmax min IS 4b-leg
   slack on 2009-2016), not hand-picked; 2017-2026 read exactly once.
2. **FULL SAMPLE (10 bps, t+1).** CAGR **12.51%**, Sharpe **1.2286**, MaxDD **-11.81%**,
   halves **1.3171 / 1.1415**. Turnover 3.13/yr, 19.8 refreshes/yr, mean gross 0.777.
3. **VS LIVE RULES v2.** 7.96% / 1.0972 / -12.24%, halves 1.2296 / 0.9669. **PATH 4a PASSES:**
   Sharpe higher in BOTH halves (+0.0875, +0.1746) and MaxDD 0.43 pp shallower.
4. **VS SPY.** 15.12% / 0.8844 / -33.72%, halves 0.9571 / 0.8249. **PATH 4b PASSES**, all five
   legs positive: H1 +0.3600, H2 +0.3166, OOS +0.4191, MaxDD vs `0.60 x SPY` +8.42 pp, CAGR vs
   `0.70 x SPY` +1.92 pp.
5. **RULE 8 (OOS 2017-2026, read ONCE).** 13.01% / **1.2928** / -11.81%, against SPY 15.26% /
   0.8737 / -33.72% and live RULES v2 7.85% / 1.1017 / -12.24%. Clears 4b OOS and 4a OOS.
6. **COSTS.** 0 bps 1.2603 / 25 bps 1.1812 / 50 bps 1.1020. Both paths hold at 25 bps; at 50 bps
   4b still passes and 4a fails.
7. **CAVEATS.** 1 of 24 picks on one panel at one cadence — a multiple-comparison caveat applies,
   and the CAGR leg's margin is thin (+1.92 pp). SURVIVORSHIP: B136 is a CURRENT-constituent list,
   so the levels are optimistic and both 4b bars are easier than on a point-in-time panel. The
   family clears 4b 0 of N on SMALL665 (confirmed five times).
8. **EVIDENCE.** `research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.py`, rows
   `panel=B136, book_tape=FULL, bar=FULL, target=0.10, T_trade=W, family=DRIFT, h=0.08` of
   `.grid.csv.gz`; pick row 95 of `.walkforward.csv`; gates 11/11 in `.gates.csv`.
9. **EXACT RULES WORDING, if adopted at a Sunday review (replaces clause 2-3 of RULES v2 wholesale):**

   > **2. Panel.** Hold every instrument in `research/universe_broad.json` that is priced that day.
   > **3. Weight.** Each held name gets `G_t / N_t` of NAV, where `N_t` is the number of instruments
   > priced that day and `G_t` is the GROSS SCALAR. Un-deployed weight is CASH; never re-spread.
   > **4. Gross scalar.** Let `sigma_t` be the annualised 20-day realised volatility of the
   > UNLEVERED equal-weight panel portfolio through close `t`. The TARGET gross is
   > `g_t = min(0.10 / sigma_t, 1.00)`; if `sigma_t` is unavailable, `g_t = 0`.
   > **5. Refresh trigger (DRIFT, not calendar).** Carry the gross scalar `G` forward unchanged.
   > At each close `t`, if `|g_t - (current deployed gross)| > 0.08`, set `G = g_t`; otherwise
   > leave `G` unchanged. Gross is never levered above 1.00.
   > **6. Trade.** Rebalance name weights to `G / N` on the weekly rebalance date only; on a
   > non-rebalance day on which the trigger fires, rescale the existing holdings pro rata to the
   > new `G` and trade nothing else. All weights decided at close `t` are executed at close `t+1`.
   > **7. Costs.** 10 bps per unit turnover.

10. **STATUS.** KEEP-candidate on BOTH paths, awaiting Sunday review. Not adopted; RULES.md,
    PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.
