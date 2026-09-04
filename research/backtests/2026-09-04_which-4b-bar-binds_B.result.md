# Idea 84 — which-4b-bar-binds-decides-the-lever (lane B, 2026-09-04)

**Verdict: KILL idea 83's two-branch lever rule as worded — the branch assignment is
degenerate and its CAGR branch names the wrong instrument. Replacement one-line clause
proposed and measured. By-product: a KEEP-candidate (4b) strengthening — idea 57's
`ew-band3` at g=0.85 is the project's first arm to pass 4b full AND OOS on BOTH large-cap
universes at 5, 10 AND 25 bps, which answers idea 58's cost fragility.**

Script `2026-09-04_which-4b-bar-binds_B.py`; console `…console.txt`; grids
`…grid.csv` (480 points) and `…gladder.csv` (312 points). Every point reported.
Harness check: the budget=inf arm reproduces `engine.backtest` to `0.000e+00` on all four
books and both universes, and the g=0.75/B=inf control rows reproduce the published rows of
ideas 2 (12.7%/1.093/-18.3%, halves 1.088/1.103), 46 (11.3%/1.072/-16.7%), 57
(11.3%/1.136/-15.1% u56; 11.1%/1.064/-16.8% broad) and 72 (10.7%/1.027/-17.7% broad) exactly.

## Design
Books = the four standing candidates, constructions copied verbatim, **not tuned**:
`C2/CAND20` (idea 2), `C46/frac.85` (idea 46), `C57/ew-band3` (idea 57), `C72/EWall`
(idea 10/72). Two tuned parameters, both levers: gross `g ∈ {0.55,0.65,0.75,0.85,1.00}`
(≤ 1, no leverage) crossed with idea 85's **entry-only** buy budget
`B ∈ {inf,0.30,0.20,0.10}` (every sell honoured, buy leg scaled pro-rata). Idea 83's total
budget is not re-run — it is already KILLed. 8 cells × 20 arms × 3 costs = 480 points, plus
a 13-point fine gross ladder (0.40–1.00) per cell for Part D.

## 1. The tabulation the queue asked for (10 bps, published settings g=0.75/B=inf)

| book | universe | CAGR | Sharpe | MaxDD | binding bar | 4b |
|---|---|---|---|---|---|---|
| C2/CAND20 | u56 | 12.7% | 1.093 | -18.3% | **DD** (slack 1.9pp) | PASS |
| C46/frac.85 | u56 | 11.3% | 1.072 | -16.7% | **CAGR** (slack 0.66pp) | PASS |
| C57/ew-band3 | u56 | 11.3% | 1.136 | -15.1% | **CAGR** (slack 0.59pp) | PASS |
| C72/EWall | u56 | 10.4% | 1.050 | -15.9% | **CAGR** (miss 0.26pp) | fail |
| C2/CAND20 | broad | 13.1% | 0.958 | -20.1% | **H2** (miss 0.023) | fail |
| C46/frac.85 | broad | 11.2% | 1.024 | -18.6% | **CAGR** (slack 0.50pp) | PASS |
| C57/ew-band3 | broad | 11.1% | 1.064 | -16.8% | **CAGR** (slack 0.44pp) | PASS |
| C72/EWall | broad | 10.7% | 1.027 | -17.7% | **CAGR** (slack 0.05pp) | PASS |

Census: **CAGR floor binds 6 of 8 cells**, DD cap 1, H2 1. Binding-bar convention (fixed in
advance, a reporting convention not a result): 0.05 Sharpe ≡ 1pp CAGR ≡ 1pp MaxDD.
The census is not stable in cost: C2/u56 flips DD→H1 between 10 and 25 bps and C2/broad
flips DD→H2 between 5 and 10 bps, so a rule keyed to the binding bar inherits PROTOCOL's
10 bps *assumption*. It is not stable across windows either — the IS-only (2009–16) binding
bar disagrees with the full-sample one in **3 of 8** cells.

## 2. Why the two-branch rule collapses (the mechanism)
The Sharpe bars are **g-invariant in all 24 (cell, cost) triples**: across the whole ladder
g = 0.40 → 1.00 the spread of full-sample Sharpe is at most **0.0061** and of every Sharpe
margin at most 0.0066, and `shp_ok` never changes value (0 of 24 cells). That reproduces
idea 66 on four books at once and forces the geometry:

- **gross is one axis carrying BOTH non-Sharpe bars.** It moves CAGR ≈ +1.4pp and MaxDD
  ≈ −2.0pp per +0.10 of g, at dSharpe ≈ 0.000. So "DD-bound → cut g" and "CAGR-bound →
  raise g" are **the same lever in two directions**, not two branches.
- **the entry-only budget is CAGR-neutral by construction.** It saves cost but raises cash:
  broad EWall B=0.20 cuts turnover 8.27x → 7.80x (worth 0.05pp at 10 bps) while realised
  gross falls 0.750 → 0.742 (worth −0.11pp). Observed d_CAGR across all CAGR-bound cells:
  **+0.0001 to +0.0020** (0.01–0.20pp) against a gap that needs 0.26pp on the one failing
  cell. Its real content is Sharpe (+0.047 on C46/broad, +0.050 on C72/broad at B=0.20) and
  MaxDD — the bar gross cannot touch.

So idea 83's branch B is **refuted**: on a CAGR-bound book the instrument that moves the
binding margin is gross, in the raising direction (best d_CAGR-margin +0.037, i.e. +3.7pp,
at g=1.00), and the budget is two orders of magnitude too small. Idea 83 had the *sign*
right (12 of 12 cut-gross arms on CAGR-bound cells lower the CAGR margin, best −0.0139) and
the *remedy* wrong.

## 3. The branch idea 83 does not have — Sharpe-bound books
On the one Sharpe-bound cell (C2/CAND20 on broad, H2-bound), `m_H2` spans −0.119 to −0.020
over all 20 arms and **never turns positive**; the best any lever family does in the
improving direction is **+0.0027**. Zero arms convert. My pre-registered P3 was worded as a
symmetric threshold ("no lever moves a binding Sharpe margin by more than 0.05") and is
**FALSIFIED as worded** — g=1.00/B=0.10 moves H2 by −0.099 — but the falsification is
entirely downward. The operative claim holds: **no lever can fix a Sharpe-bound book; only
a book change can.** Reported both ways rather than rewriting the pre-registration.

## 4. Part D — the replacement clause, measured
Because both non-Sharpe bars sit on the gross axis, 4b defines an **interval**
`[g_min, g_max]` per (book, universe, cost): `g_min` from the CAGR floor, `g_max` from the
DD cap. A book passes 4b **iff that interval is non-empty AND its (g-invariant) Sharpe bars
pass**. Fine ladder 0.40–1.00 step 0.05:

| book | u56 5/10/25 bps | broad 5/10/25 bps |
|---|---|---|
| C2/CAND20 | [.65,.80] / [.65,.80] / Sharpe FAIL | [.60,.75] / Sharpe FAIL / Sharpe FAIL |
| C46/frac.85 | [.70,.90] / [.75,.90] / Sharpe FAIL | [.70,.80] / [.75,.80] / **empty** |
| C57/ew-band3 | [.70,1.00] / [.75,1.00] / [.80,1.00] | [.75,.90] / [.75,.90] / [.80,.90] |
| C72/EWall | [.75,.95] / [.80,.95] / Sharpe FAIL | [.75,.85] / [.75,.85] / **empty** |

`C57/ew-band3` is the only book with a non-empty interval and passing Sharpe bars on both
universes at all three costs. Cross-universe intersection: **[0.75,0.90] at 5 and 10 bps,
[0.80,0.90] at 25 bps → g = 0.85 is the interior point common to all three.**

## 5. Cross-universe 4b (full AND OOS), all 80 arms per cost
5 bps 29/80, **10 bps 18/80**, 25 bps **6/80**. At 25 bps four of the six survivors are
`C57/ew-band3` at g=0.85 (all four budgets); the other two are single g=1.00/B=0.10 points
on C46 and C72 that sit on the DD cap. 4a (beat the live book): 23/80 at 5 and 10 bps,
38/80 at 25 bps, and every 4a pass is a de-grossed g ≤ 0.65 arm — the same pattern idea 88
found.

## 6. Walk-forward (rule 8), params from 2009–2016 only, 2017–2026 untouched
OOS references: SPY 15.50%/0.884/-33.72%; RULES v1 7.78%/0.751/-13.83% (u56),
5.99%/0.581/-21.19% (broad).

| | CTL (published) | R0 (argmax IS Sharpe) | RBIND (the rule under test) |
|---|---|---|---|
| mean OOS Sharpe over 8 cells | 1.083 | 1.097 | **1.098** |

RBIND agrees with R0 in 6 of 8 cells. It differs twice, and the two differences cancel: on
C2/broad it avoids R0's g=1.00/B=0.10 pick (OOS Sharpe 0.824 vs the control's 0.894,
**−0.070**), and on C46/broad it forgoes R0's +0.060 because the IS binding bar there is a
Sharpe bar so the rule declares "no lever". Net **+0.001**. On `C57/ew-band3` RBIND selects
**g=0.85/B=0.20 on both universes** from IS data alone (R0 picks g=1.00 on u56, which breaks
the DD cap on broad) — the g=0.85 setting below is therefore rule-8 selected, not fitted.

## 7. The KEEP-candidate by-product — `C57/ew-band3` at g = 0.85
| universe | cost | CAGR | Sharpe | MaxDD | halves | OOS CAGR/Sharpe/MaxDD | TO | 4b full/OOS |
|---|---|---|---|---|---|---|---|---|
| u56 | 10 | 12.8% | 1.136 | -17.1% | 1.113/1.160 | 14.4% / 1.234 / -17.1% | 5.5x | PASS/PASS |
| broad | 10 | 12.6% | 1.064 | -18.9% | 1.163/0.971 | 12.7% / 1.073 / -18.9% | 5.8x | PASS/PASS |
| u56 | 25 | 11.9% | 1.062 | -17.2% | 1.039/1.085 | 13.4% / 1.161 / -17.2% | 5.5x | PASS/PASS |
| broad | 25 | 11.6% | 0.989 | -19.1% | 1.093/0.892 | 11.7% / 0.997 / -19.1% | 5.8x | PASS/PASS |

vs SPY 15.3%/0.890/-33.7% (halves 0.957/0.837, OOS 15.5%/0.884) and RULES v1 6.5%/0.67/-13.8%
(u56), 6.4%/0.64/-21.2% (broad). The published g=0.75 version fails cross-universe 4b at
25 bps on the CAGR floor (u56 10.5%, broad 10.3% against a 10.68% floor) — **idea 58's
finding, and the gross lever is exactly the instrument that repairs it**, because the bar
that breaks at 25 bps is the CAGR floor. 4a: passes on broad at both costs, fails on u56
(v1's -13.8% MaxDD is lower). Adding B=0.20 is marginally better on Sharpe
(1.139/1.075 at 10 bps, 5.3x/5.6x turnover) but is **not** required and is not proposed.

## 8. Honest limits
- Survivorship: both lists are current constituents, one-directional. It inflates CAGR, so
  it makes the CAGR floor *easier* and the Sharpe bars *harder* than they would have been
  live — which biases the census in section 1 toward under-reporting CAGR-bound cells.
  The lever *deltas* (the result) share panel and days and are far less exposed.
- g = 0.85 is a policy dial with zero Sharpe content (section 2), not an edge. It should be
  read as "the risk budget 4b's own two bars imply", never as a discovered parameter.
- The interval endpoints are on a 0.05 grid, and the window's width on broad at 25 bps is
  only 0.10 — one grid step of slack on each side.
- Only 2020 and 2022 are real stress tests in this sample; 2009–2026 is trend-favourable.
- Nothing here justifies real capital ahead of the ≥8 weeks of live tracking the Sep 3 memo
  already requires.
