# Idea 1160 (cloud lane, 2026-09-17) — is the MAXDD LEVEL the whole of the SMALL panel's REGIME-to-LENGTH difference?

**ANSWERED = NO. PREMISE REFUTED, and refuted by an identity rather than by a close call.**
Putting the U56 anchor book on SMALL's drawdown level — exactly, to 1e-9 pp, at gross 1.5054
— closes **none** of the ratio gap. Across 48 (construction, tape, donor, mechanism, ladder)
cells the median gap **widens by 8.5%**, and only 2 of 48 clear the pre-registered
half-the-gap bar. The reason is arithmetic: the ratio's two terms are homogeneous **in the
same degree**, so their quotient is scale-free.

Script: `2026-09-17_is-the-MAXDD-LEVEL-the-whole-of-the-SMALL-panel-s-REGIME-to-LENGTH-DIFFERENCE_cloud.py`
(standalone, offline, deterministic, 207 s). Console: `.console.txt`.

## Two things the run had to fix before it could answer anything

**1. A price vintage moved under the lane.** `data/prices.csv` gained the 2026-09-16 bar in
commit `6f1fcb1` between this session's first idea and this one. The record's committed U56
triples were computed on tapes ending 2026-09-15, so on the current file they no longer
reproduce to their own tolerances. Every tape here is therefore pinned at **2026-09-15** (a
no-op for B136 and SMALL, which end 2026-09-11) and both gates are run either way:

| gate | pinned | unpinned | inflation |
|---|---|---|---|
| G2 committed U56 W/H126/N=20 triple | 4.12e-05 | 1.62e-03 | **39x** |
| G3 SPY OOS triple | 1.70e-04 | 2.89e-03 | **17x** |

**One extra daily bar out of 4,705.** MaxDD — a max over the path — does not move at all
(G5 reproduces all three panels' levels to 7.2e-06); CAGR and Sharpe, means over the path, do.
This is idea 522's class and it is published here rather than absorbed.

**2. 1148/1157's ratio is not a single book's.** Its groups are the **four dial ladders**
(CADENCE, GROSS, H, N) and each value is a median over that ladder's rung books at one part of
the tape. A run that computes the anchor book's own ratio is computing a *different object*.
This run therefore carries **both** constructions everywhere: `C_POOLED` (1148/1157's, and
where the committed number lives) and `C_BOOK` (what the queue's words literally name).

## Gates — 8 of 8 PASS

| gate | what | value |
|---|---|---|
| G1 | fast runner ≡ `engine.backtest` | 1.39e-17 |
| G2 | committed U56 triple, pinned | 4.12e-05 |
| G3 | SPY OOS triple, pinned | 1.70e-04 |
| G4 | live RULES v2 MaxDD ≡ −12.05% | 4.95e-05 |
| G5 | 1157's committed MaxDD **levels**, all three panels | 7.17e-06 |
| G6a | 1157's `cells.csv` present with all 9 (ladder, panel) cells | 0.00e+00 |
| G6 | **1148/1157's SMALL/MAXDD R_MATCHED replayed BIT FOR BIT** — same groups, same seed (11481148), same loop order: replica **0.794259x** vs committed **0.794259x** | 1.50e-07 |
| G7 | swapping 1157's 200-random-pair statistic for the EXACT all-pairs one moves all 9 committed cells by < 5% | 5.00e-02 |

**G7 passes with essentially no margin** (4.9997e-02 against a 5e-2 bar; the binding cell is
F_FINE/U56, 0.7259 vs 0.6913). Read it as "the swap moves one cell of nine by a full 5%", not
as a comfortable pass. Every number this run *moves* uses the exact statistic, which carries no
Monte-Carlo term at all.

Anchor levels, re-derived: U56 −19.1276%, B136 −20.7403%, SMALL −35.8141% —
**SMALL is 1.8724x deeper**, the gap the queue points at.

## The test itself (T_OWN, target S_MAXDD)

Solved scale: U56 λ = 2.0072 (gross **1.5054**), B136 λ = 1.8394 (gross **1.3795**). Both hit
SMALL's −35.814% exactly.

| constr | donor | mech | ladder | R unscaled → scaled | SMALL | gap closed |
|---|---|---|---|---|---|---|
| C_POOLED | U56 | M_GROSS | F_1140 | 1.1495 → 1.1778 | 0.7943 | **−8.0%** |
| C_POOLED | U56 | M_GROSS | F_FINE | 0.7259 → 0.7217 | 0.5502 | +2.4% |
| C_POOLED | U56 | M_GROSS | F_FINER | 0.6454 → 0.6637 | 0.4699 | −10.4% |
| C_POOLED | B136 | M_GROSS | F_FINE | 0.7448 → 0.7444 | 0.5502 | +0.2% |
| C_BOOK | U56 | M_GROSS | F_FINE | 0.7400 → 0.8097 | 0.6118 | **−54.4%** |
| C_BOOK | B136 | M_RETURN | F_FINE | 0.6443 → 0.6415 | 0.6118 | +8.5% |

(all 192 rows in `.landing.csv`.)

**LANDING TALLY at the pre-registered 50% bar: 2 of 48 cells, median gap closed −8.5%.**
By construction: C_POOLED **0 of 24** (median −7.9%), C_BOOK 2 of 24 (median −12.3%). By
target: S_MAXDD 2 of 48, S_VOL **0 of 48** (median −2.0%), S_ULCER 2 of 48. A negative median
means the usual effect of matching the level is to push the donor *further from* SMALL.

## Why — the identity

The ratio is within-spread over between-spread, both in the statistic's own units. Elasticities
over the nine-rung λ ladder (d log x / d log λ; 1.000 would be exactly homogeneous of degree 1):

| constr | panel | LEVEL | within | between | **RATIO** |
|---|---|---|---|---|---|
| C_POOLED | U56 | +0.9043 | +0.7942 | +0.7791 | **+0.0152** |
| C_POOLED | B136 | +0.8963 | +0.8014 | +0.8003 | **+0.0011** |
| C_POOLED | SMALL | +0.7999 | +0.6938 | +0.6554 | **+0.0384** |
| C_BOOK | U56 | +0.9043 | +0.8297 | +0.7068 | +0.1229 |
| C_BOOK | B136 | +0.8963 | +0.7968 | +0.7843 | +0.0125 |
| C_BOOK | SMALL | +0.7999 | +0.6562 | +0.6343 | +0.0219 |

The ratio's elasticity is the **difference of the other two**, to four decimals
(0.7942 − 0.7791 = 0.0151 vs the fitted +0.0152). So H_HOMO reads NO — neither term is
homogeneous of degree 1, both sit near 0.79 — but that is not what the invariance needs. What
it needs is that the two are homogeneous **to the same degree**, and they are. Doubling the
exposure moves the drawdown *level* by +0.90 in log and the *ratio* by +0.015.

On the pooled construction U56's ratio crosses 0.726 → 0.722 as its MaxDD goes −19.13% →
−35.70%; SMALL's own ratio over the same λ ladder moves 0.550 → 0.570 as its MaxDD goes
−35.81% → −61.74%. **The two panels stay apart at every level either of them is put on.**

## The residual is not resolvable anyway (moving-block null, 200 draws, L=63)

| panel | λ | point | null median | 90% band | share sub-1 |
|---|---|---|---|---|---|
| U56 (scaled to SMALL's level) | 2.0072 | 0.8097 | 0.6940 | [0.4952, 1.1828] | 0.920 |
| B136 (scaled) | 1.8394 | 0.6456 | 0.6917 | [0.5257, 1.0191] | 0.925 |
| SMALL | 1.0000 | 0.6118 | 0.6083 | [0.4112, 0.8569] | 0.975 |

Both donors' bands **overlap** SMALL's. H_NULL reads NO: after matching the level, the
donor-vs-SMALL residual does not clear either book's own resampling noise — the same reading
1157 reached about the cell itself. Every panel is sub-1 in 0.92–0.98 of draws, so "sub-1" on
its own carries no information.

## Rule 8 walk-forward and both KEEP paths

λ chosen on the first half only (matched to SMALL's IS-half MaxDD), second half untouched.

| tape | donor | arm | λ (gross) | full CAGR / Sharpe / MaxDD | OOS CAGR / Sharpe / MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| T_OWN | U56 | ANCHOR | 1.000 (0.750) | 15.58% / 1.140 / −19.13% | 16.97% / 1.164 / −19.13% | **PASS** | FAIL |
| T_OWN | U56 | IS_MATCHED | 1.865 (1.399) | 29.17% / 1.141 / −33.61% | 31.88% / 1.166 / −33.61% | FAIL | FAIL |
| T_OWN | U56 | FULL_MATCHED | 2.007 (1.505) | 31.39% / 1.141 / −35.81% | 34.32% / 1.166 / −35.81% | FAIL | FAIL |
| T_OWN | B136 | ANCHOR | 1.000 (0.750) | 16.04% / 1.063 / −20.74% | 16.02% / 1.010 / −20.74% | FAIL | FAIL |
| T_MATCHED | U56 | ANCHOR | 1.000 (0.750) | 14.10% / 1.062 / −19.21% | 15.93% / 1.109 / −19.21% | **PASS** | FAIL |
| T_MATCHED | U56 | FULL_MATCHED | 2.009 (1.507) | 28.19% / 1.063 / −35.81% | 32.02% / 1.111 / −35.81% | FAIL | FAIL |

SPY OOS 15.21% / 0.871 / −33.72% (T_OWN), 15.33% / 0.877 / −33.72% (T_MATCHED); live RULES v2
OOS Sharpe 1.276 / MaxDD −12.05%. **4a 0 of 12. 4b 2 of 12, and both are the incumbent anchor
at its own gross 0.75** — leverage buys CAGR and drawdown in the same proportion, leaves Sharpe
untouched to three decimals (1.140 → 1.141), and loses 4b's drawdown cap immediately.

The ratio itself does not transfer across the split either: U56's reads **0.5482 in-sample
against 0.4344 out**, while SMALL's goes the other way, 0.5325 → 0.5621. Matching the level
changes the in-sample reading by 0.0018 (0.5482 → 0.5500 as gross goes 0.75 → 1.51).

## Hypotheses

| | | |
|---|---|---|
| H_MONO | \|MaxDD\| monotone in scale on every panel | **YES** |
| H_MATCH | a scale hits SMALL's level to < 0.01 pp everywhere | **YES** |
| H_LAND | **the queue's prediction** — the donor lands on a majority of cells | **NO** (2 of 48) |
| H_INVAR | the ratio is near scale-invariant (\|elasticity\| < 0.15) | **YES** |
| H_HOMO | both terms homogeneous of degree ~1 | **NO** (both ~0.79, not ~1.0 — and equality, not degree 1, is what carries the invariance) |
| H_NULL | the residual clears the moving-block band | **NO** (bands overlap) |
| H_CONSTR | same verdict on both constructions | **YES** |

## What this leaves standing

1157's *observation* is untouched: SMALL's ratio is lower than U56's and its drawdown level is
1.87x deeper. What is refuted is the *mechanism* it proposed. The level is not the carrier,
because a ratio of two same-unit spreads cannot see the level. Whatever separates SMALL from
U56 on this statistic is a difference in the **shape** of the drawdown distribution across
stretches, not its scale — and, per Arm 3, is not resolvable against either book's own
resampling noise at this tape length.

## Limits

- **SURVIVORSHIP (rule 9):** all three panels are current-constituent lists; the SMALL pool is
  the current output of a sub-$2B screen and is the most biased of the three.
- **LEVERAGE:** the matched books run at gross 1.22–1.51 with negative cash and **no financing
  charge**. They are diagnostics of a ratio's arithmetic, never proposed books; their CAGR
  figures would fall by the borrow rate on 0.5–0.75 of NAV if they were.
- The elasticities are OLS slopes through 9 λ rungs spanning 0.5–3.0; they are descriptive, and
  no interval is quoted for them (idea 1044/1048's point: an exponent on this tape carries a
  ~0.7-wide 90% interval, which is wider than the +0.0011 to +0.038 being reported — so the
  claim made here is the **identity** ratio ≈ within − between, verified to four decimals, not
  the individual slopes).
- 200 block draws resolve a band edge to roughly ±0.02, no finer.
- **NOTHING IS PROPOSED**, no memo, no candidate. RULES.md, PROTOCOL.md, scan.py, bot.py and
  baseline.py are untouched (rule 6).
