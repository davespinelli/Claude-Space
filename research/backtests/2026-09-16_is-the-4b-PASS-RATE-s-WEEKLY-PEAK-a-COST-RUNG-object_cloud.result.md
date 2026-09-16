# Idea 1059 — is the 4b PASS RATE's WEEKLY PEAK a COST-RUNG object?

**cloud lane, 2026-09-16.** Script `2026-09-16_is-the-4b-PASS-RATE-s-WEEKLY-PEAK-a-COST-RUNG-object_cloud.py`.
Two tuned dials: **cost rung {0, 10, 25, 50} bps × cadence {D, W, M, Q}** = 16 points, all reported.
Population is 968's verbatim census (6 mechanisms × 2 panels × the cadence's phase family P + the
canonical period-end = 12 / 36 / 132 / 384 books per cell), gross 0.75 headline with 0.50 / 1.00
printed and never selected on. 3,384 books × 4 rungs + 480 null books × 4 rungs = 15,456 rows.
**Gates 9 of 9 pass**, including G5, an exact cross-run of 968's committed pass-rate profile
(U56 0.333 / 0.833 / 0.205 / 0.044, B136 0.000 / 0.028 / 0.000 / 0.000; max|d| 4.55e-04).

## THE ANSWER: the peak MOVES, but not where the queue predicted, and never to Q

4b pass rate, U56 books, gross 0.75 (rows = rung, cols = cadence):

| cost | D | W | M | Q | argmax |
|---|---|---|---|---|---|
| 0 bps | **0.833** | **0.833** | 0.227 | 0.044 | D+W (tie) |
| 10 bps | 0.333 | **0.833** | 0.205 | 0.044 | W |
| 25 bps | 0.000 | **0.250** | 0.189 | 0.042 | W |
| 50 bps | 0.000 | 0.000 | **0.121** | 0.036 | M |

B136: W 0.139 / 0.028 / 0.000 / 0.000 across the rungs — the peak dies rather than slides.

- **H_SLIDE FAIL.** The queue's prediction was D at 0 bps and Q at 50 bps. Got a D+W **tie** at
  0 bps and **M** at 50 bps. Q is never the argmax on books at any rung, on either panel.
- **H_MOVE PASS.** The peak does move: D+W → W → W → M. PROTOCOL's 10 bps is what **breaks the
  D/W tie** — D falls 0.833 → 0.333 between 0 and 10 bps while W does not move at all. So the
  rung is decisive at exactly one boundary (D versus W) and is on a plateau for W itself.
- **H_PEAK FAIL.** Unimodal at 0 / 10 / 25 bps, multi-modal at 50 bps (the surface is nearly dead:
  max 0.121).

## THE MECHANISM: two legs bite from opposite ends and the crossing is what moves

Leg FAILURE share, U56 gross 0.75:

| leg | cadence | 0 bps | 10 | 25 | 50 |
|---|---|---|---|---|---|
| L_CAGR | D | 0.167 | 0.333 | 1.000 | 1.000 |
| L_CAGR | W | 0.167 | 0.167 | 0.333 | 1.000 |
| L_DD | M | 0.606 | 0.629 | 0.644 | 0.667 |
| L_DD | Q | 0.828 | 0.828 | 0.831 | 0.836 |

Annual drag at the rung: D 0 / 224 / 561 / 1121 bp, W 0 / 90 / 226 / 452, M 0 / 41 / 102 / 205,
Q 0 / 22 / 56 / 111.

Cost kills the FAST cadences through the CAGR floor and the H1 Sharpe leg (SPY pays no turnover
at any rung, so the whole ladder is a one-sided handicap). It barely touches the SLOW ones: L_DD's
failure share on M moves 0.606 → 0.667 over a 50 bps sweep, i.e. **6 pp for a 5x cost move**, which
is 968's "L_DD is a drawdown fact, not a cost fact" measured on the cost axis directly. The peak
sits where the rising CAGR-leg curve crosses the flat DD-leg curve, and that crossing can only walk
as far as M, because Q's DD leg is already failing 83% of its books at zero cost. **H_DRAG FAIL**
(the winning cadence's own drag is 90 / 226 / 205 bp/yr at 10 / 25 / 50 bps — a 2.50x spread, not a
constant drag budget).

## THE NULL: the peak is NOT a pure cadence-and-cost object

**H_NULL FAIL, at 0 of 4 rungs.** A gross-matched coin flip peaks at **Q at every positive rung**
(0.150 / 0.150 / 0.050) and at D+Q at 0 bps, while the books peak at W then M. The null's own
turnover (239/yr at D, 49.8 at W) makes every fast cadence unreachable for it at any positive cost,
so the null's argmax is just "the cheapest cadence". The books' weekly peak is therefore a
**selection × cadence** fact that the null does not reproduce — it is not explained by cost alone.

## RULE 8 (2009–2016 chooses, 2017–2026 read once), U56 gross 0.75, 10 bps

| book | IS pick | OOS best | OOS CAGR | OOS Sharpe | OOS MaxDD | full CAGR/Sharpe/MaxDD | halves |
|---|---|---|---|---|---|---|---|
| CAND20 | M | M ✓ | **17.53%** | **1.3061** | −19.51% | 15.28% / 1.2125 / −19.51% | 1.205 / 1.227 |
| R3_84 | M | M ✓ | 16.89% | 1.2686 | −19.61% | 15.11% / 1.1989 / −19.61% | 1.207 / 1.198 |
| MOMONLY | M | M ✓ | 15.18% | 1.1481 | −19.77% | 14.23% / 1.1415 / −19.77% | 1.217 / 1.087 |
| R3_55 | Q | M ✗ | 15.23% | 1.0370 | −28.18% | 14.42% / 1.0594 / −28.18% | 1.213 / 0.954 |
| NOR3 | M | M ✓ | 15.73% | 1.1802 | −20.24% | 14.16% / 1.1293 / −20.24% | 1.170 / 1.102 |
| BAND03 | M | D ✗ | 9.55% | 1.2234 | −14.38% | 8.87% / 1.1715 / −14.38% | 1.217 / 1.135 |

Comparands: **RULES v2 (live)** OOS 9.45% / **1.2762** / −12.05%, full 8.62% / 1.2007 / −12.05%,
halves 1.232 / 1.176. **SPY** OOS 15.21% / 0.8711 / −33.72%, full 15.10% / 0.8829 / −33.72%.

**H_RULE8 FAIL.** At PROTOCOL's own rung the IS-Sharpe chooser's pick clears the OOS reading of 4b
in **3 of 12** (panel, mechanism) cells (0.250), hit rate 0.750 on the OOS-best cadence. Both
IS-only choosers pick **M**, not the full-sample peak **W**, at 10 and 25 bps on both panels: the
weekly peak is **not findable in sample**. At 50 bps C_ISSHARPE's hit rate collapses to 0.167.

## KEEP paths

| panel | rung | n | 4b | 4a | both |
|---|---|---|---|---|---|
| U56 | 0 / 10 / 25 / 50 | 24 | 15 / 11 / 5 / 4 | 0 / 0 / 0 / 0 | 0 |
| B136 | 0 / 10 / 25 / 50 | 24 | 1 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 |

**4a is 0 of 48 at every rung** — every book that clears 4b does so by carrying 19–20% of drawdown
against the live book's 12.05%, exactly the trade PROTOCOL rule 4 was split to expose. The eleven
canonical-phase 4b passers at 10 bps are already-committed cells (U56 W CAND20/R3_55/R3_84/NOR3/
MOMONLY, U56 M CAND20/R3_55/R3_84/MOMONLY, U56 D R3_84/MOMONLY). **Nothing is promoted.**

## VERDICT

**KILL the queue's slide prediction** (peak never reaches Q at any rung, on either panel, at any
gross) and **KILL the cost-only reading of the weekly peak** (the gross-matched null peaks at Q at
every positive rung — 0 of 4 agreement). **CONFIRM** that 10 bps is a cadence chooser at exactly
one boundary: it removes D (0.833 → 0.333) and leaves W untouched, so 968's weekly headline is a
statement about the D/W margin at PROTOCOL's rung, not about weekly as such. **CONFIRM** L_DD's
cost-invariance directly (6 pp of failure share for a 5x rung move on M). Gross 0.50 inverts the
whole surface (B136 peaks at Q, U56 is empty), so the peak is not gross-robust either. Hypotheses
1 of 6, gates 9 of 9, nothing promoted.

Survivorship: U56/B136 are current-constituent panels; the bias is common to books and null and
flatters both the CAGR floor and the DD cap against SPY, which is a real index series.
