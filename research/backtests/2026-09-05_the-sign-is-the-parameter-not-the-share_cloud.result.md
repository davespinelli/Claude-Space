# Idea 168 — the-sign-is-the-parameter-not-the-share (cloud, 2026-09-05)

**Verdict: PARK, with one hard negative result about the live rules.**
RULES v1's volatility scaler is on the **wrong side of zero**, not merely unnecessary. Across
352 books (2 large-cap panels x 11 exponents x 8 book shares x 2 cost rungs) the live
`k = -0.5` loses to the no-scaler control on Sharpe in **32 of 32** (panel, cost, share) cells
and its signed dCAGR is negative in **16 of 16** cells at 10 bps. No new 4b KEEP survives rule 8.

## What was run
Family `s_k = composite x vol20^k`; `k = -0.5` is RULES v1 (`comp / sqrt(vol20)`), `k = 0` the
no-scaler control, `k = +0.5` idea 159's POS. Weekly, t+1, `norm` construction at gross 0.75.
Two tuned parameters, both swept exhaustively and all 352 grid points published in `.grid.csv`
and `.curve.csv`: the exponent k (11 values, idea 168's five a strict subset) and the book
share m (8 values; m = 1.00 dropped a priori under idea 153's confound (i)). Panel and cost
rung are carried corpus axes, never selected on.

## Reproduction gate (asserted before any new number)
* **[a] EXACT.** k in {-0.5, 0, +0.5} reproduce idea 159's committed INV/NONE/POS books
  cell-for-cell over 48 shared cells: max|diff| CAGR 9.7e-17, Sharpe 2.2e-16, MaxDD 8.3e-17,
  H1/H2 2.2e-16. (The float route at k = +-0.5 is pinned to idea 159's own — `x**-0.5` and
  `1/(x**0.5)` differ by one ulp, which flipped a rank tie in 2 of 48 cells before pinning,
  worth 0.0125pp of CAGR at the 2-name book. Same mathematical function, pinned arithmetic.)
* **[b] PREMISE HOLDS.** Live `k = -0.50`: signed dCAGR negative 16/16. `k = +0.50`: positive
  15/16. Idea 159's 20-of-20 / 19-of-20 signs reproduce on the 16 shared points.

## The curve (all grid points in `.curve.csv`)
Signed dCAGR vs the k = 0 control is **monotone increasing in k** over essentially the whole
grid on both panels and both cost rungs. Examples at 10 bps (pp/yr):

| panel | share (n) | k=-1.00 | k=-0.50 (live) | k=0 | k=+0.50 | k=+1.00 |
|---|---|---|---|---|---|---|
| u56 | 0.27 (10) | -6.94 | -4.01 | 0.00 | +3.82 | +4.67 |
| u56 | 0.53 (20) | -4.95 | -2.72 | 0.00 | +0.56 | +0.92 |
| broad | 0.05 (5) | -12.89 | -10.27 | 0.00 | +5.79 | +6.87 |
| broad | 0.53 (48) | -3.13 | -2.07 | 0.00 | +0.31 | +0.49 |

* Grid argmax at the **+1.00 endpoint in 19 of 32 cells**, interior in 13, at -1.00 in **0**.
  Median grid argmax k* = **+1.00**; median Sharpe-argmax k* = **+0.75**.
* The **positive zero-crossing k0+ does not exist in 26 of 32 cells** — the curve does not come
  back down inside |k| <= 1. Idea 168's headline quantity is unbounded above on this grid and is
  reported as such rather than extrapolated. **P3 confirmed.**
* **P4 REFUTED.** The exponent is the LARGER dial, not a second-order one: Sharpe range across
  the 11 exponents at fixed share (mean 0.29-0.61 by cell) exceeds the range across the 8 shares
  at fixed k (mean 0.21-0.48) in **4 of 4** (panel, cost) cells.

## KEEP paths (both evaluated, all 352 books)
4a: 129/352. 4b: **47/352, every one of them at 10 bps — 0 of 176 at 25 bps.** No 4b pass at any
k <= -0.50; the passing band runs k in [-0.25, +1.00] at shares 0.20-0.75, i.e. a **plateau, not
a point**. Best single book: u56, k = +0.75, m = 0.27 (n = 10) — CAGR 17.25%, Sharpe 1.0931,
MaxDD -20.22%, halves 1.0198 / 1.1621, OOS Sharpe 1.1765, against SPY 15.23% / 0.889 / -33.72%,
halves 0.957 / 0.834, OOS 0.882.

## Rule 8 walk-forward (chosen on 2009-2016, read ONCE on 2017-2026)
Mean over the 4 (panel x cost) cells; SPY OOS 15.45% / 0.8820 / -33.72%:

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | vs A_ZERO on Sharpe |
|---|---|---|---|---|
| A_ISK (k chosen on IS) | 17.92% | 0.9144 | -25.32% | **+0.084, wins 4/4** |
| A_ISKS (k and share on IS) | 16.10% | 0.8453 | -23.94% | +0.015, wins 2/4 |
| A_ZERO (k = 0 fixed) | 14.75% | 0.8305 | -23.16% | — |
| A_LIVE (k = -0.5 fixed) | 5.34% | 0.5319 | -17.31% | **-0.299, wins 0/4** |

RULES v1 OOS on the same cells: 7.73% / 0.7471 (u56@10), 3.78% / 0.3992 (u56@25),
5.94% / 0.5763 (broad@10), 1.11% / 0.1554 (broad@25).

**The dial is real out of sample** — the IS-chosen exponent beats both fixed exponents in every
cell — but **A_ISK fails the OOS-window 4b bars in 4 of 4 cells** (the drawdown cap in three,
H1 in the fourth). Under PROTOCOL rule 8 that is PARK, not KEEP.

## Why PARK and not KEEP
The full-sample 4b passes are real but they are the corpus's existing books re-labelled, and the
one arm that actually chooses k prospectively cannot clear 4b on the untouched window. The
result that *does* stand on its own is the sign: five prior findings compared three points and
concluded "delete the scaler"; sweeping the dial says the optimum is not at 0 but past +0.5, and
the live -0.5 is the worst point on the whole grid at every share tested.

## Reconciliation with lane B's independent concurrent run of the same idea
Lane B ran idea 168 in parallel (`2026-09-05_..._B`-family, 162 books: a 9-point k ladder x 3
shares x 2 constructions x 3 panels). **The two runs agree on every shared dimension** and were
written without sight of each other:

| claim | this run (352 books, 2 panels) | lane B (162 books, 3 panels) |
|---|---|---|
| curve shape in k | monotone increasing, argmax at +1.00 endpoint 19/32 | Spearman(k, dCAGR) +0.93..+1.00 in 12/12; argmax k >= +0.50 in 12/12 |
| live k = -0.5 | loses to k=0 on Sharpe 32/32 | passes 4b in 1/12; worst arm out of sample (0.838) |
| lowest 4b-passing k | -0.25 | -0.25 in 8/12 large-cap cells |
| 25 bps | 0 of 176 books pass 4b | nothing passes 4b at 25 bps |
| small panel | not run (idea 168 says large-cap only) | every sign reverses, 18/18 |

**Where they differ, lane B's number is the better-powered one and should be preferred.** On
whether an IS-fitted exponent beats the k = 0 constant out of sample, this run's A_ISK wins 4/4
across only **4** (panel, cost) cells, while lane B's S_IS wins **18 of 36** — a coin flip, and
the fifth such coin flip after ideas 110/151/132/166. Four cells cannot distinguish a real
selector edge from noise; the honest reading of the two together is that **the exponent's
direction is a robust finding and the IS selection of it is not.** That reinforces the PARK
verdict rather than weakening it.

## Caveats (carried, not buried)
* **SURVIVORSHIP is the main threat to the positive-k finding and cuts exactly the wrong way.**
  Both panels are current-constituent lists (idea 54). Tilting toward high vol is precisely the
  instrument survivorship flatters: the high-vol names that blew up and left the index are
  absent, so every k > 0 book is measured without its worst would-be constituents. The whole
  positive half of this curve is an **upper bound** and must not be read as a live instruction to
  invert the scaler. The negative half — that k = -0.5 loses to k = 0 — is *not* exposed this
  way, because it compares two books drawn from the same surviving panel.
* Nothing here clears 4b at 25 bps, on any panel, at any exponent or share.
* dCAGR is a full-sample difference of compounded numbers; dSharpe and dMaxDD are published
  beside it in `.curve.csv` so no one statistic carries the verdict.
* vol20 floored at 0.08 before exponentiation (idea 81's convention, carried verbatim).
* Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.

Artefacts: `.console.txt`, `.grid.csv`, `.curve.csv`, `.crossing.csv`, `.walkforward.csv`,
`.repro.csv`.
