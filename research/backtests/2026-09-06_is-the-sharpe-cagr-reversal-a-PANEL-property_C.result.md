# Idea 271 — is-the-sharpe-cagr-reversal-a-PANEL-property-not-a-width-one (lane C, 2026-09-06)

**Verdict: ANSWERED / KILL of the strong form.** The panel-level reversal share is **not**
predictable from the four pre-backtest panel characteristics. What is real is a single
binary fact — small-cap panels never reverse, large-cap panels usually do — and the
regression's headline R² is that indicator, not a law. No KEEP-candidate, no memo, no
RULES change; `RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

Script: `2026-09-06_is-the-sharpe-cagr-reversal-a-PANEL-property_C.py`
(`--q5` re-reads the committed CSVs and reprints the decomposition without a backtest).

## Design

Idea 269C's five matched-ratio panels cannot answer the queue's question: four regressors
on five observations has zero residual degrees of freedom. So the **panel count** was
enlarged, not the regressor count. A pre-registered seeded pool of random **sub-panels** —
each SOURCE in {U56, B136, BSTK100, SMALL439, ETF36} × k_frac {0.25, 0.40, 0.55, 0.70,
0.85} × seed {0,1}, subject to k ≥ 12 — gives **53 panels** (5 named + 48 sub), and idea
269C's whole matched-ratio grid was re-run on every one: **371 reversal cells, 1060
backtests, 530 grid points per cost rung, all reported.** Weekly, t+1, 10 bps, gross 0.75,
gate above-200d AND vol20 < 0.60, ranking key = composite without the vol scaler; 0 bps is
a diagnostic column only. Reversal is idea 259/269's epsilon rule unchanged.
Tuned parameters: **panel (53) and target ratio r\* (7)** — the characteristics are
measured, not tuned.

Characteristics (prices + the gate only; no return stream, no arm; computed twice, once
full-sample and once on the IS window alone, so rule 8 never sees an OOS-informed
regressor): `breadth` = mean n_elig/k on rebalance days; `disp` = mean cross-sectional sd
of trailing 63d returns among eligible names; `corr` = mean off-diagonal pairwise
correlation; `evol` = mean vol20 of eligible names. `k` and `n_elig` are reported as
controls.

## Reproduction gate (2/2 exact, before any new number was read)

| cell | this run | idea 269C published |
|---|---|---|
| B136/EWall | 10.7% / 1.026 / -17.7%, OOS 1.019 | 10.7% / 1.026 / -17.7%, OOS 1.019 |
| U56/EWall | 10.4% / 1.049 / -15.9% | 10.4% / 1.049 / -15.9% |

Per-panel reversal counts **6/6/4/2/0 of 7** (B136 / BSTK100 / U56 / ETF36 / SMALL439) and
the share-by-ratio sequence **0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00** both
reproduce exactly. 4 of 371 cells are degenerate (two ratios rounding to the same n on a
narrow panel); the share is 0.4959 over the non-degenerate cells vs 0.4906 over all.

## (1) The parent's panel disagreement survives sub-sampling — and gets wider

Pool share mean **0.4906**, sd 0.3261, 0/7 in 11 panels and 7/7 in 2. By source:

| source | panels | share | sd | min | max |
|---|---|---|---|---|---|
| B136 | 11 | 0.7922 | 0.1612 | 0.5714 | 1.0000 |
| BSTK100 | 11 | 0.6234 | 0.2328 | 0.0000 | 0.8571 |
| U56 | 11 | 0.5974 | 0.2375 | 0.0000 | 0.8571 |
| ETF36 | 9 | 0.3651 | 0.2486 | 0.0000 | 0.7143 |
| SMALL439 | 11 | 0.0519 | 0.0963 | 0.0000 | 0.2857 |

The source ordering is idea 269C's ordering. But the **within-source spread is as large as
the between-source spread** everywhere except SMALL439: two random 25%-draws of BSTK100
score 0/7 and 5/7. "The panel decides" is true at the level of families, not of panels.

## (2) The regression fits in sample — R² 0.7112 on 53 panels

| term | coef | t |
|---|---|---|
| breadth | +0.6056 | **+8.84** |
| disp | +0.4654 | +2.73 |
| corr | −0.0771 | −1.34 |
| evol | −0.1140 | −0.78 |

Adding k and n_elig lifts R² to 0.7318 (controls alone reach 0.5622). At cell level with
SEs clustered by panel: width alone (idea 269C's regressor) R² 0.1235, four chars alone
0.2970, chars + width **0.4199** — so the characteristics carry roughly 2.4× what width
carries, and the two are close to additive.

## (3) …and the R² is one indicator variable (Q5)

- A **single dummy** `source == SMALL439` gives R² **0.4828**, and `breadth < 0.5` gives
  R² **0.4828** — the two are *identical*, because breadth is perfectly bimodal:
  SMALL439-source panels 0.3074–0.3290, every other panel 0.6191–0.7445, **no overlap**.
- Inside the large-cap cluster (42 panels) **breadth alone explains 0.0240**. The
  "continuous" predictor stops predicting the moment the small-cap panel leaves the pool.

## (4) Out of source it beats nothing (the only honest test)

Leave-one-SOURCE-out, panel-level share:

| held out | panels | actual | predicted | out-of-source R² |
|---|---|---|---|---|
| B136 | 11 | 0.7922 | 0.6462 | **+0.7764** |
| BSTK100 | 11 | 0.6234 | 0.7746 | +0.1727 |
| ETF36 | 9 | 0.3651 | 0.0208 | −1.6952 |
| SMALL439 | 11 | 0.0519 | 0.8352 | −0.9817 |
| U56 | 11 | 0.5974 | 0.8667 | −1.0658 |

**Mean out-of-source R² −0.5587**: quoting the pool mean beats the fitted model in 4 of 5.
Restricted to the large-cap cluster it is worse — **−1.1035**, the mean winning 3 of 4.
This is the answer to the queue's question: **the panel-level share is not predictable.**

## (5) Rule 8 — the relationship

IS 2009-01-01..2016-12-31 fits, OOS 2017-01-01..end read once. IS fit of P(reversal) on
4 chars + width: R² 0.2820 over 371 cells. **All 38 threshold grid points printed**
(19 for the characteristic rule, 19 for idea 269C's width rule).

| classifier | IS acc | OOS acc |
|---|---|---|
| CONST (IS majority = False) | 0.5553 | 0.5903 *(= base rate)* |
| R_THRESH (r < 0.55) — idea 269C's width rule | 0.6011 | 0.6469 |
| SOURCE (per-source IS majority) | 0.6658 | 0.6739 |
| PANEL (per-panel IS majority) | 0.7520 | 0.6469 |
| **CHAR (p̂ ≥ 0.50, all sources)** | 0.7412 | **0.7709** |
| CHAR-LOSO (refit without the held-out source) | — | 0.7547 |

The IS-argmax threshold 0.50 gives OOS 0.7709 against an OOS optimum of 0.8032 at 0.55 —
the selection cost is small, and the characteristic rule beats every rival including the
parent's width rule. **But the pooled number is one source.** Per-source LOSO:

| held out | cells | predicted rate | OOS acc | own base rate | lift |
|---|---|---|---|---|---|
| B136 | 77 | 0.7143 | 0.8312 | 0.6234 | **+0.2078** |
| BSTK100 | 77 | 0.8442 | 0.6364 | 0.5065 | +0.1299 |
| U56 | 77 | 0.8701 | 0.6234 | 0.5714 | +0.0519 |
| ETF36 | 63 | 0.0000 | 0.6667 | 0.6667 | 0.0000 |
| SMALL439 | 77 | 0.0000 | **1.0000** | **1.0000** | **0.0000** |

SMALL439's 77/77 is **extrapolation, not a validated relation**: its breadth sits
**−13.1 sd** outside the large-cap training range, the fit therefore predicts zero
reversals there, and it happens to be right — against a base rate that is already 1.0000,
so the lift is exactly zero. ETF36 is the same shape with no payoff: predicted rate 0.000,
accuracy exactly its base rate. **Mean lift over the four large-cap sources +0.0974**, and
it is +0.21 / +0.13 / +0.05 / 0.00 — one source carries it.

## (6) Rule 8 — the book (pooled equal-weight over the 5 named panels, OOS read once)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| EWALL (do nothing) | 8.81% | 0.8807 | -20.6% | 0.99 / 0.78 | 8.61% | 0.8574 | -20.6% |
| FWD20 (incumbent) | 10.84% | 0.9028 | -21.4% | 1.00 / 0.82 | 11.12% | 0.9031 | -21.4% |
| S_SHARPE | 12.77% | 0.9372 | -21.6% | 1.07 / 0.82 | 12.43% | 0.8887 | -21.6% |
| S_CAGR | 14.36% | 0.8462 | -23.0% | 0.93 / 0.77 | 13.99% | 0.7973 | -23.0% |
| **CSEL** (the characteristic rule) | 9.46% | 0.8203 | -20.7% | 0.83 / 0.81 | 10.81% | **0.9050** | -20.7% |
| RSEL (idea 269C's width rule) | 9.42% | 0.8876 | -21.4% | 0.96 / 0.83 | 9.64% | 0.8966 | -21.4% |
| RULES v1 | 6.74% | 0.7399 | -17.3% | 0.89 / 0.61 | 6.43% | 0.6908 | -17.3% |
| **RULES v2 (live)** | 7.07% | **1.0464** | **-11.2%** | 1.11 / 0.98 | 7.16% | **1.0776** | -11.2% |
| SPY | 15.23% | 0.8890 | -33.7% | 0.96 / 0.83 | 15.45% | 0.8820 | -33.7% |

CSEL is a rare case in this record: it **beats doing nothing out of sample** (+0.0476 of
Sharpe over EWALL, and +0.0019 over the FWD20 incumbent). It still buys nothing. Its
full-sample Sharpe 0.8203 is the **worst** book in the table bar RULES v1 — below EWALL's
0.8807 — so the OOS win is a window, not an edge; and it is 0.17 of Sharpe and 9.5 pp of
drawdown behind the live book on the same panels. Idea 259's S_CAGR-vs-S_SHARPE exchange
rate reproduces once more: **+1.56 pp/yr of OOS CAGR for −0.091 of OOS Sharpe.**

## (7) KEEP paths — all 530 points per rung reported

| rung | 4a (vs live RULES v2) | 4a (vs RULES v1) | 4b |
|---|---|---|---|
| 10 bps | **0 / 530** | 110 / 530 | 54 / 530 |
| 0 bps | **0 / 530** | 67 / 530 | 91 / 530 |

The 4a pathology again: nothing beats the live book, 110 things beat the book it replaced.
Binding bar over the 476 failures at 10 bps: DD 360, H2 330, OOS 317, CAGR 305, H1 298.
Every 4b pass sits on a B136/BSTK100/U56-derived panel; **SMALL439 and ETF36 are 0 of 200**,
reproducing idea 136. The eight **named-panel** passes are exactly idea 269C's published
set — `U56/FWD 14, 20, 31` and `B136/EWall, FWD 35, 50, 74, 99` — reached here as controls.
The best cells in the whole run (`BSTK100~0.40~s0` 14.7%/1.140/-19.6% OOS 1.285) are
**random sub-panels**, which idea 78/83 priced at a 46% base rate for clearing 4b by
construction; they are not books. **No KEEP-candidate.**

## Survivorship

Every panel is a subset of a current-constituent list, so the bias is inherited whole. The
un-ranked book holds everything and takes the full survivorship premium while a ranked book
can only redistribute it, so the bias runs **toward** reversals — toward finding more
structure than a live universe would have shown. The "not predictable" verdict is therefore
conservative; the +0.0974 large-cap classification lift is an upper bound.

## For the record

1. **Idea 269C's verdict stands but should be re-worded.** "It is the panel that decides"
   is right only at the level of panel *families*; within a family, two random draws of the
   same source disagree 0/7 vs 5/7. There is no panel-level number to publish.
2. **`breadth` is a small-cap dummy on this corpus, not a characteristic.** Any published
   claim that regresses on breadth across mixed panels is reporting a two-cluster split.
   Queued as 276.
3. **Do not add a predicted-reversal column to the leaderboard.** Out of source the model
   loses to its own mean in 4 of 5 sources.
4. The one usable fact is negative and cheap: **a panel whose gate admits under half its
   names does not produce the reversal** (SMALL439: 0 of 77 cells, in both windows).

Follow-ups queued: 276, 277, 278.
