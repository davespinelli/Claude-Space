# Idea 124 — book-size floor for any quoted price

**Cloud lane, 2026-09-07. Verdict: KILL — there is NO book-size floor to state. The admissible
share is NOT monotone in n under any reading (R3 FALSE at all four tau; 2, 3, 2 and 1 of 5 ladder
steps go DOWN on the published / u56 / broad / all-rows readings), no rung reaches 1.00 (R1 =
None) and the first rung reaching 0.90 is ALL — the whole panel. Worse for the queue's own
phrasing: TOP20, the rung "~20 names" would enshrine, is the WORST non-V1u rung on the ladder
(0.551 published-share, against TOP5's 0.846 and TOP40's 0.885), and it is the worst in BOTH
universes. My pre-registered P1 is REFUTED. P3 is CONFIRMED and is the run's real finding: idea
122's V1u failures are the VOL SCALER, not the 5-name count — TOP5 holds the same 5 names at the
same 0.15 weight and fails the panel axis 0 times against V1u's 24, a +0.456 gap in admissible
share. Rules unchanged. One 4b KEEP-candidate by-product, PARK-recommended (memo written).**

Script `2026-09-07_book-size-floor-for-any-quoted-price_cloud.py`; `.console.txt` (final run,
bootstrap draws reloaded from the committed CSV) and `.console_bootstrap.txt` (the run that
computed the 8,960 draw-rows, with its timings); data `.grid.csv` (224 rows), `.bootstrap.csv`
(8,960 rows), `.d3.csv`, `.walkforward.csv`.

## Pre-registration

Idea 122's 3-axis sign test is adopted VERBATIM with its own settings, so this run cannot pick
its own bar: **D1** dMaxDD > 0 at every rung in {0, 5, 10, 25} bps; **D2** dMaxDD > 0 in BOTH
2009-2016 and 2017-2026; **D3** dMaxDD > 0 in at least tau of 40 name-subsample draws that delete
q of the panel, signals recomputed on the sub-panel. ADMISSIBLE = D1 & D2 & D3.

The new axis is one dial: **TOPn** holds the top n names of idea 94's plain composite at
`GROSS/n` each, so gross is 0.75 at every rung and only the NAME COUNT moves. n in
{3, 5, 10, 20, 40, ALL}. n = 20 nests idea 94/122's TOP20 exactly; n = ALL nests its EWall
exactly. **V1u** (idea 94's 5-name book: composite DIVIDED by sqrt(vol20), 0.15 per name) is
carried as a reference book, not a rung — TOP5 differs from it only by the vol scaler.

**Tuned: exactly two — n and tau {0.80, 0.90, 0.95, 1.00}.** q is FIXED at 0.10 (ideas 119/122's
own headline) and the sub-panels are drawn by consuming idea 122's rng in ITS order, so the
q = 0.10 draws are bit-for-bit its published draws. Universe {56, 136} and rung {10, 25} bps are
REPORTED axes; all 224 rows are printed and committed.

## Reproduction gates — 3 of 3, before any new number was read

| gate | result |
|---|---|
| G1 `TOPn(20)` nests TOP20 and `TOPn(ALL)` nests EWall, over all 11 (gate, conv) variants, both panels | max\|diff\| **0.000e+00** |
| G2 my TOP20 / ALL / V1u grid rows vs idea 122's committed `signtest.csv` (8 columns x 64 rows each) | **8.9e-16 / 1.8e-15 / 1.8e-15** |
| G3 my D3 draw fractions vs idea 122's committed `d3.csv` at q = 0.10 (32 arms each) | **0.000e+00 / 0.000e+00 / 0.000e+00** — the sub-panels are its published draws |

## [A] The price list by book size

| book | published rows | median rate | median dMaxDD | median dCAGR |
|---|---|---|---|---|
| TOP3 | 37/64 | 0.806 | 5.92 | 8.16 |
| TOP5 | 26/64 | 0.996 | 6.95 | 7.02 |
| TOP10 | 40/64 | 0.683 | 4.99 | 3.37 |
| TOP20 | 49/64 | 0.465 | 3.83 | 1.58 |
| TOP40 | 52/64 | 0.389 | 5.74 | 2.14 |
| ALL | 48/64 | 0.505 | 6.92 | 3.82 |
| V1u | 41/64 | 0.090 | 2.27 | 0.14 |

## [B] The queue's question: admissible share by book size

| book | pub | tau=0.80 | tau=0.90 | tau=0.95 | tau=1.00 | D1 only | D2 only | D3@0.90 |
|---|---|---|---|---|---|---|---|---|
| TOP3 | 37 | 0.703 | 0.649 | 0.486 | 0.432 | 0.973 | 0.703 | 0.811 |
| TOP5 | 26 | 0.846 | **0.846** | 0.846 | 0.769 | 1.000 | 0.846 | **1.000** |
| TOP10 | 40 | 0.650 | 0.650 | 0.650 | 0.600 | 1.000 | 0.675 | 0.950 |
| TOP20 | 49 | 0.551 | **0.551** | 0.490 | 0.490 | 1.000 | 0.551 | 1.000 |
| TOP40 | 52 | 0.885 | 0.885 | 0.885 | 0.885 | 1.000 | 0.962 | 0.923 |
| ALL | 48 | 0.979 | **0.979** | 0.958 | 0.958 | 1.000 | 0.979 | 1.000 |
| V1u | 41 | 0.537 | 0.390 | 0.390 | 0.293 | 0.878 | 0.585 | 0.415 |

Failure counts among published rows (D1 / D2 / D3@0.90 / any): TOP3 1/11/7/13, TOP5 0/4/0/4,
TOP10 0/13/2/14, TOP20 **0/22/0/22**, TOP40 0/2/4/6, ALL 0/1/0/1, V1u **5/17/24/25**.

**The binding axis is D2 — the WINDOW — not the panel.** P2 is refuted: on these large-cap
panels the cost axis is free everywhere except V1u (5 rows), the panel axis is free at n >= 5
except TOP40's 4 rows, and every rung's failures are dominated by the denominator changing sign
between the two halves of the sample. At TOP20 that is 22 of 22 failures.

## [B2] Two robustness readings, and a selection effect worth naming

| book | published share | ALL-rows share | u56 pub | broad pub |
|---|---|---|---|---|
| TOP3 | 0.649 | 0.375 | 0.889 | 0.421 |
| TOP5 | 0.846 | 0.344 | 1.000 | 0.714 |
| TOP10 | 0.650 | 0.406 | 0.864 | 0.389 |
| TOP20 | 0.551 | 0.453 | 0.818 | 0.333 |
| TOP40 | 0.885 | 0.719 | 1.000 | 0.786 |
| ALL | 0.979 | 0.734 | 0.958 | 1.000 |

spearman(rung, share) = +0.600 published, +0.943 all rows, +0.116 u56, +0.486 broad; down-steps
2 / 1 / 3 / 2 of 5 — **not monotone under any of the four**. The two readings disagree because
idea 94's own 0.10 pp publication floor is a **selection filter that favours the narrow books**:
TOP5 publishes only 26 of 64 rows, and the ones that survive the floor are exactly those with a
large \|dMaxDD\|, hence the stable ones. Read over all rows the small books collapse to
0.34-0.45 and the ladder is nearly monotone with its jump between n = 20 and n = 40 — but even
there no rung reaches 0.90, so there is still no floor to state.

## [C] The floor: R1, R2, R3

| tau | R1 (share = 1.00) | R2 (share >= 0.90) | R3 monotone? | ladder |
|---|---|---|---|---|
| 0.80 | **None** | ALL | **False** | .70 .85 .65 .55 .88 .98 |
| 0.90 | **None** | ALL | **False** | .65 .85 .65 .55 .88 .98 |
| 0.95 | **None** | ALL | **False** | .49 .85 .65 .49 .88 .96 |
| 1.00 | **None** | ALL | **False** | .43 .77 .60 .49 .88 .96 |

The queue asked for "a number PROTOCOL can state instead of '~20 names'." **There is no such
number on this ladder.** The only rung that clears 0.90 is "every name in the panel", the shape
is non-monotone at every tau, and ~20 names is the ladder's worst rung. The defensible PROTOCOL
clause is therefore not a count at all but the axis that binds: *no rate may be quoted unless its
denominator's sign holds in BOTH halves of the sample* (D2), which alone would have blocked
22 of TOP20's 49 published rows and 70 of the 293 published rows here.

## [D] The V1u decomposition — the run's real finding

TOP5 and V1u hold 5 names at 0.15 each and differ ONLY by the 1/sqrt(vol20) factor in the
ranking. Admissible share: **TOP5 0.846 vs V1u 0.390 at the headline tau (gap +0.456)**; at
tau = 0.80 / 0.95 / 1.00 the gap is +0.310 / +0.456 / +0.477. Panel-axis failures: **TOP5 0,
V1u 24**. Cost-axis failures: **TOP5 0, V1u 5**. Idea 122's headline — "all 24 panel and all 5
cost failures are the 5-name V1u book" — is exactly reproduced here (G2/G3), and this run shows
the attribution to *five names* is wrong: the same five-name width without the vol scaler has
zero failures on both of those axes. What destabilises the denominator is dividing the score by
a volatility estimate, which makes the book's composition — and therefore its drawdown —
a function of the noisiest input in the stack.

## [E] Rule 8 walk-forward (idea 94's S1 selector; S2 = the same after the IS-only sign screen)

Mean OOS Sharpe: **S1 0.8686 (28 cells), S2 0.8547 (112)**. By book: TOP3 0.841, TOP5 0.891,
TOP10 0.856, TOP20 0.895, TOP40 **1.052**, ALL **1.136**, V1u **0.333** — the wide books win the
menu, the vol-scaled 5-name book is a disaster out of sample. The screen changes **0 / 2 / 8 / 14
of 28** picks at tau = 0.80 / 0.90 / 0.95 / 1.00, for mean dOOS Sharpe **+0.0000 / +0.0025 /
-0.0280 / -0.0300**: at its own headline setting the screen is a no-op, and tightening it costs
OOS Sharpe. That is idea 122's own conclusion (REPORT-ONLY, not a selector) confirmed on six new
books. The picked denominator's OOS sign held in **109/140** picks.

Best walk-forward cell, u56 / ALL / 10 bps: OOS Sharpe **1.203**, CAGR 13.41%, MaxDD -17.71%,
against its own control 1.136, RULES v2 1.285 and SPY 0.882. Worst, u56 / TOP3 / 25 bps under
S2(1.00): OOS 0.712, CAGR 11.39%, MaxDD -22.38%.

## KEEP paths, all 224 rows

**4a vs RULES v2 (live): 0/224 at both rungs.** (Against RULES v1, idea 94's own convention:
36/224 at 10 bps and 75/224 at 25 — the 4a verdict is entirely a question of which book is
"live", which is the idea-136 pathology again.) **4b: 34/224 at 10 bps, 16/224 at 25**, by book
0/2/1/9/13/9/0 at 10 bps for TOP3/TOP5/TOP10/TOP20/TOP40/ALL/V1u.

Best 4b row, u56 / **TOP40 + band3-rw** / 10 bps: CAGR 11.36%, Sharpe 1.211, MaxDD -15.66%,
halves 1.250/1.186, OOS 1.276; margins H1 +0.294, H2 +0.352, OOS +0.394, DD +4.57 pp, CAGR
+0.70 pp. It buys 5.91 pp of drawdown for 2.31 pp of CAGR — a rate of **0.390**, below idea 94's
static-gross lever at 0.57. Memo written, **PARK-recommended**: it is one row selected post-hoc
from 224, the rule-8 selector does NOT pick it at any tau below 1.00 (S1 takes `ebud-0.10`, OOS
1.151), and it fails 4b on broad (DD at 10 bps, H2+DD at 25).

## Caveats

(1) universe.json and universe_broad.json are current-constituent lists — **SURVIVORSHIP** — so
every absolute level is optimistic; this run reports within-cell differences and the stability of
a sign, both far less exposed, but a survivorship-free panel could still move which rows pass.
(2) idea 94's `rw` convention keeps the per-name weight at GROSS/n regardless of how many names
the gate admits, so at large n an `rw` arm de-grosses substantially — inherited verbatim and not
a choice of this run, but it means TOP40's `rw` arms are part exposure cuts. (3) The published-row
denominator changes with n (26 to 52 of 64), which [B2] prices directly. (4) The small panel is
not in this run: idea 94's price list, which the queue asks to re-price, is a large-cap list.
