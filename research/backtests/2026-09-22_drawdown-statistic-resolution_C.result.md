# Idea 1542 (lane C, 2026-09-22) — how many committed DRAWDOWN CLAIMS sit INSIDE the DD leg's own SE, and is there ANY drawdown-path statistic that can adjudicate a 1 pp move at this sample length?

**ANSWERED = NO STATISTIC CAN, AND THE ONE THE PROTOCOL ALREADY USES IS THE BEST OF THE SIX.**
KILL for the idea's constructive proposal ("if one exists, the 4b DD cap should be restated in it").
No new KEEP on either path: **4a 0 of 60 book cells; 4b 11 of 60 FULL / 10 of 60 OOS, every one of them a plain
GROSS rung of the live band book** — i.e. this run reproduces idea 2264's candidate on an independent script and
finds nothing else.

Script: `2026-09-22_drawdown-statistic-resolution_C.py` (deterministic, seed 1542; verified identical under a
second `PYTHONHASHSEED`). Artefacts: `.books.csv` (60), `.contrast_se.csv` (2,916), `.dd_leg.csv` (396),
`.adjudication.csv` (324), `.walkforward.csv` (18), `.census.csv` (6,171), `.points.csv`, `.log.txt`.
Price-only on the committed caches. Costs 0/10/25 bps, PROTOCOL rung 10; weights at close t applied at t+1.

## Tuned dials: exactly two
The **STATISTIC** (6 rungs) and the bootstrap **BLOCK LENGTH L** (3 rungs). Panel (u56, b136), cost rung
(0/10/25 bps), device (10) and window (FULL / H1 / H2 / IS 2009-2016 / OOS 2017-2026) are **reported at every
grid point, never selected**. All 18 (statistic x L) points are published below, and all 324 (panel x cost x
window x L x statistic) adjudication rows are in `.adjudication.csv`.

## Gates (all PASS)
| gate | test | reading |
|---|---|---|
| G1 | derived cost rung == full re-simulation at 10 bps | max&#124;dr&#124; **0.000e+00** |
| G2 | the anchor IS the live RULES v2 book | max&#124;dw&#124; **0.0** |
| G3 | anchor u56 @10 bps reproduces its committed MaxDD | −12.05%, &#124;d&#124; = **0.005 pp** |
| G4 | determinism | log byte-identical under a second `PYTHONHASHSEED` |

## The method
For each device (gross ladder 0.25→1.50 at band 0.03; band ladder 0.00/0.06/0.09 at gross 0.75; RULES v1 n=5)
against the frozen incumbent, a **paired circular-block bootstrap** (same resample index for every book,
B = 1,000) gives the SE of the **contrast** stat(device) − stat(anchor) for six statistics of the drawdown path:
MaxDD, Calmar, Ulcer, time-under-water, CVaR5 of rolling 1y returns, mean drawdown. Each statistic is then
scored by its **ADJUDICATION RATIO**

  `R = |dS/dMaxDD| / (2 x median contrast SE)`, the slope fitted across the gross ladder,

so **R ≥ 1 means the statistic resolves a move worth 1 pp of MaxDD at |t| > 2**. MaxDD has slope 1 by
construction, so its R is simply `1 / (2 x SE)` and the comparison is like-for-like in MaxDD units.

## RESULT 1 — nothing reaches R = 1. **0 of 324 grid points.**
Highest R anywhere in the grid: **0.621** (u56, 0 bps, IS window, L = 126, **MaxDD**). Pooled means @10 bps:

| statistic | R FULL | R IS | R OOS | OOS decisive share |
|---|---|---|---|---|
| **MaxDD (incumbent)** | **0.405** | **0.527** | **0.387** | **63.0%** |
| MeanDD | 0.355 | 0.439 | 0.248 | 53.7% |
| Ulcer | 0.343 | 0.494 | 0.268 | 55.6% |
| CVaR5 of rolling 1y | 0.155 | 0.166 | 0.144 | 5.6% |
| Time-under-water | 0.146 | 0.149 | 0.109 | 38.9% |
| Calmar | 0.058 | 0.050 | 0.041 | 0.0% |

The statistic PROTOCOL 4b already uses is the **best** of the six on every window, and the two most-cited
alternatives in the record's prose — Calmar and CVaR — are the **worst**, by an order of magnitude on Calmar.
The answer to 1542's constructive half is therefore not "restate the cap in X"; it is **there is no X**.

## RESULT 2 — the resolution floor, stated in the cap's own units
MaxDD contrast resolution `2 x SE` @10 bps, in pp:

| panel | L | FULL | IS | OOS |
|---|---|---|---|---|
| u56 | 21 / 63 / 126 | 2.73 / 2.28 / **1.94** | 2.31 / 2.05 / **1.65** | 2.79 / 2.33 / **2.10** |
| b136 | 21 / 63 / 126 | 2.84 / 2.68 / **2.60** | 1.95 / 1.89 / **1.69** | 3.14 / 2.85 / **2.56** |

**The smallest MaxDD move this corpus can convict is ~1.9–2.8 pp.** Any committed claim that a device "moved
drawdown" by less than that is a claim the tape cannot support, whichever of the six statistics it is written in.

## RESULT 3 — more tape does not buy drawdown resolution (it costs it)
Median MaxDD contrast SE is **larger on the FULL window than on the 2.21x shorter IS window** (ratio
SE_FULL/SE_IS = **1.35**), because MaxDD is a maximum over the window: both its level and its dispersion grow
with horizon. The time-average statistics do shrink (Calmar 0.60, TUW 0.75, MeanDD 0.91, CVaR 0.95, Ulcer 1.03),
but their slope per pp of MaxDD shrinks at least as fast, so **R falls with sample length for all six**
(e.g. MaxDD 0.527 IS → 0.405 FULL). The record cannot wait its way out of this: "five more years of tape"
is not a remedy for a MaxDD contrast.

## RESULT 4 — rule 8, read once
Chooser: the statistic and L with the highest **IS (2009-2016) pooled R at 10 bps**; 2017-2026 read once.
**Pick = MaxDD, L = 126** (R_IS 0.599) → **R_OOS 0.433, decisive share 77.8%**. The incumbent statistic under the
same rule is the same object, so the **lift of the chooser over doing nothing is exactly 1.00x** — an IS-only
chooser cannot find a better drawdown statistic because there is not one to find. All 18 grid points are in
`.walkforward.csv`; the runner-up families (Ulcer L=126, R_IS 0.543 → R_OOS 0.285; MeanDD L=63, 0.485 → 0.246)
both **degrade** out of sample by a third to a half, while MaxDD degrades by a quarter.

## RESULT 5 — PROTOCOL 4b's own DD leg, priced against its own SE (this is the decision-relevant one)
Bootstrapping the leg PROTOCOL actually convicts on, `margin = MaxDD(book) − 0.60 x MaxDD(SPY)` in pp:
**57.5% of the 120 (panel x window x L x device) cells @10 bps are decidable at |t| > 2**; 67.6% among the cells
whose leg passes. The live anchor's own leg is comfortably decidable (u56 FULL **+8.18 pp, SE 2.56, t +3.19**).
**But the record's headline 4b candidate is not.** u56 `GROSS_g1.00` (idea 2264's candidate), OOS, L = 126:
leg margin **+4.32 pp, SE 2.36, t +1.83 — PASS but UNDECIDABLE**; `GROSS_g1.25` **+0.54 pp, t +0.24**. On b136 the
same g = 1.00 leg is decidable (**t +2.01**) but that cell misses 4b OOS on the CAGR floor at ≥10 bps. So the
one book the record is carrying toward real capital clears the drawdown cap by a margin its own bootstrap
cannot separate from zero on the panel where it passes.

## RESULT 6 — the census
6,171 committed book-level MaxDD figures over **387 files** (5,391 `CAGR/Sharpe/MaxDD` triples + 780 named
`MaxDD ... %`), each contrasted with the frozen incumbent's committed −12.05%. Median committed MaxDD −19.05 pp;
median |contrast| 7.05 pp.

| SE used | inside 1 SE | inside 2 SE (not distinguishable at &#124;t&#124; > 2) |
|---|---|---|
| idea 1511's 2.93 pp | 27.1% | **41.9%** |
| this run, L = 21 (1.38 pp) | 19.6% | 26.7% |
| this run, L = 63 (1.20 pp) | 18.9% | 24.9% |
| this run, L = 126 (1.15 pp) | 18.8% | **24.5%** |

So **between a quarter and two-fifths of every committed drawdown figure in the record is a number the tape
cannot tell apart from the live book** — the wide end on 1511's own SE, the narrow end on the SE measured here.
*Limit of the census, stated rather than glossed:* it reads committed book-level MaxDD **figures**, contrasted
against one anchor; the figures come from books on different panels, windows and cost rungs, whereas the SE is
for a paired same-tape contrast. It bounds how much of the record is resolution-limited; it does not adjudicate
any individual prose claim.

## Books (PROTOCOL 4a and 4b at every cell) — `.books.csv`, 60 cells
4a: **0 of 60**, unconditionally (gross is Sharpe-neutral on this book: u56 Sharpe 1.2010 → 1.2000 over
g = 0.25..1.50, and every rung above the live gross is strictly deeper in drawdown). 4b FULL 11, 4b OOS 10, all
`GROSS_g1.00` / `GROSS_g1.25` on u56 (and g1.25 on b136). u56 @10 bps: anchor FULL 8.62% / 1.2010 / −12.05%,
OOS 9.46% / 1.2767 / −12.05%, turnover 1.77x; `GROSS_g1.00` FULL 11.53% / 1.2009 / −15.91%,
**OOS 12.67% / 1.2760 / −15.91%**, turnover 2.35x; SPY FULL 15.14% / 0.8851 / −33.72%,
OOS 15.29% / 0.8751 / −33.72%. Band rungs and RULES v1 (n=5, turnover 23.6x/yr, Sharpe 0.655) pass nothing.

## Verdict
**KILL** for 1542's constructive proposal (no statistic of the drawdown path can adjudicate a 1 pp move on this
corpus; the cap should stay in MaxDD, which is the best of the six). **CENSUS DELIVERED** (24.5%–41.9% of the
record's committed drawdown figures are inside the DD leg's own SE). **CAVEAT FILED** against the record's only
reliable 4b passer: its OOS drawdown margin is +4.32 pp at SE 2.36, t +1.83 — a pass, but not a decidable one.
