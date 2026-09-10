# Idea 412 — does PARTIAL REBALANCING beat CADENCE as the turnover dial?  (cloud, 2026-09-10)

**VERDICT: SPLIT — the queue's PREMISE is REFUTED outright and backwards, its QUESTION is
answered NULL and shown to be BELOW ITS OWN NOISE FLOOR, and the record should adopt NEITHER dial
as its turnover instrument.  No KEEP, no book promoted, no memo, no RULES change.  RULES.md /
PROTOCOL.md / scan.py / bot.py / baseline.py untouched.**

Script `2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_cloud.py`; console,
`.grid.csv` (4 608 arm-rows), `.matched.csv` (864 matched sites), `.phase.csv`, `.walkforward.csv`
committed beside it.  Runs in 142 s, deterministic.

## Corpus and the two tuned parameters
The queue names them and both are swept in full with every point reported.
**P1 cadence:** every *k* trading days at offset *p*, k ∈ {1, 5, 21, 63} (≈ D/W/M/Q) × up to 5
evenly spaced phases = **16 cadence variants**.  **P2 lambda:** idea 137's partial-rebalance dial,
verbatim ladder, **8 points**.  The full 16 × 8 cross is run on 3 panels × 2 books = **768
simulations**, read at 6 cost rungs off the exact rung identity = **4 608 arm-rows**.  Panels,
books and rungs are reported axes, never selected on.  The only selection is PROTOCOL rule 8.

**Phase is treated as a nuisance parameter, not a dial** — a calendar cadence like "last trading
day of the month" is one of ~21 possible monthly schedules, and the record has already flagged
this (2026-09-06 phase-averaged cadence).  Every cadence number here is reported phase-averaged
with its spread.

## Gates — all pass, before any new number was read
* **G1** the vectorised segment runner vs `engine.backtest` at **all four** calendar cadences on
  all three panels: max|dr| ≤ **6.4e-16**, max|dturnover| ≤ **1.6e-15**.
* **G2** the rung identity `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`:
  **6.4e-16 / 6.3e-16 / 6.1e-16**.
* **G3** the k-day cadence nests the calendar one where it must: k = 1 reproduces `freq='D'` at
  **0.000e+00** on all three panels.
* **G4** turnover monotone **down in k: 48/48** cells.  Monotone down in lambda: **87/96**, and
  the 9 exceptions are reported rather than hidden — all 9 are **EWALL** cells whose entire
  lambda turnover range is **0.0006–0.0008 x/yr** and whose largest wrong-way step is
  **1.66e-04 x/yr**.  Lambda is **inert** on those cells, not non-monotone in any usable sense —
  which is itself the run's first substantive finding (below).
* **Bonus check:** at the 36 sites where the two dials coincide (k=5/phase=0 *is* lambda=1) the
  interpolated match returns dSharpe **exactly 0.000000**, one per (panel, book, rung).

## FINDING 0 — lambda is not a turnover dial on the un-ranked book at all
Realised turnover reach at 0 bps, phase-averaged:

| panel | book | base (k=5, λ=1) | CADENCE reach | LAMBDA reach | overlap |
|---|---|---|---|---|---|
| u56 | EWALL | 0.81 | **0.24 – 1.78** x/yr | **0.81 – 0.81** | 0.81 – 0.81 |
| broad | EWALL | 0.85 | **0.25 – 1.84** | **0.84 – 0.85** | 0.84 – 0.85 |
| small | EWALL | 1.71 | **0.53 – 3.69** | **1.70 – 1.71** | 1.70 – 1.71 |
| u56 | TOP20 | 8.80 | **2.38 – 22.35** | 3.75 – 8.80 | 3.75 – 8.80 |
| broad | TOP20 | 12.86 | **3.40 – 31.43** | 5.22 – 12.86 | 5.22 – 12.86 |
| small | TOP20 | 16.01 | **4.25 – 38.15** | 6.71 – 16.01 | 6.71 – 16.01 |

On EWALL the whole lambda ladder from 1.00 to 0.06 moves turnover by **under 0.001 x/yr** — the
EWMA of an almost-constant weight matrix is the same almost-constant weight matrix — while cadence
spans a **7.4x** range.  On TOP20 lambda reaches down to only **43 %** of base turnover and can
never go up; cadence reaches **27 %** and **254 %**.  **Cadence is a strictly wider instrument on
every one of the six cells, and on three of them lambda has no instrument at all.**  This alone
answers the queue's adoption question before any performance number is read.

## H1 — the queue's PREMISE is refuted, and refuted backwards
The queue asserts "only lambda changes the book's path".  Measured as annualised tracking error
to the un-dialled base book, **at matched realised turnover**:

| | median TE | |
|---|---|---|
| **cadence** | **0.0188** | |
| **lambda** | **0.0009** | |
| median dTE (cad − lam) | **+0.0052** | |

**Cadence's tracking error is the larger one at 438 of 474 matched sites (92.4 %)**, and by a
median factor of ~20x.  By cell (median TE cadence vs lambda): u56/TOP20 0.0183 vs 0.0109,
broad/TOP20 0.0256 vs 0.0153, small/TOP20 0.0557 vs 0.0314, and on all three EWALL cells cadence
is 6–19x lambda (u56 0.0019 vs 0.0003, broad 0.0019 vs 0.0001, small 0.0035 vs 0.0004).  **Per unit of turnover
saved, it is CADENCE that moves the book's path, not lambda.**  The queue has the mechanism
exactly the wrong way round: lambda spreads the *same* trades over more days, while a slower
cadence holds *stale* weights for a quarter at a time.

## H2 — the head-to-head at matched turnover is a NULL
For every cadence arm (λ=1) the lambda curve (k=5, phase=0) is interpolated at the same realised
turnover, and vice versa.  Arms outside the other dial's range are **not extrapolated**: they are
counted and dropped.  **Bracketing: 474 of 864 matched sites (54.9 %)** — the honest limitation,
stated as idea 403 stated its own.

| direction | n | median dSharpe | cadence wins | median dCAGR | median dMaxDD |
|---|---|---|---|---|---|
| CAD→LAM (per rung, 31 each) | 186 | **0.0000** | 60/186 | 0.0000 | −0.0027 … 0.0000 |
| LAM→CAD (per rung, 48 each) | 288 | **+0.0005** | 201/288 | −0.0001 | +0.0010 |

**POOLED: cadence beats lambda on Sharpe in 261 of 474 bracketed sites (55.1 %), median dSharpe
+0.0003, median dCAGR −0.0081 %, median dMaxDD +0.0577 %.**  At PROTOCOL's own 10 bps rung:
44/79, median **+0.0003**.  Excluding the 36 self-matches: 261/438 (59.6 %), median **+0.0003**,
median |dSharpe| **0.0114**.  By cell the sign is not even stable — small/EWALL goes **0 of 54**
to cadence (median −0.0031) while small/TOP20 goes 60/108 (median +0.0138).

## THE RESOLUTION FINDING — the comparison is below its own noise floor
A cadence arm's Sharpe depends on which phase you happen to rebalance on.  Measured over the same
arms:

| k | mean SD across phases | max range | mean range |
|---|---|---|---|
| 5 (≈W) | 0.0117 | 0.0896 | 0.0303 |
| 21 (≈M) | 0.0176 | 0.1192 | 0.0450 |
| 63 (≈Q) | **0.0461** | **0.3796** | **0.1221** |

| | value |
|---|---|
| median \|dSharpe\| between the two dials at matched turnover | **0.0114** |
| median SD of the SAME cadence arm across its own phases | **0.0150** |
| **ratio effect / noise** | **0.760** |
| 90th pct \|dSharpe\| 0.0299 vs 90th pct phase SD | 0.0526 |

**The gap between the two dials is smaller than the spread of one of them across an arbitrary
choice of rebalance day.**  A quarterly arm's Sharpe moves by up to **0.38** purely on phase —
more than a thousand times the +0.0003 median gap the head-to-head produces.  Any published
cadence-vs-lambda verdict measured on a single phase is a verdict on the phase.

## H3 / Rule 8 (PROTOCOL 8) — the adoption question, chosen on 2009–2016, 2017–2026 read once
36 cells (3 panels × 2 books × 6 rungs) × 4 pre-registered menus.

| menu | median pick | OOS Sharpe | OOS CAGR | OOS MaxDD | beats SPY | beats RULES v2 | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|---|
| NONE (no dial) | k=5, λ=1 | 0.9262 | 13.58 % | −27.39 % | 22/36 | 14/36 | 0/36 | **0/36** |
| CADONLY | k=21, λ=1 | 0.9356 | 14.07 % | −27.58 % | 23/36 | 14/36 | 0/36 | **0/36** |
| LAMONLY | k=5, λ=0.25 | **0.9499** | 14.16 % | −27.62 % | 23/36 | 14/36 | 0/36 | **0/36** |
| JOINT | k=21, λ=0.70 | 0.9365 | 14.04 % | −27.78 % | 22/36 | 14/36 | 0/36 | **0/36** |

Head-to-head over the 36 cells:
* **CADONLY beats LAMONLY in 19/36 — a coin flip — median gap +0.0001.**
* CADONLY beats NONE in 19/36 (median +0.0062); **LAMONLY beats NONE in only 15/36 (median
  −0.0001)**, i.e. the lambda chooser is worse than not choosing.
* **JOINT beats both single dials in 2 of 36 cells** and is worse than the better single dial by a
  median **−0.0082** — spending the second parameter is a strict loss out of sample.

At 10 bps: u56 CADONLY 15.37 %/1.153/−22.7 % and LAMONLY 15.88 %/1.178/−22.2 % against SPY
15.32 %/0.876/−33.7 % and RULES v2 9.48 %/**1.279**/−12.1 %; broad CADONLY 14.97 %/1.007/−26.2 %
and LAMONLY 15.08 %/1.039/−25.9 % vs RULES v2 7.98 %/1.119/−12.2 %; small CADONLY
12.66 %/0.686/−33.6 % and LAMONLY 12.69 %/0.690/−34.0 % vs RULES v2 3.85 %/0.568/−14.7 %.

## The answer to the queue's question
**Neither.**  The record should adopt **neither dial as "the" turnover instrument**, and the
reasons are three, in decreasing order of force:
1. **Lambda is inert on the un-ranked book** (turnover range under 0.001 x/yr on all three EWALL
   cells).  An instrument that cannot move the quantity it targets on half the record's books is
   not a candidate.
2. **Where both dials do work, they are indistinguishable** — 55.1 % / median +0.0003 — and the
   difference sits at **0.76x the cadence dial's own phase noise**.
3. **Neither chooser earns its parameter** out of sample: LAMONLY loses to using no dial at all
   (15/36), CADONLY beats it in 19/36, and JOINT — the two-parameter version — is worse than the
   better single dial in 34 of 36 cells.

The queue's stated reason for preferring lambda ("only lambda changes the book's path") is not a
tiebreaker but a **reversed** fact: cadence perturbs the path ~20x more per unit of turnover
saved.  If the record wants a *path-preserving* turnover instrument, lambda is the right choice —
but on the books where it can actually move turnover at all, and it should be adopted for that
property, not for a performance edge, because there is none.

## KEEP paths (PROTOCOL 4, both evaluated on every arm-row)
**4a: 0 / 4 608.  4b: 0 / 4 608.  BOTH: 0 / 4 608 — at every rung from 0 to 50 bps and in every
one of the six (panel, book) cells.**  These are ungated, un-sleeved momentum and equal-weight
books whose MaxDD runs −22 % to −34 % against 4b's cap of 0.60 × SPY = **20.2 %**; the DD leg
fails everywhere and no turnover dial moves it (idea 527/531's reading of 4b as a DD-cap test,
seen again).  Nothing is promoted, no memo is filed.

## Predictions, scored
P1 **WRONG** — I predicted the queue's premise would survive (lambda moving the path more).  It is
refuted at 438/474 sites and by a factor of ~20.
P2 **RIGHT** — I predicted the head-to-head would be a null (55.1 %, median +0.0003).
P3 **RIGHT** — I predicted the joint chooser would lose to the single dials out of sample (2/36).
P4 **PARTLY RIGHT** — I predicted phase would matter; I did not predict it would be **larger than
the effect under test** (ratio 0.760).
P5 **WRONG** — I predicted lambda would have a usable reach on EWALL; it has essentially none.

## Caveats carried
* **SURVIVORSHIP (idea 54):** current constituents on all three panels; SMALL439 drops the 44
  `max_1d_move >= 1.0` tickers from `data/small_meta.csv` first (439 investable names, 2010→2026).
* **Both dials can only lower turnover from the daily book**, so the match is one-sided and its
  **54.9 % bracketing rate is reported, not assumed**; 390 of 864 matched sites are outside the
  other dial's range and are dropped rather than extrapolated through.
* A **k-day cadence is not a calendar cadence**; the two are bridged (G1/G3) and never conflated.
  The phase set is 5 evenly spaced offsets per k, not the full k, so the phase spreads here are
  **lower bounds** on the true nuisance.
* TE to the base book is one path statistic among several; it is chosen because it is the one the
  queue's premise is about, and it is reported at 0 bps so cost cannot drive it.
* MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
* Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
