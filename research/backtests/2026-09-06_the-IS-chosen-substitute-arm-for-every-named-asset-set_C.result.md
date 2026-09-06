# idea 212 — the IS-chosen-substitute arm for every named asset set (lane C, 2026-09-06)

**VERDICT: KILL — 0 of 8 published named-asset-set separations survive being CHOSEN rather than
GIVEN.** No book proposed, no KEEP candidate; RULES.md, scan.py, bot.py, baseline.py untouched.
Idea 190's single instance (TLT/GLD/UUP) is reproduced to 2.2e-16 and generalises to every other
human-chosen asset set in the record.

## What was asked and what was run
The queue asked for a census of the LEADERBOARD for instruments whose ASSET IDENTITIES were
human-chosen, and for idea 190's decisive arm (S5, IS-chosen substitute) on each.

**Census** (computed, not asserted — ticker literals in `research/backtests/*.py`, mapped to the
LEADERBOARD rows produced by the scripts that hard-code them; the running script excludes itself):

| set | k | scripts | LB rows |
|---|---|---|---|
| TLT+GLD+DBC+UUP (S4) | 4 | 15 | 222 |
| TLT+GLD+UUP (S3) | 3 | 15 | 145 |
| BTC-USD+ETH-USD | 2 | 11 | 454 |
| TLT+GLD+SHY (defensive) | 3 | 1 | 140 |
| GLD+DBC+UUP · TLT+DBC+UUP · TLT+GLD+DBC (S4 leave-one-outs) | 3 | 1 each | 28 each |
| SPY+TLT+GLD (risk parity) | 3 | 1 | 28 |
| SPY+EFA+EEM+TLT+GLD+DBC (dual momentum classes) | 6 | 1 | 8 |

9 distinct sets, 1081 LEADERBOARD rows. **The idea's own example "GDX/SLV pairs" does not exist in
the record** — no committed script hard-codes it; the census is the answer to that hypothesis.
BTC-USD+ETH-USD (454 rows) is censused but NOT run, reason stated: `baseline.EXCLUDE` drops both
from every cached panel, so its substitution population is empty — there is no second crypto
instrument to be chosen instead. **8 sets carrying 627 LEADERBOARD rows were run.**

**Arm.** Idea 134's committed static-sleeve construction, imported not re-typed: `(1-f)·R_n +
f·sleeve(members)` rescaled to gross 0.75, weekly, t+1. Substitution population per set = idea
190's 12-member DIV pool ∪ the set's own members, minus its members, **enumerated whole, no draws,
no seed**: C(9,3)=84 / C(8,4)=70 / C(10,3)=120 / C(9,6)=84. Two tuned parameters only, both fitted
in sample: sleeve share f ∈ {0.10, 0.20, 0.50} and the substitute asset set. Carried axes, never
selected on, every level reported: named set, panel {u56, broad136}, base n {10, 20, 40}, cost
{10, 25} bps → **96 walk-forward cells, 25,320 grid rows** (all in `.grid.csv.gz`).

## Reproduction (asserted before any new number was read)
* [a] vectorised `run()` vs `engine.backtest` on the evaluated sample: max|dret| 1.388e-17,
  max|dturn| 3.331e-16 — PASS. (The engine emits 2 NaN returns in the pre-warm-up head; excluded
  and stated, not hidden.)
* [b] cost identity, 0 bps + turnover → 10 bps vs a genuine 10 bps engine run: 0.000e+00 — PASS.
* [c] numpy sleeve == idea 134's `sleeve_weights` for every named set, both panels: max|d| 0.0.
* [d] **idea 190's committed walk-forward rebuilt from this run's own grid**: S0 in 12/12 cells
  (max|d| 2.220e-16) and 190's S1 pick — an argmax over BOTH S3 and S4 and 3 f's — recovered in
  12/12 cells (OOS Sharpe max|d| 2.220e-16).

## Rule-8 walk-forward (params ≤2016-12-31, 2017–2026 read once), 96 cells
d1 = OOS Sharpe(assets GIVEN) − do-nothing; d5 = OOS Sharpe(assets CHOSEN) − do-nothing.

| set | LB rows | d1 mean (t) | d1 win | d5 mean (t) | d5 win | d5−d1 (t) | survives |
|---|---|---|---|---|---|---|---|
| TLT+GLD+DBC+UUP | 222 | **+0.0914** (+7.69) | 12/12 | **−0.2507** (−16.52) | 0/12 | −0.3421 (−20.73) | NO |
| TLT+GLD+UUP | 145 | **+0.0699** (+6.85) | 12/12 | **−0.2509** (−17.29) | 0/12 | −0.3208 (−19.09) | NO |
| TLT+GLD+SHY | 140 | −0.0703 (−4.95) | 0/12 | −0.2144 (−10.70) | 0/12 | −0.1441 (−4.72) | NO |
| GLD+DBC+UUP | 28 | +0.0670 (+4.41) | 12/12 | −0.2423 (−16.35) | 0/12 | −0.3094 (−17.82) | NO |
| SPY+TLT+GLD | 28 | +0.0319 (+2.79) | 9/12 | −0.2144 (−10.70) | 0/12 | −0.2463 (−11.04) | NO |
| TLT+DBC+UUP | 28 | +0.0362 (+4.71) | 12/12 | −0.2244 (−8.69) | 0/12 | −0.2606 (−11.02) | NO |
| TLT+GLD+DBC | 28 | +0.0475 (+4.84) | 12/12 | −0.2144 (−10.70) | 0/12 | −0.2619 (−13.44) | NO |
| SPY+EFA+EEM+TLT+GLD+DBC | 8 | +0.0042 (+1.45) | 9/12 | −0.1242 (−12.84) | 0/12 | −0.1283 (−15.79) | NO |

* separations that REPRODUCE with the assets GIVEN: **7 of 8** (TLT+GLD+SHY is the exception — the
  defensive sleeve loses to do-nothing even when handed over).
* separations that SURVIVE being CHOSEN: **0 of 8; 0 of 96 cells has d5 > 0** (d5 range
  −0.3445 … −0.0603).
* pooled: d1 **+0.0347** (t +5.69, 78/96) · d5 **−0.2170** (t −29.72, 0/96) · d5−d1 **−0.2517**
  (t −24.61, negative in 94/96).
* the population MEAN substitute is −0.0967 vs do-nothing and the cash carve-out is −0.0025, so the
  IS-CHOOSER is worse than picking at random from the same pool by 0.12 of Sharpe: this is a
  selector failure, not a pool failure.

**OOS levels, mean over the 96 cells:** S0 do-nothing 0.9805 / 14.75% / −24.28% · S1 assets GIVEN
1.0152 / 11.20% / −17.52% · **S5 assets CHOSEN 0.7635 / 7.19% / −17.06%** · population mean 0.8838 ·
cash carve-out 0.9780 / 9.58% / −16.19% · **RULES v1 0.4695 / 4.64% / −18.98%** · **SPY 0.8820 /
15.45% / −33.72%**. OOS-window 4b: S0 0/96, S1 23/96, **S5 0/96**, cash 12/96.

**What the chooser picks:** IEF in **96/96** cells and LQD in **96/96** — IEF+LQD+SLV ×28,
IEF+LQD+UNG ×23, IEF+LQD+TLT ×12. The IS-Sharpe rule buys the lowest-vol credit/duration pair
available and is punished for it out of sample, whatever named set it is substituting for.

## Both KEEP paths, full sample, all 25,320 grid rows
| arm | rows | 4a | 4b | 4b on OOS window |
|---|---|---|---|---|
| REAL (named sets) | 288 | 139 (48.3%) | **82 (28.5%)** | 77 (26.7%) |
| SUB (substitutes) | 24,984 | 10,582 (42.4%) | **4,561 (18.3%)** | 4,330 (17.3%) |
| S0 do-nothing | 12 | 3 | 0 | 0 |
| CASH carve-out | 36 | 19 | 8 | 7 |

The named sets do sit above their own populations ex post (28.5% vs 18.3% 4b) — **and that is
exactly the gap the project's own selector cannot reach**: given the same twelve instruments the
human was given, IS-Sharpe lands on a set that fails 4b in 96/96 OOS cells. Binding 4b bar: DD then
CAGR for REAL rows; a Sharpe bar plus CAGR (H2,OOS,CAGR ×29; H1,H2,OOS,CAGR ×28) for S5 rows.

## Scoreboard vs the pre-registered predictions
P1 HOLDS ([a]–[d] all pass) · P2 HOLDS (9 censused ≤ 10, family-concentrated) · **P3 FAILS 7/8**
(TLT+GLD+SHY does not separate even when given) · **P4 HOLDS 0/8 survive** · P5 HOLDS (97.9%) ·
**P6 FAILS** (CAGR appears in only 45.8% of S1 OOS-4b failure lists; DD binds as often).

## Product (proposed, NOT committed — PROTOCOL changes are a Sunday-review matter)
Proposed PROTOCOL clause **11e**: *any result whose instrument identities were chosen by a human
must publish the IS-chosen-substitute arm beside it — the same construction with the assets picked
by the project's own IS selector from a stated, enumerated pool. A separation that exists only
when the assets are handed over is a hindsight statistic and may not be called an edge.* On this
record that clause retires the asset-selection reading of **627 LEADERBOARD rows** across 8 named
sets: what survives is the ASSET-CLASS reading (a de-grossing carve-out into low-beta instruments,
which the cash control reproduces at −0.0025 of Sharpe), not the identities.

## Caveats carried
* SURVIVORSHIP: u56 and broad136 are current-constituent lists (idea 54); real and substitute arms
  inherit it identically, so the comparison is unaffected, the levels are not.
* The DIV pool is a survivor list of instruments this project has always used. The enumeration is
  exact for that pool and says nothing about assets outside it — and the pool is the concession
  made to the named sets: the chooser gets the human's own twelve instruments and still loses.
* The census sees only identities that reached a committed script, and attributes a script's
  LEADERBOARD rows to every set it hard-codes, so 627 is a count of rows-touched, not of distinct
  claims. It is a floor on exposure, not a ceiling.
* Crypto (454 rows) is untested here for a data reason, not a methodological one.
* Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.

Files: `.py`, `.console.txt`, `.census.csv`, `.grid.csv.gz` (25,320 rows), `.keep.csv.gz`,
`.walkforward.csv` (96 cells). Deterministic, no seed anywhere.
