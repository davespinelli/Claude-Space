# Idea 672 — restate the KEEP-4b candidate against a gross-matched gated equal-weight book

**Run:** 2026-09-11 UTC, cloud. **Script:** `2026-09-11_restate-the-KEEP-4b-CANDIDATE-against-a-GROSS-MATCHED-gated-equal-weight-book_cloud.py`

**Verdict: ANSWERED — DO NOT SWAP. The simpler book IS worse on the candidate's own panel, and the
reason is the CAGR floor, not Sharpe.** On the FULL U56 panel (not draws) the exactly gross-matched
gated equal-weight book **EWmatched** scores **10.20% / 1.086 / −15.87%** against the incumbent
CAND20's **12.63% / 1.090 / −18.31%** at 10 bps. Selection is worth **+0.0048 Sharpe** — idea 504's
"ranking earns no Sharpe" result replicates on the real panel — but it is worth **+2.43 pp of CAGR**,
and SPY's 4b floor on U56 is 0.70 × 15.11% = **10.58%**. EWmatched misses that floor by 0.38 pp and
**fails 4b; CAND20 passes.** The record's standing KEEP-4b book survives its own gross-matched
control, and survives it on exactly the leg idea 504 said ranking buys.

**But the ordering is a panel fact, not a law:** on B136 the same head-to-head reverses
(dSharpe **−0.0889** full, **−0.1375** OOS) and it is **EWmatched and EWfull that pass 4b while CAND20
fails on its H2 leg**. On SMALL439 nothing passes anything. No book is promoted, no RULES change is
proposed by this run; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` @10 bps | **6.939e-18** PASS |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | **0.000e+00** PASS |
| G3 the standing **2026-09-04 KEEP-4b incumbent** re-derived on full U56 | got **12.63% / 1.0903 / −18.31%** vs published **12.66% / 1.0921 / −18.31%**, max\|d\| **1.777e-03** PASS |
| G4a EWfull holds exactly gross 0.75 whenever any name is eligible | **8.882e-16** PASS |
| G4b EWmatched's realised daily gross == CAND20's, every day | **9.992e-16** PASS |
| G5 SMALL439 drops all 44 tickers with `max_1d_move >= 1.0` (483 → 439) | PASS |
| G6 EWfixIS's constant gross read from IS rows only | **0.718759** (IS) vs 0.715911 (full sample, **not used**) PASS |

G3 uses idea 504's pinned reading of the incumbent: rank over **all** columns (SPY included, as
`baseline` does), a **fixed 0.75/20 per selected name** (de-gross to cash below 20 eligible, do not
renormalise), vol scaler **off**, vol20 cap **0.60 on**. The 1.8e-03 residual is the price-cache
vintage channel.

## Design — 2 tuned parameters, all 12 grid points reported

Books, all on the FULL panel through the **same** gate (above the 200d MA, vol20 < 0.60, composite
with no vol scaler, weekly cadence, 10 bps):

| Book | Gross convention |
|---|---|
| CAND20 | the incumbent: top-20 by composite at a fixed 0.75/20 per name |
| EWmatched | every eligible name, equal weight, **at CAND20's own gross that day** (exact, G4b) |
| EWfixIS | every eligible name at a **constant** gross = CAND20's mean gross over 2009–2016 **only** |
| EWfull | every eligible name at a full 0.75 — the record's standard EW-all control |

**TUNED (2):** gross convention (matched / fixIS / full) × panel (U56 / B136 / SMALL439).
**FIXED, not chosen by outcome:** n = 20, gross 0.75, the gate, cadence W, warm-up 260 rows, cost
10 bps (PROTOCOL rule 2), IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL rule 8). A 0/25 bps table is
printed as a **labelled robustness appendix** and carries no verdict.

## The grid @ 10 bps (`.grid.csv`)

| Panel | Book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b | fails |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | **CAND20** | **12.63%** | **1.090** | **−18.31%** | 1.096 | 1.092 | **14.31%** | **1.165** | −18.31% | n | **Y** | — |
| U56 | EWmatched | 10.20% | 1.086 | −15.87% | 1.104 | 1.071 | 11.11% | 1.160 | −15.87% | n | n | CAGR |
| U56 | EWfixIS | 9.92% | 1.044 | −15.24% | 1.076 | 1.018 | 10.75% | 1.103 | −15.24% | n | n | CAGR |
| U56 | EWfull | 10.35% | 1.044 | −15.87% | 1.076 | 1.018 | 11.22% | 1.103 | −15.87% | n | n | CAGR |
| B136 | CAND20 | 13.09% | 0.957 | −20.05% | 1.125 | 0.811 | 12.49% | 0.892 | −20.05% | n | n | H2 |
| B136 | **EWmatched** | 10.78% | 1.046 | −17.47% | 1.176 | 0.925 | 10.57% | 1.029 | −17.47% | n | **Y** | — |
| B136 | EWfixIS | 10.54% | 1.026 | −17.41% | 1.146 | 0.914 | 10.41% | 1.019 | −17.41% | n | n | CAGR |
| B136 | **EWfull** | 10.72% | 1.026 | −17.69% | 1.146 | 0.914 | 10.58% | 1.019 | −17.69% | n | **Y** | — |
| SMALL439 | CAND20 | 6.56% | 0.463 | −27.43% | 0.603 | 0.348 | 7.23% | 0.487 | −27.43% | n | n | all 5 |
| SMALL439 | EWmatched | 3.86% | 0.356 | −33.96% | 0.437 | 0.292 | 3.48% | 0.321 | −33.96% | n | n | all 5 |
| SMALL439 | EWfixIS | 3.68% | 0.337 | −39.90% | 0.440 | 0.261 | 3.17% | 0.293 | −39.90% | n | n | all 5 |
| SMALL439 | EWfull | 3.68% | 0.337 | −39.90% | 0.440 | 0.261 | 3.17% | 0.293 | −39.90% | n | n | all 5 |

Comparands: **SPY** 15.11% / 0.883 / −33.72% (H1 0.960, H2 0.821; OOS 15.24% / 0.872) on U56,
15.23% / 0.889 / −33.72% on B136, 14.13% / 0.862 on SMALL439. **Live RULES v2** 8.61% / 1.200 /
−12.05% (U56), 8.03% / 1.106 (B136), 3.81% / 0.572 (SMALL439). **4a 0/12, 4b 3/12, BOTH 0/12.**

## Head-to-head — CAND20 minus its EXACT gross match (pure selection)

| Panel | dSharpe | dCAGR | dMaxDD | OOS dSharpe | OOS dCAGR |
|---|---|---|---|---|---|
| U56 | **+0.0048** | **+2.43 pp** | −2.43 pp (deeper) | +0.0049 | +3.20 pp |
| B136 | **−0.0889** | +2.30 pp | −2.58 pp (deeper) | **−0.1375** | +1.91 pp |
| SMALL439 | +0.1072 | +2.70 pp | **+6.53 pp (shallower)** | +0.1660 | +3.76 pp |

Ranking buys **CAGR on every panel** (+2.3 to +2.7 pp) and pays for it in drawdown on the two large-cap
panels. It buys essentially **no Sharpe on U56 (+0.005)** and **negative Sharpe on B136**. Idea 504's
draw-level finding therefore replicates at full-panel resolution on U56 and strengthens on B136 — and
it is still not sufficient to retire the clause, because PROTOCOL 4b's CAGR floor is measured against
SPY and only the concentration premium reaches it.

## PROTOCOL rule 8 — chooser fitted on 2009–2016 only, scored 2017–2026 untouched (`.walkforward.csv`)

| Panel | IS Sharpes (CAND20 / EWmatched / EWfixIS / EWfull) | Pick | OOS CAGR / Sharpe / MaxDD | SPY OOS | live v2 OOS |
|---|---|---|---|---|---|
| U56 | 0.993 / **0.993** / 0.970 / 0.970 | CAND20 | **14.31% / 1.165 / −18.31%** | 15.24% / 0.872 / −33.72% | 9.45% / 1.275 / −12.05% |
| B136 | 1.044 / **1.065** / 1.035 / 1.035 | EWmatched | 10.57% / 1.029 / −17.47% | 15.45% / 0.882 / −33.72% | 7.98% / 1.119 / −12.24% |
| SMALL439 | 0.420 / 0.417 / **0.421** / 0.421 | EWfull | 3.17% / 0.293 / −39.90% | 15.45% / 0.882 / −33.72% | 3.85% / 0.568 / −14.68% |

The chooser picks a **different book on every panel**, and on U56 it separates CAND20 from EWmatched by
**0.0004 of IS Sharpe** — a coin flip that swings 3.2 pp of OOS CAGR and 2.4 pp of OOS drawdown. The
U56 pick beats SPY OOS on Sharpe (1.165 vs 0.872) and loses to it on CAGR (14.31% vs 15.24%); the live
book beats both on Sharpe (1.275) at a third of the return.

## Cost appendix — labelled robustness, no verdict taken here (`.costappendix.csv`)

| Rung | 4a | 4b | 4b passers |
|---|---|---|---|
| 0 bps | 0/12 | 8/12 | every U56 and every B136 book |
| **10 bps (binding)** | **0/12** | **3/12** | U56 CAND20, B136 EWmatched, B136 EWfull |
| 25 bps | 0/12 | 1/12 | U56 CAND20 |

The 4b footprint is **cost-fragile in the control books and cost-robust in the ranked one**: CAND20 on
U56 is the only point that passes at 25 bps, because it is the only one with CAGR to spare above the
floor. That is the same mechanism, priced a third way.

## Survivorship (PROTOCOL 9)

B136 is today's constituents; SMALL439 is the current sub-$2B screen only (`data/SMALL_PANEL_README.md`)
— names acquired, delisted or grown out of the screen are absent, so every **level** on those panels is
biased upward and none is a tradeable estimate. U56 carries a milder form of the same bias. The claim
this run rests on is a **within-panel difference** over the same names and days, which the bias applies
to on both sides.

## Memo for the Sunday review — 10 lines

1. **No swap.** The queue's proposal (retire the ranking clause for the simpler gated equal-weight book)
   is **rejected on the candidate's own panel**: EWmatched fails PROTOCOL 4b's CAGR floor by 0.38 pp.
2. The standing **2026-09-04 KEEP-4b candidate stands unchanged**; this run proposes no new book.
3. Its 4b pass is a **CAGR-floor pass**, not a Sharpe pass: selection is +0.005 Sharpe on U56, −0.089 on B136.
4. Exact RULES wording if the Sunday review ever promotes it, unchanged from the 2026-09-04 candidate:
   > *Each Monday, score every instrument by the average of its percentile ranks on 12-1 momentum,
   > 6-month and 3-month return (no volatility scaler). An instrument is **eligible** if its close is
   > above its 200-day moving average and its 20-day annualised volatility is below 0.60. Hold the
   > **top 20 eligible** names at a fixed **3.75% of NAV each** (0.75 gross ÷ 20). If fewer than 20 are
   > eligible, hold only those and leave the remainder in **cash** — never re-spread. Trade at the next
   > day's close; assume 10 bps per unit turnover.*
5. Attach this clause to any promotion: **the ranking earns return, not risk-adjusted return.**
6. It is worth +2.4 pp CAGR and −2.4 pp MaxDD on U56 versus holding every eligible name at the same gross.
7. On B136 the ordering **reverses** and the simpler book is the one that passes 4b — the clause is a
   panel fact, and U56 is the panel it was chosen on.
8. The rule-8 chooser cannot tell the two apart on U56 (IS Sharpe 0.9934 vs 0.9930).
9. At 25 bps only CAND20/U56 survives 4b; at 0 bps eight of twelve books do. The bar, not the book, moves.
10. **Recommended action: no RULES change this week.** Re-ask the swap only with a panel-of-origin clause.
