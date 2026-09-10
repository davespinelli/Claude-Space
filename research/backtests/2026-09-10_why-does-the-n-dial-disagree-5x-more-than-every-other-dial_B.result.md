# Idea 494 — why does the `n` dial disagree 5x more than every other dial? (lane B, 2026-09-10)

**Verdict: KILL of the queue's premise AND of the queue's own proposed statistic; the question
is ANSWERED by a third thing. `n` does NOT "move realised gross and concentration together" —
on lane B's own ladder the `n` dial moves realised gross by exactly 0.0000 (gross is pinned at
0.75 by construction) and moves only concentration; and concentration is not the driver either,
because `C/quantile` moves held-name count 11.37x (MORE than B/n's 10.99x) and disagrees 2/12.
Disagreement does track the CURVATURE gap the queue names — but the LEVEL gap beats it on every
reading (Spearman across the 11 dials +0.518 vs +0.937; logistic b +0.509 vs +1.395;
pseudo-R2 0.167 vs 0.332), and the specific mechanism is a SIGN FLIP in the level term: in
21 of 132 cells the IS Sharpe surface tilts toward one end of the dial and the IS CAGR surface
toward the other, and those cells disagree 71.4% against 12.6% everywhere else. On lane B's `n`
the two tilts are +0.687 (Sharpe wants WIDE) and -0.278 (CAGR wants NARROW), flipping in 8 of
12 cells. No KEEP, no memo, no RULES change; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.**

Script `2026-09-10_why-does-the-n-dial-disagree-5x-more-than-every-other-dial_B.py` (grid,
780 s) + `..._B_addendum.py` (a pure re-read of the parent's `.cells.csv`, no backtest re-run).
Outputs `.arms.csv` (732 rows — ALL grid points), `.cells.csv` (264 cells = 132 CAL + 132 MID),
`.geometry.csv` (2,700 per-arm z-surface rows), `.abstain.csv`, `.walkforward.csv`,
`.console.txt`, `_addendum.signflip.csv`, `_addendum.console.txt`.
10 bps per unit turnover, weights at close t applied at t+1, long only, no leverage, weekly base
cadence except on the cadence dial. PROTOCOL rule 8 throughout: both selectors see IS
2009-01-01..2016-12-31 only, OOS 2017-01-01+ read once.

## Design

The grid is idea 499's, re-run verbatim: 12 panels x 2 dial sets (lane B's 5 dials, the cloud
parent's 6) x their arms, at 10 bps, with CAL (protocol rule 8) and MID (sample midpoint) both
computed. Nothing about the backtests is new. What is new is the decomposition laid over each
cell. For a cell (panel, dialset, dial) and metric m in {IS Sharpe, IS CAGR}: order the arms
along the dial, map them to x in [-1,+1], z-score m across that cell's arms (so units and
height drop out and the fit is about SHAPE), and fit `z = b0 + b1*x + b2*q`, q = x^2
orthogonalised against {1, x}, reporting the STANDARDISED coefficients. **b1 is the LEVEL term**
(which end of the dial the surface prefers), **b2 the CURVATURE term** (interior peak or trough).
Then `LEVELGAP = |b1_S - b1_C|`, `CURVGAP = |b2_S - b2_C|`, and `SHAPEDIST` = the model-free RMS
distance between the two z-surfaces. A cell DISAGREES iff argmax IS Sharpe and argmax IS CAGR
pick different arms — idea 270's and idea 499's own definition, arm identity, no tie band.
Arm spacing is an ENUMERATED axis (ORD = equally spaced by arm order, headline because `EWall`
and `FREQ_*` have no numeric value; VAL = the dial's own value, log for n and cadence); both are
in `.cells.csv` and both give the same answer.

**Tuned parameters (PROTOCOL rule 4: max 2):** (1) the dial value inside a cell, chosen by each
selector on IS only; (2) the abstention threshold tau on CURVGAP, pre-registered ladder
{0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, inf}, every rung reported. dialset / panel / spacing / split
are enumerated axes, not tuned.

## Reproduction gate — PASS, to the cell, before anything new was read

| dial | reproduced | published (idea 499) | | dial | reproduced | published |
|---|---|---|---|---|---|---|
| B/n | **7/12** | 7/12 | | C/cadence | **6/12** | 6/12 |
| B/trim | **2/12** | 2/12 | | C/band | **5/12** | 5/12 |
| B/cadence | **1/12** | 1/12 | | C/volcap | **3/12** | 3/12 |
| B/gross | **1/12** | 1/12 | | C/quantile | **2/12** | 2/12 |
| B/volgate | **1/12** | 1/12 | | C/n | **1/12** | 1/12 |
| | | | | C/gross | **0/12** | 0/12 |

Pooled B 12/60, C 17/72 — idea 499's headline exactly. Every number below sits on that grid.

## 1. The queue's premise is dead, two ways

| dialset | dial | rate | gross_range | nheld_ratio |
|---|---|---|---|---|
| B | **n** | **0.583** | **0.0000** | 10.99 |
| C | cadence | 0.500 | 0.0000 | 1.00 |
| C | band | 0.417 | 0.0168 | 1.04 |
| C | volcap | 0.250 | 0.0122 | 1.96 |
| B | trim | 0.167 | 0.0107 | 1.02 |
| C | **quantile** | **0.167** | 0.0085 | **11.37** |
| B | cadence | 0.083 | 0.0000 | 1.00 |
| B | **gross** | **0.083** | **0.7474** | 1.00 |
| B | volgate | 0.083 | 0.0117 | 1.91 |
| C | **n** | **0.083** | 0.0000 | **8.95** |
| C | gross | 0.000 | 0.4690 | 1.00 |

* **`n` does not move realised gross at all.** Both `n` ladders hold gross fixed by
  construction; measured over the sample, `gross_range` is 0.0000 on both. The dial that does
  move gross (B/gross, range 0.747) disagrees 1/12, and C/gross (0.469) disagrees 0/12.
* **Concentration alone does not do it either.** `C/quantile` spreads held-name count 11.37x —
  wider than B/n's 10.99x — and disagrees 2/12; `C/n` at 8.95x disagrees 1/12.
* As covariates in a logistic on all 132 cells: **premise-only pseudo-R2 0.044** against
  **geometry-only 0.362**, and `gross_range` enters with the WRONG SIGN (-0.736). Cell-level
  `rate ~ nheld_ratio` is r +0.070, panel-clustered permutation **p 0.391** — not distinguishable
  from noise.

## 2. Curvature is real but second; the LEVEL term is the story (ORD, CAL, 10 bps)

| statistic | Spearman across the 11 dials | cell-level r | perm p | logistic b (both in) | 1-covariate pseudo-R2 |
|---|---|---|---|---|---|
| **CURVGAP** (the queue's ask) | +0.518 | +0.442 | 0.0000 | **+0.509** | 0.167 |
| **LEVELGAP** | **+0.937** | **+0.625** | 0.0000 | **+1.395** | **0.332** |
| SHAPEDIST (model-free) | +0.933 | +0.665 | 0.0000 | — | — |

So the queue's statistic is not nothing — CURVGAP survives a panel-clustered permutation at
p < 1e-4 and keeps a positive coefficient with LEVELGAP in the model — but it is the smaller
half of the shape difference, and SHAPEDIST (which needs no parabola at all) matches LEVELGAP,
which says the quadratic term is adding little. Permutations shuffle disagreement labels WITHIN
each panel, so a panel's own overall disagreement level is held fixed under the null.
VAL spacing gives the same ordering (+0.527 vs +0.839; b +0.569 vs +1.405), as does the MID
split (r +0.419 vs +0.680).

## 3. The actual mechanism: the two surfaces tilt toward OPPOSITE ENDS of the dial

| dialset | dial | rate | SIGNFLIP(b1) | b1_S | b1_C | SIGNFLIP(b2) |
|---|---|---|---|---|---|---|
| B | **n** | 0.583 | **8/12 = 0.667** | **+0.687** | **-0.278** | 3/12 |
| C | cadence | 0.500 | 7/12 = 0.583 | -0.155 | +0.593 | 1/12 |
| C | band | 0.417 | 1/12 | +0.698 | +0.936 | 2/12 |
| C | volcap | 0.250 | 0/12 | +0.281 | +0.434 | 5/12 |
| B | trim | 0.167 | 2/12 | +0.618 | +0.871 | 4/12 |
| C | quantile | 0.167 | 2/12 | +0.306 | +0.279 | 2/12 |
| B | cadence / gross / volgate | 0.083 | 0/12 each | — | — | 4-7/12 |
| C | n | 0.083 | 1/12 | +0.296 | +0.226 | 0/12 |
| C | gross | 0.000 | 0/12 | +0.996 | +1.000 | 7/12 |

**21 of 132 cells flip the sign of the level term; 15 of those 21 disagree (71.4%), against
12.6% of the other 111.** Cell-level r +0.520 at permutation p 0.0000; a one-covariate logistic
on SIGNFLIP alone reaches pseudo-R2 0.214. The curvature sign flip is worth nothing at all:
r **-0.0003, p 1.0000**.

On lane B's `n` this is concrete and readable: **IS Sharpe tilts toward the WIDE end (+0.687) and
IS CAGR toward the NARROW end (-0.278)**, so the two selectors walk to opposite ends of the same
ladder — which is exactly idea 499's observation ("5 of its 7 disagreements are S_SHARPE picking
`EWall` or a wide FWD against S_CAGR picking FWD5") restated as one number. The only other dial
with a large flip rate is `C/cadence` (7/12), which is idea 499's "CAGR wants a slower book"
shape, likewise now a single statistic. **The 5x is a sign disagreement about direction, not a
disagreement about the shape of an interior optimum.**

## 4. Does `n`'s excess survive the geometry? YES — and `band`'s does not

Logistic on CURVGAP + LEVELGAP only, then each dial's observed rate against the fitted rate:

| dialset | dial | observed | geometry-predicted | residual |
|---|---|---|---|---|
| C | band | 0.417 | 0.190 | **+0.226** |
| C | volcap | 0.250 | 0.171 | +0.079 |
| C | quantile | 0.167 | 0.127 | +0.039 |
| C | cadence | 0.500 | 0.492 | +0.008 |
| **B** | **n** | **0.583** | **0.617** | **-0.034** |
| ... | ... | ... | ... | ... |
| B | volgate | 0.083 | 0.161 | -0.077 |

Mean |residual| 0.064. **The `n` dial is one of the best-explained dials on the board** — its
observed 58.3% is what two shape statistics predict for it — so there is no residual "n effect"
left to explain once the surfaces are described. The dial the geometry does NOT explain is
`C/band` (+0.226), which is a new open question, not this one.

## 5. PROTOCOL rule 8 walk-forward — the geometry buys no capital (OOS 2017+, read once)

CURVGAP is an IS-only quantity, so it can be used as an ABSTENTION rule: if CURVGAP > tau, refuse
to tune the dial and hold the cell's DONOTHING arm; else take S_SHARPE's IS pick. Means over the
132 CAL cells, all eight pre-registered rungs reported:

| tau | took / 132 | OOS Sharpe | OOS CAGR | OOS MaxDD | arm passes 4a | arm passes 4b |
|---|---|---|---|---|---|---|
| 0.00 (= always abstain, DONOTHING) | 0 | **0.8071** | 8.17% | -24.49% | 0 | 8 |
| 0.25 | 106 | 0.8042 | 8.67% | -25.61% | 3 | 15 |
| 0.50 | 127 | 0.8037 | 8.71% | -25.61% | 4 | 16 |
| 0.75 | 130 | 0.7999 | 8.73% | -25.66% | 4 | 15 |
| 1.00 / 1.50 / 2.00 / inf (= never abstain, S_SHARPE) | 132 | 0.8005 | 8.74% | -25.65% | 4 | 15 |

Comparands on the same cells: **S_CAGR 0.7805 / 8.77% / -26.42%**, **RULES v2 (live)
0.9194 / 7.00% / -14.38%**, **RULES v1 0.4637 / 5.48% / -25.70%**, **SPY 0.8815 / 15.44% /
-33.72%**. The whole ladder spans 0.7999-0.8071 of OOS Sharpe — a range of 0.007, smaller than
the S_SHARPE/S_CAGR gap it is supposed to arbitrate, and its best rung is the corner that never
tunes anything. **No 4a** (every rung is below the live book's 0.9194 OOS Sharpe) and **no 4b**
(every rung is below SPY's 0.8815 OOS Sharpe, failing the OOS leg outright, before the DD and
CAGR legs are read). Picking tau on OOS would land on tau = 0, i.e. do nothing — reported as
oracle headroom only, not as a rule-8 result.

Both KEEP paths over EVERY arm in the grid: **CAL 4a 12/696, 4b 46/696; MID 4a 16/696,
4b 42/696.** All 12 CAL 4a passers are `trim`/`band` arms on SMALL439 and the seeded sub-panels
(the same arm priced twice under lane B's and the cloud's names), none on a `n` arm, and none of
them is a claim this idea makes.

## What the record should carry forward

1. Idea 270's "`n` disagrees 5x" is **not** about gross, and not about concentration. It is a
   **direction conflict**: on the n ladder IS Sharpe prefers wide books and IS CAGR prefers
   narrow ones, so the two selectors leave from opposite ends.
2. The reportable statistic is **SIGNFLIP(b1)** — do the two IS surfaces tilt the same way? —
   at 71.4% vs 12.6% disagreement, ahead of both LEVELGAP and the queue's CURVGAP.
3. Curvature is a real but secondary term, and **curvature SIGN is worthless** (r -0.0003).
4. None of this is worth capital: the abstention rule built on it moves OOS Sharpe by 0.007 and
   loses to both the live book and SPY at every rung.

**Caveats.** "Dial set" still bundles book form, ranking key, eligibility legs and arm list
(idea 499's caveat, unchanged); the decomposition describes the surfaces, it does not unbundle
what generated them. Quadratic R2 averages 0.58-1.00 by dial and is written per cell, so
poorly-described surfaces are visible rather than silently treated as parabolas. SIGNFLIP is
undefined-ish when a tilt is near zero; no tie band is used, matching the parents' arm-identity
convention. SURVIVORSHIP: B136 / BSTK100 are current constituents of a current screen and
SMALL439 is the 483-name sub-$2B panel with the 44 tickers whose `max_1d_move >= 1.0` dropped
first; the 8 seeded sub-panels inherit that bias. No network was used.
