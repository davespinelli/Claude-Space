# Idea 425 — the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt (lane C, 2026-09-08)

**ANSWERED. 2 of the flagged file's 9 LEADERBOARD rows can be reached by the floor at all, and
BOTH move — but neither changes a verdict. What the substitution does kill is a different,
CHANGELOG-level claim: "at a $1M ADV floor the published damage shrinks from -6.52 to -4.87 pp"
is a DOLLAR-floor artefact. At matched admission rate a share-volume floor leaves that damage at
-6.59 pp — slightly worse than no floor at all.**

Script `research/backtests/2026-09-08_the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt_C.py`;
outputs `.console.txt`, `.grid.csv` (576 points), `.ladder.csv`, `.maskdiff.csv`, `.rows.csv`,
`.walkforward.csv`, `.verdicts.csv`.

## What was on trial

Not a book. Idea 197's census flagged `adv_mask` in `2026-09-06_band-gate-on-small-panel_B.py`:

```python
dv = (px * vol).rolling(20).median();   admit iff dv >= floor
```

`px` is the auto-adjusted close, so the mask is not invariant under `px -> px @ diag(c)` — the
contamination enters the PANEL, not a score. The flag is correct about the CODE. It says nothing
about whether a published NUMBER moves, and that is the only thing that can force a correction.

## Design

Two tuned parameters, and only two: the floor INSTRUMENT (DV vs VOLSH) and its LEVEL. The level is
not fitted to any return — it is solved from an admission-rate identity, and the whole ladder is
printed. Everything else (panel, convention rw/dg, composition TREND/FULL, 9 arms, cost rungs
0/5/10/25 bps) is reported at every value and selected at none. **576 grid points, all printed.**

Three floors, on the flagged file's own book (ew-all, gross 0.75), arms and panels verbatim:

| floor | construction | mean names admitted / day |
|---|---|---|
| DV0 | no floor (the identity mask) | 439.0 |
| DV1M | `(px*vol).rolling(20).median() >= $1M` — **the flagged line** | 252.10 |
| VOLSH70k | `vol.rolling(20).median() >= 69,650 shares` — **the substitute** | 252.09 |

## Reproduction gates (all printed before any new number was read)

| gate | result |
|---|---|
| `fast_bt` vs `engine.backtest` | 8.674e-18 |
| SPY on the SMALL439 window | 14.13%/0.862/-33.7%, halves 0.891/0.858 — exact |
| LIVE RULES v2 on U56 @10bps | 8.66%/1.2056/-12.05% — exact |
| LIVE RULES v1 on SMALL439 @10bps | 8.15%/0.603/-32.8% — exact |
| **the flagged file's 288 SMALL439 cells, both floors** | **max abs dSharpe 9.7e-17 — bit-exact** |
| its 144 U56 cells | 8.2e-06 — **diagnosed**: U56 reads `data/prices.csv`, rewritten by the daily-close job on 2026-09-07 *after* the flagged file ran; `data/prices_small.csv.gz` has not moved. No U56 cell carries a floor, so the drift cannot enter any DV-vs-VOLSH contrast; it is carried into R8's 108-arm count and reported there. |

## S1 — structural census (stated before the substitution was run)

A row quoted at floor $0 cannot move: `adv_mask` returns the all-True mask before it touches
`px * vol`. Reading the 9 rows:

| row | reachable? | why |
|---|---|---|
| R1 Q1 reproduction gates | no | floor $0 throughout |
| R2 P1 published gate damage | no | row title says "floor $0" |
| R3 four-way decomposition | no | quoted at `floor_musd=0` |
| R4 P2 band3 recovery | no | row title says "floor $0" |
| R5 P4 saturation | no | pre-registered cell is floor $0 |
| R6 P3 flip rates | no | `flip_rate()` takes the gate state only; no mask argument exists |
| **R7 rule-8 walk-forward (48 cells)** | **YES** | 16 of its 32 SMALL439 cells are the $1M DV floor |
| **R8 both KEEP paths (108 arms)** | **YES** | 36 of the 108 arms are the $1M DV floor |
| R9 by-product: vol20 half on U56 | no | U56 runs at floor $0 |

**7 of 9 published rows are quoted where the flagged line is the identity map.**

## S2 — the flag is right at the mask

Idea 197's T1 operator applied to the MASK, both published sigmas, 3 draws each, over 1,368,684
live ticker-days: the DV mask's admitted set moves on **1.05%–3.00%** of them. The VOLSH mask moves
on **0** at every sigma and draw, as the theorem requires.

## S3 — the two masks are different objects

At matched admission rate (252.1 vs 252.1 names/day) they still disagree on **15.55%** of the union
of admitted ticker-days (Jaccard 0.845); the swap moves 21.3 names out and 21.3 in on an average
day. A null below would therefore have been informative, not vacuous.

## S4 — the two reachable rows both MOVE, neither changes a verdict

| row | published claim | DV (published) | VOLSH | |
|---|---|---|---|---|
| R7 | SMALL439 IS-pick mean OOS Sharpe | 0.399 | 0.451 | MOVES |
| R7 | do-nothing mean OOS Sharpe | 0.366 | 0.415 | MOVES |
| R7 | band3 / 200d mean OOS Sharpe | 0.281 / 0.264 | 0.337 / 0.316 | MOVES |
| R7 | IS-pick / do-nothing mean OOS CAGR | 4.12% / 4.93% | 4.79% / 5.85% | MOVES |
| R7 | picks beating SPY OOS | **0 of 32** | **0 of 32** | restates |
| R7 | "pick loses to do-nothing on OOS CAGR" | True | True | restates |
| R7 | U56: constant b=0.03 beats the IS chooser | 12/16 (1.249 vs 1.191) | unchanged (floor-free) | restates |
| R8 | 4a KEEP | **0 / 108** | **0 / 108** | restates |
| R8 | 4b KEEP | **15 / 108** | **15 / 108** | restates |
| R8 | 4b KEEP on SMALL439 alone | **0 / 72** | **0 / 72** | restates |
| R8 | 4b binding bars CAGR / H1 / H2 / OOS | 86 / 72 / 72 / 72 | 86 / 72 / 72 / 72 | restates |
| R8 | 4b binding bar DD | **50** | **46** | MOVES |

Every level moves; every conclusion holds. At the cell level the substitution is emphatically not a
null — over the 36 touched arm-cells |dSharpe| averages **0.098** (max 0.152) and |dCAGR| averages
**1.23 pp** (max 2.56 pp) — but all six 4b verdict changes are KILL-to-KILL, differing only in
which bar binds, and on the drawdown bar alone. No arm changes side of a KEEP path.

## The result worth keeping: the leak has a size and a SIGN

Across all **144** SMALL439 cells the floor touches (9 arms x 2 conv x 2 comp x 4 rungs), the
share-volume-floored panel out-earns the dollar-volume-floored panel **at matched admission rate**:

| | mean | median | min | max | sign positive |
|---|---|---|---|---|---|
| dCAGR (VOLSH - DV), pp/yr | **+1.23** | +1.09 | +0.33 | +2.60 | **144 / 144** |
| dSharpe | **+0.098** | +0.100 | +0.042 | +0.153 | **144 / 144** |

The un-gated book alone reads 6.20% under DV1M and 8.80% under VOLSH70k (dg/TREND, 10 bps) while
holding the same 252.1 names/day. The sign never flips. That is what a back-adjusted price LEVEL
inside an eligibility mask does: a fixed dollar floor preferentially excludes names whose adjusted
history was scaled down by their own future dividends and splits, and the excluded cohort is not
random with respect to return. Stated as the measured contrast; the mechanism is the theorem's, and
no split/dividend calendar is cached offline to attribute it name by name.

## By-product — one published sentence IS wrong

The flagged file's CHANGELOG entry says "at idea 121's proposed $1M ADV floor the published damage
shrinks from -6.52 to -4.87 pp @10bps but never changes sign". Re-measured here:

| floor | published gate damage @10bps |
|---|---|
| DV0 | **-6.5155 pp** (exact reproduction) |
| DV1M | **-4.8661 pp** (exact reproduction) |
| VOLSH70k, matched admission | **-6.5920 pp** |

The softening is the dollar floor's price channel, not liquidity: screen for liquidity with shares
and the damage is not softened at all — it is marginally larger than with no floor. The sentence
should be read as a fact about `(px*vol)`, not about liquid names.

## Verdicts

**4a 0/108. 4b 15/108 (all U56), 0/72 on SMALL439 — under BOTH floor instruments.** Rule 8
(band width chosen on 2010–2016, 2017–2026 read once, 48 cells per instrument): the SMALL439 IS
pick posts OOS Sharpe 0.399 (DV) / 0.451 (VOLSH) against SPY's 0.882 and beats SPY in **0/32**
either way, and loses to do-nothing on OOS CAGR either way (4.12% vs 4.93%; 4.79% vs 5.85%).
Nothing here is a book and nothing is promotable — this is a record-hygiene result.

**SURVIVORSHIP** (PROTOCOL rule 9): both panels are current constituents, and the small panel's
missing delisted cohort sits in exactly the thin names a liquidity floor argues about. Absolute
levels on SMALL439 are therefore uninterpretable, and only floor-minus-floor contrasts on the same
arms, days and book are read above. The +1.23 pp gap is a contrast between two masks over the same
surviving names; it is not a claim that either floored panel would have earned that in real time.
