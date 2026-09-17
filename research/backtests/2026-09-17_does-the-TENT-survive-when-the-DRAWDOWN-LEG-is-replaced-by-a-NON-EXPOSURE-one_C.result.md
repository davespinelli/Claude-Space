# Idea 1166 (lane C, 2026-09-17) — does the TENT survive when the DRAWDOWN LEG is replaced by a NON-EXPOSURE one?

Claimed as queue idea **1163** and renumbered **1164** on claim (1163 was already taken in the
queue's Done section by the cloud lane's `is-the-RECORD-REPRODUCIBLE-AT-ALL` idea), then **1166** on
push, because lane B's concurrent push filed new open ideas 1164 and 1165 first — defect 932, lane
collision, third time. 1162 is likewise duplicated in the Open list and was left alone.

Script: `2026-09-17_does-the-TENT-survive-when-the-DRAWDOWN-LEG-is-replaced-by-a-NON-EXPOSURE-one_C.py`
(11 s, deterministic, no network; tapes PINNED at 2026-09-15).

## ANSWER = YES IN SHAPE, NO IN SUBSTANCE — and the queue's yes/no is the wrong question

The tent's **shape** (non-monotone min, interior argmax, binding leg changing across the ladder)
**survives** a non-exposure swap at 6 of 40 cells, so `H_TENTDIES` as pre-declared **FAILS** and
so does `H_PAIRONLY`. But **not one** of those six survives the peak test: on the gross dial the
peak beats **both** endpoints by over one paired bootstrap SD at **4 of 4 exposure-leg cells and
0 of 4 non-exposure ones**. 1154's mechanism reading is therefore right in substance and its
*shape* test (non-monotone + interior) is simply too weak to state it.

**The mechanism, exactly.** A degree-0 leg does not go flat — it goes *nearly* flat, and the min
becomes a **RAMP-then-PLATEAU**, not a tent: `M_CAGR` climbs until it crosses the swapped leg, and
past the crossing the plateau tilts by the leg's residual only. On the gross ladder that residual
is **−0.0041 (U56 TUW), −0.0035 (B136 TUW), −0.0096 (U56 ULCER), +0.0053 (B136 ULCER)** against a
ramp of **+0.58 to +0.73** — two orders of magnitude apart. The argmax sits at the crossing and its
exact rung is decided by that tilt, i.e. by noise. **The tilt's SIGN is not even stable across
panels**: U56's ulcer margin runs +0.0858 → +0.0723 (down, so a "tent" picking 0.625) while B136's
runs +0.1161 → +0.1305 (up, so a monotone RAMP picking the endpoint 1.000) — the same leg, the same
construction, opposite shapes, on a measured degree slope of −0.0078 vs +0.0084.

**The exposure legs behave as 1154 said.** `L_VOLTGT` — a vol cap, still a degree-1 object — is a
TENT on both panels with a plateau tilt of **−0.193 / −0.324** and a peak resolved at **+2.15 /
+2.66 SD** on the far side, and `L_DD` at **+2.81 / +3.52 SD**. `H_TENTLIVES` **HOLDS**: swapping
one exposure leg for another keeps the object intact. So the tent is a property of the **pair's
homogeneity degrees**, exactly as 1154 read it — a *resolvable* tent needs two degree-1 legs.

**Degrees measured, not asserted (`H_DEGREE` HOLDS, 14 of 14).** On the gross ladder the OLS slope
of log|stat| on log(gross): |MaxDD| +0.979/+0.981, vol +1.001/+1.001, ulcer index +1.014/+1.002,
CAGR +1.006/+1.011; Sharpe +0.001/+0.003, UPI −0.008/+0.008, TUW +0.008/+0.005 (U56/B136). G12
validates the machinery on an exactly-scaled synthetic book first (deg-1 stats +0.98..+1.02,
deg-0 stats within 0.013 of zero).

## A DEFECT IN THIS RUN'S OWN PRE-REGISTRATION, PUBLISHED NOT ABSORBED

The pre-declared `FLAT` guard — "the min's whole-ladder spread is under one paired SD" — caught
**0 of the 6** non-exposure tents on the gross dial, because the spread it measures is carried
*entirely by the ramp*: the U56 TUW cell reads **7.23 SD** of whole-ladder spread while its peak
stands **0.06 SD** above the far endpoint. The peak test (`need_lo`, `need_hi`, each against the
paired SD of that very difference) is **POST-HOC, added after the first run and labelled as such
everywhere**; the pre-registered verdicts are published unchanged above and in `.hypotheses.csv`.
Any future run pricing a "tent", "hump" or "interior pick" should use per-endpoint margins, not a
whole-ladder spread.

## THE TWO TUNED PARAMETERS, AND WHY THE MULTIPLIER IS NOT A THIRD

LEG {L_DD (control), L_VOLTGT, L_TUW, L_ULCER} × DIAL {D_GROSS, D_N, D_HOLD, D_CADENCE, D_MAXVOL}
= 20 cells per panel, **40 in all, every one published** in `.shapes.csv` / `.picks.csv`; all 66
rungs per panel are in `.grid.csv` whatever a chooser did. `M_S` and `M_CAGR` never move — only the
third leg of the min is swapped, which is what makes the four choosers comparable. The cap
multiplier is **algebraically not a parameter**: `(mult·spy − book)/(mult·spy)` is a positive affine
transform of `−book`, so each leg's monotonicity, direction and rho are exactly multiplier-invariant
(**G11 = 0.00e+00**). It can only move where the legs cross, so all four multipliers
{0.60, 0.80, 1.00, 1.25} are published in `.mult.csv` and the verdict is read at the pre-declared
primary (0.60 for L_DD = 4b's own constant, 1.00 for L_VOLTGT/L_TUW). The annex is itself
informative: L_DD's tent **dies at mult 1.25** on both panels (pick goes to the endpoint 1.000) and
L_TUW's **does not exist at mult 0.60** (pick 0.200) — the crossing leaves the ladder at both ends.

## GATES — 14 of 14 PASS, printed before any result number

G1 fast runner ≡ `engine.backtest` 1.39e-17 · **G2** committed U56 W/H126/N=20 triple 4.12e-05
(15.5793% / 1.1397 / −19.1276%), and **the vintage published not absorbed: the same gate UNPINNED
reads 1.62e-03, 39.4x, off one extra bar of 4,706** · G3 SPY OOS triple 1.70e-04 · G4 1098/1102's
n=12 triple 4.71e-05 · G5 live RULES v2 MaxDD 4.95e-05 · G6 determinism 0 · G7 cadence masks 0 ·
**G8 CROSS-RUN: 1150's eight single-statistic picks AND 1154's two tent picks reproduce exactly
(0.625 U56 / 0.575 B136)** · **G8b 1154's committed U56 margin endpoints reproduce to 4.94e-05**
(M_S +0.2353→+0.2377, M_DD +0.7127→−0.3903, M_CAGR −0.6485→+0.7738) · G9 / G9b the ALGEBRA on
20,000 synthetics, so the run cannot be read as having discovered that min(mono, flat) is monotone
or that min of two opposed monos is unimodal · G10 ladders nest the record's rungs · G11 the affine
identity · G12 the degree machinery on an exactly-scaled book 1.77e-02.

## RULE 8 AND BOTH KEEP PATHS

Every chooser is IS-only by construction, so each of the 40 picks **is** a walk-forward decision:
read on 2009-01..2016-12-31, scored on 2016-12-31..2026-09-15 untouched.

| arm | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|
| SPY (U56 span) | 15.10% / 0.8829 / −33.72% | 0.9588 / 0.8207 | 15.21% / 0.8711 / −33.72% |
| live RULES v2 (U56) | 8.62% / 1.2008 / −12.05% | 1.2322 / 1.1760 | 9.46% / 1.2763 / −12.05% |
| SPY (B136 span) | 15.16% / 0.8861 / −33.72% | 0.9596 / 0.8259 | 15.33% / 0.8767 / −33.72% |
| live RULES v2 (B136) | 7.98% / 1.0993 / −12.24% | 1.2348 / 0.9658 | 7.88% / 1.1059 / −12.24% |
| **U56 D_GROSS L_VOLTGT pick 0.775** | **16.10% / 1.1398 / −19.72%** | **1.2038 / 1.0972** | **17.54% / 1.1645 / −19.72%** |
| U56 D_GROSS L_DD pick 0.625 (1154's) | 12.96% / 1.1393 / −16.12% | 1.2034 / 1.0966 | 14.10% / 1.1639 / −16.12% |
| U56 D_GROSS L_TUW pick 0.575 | 11.91% / 1.1391 / −14.90% | 1.2032 / 1.0964 | 12.96% / 1.1637 / −14.90% |
| B136 D_GROSS L_VOLTGT pick 0.675 | 14.43% / 1.0628 / −18.81% | 1.2893 / 0.8838 | 14.43% / 1.0093 / −18.81% |
| B136 D_GROSS L_DD pick 0.575 | 12.29% / 1.0620 / −16.18% | 1.2884 / 0.8829 | 12.30% / 1.0084 / −16.18% |

- **4a = 0 of 132 cells and 0 of 40 picks** (`H_NOPAY4a` HOLDS) — as at 1150's 528, 1154's 132 and
  1161's 66. The live book's MaxDD is −12.05%; no cell on any of the five dials gets near it.
- **4b full + OOS: 34 of 132 ladder cells (25.8%) and 7 of 40 picks (17.5%)**. `H_PICKPAY` HOLDS on
  its stated bar (interior picks 7 of 27 = 25.9% vs base rate 25.8%) but the honest reading is that
  the bar is a coin-flip margin: **every one of the 13 endpoint picks fails 4b (0 of 13)** and every
  pass is an interior pick, which is the real signal, and it is about interiority, not about the leg.
- **NOTHING NEW FOR CAPITAL, and the reason is the incumbent.** On U56 the frozen live gross 0.750
  already clears 4b full+OOS (15.58% / 1.1397 / −19.13%, OOS Sharpe 1.1644), and 11 of the 33 gross
  rungs (0.525..0.775) clear it, so a chooser that lands at 0.775 has bought nothing: its whole-
  ladder Sharpe spread is 1.1391→1.1398. The selector's only live claim is on **B136**, where the
  incumbent 0.750 FAILS (−20.74% MaxDD vs the −20.23% cap) and the L_VOLTGT pick 0.675 passes. That
  is the same de-grossing-selector family 1154 and 1161 already PARKED; a memo with exact RULES
  wording is filed beside this file and **recommends PARK, not enact**.
- Best ladder cell (not reachable by any chooser here): U56 D_N rung 12 — 17.71% / 1.1692 / −20.17%
  full, OOS 18.89% / 1.1759 / −20.17%.

## HYPOTHESES

| hypothesis | bar | value | verdict |
|---|---|---|---|
| H_DEGREE | declared degrees == measured slopes (deg1 ≥ 0.5, deg0 ≤ 0.25) | 14/14 | **HOLDS** |
| H_TENTLIVES | L_VOLTGT (exposure) is a TENT on D_GROSS, both panels | True, True | **HOLDS** |
| H_TENTDIES | L_TUW and L_ULCER monotone AND endpoint on D_GROSS, both panels | 1 of 4 (B136 ULCER only) | **FAILS** |
| H_PAIRONLY | no NON-exposure leg is a TENT on ANY dial | 6 of 15 tents are non-exposure | **FAILS** |
| H_PICKPAY | interior picks clear 4b full+OOS at ≥ the ladder base rate | 0.259 vs 0.258 | HOLDS (coin-flip margin) |
| H_PEAKRESOLVED *(POST-HOC)* | peak beats BOTH endpoints by >1 paired SD only for exposure legs | exposure 4/4, non-exposure 0/4 | **HOLDS** |
| H_NOPAY4a | 4a is 0 of every cell and every pick | 0/132 cells, 0/40 picks | **HOLDS** |

## WHAT THIS CHANGES AND WHAT IT DOES NOT

Nothing is enacted (PROTOCOL rule 6). RULES.md, scan.py, bot.py and baseline.py are untouched.
Two things are offered to the record, neither proposed as a clause here: (i) an interior argmax on
a min-of-legs chooser must be published with its **per-endpoint** margins in paired SDs, because a
whole-ladder spread cannot tell a tent from a ramp-then-plateau; (ii) the homogeneity degree of a
leg's statistic in the dial is cheap to measure (one OLS slope on an existing ladder) and predicts
whether the pick is an object or a coin flip at 8 of 8 gross cells here.

Files: `.gates.csv` (15) `.grid.csv` (132×64) `.degree.csv` (14) `.shapes.csv` (40×33)
`.picks.csv` (40) `.mult.csv` (120) `.walkforward.csv` (44) `.hypotheses.csv` (7) `.console.txt`.
