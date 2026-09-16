# Idea 1119 (lane B, 2026-09-16) — does the LADDER axis answer hold on the SMALL panel?

**ANSWERED = YES, the axis answer HOLDS — but the STRONG form the record has been quoting
does NOT, and the idea's own mechanism premise fails BACKWARDS.**

Script: `2026-09-16_does-the-LADDER-axis-answer-hold-on-the-SMALL-panel_B.py`
Gates **12 of 12 PASS**. Hypotheses **3 of 7**. Nothing proposed as capital.

## The two dials, and no more (PROTOCOL rule 4)

`PANEL` {U56, B136, SMALL663} × `q` {0.80, 0.90, 0.95} = **9 combinations, all published**.
LADDER and STATISTIC are not dials — they are the two candidate answers, and all 3 × 4 × 4 = 48
cells are reported under every combination. DEFINITION is not a dial (`INF_FLOOR` headline;
`ZERO_CONTENT` and `NO_TAPE_500` printed beside everywhere). L = 63 headline, L ∈ {21, 126}
beside. Frozen at 1082/1094/1098/1102/1108/1110/1116's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, W cadence, min hold 126, N = 20, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, 1000 draws, crc32 seeds.

**The seeds are 1116's verbatim, deliberately.** U56 and B136 here are a *bit-exact
reproduction* of 1116's committed cells, not an independent redraw, so the two panels that
already answered cannot move underneath the comparison: **G8 reproduces all 288 of 1116's
committed U56/B136 cells at max |Δgap| 0.00e+00, max |Δfloor| 0.00e+00, 288 of 288 infinite-floor
flags**, and **G9 reproduces its committed ETA2 pair to 2.4e-05 / 4.4e-05**. The price is that the
two old panels carry no new seed evidence here; SMALL663 gets its own reseed check (D2).

## A correction to the idea's own premise, made before any number

**The SMALL panel is not 485 names.** `data/prices_small.csv.gz` was rebuilt on 2026-09-11 to
715 tickers × 4,198 trading days; the README's documented `max_1d_move >= 1.0` exclusion (the
un-reversed level steps — AMPY +16,083%) drops **52**, leaving **663 tradable names** plus SPY as
a benchmark column that is *not* a constituent and is made un-selectable (G10: SPY's max book
weight is 0.00e+00 at every rung). "485" is a stale count from the 2026-09-04 vintage of the
cache. The panel is labelled **SMALL663** in every artefact.

## THE ANSWER: the ladder axis HOLDS on SMALL663

At the headline (INF_FLOOR, q = 0.90): **ETA2_LAD 0.3016 against ETA2_STAT 0.0476**, margin
+0.2540, ratio 6.3×; concordance within-ladder **0.5417** against within-statistic **0.3750**.
Across the three q rungs the binary reading favours LADDER **2 of 3**, concordance **2 of 3**,
and both continuous readings — REL_FLOOR and LOG_M, which need no threshold — favour it **3 of
3**. The table is degenerate at 0 of 3 q rungs, so the pre-registered binary route applies and
the decision rule returns **HOLDS**. **Three independent reseeds agree 3 of 3** (binary and
REL_FLOOR alike), so this is not a seed artefact.

**H_MARGIN_SHRINKS PASSES, and the idea's framing is confirmed and extended.** The margin falls
monotonically with panel width: **U56 +0.7619 → B136 +0.5079 → SMALL663 +0.2540** (ratios
17.0× / 11.7× / 6.3×). The axis answer survives on the widest, noisiest panel — but it is
**a third of the effect** it is on U56, and the record quotes the U56 number.

## KILL of the STRONG form: the rows are NOT the same ladders (H_HC_SAME_ROWS FAILS)

1116 concluded that H and CADENCE decide nothing at any of the four statistics on both large
panels. That row assignment **does not transfer**. SMALL663's INF_FLOOR row sums (of 4) are
**N 0, H 2, GROSS 2, CADENCE 3** against U56's **0 / 4 / 1 / 4** and B136's **2 / 4 / 0 / 3**:

| ladder | stat | INF U56 / B136 / SMALL663 | rel_floor U56 / B136 / SMALL663 |
|---|---|---|---|
| H | S_FULL | 1 / 1 / **0** | 1.0000 / 1.0000 / **0.7578** |
| H | CAGR | 1 / 1 / **0** | 1.0000 / 1.0000 / **0.7773** |
| GROSS | S_FULL | 0 / 0 / **1** | 0.6521 / 0.1002 / **1.0000** |
| GROSS | S_OOS | 1 / 0 / **1** | 1.0000 / 0.1019 / 1.0000 |

**All three panels agree at only 8 of 16 cells, and SMALL663 differs from BOTH at 4 of 16.** The
H ladder becomes *partly resolvable* on the small-cap panel exactly where the record says it
never is, and the GROSS ladder — 1108's near-scaling family, the one 1116 tested as the risk
that a "ladder answer" was really a "GROSS answer" — goes the other way on the Sharpe columns.
**Read plainly: "un-resolvability is a property of the dial" survives as an axis statement; "H
and CADENCE are the un-resolvable dials" is a U56/B136 statement and must stop being quoted as
a general one.**

## KILL of the idea's mechanism premise, and it fails BACKWARDS

**H_MORE_UNRES FAILS.** The direct prediction of "where the draw dominates" is that the small-cap
panel carries *more* un-resolvable cells. It carries **fewer**: INF_FLOOR **7 of 16** against
**9 of 16** on both large panels (ZERO_CONTENT 7 / 9 / 9; NO_TAPE_500 4 / 5 / 5). The noisiest
panel is the *most* resolvable one.

**H_RELIABILITY FAILS too.** Median paired per-cell reliability on S_OOS runs **U56 0.0000,
B136 0.2382, SMALL663 0.0000** — SMALL663 does not sit below U56, it ties it at the floor, so
1073's 0.0915-vs-0.5126 ordering (a different object: one book's draw-to-draw reliability) does
not reproduce as a ladder-level ordering. Worth recording separately: **the unpaired estimator is
0.0000 at all 48 cells on all three panels** — the cross-rung signal variance is smaller than the
raw bootstrap variance everywhere, and only the paired form (the error variance that actually
enters the sign agreement the floor is built from) recovers anything at all.

**D3 — and SNR does not rescue the premise either; it runs the wrong way.** SMALL663 has the
**worst** mean signal-to-noise of the three (spread/pair-SD **2.5506** against U56 3.4029 and
B136 3.4791; its spread is wider at 3.77 but its per-pair noise grows faster, 1.82 against
0.92/1.07) and it still carries the fewest infinite floors. The reason is what INF_FLOOR
measures: **it is an ORDER statistic, not a precision statistic.** The floor is infinite only
when no resolved pair sits above the *largest* un-resolved gap, so one well-separated pair at the
top of a right-skewed gap distribution makes a cell finite however poor the panel's average
precision is — and SMALL663's gap distribution is the most right-skewed of the three (mean
max/median gap **3.36** against 2.53 / 2.28), while having the *smallest* share of pairs
separated by more than 2 pair-SDs (0.0833 against 0.1389 / 0.1965).

**Consequence for the record, stated as a caution and not as a measured law: an INF_FLOOR count
is not a panel-precision ranking and must not be read as one.** This run establishes that it is
not monotone in mean SNR across three panels; it does not establish what it *is* monotone in, and
nothing here licenses the reverse reading either.

## The declared hypotheses

| hypothesis | verdict | detail |
|---|---|---|
| H_LADDER_SMALL | **PASS** | ETA2_LAD 0.3016 > ETA2_STAT 0.0476 on SMALL663, q = 0.90 |
| H_STAT_SMALL | FAIL | mirror; the statistic axis wins nowhere |
| H_CONCORD_SMALL | **PASS** | within-ladder 0.5417 > within-statistic 0.3750 |
| H_MARGIN_SHRINKS | **PASS** | +0.7619 → +0.5079 → +0.2540 (U56 → B136 → SMALL663) |
| H_MORE_UNRES | FAIL (backwards) | INF_FLOOR 9 / 9 / **7** of 16 |
| H_HC_SAME_ROWS | FAIL | SMALL663 row sums N 0 / H 2 / GROSS 2 / CADENCE 3 |
| H_RELIABILITY | FAIL | median paired S_OOS reliability 0.0000 / 0.2382 / 0.0000 |
| DECISION_RULE | **HOLDS** | binary route; binary 2/3, concord 2/3, rel_floor 3/3, log_M 3/3 |

## Rule 8 and both KEEP paths — nothing proposed

The book at all 81 rungs is byte-identical across both dials (only which cells get *called*
un-resolvable changes), so 4a and 4b are invariant to PANEL-as-a-dial and to q by construction.
Scored anyway because rule 4 requires it. Rung chosen on IS 2009–2016 alone, per ladder, three
choosers (`C_ISSHARPE` / `C_ISDD` / `C_ISCAGR`), OOS 2017–2026 read once.

- **IS-chosen picks: 4b full 4 of 36, 4b OOS 4 of 36, 4a 0 of 36** — all four on U56.
- **Whole grid: 4b full 16 of 81, 4b OOS 17 of 81, 4a 0 of 81** (U56 10/27, B136 6/27,
  **SMALL663 0 of 27 on every path**).
- **SMALL663 fails every 4b leg almost everywhere**: L_H1 26/27, L_H2 27/27, L_OOS 27/27,
  L_DD 25/27, L_CAGR 26/27. The best SMALL663 IS-pick is H = 252 at 13.36% / 0.7844 / −37.41%
  full and 11.16% / 0.6676 / −37.41% OOS, against **SMALL663 SPY 14.06% / 0.8581 / −33.72%
  full, 15.33% / 0.8767 / −33.72% OOS** and **live RULES v2 on that panel 4.30% / 0.6629 /
  −13.89% full, 3.75% / 0.5590 / −13.89% OOS**. It loses to SPY on return, Sharpe and drawdown
  at once.
- U56 reference: SPY 15.10% / 0.8829 / −33.72% full, 15.21% / 0.8711 / −33.72% OOS; live
  RULES v2 8.62% / 1.2007 / −12.05% full, 9.45% / 1.2762 / −12.05% OOS.

**PARK, not KEEP. Nothing is proposed as capital.**

## Survivorship (PROTOCOL rule 9)

All three panels are current-constituent lists and **SMALL663 is by far the worst**: its universe
is the *current* sub-$2B screen, so every name survived 2010–2026 still listed, still public and
still under $2B, and the acquired / delisted / bankrupt small caps are all missing. A rung-to-rung
GAP and a rung-to-rung AGREEMENT contrast two books over the *same* inflated tape, so the bias
very largely cancels out of the floor and out of every quantity decomposed here — which is why
the axis question can be asked on this panel at all. It does **not** cancel out of the 4b legs,
which are measured against SPY, so every SMALL663 4b figure above is an upper bound and a badly
inflated one. That it still fails 4b 27 of 27 on an inflated tape is the reading that matters.

## The declared approximation, and its direction

`NO_TAPE_500` rests on 1110's projection A′ = Φ(√M Φ⁻¹(A)). Both of its assumptions run *toward*
resolution, so every `M_needed` is a lower bound and every NO_TAPE_500 count is a lower bound on
un-resolvability. The exponent is **inherited** from 1110's sub-tape fit, which was made on
U56/B136 only, so it is weakest exactly on the new panel: SMALL663's `M_needed` / `LOG_M` column
is the least trustworthy quantity in this run. It is published in full and is never the sole
basis of a verdict — the decision rule's continuous route requires REL_FLOOR to agree with it.

## Artefacts

`grid` (81 book rows) · `benchmarks` · `cells` (432 rows) · `decomp` (27) · `marginals` ·
`reliability` (48) · `hypotheses` · `cross1116cells` (288, the bit-exact reproduction) ·
`d1` (panel-by-panel cell table) · `d2` (SMALL663 reseeds) · `d3` (SNR / order-statistic) ·
`walkforward` (36 IS picks) · `gates` · `console.txt`.

## LANE COLLISION, and the cross-read (added at push time)

The **cloud lane claimed and completed the same idea in the same hour** and pushed first
(`2026-09-16_does-the-LADDER-axis-answer-hold-on-the-SMALL-panel_cloud.py`) — idea 932's
numbering/claim defect again. Both results are kept and cross-read, as the record did for idea
969. This section was written after reading that run's `redraws.csv`; nothing above it was
changed.

**The two runs confirm each other number for number at the shared seed base.** Two independently
written scripts return identical values at base 11161116: U56 9 un-resolvable / ETA2
0.8095 / 0.0476, B136 9 / 0.5556 / 0.0476, SMALL 7 / 0.3016 / 0.0476, and the same SMALL
INF_FLOOR row vector N 0 / H 2 / GROSS 2 / CADENCE 3.

**Where the cloud lane corrects this run.** `H_MARGIN_SHRINKS` above passes at 1116's single seed
base. That lane's 8-base redraw shows **U56's ratio runs 3.18–17.00× (median 7.00×) against
B136's 11.00–11.67× (median 11.00×)**, so 1116's 17.0× is U56's redraw *maximum* and at the
median the two large panels order the other way. What survives the redraw: **SMALL663's ratio is
a constant 6.33× at 8 of 8 bases, below B136 at 8 of 8 and below U56 at 4 of 8.** The defensible
statement is **"the margin is smallest on the small-cap panel"**, not "the margin shrinks
monotonically as the panel widens". The PASS above stands as scored at its declared base; this
paragraph is how the finding should be carried.

**Where the two differ on counts, and why it changes nothing.** This run reads 9 and 9 infinite
floors on the large panels where the cloud lane's own base reads 10 and 10 — because this run
re-uses 1116's seeds on purpose and gates the bit-exact reproduction (G8). That is the
cell-level seed fragility 1116's D1 already measured. `H_MORE_UNRES` fails backwards against
9/9 and against 10/10 alike, and the cloud lane's 8 bases put SMALL at a constant 7 against
U56 8–10 and B136 9–10 at every base, which makes the backwards failure robust rather than a
draw.

**Where this run adds.** The per-cell three-panel table (D1: all three agree at only 8 of 16
cells, SMALL differs from both at 4 of 16); the measured reliability column (1073's mechanism
re-measured rather than inherited); and **D3, which corrects the cloud lane's explanation of the
shared fact**. That run attributes "SMALL is the most resolvable" to its "far larger ladder
spreads". The spreads are indeed larger (3.77 against 2.84 / 3.30) — but the per-pair noise
grows faster (1.82 against 0.92 / 1.07), so **SMALL663's mean signal-to-noise is the worst of the
three, not the best**, and spread alone does not carry it. What carries it is that INF_FLOOR is
an order statistic.

**Where the two agree completely.** The sub-$2B panel is not capital: 0 of 27 rungs and 0 of 12
IS picks pass 4b on either window, in both runs, independently.
