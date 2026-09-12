# Idea 576 — price-the-ZERO-CASH-convention-on-the-gross-LADDER (lane B, 2026-09-12)

**ANSWERED = NO, THE +0.0065 IS NOT THE ZERO-CASH CONVENTION — and crediting cash does not
flatten the ladder, it re-prices PROTOCOL 4b.** KILL of the premise; PARK of the two books the
credit creates.

**INDEPENDENT REPLICATION.** The cloud lane ran this same idea concurrently and committed first
(`2026-09-12_price-the-ZERO-CASH-convention-on-the-gross-LADDER_cloud.py`). The two runs were
written without sight of each other and agree: median slope **+0.00602 → −0.344 / −0.683 (cloud
−0.341 / −0.683)**, break-even **c\* 1.9 bps (cloud 2.6)**, the same single BOTH book (U56 TOP20
monthly g=0.40 at 300 bps), the same rule-8 WF-B pick (**MA-DG g=1.00**, 11.35% / 1.186 vs cloud
11.34% / 1.1844), the same panel ordering and the same PARK. Residual differences are convention,
not method: this run reads all 51 tuned points as OLS slopes over the full 17-point grid and adds
the excess-Sharpe leg (H_EXCESS), which the cloud run does not carry.

Script `research/backtests/2026-09-12_price-the-ZERO-CASH-convention-on-the-gross-LADDER_B.py`.
6 unlevered forms x 3 panels x 2 cadences x 17 grosses x **3 cash rates (0 / 150 / 300 bps)** =
**1,836 books, every one written to `.grid.csv`** and none dropped from a headline. Two tuned
parameters: cash rate and gross. 10 bps costs, t+1 fills, no leverage, panels cut 2026-09-04.

## Gates (all PASS)

| gate | what | result |
|---|---|---|
| G1 | this runner vs idea 311's **committed script** on today's panels, 108 book-points | **0.000e+00** on weights AND returns |
| G2 | `fast_backtest(cash=0)` vs `engine.backtest` (cached and uncached paths) | **2.776e-17** |
| G3 | a zero-weight book earns exactly `c/1e4/252`, every day, at every c | **0.000e+00**; CAGR 1.5113% / 3.0453% = compounded target |
| G4 | EWall at g=1.00 (no cash leg) is invariant in c over the scored sample | **1.388e-17** |

**DATA DRIFT (reported, not asserted).** Idea 311's committed `.grid.csv` was produced on caches
this repository no longer holds. Today's small-cap screen carries **663** tradable names, not the
**439** idea 311 ran, so **204 of its 612 rows have no counterpart at all**. Of the 408 that do,
`max |d|` is **1.30e-02** (B136) and **9.33e-03** (U56), both on `turnover`; Sharpe 1.56e-03 /
1.01e-03. Since this run's code is bit-identical to idea 311's, that residual is data, not method
— and a committed grid whose panel has silently changed identity is idea 565's problem arriving
in a **price** cache.

## A — the slope. The credit does not flatten it; it inverts it, 100x over

| statistic (36 cells) | c = 0 | c = 150 | c = 300 |
|---|---|---|---|
| median Sharpe-vs-g slope | **+0.00602** | −0.34395 | −0.69344 |
| median \|slope\| | **0.00662** | 0.34395 | 0.69344 |
| cells with slope > 0 | 32/36 | 0/36 | **0/36** |
| median Sharpe span over the 17 grosses | **0.00529** | — | **0.67922** |

- **H_FLAT FAIL.** |slope| does not shrink: it grows **52x** at 150 bps and **105x** at 300 bps.
  A credited ladder is 128x past idea 51's 0.0100 invariance bar; a zero-cash one sits inside it.
- **H_SIGN PASS**, 36/36 negative at 300 bps — the algebra's `((1-g)/g)·c/sigma` term, not a flattening.
- **The implied break-even rate is ~2 bps.** Interpolating each cell's slope linearly in c, the
  rate that would zero it has median **c\* = 1.9 bps** (IQR 0.5–5.7, range −3.8 to 34.2, 32/36
  inside [0, 300]). The drift idea 576 set out to explain is worth about **two basis points** of
  cash yield. No plausible cash rate explains it.
- **H_EXCESS PASS, 36/36 at both rates.** Read coherently — Sharpe's own risk-free rate set to the
  same c for the book *and* for SPY — the slope is invariant in c: median |xslope(c) − xslope(0)|
  **0.00064** (150) and **0.00128** (300), max **0.00548**, every cell inside idea 51's 0.0100 bar.
  The median excess slope stays **+0.00602 → +0.00691 → +0.00709**. **The +0.0065 survives the
  credit untouched**, so it is a path/compounding-and-cost artefact of a drifting book, not cash.
  Everything H_FLAT and H_SIGN see is the artefact of scoring a cash-credited book against a
  **zero** risk-free rate — which is exactly what `engine.metrics` does.

## B — the band widens, the ordering survives, and 4b's binding leg changes identity

| c (bps) | non-empty bands | median width (non-empty / all 36) | EMPTY by SHARPE | EMPTY by SCALE |
|---|---|---|---|---|
| 0 | 20/36 | 0.05 / 0.00 | **13** | 3 |
| 150 | 23/36 | 0.10 / 0.05 | 9 | 4 |
| 300 | **24/36** | **0.15 / 0.10** | **0** | **12** |

- **H_WIDEN PASS**: 0 → 300 bps leaves **24 cells WIDER, 12 SAME, 0 NARROWER**; every non-empty
  band stays contiguous (20/20, 23/23, 24/24). Bands extend **downward** in g, as predicted.
- **H_ORDER PASS**: median band width U56 **0.100 / 0.150 / 0.200** vs B136 **0.050 / 0.075 /
  0.150** vs SMALL663 **0.000** at all three rates — U56 > B136 at every rate, on the native and
  the excess legs alike. SMALL663 is empty in all 36 of its cells at all three rates.
- **The reason bands are empty flips wholesale.** At 0 bps, 13 of 16 empties are Sharpe-leg kills;
  at 300 bps, **zero** are — all 12 are DD/CAGR. Idea 311's H_SHARPE ("the Sharpe legs, not the
  scaling legs, decide 4b on gross-scalar books") is itself a **zero-cash-convention artefact**.
- Idea 311's H_NODISC is unmoved: the ungated EWall control's band is >= the median treatment's in
  **0/6 cells at every rate**.

## C — both KEEP paths, all 1,836 books

| c (bps) | 4a vs v2 @0% | 4a vs v2 @c | 4b | 4b (excess legs) | BOTH | n |
|---|---|---|---|---|---|---|
| 0 | 34 | 34 | 50 | 50 | **0** | 612 |
| 150 | 164 | 124 | 69 | 69 | **0** | 612 |
| 300 | 182 | 142 | **96** | 92 | **1** | 612 |

Binding 4b legs (failures, of 612): CAGR **336 → 307 → 273**, DD 273 → 268 → 266, H2 221 → 204 →
165, OOS 221 → 197 → 154, H1 130 → 76 → 51. **The verdict moves with an undeclared dial: a 300 bps
credit nearly doubles 4b passes (50 → 96) and quadruples 4a passes even against a baseline credited
at the same rate (34 → 142).** 4a is not cash-neutral either, because it compares books at
different gross and the credit pays the low-gross one more.

The single BOTH-path book is **U56 / TOP20 / monthly / g = 0.40 / c = 300**: CAGR 10.78%, Sharpe
1.484, MaxDD −11.82%, OOS 11.62% / 1.485 / −11.82%; it passes on the excess legs too. At c = 0 the
identical book **fails 4b on CAGR alone** (8.81%) and fails 4a. Its pass is bought entirely by
crediting 60% of NAV at 3%.

## Rule 8 — walk-forward (band solved on 2009–2016 only, 2017–2026 read once)

**WF-A**: non-empty IS band in **20 / 23 / 27** of 36 cells at 0 / 150 / 300 bps; the IS midpoint
g\* lands inside that rate's OOS band in **9/20 → 15/23 → 22/27**. The credit makes the dial look
far more portable than it is — the g that survives is the one the credit props up.

**WF-B** (form by IS Sharpe, g = IS band midpoint, B136 weekly, OOS read once):

| c | pick | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b fail |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | TOP10 g=0.50 | 11.63% | 0.970 | −17.95% | 1.268 / 0.764 | 10.78% | 0.835 | −17.95% | False | H2,OOS |
| 150 | TOP10 g=0.50 | 12.46% | 1.032 | −17.89% | 1.342 / 0.819 | 11.62% | 0.891 | −17.89% | False | H2 |
| 300 | **MA-DG g=1.00** | 11.35% | **1.186** | −16.57% | 1.286 / 1.087 | **11.50%** | **1.221** | −16.57% | False | **—** |
| — | RULES v2 (cash 0%) | 8.03% | 1.106 | −12.24% | 1.230 / 0.984 | 7.98% | 1.119 | −12.24% | — | — |
| — | RULES v2 (cash 300bps) | 9.56% | 1.300 | −12.16% | 1.420 / 1.183 | 9.52% | 1.318 | −12.16% | — | — |
| — | SPY | 15.23% | 0.889 | −33.72% | 0.957 / 0.834 | 15.45% | 0.882 | −33.72% | — | — |

At 300 bps the rule-8 book clears **every 4b leg — full sample, the OOS window alone, and the
excess reading** (SPY 70% CAGR floor 10.66%, 60% DD cap −20.23%). At 0 and 150 bps the same
machinery fails. **4a is False at every rate** (MaxDD −16.57% vs the baseline's −12.16%).

## Verdict

**KILL of idea 576's premise** (H_FLAT FAIL, H_EXCESS PASS 36/36, break-even c\* ≈ 2 bps): the
+0.0065/unit-g drift is not the zero-cash convention and no cash rate removes it.

**PARK, not KEEP, for both books the credit creates.** Both rest on a **flat 300 bps applied to
2009–2016**, when realised US T-bill yields were 0–30 bps — the credit is counterfactual in
exactly the window that decides the CAGR floor and the IS band, and at 150 bps both books fail.
Promoting either would be adopting idea 642's unanswered question as an assumption. The blocking
test is a **realised short-rate series** (no network in this sandbox; `data/` carries none), which
is local/Actions work.

**No RULES change, no book promoted.** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched.

**Proposal for the Sunday review (PROTOCOL.md NOT edited here).** Any 4b or 4a verdict on a book
that holds cash must declare the cash rate it was scored at, because the verdict moves with it
(4b 50 → 96 of 612 across 0 → 300 bps), and a credited book must be scored on **excess** Sharpe at
the same rate for the book and the benchmark — `engine.metrics` defaults to `rf=0`, which pays a
low-gross book a free Sharpe it has not earned.

**SURVIVORSHIP / CAVEATS.** B136 and the small panel are current constituents; small-panel names
with `max_1d_move >= 1.0` dropped first. Cash is a flat annual rate compounded daily — wrong in
level over 2009–2026 by construction. 2009–2026 is one regime; only 2020 and 2022 are real stress.
