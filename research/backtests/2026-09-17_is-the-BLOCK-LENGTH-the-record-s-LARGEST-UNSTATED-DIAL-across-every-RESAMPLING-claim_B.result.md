# Idea 1208 (lane B, 2026-09-17) — is the BLOCK LENGTH the record's LARGEST UNSTATED DIAL across every RESAMPLING claim?

**VERDICT: YES on the word "resolved", NO on capital. KILL (capital) — no new book. SCHEMA CLAUSE EARNED.**

Dials (PROTOCOL rule 4, max 2): **CLAIM SET** {CS_STRICT, CS_PROX, CS_ALL} and **L LADDER**
{LL_REC = 1154's [21,63,126,252], LL_FULL = [1,2,5,10,21,42,63,126,252,504,1008], LL_WIDE = LL_FULL+T}.
All 9 cells published in `.dialgrid.csv` / `.projection.csv`; every individual L rung in `.ladder.csv`.
Panel (3) x anchor (2) x ladder (4) x chooser (3) = **72 decisions**, 1101/1154's own object, built at
every point and never selected on. SEED / B / q are Arm D's comparands, not dials. 14/14 gates pass.

## 1. The ladder has a degenerate top rung, and the record has never said so (Arm 0, data-free)

A joint moving-block redraw at `L = T` is the **identity**: `nb = ceil(T/T) = 1`, drawn from
`range(max(T-T,1)) = {0}`, so every draw replays the observed path and `P_pick` of the observed argmax
is exactly 1.000. G1 proves it bit for bit (max |idx - arange| = 0.000e+00); G2 confirms `L = 1` is a
genuine iid draw. **A resolution rate quoted without L is quoted from an interval whose upper end is
1.000 by arithmetic, not by evidence.**

## 2. Census: 77 committed verdicts rest on a block resample and state no L (Arm A)

Corpus 34,011 committed text units (LEADERBOARD.md + CHANGELOG.md + 1,164 `.md` files).

| claim set | units | carry a verdict word | of those, state L | **state NO L** |
|---|---|---|---|---|
| CS_STRICT | 478 | 267 | 190 (0.7116) | **77 (0.2884)** |
| CS_PROX | 2,409 | 1,189 | 191 (0.1606) | **998 (0.8394)** |
| CS_ALL | 1,366 | 814 | 191 (0.2346) | **623 (0.7654)** |

Where L *is* stated it is overwhelmingly 63 (145 occurrences) against 21 (34), 126 (27), 252 (20) —
1101's unargued choice, inherited. Only 37 units anywhere state an L *ladder* rather than a point.

## 3. Resolution rate is monotone in L over the whole ladder, from 0.1528 to 1.0000 (Arm B)

Same 72 decisions, bar 0.90, B = 1000, record's seeds — **nothing changes but L**:

| L | 1 | 2 | 5 | 10 | 21 | 42 | **63** | 126 | 252 | 504 | 1008 | T |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| resolved | 11 | 12 | 12 | 13 | 14 | 16 | **16** | 17 | 20 | 23 | 34 | 72 |
| rate | .1528 | .1667 | .1667 | .1806 | .1944 | .2222 | **.2222** | .2361 | .2778 | .3194 | .4722 | 1.000 |
| mean P_pick | .5604 | .5636 | .5633 | .5672 | .5781 | .5949 | .6070 | .6276 | .6590 | .6904 | .7054 | 1.000 |

Non-decreasing at every one of the 12 rungs. 1154's own ladder replays inside seed noise
(L=21 dev 4.4e-05, L=63 0.0139, L=126 0.0139, L=252 0.0278: G7 x4 pass). **Reach is 14 at every L** —
the argmax rung is an IS-observed fact and carries no L-dependence at all; only the *bar* does.

## 4. How many committed verdicts are L-dependent (Arm C + Arm F)

A decision is L-DEPENDENT if its resolved/unresolved verdict changes anywhere on the ladder:

| L ladder | rungs | always | never | **L-DEPENDENT** | rate |
|---|---|---|---|---|---|
| LL_REC (1154's) | 4 | 14 | 52 | 6 | 0.0833 |
| **LL_FULL** | 11 | 11 | 38 | **23** | **0.3194** |
| LL_WIDE (+T) | 12 | 11 | 0 | 61 | 0.8472 |

Spread evenly across the record's own structure — by ladder N 7/18, GROSS 6/18, CADENCE 5/18, H 5/18;
by chooser CH_ISCAGR 9/24, CH_ISSHARPE 8/24, CH_ISDD 6/24; by panel U56 9/24, SMALL 8/24, B136 6/24.
No cell is immune.

**Projection, stated as a projection.** 77 CS_STRICT verdict-carrying sentences state no L; at the
measured 0.3194 that is **24.6 L-dependent committed verdicts [16.3, 32.9]** (CS_PROX: 318.8
[211.3, 426.3]). This is a rate measured on the record's own pick decisions and applied to the
unstated-L population — **not 77 re-runs**. Sentences resting on a block null for something other
than a pick are not covered and nothing is claimed about them.

## 5. The comparative the word "largest" demands (Arm D)

Each knob moved across its own honest range with the other three frozen at the record's values,
same 72 decisions:

| knob | range | min rate | max rate | **swing** | stated in the record? |
|---|---|---|---|---|---|
| **L** | 1 .. 1008 | 0.1528 | 0.4722 | **0.3194** | **no** |
| q | 0.60 .. 0.99 | 0.1528 | 0.4583 | 0.3056 | yes, always |
| SEED | 8 streams | 0.2083 | 0.2361 | 0.0278 | no |
| B | 125 .. 4000 | 0.2222 | 0.2361 | 0.0139 | usually |

**L is the largest knob of all four — larger than the one the record always publishes (q), 11.5x the
seed and 23x the draw count — and it is the one the record never argues.** H_LARGEST and
H_LARGEST_ALL both SUPPORTED.

## 6. Rule 8 walk-forward and both KEEP paths (Arm E) — and the finding that kills it for capital

Every dial fixed on 2009–2016 only; 2017–2026 read once. 10 bps, next-day execution, 260-row warm-up.
426 rule-8 rows (162 rung books + 264 `CH_RESOLVED_L*` chooser rows, one per L rung).

- **4a: 0 of 426.** (A_H1 218, A_H2 3, A_DD 9 — the live book's -12.05% MaxDD is not beatable by a
  growth book, PROTOCOL rule 4's own reason for path 4b.)
- **4b: 105 full / 109 OOS / 104 BOTH → 19 DISTINCT realised books, and every one of the 19 is a rung
  book the record already holds** (U56 and B136 anchors A/B on 1101's N / H / GROSS / CADENCE ladders).
  Best: U56 N=20 anchor B — full 11.03% / 1.1354 / -18.01%, **OOS 12.42% / 1.1771 / -18.01%** against
  U56 SPY OOS 15.15% / 0.8684 / -33.72% (CAGR 82% of SPY's, DD 53% of SPY's) and LIVE v2 OOS
  9.42% / 1.2714 / -12.05%. **CONFIRMATORY, NOT GENERATIVE. NOT PROMOTED, NO MEMO, NO RULES CHANGE.**
- **THE L DIAL IS INERT ON MONEY.** Acting only on resolved picks, mean OOS Sharpe over the 24 chooser
  rows runs 0.8268 (L=1) / 0.8273 (L=10..126) / 0.8321 (L=504) / 0.8307 (L=1008): **a total spread of
  0.0053 across a dial that moves the resolution rate by 0.3194.** The word "resolved" swings by a
  factor of 3.1; the capital consequence is four thousandths of Sharpe.

## 7. What the record should take

The defensible sentence, and nothing more: **L IS THE LARGEST UNSTATED DIAL IN THE RECORD'S
RESAMPLING VOCABULARY AND THE SMALLEST ONE IN ITS BOOK.** A schema clause requiring `L` beside every
block-resampling verdict is cheap (77 CS_STRICT sentences to amend, ~25 of them L-dependent) and
buys checkability, not return. It is PROPOSED for the Sunday review (rule 6) as a PROTOCOL/schema line
only. No RULES change, no new book, no promotion.

## Survivorship (rule 9)

U56 (56 cols) and B136 (136) are CURRENT-constituent lists; SMALL is the current constituents of a
sub-$2B screen. Every LEVEL — CAGR, MaxDD, Sharpe, and every null built on them — is optimistic, and a
resample null prices sampling error on the tape it is handed and cannot correct that. It largely
cancels out of the headline claims, which are ratios of one construction against itself on the same
tape (the same 72 decisions at different L), and it does NOT cancel out of the 4b legs, so the 4b
passes in section 6 are an upper bound.

Script: `research/backtests/2026-09-17_is-the-BLOCK-LENGTH-the-record-s-LARGEST-UNSTATED-DIAL-across-every-RESAMPLING-claim_B.py`
Artefacts: `.datafree` `.census` `.census_units` `.ladder` `.rate_by_L` `.dialgrid` `.Ldependence`
`.knobs` `.swings` `.walkforward` `.money` `.projection` `.gates` `.hypotheses` `.log.txt`
