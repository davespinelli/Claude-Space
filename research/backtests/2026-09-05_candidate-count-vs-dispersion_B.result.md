# Idea 78 — candidate-count-vs-dispersion (lane B, 2026-09-05)

**Verdict: ANSWERED — KILL of both readings. Neither the candidate COUNT nor the DISPERSION governs the
ranking payoff; SELECTIVITY q = n / n_elig does, and idea 73's +0.964 is what a fixed n looks like when the
pool grows underneath it.** No new book, no RULES change. Script:
`research/backtests/2026-09-05_candidate-count-vs-dispersion_B.py`
(console `…console.txt`, grids `…gridA.csv` / `…gridB.csv`, walk-forward `…walkforward.csv`,
proposed reporting clause `…memo.md`).

## The question

Idea 73 killed dispersion as a universe clause but left its own diagnostic confounded: across seven panels
the gross selection spread ranked with the eligible-candidate count (+0.571 / +0.857 / +0.964 at n = 5/10/20)
better than with dispersion (+0.429 / +0.679 / +0.357), and across panels the two move together. This run
separates them inside ONE panel (B136), where the names, the gate, the survivorship exposure, the costs and
the days are all held fixed, using a random subsample of the candidate set as the instrument.

## Pre-checks (run before any new number was read)

| check | result |
|---|---|
| [a] harness, universe.json window | `U56/CAND20` **12.7% / 1.092 / -18.3%, halves 1.088/1.102** vs idea 2's published 12.7% / 1.093 / -18.3%, 1.088/1.103 — the last-digit gap idea 81 already logged (the row reads 1.09214). `U56/v1` 6.5% / 0.664 / -13.8% vs the live 0.666 |
| [b] idea 73's premise, recomputed from scratch on all 7 panels | **EXACT: Spearman(n_elig, spread) +0.5714 / +0.8571 / +0.9643 and Spearman(sd, spread) +0.4286 / +0.6786 / +0.3571.** The confound itself is Spearman(n_elig, sd) = **+0.321** across panels |

## Test A — gross spread at EXACTLY matched candidate count (3 k × 3 n × 100 draws = 900 points)

Each rebalance week, k names are drawn at random from the eligible set and treated as the whole candidate
set. Candidate count is then exactly k in every week of every cell; dispersion is free to vary draw to draw.
Primary week set = the 697 weeks (75.7%) with n_elig ≥ 80 = max k, identical for every cell.

**A1 — at fixed n, spread rises steeply with k, with dispersion matched** (annualised, common weeks):

| k | mean sd | spread n=5 | n=10 | n=20 | t(5) | t(10) | t(20) |
|---|---|---|---|---|---|---|---|
| 20 | 0.2512 | +0.0366 | +0.0211 | -0.0000 | 1.29 | 1.42 | 0.03 |
| 40 | 0.2611 | +0.0584 | +0.0334 | +0.0223 | 1.60 | 1.46 | 1.83 |
| 80 | 0.2683 | +0.0910 | +0.0657 | +0.0359 | 2.09 | 2.14 | 1.84 |

**A2 — dispersion pays nothing once count is held exactly fixed.** Spearman(draw sd, draw spread) over the
100 draws of a cell is **-0.13 … +0.13, negative in 7 of 9 cells**. Pooled standardised OLS
`spread ~ z(log k) + z(sd)` over 300 draws per n:

| n | β(log k) bp/yr | t | β(sd) bp/yr | t |
|---|---|---|---|---|
| 5 | +201.2 | **+7.76** | +24.2 | +0.93 |
| 10 | +209.8 | **+13.36** | -31.1 | -1.98 |
| 20 | +145.7 | **+23.24** | +1.5 | +0.24 |

So **idea 78's premise holds as posed**: the count is the live variable and dispersion is not.

**A3 — but the count effect is not a count effect.** A book of n out of k takes the top q = n/k of the
cross-section, so raising k at fixed n also makes the book more selective. Hold q fixed and let the count
vary 4×:

| q = n/k | cells | spreads | range | weekly SE of a cell |
|---|---|---|---|---|
| 0.125 | (40,5) (80,10) | +0.0584, +0.0657 | +0.0073 | 0.031–0.036 |
| **0.250** | (20,5) (40,10) (80,20) | **+0.0366, +0.0334, +0.0359** | **+0.0032** | 0.020–0.028 |
| 0.500 | (20,10) (40,20) | +0.0211, +0.0223 | +0.0012 | 0.012–0.015 |

Every diagonal range is a fraction of one cell's own standard error. Over the 9 cells,
**Spearman(q, spread) = -0.975** against Spearman(k, spread) = +0.685, and along the q = 0.25 diagonal
Spearman(k, spread) = **-0.500**. The governing variable is the quantile depth, not the pool size and not the
spread of the pool.

## Test B — book level, 10 bps, next-day execution (3 k × 2 n × 50 fixed random sub-panels = 300 books)

| k | n | mean n_elig | CAGR | Sharpe | MaxDD | EWall Sharpe | premium | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 5 | 13.3 | 11.4% | 0.842 | -22.0% | 0.931 | **-0.088** | 17/50 | 1/50 |
| 20 | 20 | 13.3 | 6.8% | 0.979 | -11.8% | 0.931 | +0.048¹ | 49/50 | 0/50 |
| 40 | 5 | 26.9 | 12.0% | 0.797 | -24.1% | 0.962 | **-0.165** | 8/50 | 0/50 |
| 40 | 20 | 26.9 | 10.4% | 0.975 | -18.3% | 0.962 | +0.013 | 49/50 | 17/50 |
| 80 | 5 | 54.0 | 14.3% | 0.837 | -24.3% | 1.010 | **-0.173** | 7/50 | 1/50 |
| 80 | 20 | 54.0 | 12.0% | 0.967 | -19.6% | 1.010 | -0.043 | 48/50 | 23/50 |

¹ at k=20, n=20 the book holds every eligible name, so its "premium" is a weighting artefact (fixed 1/n vs
gross-normalised) and is excluded from the premium-vs-k reading.

**Net of costs the sign reverses.** Gross spread rises with selectivity; the net Sharpe premium *falls* with
pool size — pooled Spearman(k, premium) = **-0.358** (n=5) and **-0.601** (n=20), Spearman(sd, premium)
= -0.086 / -0.274. This is idea 82's "ranking subtracts value" reproduced on a within-panel instrument: 4a
passes 178 of 300, 4b passes 42 of 300, and on the full panel `EWall` (Sharpe 1.026, MaxDD -17.7%) beats
both `CAND5` (0.880) and `CAND20` (0.957) and is the only one of the three that passes 4b.

## Test C — PROTOCOL rule 8 walk-forward (IS ≤ 2016, OOS 2017-2026 read once)

SPY OOS 15.45% / **0.882** / -33.7%; RULES v1 on B136 OOS 5.94% / 0.576 / -21.2%; do-nothing control
(full-panel CAND20) OOS 12.49% / 0.892 / -20.1%.

| selector (n=20, pre-registered) | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | its cell's mean OOS Sharpe | its cell's 4b base rate | 4b |
|---|---|---|---|---|---|---|---|
| S0 do-nothing (full B136) | — | 12.49% | 0.892 | -20.1% | — | — | H2 |
| S1 IS-Sharpe argmax | k=20 d19 | 8.37% | 1.105 | -10.5% | 0.992 | 0.00 | CAGR |
| S2 DISPERSION (max IS sd) | k=20 d39 | 9.03% | 1.184 | -9.4% | 0.992 | 0.00 | CAGR |
| S3 COUNT (max IS n_elig) | k=80 d26 | 12.00% | 0.953 | -19.6% | 0.939 | **0.46** | **—** |
| S4 random sub-panel | k=40 d35 | 10.30% | 0.984 | -17.6% | 0.994 | 0.34 | CAGR |

**S3's 4b pass is the cell's base rate, not information.** It lands in the (k=80, n=20) cell where **46% of
RANDOM sub-panels pass 4b**, and its OOS Sharpe of 0.953 is +0.014 against that cell's mean of 0.939 — a
fifth of the cell's own dispersion (sd 0.063). S1 and S2 both land in the k=20 cell, whose CAGR floor fails
in **50 of 50** draws, and are killed by it despite the highest OOS Sharpes in the table. Selector
correlations over the 150 sub-panels: Spearman(IS Sharpe, OOS Sharpe) +0.217, **Spearman(IS sd, OOS Sharpe)
+0.194, Spearman(IS n_elig, OOS Sharpe) -0.262** — the count selector points the wrong way out of sample.
The secondary n=5 block agrees: every selector fails 4b, S3 on H1 and DD.

## What this run establishes

1. **Idea 73's +0.964 is real and reproduces exactly, and it is not about candidate count.** Holding n fixed
   while the pool grows silently deepens the quantile the book takes; at matched q the effect is gone.
2. **Dispersion pays nothing at matched count** (|t| ≤ 1.98 in the pooled fit, sign negative in 7 of 9
   cells) — an independent, within-panel confirmation of idea 73's KILL, now free of its confound.
3. **The gross selectivity payoff does not survive costs.** More selective = more gross spread but *worse*
   net Sharpe premium against equal-weighting the same pool, monotonically in k.
4. **Rule 8 gives no KEEP.** No selector beats the do-nothing control by more than its cell's noise; the one
   4b pass matches a 46% base rate; the only full-panel 4b passer is idea 10's pre-existing `B136/EWall`.

## Limitations, stated

- **Survivorship:** `universe_broad.json` is current constituents, one-directional. A random sub-panel
  inherits it in full, and the count selector S3 (max in-sample n_elig = "the names that were trending most
  in-sample") is exactly the selector survivorship flatters most — which makes its null result stronger, not
  weaker.
- The primary week set drops the 24.3% of weeks with fewer than 80 eligible names so that every cell is
  evaluated on identical days; the each-cell-own-weeks reading is reported beside it and tells the same story.
- Test B's fixed sub-panels match the count only in expectation (n_elig scales with k); Test A matches it
  exactly. The two agree on dispersion and disagree in sign on k only after costs, which is the point of 3.
- Two tuned parameters (k, n); all 900 gross and 300 book points reported.
