# Idea 222 — a-phase-averaged-cadence-as-the-honest-estimator (lane C, 2026-09-06)

**VERDICT: KILL of BOTH published shape claims. Idea 175's humped ladder and idea 188's
M-vs-6W family split are alignment artefacts; both collapse when the block phase is averaged
out. No new book, no KEEP candidate, RULES/scan/bot/baseline untouched.**

6785 backtests = 115 books (ideas 175/187's corpus verbatim) x 13 ladder points x all k phases
(59 phase-runs per book), 10 bps, t+1, IS <= 2016-12-31, OOS 2017-01-01.. read once.
Four estimators, all reported, none preferred: **PH0** (phase 0 only — what the whole record
publishes), **MEANPH** (mean across the k phases of each phase's own metric — the de-confounded
shape estimator, identically PH0 at a k=1 point), **BLEND-DR** (mean of the k phase return
series) and **BLEND-BH** (equal-weight blend of the k equity curves, sleeves left to drift).

## Reproduction — 5 of 5, asserted before any new number

| control | result |
|---|---|
| [a] cad_mask == engine.rebalance_mask at D/W/M/Q; reb/yr monotone over all 13 | PASS |
| [b] fast_backtest == engine.backtest | max ldret 1.4e-16, ldturn 1.1e-15 |
| [c] PH0 ladder == idea 175's committed ladder.csv, 805/805 shared rows | **7.105e-15**, 0 verdict mismatches |
| [d] phase sweep == idea 187's committed phase.csv, 1955/1955 genuine-phase rows | **2.220e-16**; its 345 surplus Q rows (phases 1-3 of a k=1 point) identical to its own Q phase 0 at **0.000e+00** |
| [e] degenerate-phase identity at D/W/M/Q | MEANPH and BLEND-DR **bitwise 0.0**; BLEND-BH 5.3e-14 (equity round-trip) |

[e] is the negative control for the whole construction: zero phase freedom produces zero
averaging effect, so every effect below is phase and not machinery.

## Q1 — the phase-averaged ladder is NOT the ladder idea 175 published

Mean OOS Sharpe, 115 books, all 13 points (full table in `.shape.csv`):

```
est          D     2D      W     2W      M     6W     7W     8W     2M    10W      Q    16W     2Q   argmax
PH0      0.621  0.662  0.680  0.689  0.756  0.780  0.606  0.651  0.826  0.693  0.539  0.630  0.646     2M
MEANPH   0.621  0.664  0.680  0.708  0.756  0.677  0.674  0.674  0.719  0.670  0.539  0.653  0.596      M
```

1. **The slow zone stops being jagged.** Spread across {6W,7W,8W,2M,10W} falls
   **0.2198 -> 0.0491 pooled (4.5x)**, 0.2259 -> 0.0631 SMALL, **0.3108 -> 0.0637 U56 (4.9x)**,
   0.2859 -> 0.0570 ETF. Idea 187's 6W -> 7W collapse of -0.174 becomes **-0.003**. The five
   slow points are one flat plateau; the jaggedness was phase, exactly as idea 187 argued.
2. **The argmax moves to M in every family** (PH0: 2M pooled, 6W on U56 and ETF). Modal argmax
   share 6W 50.4% -> **M 52.2%**; the pre-registered 6W..10W zone share collapses
   **80.0% -> 7.8%**.
3. **Idea 175's headline gap reverses sign.** 6W-minus-W published +0.0999 ALL / +0.1640 U56 /
   +0.1600 ETF; under MEANPH it is **-0.0029 ALL / -0.0500 U56 / -0.0430 ETF**. Under BLEND it
   is +0.018/+0.020 pooled, i.e. positive only by the sleeve-count bonus of point 5 below.
   Idea 175's monotone rise D -> 6W is **False** under all three averaged estimators.
4. **What survives is not a hump.** MEANPH's full range is 0.2173 pooled — *above* idea 187's
   0.1518 pooled phase spread, so P3 misses pooled — but **below** it in all three families
   (SMALL 0.1935 vs 0.2618, U56 0.2941 vs 0.3957, ETF 0.3644 vs 0.3862). The surviving range
   runs between **M and Q, both k=1 points with no phase freedom at all**: there is real cadence
   content on this ladder, and none of it is at 6W. **Q stays the worst of 13 under every
   estimator** (P4 missed) — Q's badness was never a phase artefact.

## The BLEND confound, named and measured (P6 hit)

BLEND-DR minus MEANPH is **exactly 0.0000 at every k=1 point** and rises with sleeve count:
0.0031 (k=2) -> 0.0211 (k=6) -> 0.0292 (k=10) -> **0.0333 (k=16)**, Spearman(k, bonus) **+0.8883**.
A BLEND ladder therefore tilts toward slow points for a diversification reason that has nothing
to do with cadence. It is too small to overturn the ordering here (BLEND's argmax is still M),
but any future "slower is better" claim read off a blended book inherits it. **MEANPH is the
shape estimator; BLEND is the implementability estimator; they are not interchangeable.**

## Q2 — idea 188's M-vs-6W family split does not survive (P5 hit)

Paired per book, OOS Sharpe M minus 6W (`.split.csv`):

| est | SMALL | U56 | ETF | ALL |
|---|---|---|---|---|
| PH0 (reproduces idea 188's signs) | +0.0815 (t +3.78) | **-0.1171 (t -13.99, 0W/33L)** | **-0.0870 (t -16.36, 0W/33L)** | -0.0238 |
| **MEANPH** | +0.0419 (t +3.00) | **+0.0967 (t +13.03, 33W/0L)** | **+0.1163 (t +13.81, 32W/1L)** | **+0.0790 (t +10.69, 96W/19L)** |
| BLEND-DR | +0.0293 (t +2.09) | +0.0658 (t +8.79) | +0.0925 (t +9.99) | +0.0579 |
| BLEND-BH | +0.0273 (t +1.95, sign p 1.00) | +0.0635 (t +8.59) | +0.0906 (t +9.84) | +0.0558 |

**The split does not weaken — it inverts into unanimity.** U56 and ETF go from 0-for-33 and
0-for-33 against M to 33-for-33 and 32-for-33 for it. Idea 188's signal-horizon mechanism was
built to explain a sign that only exists at 6W phase 0. SMALL's preference for M is the one
sign that survives averaging, and it is the weaker of the three.

## Rule 8 (PROTOCOL rule 8) — fourteenth straight do-nothing win, but a much cheaper loss

Fitted selector minus the best constant, paired, pooled (`.walkforward.csv`):

| est | best const | SEL-SHARPE - best const | SEL-4B - best const |
|---|---|---|---|
| PH0 | 2M (0.8258) | **-0.1584 (t -11.76)** | -0.1658 (t -12.45) |
| MEANPH | M (0.7559) | **-0.0246 (t -2.93)** | -0.0388 (t -3.81) |
| BLEND-DR | M (0.7559) | -0.0218 (t -2.93) | -0.0333 (t -3.30) |
| BLEND-BH | M (0.7559) | -0.0211 (t -2.88) | -0.0308 (t -3.04) |

P7 hits on both halves: the selector still loses, and its shortfall shrinks **6.4x** once the
phase noise it was reading is averaged away. **CONST-M is the only arm whose value is identical
under all four estimators (0.7559) — it is a k=1 point and carries no alignment risk at all.**
Under MEANPH it beats every implementable arm pooled and on U56/ETF (SMALL prefers 2M, 0.3242).
Benchmarks over the same OOS window: SPY 15.45%/0.8820/-33.72%; RULES v1 7.73%/0.7471/-13.83%
(U56 parent), 6.35%/0.4923/-36.12% (SMALL parent).

## Both KEEP paths, all 5980 estimator-rows (`.keep.csv`)

| est | 4a | 4b | SMALL | U56 | ETF | 4b on the fixed panels |
|---|---|---|---|---|---|---|
| PH0 | 272 | 90 | 0 | 90 | 0 | U56 @ W, M, 2D, **2M** |
| MEANPH | 232 | 73 | 0 | 73 | 0 | U56 @ W, **2W**, 2D, M |
| BLEND-DR/BH | 254 | 90 | 0 | 90 | 0 | U56 @ W, **2W**, 2D, M |

PH0's 272/90 reproduces idea 187 exactly. SMALL 0 and ETF 0 on 4b is the **fourteenth**
reproduction of idea 136. The one thing that moves is the concrete cost of phase-0 reporting:
**U56 @ 2M holds a published 4b pass only at phase 0 and loses it under averaging, while
U56 @ 2W gains one.** Averaging flips 4b in 37 of 1495 (book, point) cells under MEANPH (10
gained, 27 lost, net -17) and 40 under BLEND (20/20, net 0). Per idea 144 a re-cadenced or
re-phased book is the SAME book, so **nothing here is proposed** and the standing 4b candidate
is untouched.

## Predictions: 4 hit, 1 partial, 3 missed

P1 hit ([a]-[e]). P2 **hit in substance, missed as written**: the slow-zone spread falls 4.5x
and the 0.174 collapse becomes 0.003, but the interior turn count rises 4 -> 5 (the residual
turns are small dips at 16W/2Q), so "turns fall by half" is false — TV/range falls 3.30 -> 2.82,
not to ~2. P3 **missed pooled, hit in all three families** (see Q1.4). P4 **missed**: Q stays
worst. P5 **hit, and harder than predicted** (flip, not fade). P6 **partial**: the bonus is
k-ordered as predicted (rho +0.888) but too small to move the argmax to 16W. P7 hit. P8 hit.

## Proposed for Sunday review (report-only; PROTOCOL, not RULES)

Extending idea 187's proposed clause 12 with the estimator this run validates:

> **12. Phase-averaged cadence.** Any comparison between multi-unit-block cadences (2W, 6W, 2M,
> …) must be made on the **phase-averaged** book: run all k phases at cadence k and report the
> mean of their metrics (MEANPH). A single-phase figure is one draw from a distribution whose
> spread exceeds every cadence effect this project has published, and may be reported only
> beside its own phase spread. Where a *blended* book (mean of phase returns, or of phase
> equity curves) is reported instead, its diversification bonus over MEANPH — 0 at k=1, rising
> to +0.033 of Sharpe at k=16 here — must be published beside it, because that bonus is ordered
> in sleeve count and not in cadence.

## Caveats

SURVIVORSHIP: SMALL439/U56/ETF36 are current-constituent lists (data/SMALL_PANEL_README.md,
idea 54); every phase and point inherits it equally so the paired comparisons hold, but no level
here is an attainable return. BLEND-DR's daily re-levelling between sleeves is not costed
(BLEND-BH is the costed bound and agrees with it to <0.003 of Sharpe everywhere). Idea 38: D/2D
rebalance on some non-trading days on the calendar-day-indexed panels. 10 bps and t+1 only;
idea 188 established the cadence split is not a cost effect. The OOS window was read once.

Script `research/backtests/2026-09-06_a-phase-averaged-cadence-as-the-honest-estimator_C.py`;
`.console.txt`, `.shape.csv`, `.split.csv`, `.walkforward.csv` and (gzipped, pandas reads them
directly) `.phaserows.csv.gz` (6785 phase rows), `.ladder.csv.gz` / `.keep.csv.gz` (5980
estimator rows with both verdict columns) alongside.
