# Idea 310 — is-EVOL-the-real-survivor-not-DISP (cloud, 2026-09-09)

**ANSWERED / EVOL IS THE STABLE ONE, DISP IS NOT — and idea 284's stratum is a ±2σ outlier of
both distributions, though removing it never flips the ordering. KILL for tradability: neither
direction survives the draw-wise walk-forward, 0/324 on both KEEP paths.**

## Design
Re-fit of the within-stratum partials from idea 293's committed 540-panel artefact (9 strata of
60 seeded draws; the 5 NAMED panels excluded from every fit). Two dials only: **control set**
(REC = the other three characteristics, the record's own; PLUSN = + `n_elig`; MINIMAL = breadth
and corr only, so `disp` and `evol` never control each other) × **estimator** (RANKPART = the
record's rank-partial; OLSZ = OLS t on z-scored ranks). 9 strata × 3 books × 4 characteristics ×
6 settings = **324 fitted partials, all reported**.

Gates: **G1** the REC/RANKPART re-fit reproduces idea 293's committed `rho_partial` on all 108
rows to **9.7e-17**; **G2** the (q 0.500, k 40) cell reproduces idea 284's published disp
+0.264/+0.247/+0.261 and evol −0.126/+0.031/−0.073 to **5.3e-04**; **G3** 9 × 60 draws, no NAMED
panel in any fit.

## What the numbers say

**B1/B2 — evol is stable in sign and size; disp is not, in every one of the six settings.**

| setting | disp mean (sd) | disp sign-hold | evol mean (sd) | evol sign-hold |
|---|---|---|---|---|
| REC / RANKPART (the record's) | +0.0046 (0.151) | **9/27** | +0.1551 (0.122) | **25/27** |
| REC / OLSZ | −0.0106 (0.224) | 18/27 | +0.2189 (0.182) | 25/27 |
| PLUSN / RANKPART | +0.0088 (0.148) | 9/27 | +0.1564 (0.124) | 25/27 |
| PLUSN / OLSZ | −0.0035 (0.218) | 18/27 | +0.2210 (0.183) | 25/27 |
| MINIMAL / RANKPART | +0.1469 (0.126) | 21/27 | +0.2104 (0.097) | **27/27** |
| MINIMAL / OLSZ | +0.1512 (0.128) | 21/27 | +0.2120 (0.095) | **27/27** |

|mean|/SD: evol **1.20–2.24** (clears the pre-registered bar of 1 everywhere), disp **0.02–1.18**
(clears it only under MINIMAL). By the pre-registered sign bar (≥24/27) evol is stable in all six
settings and disp in none. `corr` is stable too (−0.2180, 27/27 under the record's estimator);
`breadth` is not (21/27, |mean|/SD 0.77) — idea 284's zero holds.

**The mechanism runs the opposite way to idea 284's reading.** Moving from REC to MINIMAL — the
only change being that `disp` and `evol` stop controlling each other — lifts disp from +0.0046 to
+0.1469 and its sign-hold from 9/27 to 21/27, while evol barely moves (+0.1551 → +0.2104, 25/27 →
27/27). So `evol` mediates `disp`, not "evol is mediated by the other two". Eligible-set vol is
the carrier; dispersion is largely its shadow.

**B3 — the disagreement is not one cell in the ordering, but idea 284's cell is a genuine
outlier.** Leave-one-stratum-out: **no** single stratum's removal flips the evol > disp mean
ordering, in any of the six settings — so idea 293's headline never depended on the (q 0.500,
k 40) cell. But that cell is where the two claims part: disp there is +0.2572 against a
other-24 mean of −0.0270 (sd 0.128, **z +2.22**), evol is −0.0562 against +0.1815 (sd 0.098,
**z −2.42**), and it is the only cell in the grid where evol takes the minority sign in more than
one book (1/3 books hold the grid sign there, 24/24 elsewhere). Idea 284's headline is a correct
description of the one stratum it measured and an unrepresentative one of the other eight.

**B4 — neither estimate replicates across seed halves.** Refitting on seeds 0–29 vs 30–59, sign
agreement is evol 18–20/27 and disp 13–19/27, against 13.5/27 for a coin. Stability *across
strata* is not stability *within* one: 30 draws cannot pin either sign.

**B5 — rule 8, both directions.** Time: characteristics IS-only (≤ 2016), every book metric OOS
(≥ 2017). Draw: the selector direction is fit on seeds 0–29 and applied once to seeds 30–59.
Mean OOS Sharpe of the picks — evol **0.6624–0.6675**, disp **0.5588–0.6215** — against the
do-nothing anchor (mean OOS Sharpe of the 30 unseen draws) **0.6715**: *both lose to doing
nothing*, evol by less. Beats-anchor counts: evol 13–15/27, disp 9–12/27. Beats SPY 4/27 (evol),
2–3/27 (disp); beats RULES v2 5/27 and 3/27. Mean OOS CAGR 9.13–9.18% (evol) and 7.19–8.17%
(disp) against SPY OOS 15.45% and RULES v2 OOS 6.56%; mean OOS MaxDD −28.8% to −30.1% against
SPY −33.72% and RULES v2 −13.68%.

**B6 — both KEEP paths.** **4a 0 / 324, 4b 0 / 324.** The 4b bars fail on DD in 318 of the 324
selected panel-books (154 fail all five). Base rate over the pool the selector draws from: 4b
clears on 39 of 1,620 panel-books (**2.4%**) — so the selectors did not merely fail to beat the
base rate, they picked below it.

## Verdict
**ANSWERED for the queue's question — `evol` is the survivor, `disp` is not** — with the sharper
finding that disp's apparent survival in idea 284 is an artefact of the control set: it survives
only when evol is removed from the controls, never the reverse. The 284/293 disagreement is not
caused by that cell in the ordering sense (no leave-one-out flip) but is entirely explained by
it in the claim sense: (q 0.500, k 40) is a ~2.2–2.4σ outlier in both characteristics and the
only cell where evol changes sign.

**KILL as anything tradable.** Both selectors lose to the do-nothing anchor out of sample, and
0 of 324 selected panel-books clears either KEEP path. The record should carry `evol` as the one
within-stratum characteristic whose *direction* is stable (higher eligible-set vol → higher OOS
Sharpe within a fixed cap mix, the reverse of the pooled sign), and should stop quoting idea
284's `disp` survival without naming its control set and its single stratum.

## Caveats
SURVIVORSHIP: the panels are drawn from SMALL439 and BSTK100, both current constituents of their
screens, so every panel's return level is inflated and both KEEP columns inherit that whole
(the 44 SMALL439 tickers with `max_1d_move >= 1.0` were already dropped by idea 293). The fit
inputs are idea 293's committed panel artefact, so this run inherits its construction verbatim —
including its vintage — and tests the estimator, not the panel build. The within-stratum ordering
is a within-corpus regularity, never a tradable edge; B5/B6 are what settle that.
