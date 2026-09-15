# Idea 869 (lane B, 2026-09-15) — does any committed BOOK carry ALPHA once its own BETA is charged?

**ANSWERED, and the two halves of the answer point opposite ways: YES the alpha is real and
statistically clean, NO it is not worth capital. KILL for capital.** No RULES change, no book
promoted, no KEEP claimed, no PROTOCOL edit applied. `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched (rule 6).

## What was run

7 books × 3 panels = **21 book-panels**, every book a `research/baseline.py` primitive at a
committed constant (`rules_v2_weights` at gross 0.50/0.75/1.00, the 2026-09-03 memo's Finding-2
EWELIG book at gross 0.75/1.00, `rules_v1_weights` at its committed n=5, and SPY buy-and-hold as
the zero-signal control). 10 bps, weekly, t+1, no leverage, no shorts, 260-day warm-up skip.
Two tuned parameters exactly — **BETA ESTIMATOR** {FULL, IS, R52, R104, EWMA} × **SHRINKAGE λ**
{0.00, 0.25, 0.50, 0.75, 1.00} — with panel, book and window as reported axes: **525 grid points,
every one published** in the `.grid.csv`.

## Gates — eight, all PASS, printed before any result number

| gate | result |
|---|---|
| G1 | LIVE book U56 = **8.6227% / 1.2013 / −12.0549%**, committed triple, max\|d\| **4.795e-07** |
| G2 | SPY U56 = **15.1302% / 0.8845 / −33.7173%**, max\|d\| **6.013e-06** |
| G3 | this run's count halves **are** `baseline._row`'s `len(r)//2` halves, **0.000e+00** over 21 books |
| G4 | BETAMATCH at λ=1.00 **is** the committed SPY100 comparand, max\|d return\| **0.000e+00** |
| G5 | Sharpe(β×SPY) == Sharpe(SPY) over β 0.1..2.0 at rf=0, max\|d\| **2.220e-16** (the algebra, verified) |
| G6 | determinism — grid rebuilt in a second pass hashes identically (`176b38141e433c12`) |
| G7 | SPYBH reads alpha **+2.93e-16** / β **1.000000000** / R² **1.000000000**, t NaN by the degeneracy guard; a PLANTED +5.00%/yr on the LIVE book moves alpha **+3.6149% → +8.4951%** (d **+4.8802%**, the arithmetic-vs-geometric gap), t **3.93 → 9.23**, β unchanged at 0.3134 |
| G8 | the EWELIG book rebuilt here reproduces **Finding 2** of the committed 2026-09-03 memo on U56: **10.3562% / 1.0450 (halves 1.07 / 1.02)** vs the memo's 10.4% / 1.05 (1.07 / 1.03) |

## Part A — the CAPM census (annualised alpha, Newey-West t, lag 21)

| panel | book | CAGR | Sharpe | MaxDD | alpha | t | β | R² | t H1 | t H2 | t OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | BAND03_g075 (LIVE) | 8.62% | 1.2013 | −12.05% | **+3.61%** | **+3.93** | 0.313 | 0.612 | +2.50 | +3.08 | +3.60 |
| U56 | BAND03_g100 | 11.54% | 1.2011 | −15.91% | **+4.82%** | **+3.93** | 0.418 | 0.612 | +2.50 | +3.08 | +3.59 |
| U56 | EWELIG_g075 | 10.36% | 1.0450 | −15.87% | +3.32% | +2.99 | 0.449 | 0.644 | +1.86 | +2.39 | +2.75 |
| B136 | BAND03_g075 | 7.98% | 1.0993 | −12.24% | +2.73% | +3.14 | 0.332 | 0.664 | +2.49 | **+1.86** | +2.56 |
| B136 | EWELIG_g075 | 10.66% | 1.0211 | −17.69% | +2.61% | +2.94 | 0.514 | 0.757 | +2.41 | **+1.61** | +2.26 |
| SMALL716 | BAND03_g075 | 4.64% | 0.7129 | −12.18% | +1.10% | **+0.85** | 0.251 | 0.408 | +0.53 | +0.57 | +0.54 |
| SMALL716 | EWELIG_g075 | 5.79% | 0.5174 | −31.81% | **−1.57%** | −0.71 | 0.545 | 0.564 | −0.41 | −0.61 | −0.71 |
| U56 | V1_n5 | 6.37% | 0.6563 | −13.83% | +1.95% | +1.00 | 0.303 | 0.276 | +0.61 | +0.81 | +0.97 |

(all 21 rows in `.capm.csv`.)

- **3 of 18** signal book-panels have alpha at **t > +2 in BOTH count halves** — and all three are the
  same U56 200d-band object at its three gross rungs.
- **10 of 18** clear t > +2 full-sample; **10 of 18** clear it OOS. The both-halves bar is the one that bites.
- **The alpha is one object scaled by gross.** alpha/gross across the three BAND03 rungs:
  U56 **+4.8195 / +4.8199 / +4.8191 %** (spread **8.05e-06**), β/gross 0.4176 / 0.4179 / 0.4182
  (spread 6.06e-04). Same on B136 (+3.632 / +3.634 / +3.634 %) and SMALL716 (+1.468 / +1.467 / +1.465 %).
- **It is panel-bound.** U56 +4.82%/unit gross → B136 +3.63% (H2 t only +1.86) → SMALL716 +1.47%
  (t +0.85), and the EWELIG family's SMALL716 alpha is **negative** (−2.10%/unit gross).
  SMALL716/V1_n5 reads +22.08%/yr alpha at **R² 0.009** and t +1.82 — a 5-name book on a
  current-constituent small panel that the CAPM does not describe at all; it is reported, not believed.

## Part B — the beta-matched comparand (525 points, all published)

Replace 4b's 100%-invested SPY with **β_t × SPY + (1−β_t) × CASH at rf=0**, the cheapest portfolio
carrying the book's own market exposure.

- **4a: 0 of 21** book-panels (the live book is its own comparand on U56, so it cannot pass).
- **4b, committed SPY100 comparand: 3 of 21** — U56/BAND03_g100, B136/BAND03_g100, B136/EWELIG_g075.
- **4b, BETAMATCH at λ=0 under a CONSTANT beta: 0 of 21 under FULL, 0 of 21 under IS.**
  All three committed passers die, **all three through the DD cap**:
  U56/BAND03_g100's comparand is 6.48% / 0.8845 / −15.18%, so the cap is **−9.11%** against the
  book's −15.91%.
- Under a **time-varying** beta the picture is not "stricter", it is **different**: R52 / R104 / EWMA
  each pass **4 of 21**, and they are a *disjoint* set (U56 and B136 BAND03 at g=0.50 and 0.75) —
  the books the committed rule fails. A drifting β makes the comparand's own Sharpe drift too,
  which is the only way the Sharpe legs can move at all.
- **Per-leg, over all 525 points:** H1 250→290, H2 250→283, OOS 250→283, **DD cap 300→185**,
  **CAGR floor 225→344**. On the **86 flips** the three Sharpe legs move on **0**; DD moves on 42,
  CAGR on 44. Flips run **both ways** — 44 FAIL→PASS (the loosened floor), 42 PASS→FAIL (the
  tightened cap) — so H3 **fails**: beta-matching is not a one-directional tightening.

This is the sharpest available statement of the record's standing diagnosis: **4b's two Sharpe legs
are exactly beta-blind and its two level legs are exactly beta-scaled.** G5 proves the first as an
identity, not a correlation.

## Part C — rule 8 (params fitted on 2009–2016 alone, 2017–2026 read ONCE)

Chooser, pre-stated: inside each (estimator, λ) cell, score every book-panel by the Newey-West t of
its **IS excess return over that cell's BETAMATCH comparand**, both built on IS data only, and take
the highest. (An OLS *intercept* is invariant to rescaling its regressor, so a CAPM alpha against
β×SPY is identically the alpha against SPY and neither dial would bite — the excess-return form is
what makes the tuned parameters real.) SPYBH excluded from the pick.

| chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| IS_EXCESS_T (2 of 25 cells) | U56/BAND03_g100 | 12.68% | **1.2765** | −15.91% |
| IS_EXCESS_T (23 of 25 cells) | B136/EWELIG_g100 | 13.96% | 1.0094 | −23.09% |
| IS_SHARPE (dial-free control) | U56/BAND03_g100 | 12.68% | **1.2765** | −15.91% |
| CONTROL RULES v2 (live) | U56/BAND03_g075 | 9.46% | **1.2772** | −12.05% |
| CONTROL SPY | — | 15.27% | 0.8740 | −33.72% |

25 IS-excess-t picks: OOS Sharpe median **1.0094** (min 1.0094, max 1.2765), OOS CAGR median 13.96%,
**2 distinct picks**. **0 of 25** beat the dial-free IS-Sharpe chooser, **0 of 25** beat RULES v2,
**25 of 25** beat SPY — which is the same low-beta tautology the DD leg exposes. **H4 holds.**

## Why no KEEP memo

Three book-panels do pass PROTOCOL 4b **as written** (SPY100 comparand), and the rule-8 leg confirms
U56/BAND03_g100 OOS at 12.68% / 1.2765 / −15.91% against SPY's 15.27% / 0.8740 / −33.72%. None of
them is this run's discovery — BAND03 at gross 1.00 is already on the record's shelf (idea 844
Part C prices it at 11.54%) — and this run's own result is that **all three fail the moment the
comparand carries the same beta they do**. Promoting a book on a leg this run shows to be a beta
artefact would be the opposite of what the evidence says, so nothing is promoted and no RULES
wording is proposed.

## Caveats

PROTOCOL 9: U56, B136 and SMALL716 are all **current-constituent** lists, so every alpha here
inherits survivorship bias **upward**. rf=0 throughout, as the record's committed convention — idea
676 already showed the CAGR floor does not survive a non-zero cash credit, and the same credit
would cut into the β<1 comparand's return here too (not re-priced; it is 676's question, not this
one's). Beta is estimated against SPY alone; no size, value or momentum factor is charged, so
"alpha" here means "not explained by the market", not "not explained by anything".

_Research, not investment advice. Past performance is not indicative of future results._
