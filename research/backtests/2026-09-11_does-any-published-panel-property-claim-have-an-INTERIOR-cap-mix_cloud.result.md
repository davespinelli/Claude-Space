# Idea 524 — does any published panel-property claim have an INTERIOR cap mix?
## SECOND, INDEPENDENT RUN (cloud, 2026-09-11), published as a cross-check of lane B's same-day answer

cloud, 2026-09-11 · script `2026-09-11_does-any-published-panel-property-claim-have-an-INTERIOR-cap-mix_cloud.py`
Console `…_cloud.console.txt` · CSVs `.census` `.claims` `.cells` `.keeppaths` `.curvature` `.walkforward` `.picks` `.timing` `.baseline`

**Provenance, stated first.** This run was claimed and executed from a queue snapshot in which
524 was still open. Lane B answered the same idea the same day and pushed first; this is
therefore **not a new answer but an independent replication**, built from a different corpus
rule, a different detector and a different grid, and it is published only because it agrees.
Lane B's entry stands as the primary; where the two differ, **lane B's numbers are the
record's**, and the differences are named below.

## Verdict: ANSWERED / NO — **no published panel-property claim has an interior cap mix, and an interior comparand is cheap but buys exactly one thing: the DRAWDOWN leg.** Agrees with lane B on every headline. No KEEP (4a 0/400, 4b 5/400, every pass at q=0).

## Part A — the census (independent detector)

Corpus: **417 claim-bearing documents** (LEADERBOARD, CHANGELOG, QUEUE, RULES, PROTOCOL, every
`*.result.md` and memo). **6,957 lines name at least one panel; 2,190 name ≥ 2 distinct
panels; 1,139 of those are claim-shaped** (carry a comparison verb).

| q-span crossed by the claim | lines | share |
|---|---|---|
| **0.0** — same corner (within-stratum, but AT a corner) | 333 | 29.2% |
| **1.0** — the two corners, fully confounded | 806 | 70.8% |
| **0 < span < 1 — INTERIOR** | **0** | **0.0%** |
| UNKNOWN q (panel token off the map) | 0 | — |

**Zero interior contrasts, counted not guessed.** Lane B reports 0 of 147 TIGHT and 0 of 402
LOOSE cross-panel property claims; this run reports 0 of 1,139 claim-shaped multi-panel lines.
Different unit (lines vs files), different corpus rule, **same integer: zero.**

**A detector trap worth recording.** A loose `q<number>` scan finds **225** lines in 32
documents — but `q` is **overloaded** in this record: **110 of them (48.9%)** sit beside
trim / quantile / decile / breadth vocabulary and are a *quantile* q (`q0.17` trailing
threshold, `q=0.90` selectivity), not a cap mix. The tight cap-mix vocabulary (idea 284's
`q#.###~s` seed ids, "cap mix", "mixed panel", "interior panel", "q = share") finds **14 lines
in 5 documents**, all of them ideas 284/286's own outputs — *a study's results, not standing
comparands a later idea can cite.* Any future census of `q` in this record must disambiguate
the two meanings or it will over-count by ~2×.

## Part B — pricing a standing interior comparand

**5 q × 2 k × 8 seeds = 80 mixed panels**, plus 5 named reproduction rows, on the common
calendar 2010-01-04 → 2026-09-04 (4,194 days). Arms: EWall, CAND10, CAND20, RULES v1, RULES
v2. 10 bps, weekly, next-day, gross 0.75. Panel construction, book arms, statistics block and
PROTOCOL keep flags are **imported from idea 284's module**, not re-typed. Seeds are
replication; none is chosen.

**COMPUTE COST: 3.60 s** per panel's 5-arm block (median 3.56 s; k=40 2.96 s, k=80 4.24 s).
A standing q=0.5 comparand at 8 seeds across both widths costs **~58 s per run**. Trivial.
(Lane B prices the same thing at 0.73 s per 5 book cells and finds one draw suffices; the unit
differs — per-panel-block vs per-cell — and neither figure is a constraint.)

**INFORMATION VALUE — what it buys.** An interior panel is redundant if it lands on the
straight line between the two corners. Scoring every interior cell against the corner-implied
value `q·v(1) + (1−q)·v(0)`, in units of that cell's own seed standard error:

| metric | median \|z\| |
|---|---|
| **H1** | **2.90** |
| **MaxDD** | **2.78** |
| **OOS MaxDD** | **2.71** |
| Sharpe | 1.70 |
| CAGR | 1.39 |
| H2 | 1.27 |
| OOS Sharpe | 1.15 |
| OOS CAGR | 1.00 |

**170 of 288 statistics (59.0%) sit more than one seed SE off the corner line; 105 (36.5%)
more than two.** And the departures are not scattered — **all eight largest are MaxDD or
OOS MaxDD at q = 0.50**, up to **z = +8.91** (k=80 RULES v2: observed −10.92% against a
corner-implied −14.86%). The sign is uniform: **the interior panel's drawdown is SHALLOWER
than the corners imply.** Mixing caps diversifies drawdown in a way neither endpoint shows,
and no endpoint-only comparison can represent it.

**This is lane B's result reached by a different statistic.** Lane B: "VALUE is the DD leg
alone — mean chord position 0.3401 vs 0.5, 24 of 75 triples reject the straight-axis null at
|t|>2 and all 24 BELOW the midpoint; the q=0.5 panel's MaxDD is shallower than both endpoints
in 31 of 90 cells." This run: MaxDD median |z| 2.78 against OOS CAGR 1.00, every largest
departure a q=0.5 drawdown, every one in the same direction. **Where the two runs differ:**
lane B finds CAGR/Sharpe/OOS-Sharpe stay inside the endpoint *interval* 97.8% of the time;
this run finds them off the endpoint *line* by >1 SE in a majority of cells. Those are
different tests — containment vs interpolation — and both can be true; the interpolation test
is the stricter one and is the one that bears on "does a corner-only comparison mislead".
This run also finds **H1 (first-half Sharpe) departs as hard as MaxDD**, which lane B did not
test.

## PROTOCOL KEEP paths — all 400 cells reported
**4a: 0 of 400. 4b: 5 of 400 — every pass at q = 0.00** (k=40 CAND20 and EWall, k=80 EWall),
**0.000 at q = 0.25 / 0.50 / 0.75 / 1.00.** Lane B: 4a 0/450, 4b 7/450, every pass at q ≤ 0.25.
Both are a fresh reproduction of the 276/285/286 finding that 4b lives at the large-cap corner.
Binding bar over the 395 failures: the all-legs failure `H1,H2,OOS,DD,CAGR` dominates (136),
then `H2,OOS,DD` (68); **`CAGR` alone binds 32 and `DD` alone 27.**

## Rule 8 (PROTOCOL 8) — IS 2009–2016 chooses, OOS 2017–2026 read once

| k | pick q | pick arm | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | interior? |
|---|---|---|---|---|---|---|---|
| 40 | **0.00** | v2 | 1.0827 | 8.67% | 1.0945 | −12.96% | no |
| 80 | **0.00** | v2 | 1.1123 | 8.79% | 1.1382 | −12.76% | no |

Against the standing comparands on U56: **RULES v2 (live)** 8.61% / 1.1998 / −12.05%, halves
1.2349 / 1.1718, OOS 9.45% / **1.2747** / −12.05%; **SPY** 15.11% / 0.8835 / −33.72%, OOS
15.24% / 0.8721 / −33.72%. **Both picks beat SPY's OOS Sharpe and neither beats the live
book's.** Rule 8 never picks an interior panel — consistent with lane B's "q=0 in 4 of 4
books".

## Caveats
**SURVIVORSHIP:** SMALL439 and BSTK100 are current constituents of their screens, so every
small-cap and interior cell is biased upward by an unknown amount. The reported quantity is the
**corner-vs-interior contrast**, not the level — but the contrast is not immune: if survivorship
inflates the q=1 corner more than q=0, the measured curvature absorbs part of that. The
drawdown result is the least exposed of the four (a shallower MaxDD at q=0.5 than at *both*
endpoints cannot be produced by a monotone bias in either endpoint alone). Seed dispersion at
8 seeds gives a noisy SE, so individual |z| values are indicative and the **median across
metrics** is the reported statistic. The census is keyword-based, not semantic.

## For the queue
This run adds nothing to lane B's verdict and should not be cited beside it as a second
observation of the same fact — it is a replication. Its one transferable by-product is the
`q`-overloading trap: **48.9% of loose `q<number>` hits in this record are quantile thresholds,
not cap mixes.** Ideas 674, 675 and 677 all key on `q` and should say which `q` they mean.
