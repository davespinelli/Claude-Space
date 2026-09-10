# Idea 466 — re-read every chooser result on the OOS RANK of its constant arm (lane B, 2026-09-10)

**VERDICT: KILL of the queue's premise.** The record's degenerate menus are **NOT** constant on the
losing side. Idea 458's three published ranks are the 91.5th percentile of the very record they were
generalised to.

## The statistic
For each degenerate (file, panel) menu — one arm is the IS-Sharpe argmax in *every* cell — read the
constant arm's **normalised OOS rank** `u = (rank-1)/(n_arms-1)`, rank 1 = best OOS.
`u = 0.5` is the coin-flip null; **CONSTANT-ON-A-LOSER := u > 0.5**.

## Gates (all PASS, before any new number was read)
| gate | result |
|---|---|
| G1 458's census reproduced on its own corpus (files < 2026-09-09), its code imported by path | **121 degenerate (pub. 121) in 57 files (pub. 57), 15 control-won (pub. 15)** — exact. Denominator 572/196 vs published 566/194: +6 menus in +2 files dated 09-08 that landed after 458 ran |
| G2 rank convention (worst=1, best=0, MaxDD −0.10 above −0.30, all-tied=0.5) | PASS |
| G3 no IS/OOS column collision over the corpus | 0 collisions |
| G4 `fast_bt` vs `engine.backtest`, returns AND turnover, W and M | 3.331e-16 |
| G5 IS/OOS disjoint and exhaustive | IS 2009-01-13..2016-12-30 (2007d), OOS 2017-01-03..2026-09-09 (2434d) |

## R1 — the answer (458's frozen corpus, the queue's own 121 menus)
117 of the 121 degenerate menus publish an OOS Sharpe column.

| | n | mean u | median u | **loser share (u>0.5)** | u=1.0 | u=0.0 | t vs 0.5 |
|---|---|---|---|---|---|---|---|
| **degenerate** | 117 | **0.290** | 0.181 | **11.1%** | 3.4% | 29.9% | **−8.06** |
| non-degenerate control (modal IS winner) | 447 | 0.439 | 0.440 | 39.6% | 6.7% | 12.5% | −4.23 |

**Only 13 of 117 published chooser verdicts are constant-on-a-loser.** The constant arm beats the
median arm out of sample by 0.21 of the rank range, and beats the *non-degenerate* menus' modal
winner. Degeneracy is associated with a **better** OOS arm, not a worse one.

### Every P1 × P2 grid point (6 cells × 2 corpora × degenerate/control = 48 rows in `.grid.csv`)
P1 OOS metric ∈ {Sharpe, CAGR, MaxDD}; P2 aggregation ∈ {percell, pooled}. Frozen corpus,
degenerate menus: mean u **0.290 / 0.283** (Sharpe), **0.369 / 0.352** (CAGR), **0.532 / 0.532**
(MaxDD, t = +0.94/+0.89 — *at the null*). Today's 1,281-menu corpus: 0.271/0.246, 0.270/0.240,
0.484/0.473. **The claim fails on Sharpe and CAGR (sign reversed, t ≈ −8 to −16) and is a coin flip
on MaxDD, at every grid point and on both corpora.**

### Not a menu-width artefact
Frozen corpus by `n_arms`: 2 → mean u 0.346 (n 38), 3 → 0.166 (16), 4-5 → 0.441 (13), 6-10 → 0.234
(15), **11+ → 0.254 (35, loser share 11.4%, never u=1)**. The bucket comparable to 458's own 31-arm
menu is the *least* loser-like.

### Where 458's probe actually sits
| 458's published rank | u | census percentile |
|---|---|---|
| u56 31/31 | 1.000 | **96.6%** |
| broad136 22/31 | 0.700 | **92.3%** |
| SMALL439 7/31 | 0.200 | 51.3% |
| probe mean 0.633 | | **91.5%** |

## R2 — PROTOCOL rule 8, live prices, out of corpus
458's probe menu (control + 10 band-gated arms), cells = 30 seeded 60% sub-panel draws/panel
(seed 20260910), arm chosen on IS Sharpe 2009-2016 only, 2017-2026 read once, 10 and 25 bps.

- **No live menu is degenerate at all** (modal share 0.533-0.867, never 1.00): 458's 400/400 does
  not survive a change of cell definition.
- The modal arm's OOS rank **reverses by panel**: mean u 0.943/0.900 (u56, 10/25 bps), 0.587/0.327
  (broad136), 0.187/0.087 (small484). "Constant on a loser" is a u56 fact, not a record fact.
- The full-panel IS argmax ranks **2/11** OOS on u56, 8/11 then 3/11 on broad136, **1/11** on
  small484 — against 458's 31/31.

### The chooser as a real book (10 bps, both KEEP paths)
| panel | arm | halves (SPY) | OOS CAGR/Sharpe/MaxDD | SPY OOS | 4a | 4b |
|---|---|---|---|---|---|---|
| u56 | b0-g1.00-M | 1.258/1.178 (0.959/0.826) | 12.72% / 1.278 / −15.54% | 15.32% / 0.876 / −33.72% | **False** | **True** |
| broad136 | control | 1.235/1.024 (0.957/0.834) | 18.62% / 1.102 / −32.71% | 15.45% / 0.882 / −33.72% | False | False |
| small484 | control | 0.846/0.719 (0.891/0.858) | 15.65% / 0.734 / −45.75% | 15.45% / 0.882 / −33.72% | False | False |

RULES v2 halves: u56 1.231/1.180, broad136 1.229/0.984, small484 0.542/0.680.

**The one 4b pass is NOT a new KEEP candidate.** `u56 b0-g1.00-M` (11.96%/1.216/−15.54% full,
12.72%/1.278/−15.54% OOS) reproduces idea 458's own **PARK** arm and idea 467's convergent
reproduction of it to the third digit. 4a fails on the MaxDD leg (−15.54% vs RULES v2's −12.05%),
and the arm is picked by IS argmax over an 11-arm menu — the selection this very file shows carries
no reliable OOS information. It stays **PARK**.

## What the record should say
Idea 458's "the degenerate menus are constant on the losing side" is true of **its own probe menu
and of no one else's**: at 11.1% (Sharpe) it is a minority phenomenon, and the majority direction is
the opposite. Every downstream file that inherited 458's CAUTION on this ground should re-read it as
"a constant chooser is uninformative, not adverse". 458's separate and stronger finding — that the
IS degeneracy itself does not transfer (corr(D_is, D_oos) = −0.05) — is untouched by this and is
independently confirmed here: no live menu is degenerate under a different cell definition.
