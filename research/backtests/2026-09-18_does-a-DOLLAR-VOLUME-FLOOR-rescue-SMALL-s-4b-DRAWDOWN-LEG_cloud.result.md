# Idea 1343 (lane cloud, 2026-09-18) — does a DOLLAR-VOLUME FLOOR rescue SMALL's 4b DRAWDOWN LEG?

**VERDICT: KILL, decisively, and in the opposite direction to the hypothesis.** A 63-day median
dollar-volume floor does not repair SMALL's drawdown — it **destroys** the book, monotonically,
on every axis and at every N. At N=15 the floor takes MaxDD from **−33.35% to −66.87%** and CAGR
from **+7.06% to −5.59%** as it rises $0 → $30M. The 4b DD leg passes in **0 of 20** cells; the
best MaxDD anywhere in the grid is −29.52%, still **9.29 pp** outside the −20.23% cap. And the
damage is **not** the smaller pool: a pool-size-matched random-subset null holds at −28.6% to
−31.6% MaxDD and ~0.49–0.57 Sharpe at every rung, so the DV screen's **own** effect at $30M is
**−35.84 pp of MaxDD and −0.8584 of Sharpe**. 28 cells + 100 null books, all published.
10 gates pass, 0 fail. Offline, deterministic, 25.7 s. No RULES/PROTOCOL change (rule 6).

## The instrument
Two dials and no more (rule 4): **DV {$0, $1M, $3M, $10M, $30M} × N {10, 15, 20, 30}** on SMALL,
at the frozen incumbent (H=126, gross 0.60, weekly, 10 bps, t+1, no leverage). U56 and B136 run
at DV=$0 across the same N ladder as un-screened controls (`baseline.load_volume` serves the
small panel only). The screen: `dv_t` = 63-day rolling **median** of close × share volume, read
at the selection row t−1 and applied at t — a median so one halt or block print cannot admit a
name. The floor gates **admission only**; a held name exits on the record's min-hold rule H, as
every other eligibility gate in this family behaves. SMALL liquidity for scale: p10 $2M,
p25 $3M, p50 $7M, p75 $13M, p90 $22M.

## 1. The floor is monotone poison — MaxDD on SMALL
| N | $0 | $1M | $3M | $10M | $30M |
|---|---|---|---|---|---|
| 10 | −36.19% | −38.01% | −48.61% | −57.65% | **−72.22%** |
| 15 | −33.35% | −36.32% | −45.50% | −55.87% | **−66.87%** |
| 20 | −29.52% | −34.78% | −41.96% | −53.72% | −69.19% |
| 30 | −29.94% | −32.16% | −38.19% | −54.99% | −65.45% |

CAGR moves the same way (N=15: 7.06% → 3.67% → 0.11% → −2.61% → −5.59%), Sharpe likewise
(0.5202 → −0.2877). **4a 0 of 28 cells; 4b 8 of 28, every one of them a U56 or B136 control —
SMALL is 0 of 20, failing all four legs (H1/H2/DD/CAGR) in every cell.**

## 2. It is the screen, not the pool (the confound, priced)
Null control, not a dial: at each rung's realised pool share, 20 **fixed random sub-pools** of
the matched size are drawn from the un-screened investables and run at N=15; the median is the
comparand. 100 books, seeded deterministically.

| DV | matched pool | DV-screened | random-pool median | **DV's own effect** |
|---|---|---|---|---|
| $1M | 409 | 3.67% / 0.3061 / −36.32% | 6.30% / 0.4879 / −31.57% | −2.63 pp / −0.1818 / **−4.76 pp** |
| $3M | 273 | 0.11% / 0.0856 / −45.50% | 6.06% / 0.4902 / −29.68% | −5.95 pp / −0.4046 / **−15.82 pp** |
| $10M | 107 | −2.61% / −0.0919 / −55.87% | 6.71% / 0.5660 / −28.59% | −9.32 pp / −0.6579 / **−27.29 pp** |
| $30M | 28 | −5.59% / −0.2877 / −66.87% | 6.88% / 0.5707 / −31.03% | −12.47 pp / −0.8584 / **−35.84 pp** |

A random 28-name sub-pool of this panel draws down 31%; the 28 **most liquid** names draw down
67%. Within a sub-$2B universe, high dollar volume is not a quality signal — it selects the
heavily traded, heavily contested, story-and-distress end of the panel, and that cohort is where
the drawdown lives. **The record's standing reading — that SMALL's DD leg is a concentration or
exposure fact — survives this run; the liquidity reading does not.**

## 3. Rule 8 (2017–2026 read once), (DV, N) by argmax IS Sharpe
| panel | pick | OOS pick | OOS anchor (DV=$0, N=15) | 4b all legs |
|---|---|---|---|---|
| SMALL | DV=$0, N=30 | 5.60% / 0.4508 / −29.94% | 6.40% / 0.4653 / −33.35% | **0** |
| U56 | DV=$0, N=15 | 15.12% / 1.1947 / −16.38% | = anchor | 1 |
| B136 | DV=$0, N=10 | 13.49% / 0.9210 / −16.41% | 14.11% / 1.0454 / −15.97% | 1 |

SPY OOS 15.33% / 0.8769 / −33.72%; live RULES v2 OOS (SMALL calendar) 4.47% / 0.6518 / −12.18%.
**The IS chooser rejects the floor outright on the one panel where it exists** — it picks $0 —
and the only thing it buys on SMALL is −0.0146 of OOS Sharpe for a 3.41 pp shallower drawdown
that is still 9.7 pp outside the cap. 4b all legs after rule 8: **2 of 3**, both on the
un-screened large-cap controls, neither touched by this idea's dial.

## 4. What this closes
SMALL's 4b failure is **not** a tradability artifact. The book is not being dragged down by names
too thin to own; if anything it is being held up by them. That removes liquidity from the list of
candidate repairs for this panel and leaves the record's own two — concentration (N) and exposure
(gross) — both already walked and both already short of the cap. **KILL.**

## Gates (10/10)
G0 sample ≥ 10 y · **G1** SMALL DV=$0 / N=15 replays idea 1305's committed flat control
7.06% / 0.5202 / −33.35% · **G2** U56 N=15 replays idea 1215's committed incumbent
13.66% / 1.1706 / −16.38% · **G3** the floor is monotone — the admitted pool never grows as the
floor rises (238 → 147 → 98 → 38 → 10 names clearing every gate per rebalance row) · **G4**
admission audit: **0** names ever admitted below the floor in force at their selection row ·
G5/G6 IS and OOS windows disjoint, OOS starts 2017-01-03 · G7 the DV median is causal by
construction (rolling, read at t−1, applied at t).

## Survivorship (rule 9), and why it bites harder here
SMALL663 is a **current-constituent** sub-$2B screen carried back to 2010, so its levels are an
upper bound. A DV floor interacts with that bias in a **stated direction**: it removes the
thinnest survivors, which are disproportionately the names whose survival was least likely, so
any DD *improvement* from the floor would be partly a re-selection of the surviving cohort and
would be an upper bound on the real effect. This run finds no improvement at all — the floor
makes drawdown worse — so the bias works **against** the measured result and the KILL is, if
anything, understated. U56 and B136 are also current-constituent lists.

Data: `.grid.csv` (28 cells) · `.poolnull.csv` (5 rungs × 20 seeds) · `.walkforward.csv` ·
`.gates.csv` · `.liquidity.csv` · `.console.txt`.
