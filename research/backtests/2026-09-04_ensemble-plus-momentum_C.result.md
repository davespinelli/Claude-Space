# Idea 26 — ensemble-plus-momentum — **KILL as worded; PARK the by-product**

Lane C, 2026-09-04. Script `research/backtests/2026-09-04_ensemble-plus-momentum_C.py` · console `…_C.console.txt` · grids `…_C.grid.csv` / `.walkforward.csv` / `.diversification.csv` / `.costladder.csv`.

**60 grid points, all reported** = 5 sleeve fractions f ∈ {0.00, 0.25, 0.50, 0.75, 1.00} × 3 equity books × 2 universes × 2 gross conventions. Two tuned parameters (f, book). 10 bps, weekly, t+1, long-only, no leverage. Eval window 2009-01-13 → 2026-09-04 after the 260-day warm-up.

**Harness check:** the run reproduces idea 2's published 4b KEEP row on u56 — 12.7% / 1.092 / -18.3%, halves 1.088 / 1.102 (published 12.7% / 1.093 / -18.3%, 1.088 / 1.103) — and the live v1 row 6.5% / 0.664 / -13.8%. It also reproduces the broad-universe H2 failure logged for idea 2 (0.811 vs SPY 0.834; queue idea 44 records 0.814 vs 0.837).

## The idea as worded: 50% sleeve + 50% v1 top-5

| Arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|
| u56 · v1 · f=0.50 natural | 5.8% | 0.791 | -11.9% | 0.725 / 0.854 | 0.935 | **PASS** | FAIL |
| u56 · v1 · f=0.50 matched | 6.3% | 0.803 | -12.0% | 0.756 / 0.847 | 0.921 | **PASS** | FAIL |
| broad · v1 · f=0.50 natural | 5.8% | 0.788 | -12.1% | 0.814 / 0.763 | 0.837 | **PASS** | FAIL |
| broad · v1 · f=0.50 matched | 6.1% | 0.779 | -14.9% | 0.856 / 0.705 | 0.778 | **PASS** | FAIL |
| RULES v1 baseline (u56) | 6.5% | 0.664 | -13.8% | 0.641 / 0.688 | 0.747 | — | — |
| SPY | 15.2% | 0.889 | -33.7% | 0.957 / 0.834 | 0.882 | — | — |

4a passes on both universes and both conventions, and survives rule 8 (f\* chosen on 2009-2016 gives OOS Sharpe 1.038 / 0.988 on u56 and 0.837 / 0.915 on broad, all above the baseline's 0.747 / 0.576). **4b fails on two bars at once**: H1 Sharpe 0.725 < SPY's 0.957, and CAGR 5.8% against the 70%-of-SPY floor of 10.66%. A 5.8%-CAGR book is not capital-worthy however good its ratio; the 4a pass is against a baseline the project has already established is weak, which is exactly why PROTOCOL added 4b.

## The mechanism the idea proposed is real — and it is not enough

`dSharpe(f) = Sharpe(blend) − [(1−f)·Sharpe(f=0) + f·Sharpe(f=1)]` is **positive in 36 of 36 interior cells**, mean **+0.052**, median +0.050, range [+0.008, +0.085]. The blend genuinely beats the weighted average of its parts everywhere — the diversification claim is confirmed as a mechanism.

It fails anyway because the two axes move at different speeds. Sharpe gains ~+0.05 of convexity; **CAGR falls almost exactly linearly** (u56 top20: 12.7% → 10.8% → 8.9% → 7.0% → 5.0% across f), because the sleeve's own CAGR is 5.0%. 4b's CAGR floor is therefore binding by f=0.50 in every cell. Daily-return correlation of sleeve-to-book is 0.63–0.82 (u56) / 0.63–0.75 (broad) — the sleeve is not the uncorrelated asset the idea assumed; it is a lower-return version of the same long-equity trend exposure.

## By-product: `top20 + 25% sleeve` is the only cross-universe 4b pass in the grid

| Arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4b |
|---|---|---|---|---|---|---|
| u56 · top20 · f=0.00 (incumbent) | 12.7% | 1.092 | -18.3% | 1.088 / 1.102 | 1.168 | PASS |
| u56 · top20 · f=0.25 natural | 10.8% | 1.085 | -16.0% | 1.061 / 1.110 | 1.184 | PASS |
| broad · top20 · f=0.00 (incumbent) | 13.1% | 0.957 | -20.1% | 1.125 / **0.811** | 0.892 | **FAIL (H2)** |
| broad · top20 · f=0.25 natural | 11.1% | 0.972 | -17.3% | 1.106 / **0.854** | 0.940 | PASS |
| broad · top20 · f=0.25 matched | 11.5% | 0.974 | -17.7% | 1.124 / 0.839 | 0.924 | PASS |

A 25% sleeve overlay repairs idea 2's known broad-universe H2 shortfall (0.811 → 0.854 vs SPY's 0.834) and is the only (book, f) combination passing 4b on **both** universes under **both** gross conventions. Three things stop it being a KEEP:

1. **Unselectable under rule 8.** In-sample (2009-2016) Sharpe is *monotone decreasing* in f on both universes (u56 0.993 → 0.955 → 0.893 → 0.788 → 0.614; broad 1.044 → 1.015 → 0.959 → 0.846 → 0.612), so the walk-forward selector picks f = 0.00 in all four top20 cells. Out of sample the ordering inverts (broad OOS Sharpe rises monotonically 0.892 → 0.940 → 1.002 → 1.070 → 1.090). Rule 8 as written cannot select this arm, and idea 88 already killed the amendment that would have let it.
2. **The whole effect is one calendar year.** Year-by-year, the sleeve's contribution to return is **negative in 17 of 18 years on both universes**. The single positive year is 2022 (+1.6pp u56, +2.2pp broad). A 4b margin of 0.020 Sharpe on H2 that rests on one bear year is not a rule.
3. **It is priced at the protocol's cost assumption, not inside it.** The joint cross-universe 4b pass survives 5 and 10 bps and dies at 15 (u56 CAGR falls to 10.3% against the 10.66% floor; broad H2 to 0.805). That does extend the incumbent's window — idea 82 measured idea 2's cross-universe breakeven at 7.5 bps, and f=0.25 passes both lists at 10 where f=0.00 passes both only at 5 — but PROTOCOL's 10 bps sits on the edge of it.

## Census

- 60 points: **4a passes 44, 4b passes 8.**
- Interior points only (the idea itself, f ∈ {0.25, 0.50, 0.75}): 36 points, 4a 31, **4b 4** — and all four are the `top20 · f=0.25` cells above.
- Every 4b pass at f=0 is a control (the incumbent books), not this idea.
- Turnover falls sharply with f (u56 v1: 23.6x/yr → 4.6x; top20: 9.6x → 4.6x), which is where part of the Sharpe convexity comes from at 10 bps.

## Verdict

**KILL** the idea as worded: 50/50 with v1 top-5 is a 4a pass against a weak book and a two-bar 4b failure, and the sleeve is 0.63–0.82 correlated with the books it is supposed to diversify. **PARK** `top20 + 25% sleeve` — the only cross-universe 4b pass the project has produced, but rule-8-unselectable, one-year-dependent, and dead by 15 bps.

_Research, not investment advice. Both universes are current constituents — survivorship bias is upward and unquantified. Data caveat (queue idea 38): `data/prices*.csv` are calendar-day indexed after 2014-09-17, so post-2014 weekends are zero-return rows; this deflates daily vol identically for every arm including the baseline and SPY, so cross-arm comparisons hold but absolute Sharpe levels do not._
