# Idea 382 — two same-day runs disagree on D3 for path-dependent arms

**Verdict: KILL of the filed premise on all three of its factual claims, and the real defect
located and named.** Lane B, 2026-09-07. Script
`2026-09-07_two-same-day-runs-disagree-on-D3_B.py`, console
`.console.txt`, 480-draw stream `.draws.csv.gz`.

## The premise was wrong three times over

| filed claim | check | result |
|---|---|---|
| P1 the two runs "share seed" | read `NDRAW, DROP_FRACS, TAUS, SEED` out of both committed scripts | **REFUTED** — `_B` uses `SEED=20260907`, `_B2` uses `SEED=20260905` (idea 122's). `NDRAW=40` and `DROP_FRACS=(0.05,0.10,0.20)` do match. |
| P2 "agree to the last digit on every GATE arm" | diff the two committed `d3.csv` | **REFUTED** — stateless arms differ on **167 of 420** rows, max **0.3500** |
| P3 "differs by exactly 0.025 (one draw of forty)" | same diff, the three named arms | **REFUTED** — those arms differ on 77 of 126 rows, spread 0.0000–**0.5750** (23 draws of 40, not one). Corpus-wide: `frac_pos_full` differs on **255/672** rows (max 0.5750), `frac_pos_IS` on **430/672** (max **1.0000**). |

The one claim that *is* true is the reproduction gate: `_B2` reproduces idea 122's committed
`d3.csv` at **0.000e+00** on all 192 shared rows and `_B` does not (max 0.35). That is
because `_B2` deliberately replays idea 122's seed and `_B` chose a new one — both legal
under the protocol as written, which is exactly why the record carries two numbers.

The normalised bootstrap pricing loops of `_B` and `_B2` are **identical** token for token,
and both scripts' `targets()` reproduce idea 94's books at 0.000e+00. There is no cost
accrual, column-order or pending-exit difference to find: the queue's three suggested
causes are all absent.

## What is actually going on

Pre-registered discrimination (H0 path-dependence defect vs H1 draw noise), decided by a
per-cell calibration: 480 independent sub-panel draws cut into 12 disjoint blocks of 40,
giving each (book, arm) cell its own null distribution of block-to-block `frac_pos` gaps —
so an arm's own noise amplification is already inside its null.

* **H_amp (descriptive, and the trap the queue fell into):** draw noise *is* larger on
  stateful arms — replicate SD 0.0328 vs 0.0055 at N=40, permutation p 0.0046, significant
  at **all four** N in {10,20,40,80}. A state machine amplifies panel composition. So
  "stateful arms disagree more" is what *pure re-drawing* looks like and is not evidence of
  a defect.
* **H0 NOT RETAINED / H1 sufficient on average:** mean cell percentile of the observed gap
  inside its own null is **0.5192 all cells (p 0.271)**, **0.5574 stateful only (p 0.214)**,
  0.4962 stateless (p 0.629). Nothing exceeds noise.
* **The sharper finding — irreproducibility is a PRICEABILITY defect, not a state defect.**
  Of 32 cells, the **23** whose denominator clears idea 94's own floor (|dMaxDD| > 0.10 pp)
  on every one of 480 draws have observed `_B` vs `_B2` gap **0.000000, max 0.000000** —
  the two runs agree exactly, seed difference and state machine notwithstanding. All 9
  disagreeing cells have sub-floor draws (mean gap 0.1028, max 0.4250).
  **spearman(fraction of sub-floor draws, replicate SD) = +0.9555.**
* The single Bonferroni-significant cell (TOPALL/ebud-0.20, z 3.93, p_bonf 0.0027) is a
  **non-instrument**: over 480 draws its |dMaxDD| never exceeds **6.66e-14** and is exactly
  zero in 94 of them. `frac_pos` there is the sign of an identically-zero quantity — float
  dust printed as a fraction. Not a defect and not draw noise: an undefined statistic.

## What it costs the record, and what fixes it

At the record's own setting (N=40, tau=0.90) **2 of 32 cells (6.2%)** get a different
admissibility verdict from the seed alone; P(two runs disagree) = 0.010. Across the full
N x tau grid the unstable share runs 0.0%–12.5%, worst at small N and tau=1.00.

Flooring the D3 draws with idea 94's existing floor is necessary but **not sufficient**:
it correctly returns NO PRICE for 3 cells and cuts mean replicate SD 33.2%
(0.00904 -> 0.00604), but 6 cells still move with the seed (max SD 0.0593) — real sampling
variance, not a bug. Buying it away is expensive: c/sqrt(N) fits give N=18 for ±0.025 on
`frac_pos_full` but **N=120** for `frac_pos_IS`, and the max-SD cell needs N≈224.

**Amendment proposed (two clauses, neither a RULES change):**
1. The D3 fraction must be computed only over draws clearing the same |dMaxDD| > 0.10 pp
   floor the record already uses to decide publication, and reported as **NO PRICE** when
   no draw qualifies. This removes every cell where the number is undefined, including the
   0.425 disagreement that prompted this idea.
2. The D3 seed must be a **PROTOCOL constant committed with the draw index**, not a
   per-script choice. `_B` and `_B2` were both compliant; the protocol, not either script,
   is what let the record carry two numbers.

## Rule 8 walk-forward (required)

Parameters (N, tau) chosen on 2009–2016 only; 2017–2026 untouched. Selector: among cells
clearing tau on the IS-window D3 fraction, take the best IS Sharpe. OOS bars — SPY
15.45%/0.882/-33.72%, RULES v2 9.53%/**1.285**/-12.05%. All 16 grid points reported in
`.walkforward_agg.csv`.

At N=40/tau=0.90: **2 distinct picks over 12 seeds** (modal 67%), OOS Sharpe
**1.175 ± 0.036** (range 1.126–1.199), **beats SPY 100%** of seeds, **beats RULES v2 0%**.
Selection stabilises with N (1 distinct pick at N=40 and 80 with tau=0.80) and destabilises
with tau (7 distinct picks at N=10, tau≥0.95). The best OOS cell anywhere on the grid,
N=40/tau=1.00 (OOS 1.278, beats v2 92%), is TOPALL/band3-dg.

## KEEP paths — all 34 cells priced, @10 bps

**4a 1/34, 4b 14/34.** The single 4a pass is TOPALL/band3-dg (8.72%/1.2088/-12.05%, halves
1.2306/1.1924, OOS 1.2863) — this is the live RULES v2 under a different name-count
denominator (v2: 8.66%/1.2056/-12.05%, halves 1.2259/1.1908), the same non-object idea 124
already reported; it fails 4b on the CAGR floor. All 14 4b passers are re-measurements of
arms already in the record. **No KEEP-candidate, no new object, no RULES change proposed.**

Full grid in `.keeppaths.csv`; per-cell forensics in `.cell_ztest.csv`,
`.calibration_cells.csv`, `.floored_convention.csv`.
