# Idea 270 — is-S_CAGR-vs-S_SHARPE-a-general-selector-pair (lane B, 2026-09-09)

**Verdict: ANSWERED, and the queue's premise is REFUTED. The +CAGR/−Sharpe exchange rate is
NOT a constant — it is dial-specific, and the n dial is an outlier rather than a
representative. KILL of "switching the selection metric buys +2.5 pp/yr for −0.025 Sharpe"
as a general statement. No KEEP-candidate, no book promoted, no RULES change; RULES.md,
scan.py, bot.py and baseline.py untouched.**

Script: `research/backtests/2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B.py`
Outputs: `.grid.csv` (348 arms + 36 baseline rows), `.picks.csv` (180), `.xr.csv` (60 cells),
`.census.csv` (6,956 record menus), `.walkforward.csv`, `.console.txt`.
10 bps per unit turnover, weekly base cadence (the cadence dial is the treatment), next-day
execution, long only, no leverage. IS 2009-01-01..2016-12-31 chooses; OOS 2017-01-01+ read
once. **Tuned parameters: one** — the dial value inside a cell, chosen on IS only. Panel and
dial are enumerated reporting axes; every grid point is reported.
**Survivorship:** B136/BSTK100 are current constituents, SMALL439 a current screen; the eight
seeded sub-panels inherit that bias.

---

## GATE — idea 259's rule-8 n-dial result, reproduced before anything new was computed

Idea 259's four panels, its arms, its saturation cap (`sat_share ≤ 0.25`), its equal-weight
pooling.

| | published (259) | here |
|---|---|---|
| panels where S_CAGR ≠ S_SHARPE | 3 of 4 | **3 of 4** |
| S_CAGR − S_SHARPE, OOS Sharpe | −0.0254 | **−0.0242** |
| S_CAGR − S_SHARPE, OOS CAGR | +2.53 pp | **+2.56 pp** |
| OOS Sharpe EWALL / FWD20 / S_SHARPE / S_CAGR | 0.8577 / 0.8428 / 0.7815 / 0.7561 | **0.8571 / 0.8426 / 0.7813 / 0.7571** |

**GATE PASS.** Picks: U56 FWD20 vs FWD5, B136 FWD10 vs FWD5, BSTK100 FWD10 vs FWD5,
SMALL439 FWD20 vs FWD20 (the one agreement).

---

## LEG A — the same selector pair on five dials × twelve panels (60 cells, 348 arms, all reported)

Dials, each a one-dimensional family off the same EWall(G) base book:
`n` (FWD top-n, 259's own dial), `cadence` (D/W/M/Q), `gross` (0.25→1.00),
`volgate` (eligibility vol cap 0.30→1.00), `trim` (RULES-v2-form MA band 0.00→0.08).

### 1. The pair barely disagrees anywhere except on n

| dial | cells | disagree | rate |
|---|---|---|---|
| **n** | 12 | **7** | **58.3%** |
| trim | 12 | 2 | 16.7% |
| cadence | 12 | 1 | 8.3% |
| gross | 12 | 1 | 8.3% |
| volgate | 12 | 1 | 8.3% |
| **pooled** | 60 | **12** | **20.0%** |

On four of the five dials the two selectors pick the **same arm** in 11 or 10 cells of 12.
Idea 259's "they pick a different arm in 3 of 4 panels" is a property of the n dial, not of
the selector pair.

### 2. The exchange rate is dial-specific

S_CAGR minus S_SHARPE, OOS, read once:

| dial | dOOS Sharpe | t | dOOS CAGR (pp) | t | xr (pp per Sharpe pt) | free lunch | both worse |
|---|---|---|---|---|---|---|---|
| n | −0.0478 | −1.32 | **+1.6986** | **+3.16** | 35.50 | 3 | 0 |
| gross | −0.0004 | −1.00 | +0.4250 | +1.00 | 1058.05 | 0 | 0 |
| trim | −0.0047 | −1.41 | +0.0659 | +1.45 | 13.96 | 0 | 0 |
| volgate | −0.0083 | −1.00 | −0.1100 | −1.00 | −13.21 | 0 | 1 |
| cadence | −0.0070 | −1.00 | −0.1252 | −1.00 | −17.94 | 0 | 1 |
| **pooled (60 cells)** | **−0.0137** | −1.78 | **+0.39** | **+2.40** | **28.63** | 3 | 2 |

Idea 259's own figure on its four panels is **105.8 pp per Sharpe point**; pooled over all
five dials it is **28.63**, and two dials have the **wrong sign** (S_CAGR gives up CAGR *and*
Sharpe). Within the n dial alone the per-cell rate runs **1.71 → 42.30** — a 25× spread
inside the single dial the claim was made on.

**Permutation tests** (20,000 draws; the blocked version shuffles dial labels *within* each
panel, the exact null for this balanced 12×5 design):

| statistic | spread of per-dial means | unrestricted p | blocked p |
|---|---|---|---|
| dOOS CAGR (pp) | 1.8238 | 0.0010 | **0.0001** |
| dOOS Sharpe | 0.0474 | 0.2820 | 0.3081 |
| per-cell xr | 1075.98 | 0.0832 | 0.3317 |

The **denominator** of the exchange rate (what you give up in Sharpe) is consistent with one
constant across dials; the **numerator** (what you buy in CAGR) is emphatically not. That is
why the ratio is not a transferable number.

### 3. The sign is not reliable either

Of the 12 disagreeing cells: S_CAGR gains CAGR in 10, loses Sharpe in 9, and shows the
queue's **+CAGR/−Sharpe shape in only 7**. Three are a **free lunch** (S_CAGR better on both
— B136/n, BSTK100/n, S5_M120/n) and two are **both worse** (S0_B60/cadence, S5_M120/volgate).

### 4. Neither selector earns its keep (another idea-229 selection-loses instance)

Mean over the 60 cells:

| | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| DONOTHING (the dial's base arm) | 0.7580 | 7.91% | −27.1% |
| S_SHARPE | 0.7618 | 8.95% | −28.6% |
| S_CAGR | 0.7482 | 9.34% | −29.5% |
| SPY (per-panel mean) | **0.8817** | **15.44%** | −33.7% |
| RULES v2 (live) | **0.9196** | 7.01% | **−14.4%** |

S_SHARPE − DONOTHING **+0.0038 (t +0.31, wins 27/60)**; S_CAGR − DONOTHING **−0.0098
(t −0.73, 25/60)**. Both selectors sit **below SPY and below the live book on OOS Sharpe in
the mean**. The dial-choosing exercise is a coin flip whichever metric you choose it with.

### 5. Both KEEP paths, every grid point

| dial | arms | 4a vs LIVE RULES v2 | 4a vs superseded v1 | 4b |
|---|---|---|---|---|
| cadence | 48 | 0 | 6 | 3 |
| gross | 72 | 0 | 24 | 3 |
| n | 84 | 0 | 11 | 6 |
| trim | 72 | **8** | 44 | 0 |
| volgate | 72 | 0 | 22 | 10 |
| **all** | **348** | **8** | **107** | **22** |

**The 4a and 4b sets do not intersect** (the 8 4a passers are all `trim` arms that fail 4b on
CAGR; the 22 4b passers all fail 4a). 4a against the superseded v1 is **13× the live-book
count** — a further reproduction of idea 482 on a fresh grid. Among the 120 **selected** arms:
4a 3, 4b 5, against **4 of 60 for do-nothing** — selection does not raise the pass rate. All
five 4b-passing picks are already-known rows (U56 FWD20 = idea 2's construction; U56/B136
`V1.00` is the plain above-MA equal-weight book with the vol gate switched off).
**No new KEEP-candidate; no memo written.**

---

## LEG B — the queue's literal ask: the record's own committed grids

2,162 committed CSVs scanned (0 unreadable, 1 skipped over 200,000 rows). **73 files** carry
`IS_Sharpe`, `IS_CAGR`, `OOS_Sharpe`, `OOS_CAGR` and a sweepable dial once idea 241's bar on
replication and reporting axes (seed, draw, rung, phase, fold, cost_bps, panel, book, arm, …)
is applied → **6,956 menus**.

| family | menus | files | disagree rate | dOOS Sharpe | dOOS CAGR (pp) | xr |
|---|---|---|---|---|---|---|
| n | 1,187 | 13 | 44.8% | −0.0316 | +0.9327 | 29.51 |
| trim | 153 | 4 | 44.4% | −0.0537 | +1.5825 | 29.46 |
| gross | 1,523 | 14 | 14.3% | −0.0056 | +0.9676 | 173.40 |
| cadence | 294 | 5 | 9.9% | −0.0075 | −0.0149 | −1.99 |
| other | 3,799 | 45 | 22.8% | −0.0064 | +0.5366 | 83.45 |

Menu-pooled: dOOS Sharpe **−0.0116 (t −13.34)**, dOOS CAGR **+0.70 pp (t +25.09)**, xr 60.06.
Those t's are inflated — one file contributes 1,028 menus. **File-clustered over the 73
files: dOOS Sharpe −0.0162 (t −3.07, negative in 36/73), dOOS CAGR +0.63 pp (t +5.07,
positive in 52/73), xr 38.74**, mean per-file agreement rate 0.735.

The census **corroborates the sign and the magnitude** of Leg A's pooled figure (record
+0.63 pp / −0.0162 vs the controlled grid +0.39 pp / −0.0137) and **reproduces the ordering**
that the n and trim dials disagree most (44.8% / 44.4%) while cadence disagrees least (9.9%).
It **cannot resolve dial-specificity**: family heterogeneity is p < 0.0001 menu-pooled but
**p = 0.2757 (CAGR) / 0.3114 (Sharpe) once clustered on file**, i.e. the apparent effect in
the corpus is between-file variation, not between-dial. Only the controlled 12×5 grid, where
every dial is measured on every panel, answers the question — and it answers it p = 0.0001.

**Caveat, stated rather than buried:** record menus are heterogeneous in construction, cost
rung, sample and universe; `other` is 3,799 of 6,956 menus (commonest dial columns `fin`,
`est`, `level`, `val`, `rate`). Leg B is a corpus check on Leg A's sign and spread, not a
controlled experiment.

---

## What this changes

1. **Do not quote "+2.53 pp/yr for −0.0254 Sharpe" as an exchange rate.** It is one dial's
   number on four panels; the same pair on the other four dials moves CAGR by −0.13 to
   +0.43 pp and reaches the wrong sign twice.
2. **The reportable invariant is the denominator, not the ratio.** Choosing on CAGR costs
   about −0.014 of OOS Sharpe wherever you do it (p = 0.31 for one constant). What it buys
   depends entirely on the dial.
3. **Selection still loses.** Neither selector beats the dial's own base arm (t +0.31 /
   −0.73), and neither beats SPY or the live book on mean OOS Sharpe.

No RULES change. `RULES.md`, `products/scan.py`, `products/bot/bot.py` and
`research/baseline.py` were not modified.
