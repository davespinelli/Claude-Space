# KEEP-CANDIDATE MEMO — **ZERO-CHOOSER VOLTGT-DRIFT** (idea 2071, lane cloud, 2026-09-21). **Path 4b only.**

1. **WHAT.** The standing candidate's book with the vol TARGET set by the panel's own trailing
   volatility instead of a number off an IS ladder: `t_t = 1.00 x` the EXPANDING (point-in-time)
   median of the panel's 20-day realised sigma (`MEDMULT m = 1.00`), everything else inherited
   (`h = 0.08`, trade W, 10 bps, t+1, gross ≤ 1.00). **No 2009-2016 statistic is read anywhere** —
   the rule is complete on day one. `m = 1.00` was PRE-STATED in the script docstring before any
   compute, as the only neutral rung of its family (target = the median sigma, multiple of one).
2. **FULL SAMPLE, B136, 10 bps, t+1.** CAGR **15.98%**, Sharpe **1.2464**, MaxDD **-16.79%**,
   halves **1.3297 / 1.1569**. Turnover 2.25/yr, 11.4 refreshes/yr, mean gross 0.900.
3. **VS LIVE RULES v2** (7.96% / 1.0972 / -12.24%, halves 1.2296 / 0.9669): both Sharpe halves
   clear, **MaxDD does not** (-16.79% vs -12.24%). **PATH 4a FAILS** — at every cost rung and on
   every panel. This is a 4b-only candidate and must not be quoted otherwise.
4. **VS SPY** (15.12% / 0.8844 / -33.72%). **PATH 4b PASSES**, five legs: H1 **+0.3726**,
   H2 **+0.3320**, OOS **+0.4108**, MaxDD vs `0.60 x SPY` **+3.44 pp**, CAGR vs `0.70 x SPY`
   **+5.39 pp**. On U56 the same rung reads 14.94% / 1.2557 / -16.43% and passes on all five.
5. **RULE 8 (OOS 2017-2026, read ONCE).** No chooser is needed, so the pre-stated rung IS the OOS
   book: **14.80% / 1.2845 / -14.68%**, OOS legs L3 **+0.4108**, L4 **+5.55 pp**, L5 **+4.12 pp**,
   against SPY OOS 15.26% / 0.8737 / -33.72% and live RULES v2 OOS 7.85% / 1.1017 / -12.24%.
   Clears 4b OOS; fails 4a OOS on drawdown. The companion `SELFQ q = 0.50` (trailing 3-year
   MEDIAN sigma) passes identically: full 14.90% / 1.2180 / -16.24%, OOS 13.86% / 1.2601 / -15.57%.
6. **COSTS.** 4b holds at **0 / 10 / 25 / 50 bps on both large panels, 2 of 2 arms at every rung**
   (Sharpe 1.2644 / 1.2464 / 1.2192 / 1.1740 on B136). The low turnover (2.25/yr against the
   standing cell's 3.13) is why: the self-scaling target refreshes 11.4 times a year, not 21.
7. **THE TRADE THIS MAKES, STATED PLAINLY.** It does not dominate the standing IS-chosen cell — it
   **moves the thin leg**. Standing cell: CAGR margin +1.92 pp (idea 2060: SE 1.10-1.46 pp, does
   NOT resolve), DD margin +8.42 pp. This rule: CAGR margin **+5.39 pp**, DD margin **+3.44 pp**.
   Idea 2060 also found the DD leg the worst-resolved of the five (it fails in 0.10-0.28 of paired
   block-bootstrap draws), so the new thin leg is the less reliable one. **This candidate has not
   been bootstrapped**; until it is, its 4b pass carries no error bar and must not be compared to
   the standing cell's on precision.
8. **CAVEATS.** (a) 4 of 9 pre-stated zero-IS arms pass (2 families x 2 large panels; CASHSHARE
   fails 0/3 and SMALL665 fails 3/3) — a multiple-comparison caveat applies to the FAMILY choice
   even though no dial was tuned. (b) SURVIVORSHIP: B136 and U56 are CURRENT-constituent lists, so
   levels are optimistic and both 4b bars are easier than on a point-in-time panel; idea 2064's
   adversarial-deletion reach has NOT been re-measured for this rung. (c) The family clears 4b
   **0 of 20 cells on SMALL665 at every cost rung** — an eighth confirmation that this is a
   large-cap-panel object. (d) Not stress-tested on latency, phase or name deletion.
9. **EXACT RULES WORDING, if adopted at a Sunday review** (replaces clause 4 of the standing memo's
   wording; clauses 2, 3, 5, 6, 7 there are unchanged):

   > **4. Gross scalar (NO CHOSEN TARGET).** Let `sigma_t` be the annualised 20-day realised
   > volatility of the UNLEVERED equal-weight panel portfolio through close `t`, and let `M_t` be
   > the median of `sigma_1..sigma_t` (an EXPANDING median: every value is known at `t`; it is
   > undefined until 126 observations of `sigma` exist). The TARGET gross is
   > `g_t = min(M_t / sigma_t, 1.00)`; if `sigma_t` or `M_t` is unavailable, `g_t = 0`.

   Equivalently: **hold full gross when the panel is at its own typical volatility, and de-gross in
   proportion when it is above it.** There is no number to choose and no window to fit.
10. **STATUS.** KEEP-candidate on path **4b only**, awaiting Sunday review. Its distinguishing claim
    is not a better Sharpe — it is that **the 4b pass survives removing the last chooser from the
    rule**. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched by idea 2071.
    Evidence: `research/backtests/2026-09-21_target-without-is-window_cloud.py` / `.result.md` /
    `.grid.csv` / `.prestated.csv` / `.walkforward.csv` / `.gates.csv` / `.log.txt` (gates 6/6;
    the standing cell reproduced to max abs d 3.15e-05).
