# Idea 576 — price the ZERO-CASH convention on the gross LADDER

**Run:** cloud, 2026-09-12.
**Script:** `2026-09-12_price-the-ZERO-CASH-convention-on-the-gross-LADDER_cloud.py`
**Verdict: ANSWERED — idea 311's mechanism is CONFIRMED and its magnitude is trivially small
(c\* = 2.6 bps/yr), which means the record's "Sharpe is invariant in gross" is an artefact of a
0% cash assumption and INVERTS at any realistic cash rate. KILL for capital; no KEEP claimed.**

## The headline number

| cash credit on the idle fraction | median Sharpe slope in g (36 cells) | cells with slope > 0 | median Sharpe span over g |
|---|---|---|---|
| **0 bps** (idea 311's convention) | **+0.00602** | 32/36 | 0.0053 |
| **150 bps** | **−0.34137** | 0/36 | 0.3349 |
| **300 bps** | **−0.68320** | 0/36 | 0.6692 |

Idea 311 committed **+0.0065/unit g**; this run reads **+0.00602** at the same convention, inside
idea 630's standing reproduction tolerance (**H_REPRO PASS**: U56 worst 0.195x its bar, B136 0.363x,
k = 3 elapsed days, both runs pinned at 2026-09-04).

**c\* = 2.6 bps/yr** — the flat cash rate at which the median slope crosses zero. The entire
+0.0065 drift the record attributed to the zero-cash convention is worth **under 3 bps of annual
cash yield**. Idea 311's reading of the *mechanism* is right.

**But the convention's error is not small.** At 150 bps the slope is **−0.341**, 52x the published
figure and of the opposite sign; at 300 bps **−0.683**. So "Sharpe is (nearly) invariant in g" —
the premise under idea 51's and idea 311's whole band construction — is true **only** at a cash
rate within ~3 bps of zero. At any rate the sample actually paid, Sharpe is strongly **decreasing**
in gross, and the g-ladder's "free dial" framing collapses. The effect is monotone in how much
cash a form holds: MA-DG (mean idle weight 0.607) reads −1.296 at 300 bps against TOP10's −0.474
(idle 0.399).

## Do the admissible 4b bands widen? YES, and none narrows

**H_WIDEN PASS.** Against the 0-bps convention: at 150 bps **16 of 36** cells widen, **0** narrow,
3 empty bands become non-empty; at 300 bps **24 widen, 0 narrow**, 4 become non-empty. Mean band
width **0.042 → 0.064 → 0.099**. Every band extends **downward** in g, which is the expected
signature — the CAGR floor is what binds at low gross, and crediting cash is worth most where the
book holds most of it.

**H_ORDER PASS.** The panel ordering of mean band width is rate-invariant:
**U56 (0.096 / 0.138 / 0.179) > B136 (0.029 / 0.054 / 0.117) > SMALL663 (0.000 at every rate,
0 of 12 cells non-empty).**

## Rule 8

WF-A (band solved on IS, g\* = IS midpoint, OOS read once) — the credit makes the band *more*
transportable, not less: g\* lands inside the OOS band in **9/20 (0 bps) → 15/23 (150) → 21/25 (300)**.

WF-B (form by IS Sharpe, g = IS band midpoint, B136/W, OOS read once):

| cash | pick | FULL CAGR/Sharpe/MaxDD (H1/H2) | OOS CAGR/Sharpe/MaxDD | 4a vs v2 | 4b legs failed |
|---|---|---|---|---|---|
| 0 bps | TOP10 g=0.50 | 11.63% / 0.970 / −17.95% (1.268/0.764) | 10.78% / 0.835 / −17.95% | False | H2, OOS |
| 150 bps | TOP10 g=0.50 | 12.46% / 1.032 / −17.89% (1.341/0.819) | 11.61% / 0.891 / −17.89% | False | H2 |
| 300 bps | MA-DG g=1.00 | 11.34% / 1.184 / −16.57% (1.284/1.086) | 11.48% / 1.219 / −16.57% | False | **none** |

Comparands: RULES v2 (B136, credited at the same rate) OOS Sharpe 1.119 / 1.218 / 1.315;
SPY OOS 15.45% / 0.882 / −33.72% (uncredited — it holds no cash).

## KEEP paths — 612 books per rate

| cash | 4a | 4b | BOTH | bought by the credit | lost |
|---|---|---|---|---|---|
| 0 bps | 34 | 50 | 0 | — | — |
| 150 bps | 124 | 69 | 0 | 19 | 0 |
| 300 bps | 142 | **95** | **1** | 45 | 0 |

**No KEEP is claimed, and the one BOTH-path book is named as an artefact.** It is U56 TOP20
monthly g=0.40 at 300 bps — a book holding **59.8% of NAV in cash** — reading 10.75% / 1.480 /
−11.82% (halves 1.590/1.407), OOS 11.59% / 1.482 / −11.82%. It clears the CAGR floor by 0.09 pp
(10.75% vs 0.70 × SPY's 15.23% = 10.66%). Three reasons it is not capital: the 300 bps flat credit
is **counterfactual** (T-bills paid ~10 bps to 2015, ~500 after 2022, so a flat rate is wrong in
both directions and wrong in the IS window specifically); **SPY is not credited**, so the comparand
is asymmetric by construction; and it is one cell of 612 found by grid scan, not by the rule-8
selector. Idea 642 holds the real-instrument (SHY) version of this question, and lane B's
2026-09-11 run already found SHY misses the 4b CAGR floor by 0.52 pp.

The cleanest single demonstration is B136 MA-DG g=1.00 W (mean idle weight 0.291): 4b fails on the
**CAGR leg alone** at 0 bps (10.38% vs the 10.66% floor) and **passes every leg** at 150 and 300
bps. That book's 4b verdict is decided by the cash convention, not by the book.

## Gates

G1 fast vs engine **2.78e-17** · G2 cash-runner at rate 0 vs plain runner **2.29e-16** ·
G3 vectorised vs an independent day-by-day reimplementation, all three rates, **2.08e-17** ·
G4 idea 311's committed grid at 0 bps, 204 rows x 10 cols per panel, inside idea 630's tolerance.

## Caveats

A flat credit is a **sensitivity instrument for the convention**, not a return forecast.
Survivorship: B136 and the small panel are current constituents, so every panel return is biased
upward. Costs 10 bps per unit turnover on the risky legs only; the cash leg is charged no turnover,
exactly as idea 311 charged it.
