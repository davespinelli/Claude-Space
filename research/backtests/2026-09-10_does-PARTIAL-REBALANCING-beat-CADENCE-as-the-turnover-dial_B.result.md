# Idea 412 — does PARTIAL REBALANCING beat CADENCE as the turnover dial? (lane B, 2026-09-10)

**VERDICT: SPLIT — lambda wins the comparison and loses the job.** At matched realised
turnover partial rebalancing IS the better dial (8 of 8 readable cells at every rung, and the
sign holds out of sample), but it cannot REACH the turnover levels the question is asked at,
and on the live u56/V2 cell it is not a turnover dial at all. The record should keep CADENCE
as its turnover instrument. No KEEP, no promotion, no RULES change; RULES.md / PROTOCOL.md /
scan.py / bot.py / baseline.py untouched.

639 simulations (3 panels x 3 books x [8 cadence levels, every phase = 63 sims] + DAILY +
7 lambda levels) read at 5 cost rungs = **3,195 arm-rows, all reported**. Exactly 2 tuned
parameters: cadence k and lambda. Weekly grid, t+1, IS <= 2016-12-31, OOS 2017-01-01.. read once.

## Gates — all five at 0.000e+00 on all three panels
| gate | result |
|---|---|
| G1 local simulator vs `engine.backtest` at D/W/M/Q, returns AND turnover | **0.000e+00** |
| G2 rung identity `r(c) = r(0) - turnover*c/1e4` | **0.000e+00** |
| G3 the V2 book vs `baseline.rules_v2_weights` | **0.000e+00** (bitwise) |
| G4 cadence k=1 mask vs engine's own `'W'` mask | 0 differing days |
| G5 `smooth(W, 1.0)` is W (the dial's off position is off) | **0.000e+00** |

## What is confirmed
**At matched realised turnover lambda beats cadence, everywhere, at every rung.** Pooled at
10 bps: mean dSharpe **+0.0377**, median +0.0185, lambda ahead at **57 of 72** matched points
and on the mean in **8 of 8** readable cells (broad/V1u +0.094, small/V1u +0.078, small/V2
+0.038, small/TOP20 +0.035, u56/V1u +0.029, broad/TOP20 +0.016, u56/TOP20 +0.010, broad/V2
+0.002). It survives rule 8: mean matched dS **IS +0.0245 -> OOS +0.0431**, sign holds in 6 of
8 cells. The mechanism is measured, not asserted — at **0 bps**, where a turnover dial buys
nothing and can only distort, the distortion per 1x/yr of turnover removed is
**CADENCE -0.0155 vs LAMBDA -0.0007** (median; lambda distorts less in 7 of the 8 cells where
both are computable). Cadence is emphatically **not** the path-neutral dial the queue's
premise assumes: it is the more distorting of the two by roughly 20x.

## What is refuted — the reach, which is the whole job
1. **Cadence cuts turnover by a median 6.38x, lambda by 2.39x, and cadence reaches lower in
   9 of 9 cells.** Lambda's entire ladder on the live V2 book spans only 1.08x (broad) to
   1.39x (small) of turnover.
2. **On u56/V2 — the live panel and the live book, the one cell RULES v2 actually runs in —
   lambda is not a turnover dial at all**: its lowest setting trades **1.784 x/yr against the
   un-smoothed book's 1.775**, i.e. smoothing *raises* turnover. There is no matched-turnover
   comparison to make there, and no level at which it could be adopted.
3. **Mechanism.** Annual turnover = (rebalances that moved anything) x (mean size of one
   rebalance). Cadence removes rebalances; lambda removes size but keeps every rebalance,
   because a smoothed target moves a little in *every* name *every* week:
   | book | native weekly | cadence at k=26 | lambda at 0.06 |
   |---|---|---|---|
   | V2 | 52.3 x 0.042 = 2.20 | 2.0 x 0.312 = **0.63** | 52.3 x 0.036 = **1.89** |
   | TOP20 | 52.3 x 0.246 = 12.85 | 2.0 x 1.009 = **2.03** | 52.3 x 0.102 = **5.32** |
   | V1u | 52.3 x 0.544 = 28.40 | 2.0 x 1.343 = **2.70** | 52.3 x 0.196 = **10.23** |
   So lambda's reach is a function of the book's CONCENTRATION: it works on a 20- or 5-name
   ranked book with large discrete switches and fails on a wide de-grossed equal-weight book.
4. **The win is mostly smaller than the noise in its own comparand.** Only **18 of 72** matched
   points at 10 bps clear the cadence phase band, whose median is **0.1576** of Sharpe (max
   0.5184) — wider than the +0.0185 median gap being argued about.

## PROTOCOL and rule 8
**4a 0 / 0 / 1 / 1 / 7 and 4b 13 / 12 / 12 / 10 / 7 of 639 at 0 / 5 / 10 / 25 / 50 bps; BOTH
0 of 639 at every rung.** Every one of the 12 4b passers at 10 bps is a cadence arm, and
every one is a **single phase** of its level (median 1 of 13 phases): **0 cadence levels pass
4b under MEANPH.** The lone 4a passer is small/V2 k=6 phase 2.

Rule 8 (dial and level chosen on 2009-2016 alone, 2017-2026 read once, 9 cells): the chooser
picks **LAMBDA in 6 of 9** cells and a non-native level in 8 of 9. Out of sample the picks
average **11.34% / 0.8872 / -21.03%** against the native weekly book's 11.04% / 0.8592 /
-22.40% and SPY's 15.41% / 0.8799 / -33.72%; they beat the native book in 4 of 9 cells, RULES
v2 in 2 of 9, SPY in 5 of 9. Head to head at each dial's own IS-best level, lambda beats
cadence IS in 6 of 9 and OOS in 6 of 9 (Spearman(IS gap, OOS gap) +0.450).

## Carried caveats
Survivorship (idea 54) on all three panels — current constituents only; on `small` (485 names,
sub-$2B) SPY is a benchmark column and is dropped from every book. The queue's description of
idea 137's chooser is echoed by this run's own chooser (non-native level 8 of 9, lambda 6 of 9)
but idea 137's committed rows were **not** joined — that is a resemblance, not a reproduction.

## Concurrent independent run — same idea, same day, different design
The cloud lane claimed and ran idea 412 at the same time as this one; neither saw the other's
design or numbers, and it pushed first (`..._cloud.py`, 4,608 arm-rows). **Both agree on
everything that matters and differ on one thing, for a reason that is itself a result.**
Agreed: the cadence phase/offset spread is larger than the effect being measured (here median
band 0.1576 of Sharpe at 10 bps against a median matched gap of +0.0185; there mean SD
0.0117-0.0461, max range 0.3796); lambda is unavailable as a dial on the wide equal-weight book
(here u56/V2 turnover *rises* 1.775 -> 1.784; there the whole ladder moves EWALL turnover by
under 0.001 x/yr on all three panels); nothing is promotable (BOTH 0/639 here at every rung,
4a/4b/BOTH 0/4,608 there). Differed: the **sign** of the matched-turnover gap — the cloud run
reads cadence at a single offset and calls the head-to-head a coin flip (19/36 to cadence,
median +0.0001); this run reads cadence phase-averaged (MEANPH, idea 222) and finds lambda
ahead in 8 of 8 readable cells. That is a design difference, not a contradiction, and both
routes end in the same place: **there is no readable performance edge either way, so the dial
should be chosen on reach and path-preservation, not on Sharpe.**

## Follow-ups
None filed — the concurrent cloud run's 619 (phase-spread census), 620 (lambda's inertness on
low-turnover books) and 621 (the no-dial control on lambda picks) already cover this run's
three. The one angle this run would add is an **ex-ante concentration screen** (effective-N, or
mean weight per held name) for whether lambda can be run as a dial on a given book at all; it
belongs inside 620 rather than as a fourth idea.
