# Idea 72 — ew-all-broad-as-the-simple-book (lane B, 2026-09-06)

**Verdict: KILL of the proposition. `EWall` is not the book to promote — it is the third of
four candidates. No new KEEP is claimed, no RULES change is proposed.**
RULES.md, scan.py, bot.py and baseline.py untouched.

180 grid points (2 panels × 5 books × 3 cadences × 2 gross conventions × 3 cost rungs), all
printed in `.console.txt` / `.grid.csv`. Two tuned dimensions only (cadence, convention);
panel, book and cost reported at every value and never selected on.

## Gates, passed before any new number was read
* analytic cost vs `engine.backtest(cost_bps=10)` — max|diff| **0.000e+00**
* idea 2 `u56/top20` **12.660% / 1.0921 / −18.308%** (published 12.7 / 1.093 / −18.3)
* idea 72 `B136/EWall` **10.716% / 1.0261 / −17.688%** (published 10.7 / 1.027 / −17.7)
* idea 57 `B136/ew-band3` **11.106% / 1.0624 / −16.801%** (published 11.1 / 1.064 / −16.8)
* live `u56/v1` **6.453% / 0.6642 / −13.828%** (published 6.5 / 0.664 / −13.8)
* MATCH lever is Sharpe-exact — |dSharpe| **0.000e+00** on the gate, **4.44e-16** worst over 90 cells

## The answer
Cross-universe 4b (both panels passing at the SAME cadence, convention and cost rung), out of 18:

| book | cells | where |
|---|---|---|
| `ew-band3` (idea 57) | **8/18** | D and W, LIT and MATCH, at 5 **and 10** bps |
| `frac085` (idea 46) | 6/18 | D@5, W@5, W@10, both conventions |
| **`EWall` (idea 72)** | **2/18** | **W@5 only** |
| `top20` (idea 2) | 1/18 | W/LIT@5 only |
| `v1` (live) | 0/18 | — |

`EWall` does not clear cross-universe 4b at PROTOCOL's own 10 bps. It passes on B136
(10.72% / 1.026 / −17.69%, halves 1.146/0.914, OOS 1.019) and fails on u56
(**10.40% / 1.049 / −15.87%**, halves 1.068/1.034, OOS 1.112) on the **CAGR floor** — 10.40%
against the 10.66% bar, short by 0.26pp. This is idea 82's "breaks even at no cost at all"
reproduced on a different axis.

Paired over all 36 (panel, cadence, convention, cost) cells, `EWall` minus each rival:

| vs | dSharpe | dOOS Sharpe | dCAGR | dMaxDD (shallower) |
|---|---|---|---|---|
| `ew-band3` | **−0.0681** (12/36) | **−0.0827** (12/36) | −0.70pp (12/36) | −0.66pp (12/36) |
| `frac085` | +0.0050 (20/36) | +0.0112 (20/36) | −0.53pp (4/36) | +0.93pp (35/36) |
| `top20` | +0.0265 (14/36) | +0.0642 (18/36) | −2.30pp (2/36) | +2.30pp (**33/36**) |
| `v1` | +0.4976 (36/36) | +0.5852 (36/36) | +5.22pp (36/36) | +6.04pp (18/36) |

So the un-ranked book beats idea 2's standing KEEP on every risk-adjusted axis while giving up
2.30pp of CAGR — but it loses to idea 57's band book on all four.

## Idea 65's cadence bar kills it outright
SWING = max−min Sharpe over {D, W, M} within a cell. Mean SWING: `ew-band3` **0.0363**
(worst 0.0623) < `EWall` 0.1926 (worst 0.4112) < `frac085` 0.2384 < `top20` 0.3436 < v1 0.7139 —
idea 3's ordering reproduces and extends to a second panel and three cost rungs. Cells passing
4b at **all three** cadences: `ew-band3` 4/12, `frac085` 2/12, `top20` 1/12, **`EWall` 0/12**.
Idea 72's book passes 4b only on a cadence dial, which is precisely what idea 65's proposed bar
was written to catch.

## Idea 81's gross correction, applied
`top20` is the only book of the five whose realised gross is not ~0.75: **0.717 (u56) / 0.739
(B136)**. Much smaller than the 0.492 idea 73 found on STK20 — but one-directional. MATCH
(idea 66's exact constant lever to a common 0.75) changes the 4b verdict in **4 of 90** cells
and **all four are `top20` losing a pass on the DD cap** (u56 monthly at 5/10/25 bps; B136
weekly at 5). Sharpe is invariant to 4.44e-16, so the whole effect lands on 4b's two absolute
bars — which is the half of 4b a gross mismatch corrupts.

## Rule 8
Book AND cadence chosen on 2009–2016 only; 2017–2026 read once. The IS chooser picks `EWall` in
**0 of 12** cells and the **monthly** cadence in **12 of 12**. u56 → `frac085/M`: OOS 14.32% /
1.236 / −18.84% against the do-nothing `EWall/W` control's 11.33% / 1.112 / −15.87%
(regret −0.124). B136 → `top20/M`: OOS 15.67% / 1.007 / **−26.10%** against the control's
10.58% / 1.019 / −17.69% (regret **+0.012** — the control wins). The control beats the IS pick
in 4 of 12, mean regret −0.0704. Benchmarks OOS: SPY 0.882; v1 0.747 (u56) / 0.576 (B136).
Selection beats doing nothing on average, and pays for it with 8.4pp of extra OOS drawdown on
the broad list — idea 64's monthly-drawdown warning, on the selector this time.

## Idea 155's rankability correction
Negligible on both panels: B136/EWall 1.0261 → **1.0253** (reproducing idea 155's published pair
exactly), B136/ew-band3 1.0624 → 1.0617, u56/EWall 1.0490 → 1.0491, u56/ew-band3 1.1348 → 1.1356.
The EWall-vs-ranked gap measured here is ranking, not coverage.

## Predictions
P1 hit (top20 under-grossed on both panels; MATCH deepens its DD and costs it 4 passes).
P2 hit (4.44e-16). P3 hit (EWall's only cross-universe cells are at 5 bps). P4 hit (`ew-band3`
smallest SWING on both panels). P5 hit (<0.001). P6 hit (EWall picked 0/12; the pick beats the
control on 1 of 2 panels).

## Caveats
Current-constituent survivorship on both panels (idea 54) flatters `EWall` MORE than the ranked
books, since it holds the whole beaten-down cohort a delisting-aware panel would remove — so this
KILL is conservative and would not have been manufactured by the bias. MaxDD is a single realised
extremum and is the noisiest column here (idea 117). MATCH re-levers with a constant read off the
full sample: it is a diagnostic convention, not a tradable rule, and no level under it is a
tradable estimate. Costs are flat linear bps on turnover, not spread-and-impact (idea 126). Daily
cadence at 25 bps is a stress rung, not a proposal. The small panel is deliberately excluded
(ideas 39/49/136: the gate is inverted there).

Script: `research/backtests/2026-09-06_ew-all-broad-as-the-simple-book_B.py`
