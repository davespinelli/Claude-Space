# Idea 554 — is-every-published-BAND-a-band-on-a-MEAN-quoted-as-a-CELL-expectation (cloud, 2026-09-09)

**Verdict: ANSWERED / KILL of the premise's generality.** No — and not because the record's
bands state their statistic, but because the record has almost no bands of that kind. Of 224
two-sided intervals in the 499 committed scripts, 80 are used as a pass/fail bar, and 64 of
those bound ONE number by construction (hand-copied reproduction gates, idea 515's category),
where cell-level coverage is 1/1 or 0/1 and the question is vacuous. That leaves **16 GRID
bands** in the whole record. Idea 551's pathology is real, confirmed and quantified — but its
population is essentially one band, the anchor itself.

Script: `2026-09-09_is-every-published-BAND-a-band-on-a-MEAN-quoted-as-a-CELL-expectation_cloud.py`
Artefacts: `.census.csv` (all 80 bands), `.anchor.csv`, `.bands.csv`, `.g2.csv`,
`.walkforward.csv`, `.keeppaths.csv`, `.console.txt`.

## (a) Do published bands state the statistic they bound?

| population | n | states its statistic |
|---|---|---|
| REPRO gates (ABSTOL, half-width ≤ 5% of centre — one number by construction) | 64 | n/a, vacuous |
| GRID bands (an interval on a quantity that ranges over cells) | **16** | **4 (25.0%)** |
| — of which demonstrably bound a MEAN | 2 | **2 (100%)** |
| — bound a single named scalar | 9 | 2 |
| — evaluated per cell | 3 | 0 |
| — unstated | 2 | 0 |

The two MEAN-bound bands both name their statistic in the line that applies them ("ratio of
mean gap", "pct77"). The band that does **not** is the anchor: `BAR_MA_RESID = (-0.70, -0.20)`
and its copy `BAND_PUB` are defined as bare 2-tuples whose comment names the quantity (pp/yr
residual) but never the statistic (a mean over 9 θ). That is the whole mechanism by which it got
quoted forward as a cell expectation — and it is the record's only instance of it.

Eligibility removed 144 intervals that merely look like bands (`COSTS = (10, 25)`,
`ANCHOR = (0.75, 20)`, `BULK_LAST_Q = (1, 2026)`, index and plot ranges); G6 confirms every
known parameter pair was dropped.

## (b) Cell-level coverage of the anchor band, all grid points

`[-0.70, -0.20]` against idea 551's own MA-THRESH `resid0_pp` cells (27 per cadence per window
= 3 panels × 9 θ):

| window | D | W | M | Q | A | POOLED |
|---|---|---|---|---|---|---|
| FULL coverage at published width | 0.481 | 0.481 | 0.556 | 0.519 | **0.074** | 0.422 |
| IS | 0.259 | 0.222 | 0.259 | 0.556 | 0.481 | 0.356 |
| OOS | 0.407 | 0.630 | 0.407 | 0.333 | 0.111 | 0.378 |

The pooled mean is **inside** its own band in 5 of 6 FULL cells while cell-level coverage runs
**7.4%–55.6%**. Smallest width multiplier reaching each coverage target (FULL): 50% needs
m = 1.0–1.5, 66.7% needs 1.5–2.0, 80% needs 1.5–2.0, 90% needs 2.0–3.0, 95% needs 2.0–3.0 and
is unreachable at ANNUAL even at m = 3.0. The published width reaches a 50% target in only
2 of 6 cells and no cell at any higher target.

**0 of the other 16 GRID bands can be re-priced from their own script's committed artefacts**
under a strict name link (a numeric column named in the bounded expression). A band whose cells
no committed CSV carries is, by construction, a band published without its cell distribution —
which is the census's second finding and the reason (b) cannot be answered for 15 of 16.

## Rule 8 walk-forward

Width chosen on the IS cells only, coverage read on the untouched OOS cells: the IS-chosen
width holds its own target OOS in **16 of 30** (cadence × target) cells (53.3%), and 5 targets
are unreachable in-sample even at m = 3.0. It holds at every target on D, W, M and POOLED and
**fails at every target on Q and A** — the same two cadences where idea 551 found the band's
domain problem. A width fitted on the first half of this object does not transfer at the ends of
the cadence dial.

## KEEP paths

Idea 554 prices **no book and has no KEEP candidate**; none is claimed. Record-wide over the 74
committed grids that carry both columns (24,906 priced book rows): 4a 2,160 (8.673%), 4b 2,454
(9.853%), **BOTH 169 (0.679%)**, concentrated in 24 grids, the largest single contributor being
`2026-09-04_which-4b-bar-binds_B.grid.csv` (53).

## Gates

G1 PASS (anchor band found in 2 scripts), G2 PASS (idea 551's published coverage reproduces from
its own decomp: 48.1/48.1/55.6/51.9% at D/W/M/Q, 7.4% at A, 85.2–100% at m = 2.0), G3 PASS (no
duplicates, lo < hi on all 224), G4 PASS (one arity and one kind per band), G5 PASS (74 grids),
G6 PASS (parameter pairs removed).

## Scope limit (stated, not repaired)

The census reads `research/backtests/*.py` through five syntactic patterns. A band that exists
only as prose in a `.result.md`, or one written in a form none of the five patterns matches, is
outside the denominator. The 80/224 and 16/80 counts are therefore lower bounds on the record's
band population, and every count above should be read as "bands the pre-registered extractor can
see". Nothing here is a return series, so survivorship does not enter directly — but the pooled
record-wide KEEP rates were computed on panels that are current constituents (SMALL439, B136)
and inherit that optimism.
