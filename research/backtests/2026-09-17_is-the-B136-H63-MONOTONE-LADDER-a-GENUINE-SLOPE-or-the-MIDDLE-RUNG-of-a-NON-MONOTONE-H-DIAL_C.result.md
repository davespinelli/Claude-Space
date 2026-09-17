# Idea 1093 (lane C, 2026-09-17) — is the B136 H=63 MONOTONE LADDER a GENUINE SLOPE or the MIDDLE RUNG of a NON-MONOTONE H DIAL?

**ANSWERED = SINGLE-RUNG ACCIDENT ON THE H AXIS, BUT NOT SEED NOISE — AND THE SLOPE ITSELF IS
GENERAL. KILL of the queue's "genuine slope over a band of holds"; CORRECTION to 1082's B136 HUMP
(an H=126 fact alone) and to 1086's "monotone is a B136 property" (U56 has one monotone hold too).**

Dials: **N in {5, 8, 10, 12, 15, 20, 25, 30, 40} x H in {21, 42, 52, 63, 76, 90, 126}** = 63 cells
per panel, **126 in total, every one published** for the book and for its own DD-matched null.
Everything else frozen at 936/1064/1071/1082/1086's construction (cap INF, CAND20 legs, max_vol
0.60, gross 0.75, W cadence, 10 bps, LAG 1, 40 seeds, null draws PAIRED across H).

## The pre-declared decision rule, and what it returned

Declared before any number: **HOLD FACT** = H=52 and H=76 (63's immediate neighbours) both
monotone decreasing on B136 **AND** bootstrap P(monotone at H=63) >= 0.50. **SINGLE-RUNG
ACCIDENT** = either fails, the two reported apart. **OUTCOME (c)** = >= 6 of 7 rungs monotone,
which would make 1086's "H=63 alone" a 3-point artefact.

| pre-declared hypothesis | verdict | reading |
|---|---|---|
| H_REP — B136 H=63 reproduces 1086 AND is monotone | **FAIL** (on the gate only) | monotone **YES**; G5c |d| = 4.07e-02 pp, but **all of it is U56** — B136 reproduces to **4.2e-05 pp** |
| H_NEIGHBOUR — H=52 and H=76 both monotone on B136 | **FAIL** | H=52 **humps**, H=76 **humps** |
| H_BAND — >= 4 of 7 B136 holds monotone | **FAIL** | **1 of 7** (H=63) |
| H_LUCK — bootstrap P(monotone at B136 H=63) >= 0.50 | **PASS** | **0.945** over 2,000 resamples |
| H_ARGMAX_MONO — B136 argmax n non-decreasing in H | **PASS** | 5, 5, 5, 5, 5, 5, **10** |
| H_U56_NONE — U56 has no monotone hold | **FAIL** | **1 of 7** (H=76) |
| H_TURN — turnover falls strictly as H lengthens, every (panel, N) | **PASS** | B136 spread 6.47x/yr |
| H_WF — >= 1 rule-8 pick clears 4b OOS | **PASS** | 1 of 8 |
| H_4A — no cell clears 4a | **PASS** | **0 of 126** |

**Verdict off the pre-declared rules: OUTCOME (b), SINGLE-RUNG ACCIDENT.** But the two failure
modes the declaration kept apart give opposite readings, and both are worth carrying:

* **The H axis is rough at this resolution.** Neither neighbour of 63 is monotone. Monotonicity
  does not survive a 17% change in the hold in either direction.
* **The H=63 ladder is NOT an unresolved object.** P(monotone) = **0.945** with **0.057** expected
  violations, against 1.40–2.01 expected violations at every other B136 hold. 1086 measured a real
  property of that exact cell; it simply does not extend one rung either way.

## The correction that matters more than the verdict

**The DECLINE is general; only EXACT MONOTONICITY is knife-edge.** On B136 the argmax sits at
**n=5 at 6 of the 7 holds** (bootstrap P(argmax=5) = **1.000** at all six, 90% argmax set `{5}`),
and the end-to-end drop EDGE(5) − EDGE(40) is **decisive at every hold**: +7.28 / +10.27 / +6.97 /
**+10.87** / +9.10 / +6.00 / +3.86 pp at **14.7 / 19.5 / 14.5 / 24.1 / 19.4 / 13.4 / 7.8 SE**.
1082's published B136 **HUMP (peak n=10)** is an **H=126 fact and nothing else** — at the other six
holds the peak is at the ladder's left end. The SLOPE premise 1082 killed was killed on one hold.

**And "monotone is a B136 property" does not survive resolution either.** U56 is monotone at
**H=76** (1 of 7), a hold 1086's three-point ladder could not see. Two panels, one monotone hold
each, at **different** holds — strict monotonicity over a 9-rung ladder is a knife-edge statistic,
not a panel or a hold property. The record should read a "monotone ladder" claim as a statement
about one cell unless a band of holds is shown.

**1086's "H=63 is not between 21 and 126" fails on B136 at finer resolution.** The argmax path is
5, 5, 5, 5, 5, 5, 10 — non-decreasing, a smooth dial (H_ARGMAX_MONO PASS). The apparent
non-monotonicity was the three-point ladder, at least on the argmax axis and on this panel.

## The EDGE ladder at every hold (pp, 40 seeds, REBUILT DD-match)

```
B136        n=5      8      10      12      15      20      25      30      40   argmax  MONO
   H= 21  + 8.074 +4.842 +5.544 +4.597 +3.072 +4.398 +3.370 +1.594 +0.799    5     no
   H= 42  +10.974 +5.154 +5.639 +5.573 +4.692 +4.022 +2.130 +1.059 +0.707    5     no
   H= 52  + 7.951 +4.947 +4.574 +4.221 +4.219 +2.269 +1.572 +2.466 +0.981    5     no
   H= 63  +11.269 +8.822 +7.663 +5.182 +4.473 +3.352 +2.133 +1.439 +0.398    5    YES
   H= 76  + 9.945 +6.206 +4.389 +5.169 +3.944 +3.241 +3.220 +1.983 +0.843    5     no
   H= 90  + 7.217 +5.375 +3.277 +1.989 +2.651 +2.512 +2.325 +2.183 +1.218    5     no
   H=126  + 5.717 +5.245 +8.324 +6.520 +6.834 +4.932 +4.269 +2.811 +1.853   10     no
U56
   H= 21  + 5.930 +6.163 +7.319 +7.650 +5.232 +3.892 +1.779 +1.734 +1.332   12     no
   H= 42  + 8.982 +7.545 +5.573 +3.624 +2.953 +2.052 +1.792 +2.080 +0.564    5     no
   H= 52  + 6.780 +6.463 +5.534 +4.216 +2.368 +3.346 +2.188 +0.879 +0.723    5     no
   H= 63  + 6.599 +8.029 +6.777 +5.362 +4.616 +2.116 +2.263 +2.066 +0.144    8     no
   H= 76  + 7.548 +4.973 +4.327 +4.001 +3.706 +3.279 +3.091 +1.873 +0.535    5    YES
   H= 90  + 7.044 +5.153 +6.656 +5.759 +5.231 +2.928 +1.966 +1.780 +1.253    5     no
   H=126  + 5.955 +5.295 +6.164 +6.784 +5.209 +5.117 +2.949 +1.536 +0.410   12     no
seed SE at H=63:  B136 0.43/0.27/0.32/0.28/0.25/0.17/0.18/0.14/0.15
```

Bootstrap P(monotone), 2,000 resamples of the 40 seeds, paired across H:
B136 **0.000 / 0.005 / 0.002 / 0.945 / 0.038 / 0.001 / 0.000**;
U56 **0.000 / 0.071 / 0.003 / 0.000 / 0.406 / 0.000 / 0.002**.

## GATES — 8 of 11 PASS, and all three failures are ONE object

| gate | \|d\| | |
|---|---|---|
| G1 fast runner == `engine.backtest` | 1.39e-17 | PASS |
| G1b `gross_rescaler(1.0)` == `nrun` | 1.39e-17 | PASS |
| G2 936/1071/1082/1086's committed W/H126 N=20 triple | 1.62e-03 | PASS |
| G3 SPY OOS triple vs committed | 2.89e-03 | **FAIL** |
| G4c \|MaxDD\| of the REBUILT null monotone in lambda | 0.00e+00 | PASS |
| G5 1082's committed H=126 EDGE ladder, both panels | 5.45e-02 pp | **FAIL** |
| G5b 1071/1082's U56 N=20 H=126 null median (CASH) | 4.74e-04 | PASS |
| G5c **1086's committed H=21 and H=63 EDGE ladders — the premise itself** | 4.07e-02 pp | **FAIL** |
| G6 live RULES v2 MaxDD == −12.05% | 4.95e-05 | PASS |
| G7 null draw deterministic in its seed recipe | 0.00e+00 | PASS |
| G8 the finer H dial is LIVE (B136 turnover spread) | 6.47x/yr | PASS |

**The three failures are the `data/prices.csv` nightly-drift defect and nothing else** (the same
object idea 1150's G4 reported). U56's tape now ends **2026-09-16**, one trading day later than
when 1086 ran; B136's still ends **2026-09-11**. Split by panel: **G5 B136 4.53e-03 (inside
tolerance), U56 5.45e-02; G5c B136 4.81e-05 and 4.21e-05, U56 3.63e-02 and 4.07e-02.** So **the
panel this idea is about reproduces 1086's committed columns to five decimal places** and every
headline above rests on it; the drift is confined to the control panel and is reported, not
tolerated away. No tolerance was widened after the fact.

## RULE 8 and both KEEP paths

IS = 2009-2016 only, OOS = 2017-2026 read ONCE. Four choosers x 2 panels = **8 picks, all
published**; base rates over the 126 cells are **4b full 9, 4b OOS 10, 4a 0**.

* **B136: 0 of 4 picks clear 4b OOS.** C_ISSHARPE / C_ISEDGE / C_ISCAGR all pick **N=5 H=63** —
  the very cell this idea is about — and it **fails O_DD** (OOS MaxDD −28.62% against the
  20.23% cap) despite OOS 20.46% / 0.9156. C_ISDD picks N=40 H=52, also O_DD.
* **U56: 1 of 4.** C_ISDD picks **N=40 H=21**, which clears 4b full **and** OOS. It is
  **PRIOR ART** — 1086 committed the same cell reached by the same chooser — and it is
  **dominated on every axis** by the standing 2026-09-04 incumbent (U56 N=20/H=126: 15.55% /
  1.1381 / −19.13%, OOS 16.92% / 1.1615): 12.03% / 1.0940 / −19.27%, OOS 12.95% / 1.1243.
  Its DD margin is **+0.960 pp**, far inside 1083's measured 4.1–7.2 pp resolution.
* **4a: 0 of 126 cells and 0 of 8 picks.** The live book's −12.05% MaxDD is not an (n, H) fact.

**Nothing is proposed. A memo is written for the one rule-8-reachable 4b cell and recommends
PARK**, with exact RULES wording, because it is prior art and a strict regression on the incumbent.
An EDGE that is real and a book that is capital-worthy remain different claims: the cell with the
largest EDGE in this whole run (B136 N=5 H=63, +11.27 pp) fails 4b outright on drawdown.

## Caveats carried

* **The lambda <= 1 clip** (1082/1086's flag) runs 0.00–1.00 of draws by cell and **inflates**
  EDGE where it binds; published at every one of the 126 cells in `.diagnostics.csv` (D2). At
  B136 H=63 the clipped share is 0.00 at n=5 and rises with n, i.e. **against** the monotone
  reading, which survives it.
* **SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists. Every level is optimistic
  and the 4b counts are upper bounds. The bias largely cancels out of EDGE (book and null drawn
  from the same pool over the same tape) but does **not** cancel out of the 4b legs, which are
  measured against SPY.
* **Strict monotonicity is a binary test over 8 steps and is brittle by construction.** The graded
  reading (argmax, end-to-end drop, decisive steps: 4–7 of 8 down, 0–1 up at every hold) is the one
  that replicates; a future citation should quote that, not "the ladder is monotone".

Script `2026-09-17_is-the-B136-H63-MONOTONE-LADDER-a-GENUINE-SLOPE-or-the-MIDDLE-RUNG-of-a-NON-MONOTONE-H-DIAL_C.py`,
9 CSVs, console log, 1 memo, 4 LEADERBOARD rows. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.
