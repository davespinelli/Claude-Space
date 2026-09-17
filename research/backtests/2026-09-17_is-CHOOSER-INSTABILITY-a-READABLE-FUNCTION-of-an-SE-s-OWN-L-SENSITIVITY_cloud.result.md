# Idea 1220 — is CHOOSER INSTABILITY a READABLE FUNCTION of an SE's OWN L-SENSITIVITY?

**Answer: NO.** The relation is positive in sample (Spearman 0.5727–0.6411 over the L-dependent
choosers) and **collapses to 0.0427–0.1966 when the same two quantities are measured out of
sample**; it is undefined at 3 of 9 cells because no chooser moves at all on the short L ladder;
and the "expensive" quantity it is fitted against takes exactly **two** values over all 72 cells.
**A cheaper statistic does work, and it is not L-sensitivity: the chooser's MOVE COUNT predicts
mean OOS Sharpe at Spearman −0.9429.** Verdict **KILL (capital)** — no new book, no candidate,
no RULES change. Run 2026-09-17, cloud lane, idea 2 of 2.

Script: `2026-09-17_is-CHOOSER-INSTABILITY-a-READABLE-FUNCTION-of-an-SE-s-OWN-L-SENSITIVITY_cloud.py`.
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

## The two dials and no more (PROTOCOL rule 4; the queue names both)

`CHOOSER SET` {K_SE3, K_SE3_NAIVE, K_ALL} × `L LADDER` {L_SHORT {21,42,63}, L_WIDE {21,42,63,126,252,504},
L_LONG {126,252,504}} = **9 cells, every one published** (`.cells.csv`).
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR (N, cadence)
{(20,W), (12,W), (20,M), (10,M)}; the N ladder {5,10,12,20,30,40,60} (k = 7, inside d2's domain);
the six L rungs; the 4a and 4b legs. The move bar is fixed at |gap| > 2·SE and is **not** a dial.
10 bps, t+1 execution, 260-row warm-up, IS 2009–2016, OOS 2017–2026 read **once**.
432 decisions over 42 books; all three SE bases are **paired** (idea 1042's honest basis).

## (0) The degeneracy gate and the measured Monte-Carlo floor

SE_IID, C_NAIVE, C_CALMAR and C_ANCHOR do not read L, so their *population* L-sensitivity ratio is
1 and their distinct-pick count is 1. Including them manufactures a positive correlation out of a
definition, so **every rho below is reported twice** — over the whole set and over the L-dependent
choosers only.

SE_IID is also the run's **noise floor, and its realised ratio is not 1**: it is re-bootstrapped
independently at each L rung, so what it reads above 1 is pure Monte-Carlo dispersion.
**Measured: median 1.0868, max 1.1606 at BOOT = 400.** SE_BLOCK's excess over 1 is 4.36× the
floor's own excess and SE_FOLD's is 9.15×, so both clear it — but **a ratio below ≈1.16 is not
evidence that a basis reads L at all**, and 1212's x1.24 for the block SE sits close to that floor.

## (1) 1212's headline does NOT reproduce on this construction

Median IS SE of the Sharpe gap by basis: **SE_BLOCK 0.1224 < SE_IID 0.1354 < SE_FOLD 0.1424.**
1212 reported the fold SE as the **smallest** of the three (0.0132 vs 0.0209 / 0.0292); here it is
the **largest**. The object differs — this run's gap is the paired IS-argmax-minus-anchor Sharpe
difference on an N ladder, 1212's was its own decision set — but it is the same statistic by name,
and the ordering the queue entry rests on is construction-dependent. **The L-sensitivity ordering
does reproduce: SE_FOLD 1.7944 > SE_BLOCK 1.3787 > SE_IID 1.0868 (floor).**

## (2) The 9 cells

| chooser set | L ladder | rho (all) | rho (L-dep only) | rho OOS (all) | rho OOS (L-dep) | mean distinct picks | mean OOS Sharpe | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|
| K_SE3 | L_SHORT | — | — | — | — | 1.0000 | 0.8935 | 9 | 0 |
| K_SE3 | L_WIDE | 0.5769 | **0.6411** | 0.2663 | **0.0427** | 1.1389 | 0.8891 | 18 | 0 |
| K_SE3 | L_LONG | 0.5414 | **0.5727** | 0.3462 | **0.1966** | 1.1389 | 0.8847 | 9 | 0 |
| K_SE3_NAIVE | L_SHORT | — | — | — | — | 1.0000 | 0.8846 | 9 | 0 |
| K_SE3_NAIVE | L_WIDE | 0.5222 | 0.6411 | 0.3298 | 0.0427 | 1.1042 | 0.8813 | 18 | 0 |
| K_SE3_NAIVE | L_LONG | 0.5002 | 0.5727 | 0.3793 | 0.1966 | 1.1042 | 0.8780 | 9 | 0 |
| K_ALL | L_SHORT | — | — | — | — | 1.0000 | 0.8845 | 12 | 0 |
| K_ALL | L_WIDE | 0.4697 | 0.6411 | 0.3636 | 0.0427 | 1.0694 | 0.8823 | 24 | 0 |
| K_ALL | L_LONG | 0.4575 | 0.5727 | 0.3909 | 0.1966 | 1.0694 | 0.8801 | 12 | 0 |

Three readings, in order of how much they cost the queue's hypothesis:

1. **The relation does not hold out of sample.** In sample rho over the L-dependent choosers is
   0.5727–0.6411; re-measuring **both** quantities on 2017–2026 gives **0.0427 (L_WIDE) and
   0.1966 (L_LONG)**. The queue asked explicitly whether it holds OOS. It does not.
2. **It is unresolvable at 3 of 9 cells.** On L_SHORT no chooser changes its pick at any panel or
   anchor, so distinct_picks is constant at 1, has zero variance, and rho is undefined. The
   L-sensitivity curve is only even *measurable* against instability once L reaches 126+.
3. **The expensive quantity is binary.** `distinct_picks` takes the values **{1, 2}** over all 72
   (panel, anchor, chooser) cells. Every rho in the table is a rank correlation fitted on two
   levels, so the in-sample 0.64 is close to the most a monotone statistic could score here and
   carries far less information than a continuous 0.64 would.

## (3) The cheap statistic that does work — and it is not L-sensitivity

| chooser | moves (of 72) | mean OOS Sharpe |
|---|---|---|
| C_ANCHOR (do nothing) | 0 | **0.9194** |
| SE_FOLD | 6 | 0.9064 |
| SE_IID | 12 | 0.8806 |
| SE_BLOCK | 13 | 0.8804 |
| C_CALMAR | 60 | 0.8493 |
| C_NAIVE (IS argmax) | 66 | 0.8578 |

**Spearman(move count, mean OOS Sharpe) = −0.9429 over the six choosers**, with one inversion
(C_NAIVE above C_CALMAR). Move count costs one in-sample pass, exactly like the L-sensitivity
curve the queue proposed, and it ranks the choosers by the thing that matters. The reading is
1221's, arrived at from a different direction: **on this tape a chooser's OOS Sharpe is very
nearly a decreasing function of how often it declines to leave the anchor**, and SE_FOLD scores
well not because its SE is better calibrated but because it is the basis that moves least.

## (4) Rule 8 and both KEEP paths

Benchmarks: U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684;
U56 RULES v2 LIVE 8.60% / 1.1980 / −12.05%, OOS 1.2714. B136 SPY 15.16% / 0.8861, OOS 0.8767;
B136 LIVE 7.98% / 1.0993, OOS 1.1059. SMALL SPY 14.06% / 0.8581, OOS 0.8767; SMALL LIVE
4.30% / 0.6637 / −13.89%, OOS 0.5600.

**0 of 432 decisions clear 4a. 24 of 432 clear 4b — and they are ONE distinct book**, the
U56 / N=20 / W / g=0.75 anchor: **14.18% / 1.1410 / −19.39%, halves 1.2223 / 1.0883,
OOS 15.55% / 1.1595**. That is the standing 2026-09-04 incumbent, reached by C_ANCHOR, SE_IID,
SE_BLOCK and SE_FOLD at every L rung on that family. **CONFIRMATORY, NOT GENERATIVE. No new
candidate, no memo, nothing enacted.** Applying 1211's decision-row correction the count is
24 rows → **1 book**, an inflation factor of 24.

## Caveats

Survivorship: `universe.json` / `universe_broad.json` are current constituents; the small panel is
the current output of a sub-$2B screen, 715 rows in `small_meta.csv` of which 52 drop for
`max_1d_move ≥ 1.0`, leaving 663 tradable — the label `SMALL439` does not denote this pool
(idea 1074 still open). The 2·SE bar is fixed, not walked, so these are pick counts at one bar;
a different bar moves every move count and therefore section (3)'s ordering. The OOS L-sensitivity
is measured on a 9.7-year window against the IS 8-year one, so the two are not length-matched —
the collapse from 0.64 to 0.04 is larger than any length effect could account for, but the two
numbers are not directly comparable to four decimals.

## What this closes and what it opens

Closes 1220: **L-sensitivity is not a usable stand-in for a walk-forward.** Opens: move count is,
at rho −0.9429 on six choosers — worth re-running against a walked bar and a larger chooser family
before anyone relies on it, since six points and one inversion is thin evidence for a rule.
