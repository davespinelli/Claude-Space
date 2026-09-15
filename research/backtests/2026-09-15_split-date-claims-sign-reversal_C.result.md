# Idea 844 — which committed SPLIT-DATE claims REVERSE SIGN at a second cut (lane C, 2026-09-15)

**ANSWERED. 15.4% of them do — and the more important finding is that the question idea 834
posed cannot even be asked of this record's price-level claims, because NONE of them is
statistically distinguishable from zero at ANY cut. KILL for capital.** No RULES change, no
book promoted, no KEEP claimed, no memo; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched (rule 6). One PROTOCOL line is **PROPOSED, NOT APPLIED**.

## Selection

Taken as the **SECOND open idea** in QUEUE.md (866 is lane A's). Read as a **PRICED** census
rather than a prose one: the record's split-conditional claims *are* the H1/H2 and IS/OOS legs
that `baseline._row` publishes for a **book**, so this run rebuilds the committed book families
from `research/baseline.py` primitives and re-reads each one's split delta at ten cuts. That
gives the run a real price leg, a rule-8 walk-forward and both KEEP paths, which a text census
of memos could not carry.

## Design

`D(C) = stat(post-C) − stat(pre-C)`. The **NATIVE** cut is `len(r)//2`, which is literally the
convention `baseline._row` uses and every committed 4b memo publishes. Nine second cuts.

- **Tuned param 1 — CLAIM SET (4, all reported):** `LIVE` (BAND075 = RULES v2 live, V1),
  `SHELF` (BAND100 = the standing 4b candidate of ideas 733/795, EWELIG075 = the 2026-09-03
  RECOMMENDATION's Finding 2), `KEEP4B` (CAND20/CAND10 = the 2026-09-04 first-KEEP family,
  top-n equal weight, **no vol scaler**), `CONTROL` (EWALL075 signal-free, SPYBH).
- **Tuned param 2 — SECOND CUT (10, all reported):** NATIVE, CALMID, 2013-01-01 … 2020-01-01.
- **Reported axes, never tuned:** panel (U56 / B136 / STK20), statistic (SH, EXSH = Sharpe −
  SPY Sharpe, CAGR, MaxDD).
- 10 bps, weekly, next-day execution (engine), no leverage/shorts, 260-day warm-up skip,
  IS/OOS boundary 2016-12-31. Moving-block bootstrap, L=21, **B=2000**, paired with SPY,
  seed 20260915.
- **Grid: 24 claims × 10 cuts × 4 statistics = 960 points, every one published**
  (`.grid.csv`); 864 second-cut pairs (`.pairs.csv`).
- Convention stated: books are priced on the panel exactly as `baseline.compare()` does
  (SPY stays in the tradable set), so the LIVE book is bit-identical to
  `baseline.rules_v2_weights` — that is what makes gate G2 exact.

## Gates — seven, ALL PASS, before any new number

| gate | result |
|---|---|
| G1 LIVE book vs the record's committed triple | CAGR 8.6227% / Sharpe **1.2013** / MaxDD **−12.0549%**, max\|d\| **4.948e-05** |
| G2 this run's NATIVE halves == `baseline._row`'s `len(r)//2` halves, 9 book-panels | max\|d\| **0.000e+00** |
| G3 SPY comparand vs the record | 15.1302% / **0.8845** / **−33.7173%**, max\|d\| **6.013e-06** |
| G4 fast metric primitives == `engine.metrics`, 12 series | max\|d\| **6.106e-16** |
| G5 **planted sign flip** (drift +a / −a / +a at 2013 and 2019) | D(2013) **−1.2206** < D(NATIVE) +1.6078 < D(2019) **+2.1539** — the detector reverses exactly where the plant does |
| G6 / G6b bootstrap determinism, and a **process-independent** stream seed | max\|d\| **0**; pinned seeds 645084766 / 1822693704 |
| G7 cut coverage | min short side of any cut on any panel **999 days** |

G6b exists because an earlier draft of this script seeded the per-cut bootstrap from Python's
built-in `hash()`, which is salted per interpreter; the grid moved between two runs of the same
file. It is now pinned with `hashlib`, and **two separate processes produce a byte-identical
`grid.csv` and console**.

## (1) The answer as literally asked

**133 of 864 second-cut pairs (15.39%) reverse sign against the record's NATIVE reading.**
53 of 96 claim-statistics never reverse; 43 reverse at ≥1 cut; **10 reverse at ≥5 of 9**.

Full 2-parameter grid, sign-reversal rate (all cells reported):

| cut | CONTROL | KEEP4B | LIVE | SHELF | ALL |
|---|---|---|---|---|---|
| CALMID | 0.0417 | 0.0417 | 0.0000 | 0.0000 | **0.0208** |
| 2013-01-01 | 0.4167 | 0.2083 | 0.2917 | 0.4167 | **0.3333** |
| 2014-01-01 | 0.1250 | 0.0833 | 0.1667 | 0.1250 | 0.1250 |
| 2015-01-01 | 0.1250 | 0.0833 | 0.1667 | 0.0833 | 0.1146 |
| 2016-01-01 | 0.1250 | 0.0833 | 0.1667 | 0.1250 | 0.1250 |
| 2017-01-01 | 0.2500 | 0.0833 | 0.2083 | 0.2500 | 0.1979 |
| 2018-01-01 | 0.0417 | 0.0833 | 0.0417 | 0.0000 | 0.0417 |
| 2019-01-01 | 0.4167 | 0.0833 | 0.2500 | 0.2500 | 0.2500 |
| 2020-01-01 | 0.2083 | 0.0833 | 0.2083 | 0.2083 | 0.1771 |

By statistic: **SH 0.3241**, EXSH 0.1528, CAGR 0.1389, **MaxDD 0.0000** — the MaxDD split leg
is sign-stable at 96 of 96 claims, because the deep episode sits on the same side of every cut
the record could plausibly use. By panel: U56 0.2083, STK20 0.1458, B136 0.1076.

## (2) The finding that matters more — idea 834's pathology rate is ZERO, and why

**0 of 864 pairs are significant at both cuts with opposite signs, because 0 of 96 claims are
significant even once.** Over all 960 grid points: min p **0.0485**, q10 0.3295, median
**0.6412**. Points with p<0.05: **1 of 960** (chance alone at a 5% size would give ~48), and
**0 of the 96 NATIVE-cut points**.

The power statement — what a split delta would have to *be* to clear p<0.05:

| stat | median \|D\| (NATIVE) | max \|D\| (grid) | median bootstrap SD | needed \|D\| at 1.96 SD | max / needed |
|---|---|---|---|---|---|
| SH | 0.1366 | 0.4238 | 0.4620 | 0.9055 | **0.47** |
| EXSH | 0.1271 | 0.3683 | 0.2664 | 0.5222 | **0.71** |
| CAGR | 0.0194 | 0.0565 | 0.0586 | 0.1149 | **0.49** |
| MaxDD | 0.0631 | 0.1172 | 0.0779 | 0.1526 | **0.77** |

The median half-Sharpe gap the record publishes is **0.15 of the bar** it would have to clear,
and even the largest gap anywhere in the grid is short of it on all four statistics. So the
queue's proposed SIGN-stability leg is the right instinct attached to the wrong diagnosis:
these are not two significant readings that disagree, they are two readings with no power at
all. Idea 834's p=0.0010 is a property of **its own statistic class** (a count over many arms),
not of the record's price-level split claims.

## (3) Rule 8 on the census statistic itself

Cuts split IS (≤ 2016-12-31: CALMID, 2013–2016) / OOS (2017–2020, untouched).
IS-only pick by claim set: **CONTROL 0.1667** > LIVE 0.1583 > SHELF 0.1500 > KEEP4B 0.1000.
The IS pick CONTROL reads **0.2292 OOS** against 0.1667 over all sets; OOS order CONTROL
0.2292 > LIVE = SHELF 0.1771 > KEEP4B 0.0833. **Spearman IS vs OOS across the four sets
+0.9487** — the reversal rate is a stable property, and the set that reverses most is the
**signal-free control**, which is what an unpowered statistic should look like.

## (4) Rule 8 walk-forward on the books (mandatory), and both KEEP paths

Full / IS 2009-2016 / OOS 2017-2026 for all 24 claims is in `.books.csv`; U56 headline:

| book | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| BAND075 (live RULES v2) | 8.62% | 1.2013 | −12.05% | 1.232/1.177 | 9.46% | 1.2772 | −12.05% |
| BAND100 (standing 4b cand.) | 11.54% | 1.2011 | −15.91% | 1.233/1.176 | 12.68% | 1.2765 | −15.91% |
| EWELIG075 | 10.36% | 1.0450 | −15.87% | 1.074/1.022 | 11.24% | 1.1045 | −15.87% |
| CAND20 | 12.60% | 1.0880 | −18.31% | 1.094/1.089 | 14.24% | 1.1602 | −18.31% |
| CAND10 | 12.78% | 0.9241 | −17.54% | 0.917/0.936 | 14.27% | 0.9698 | −17.54% |
| EWALL075 (signal-free) | 13.21% | 1.1197 | −22.53% | 1.196/1.059 | 13.70% | 1.1281 | −22.53% |
| SPY | 15.13% | 0.8845 | −33.72% | 0.959/0.824 | 15.27% | 0.8740 | −33.72% |

**KEEP paths: 4a 0 of 21, 4b 8 of 21** (`.keep.csv`). Nothing here is new — the 4b passers are
the standing BAND100 candidate on U56/B136, EWELIG075 on B136, and four books on the STK20
mega-cap panel the 2026-09-04 memo already rejected as close to a look-ahead portfolio.

## (5) What the proposed leg would cost, and Part E

The 4b half legs are themselves split-conditional claims. Re-read at all ten cuts:
12 of 21 books hold the half leg at every cut; **6 of 21 flip their half-leg verdict at ≥1 of
the 9 second cuts** (median 1.5 of 9 among those). Requiring sign-stable half legs takes
**4b from 8 of 21 to 6 of 21** — lost: **U56/CAND20** and **STK20/V1**; gained: none.

**Part E kills all six survivors for capital.** Against idea 787's bar — the book's own panel,
equal-weighted at the same 0.75 gross, signal-free — **0 of 6 beat their own control on both
Sharpe and CAGR**: U56/BAND100 +0.081 Sharpe but **−1.67pp CAGR**; B136/BAND100 −0.017 /
−3.42pp; B136/EWELIG075 −0.095 / −3.42pp; STK20/BAND075 +0.071 / −7.21pp; STK20/CAND20
−0.033 / −10.27pp; STK20/CAND10 −0.085 / −4.19pp. Consistent with 787's 0-of-82.

## PROPOSED PROTOCOL line (PROPOSED, NOT APPLIED — rule 6, the Sunday review decides)

> **PROTOCOL 4b, half-Sharpe legs.** The two half legs (Sharpe > SPY in BOTH halves) are read
> at the `len(r)//2` count split AND at 2013-01-01, 2015-01-01, 2017-01-01 and 2019-01-01. A 4b
> pass requires the half legs to hold at EVERY one of those five cuts. Beside any published
> half-Sharpe gap, state its bootstrap standard error; a gap below 1.96 SE is reported as a
> **DIRECTION**, never as a difference.

Measured price on this run's shelf: 8 of 21 → 6 of 21. The second sentence is the load-bearing
one: on this evidence **every** half-Sharpe gap the record has ever published is a direction.

## Caveats

1. The claim set is the record's committed **book** families, not every sentence in every memo;
   a text census of memo prose would reach claims this run does not (and is still OPEN as 841).
2. B136 and STK20 are current-constituent panels — survivorship bias, stated per PROTOCOL 9;
   STK20 is the 20-name mega-cap panel the 2026-09-04 memo already flagged.
3. The bootstrap is a moving block at L=21 on daily returns; a different block length would move
   the p-values, though not by the ~13× the SH column would need to reach significance.
4. Books are priced with SPY in the tradable set (baseline.compare's own convention), so EXSH
   is contaminated at 1/N weight. Stated, not corrected, because G2 exactness matters more.

## Artefacts

`.py` · `.console.txt` · `.grid.csv` (960) · `.pairs.csv` (864) · `.perclaim.csv` (96) ·
`.books.csv` (24) · `.keep.csv` (21) · `.halflegs.csv` (21) · `.control.csv` (6)
