# Idea 784 — does-the-ORIGIN-asymmetry-show-up-in-4b-PASS-RATES-not-just-the-premium
lane C, 2026-09-11 · `2026-09-11_does-the-ORIGIN-asymmetry-show-up-in-4b-PASS-RATES-not-just-the-premium_C.py`

## Answer

**It is NOT the premium re-expressed. It is a DRAWDOWN fact — and rule 8 says it is an
OUT-OF-SAMPLE-PERIOD fact that REVERSES in sample. KILL for capital.**

Idea 570's 11.84x pass-rate asymmetry (B 225/2592 vs S 19/2592) survives every attempt to
trace it back to the MA-gate selection premium, and dies the moment the legs are computed
inside 2011–2016 alone.

## Gates — ALL PASS

| gate | result |
|---|---|
| G0 metrics (numpy `mstats` vs `engine.metrics`) | **0.000e+00** (bar 1e-12) |
| G1 identity (`fast_backtest` vs `engine.backtest`) | **1.388e-17** (bar 1e-12) |
| G2 pool (573 names = B 134 + SMALL 439, 2010-01-04..2026-09-04, 4194 bars) | exact |
| G3 grid repro — idea 570's committed `.grid.csv`, **5184 of 5184 rows x 11 numeric columns** | **1.776e-15** (bar 1e-9), 0 verdict-string mismatches |
| G4 headline — its 4a 21 / 4b 244 / BOTH 1, side B 225 S 19, arm EWall 115 MA-RS 129, six binding-leg counts | **exact, all of them** |
| G5 comparand — one warm-up start across all matched frames | exact (2011-01-13) |

Two tuned parameters and no more: **BAR lambda in {0.60, 0.80, 1.00, 1.25}** (lambda = 1.00 is
PROTOCOL 4b verbatim) **x k in {18, 36, 72}**, all 12 points reported at three periods.
k=72 is infeasible at every finite tau (the S pool runs out of partners), so it exists only at
tau=inf — stated, not hidden.

## What the two sides look like (means over 2592 books each)

| side | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe | turnover |
|---|---|---|---|---|---|---|---|
| B | 13.02% | 1.0064 | −24.73% | 1.0203 | 1.0095 | 1.0488 | 3.38 |
| S | 9.05% | 0.7037 | −29.69% | 0.9476 | 0.5477 | 0.5698 | 4.06 |

Selection premium over the 216 matched draws: B −0.0420, S −0.2816, **gap +0.2396** — idea
570's headline mean, re-derived. The B side is shallower by **4.96 pp of drawdown** against a
cap of −20.23%, and wins the paired drawdown comparison in **76.9%** of the 2592 pairs.

## The decomposition — four independent readings, same answer

**1. Leave-one-leg-out (pooled, lambda = 1).** Full ratio **11.84x**.

| criterion | B | S | ratio |
|---|---|---|---|
| 4b (all five legs) | 225 | 19 | **11.84** |
| 4b without **DD** | 1453 | 519 | **2.80** (0.24x of full) |
| 4b without H1 | 247 | 19 | 13.00 |
| 4b without H2 | 228 | 19 | 12.00 |
| 4b without OOS | 225 | 19 | 11.84 |
| 4b without CAGR | 654 | 50 | 13.08 |
| SHARPE block only {H1,H2,OOS} | 1903 | 649 | **2.93** |
| LEVEL block only {DD,CAGR} | 251 | 19 | **13.21** |

Dropping the drawdown cap removes **76%** of the asymmetry. Dropping any Sharpe leg removes
**none of it** (1.00x–1.10x of the full ratio). The level block alone reproduces the whole
published number; the Sharpe block alone reaches 2.93x. Among books failing **exactly one**
leg, that leg is DD for 1228 of 1682 B books and 500 of 531 S books.

**2. The arm split.** The EWall arm applies **no gate at all** — zero selection, zero premium
by construction — and still passes **96 B vs 19 S = 5.05x**. The MA-RS arm passes 129 vs 0.
So the gate amplifies the asymmetry but does not create it: at least a 5x gap is there with
the premium switched off.

**3. Conditioning.** Crude odds ratio 12.87; across deciles of the book's own full-sample
Sharpe the Mantel-Haenszel OR is **7.63 (0.59x of crude)** — conditioning on return does not
remove it. (The same-decile-pairs variant is 1 pass vs 1 pass on 172 pairs, too thin to read,
and the MaxDD-decile row is a tautology check, not evidence: the DD leg is in the outcome.)

**4. The premium does not buy passes.** Across the 216 draws, premium gap vs pass gap:
Pearson **+0.0123**, Spearman **−0.0449**, permutation p **0.8506**. By premium-gap quartile
the pass gap is flat — 0.815 / 1.111 / 1.056 / 0.833 of 12 books per side, with the HIGHEST
premium quartile producing the SECOND-LOWEST pass gap.

Paired per-leg margins (positive = leg passes), lambda = 1, 2592 pairs, 20,000 sign-flips:

| leg | margin B | margin S | B−S | t | Cohen's d | perm p |
|---|---|---|---|---|---|---|
| H1 | +0.1296 | +0.0569 | +0.0727 | 11.60 | 0.32 | <5e-5 |
| H2 | +0.1518 | −0.3100 | +0.4618 | 64.78 | 1.32 | <5e-5 |
| OOS | +0.1668 | −0.3122 | +0.4790 | 66.72 | 1.36 | <5e-5 |
| DD | −0.0450 | −0.0946 | +0.0496 | 42.99 | 0.61 | <5e-5 |
| CAGR | +0.0313 | −0.0085 | +0.0398 | 34.60 | 0.77 | <5e-5 |

The Sharpe legs separate far more in *margin* (d 1.32/1.36) yet carry none of the pass gap —
because both sides clear them comfortably or miss them together; the **binding** leg is DD,
where B's margin is only 0.05 better and that is exactly where the bar sits.

## RULE 8

**WF-A — the asymmetry is an OOS-period fact and REVERSES in sample.** With every leg
recomputed inside one period (4-leg period-local 4b), the B/S ratio is **0.00–1.99 in IS**
(B passes FEWER than S at 9 of 12 points, e.g. 0.35 / 0.28 / 0.77 at lambda = 1) against
**2.90–293.00 in OOS**. The two periods point the same way at **2 of 11** defined points.
Per-leg failure rates say why: **in IS the B side fails the DD cap MORE often than the S side
(77.4% vs 65.7%)**; out of sample that flips (65.2% vs 85.3%) and B's H2 failure collapses to
12.7% against S's 71.8%. The published 11.84x is 2017–2026.

**WF-B — priced as a book.** IS pick (char=cvol, tau=0.05, k=18; IS 4b pass rate 0.1458):

| book | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|---|---|
| B-side (IS pick) | 13.15% | 1.0314 | −24.54% | 14.08% | 1.0502 | −24.54% | fails DD |
| S-side twin | 3.08% | 0.3047 | −22.62% | −0.03% | 0.0629 | −22.62% | fails all five |
| ORIGIN-BLIND control | 8.55% | 0.7645 | −22.07% | 7.71% | 0.6783 | −22.07% | fails 4 |
| INCUMBENT B136 MA-RS g0.75 W | 11.20% | 1.0450 | −20.12% | 11.97% | 1.0660 | −20.12% | **PASS** |
| RULES v2 U56 (live) | 8.66% | 1.2056 | −12.05% | 9.53% | 1.2851 | −12.05% | fails CAGR |
| SPY | 15.23% | 0.8890 | −33.72% | 15.45% | 0.8820 | −33.72% | — |

Decision books beat RULES v2 OOS **0/3**, beat SPY OOS **1/3**; **4a 0/3, 4b 0/3, BOTH 0/3**.
The B-side book correlates **0.9859** with the whole-B136 MA-RS gate the record already holds,
and is worse than it on drawdown (−24.54% vs −20.12%) and on OOS Sharpe.

## KEEP paths

Matched grid, 5184 books: **4a 21, 4b 244, BOTH 1** — idea 570 reproduced exactly (G4).
By side: B 4a 6 / 4b 225, S 4a 15 / 4b 19. Decision books **4a 0/3, 4b 0/3**.
A matched draw is a diagnostic panel, not a tradable rule, so nothing here is a capital
candidate whatever it passes. **No candidate, no memo, no rule change.**

## Hypotheses as pre-registered

| | verdict |
|---|---|
| H_PREM (i) Sharpe block carries it (bar: >= half the full ratio, 5.92) | **FALSIFIED** — 2.93 |
| H_PREM (ii) it is an MA-gate phenomenon (MA-RS > 2x EWall) | **HOLDS formally** (259 capped vs 5.05) **but EWall alone is 5.05x with zero selection** |
| H_DD drop-DD < 0.5x full AND drop-Sharpe > 0.8x full | **HOLDS** — 0.24x and 1.00x–1.10x |
| H_COND Sharpe-decile MH OR < half crude | **FALSIFIED** — 7.63 vs 12.87 (0.59x) |
| H_LINK premium gap predicts pass gap (\|rho\| >= 0.30) | **FALSIFIED** — Spearman −0.045, p 0.85 |

## Caveats stated

**SURVIVORSHIP:** both panels are current constituents; SMALL439 is the heavier screen and a
differential survivorship premium would push the same way as every number above. This design
controls the characteristic and the width, not the listing history — that is idea 782.
The asymmetry being a **drawdown** fact makes the survivorship channel *more* plausible, not
less: a current-constituent small-cap screen is exactly a population whose realised drawdowns
are understated, and the IS/OOS reversal is consistent with the S panel's composition being
kinder in the earlier window.
