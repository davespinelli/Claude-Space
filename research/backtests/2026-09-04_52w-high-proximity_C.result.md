# Idea 13 — 52w-high-proximity — **KILL** (2026-09-04, lane C)

Script: `research/backtests/2026-09-04_52w-high-proximity_C.py`
Console: `research/backtests/2026-09-04_52w-high-proximity_C.console.txt`
Grid: `research/backtests/2026-09-04_52w-high-proximity_C.grid.csv`
28 points (2 universes × [1 live-v1 + 1 EWall control + 3 signals × n∈{5,10,20,30}]), **all reported**.
10 bps, weekly, next-day execution. 52-week window fixed at 252d (George & Hwang's own definition, not tuned).

**Harness check:** reproduces idea 2's published KEEP row to the decimal — `u56/COMP-n20` = 12.7% / 1.093 / -18.3%,
halves 1.088/1.103 — and idea 10's `B136/EWall` 4b pass (10.7% / 1.027 / -17.7%, halves 1.146/0.917).

## Verdict

**KILL for ranking on nearness to the 52-week high, on both large-cap universes, on every test the
project has.** Replacing RULES v1's return composite with `P_t / max(P_{t-251..t})` loses to it in
**8 of 8 matched-n pairs** (same names, same days, same 200d/vol20 gate, same 75% gross):
dSharpe **-0.045 … -0.754**, paired daily **t -3.07 … -4.16**, every sign negative, mean **-7.2%/yr**
on universe.json and **-9.9%/yr** on universe_broad.json. The 50/50 BLEND arm loses in 7 of 8
(dSharpe +0.002 in its single exception, at n=30 on universe.json). **0 of 16 PROX/BLEND points pass 4b
anywhere; 0 of 28 points pass 4b on both lists.**

## Why it fails — the signal is negatively informative *inside the gate*

| signal | u56 IC (t) | u56 H1 / H2 | broad IC (t) | broad H1 / H2 |
|---|---|---|---|---|
| COMP (incumbent) | **+0.0427** (+4.16) | +0.038 / +0.048 | **+0.0242** (+3.22) | +0.022 / +0.026 |
| PROX (52w high)  | **-0.0208** (-2.13) | -0.019 / -0.022 | **-0.0252** (-3.34) | -0.023 / -0.027 |
| BLEND            | +0.0083 (+0.90) | +0.006 / +0.010 | -0.0043 (-0.63) | -0.006 / -0.003 |

Weekly rank IC vs the following week's return, eligible names only, 905/914 weeks. PROX's IC is
**negative in both halves of both universes** and significant in three of the four full-sample cells —
this is not a weak signal, it is a mildly contrarian one on this panel.

The mechanism is that **RULES v1's eligibility gate has already spent the signal**: mean PROX of eligible
names is 0.953 vs 0.902 for all names (0.950 / 0.899 on broad), because "above the 200d MA" and "near the
52-week high" are largely the same statement. What is left after the gate is a *level* statistic that
mostly ranks names by how quiet they have been — cross-sectional Spearman(PROX, COMP) is only **+0.192**
(u56) / **+0.324** (broad), so it is a genuinely different key, and the part that differs is the part that
loses. Consistent with that reading, PROX is a **de-risking, not a signal**: vol falls in 8 of 8 pairs and
MaxDD is shallower in 6 of 8, but CAGR falls further every time — the same shape as idea 10's ETF result
(risk fell, return fell more).

**PROX loses to no ranking at all.** Against the unranked EW-all-eligible control it is negative at every
n on both lists (dSharpe -0.900 … +0.004; paired t -4.10 … -1.98), while COMP beats the same control on
return in 8 of 8 (t +0.71 … +2.36). A ranking key that is worse than not ranking is not a horizon choice.

## The a-priori argument for it was wrong on its own terms

Ideas 55/57/4/3/9 all found that in this repo net Sharpe orders by flip rate, so a slower ranking key
should be favoured. A level statistic bounded near 1.0 turns out to be **faster, not slower**: at matched n
on universe.json, turnover is 40.2 / 31.1 / 14.8 / 7.8× per year for PROX vs **17.6 / 13.9 / 9.6 / 7.0×**
for COMP, and flips per ticker per year 4.8 / 7.4 / 7.0 / 5.4 vs 2.1 / 3.2 / 4.4 / 4.7. Names cluster within
a few percent of their highs, so tiny price moves reshuffle the top of the book. The whipsaw prior pointed
at this idea and the measurement points the other way — which is itself the run's most transferable finding.

## Walk-forward (rule 8) rejects it unanimously

Parameters chosen on 2009-2016 only, 2017-2026 read once.
Spearman(IS Sharpe, OOS Sharpe) over the 12 CAND points = **+0.888** (u56) and **+0.930** (broad), so unlike
idea 8 (+0.000) the selection here is well powered — this is a decision the walk-forward *can* make, and it
makes it against PROX every time.

- universe.json: S1 and S2 both pick **COMP-n20** → OOS 14.4% / 1.170 / -18.3%, clears all OOS 4b bars.
- broad: S1 and S2 both pick **COMP-n30** → OOS 11.6% / 0.904 / -20.3% (misses OOS DD by 0.1pp).
- Signal choice audited within each n: COMP wins **7 of 8** cells; the one exception (u56 n=30 → BLEND-n30,
  OOS 11.3% / 1.198 / -15.2%) clears the OOS bars but at 0.9pp less full-sample CAGR than COMP-n30.
- SPY OOS 15.5% / 0.884 / -33.7%; RULES v1 OOS 7.8% / 0.751 / -13.8% (u56), 6.0% / 0.581 / -21.2% (broad).

## Nothing is upgraded

The three 4b passes in the run are all reproductions of already-published rows, not new results:
`u56/COMP-n20` and `u56/COMP-n30` (idea 2's candidate and idea 8's PARK) and `broad/EWall` (idea 10's
`B136/EWall`). Six 4a passes appear on the broad list only, where RULES v1 itself draws down -21.2% — as
idea 9 noted, 4a should be read on universe.json, where **0 of 14 points pass it**.

## Survivorship

Current constituents of both lists, one-directional. It bites this run in a specific direction: names that
spent years far below a 52-week high and then delisted are absent, which flatters a signal that *avoids*
such names — i.e. it flatters PROX — and PROX loses anyway, so the KILL is conservative. The
signal-vs-signal comparisons hold names, days, gate and gross fixed and are much less exposed.

## RULES wording recommended

None. RULES v1's ranking composite is unchanged.

Ideas 79-80 queued.
