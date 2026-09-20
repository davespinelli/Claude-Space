# KEEP-candidate memo (path 4b) — A DRIFT THRESHOLD THAT SPENDS NO IN-SAMPLE STATISTIC (idea 2026, lane C, 2026-09-20)

1. **The book.** The standing VOLTGT construction — hold every priced name in the panel at equal
   weight at `g/N` of NAV, no ranking, no band, no vol filter, names re-spread monthly, 10 bps,
   next-day execution, never levered — but the exposure scalar `g_t = min(1, 0.16 / sigma20)` is
   re-read only when the book's held gross has drifted from it by more than **a tenth of the
   scalar itself**, `h_t = 0.10 * g_t`, rather than by idea 1799's constant `h = 0.12`.
2. **Why this is not another tuned rung.** `f = 0.10` and `t = 0.16` were PRE-STATED in the
   script's docstring before the run (`t` inherited from the standing VOLTGT memo) and never
   adjusted. The book therefore reaches its cell with **zero in-sample statistics spent** — it
   needs no chooser, and idea 1799's memo point 7 (the IS chooser walks to the laziest rung of
   whatever ladder it is given; 18 of 24 picks on the top two rungs) cannot bite.
3. **Path 4b, FULL, U56 (monthly re-spread):** 15.81% / 1.2470 / -19.12%, halves 1.2937 / 1.2055,
   vs SPY 15.12% / 0.8843 / -33.72%. All five legs clear: H1 +0.337, H2 +0.381, OOS +0.419,
   DD +1.11 pp, CAGR +5.23 pp.
4. **Path 4b, OOS (rule 8, 2017-2026 read once), U56:** **16.55% / 1.2928 / -19.12%** vs SPY
   15.26% / 0.8737 / -33.72% and live RULES v2 9.46% / 1.2766 / -12.05%. It also clears 4b FULL
   and OOS on B136 (16.10% / 1.2621 / -17.00% OOS) and on the weekly arm of both panels — **4 of 4
   large-panel arms**, against the incumbent constant-`h` family's best legal IS-only chooser at
   3 of 6 arms.
5. **It clears 0 / 10 / 25 / 50 bps** on U56-monthly and on both B136 arms (U56-weekly fails at
   50 bps only, on the DD leg by 0.28 pp), at **1.42 turns/yr** and ~10 refreshes/yr against live
   RULES v2's 1.77.
6. **What it fixes, measured not asserted.** Idea 2022 showed the incumbent constant's advantage
   over a turnover-matched calendar refresh is a 24-day 2020 episode. That replicates here
   (+0.0798 full -> **-0.0050** crash-excised, 0 of 4 arms positive) and is specific to the
   constant: the fraction rule reads **+0.0648 -> +0.0377, positive on 4 of 4 arms**. Scaling the
   threshold to the scalar in force survives deleting the episode.
7. **Robustness.** At `t = 0.16` the fraction ladder clears 4b on 24 of 28 (rung x arm) cells
   (`f` from 0.02 to 0.30; only `f = 0.5` breaks), and at `f = 0.10` on 4 of 4 arms at
   `t in {0.10, 0.12, 0.16}`. The asymmetric sibling `h_up = f*g_t, h_dn = f*g_t/4` is broader
   still (27 of 28) and wins OOS MaxDD by +0.61 pp for -0.16 pp of CAGR; it is the natural
   fallback if the Sunday review wants the drawdown leg widened.
8. **It does NOT clear path 4a** (0 of 6 arms, every family): its drawdown is deeper than the live
   book's -12.05%. 4a is the wrong bar here, exactly as PROTOCOL 4b (added 2026-09-04) says.
9. **Caveats, stated.** U56 / B136 are CURRENT constituents (survivorship; levels optimistic,
   the threshold contrast first-order immune, pass counts not). **SMALL665 clears 4b 0 of 6 arms**,
   on four legs at once. No standard errors are published here — idea 2042 owns the 4b-leg SE
   question and idea 2022 found the drift-vs-calendar sweep resolvable at only 61 of 263 cells, so
   **do not size on the +0.0377 edge**; the 4b legs themselves are what this memo rests on. The
   sigma convention is fixed at (L=20, d=0); idea 1771 owns that surface.
10. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, scan.py, bot.py and
    baseline.py are NOT modified by this run):

    > **2. Sizing.** Hold every instrument in the universe that has a price that day at `g/N` of
    > NAV, where `N` is the count of priced instruments. Let `g_t = min(1, 0.16 / sigma_20)`,
    > `sigma_20` being the annualised 20-day realised volatility of the equal-weight, unlevered
    > universe portfolio (`sqrt(252) *` the 20-day standard deviation of its daily returns,
    > computed through yesterday's close). **Re-read `g` and reset the book's total exposure to it
    > on any day on which the book's actual total exposure differs from `g_t` by more than
    > `0.10 * g_t` — a tenth of the scalar in force, not a fixed fraction of NAV; on all other days
    > leave the exposure alone.** The equal-weight re-spread of the names runs monthly. Weight not
    > deployed sits in CASH, is never re-spread across the held names, and `g` never exceeds 1.
    > No ranking, no momentum screen, no per-name volatility filter.

**Status: KEEP-candidate, path 4b, awaiting Sunday review.** It is the same family as the standing
2026-09-20 candidate with one dimensional correction, it reaches its cell without a chooser, and
it is the first cell in this family whose advantage over a turnover-matched calendar survives
excising Feb-Mar 2020. Evidence: `research/backtests/2026-09-20_ladder-free-drift-threshold_C.py`
(gates 9/9: calendar diagonal == `engine.backtest` at 0.000e+00, every zero rung == `R = D` at
0.000e+00 on 90 of 90 cells, idea 1799's KEEP cell reproduced to 4.042e-07, the standing VOLTGT
memo to 4.605e-05), `.result.md`, `.grid.csv.gz` (1,840 cells x 4 cost rungs published).
