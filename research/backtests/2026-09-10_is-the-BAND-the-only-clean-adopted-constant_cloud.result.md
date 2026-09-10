# Idea 407 — is the BAND the only clean adopted constant?

**Run:** 2026-09-10, cloud. **Verdict: ANSWERED — the band's clean status SURVIVES the finer grid
and the small panel, but for a reason that downgrades it. No KEEP, no RULES change.** RULES.md,
scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

Script: `research/backtests/2026-09-10_is-the-BAND-the-only-clean-adopted-constant_cloud.py`
Artefacts: `.grid.csv .shape.csv .counts.csv .walkforward.csv .keeppaths.csv .console.txt`

Two tuned parameters and no more: **band** (26 distinct values) and **panel** (u56 / broad /
small). Books (EWall, TOP20) and cost rungs (10, 25 bps) are idea 401's cells, carried over
unchanged so the 12-cell counts are comparable. All 312 grid points are committed.

**Gate G1 — reproduction.** Idea 401's own module is imported and its band gate, book weights,
4b bars, margins, `mono()` and panel loaders are used verbatim; this run reproduces all 12
committed band rows of `2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.shape.csv`
— PLATEAU 7/12, C1 0/12, C2 0/12, THIN 0/12, FLIP1 0/12 — with worst relative |d| **broad
2.9e-14, small 1.9e-6, u56 1.2e-2**. The split is mechanical and worth recording: `data/prices.csv`
is rewritten daily and idea 401 ran on the 2026-09-07 vintage, so u56 (whole panel) and SMALL
(its SPY benchmark column only, joined from `prices.csv`) drift while broad, whose cache was not
touched, reproduces to machine precision.

---

## The direct answer

| grid | sweep pts | PLATEAU | C1 | C2 | THIN | FLIP1 | 4b at the adopted 3% | median step_delta |
|---|---|---|---|---|---|---|---|---|
| PUB `{0,2,3,5,8}%` | 5 | 7/12 | 0/12 | 0/12 | 0/12 | 0/12 | 2/12 | 0.00347 |
| FINE `0–8% step 0.5` | 17 | **8/12** | 0/12 | 0/12 | 0/12 | 0/12 | 2/12 | 0.00086 |
| WIDE `0–12% step 0.5` | 25 | **8/12** | 0/12 | 0/12 | 0/12 | 0/12 | 2/12 | 0.00074 |

The band is still plateau, non-crossing, non-thin and non-flipping on a 0.5% grid, on all three
panels including the small one. **Idea 401's headline holds.** Three things say it holds for the
wrong reason.

**1. Three of the four statistics get EASIER to pass as the grid is refined.** `step_delta` is
proportional to the spacing, so it falls **4.7×** (0.00347 → 0.00074) from PUB to WIDE, and
`THIN` (|M\*| < step_delta) is graded against a bar that the publisher moves by publishing more
points. `FLIP1` reads the two *nearest* neighbours, which get closer for the same reason.
`plateau_frac` is a share of points, and it rises 7/12 → 8/12 on the finer grid. Only C1/C2 read
the ordered curve. **Non-THIN at 25 points is a weaker claim than non-THIN at 5 points, not a
stronger one**, so the survival is not the confirmation it reads as.

**2. In a density-free unit the band is not thick — it is INERT.** Restating each verdict in band
percentage points, which no choice of grid can move:

| grid | median plateau WIDTH (band pp) | median thin_pp = \|M\*\|/\|dm/db\| | cells with ANY 4b flip in the whole span |
|---|---|---|---|
| PUB | 8.00 | 40.07 | 1/12 |
| FINE | 8.00 | 72.01 | 1/12 |
| WIDE | 12.00 | 72.01 | 2/12 |

`thin_pp` of 72 band pp means the binding bar would need the band moved 72 percentage points —
six times the whole swept span — before the margin it rests on is spent. That is not thickness,
it is **near-zero sensitivity**: on **3 of 12 cells** (broad/TOP20 and u56/TOP20 at both cost
rungs) the binding DD margin is flat in the band to `step_delta < 1e-9`, so `thin_pp` is
literally infinite. And on **10 of 12 cells there is no band value anywhere in 0–12% that flips
the 4b verdict at all**. The plateau width is the full swept span on the WIDE grid (12.00 pp),
i.e. every band value is within 0.05 Sharpe of the best one.

**3. The book the band sits in mostly fails 4b regardless.** The adopted 3% passes 4b in **2 of
12 cells on every grid** (u56/TOP20 at 10 and 25 bps, binding bar DD, margin +0.0047 and
+0.0032). On the other 10 cells the band is a clean constant inside a book that does not clear
the bar.

---

## Rule 8 (choose the band on 2008–2016, read 2017–2026 once)

Selector: the IS 4-bar min margin (the OOS bar cannot be seen inside IS). 36 picks
(grid × panel × book × cost).

| grid | mean pick | picked the adopted 3% | Δ vs adopted | Δ vs RULES v2 | Δ vs SPY | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| PUB | 6.67% | 2/12 | **−0.0092** | −0.0345 | +0.0498 | 0.9297 | 10.80% | −19.29% |
| FINE | 7.54% | 0/12 | **−0.0105** | −0.0358 | +0.0486 | 0.9285 | 10.78% | −19.65% |
| WIDE | 9.75% | 0/12 | **−0.0072** | −0.0324 | +0.0519 | 0.9318 | 10.82% | −19.63% |

Refining the grid **moves the chosen band away from 3%** — the mean pick walks 6.67 → 7.54 →
9.75% and the adopted value stops being chosen at all (2/12 → 0/12 → 0/12) — and **the move does
not pay**: choosing the band on IS is worse than keeping 3% on all three grids (−0.007 to −0.011
OOS Sharpe). Every pick beats SPY (+0.049 to +0.052) and loses to the live RULES v2 book (−0.032
to −0.036).

Per panel, OOS 2017–2026 (mean over books × costs × grids):

| panel | rule-8 pick | adopted 3% | RULES v2 | SPY | pick CAGR | v2 CAGR | SPY CAGR | pick MaxDD | v2 MaxDD | SPY MaxDD |
|---|---|---|---|---|---|---|---|---|---|---|
| u56 | 1.1427 | **1.1998** | 1.2604 | 0.8758 | 11.96% | 9.34% | 15.32% | −16.99% | −12.07% | −33.72% |
| broad | 0.9757 | 0.9778 | 1.0963 | 0.8820 | 10.74% | 7.81% | 15.45% | −18.95% | −12.26% | −33.72% |
| small | **0.6716** | 0.6392 | 0.5360 | 0.8820 | 9.71% | 3.61% | 15.45% | −22.64% | −14.99% | −33.72% |

The small panel is the only one where dialling the band beats both the adopted 3% and RULES v2
out of sample (0.672 vs 0.639 vs 0.536) — and it still loses to SPY by 0.21 Sharpe and 5.7 pp of
CAGR, so it is not a candidate.

## Both KEEP paths (all 312 grid points)

| panel | book | 4b | 4a vs RULES v2 | 4a vs RULES v1 | points |
|---|---|---|---|---|---|
| u56 | EWall | 0 | 0 | 45 | 52 |
| u56 | TOP20 | **37** | 0 | 0 | 52 |
| broad | EWall | 0 | 0 | 51 | 52 |
| broad | TOP20 | 0 | 0 | 26 | 52 |
| small | EWall | 0 | **8** | 26 | 52 |
| small | TOP20 | 0 | 0 | 52 | 52 |

**No point passes both paths.** The 37 4b passes are all u56/TOP20 and cover 22 of 25 band values
at 10 bps and 15 of 25 at 25 bps — the band is not what makes that book pass, and its DD margin
(+0.0047 at 3%, +0.0004 at 6%) is a fifth of one percent of drawdown. The 8 4a-v2 passes are all
small/EWall and none of them clears 4b. Of the 36 rule-8 picks, 3 pass 4b and 2 pass 4a.
**No KEEP is claimed.**

---

## What this changes

Nothing in RULES: 3% stays, and this run is a reason to be relaxed about it rather than proud of
it — on 10 of 12 cells no band value in 0–12% changes the 4b verdict, and choosing the band on
in-sample data costs ~0.01 of OOS Sharpe against just leaving it alone. One reporting point,
proposed and **not** written into PROTOCOL by this run: `THIN` and `FLIP1` should be published in
the dial's own units (`thin_pp`, `flip_pp`) beside the grid-counted versions, because the counted
versions can be passed by publishing a finer grid.

**Survivorship caveat (PROTOCOL 9):** all three panels are *current*-constituent lists; the small
panel is a sub-$2B screen run today and back-filled to 2010, with the 44 tickers whose
`data/small_meta.csv max_1d_move >= 1.0` dropped first. Delisted, acquired and screened-out names
are absent, so every absolute CAGR/Sharpe above is biased upward and none is a tradable estimate.
The bias flatters the **ungated** end of the band dial (nogate, b=0), i.e. the control, so the
finding that the band's margins are inert and its choice near-costless is understated, not
overstated.
