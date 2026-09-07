# Idea 394 — is c*-widening a RISK-TIMING property, record-wide? (cloud, 2026-09-07)

**KILL of the proposed partition. "Widens c*" is NOT a property of what the overlay is timed
on, and it is not even stable across windows. Rules unchanged; no new KEEP (4a 0/126 at 0, 10
AND 25 bps; 4b 38/126 @0, 18/126 @10, 0/126 @25, and none of the 18 exceeds the standing
parent's own c* of 22.60 bps).**

## What was run

126 cells = 7 book-level overlay families x 3 dials x 3 gross rungs {0.50, 0.75, 1.00} x 2
panels (U56, B136). Parent fixed and never tuned: idea 40/41's book (eligible above the 200d
MA and vol20 < 0.60, ranked on the v1 composite WITHOUT the /sqrt(vol20) term, top
k = min(20, E_t) equal-weight at g0/k, weekly, t+1). Exactly two tuned parameters — the gross
rung and the overlay's dial. Panel, family, timing class and cost rung are census axes; every
level is reported in `.grid.csv`.

Every family uses idea 41's book-level convention verbatim (`r = m*r0`,
`turn = m*turn0 + |dm|*gross0.shift(1)`), so the ONLY thing that differs between arms is what
the multiplier `m` is timed on. Idea 335's two per-name families (MABAND, STOP) are excluded
by design: they change the convention as well as the timing variable.

| class | timed on | families (dial) |
|---|---|---|
| **R** | the book's OWN realised risk | VOLCAP (target 0.10/0.15/0.25), DDCTL (T 0.05/0.10/0.20) |
| **P** | the PANEL's state | BREADTH (depth 0.75/0.50/0.25 at B=0.40), NAMEFLOOR (F 10/20/30) |
| **X** | NEITHER — the new third class | CALCAD (May–Oct calendar, depth 0.75/0.50/0.25), TURNBUD (trailing-63d-turnover above its own expanding q-quantile, q 0.50/0.75/0.90), RANDOM (fixed-seed weekly Bernoulli(p), p 0.10/0.25/0.50) |

**Reclassification, pre-registered.** QUEUE.md lists "name-count floor" under the third class.
It is not one: gate G10 measures corr(E_t, panel breadth) on U56 at pearson **+0.993**,
spearman **+0.978** — NAMEFLOOR is a monotone transform of the same variable BREADTH is timed
on. It is filed under P, and the partition test is reported BOTH ways.

Matched control (idea 335's, verbatim): a = mean(gross_overlay)/mean(gross_parent) applied as
a constant multiplier to the same parent — the plain gross dial held at the overlay's own
realised mean exposure. Only INFORMATIVE cells count (idea 393's fix): when both sides
already fail at zero cost the inequality is 0 <= 0.

## Gates (all before any new number)

`fast_bt` == `engine.backtest` on returns AND turnover at 0 and 25 bps **0.000e+00**; overlay
at OFF (m == 1) == parent on r, turnover and gross **0.000e+00**; matched control at a = 1 ==
parent **0.000e+00**; Sharpe invariance of the gross dial **2.220e-16**; c* bisection
determinism **0.000e+00**; matched-gross solve **0.000e+00**; RANDOM schedule reproducible and
panel-independent on all 4699 shared days (0 disagreements). **G11: idea 335's 54 overlapping
cells reproduce its committed `.grid.csv` to 3.553e-15** on c*(overlay), c*(control) and mean
gross — this run is a strict superset of idea 335's book-level arms, not a re-derivation.

4 of 126 cells are vacuous and flagged as such (DDCTL T=0.20 never fires at g0=0.50 on either
panel; the book's drawdown never reaches -20% there).

## The answer

**4b / full sample, informative cells only:**

| class | widens | rate | max widening |
|---|---|---|---|
| R own realised risk | 7/19 | 36.8% | +17.67 bps |
| P panel state | 4/13 | 30.8% | +18.25 bps |
| X neither (exogenous) | **2/21** | 9.5% | +1.41 bps |

One-sided Fisher p(R widens at least as often as observed vs X) = **0.0448** as filed, but
**0.2036** under the queue's own classification (NAMEFLOOR in X). A conclusion that flips on
where one family is filed is not a partition.

**And the window kills it outright.** The same three classes, IS (2008–2016) only:

| class | widens (IS) | max widening (IS) |
|---|---|---|
| R | 3/8 | +14.60 bps |
| P | 2/6 | +1.78 bps |
| X | **4/14** | **+22.75 bps** |

The single largest c* widening anywhere in the in-sample window is produced by a **calendar**
overlay — an arm timed on the date and nothing else — and it is larger than any risk-timed
arm's. On the OOS window the ordering inverts again: P widens 10/13 (76.9%) including
**BREADTH 6/6**, the very family idea 335 filed as "a panel-state gate widens it 0/6".

So idea 335's family split is a full-sample artefact: BREADTH's 0/6 becomes 6/6 out of sample,
and the third class widens most in-sample and least out of sample. "This overlay pays for its
own turnover" cannot be screened by timing class, and cannot be screened at all without
naming the window it was measured on.

**The one regularity that survives.** The fixed-seed RANDOM control — timed on nothing —
widens **0 of 17** informative cells in every window, and carries the most negative mean
dSharpe of any family (-0.1174 at 10 bps vs its matched control). An overlay that carries no
information never buys cost budget. That is a floor, not a partition: it does not distinguish
risk timing from calendar timing, both of which widen somewhere.

**Mechanism.** spearman(dSharpe@10, c* gap) over the 53 informative cells is **+0.623** (idea
335 got +0.336 on its own 39), and within-class it is +0.442 (R), +0.448 (X), -0.033 (P). The
association is with the overlay's Sharpe lift, not with what it is timed on — and the Sharpe
lift is available to a calendar overlay as readily as to a vol cap.

## Rule 8 walk-forward (dial chosen on 2008–2016 only, 2017–2026 read once)

84 IS-chosen arms (7 families x 3 rungs x 2 panels x 2 choosers: IS c*_4b and IS Sharpe@10).
The OOS identity holds 24/33 informative; widening by class OOS is P 6/8, R 3/11, **X 0/14**.

Best OOS Sharpe among the IS-chosen arms: U56 g0=1.00 BREADTH depth=0.75 → OOS **19.27% /
1.171 / -23.00%**, against its own parent 19.37% / 1.137 / -23.98%, RULES v2 9.53% / 1.285 and
SPY 15.45% / 0.882 / -33.72%. It fails 4b on the drawdown cap (-23.00% vs the -20.23% bar).

Class means OOS @10 bps: P 13.2% / 1.019 / -18.1%, R 13.3% / 1.014 / -18.2%, X 10.4% / 0.883
/ -19.2% — the exogenous class is the worst of the three on every OOS statistic, which is the
opposite of what a "third class that widens c*" would look like.

52/84 IS-chosen arms beat SPY's OOS Sharpe; **0/84 beat RULES v2's**; 22/84 beat their own
parent. 12/84 clear the full 4b bar set @10 bps, 0/84 clear 4a.

## KEEP census

4a **0/126** at 0, 10 and 25 bps. 4b 38/126 @0, **18/126 @10**, 0/126 @25. All 18 sit on U56
(17 of them at g0=0.75, the standing rung) and every one of them has c*(overlay) <= 22.603 —
the parent's own breakeven — so not one overlay buys the standing book a wider cost budget
than it already has. No new KEEP-candidate; nothing here is capital-worthy that the record
does not already hold.

## Caveats

universe.json (56) and universe_broad.json (136) are CURRENT-CONSTITUENT lists —
**SURVIVORSHIP**; absolute CAGRs are optimistic on both, and B136 CONTAINS U56, so two panels
is not two independent samples. Gross is capped at 1.00. c* is a breakeven, not a return.
Class sizes are unequal (R 2 families, P 2, X 3) and informative-cell counts are small, so the
Fisher p is reported as an exact count statistic, not an asymptotic claim.

Files: `.grid.csv` (126), `.parents.csv` (6), `.walkforward.csv` (84), `.console.txt`.
