# Idea 674 (cloud, 2026-09-15) — is the CAGR FLOOR the only bar separating a CONCENTRATED book from its MATCHED control?

**ANSWER: NO — it is the only bar concentration WINS on. Deleting it does not zero the
discrimination, it FLIPS it: every other 4b leg separates the two books in the CONTROL's favour.
KILL for the premise as stated; nothing promoted, no RULES/PROTOCOL change proposed.**

Grid: 3 panels × **1,000 nested k=40 draws** (idea 504's own seed and draw count) × 6 concentration
levels × 2 books + EWall × 3 cost rungs = **117,000 scored books**. Books are idea 504's, unchanged:
`CAND_n` (top n by the no-vol-scaler composite, fixed gross/n per name, cash below n eligible) and
`EWmg_n` (every eligible name, equal weight, at `CAND_n`'s **own daily gross**), so the difference is
selection and nothing else — G2 confirms the daily grosses match to 8.9e-16. Gates **6 of 6 PASS**,
including **G3, a cross-run reproduction of 504's committed headline**: pass-rate gap **+0.5400**
against the committed +0.5450 (the committed CSV re-derives to +0.5450 exactly), paired median
dSharpe −0.00208 against the committed −0.00067 on a four-day-longer tape.

## H_ONLY — REFUTED. The floor is the only leg the concentrated book wins

Discrimination `D = pass4b(CAND_n) − pass4b(EWmg_n)` at PROTOCOL's floor (0.70) and rung (10 bps),
and the same D with one leg deleted:

| panel, n | D | no-L1_H1 | no-L2_H2 | no-L3_OOS | no-L4_DDcap | **no-L5_CAGRfloor** |
|---|---|---|---|---|---|---|
| U56, 3 | −0.2760 | −0.2700 | −0.2760 | −0.2760 | +0.1000 | **−0.7340** |
| U56, 10 | +0.3440 | +0.5680 | +0.3480 | +0.3440 | +0.4220 | **−0.2990** |
| U56, 20 | **+0.5400** | +0.6110 | +0.5400 | +0.5400 | +0.5400 | **−0.1340** |
| B136, 20 | +0.1910 | +0.1970 | +0.2010 | +0.1910 | +0.1990 | **−0.1270** |

Max |D| with the CAGR leg deleted is **0.7340** over the 18 (panel, n) cells and **8 of 18** are at
or above the 0.05 bar, so H_ONLY **FAILS**. The per-leg pass-rate gaps say why: at U56 / n=20 the
CAGR floor is **+0.6110** in the concentrated book's favour while `L1_H1` is **−0.1340** and the
other three are 0.0000; at n=3 the DD cap alone is **−0.8570** and `L3_OOS` −0.2080. The published
+0.545 is therefore a **net of two legs pulling opposite ways**, not a single-leg artefact — and the
correct restatement of the queue's premise is: *the CAGR floor is the only 4b leg on which
concentration scores positive at all; every other leg prefers the matched control.*

## H_STOP — 4b stops discriminating at n\* = 30, but by JOINT FAILURE

At the PROTOCOL floor, the first n with |D| < 0.05 is **n\* = 30 on both large-cap panels**
(D = +0.0120 U56, +0.0100 B136; +0.0000 / +0.0000 at n = 40). But the pass rates there are
**0.014 / 0.002** (U56) and **0.041 / 0.031** (B136): the two books stop being distinguishable
because **both stop passing**, not because they converge in quality — mean gross falls from 0.700
(n = 3) to 0.598 (n = 30) to 0.472 (n = 40) as the fixed-weight book runs out of eligible names and
de-grosses into cash, and the CAGR floor takes both books out together.

## The floor sweep — D is NOT monotone, and PROTOCOL's 0.70 sits at the peak for n = 20

`D` at 10 bps, U56 (rows = floor multiple, cols = n):

| floor | n=3 | n=5 | n=10 | n=20 | n=30 | n=40 |
|---|---|---|---|---|---|---|
| 0.00 | −0.7340 | −0.6800 | −0.2990 | −0.1340 | −0.0170 | +0.0040 |
| 0.55 | −0.7320 | −0.6800 | −0.2960 | −0.1260 | +0.0280 | +0.0000 |
| **0.70 (PROTOCOL)** | −0.2760 | −0.1790 | +0.3440 | **+0.5400** | +0.0120 | +0.0000 |
| 0.85 | +0.0180 | +0.1160 | **+0.4260** | +0.0290 | +0.0000 | +0.0000 |
| 1.00 | +0.0180 | +0.0910 | +0.0170 | +0.0000 | +0.0000 | +0.0000 |
| 1.30 | +0.0150 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |

H_FLOOR (D non-decreasing in the floor) holds on only **7 of 18** cells and H_MONO (D
non-increasing in n) on **11 of 24** rows — both **REFUTED**. D is single-peaked in the floor, and
the peak moves with n: **0.70 at n = 20** (the standing candidate's own width), 0.85 at n = 10 and
n = 5, ≥ 1.00 at n = 3. Below the peak the control wins (a floor of 0.00–0.55 hands `EWmg` a
−0.13 to −0.73 advantage, because with no return bar the four remaining legs all favour it);
above it both books fail. PROTOCOL 4b's published floor is the level at which the bar most favours a
20-name concentrated book — stated as an observed coincidence of bar and book, not as a
recommendation to move either.

## SMALL — the whole phenomenon is a large-cap fact

D = **0.0000 at every one of the 48 (floor, n) cells** on the 611-name sub-$2B panel, because the
pass rate is **0.000 for both books at every floor**: no small-cap draw of either kind clears 4b at
any floor multiple, at any concentration, at any cost rung.

## What concentration actually buys (paired per-draw medians, 10 bps)

| panel, n | dSharpe | dCAGR | dMaxDD | win(Sharpe) |
|---|---|---|---|---|
| U56, 3 | −0.0724 | **+8.61 pp** | −8.05 pp | 0.196 |
| U56, 10 | −0.0535 | +2.77 pp | −3.13 pp | 0.074 |
| U56, 20 | −0.0021 | +1.45 pp | −1.69 pp | 0.464 |
| B136, 20 | −0.0312 | +0.58 pp | −0.93 pp | 0.195 |
| SMALL, 20 | −0.0021 | +0.01 pp | −0.04 pp | 0.463 |

504's finding replicates on every panel and every width: selection buys **CAGR**, pays for it in
**drawdown**, and never earns Sharpe — the concentrated book beats its own matched control on
Sharpe in **0.464** of draws at n=20 and as little as **0.014** at n=5.

## Rule 8 (required) — n chosen on 2009-2016 IS Sharpe alone, 2017-2026 read once

| panel | cost | family chosen from | modal pick | OOS CAGR | Sharpe | MaxDD | OOS 4b rate | OOS 4a rate |
|---|---|---|---|---|---|---|---|---|
| U56 | 10 | CAND only | CAND3 (0.342) | 14.70% | 1.093 | −18.26% | 0.3250 | 0.0090 |
| U56 | 10 | matched controls only | EWmg20 (0.284) | 10.80% | 1.129 | −15.73% | **0.5390** | 0.0050 |
| U56 | 10 | both | CAND3 (0.284) | 14.14% | 1.079 | −18.62% | 0.4100 | 0.0020 |
| B136 | 10 | CAND only | CAND30 (0.323) | 10.19% | 0.950 | −17.92% | 0.0960 | 0.0090 |
| B136 | 10 | matched controls only | EWmg10 (0.402) | 9.92% | 1.000 | −17.22% | 0.2440 | 0.0000 |
| SMALL | 10 | both | CAND20 (0.252) | 2.51% | 0.267 | −27.10% | 0.0000 | 0.0000 |

SPY OOS 15.27% / 0.874 / −33.72% (U56 tape); RULES v2 (live) OOS 9.46% / 1.277 / −12.05%. An
IS-Sharpe chooser let loose inside the concentrated family lands on the **most** concentrated book
(CAND3) and realises a **lower OOS 4b rate (0.325) than never ranking at all (0.539)**; at 25 bps
both families collapse to ≤ 0.084. **4a is ≤ 0.011 in all 27 cells.** No book here is promotable.

## Verdict

**ANSWERED = NO (KILL for the premise as stated).** The CAGR floor is not the only bar separating a
concentrated book from its matched control — it is the only bar on which the concentrated book is
ahead, and the DD cap and `L1_H1` separate them just as hard in the other direction (up to −0.857
at n = 3). 4b stops discriminating at **n\* = 30**, by joint failure rather than convergence. The
discrimination surface is single-peaked in the floor multiple, with the peak at PROTOCOL's own 0.70
for the standing candidate's width and elsewhere for every other width; on SMALL it is identically
zero. Nothing promoted, no memo proposing a RULES change, and `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py`, `baseline.py` are untouched.

**SURVIVORSHIP:** U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown level
is optimistic for both books. This question is the one where that bites hardest: a top-n book picks,
out of a list that already excludes the dead, with exactly the hindsight the ranking is being
credited for — so every `CAND_n` pass rate and every D above is an **upper bound** on what a
point-in-time panel would show, and the negative results (SMALL's identical zeros, the 4a column)
are the robust ones. SMALL additionally drops the 52 tickers with `max_1d_move >= 1.0` per
`data/small_meta.csv`.

Script: `research/backtests/2026-09-15_is-the-CAGR-FLOOR-the-only-bar-separating-a-CONCENTRATED-book-from-its-MATCHED-control_cloud.py`
Artifacts: `.surface.csv` (432 rows), `.stops.csv` (24), `.walkforward.csv` (27),
`.draws.csv` (39,000), `.console.txt`.
