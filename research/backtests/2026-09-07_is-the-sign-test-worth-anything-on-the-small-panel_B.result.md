# Idea 129 — is-the-sign-test-worth-anything-on-the-small-panel (lane B, 2026-09-07)

**Verdict: SPLIT — the queue's literal question answers YES and my own pre-registration was
wrong, but the controls turn the YES into a KILL of the machinery.** An IS-admissible
small-panel denominator does stay positive out of sample more often than a rejected one
(**0.870 vs 0.660**, gap **+0.210**, permutation p **0.0205**; positive at **12 of 12** grid
points, significant at **9 of 12**). It is not cosmetic here the way it was on u56/broad. But
**every bit of that discrimination is already in `dMaxDD_IS`, a number that sits in the row
before any perturbation is run**: the naive rule `dMaxDD_IS > 0` scores **+0.235** and a
magnitude cut matched on selectivity scores **+0.251**, both *better* than the screen and both
at smaller p. Once the naive sign is known the two perturbation axes add **+0.105 at p 0.44**,
and within the only instrument stratum where the screen is not degenerate the gap is
**negative**. **PROTOCOL should keep the clause and delete its apparatus.**

Script `2026-09-07_is-the-sign-test-worth-anything-on-the-small-panel_B.py`; console
`…_B.console.txt`; data `…_B.{grid,bootstrap,d3,discrimination,controls,strata,rankcorr,
premise,selection,walkforward,keeppaths}.csv`. 3 books × 16 arms × 4 cost rungs on the
484-column sub-$2B panel, plus 3 × 40 seeded draws × 51 book-arms = **5,760 sub-panel
backtests**. TWO tuned parameters (q, τ), all 12 grid points reported. Nothing was modified.

## 0. Guard

Cached-signal target path equals idea 94's `targets()` **exactly** on this panel
(`max|diff| = 0.0e+00`), so the books and arms are idea 94's and not a re-derivation. Panel
2010-01-04 → 2026-09-04, evaluated from 2011-01-13; IS ≤ 2016-12-31, OOS ≥ 2017-01-01. SPY on
this index: 14.13% / 0.862 / −33.72%, halves 0.891 / 0.858, OOS 15.45% / 0.882 / −33.72%.

## 1. The premise is TRUE here (P1 CONFIRMED)

| window | rows with `dMaxDD > 0` | median `dMaxDD` |
|---|---|---|
| full | 75 / 96 (78.1%) | 1.66 pp |
| IS 2011–2016 | 63 / 96 (65.6%) | 0.17 pp |
| **OOS 2017–2026** | **73 / 96 (76.0%)** | 1.66 pp |

Idea 122 got **138/138** OOS-positive on u56/broad — a constant, and therefore unpredictable
by anything. On the small panel the OOS denominator is a genuine 76/24 variable, so the
question the queue asked is answerable here and was not answerable there. Draw-level sign
agreement splits by book exactly as idea 122's book-not-panel finding predicts: median
`frac_pos_OOS` **EWall 1.000 / TOP20 0.900 / V1u 0.650**.

## 2. H_DISCRIM — the queue's question (P2 REFUTED, and it was my prediction)

IS-only screen (D1 on IS-window returns at 0/5/10/25 bps **and** D3 on IS-window draws; D2 is
excluded because it reads the OOS window).

| (q, τ) | n adm / rej | P(OOS +ve \| adm) | P(OOS +ve \| rej) | gap | perm p |
|---|---|---|---|---|---|
| 0.05, 0.90 | 46 / 50 | 0.870 | 0.660 | +0.210 | 0.0205 |
| **0.10, 0.90 (headline)** | **46 / 50** | **0.870** | **0.660** | **+0.210** | **0.0205** |
| 0.10, 0.95 | 42 / 54 | 0.905 | 0.648 | +0.257 | 0.0055 |
| 0.20, 0.80 | 50 / 46 | 0.840 | 0.674 | +0.166 | 0.0945 |

All 12 points are in `…discrimination.csv`; the gap is positive at **12/12** and significant at
**9/12**, so the finding is not a grid-point pick. Continuous form: `spearman(frac_pos_IS,
frac_pos_OOS)` = **+0.540 / +0.560 / +0.532** at q = 0.05 / 0.10 / 0.20 over 48 book-arms.
**I pre-registered P2 (screen buys < 10 pp, p > 0.05). It is refuted.**

## 3. The controls (P2b, registered after P2 fell and before the controls were computed)

| screen | n adm | P(OOS +ve \| adm) | P(OOS +ve \| rej) | gap | perm p |
|---|---|---|---|---|---|
| **the screen** (D1_IS & D3_IS) | 46 | 0.870 | 0.660 | **+0.210** | 0.0205 |
| **N1** naive `dMaxDD_IS > 0` — one number, no bootstrap | 63 | 0.841 | 0.606 | **+0.235** | 0.0165 |
| **N2** top-46 by `dMaxDD_IS`, selectivity-matched | 46 | 0.891 | 0.640 | **+0.251** | 0.0054 |
| **N5** the screen *within* the naive-positive rows | 46 of 63 | 0.870 | 0.765 | +0.105 | **0.4445** |

- **N3 ROC.** `AUC(dMaxDD_IS → OOS sign) = 0.7016`; the screen is a single point at
  (FPR 0.261, TPR 0.548), i.e. `AUC = 0.6435`, strictly **inside** the magnitude curve. The
  bootstrap's own continuous output does better than the screen it feeds
  (`AUC(D3_frac_IS) = 0.7305`) — thresholding it at τ throws the information away.
- **N4 strata.** The screen is degenerate in three of four instrument kinds — `dd` 12/12
  admitted, `stop` 0/12 admitted, `bud` a clean 6/6 vs 0/6 split — and in `gate`, the only
  stratum with both cells populated (60 of 96 rows), the gap is **−0.058 (p 0.74)**.
  `AUC(instrument kind alone) = 0.7180`, again above the screen's 0.6435. So the screen is
  largely a re-encoding of *which instrument this is*: drawdown controls buy a lot of
  drawdown in every window, trailing stops buy negative drawdown in every window, and the
  three perturbation axes are an expensive way of noticing that.
- P2b **CONFIRMED**: screen − N1 = **−0.026** (the screen is *worse* than the naive rule).

## 4. Rule 8 walk-forward — the screen is inert in selection, on this panel too (P3 CONFIRMED)

S1 = idea 94's selector (lowest IS rate among arms buying ≥ 1 pp of IS MaxDD); S2 = S1 after
the IS-only screen. **0 of 6 picks changed at all 12 grid points**, mean OOS Sharpe
**0.7341 = 0.7341**, no empty cells. Idea 122 got 0 of 12 on the large-cap lists at its
headline; the small panel makes that 0 of 72 S2 selector-cells across the whole grid.

| cell | pick (S1 = S2) | OOS CAGR | OOS Sharpe | OOS MaxDD | ctl OOS Sharpe | RULES v2 | SPY |
|---|---|---|---|---|---|---|---|
| TOP20 @10 | ddctl-8/.5/high | 12.09% | 0.887 | −20.60% | 0.758 | 0.663 | 0.882 |
| EWall @10 | ddctl-8/.5/high | 9.26% | 0.842 | −22.32% | 0.737 | 0.663 | 0.882 |
| TOP20 @25 | ddctl-8/.5/recover | 10.82% | 0.789 | −23.81% | 0.650 | 0.602 | 0.882 |
| EWall @25 | ddctl-8/.5/high | 9.99% | 0.874 | −22.55% | 0.720 | 0.602 | 0.882 |
| V1u @10 | g200-rw | 17.83% | 0.569 | −44.83% | 0.559 | 0.663 | 0.882 |
| V1u @25 | g200-rw | 12.44% | 0.445 | −52.26% | 0.435 | 0.602 | 0.882 |

Every pick beats its own control and RULES v2 on OOS Sharpe in 6/6; **none beats SPY's 0.882**
except TOP20 @10 by 0.005, and that one loses 3.4 pp of OOS CAGR to it.

## 5. Both KEEP paths (PROTOCOL rule 4) — P4 CONFIRMED, no new KEEP

| scope | n | 4a vs RULES v2 | 4a vs RULES v1 | 4b |
|---|---|---|---|---|
| all rows | 96 | **0** | 37 | **0** |
| publishable rows | 70 | 0 | 31 | 0 |
| IS-admissible rows | 46 | 0 | 12 | 0 |
| full three-axis admissible | 37 | 0 | 12 | 0 |

Walk-forward picks: 4a 0/78, 4b 0/78. Another reproduction of "the small panel passes 4b
zero times" — idea 160B logged itself as the sixth of idea 136, and ideas 117 / 121 / 127
carry the same zero. The nearest miss is
`TOP20/ddctl-8/.5/high @10 bps`: 11.70% / 0.908 / −20.60%, halves **1.183 / 0.668**, OOS
0.887 — it clears the CAGR floor and the OOS bar and dies on **H2 (0.668 vs SPY 0.858)** and on
the drawdown cap by **0.37 pp** (20.60% vs the 20.23% allowance). `EWall/ddctl-8/.5/high @25`
is second (fails H1, OOS, DD). Note the 4a column is 37/96 against RULES v1 and **0/96 against
RULES v2**: on this panel the live book is a 4.07% / 0.615 / −12.09% cash-heavy book, and
its drawdown is what no small-cap arm can match.

## 6. What PROTOCOL should say (for the Sunday review — nothing adopted here)

Idea 122 proposed the sign test as a report-only clause with a three-axis apparatus. This run
says keep the clause and **delete the apparatus**:

> *Denominator sign test (revised).* No ratio may be quoted unless its denominator is
> positive **and its in-sample magnitude is stated**. For a drawdown price, quote
> `rate` only when `dMaxDD_IS > 0`; report `(dCAGR, dMaxDD_IS, dMaxDD_OOS)` otherwise. The
> cost-rung and name-draw perturbations of idea 122 are **not** required: on the one panel
> where the denominator's sign is measurable at all they are beaten by the naive sign rule
> (+0.235 vs +0.210 of OOS sign rate), add nothing once it is applied (+0.105, p 0.44), are
> negative inside the one non-degenerate instrument stratum (−0.058, p 0.74), and change
> **0 of 72** walk-forward selector-cells. The test remains a REPORTING bar and must never select.

Idea 122's *scope* sentence — a price on fewer than ~20 names or in a window whose benchmark
MaxDD is shallower than ~25% has no measurable denominator — **survives and is reinforced**:
V1u's median OOS `dMaxDD` on this panel is **0.05 pp** against EWall's 3.75 pp.

## 7. Not claimed

`data/prices_small.csv` is a current-constituent screen (`data/SMALL_PANEL_README.md`); every
absolute level is optimistic and a delisting-aware panel could move which rows pass. The
draw pool includes the benchmark SPY column, idea 119's convention. 40 draws makes τ = 0.95
and τ = 1.00 coarse (≥38 and 40 of 40). n = 96 rows is small for a 2×2 and the permutation
test is the honest bound on that; the controls are scored on the identical 96 rows, so their
*comparison* is paired even where the individual p-values are not decisive. This run says
nothing about whether any of these prices is *useful* — only about the denominator's sign.
P2b was written after P2 was refuted and before the controls were computed; it is a
post-hoc-registered prediction and is labelled as one.
