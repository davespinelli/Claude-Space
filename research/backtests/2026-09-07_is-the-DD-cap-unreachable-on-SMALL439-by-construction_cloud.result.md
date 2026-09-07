# Idea 326 — is the 4b DD cap unreachable on SMALL439 by construction?

**Script:** `2026-09-07_is-the-DD-cap-unreachable-on-SMALL439-by-construction_cloud.py`
**Panel:** 439 sub-$2B names (483 screened, 44 dropped for `max_1d_move >= 1.0`) + SPY as benchmark only.
**SURVIVORSHIP:** current constituents of the screen; the panel has no delisted names, so every
level number here (CAGR especially) is biased upward. That bias makes the finding *stronger*, not weaker.
**Terms:** 10 bps, next-day execution, weekly. Two tuned parameters only: `n` (names held) and `g` (gross).
All 30 grid points reported in `.grid.csv`; console in `.console.txt`.

## Verdict: **KILL of the "DD is the problem" framing — but the structural claim is CONFIRMED, and stronger than idea 34 stated.**

Reference levels on this sample: SPY CAGR 14.13%, Sharpe 0.862, MaxDD −33.72% (H1/H2 0.891/0.858;
OOS 15.45%/0.882/−33.72%). 4b bars: MaxDD cap −20.23%, CAGR floor 9.89%.
RULES v2 on this panel: 3.81% / 0.572 / −14.68% (0.570/0.577). RULES v1: 7.41% / 0.565 / −36.12%.

**4b passes 0/30. 4a passes 5/30** (all five are the g=0.25 rung, which beats a 3.8%-CAGR baseline on
Sharpe with less drawdown — a statement about how low the live book sits, not about small caps).

### 1. DD is *a* failing bar in 21/30, but it is not *the* binding bar
Failure-mode tally: `H1+H2+OOS+DD` 15, `H1+H2+OOS+CAGR` 9, `H1+H2+OOS+DD+CAGR` 6.
The three Sharpe-vs-SPY bars fail in **30/30** cells (H1 30, H2 30, OOS 30). Every small-panel book on
this grid is below SPY on risk-adjusted return in both halves *and* out of sample. DD is the bar the
record keeps *quoting* because it is the one that moves when you change gross; the Sharpe bars fail
silently at every gross level. Idea 34's "DD fails in 24 of 24" is true and misleading.

### 2. The DD cap and the CAGR floor are mutually exclusive at every n — the admissible gross band is EMPTY
| n | DD cap met at | CAGR floor met at | interpolated band |
|---|---|---|---|
| 10 | g ≤ 0.358 | g ≥ 0.465 | EMPTY |
| 20 | g ≤ 0.407 | g ≥ 0.527 | EMPTY |
| 40 | g ≤ 0.424 | g ≥ 0.497 | EMPTY |
| 80 | g ≤ 0.396 | g ≥ 0.682 | EMPTY |
| ALL | g ≤ 0.381 | g ≥ 0.725 | EMPTY |

### 3. The closed form: 4b's two level bars are a gross-invariant **Calmar** bar
An unlevered book at gross `g` is a cash blend, so CAGR and |MaxDD| both scale ~linearly in `g` and
`Calmar = CAGR/|MaxDD|` is ~invariant to it (observed spread over the whole ladder: 0.010–0.025).
Both level bars can therefore hold at *some* `g` only if

> **Calmar_book ≥ (0.70/0.60) × Calmar_SPY = 1.1667 × Calmar_SPY**

Here Calmar_SPY = 0.4191, so the bar is **0.4889**. Best cell is n=40 g=1.00 at **0.4356** — short by
0.053, and no cell clears (0/30). Sharpe is gross-invariant at rf=0 for the same reason, so *no gross
scalar, de-grossing instrument or cash overlay can move any of 4b's five bars on this panel.*
The de-grossed 4b variant idea 326 asked about does not exist as a way through.

### 4. Rule 8 walk-forward — (n,g) chosen on 2010–2016, 2017–2026 read once
| book | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| IS chooser → n=40, g=1.00 | 21.25% | 0.821 | −43.51% |
| anchor n=20, g=0.75 | 14.61% | 0.677 | −34.89% |
| EWALL g=1.00 | 13.07% | 0.639 | −47.24% |
| RULES v2 baseline | 3.85% | 0.568 | −14.68% |
| SPY | 15.45% | **0.882** | −33.72% |

The IS chooser picked the OOS-best cell (regret 0.0000) — and it still loses to SPY on Sharpe by 0.061
while drawing 10pp more. Re-cutting the bars on the OOS window alone changes nothing: 21/30 breach the
OOS DD cap, 15/30 sit below the OOS CAGR floor.

### 5. Text census of the record
477 LEADERBOARD rows name the small panel; 208 mention DD/drawdown; 56 name DD as a failing bar. This is
a keyword census, not a re-run — it locates the framing, it does not verify those rows' numbers.

## What is owed
**PROTOCOL caveat, not a new 4b variant.** Suggested wording for PROTOCOL rule 4b:
*"4b's DD cap and CAGR floor jointly impose a gross-invariant Calmar bar of (0.70/0.60)×Calmar_SPY.
A panel whose best book sits below that bar cannot pass 4b at any gross level; report the panel's
best Calmar against the bar before quoting a DD failure as a property of the rule under test.
SMALL439 (2010–2026) tops out at Calmar 0.436 against a 0.489 bar and is 4b-infeasible by construction."*
A de-grossed 4b variant would be the wrong fix: it would not rescue the Sharpe bars, which fail 30/30.
