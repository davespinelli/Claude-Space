# KEEP-candidate memo (path 4b) — THE BAND BOOK AT GROSS 1.00, certified CADENCE-ROBUST and CHOOSER-REACHABLE by idea 1753 (lane cloud, 2026-09-20)

1. **The book.** Hold every priced instrument in the universe whose 200-day band state is IN at
   `1.00/N` of NAV (`N` = instruments priced that day); gated-out weight sits in CASH and is never
   re-spread. Band state: IN above `MA200*(1+0.03)`, OUT below `MA200*(1-0.03)`, previous state in
   between, OUT before 200 closes exist. This is the LIVE RULES v2 clause-2 device with gross
   raised from 0.75 to **1.00** — no new device, no ranking, no vol filter. Next-day execution,
   10 bps. Gated identical to `baseline.rules_v2_weights(px, 0.03, 1.00)` at 0.000e+00 (G0).
2. **Path 4b, FULL, U56, weekly, 10 bps:** 11.53% / 1.2008 / −15.91%, halves 1.2282 / 1.1798, vs
   SPY 15.12% / 0.8843 / −33.72% (halves 0.9570 / 0.8249). All five 4b legs clear; margins
   L1 +0.2711, L2 +0.3549, L3 +0.4023, DD +4.32 pp, CAGR +0.95 pp.
3. **Path 4b, OOS (rule 8, 2017-2026 read once), U56, weekly:** 12.67% / 1.2759 / −15.91% vs SPY
   15.26% / 0.8737 / −33.72% and live RULES v2 9.46% / 1.2766 / −12.05%. 4b OOS PASS.
4. **What idea 1753 adds — the pass is a CADENCE WINDOW, not a weekly artefact.** On the ladder
   D / W / 2W / M / Q (phase at the committed last-trading-day anchor), **4 of 5 rungs clear all
   five legs**: D 12.45%/1.2873/−14.77% OOS, W 12.67%/1.2759/−15.91%, 2W-a 13.10%/1.3096/−15.99%,
   M 12.82%/1.2251/−18.81%. Only **Q** fails, on the DD cap alone (−26.07% against a −20.23% cap,
   L4_DD −5.84 pp) while still clearing the CAGR floor by +0.07 pp. Idea 1741's sign reversal at Q
   is therefore a DRAWDOWN reversal, and it does not reach the rungs a desk would trade.
5. **Cost-robust inside the window.** Over 0 / 10 / 25 / 50 bps, 19 of 24 U56 g=1.00 cells pass;
   2W and M clear all four rungs, D and W die only at **50 bps** and only on the CAGR floor.
6. **Rule 8 on the cadence dial: the pass is REACHABLE.** All three legal IS-only choosers
   (IS Sharpe / IS Calmar / IS 4b-leg count, computed on `r.loc[:2016-12-31]`) land on **M** on U56
   at g=1.00 — inside the passing set — and all three clear 4b OOS. Cost of choosing against the
   OOS oracle (2W-a, 1.3096): **−0.085 of OOS Sharpe**. This is the first cadence dial in the
   record whose IS argmax reaches a 4b passer; the VOLTGT016 candidate reached 0 of 3 (idea 1771).
7. **It does NOT clear path 4a — 0 of 144 cells, on any panel.** Its H2 sits 0.0007 below the live
   book's (1.1798 vs 1.1805) and its drawdown is 3.9 pp deeper than the live −12.05%. 4a is the
   wrong bar here, which is what rule 4b was added on 2026-09-04 to handle.
8. **Caveats, stated, and they are the binding half of this memo.** (a) The window is a
   **gross-1.00** object: at gross 0.75, 0 of 24 cells pass on any panel at any cadence, every one
   on the CAGR floor — consistent with idea 1757's finding that the floor is a realised-gross bar.
   (b) It is a **U56** object: on B136 only 2W-a clears all five legs and the IS choosers pick
   W/M, which fail OOS (0 of 6); on SMALL665, 0 of 24, failing 4–5 legs at every rung.
   (c) U56 / B136 are CURRENT constituents and SMALL a current sub-$2B screen, so every CAGR and
   drawdown LEVEL is optimistic; the cadence contrasts are same-tape and first-order immune, the
   pass counts are not. (d) Running at gross 1.00 means no cash buffer when the band is fully IN.
9. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, PROTOCOL.md, scan.py, bot.py
   and baseline.py are NOT modified by this run):

   > **2. Sizing.** On the last trading day of each week (a two-week or month-end cadence is
   > equally certified; a QUARTERLY cadence is not and must not be used), hold every instrument in
   > the universe that has a price that day and whose 200-day band state is IN at `1.00/N` of NAV,
   > where `N` is the count of priced instruments. Band state is IN when the close exceeds
   > `MA200 x 1.03`, OUT when it falls below `MA200 x 0.97`, otherwise unchanged, and OUT until 200
   > closes exist. Weight not deployed sits in CASH; it is never re-spread across the held names,
   > and gross never exceeds 1. No ranking, no momentum screen, no per-name volatility filter.

10. **Status: KEEP-candidate, path 4b, awaiting Sunday review.** NOT proposed as a live rules
    change by this run. Evidence: `research/backtests/2026-09-20_band-g100-cadence-artefact_cloud.py`
    (`_grid.csv`, 144 cells, gates 9/9; G3 reproduces idea 1761's 12 committed CAL cells at
    max |Δ| 8.882e-16).
