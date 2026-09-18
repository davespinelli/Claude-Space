# Idea 1283 (lane cloud, 2026-09-18) — should a PRE-REGISTERED DECISION RULE be required to PRICE ITS OWN MARGIN?

**ANSWERED — YES, and the price is measured. KILL for capital (nothing promoted, no new book).**

Monthly, next-day execution, 10 bps, warm-up 260 rows. Two tuned parameters only: N and gross.
Panels U56 / B136 / SMALL (663 names after dropping the 52 with `max_1d_move >= 1.0` from
`data/small_meta.csv`). Script:
`research/backtests/2026-09-18_should-a-PRE-REGISTERED-DECISION-RULE-be-required-to-PRICE-ITS-OWN-MARGIN_cloud.py`

## Gates
- **G1** fast runner ≡ `engine.backtest` post-warm-up: max|Δreturns| 6.94e-18 / 1.39e-17,
  max|Δturnover| 0.000e+00 on two cells (U56 N=20 g=0.65; B136 N=10 g=1.00).
- **G2 (replication, unplanned)** the standing 2026-09-04 KEEP-4b candidate (U56, top-20 by the
  v1 composite without the vol scaler, gross 0.65, monthly) reproduces here at
  **CAGR 12.69% / Sharpe 1.2019 / MaxDD −17.11% / halves 1.2149 / 1.1982 / OOS 1.2824**
  against idea 879's committed 12.69% / 1.201 / −17.11% / 1.215 / 1.198 / 1.281.

## Capital leg — all 84 grid points reported (`.grid.csv`)
| panel | SPY CAGR / Sharpe / MaxDD (OOS Sharpe) | RULES v2 CAGR / Sharpe / MaxDD (OOS) |
|---|---|---|
| U56 | 15.13% / 0.8848 / −33.72% (0.8745) | 8.62% / 1.2017 / −12.05% (1.2778) |
| B136 | 15.16% / 0.8861 / −33.72% (0.8767) | 7.98% / 1.0993 / −12.24% (1.1059) |
| SMALL | 14.06% / 0.8581 / −33.72% (0.8767) | 4.30% / 0.6637 / −13.89% (0.5600) |

**4a: 0 of 84.** **4b (full legs + OOS Sharpe leg): 12 of 84** — U56 9/28, B136 3/28, SMALL 0/28.
Best 4b cell by OOS Sharpe: U56 N=40 g=1.00 — 14.51% / 1.1920 / −17.96%, halves 1.1922 / 1.1933,
OOS Sharpe 1.2938, OOS CAGR 16.12%, turnover 3.13x/yr. **Nothing is promoted**: every 4b passer is
a cell of the family the record already holds, and none beats live RULES v2 on 4a.

## Margin leg — rule 8, dial chosen on 2009–2016 IS Sharpe alone, 2017–2026 read ONCE
33 choice sets (3 panels × 4 gross with N as the dial; 3 panels × 7 N with gross as the dial).
Each winner's IS Sharpe margin over its own runner-up is priced against a **paired moving-block
bootstrap** of the winner-minus-runner-up difference (block 63, B=400, seed 1283).

| group | n | mean OOS gain vs do-nothing anchor | vs runner-up | beats SPY OOS |
|---|---|---|---|---|
| z < 1 (margin inside its own floor) | 15 | **−0.0944** | −0.0549 | 4/15 |
| 1 ≤ z < 2 | 7 | +0.0029 | +0.0023 | 2/7 |
| z ≥ 2 | 11 | +0.0031 | +0.0023 | 11/11 |

- median floor SE **0.0030**, median |IS margin| **0.0039** — half the record's decisions are made
  on margins of the same order as their own noise.
- **15 of 33** winning margins are inside their own 1-SE floor.
- ρ(z, OOS gain) = **+0.1609**. ρ(raw IS margin, OOS gain) = **−0.9772** — a two-cluster artifact,
  not a within-cluster law, and reported as such (see the degeneracy row below).

### The decisive group is the record's known degenerate ladder
| dial | n | mean IS Sharpe spread | mean pairwise OOS corr | mean z | mean OOS gain |
|---|---|---|---|---|---|
| N (real dispersion) | 12 | 0.2798 | 0.9272 | **0.48** | **−0.1187** |
| gross (a rescaling) | 21 | 0.0085 | **0.9997** | 1.78 | +0.0030 |

**No choice set with real dispersion ever clears its own floor** (mean z 0.48). The entire z ≥ 2
group is the gross ladder, whose members correlate 0.9997 out of sample — ideas 1214/1223' defect
exactly. Its 11/11 "beats SPY" is a property of the panel and N, not of the pick.

## The gate as a deployable chooser (rule 8, OOS read once)
| policy | fires | mean OOS Sharpe |
|---|---|---|
| always take the IS-max pick | 33/33 | **0.8414** |
| fire only if z ≥ 1, else hold the choice set | 18/33 | **0.8843** |
| fire only if z ≥ 2, else hold the choice set | 11/33 | 0.8837 |
| do nothing (hold the whole choice set) | 0/33 | 0.8826 |
| panel SPY, set-weighted | — | 0.8760 |

Acting on the IS-max pick costs **−0.0412** mean OOS Sharpe against doing nothing. The margin gate
recovers **+0.0429** of that — but only **+0.0017** over the do-nothing anchor. **The gate's whole
value is in refusing to fire.** It is a veto, not a selector, and it must not be sold as one.

## Census leg (mechanical, regexes printed in the console log)
163 files (LEADERBOARD.md + 162 memos), 12,515 non-blank lines. **617** lines name a pre-declared /
pre-registered / decision rule; **43 of those (7.0%)** also name a minimum margin, floor or
threshold. The regexes are coarse and over-count (a line mentioning "floor" anywhere matches), so
7.0% is an **upper bound** on the share of committed decision rules that price their own margin.

## Proposed PROTOCOL line (PROPOSED, NOT APPLIED — rule 6, Sunday review)
> **10. Margin.** A pre-registered decision rule that selects among books must publish, with the
> decision, the bootstrap SE of its own winner-minus-runner-up statistic (paired moving-block,
> block 63, B ≥ 400, seed stated) and the ratio z = margin / SE. A rule may fire only at z ≥ 1.
> Below that it must stand down to the do-nothing anchor. A choice set whose members correlate
> above 0.99 out of sample is degenerate and its z is not evidence.

## What is NOT claimed
That the margin gate picks better books (it does not: +0.0017 over the anchor). That z ≥ 2 is
validated (its 11 sets are all degenerate). That the −0.9772 correlation is a law. That any
committed verdict in the record flips — the census is an upper bound on a regex, not an audit.

## Survivorship (rule 9)
U56 / B136 / SMALL are current constituents only. Every LEVEL here is an upper bound. The quoted
results are within-grid differences on identical panels and identical dates and are first-order
immune to that bias.
