# Idea 649 — is EVERY published CHOOSER WIN in the record a PHASE WIN?  (lane C, 2026-09-10)

**Verdict: ANSWERED — effectively YES, and the reason is not the one the queue expected. No KEEP.**

1. **Corpus.** 28,002 committed `d = OOS_Sharpe(pick) − OOS_Sharpe(control)` rows from **129 files**
   whose own column names put both sides explicitly in the OOS window (38,150 rows / 150 files
   before that strictness filter; both populations reported, the strict one is the headline).
2. **The record's chooser wins are indistinguishable from noise on FREQUENCY.** Committed win rate
   **36.6%** (52.3% with the 30.0% of rows that are exact ties removed) against a null-ladder win
   rate of **44.2%** (55.7% ties removed) — **excess −3.4 pp**. The record's chooser beats its
   control *less* often than a ladder that cannot carry information.
3. **…and on MAGNITUDE.** Median committed win **+0.0439** vs median null win **+0.0455 (0.97x)**.
   Only **7.7% of committed wins** (2.8% of all rows) clear the null p95 of +0.1773; **0.7%** clear
   the p99. A record-wide 95% bar on this statistic is roughly **+0.18 OOS Sharpe**.
4. **The floor is a CONTROL-LUCK statistic, not a chooser statistic — the load-bearing finding.**
   In the record's own convention (control = the ladder's named DEFAULT rung) the null win rate
   swings **0.231 (u56) → 0.653 (broad136) → 0.785 (small439)** across panels. Drawing the control
   uniformly from the same rungs collapses that spread to **0.398–0.485** with mean **+0.009..+0.015**,
   i.e. to the ~0.5 a null should give. The DEF−SYM gap is **0.25–0.34 win-rate points per panel**,
   larger than any chooser edge the record publishes.
5. **So idea 624's phase win is not about phase.** G6 reproduces it exactly from this file's own
   grid — **+0.1083 (u56)** and **+0.1882 (small439)**, against 624's published +0.108 / +0.188 — and
   PART B3 shows the same magnitude falls out of a ladder whose rungs are seeded jitter or name
   permutations. What 624 measured is where the rung named `W` (and `seed 0`) happened to land in
   the OOS distribution, not what the chooser did.
6. **Three null families, all reported, none selected on** (P1): `PHASE` (6 rungs, target weights
   byte-identical at every rung — G5 max distance **0.000e+00** on all three legs, all panels),
   `JIT` (32 seeded rungs, informationless tie-break jitter on the record's real composite, mean
   JAC 0.055–0.134), `PERM` (32 seeded name-label permutations, mean JAC 0.739–0.954, each day's
   cross-sectional score distribution preserved to **0.000e+00**). Panels u56 / broad136 / small439
   (P2). Ladder length L ∈ {3,4,5,6,8} and cost rungs {0,10,25,50} bps are reported axes.
7. **The floor barely moves with ladder length.** SYM win rate 0.42→0.51 (u56), 0.29→0.48
   (broad136), 0.43→0.44 (small439) from L=3 to L=8; the p95 moves by under 0.07 Sharpe. Longer
   ladders are not what makes a chooser win look big.
8. **Side finding, independently reportable: PROTOCOL 4b admits informationless books.** 4a
   **0/210**, 4b **58/210** at 10 bps — including **21 of 96 PERM arms**, books whose name→score
   link is destroyed by a random permutation. 4b's DD-cap-plus-CAGR-floor shape (ideas 527/531) is
   passed by noise at a 22% rate on this grid.
9. **Book, rule 8, 10 bps, OOS 2017-2026.** u56: PHASE pick 16.85%/1.2780/−18.66%, JIT
   14.84%/1.1497/−19.81%, PERM 11.79%/1.0758/−18.90% vs RULES v2 9.48%/1.2788/−12.05% and SPY
   15.32%/0.8758/−33.72%. broad136: PHASE 12.67%/0.8795/−21.70%, JIT 13.24%/0.9264/−21.58%, PERM
   11.10%/0.9607/−21.19% vs RULES v2 7.98%/1.1185/−12.24% and SPY 15.45%/0.8820/−33.72%. small439:
   PHASE 10.21%/0.6262/−28.31%, JIT 6.72%/0.4493/−31.47%, PERM 4.16%/0.3340/−32.34% vs RULES v2
   3.85%/0.5680/−14.68%. No chooser pick beats RULES v2 on Sharpe except small439/PHASE, whose
   MaxDD is 1.93x v2's; none of these is a book anyone should hold.
10. **Proposed PROTOCOL line (not adopted here — rule 6 reserves that for Sunday review):** *a
    chooser-vs-control claim must publish the control's RANK among the ladder's own OOS values, or
    the same delta against a uniformly-drawn control.* Without it the published number is not a
    measurement of the chooser. **KILL** the class of bare "the pick beat the control" claims.

**Caveats.** SURVIVORSHIP (idea 54): all three panels are current constituents; SMALL439 drops 44
tickers at `max_1d_move ≥ 1.0` and its levels are not investable history — only within-panel
arm-minus-arm contrasts are read from it. PART A prices what the record COMMITTED, at each file's
own warm-up, cost rung and window split; those rows are not re-run here, so the comparison to this
file's floor is approximate and is reported as such. The `PHASE` rung `W` is the engine's calendar
mask (last trading day of the week, never a skipped week) and is therefore not exactly exchangeable
with the five weekday rungs — `FRI` was added so the family contains a clean 5-way exchangeable set.
Idea 534: files, not claims, are the census unit; a control column named something this reader does
not know is missed, not faked. Idea 321: MaxDD is one number off one path. Idea 126: t+1 execution.

Gates: G1 `fast_bt` == `engine.backtest` on returns and turnover, max 6.98e-16 all panels. G2
cost-rung identity vs a live 25 bps engine run, max 6.98e-16. G3 default rung in every ladder. G4 IS
≤ 2016-12-31 / OOS ≥ 2017-01-01 disjoint and exhaustive. G5 nullity measured from target weights.
G6 replication of idea 624. PROTOCOL.md / RULES.md / scan.py / bot.py / baseline.py untouched.
