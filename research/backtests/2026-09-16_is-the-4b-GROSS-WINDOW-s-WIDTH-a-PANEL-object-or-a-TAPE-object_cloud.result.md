# Idea 1152 (cloud lane, 2026-09-16) — is the 4b GROSS WINDOW's WIDTH a PANEL object or a TAPE object?

**ANSWERED = BOTH, and the queue's either/or is the wrong question.** Width is a panel object
AND a tape-length object; at matched length the panel term is the larger of the two (1.473x),
and on the SMALL panel the window is not narrow but **STRUCTURALLY EMPTY at 0 of 33 rungs**,
for a reason no setting of gross can repair.

Script: `2026-09-16_is-the-4b-GROSS-WINDOW-s-WIDTH-a-PANEL-object-or-a-TAPE-object_cloud.py`
(standalone, offline, deterministic, 148 s). Console: `.console.txt`.

## What was run

Two tuned dials, exactly as the queue names them: **PANEL** {U56, B136, SMALL} x **SUB-TAPE
FRACTION** f in {1, 2, 3, 4, 6}. The 33-rung gross ladder (0.200..1.000 step 0.025) is the
object being measured, not a dial, and every rung is published at every cell. Cost frozen at
the PROTOCOL's 10 bps. **Controls, never selected on:** TAPE {T_OWN, T_MATCHED — every panel
restricted to the SMALL panel's own 4,198 trading days, so the three are matched row for row}
and PARTITION {ALIGNED, OFFSET}. Everything else is frozen at 1150's construction (CAND20,
N=20, H=126, W, LAG 1, warm-up 260, IS end 2016-12-31).

Published: `.grid.csv` 10,692 rows (every panel x tape x partition x fraction x stretch x
rung), `.windows.csv` 324 stretch-windows, `.fulltape.csv` 198 full-tape rungs, `.nulls.csv`
60 null ladders, `.verdict.csv`, `.length.csv`, `.walkforward.csv`, `.hypotheses.csv`,
`.gates.csv`.

## Gates — 9 of 9 PASS

| gate | what | value |
|---|---|---|
| G1 | fast runner ≡ `engine.backtest` (U56 W/H126/N=20, g=0.75) | 2.08e-17 |
| G2 | CROSS-RUN the committed U56 W/H126/N=20 triple | 3.18e-07 |
| G3 | SPY OOS triple on U56's own tape | 1.70e-04 |
| G4 | live RULES v2 MaxDD ≡ committed −12.05% | 4.95e-05 |
| G5 | determinism of the SMALL pipeline | 0.00e+00 |
| G6a | 1150's committed grid present and carrying the quoted window | 0.00e+00 |
| G6 | **CROSS-RUN 1150's five-leg window reproduced rung for rung** (U56 0.525..0.775 = 11; B136 0.500..0.725 = 10) | 0.00e+00 |
| G7 | the four-leg CORE window contains the five-leg window at every f=1 cell | 0.00e+00 |
| G8 | **where no Sharpe leg binds, WIDTH ≡ 33 − \|L_DD fails\| − \|L_CAGR fails\|** | 0.00e+00 |

## The width table (median over stretches; f=1 is the whole warm tape)

T_MATCHED (all three panels on the same 3,938 warm days):

| panel | f=1 | f=2 | f=3 | f=4 | f=6 |
|---|---|---|---|---|---|
| U56 | **11** | 8 | 8 | 0 | 0 |
| B136 | **6** | 2 | 0 | 0 | 0 |
| SMALL | **0** | 0 | 0 | 0 | 0 |

T_OWN (each panel over its own tape): U56 11 / 9 / 9 / 0 / 0; B136 10 / 4.5 / 9 / 0.5 / 0;
SMALL 0 / 0 / 0 / 0 / 0. Excluding the stretches where SPY's own CAGR is ≤ 0 (a floor that
rewards losing) changes not one cell of either table.

**Contiguity: 324 of 324 stretch-windows are contiguous, 0 carry a gap.** 1150's "window"
word survives every panel, every fraction and every partition — including the 241 of 324
stretch-windows that are EMPTY, which are trivially contiguous and are the reason the
fraction ladder's floor is a censoring floor, not a measurement.

## Why the width is what it is

Per-leg failure count over the 33 rungs (`.fulltape.csv`):

| tape | panel | L_H1 | L_H2 | L_OOS | L_DD | L_CAGR |
|---|---|---|---|---|---|---|
| T_OWN | U56 | 0 | 0 | 0 | 9 | 13 |
| T_OWN | B136 | 0 | 0 | 0 | 11 | 12 |
| T_OWN | SMALL | **33** | **33** | **33** | 25 | 32 |
| T_MATCHED | U56 | 0 | 0 | 0 | 9 | 13 |
| T_MATCHED | B136 | 0 | 0 | 0 | 15 | 12 |
| T_MATCHED | SMALL | **33** | **33** | **33** | 25 | 32 |

On U56 and B136 no Sharpe leg binds at any rung, so (G8) the width is *arithmetic*: 33 minus
the two opposed exposure legs' failure counts, exactly. Length-matching costs B136 four rungs
(10 → 6) and U56 none (11 → 11), and it does so entirely through L_DD (11 → 15 failures).

**On SMALL every Sharpe leg fails at every rung.** Gross moves CAGR and drawdown and is very
nearly Sharpe-neutral, so no rung of the ladder can rescue a panel whose book loses to SPY on
Sharpe. The SMALL zero is therefore not a narrow window — it is a different kind of object,
and averaging it into a "width" alongside U56's 11 mixes two things.

## The verdict rule, and what it says

Declared before any number: PANEL object iff the between-panel spread of width at matched
length exceeds the within-panel spread across equal-length stretches, both using 1157's
count-matched pairwise statistic (never a max-minus-min, 1155's defect).

| tape | partition | between | within | ratio | verdict |
|---|---|---|---|---|---|
| T_OWN | ALIGNED | 5.806 | 2.347 | 2.474 | PANEL |
| T_OWN | OFFSET | 6.604 | 3.108 | 2.125 | PANEL |
| **T_MATCHED** | **ALIGNED** | **5.191** | **3.524** | **1.473** | **PANEL** |
| T_MATCHED | OFFSET | 0.000 | 2.060 | 0.000 | TAPE |

(each also run excluding spy_down stretches; 8 readings in all, **PANEL 6, TAPE 2**.)

**Stated rather than buried:** the two TAPE readings both have a between-panel spread of
*exactly zero*, not because the panels agree but because all three panel medians are censored
at 0 under the OFFSET partition. A TAPE verdict reached that way is a floor artefact.

And the tape term is real too: width rises with log tape length at +6.66 (U56) and +4.96
(B136) rungs per log-day on T_OWN, +4.22 / +1.63 on T_MATCHED, spearman +0.26 to +0.64. Both
H_PANEL and H_TAPE read YES. Width is **both**, with the panel term larger at matched length.

## The gross-matched random-book null (20 seeds, T_MATCHED)

| panel | book width (core / five) | null median | null range | book strictly above |
|---|---|---|---|---|
| U56 | 11 / 11 | 0.0 | [0, 6] | **1.000** |
| B136 | 6 / 6 | 0.0 | [0, 4] | **1.000** |
| SMALL | 0 / 0 | 0.0 | [0, 0] | **0.000** |

A random 20-name book of the same gross, cadence and hold gets a *median width of zero* on
every panel and never reaches the real book's. **Tie warning, stated rather than buried:** the
conventional ≤ percentile reads 1.000 for SMALL too, purely because every null draw ties the
book's 0 — the strictly-above column is the honest one and reads 0.000 there. Null windows are
contiguous at 20 of 20 seeds, so contiguity itself is mechanical and is not evidence.

## Rule 8 walk-forward — the window does not survive it

Parameters chosen on ≤ 2016-12-31 only, evaluated on the untouched second half.

| tape | panel | IS window | OOS window | Jaccard |
|---|---|---|---|---|
| T_OWN | U56 | 6 [0.575..0.700] | 13 [0.475..0.775] | 0.462 |
| T_OWN | B136 | 8 [0.500..0.675] | 9 [0.525..0.725] | 0.700 |
| T_OWN | SMALL | 0 (empty) | 0 (empty) | n/a |
| T_MATCHED | U56 | 1 [0.575] | 11 [0.525..0.775] | **0.091** |
| T_MATCHED | B136 | **0 (empty)** | 6 [0.500..0.625] | 0.000 |
| T_MATCHED | SMALL | 0 (empty) | 0 (empty) | n/a |

Where an IS window exists at all it is 3 of 3 for containing its own midpoint inside the OOS
window — but it fails to exist in **3 of 6 cells**, and on T_MATCHED/U56 the IS window is a
single rung against an 11-rung OOS window. H_WF reads NO. The honest summary: *an
out-of-sample window is not something the first half tells you the width of.*

The IS-Sharpe chooser picks the top rung g=1.00 on 6 of 6 cells — 1101/1150's boundary-pick
finding again, reproduced here on a third construction. Its OOS triples:

| tape | panel | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | SPY OOS | live book OOS |
|---|---|---|---|---|---|---|---|
| T_OWN | U56 | 1.00 | 22.72% | 1.165 | −24.93% | 15.21% / 0.871 / −33.72% | 1.276 / −12.05% |
| T_OWN | B136 | 1.00 | 21.30% | 1.012 | −26.97% | 15.33% / 0.877 / −33.72% | 1.106 / −12.24% |
| T_OWN | SMALL | 1.00 | 8.69% | 0.454 | −45.42% | 15.33% / 0.877 / −33.72% | 0.560 / −13.89% |
| T_MATCHED | U56 | 1.00 | 21.28% | 1.110 | −25.00% | 15.33% / 0.877 / −33.72% | 1.277 / −12.07% |
| T_MATCHED | B136 | 1.00 | 22.39% | 1.020 | −30.08% | 15.33% / 0.877 / −33.72% | 1.105 / −12.25% |
| T_MATCHED | SMALL | 1.00 | 8.69% | 0.454 | −45.42% | 15.33% / 0.877 / −33.72% | 0.560 / −13.89% |

Every one of those picks fails 4b's drawdown cap (0.60 x 33.72% = 20.23%), which is precisely
why the chooser's endpoint is outside the window.

## Both KEEP paths

- **4a (beat the live book): 0 of 198** full-tape (gross, tape, panel) cells; 371 of 10,692
  sub-tape rows, none of them a book anyone could have chosen in advance.
- **4b full-tape five-leg:** U56 11/33 and B136 10/33 on their own tapes, U56 11/33 and B136
  6/33 length-matched, **SMALL 0/33 on both**.
- **NOTHING IS PROPOSED.** Every 4b pass here is a rung of the incumbent CAND20 book that 1150
  already published; this run measures the width of that pass set. RULES.md, PROTOCOL.md,
  scan.py, bot.py and baseline.py are untouched (rule 6).

## Hypotheses

| | | |
|---|---|---|
| H_REPRO | 1150's five-leg window reproduces rung for rung | **YES** |
| H_CONTIG | the pass set is a contiguous window at ≥ 90% of stretch cells | **YES** (324/324) |
| H_PANEL | width is a panel object (between > within) | **YES** (1.473x, 6 of 8 readings) |
| H_TAPE | width is a tape-length object (rises with log length) | **YES** (+1.63 to +6.66) |
| H_NULL | the width is not reachable by a gross-matched random book | **YES** on U56/B136, vacuous on SMALL |
| H_WF | the IS window's midpoint is inside the OOS window on a majority of cells | **NO** (3 of 6; the IS window does not exist in the other 3) |

## Limits

- **SURVIVORSHIP (rule 9):** all three panels are current-constituent lists and the SMALL pool
  is the current output of a sub-$2B screen, so every panel is biased upward and SMALL most of
  all. The SMALL reading here is that the book fails 4b *even with* that bias.
- The fraction ladder censors at 0: 241 of 324 stretch-windows are empty, so slopes fitted
  through f=4 and f=6 are fitted through a floor and are lower bounds on the length effect.
- 20 null seeds resolve a percentile to ±0.05, no finer; the null is a random-selection book,
  not a rotation of the real one.
- Width is an integer on a 33-rung grid, so every spread quoted here is quantised at 1 rung;
  the 5.191 vs 3.524 headline is 1.7 rungs of separation and should not be read as more.
