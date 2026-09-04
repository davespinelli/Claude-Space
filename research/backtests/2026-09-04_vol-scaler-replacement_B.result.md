# Idea 40 — vol-scaler-replacement (lane B, 2026-09-04)

Script: `research/backtests/2026-09-04_vol-scaler-replacement_B.py` · 21 grid points, all reported
Data: `data/prices.csv` on the corrected trading-day index (commit c006b43); verified in-script (252/251/252 rows in 2013/2018/2024).

## Question
Lane A showed the `/sqrt(vol20)` term in the v1 composite is harmful (+10.1%/yr to remove, t 3.33)
but that the un-scaled book breaches PROTOCOL 4b's drawdown cap at every n. Can a **book-level**
risk control — applied after selection, so it cannot corrupt the signal — do the job the per-name
scaler was supposed to do?

## Design
Base book fixed (not tuned): eligible (above 200d, vol20<0.60), top-n by the v1 composite **without**
`/sqrt(vol20)`, equal weight, **75% gross** (v1's live gross), weekly, 10 bps, next-day execution.
Three arms: **NONE** (control = lane A's OFF book) · **DD** (QUEUE idea 22: halve exposure when the
book's own drawdown from its running equity peak exceeds D, restore at a new equity high) ·
**BREADTH** (halve exposure when the fraction of universe names above their own 200d MA < B).
Two tuned parameters only: n ∈ {3,5,8} and threshold (D ∈ {6,8,12}% / B ∈ {30,40,50}%). Gross,
the 0.5 halving factor, the lookbacks and the schedule are all v1's own. Both overlay signals use
data through t and execute at t+1; each switch pays 10 bps on |Δmult| × gross.

## Result — no grid point passes 4b. KILL as a v1 replacement.

Reference on this sample: RULES v1 6.5% / 0.666 / -13.8% (halves 0.641/0.692) · SPY 15.3% / 0.890 /
-33.7% (halves 0.957/0.837, OOS Sharpe 0.884). 4b thresholds: MaxDD cap **-20.2%**, CAGR floor **10.7%**.

### 1. The drawdown rule (idea 22) is a KILL, and the mechanism is unambiguous
It is not a tail control — it is a permanent de-leveraging. The book sits at **half exposure on
52–79% of all days** (a 6–12% drawdown trigger on a 15–21%-vol book fires constantly, and "recover to
a new equity high" is a rare event). Across all 9 DD points it keeps only **49–62% of the raw book's
CAGR** to buy back **23–39% of its drawdown**, and Sharpe falls at every single (n, D):

| n | raw (NONE) | DD D=6% | DD D=8% | DD D=12% |
|---|---|---|---|---|
| 3 | 21.9% / 1.037 / -25.8% | 11.8% / 0.888 / -16.6% | 12.0% / 0.858 / -15.8% | 13.5% / 0.888 / -18.5% |
| 5 | 16.5% / 0.952 / -21.6% | 9.0% / 0.806 / -14.3% | 8.0% / 0.702 / -15.5% | 8.7% / 0.705 / -15.7% |
| 8 | 13.8% / 0.932 / -17.9% | 7.1% / 0.722 / -12.1% | 7.4% / 0.700 / -13.8% | 8.2% / 0.707 / -15.4% |

Two points (**DD n=8 D=6%** and **D=8%**) do pass **KEEP path 4a** — Sharpe 0.690/0.753 and
0.713/0.694 vs the baseline's 0.641/0.692, MaxDD -12.1% / -13.8% vs -13.8%. This is a real pass by
the letter of 4a and it is exactly the pathology 4b was added on Sep 4 to catch: they clear the bar
only because the live book is weak, and they fail every 4b test (CAGR 7.1%/7.4% vs a 10.7% floor,
both halves and OOS below SPY). **Recommendation: do not adopt.** See the memo below.

### 2. The breadth gate is nearly free — and is the nearest 4b miss in the project so far
It sits at half exposure on only 7–17% of days and costs ~1pp of CAGR for ~4pp of drawdown:

| n | raw (NONE) | B=30% | B=40% | B=50% |
|---|---|---|---|---|
| 3 | 21.9% / 1.037 / -25.8% | **21.0% / 1.027 / -20.6%** | 19.9% / 1.002 / -20.9% | 19.4% / 0.994 / -21.4% |
| 5 | 16.5% / 0.952 / -21.6% | 16.0% / 0.949 / -17.8% | 15.5% / 0.941 / -17.2% | 15.0% / 0.932 / -17.9% |
| 8 | 13.8% / 0.932 / -17.9% | 13.4% / 0.930 / -19.1% | 13.0% / 0.926 / -16.8% | 12.4% / 0.904 / -18.1% |

Drawdown improves in **8 of 9** points (the exception is n=8/B=30%, +1.2pp worse). Sharpe is
slightly *worse* in 9 of 9: the gate is a drawdown reducer, not a Sharpe improver — an honest
description, not a headline.

**BREADTH n=3 / B=30%** passes 4b's H1 (0.961 vs SPY 0.957), H2 (1.089 vs 0.837), OOS Sharpe
(1.081 vs 0.884) and CAGR (21.0% vs a 10.7% floor), and **fails on MaxDD alone by 0.4pp: -20.6%
against a -20.2% cap.** Not tuned further — that would be tuning until it works (PROTOCOL rule 7).

### 3. Walk-forward (rule 8): params chosen on 2009–2016, evaluated on 2017–2026 untouched
Two selection rules were fixed in the script before any OOS number was read.

| Arm / rule | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| NONE / S1 (best IS Sharpe) | n=3 | 1.016 | 23.9% | 1.057 | -25.8% |
| DD / S1 | n=3 D=12% | 0.869 | 14.8% | 0.908 | -18.5% |
| DD / S2 (IS DD cap) | n=5 D=6% | 0.764 | 9.9% | 0.840 | -14.3% |
| **BREADTH / S1** | **n=3 B=30%** | 0.957 | **23.8%** | **1.081** | **-20.6%** |
| RULES v1 | — | 0.553 | 7.8% | 0.751 | -13.8% |
| SPY | — | 0.899 | 15.5% | 0.884 | -33.7% |

The breadth pick beats SPY out-of-sample on CAGR (+8.3pp) and Sharpe (1.081 vs 0.884) at 61% of
SPY's OOS drawdown, and beats RULES v1 by 16pp of CAGR. S2 (the 4b-aware rule) selects nothing in
the NONE and BREADTH arms — no in-sample point met the in-sample DD cap of -13.2%, which is itself
the finding: this book cannot be made to satisfy 4b's drawdown test by a book-level gate.

### 4. Stress years (n=5, B/D=40%/8%)
| | NONE | DD D=8% | BREADTH B=40% | RULES v1 | SPY |
|---|---|---|---|---|---|
| 2011 | -0.9% | +0.5% | +0.3% | +1.9% | +1.9% |
| 2018 | +17.3% | +8.8% | +16.0% | +8.0% | -4.6% |
| 2020 | +32.6% | +16.5% | +28.2% | +8.4% | +18.3% |
| 2022 | -5.0% | -6.8% | -6.3% | +2.6% | -18.2% |
The DD rule gives up half of 2020 and does not help in 2022. The breadth gate keeps most of 2020's
recovery and is no better than the raw book in 2022 (the 2022 decline was slow enough that the
un-gated book's own 200d exits did the work).

## Verdict
**KILL** as a capital-worthy (4b) replacement for the vol scaler: 0 of 21 points pass.
**PARK** the breadth gate (all 9 points; the n=3/B=30% point misses 4b on drawdown by 0.4pp and is
the walk-forward selection). **KILL** the book-level drawdown rule as a mechanism — QUEUE idea 22 is
answered negatively here and does not need its own run: a fixed drawdown trigger with a
new-high reset on a book of this volatility is a permanent 50% de-leveraging, not risk control.
Two DD points pass 4a marginally; the memo below recommends against adopting them.

## Caveats
`research/universe.json` is a current-constituent list — survivorship bias flatters every momentum
book here, including the 21%/yr n=3 numbers. 2009–2026 is one regime with only 2020 and 2022 as real
stress. The breadth gate's edge rests on ~7% of days; it is a small-sample effect on the tail.
Nothing here justifies real capital ahead of the live paper record that started Sep 4.

## Follow-ups queued
41 (breadth-gate-depth: is the 4b DD miss closed by a deeper cut than 0.5 rather than a tuned
threshold?), 42 (breadth-gate on the equal-weight-all-eligible v2 candidate of idea 28),
43 (why H1 Sharpe is the recurring binding constraint against SPY across ideas 24, 25, 28, 40).
