# MEMO — 4a KEEP-candidate: RULES v2 core + 50% three-asset macro sleeve (broad panel)

From idea 106, 2026-09-07 (cloud). Script:
`research/backtests/2026-09-07_is-DBC-a-drag-or-a-contango-artefact_cloud.py`.
**Path 4a only** (beat the book). It fails 4b on the CAGR floor — as does RULES v2 itself.

## Exact RULES wording

> **Clause S (macro sleeve).** Hold **50% of NAV** in the equity book and **50%** in a
> three-asset macro sleeve of **TLT, GLD, UUP**. The sleeve's weights are set each rebalance
> as `vote x inverse-vol`, row-normalised over the three assets: `vote` is the fraction of
> {12-1 month, 6-month, 3-month} total returns that are positive (0, 1/3, 2/3 or 1), and
> `inverse-vol` is 1 / (60-day return standard deviation). The equity leg is equal-weight
> across every eligible name at **75% gross** (eligible = above its 200-day mean with 20-day
> annualised vol < 0.60). Weekly cadence, weights decided at the close and applied at the next
> close. No leverage: the two legs are held as written, not rescaled.

## The numbers (broad panel, 136 names, 10 bps, weekly, 2009-01-13 → 2026-09-04)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | OOS CAGR | turn/yr | gross |
|---|---|---|---|---|---|---|---|---|
| **Candidate (equal-weight leg)** | **6.81%** | **1.2518** | **-10.28%** | **1.3165 / 1.1947** | **1.2665** | 6.96% | 6.42 | 0.672 |
| S4 sibling (adds DBC) | 6.76% | 1.1890 | -10.24% | 1.2143 / 1.1673 | 1.2317 | 7.05% | 6.50 | 0.665 |
| RULES v2 (live) | 8.03% | 1.1058 | -12.24% | 1.2291 / 0.9844 | 1.1185 | 7.98% | — | 0.75 |
| SPY | 15.23% | 0.8890 | -33.72% | 0.9566 / 0.8340 | 0.8820 | 15.45% | — | 1.00 |

**4a verdict: PASS.** H1 1.3165 > 1.2291, H2 1.1947 > 0.9844, MaxDD -10.28% better than
-12.24%. It also beats RULES v2 out of sample (1.2665 vs 1.1185).

A `top20` variant of the same clause passes 4a too (8.03% / 1.1243 / -10.76%, H1 1.2571 /
H2 1.0144, OOS 1.0697) but is worse on every axis and turns over 9.21x/yr. **Recommend the
equal-weight leg.**

## Why this is not a scan hit

Rule 8 selects it. With `(arm, f)` chosen on 2009-2016 IS Sharpe and 2017-2026 read once,
the chooser lands on **`noDBC@f=0.50` in 8 of 8 cells** at 10 bps, beating the no-sleeve
control 8/8 and SPY 8/8. These two 4a passes are that pick, on the broad panel. An
independently written lane-B run of the same idea on the same day selects the identical arm
and finds the identical two 4a cells.

## What must be said against it before any Sunday review adopts it

1. **It is a 4a candidate only.** CAGR 6.81% against 4b's 10.66% floor — it fails, and by a
   wider margin than RULES v2's own 8.03% miss. This clause buys Sharpe and drawdown by
   giving up return. Adopting it moves the live book *further* from capital-worthy.
2. **Not cross-panel.** On u56 the same book is 6.64% / 1.2262 / -8.71% with H1 **1.1632**
   against RULES v2's u56 H1 of **1.2259** — it **fails 4a on the first half**. The pass
   exists because RULES v2 is weaker on broad (H2 0.9844) than on u56 (H2 1.1908). One
   panel, not two.
3. **Not tested at 25 bps.** At 25 bps the candidate is 5.79% / 1.0714 / -10.54%
   (H1 1.1330 / H2 1.0169), but this run did not compute RULES v2 at 25 bps, so no 4a verdict
   at that rung is claimed.
4. **The sleeve's composition is under active doubt.** Idea 106 §2 finds `noTLT` has a
   *larger* era reversal than `noDBC`, with a deletion gain of **+0.1391 (8/8 cells)** in
   2021-2026 — i.e. on the most recent era the evidence favours dropping **TLT**, which this
   clause keeps. Open idea 105 separately asks whether the GLD leg is the whole sleeve.
   **The `f=0.50` fraction and the equal-weight leg are well supported; the three-asset
   membership is not settled.**
5. **The `noDBC` prune this clause encodes is worthless outside the `natural` convention.**
   The out-of-sample gap of `noDBC` over `S4` is **+0.0135 (12/16 cells) at natural gross but
   -0.1052 (0/16) at g=1.00** — confirmed to four decimals by an independent lane-B run. This
   candidate is written at natural gross, which is the side the prune wins on, but the record
   should not read the prune as a general result: idea 101/104's candidate is written at
   g=1.00, and **there the prune is behind in 16 of 16 cells.** The turnover saving
   (-0.0966x/yr, worth roughly 0.02 of Sharpe) does not cover that.
6. **It dies quickly on cost.** Lane B's ladder puts the 4a count at **6 / 2 / 1 / 0 / 0** at
   5 / 10 / 15 / 20 / 25 bps: these passes are **gone by 20 bps**.
7. **Survivorship**: the broad panel is current constituents, so the equity leg's level is
   biased up. The four sleeve ETFs are alive throughout.

## Recommendation

**PARK as a 4a candidate; do not adopt at the next Sunday review.** The single-panel pass
(point 2), the unsettled membership (points 4 and 5) and the death by 20 bps (point 6) are
each independently enough to wait; together they say this is a reporting result, not a rules
change. The cheap next
step is to re-run this exact clause with the membership swept — `noTLT` and `GLD`-only
against `noDBC` — on both panels at 10 and 25 bps, which is open ideas 105 and the §2 flag
combined into one grid.
