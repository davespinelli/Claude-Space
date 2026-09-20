# Idea 1632 (lane C, 2026-09-20) — is the BAND's U56-only survival a PANEL effect or a NAME-COUNT effect?

**VERDICT: ANSWERED — PANEL. KILL the name-count hypothesis; CONFIRM idea 1617's reading. NO NEW BOOK.**

## What was at stake
Idea 1617 priced every eligibility filter the record owns against a twin matched on **realised** mean
gross and found exactly one convincing survivor: the live band `c = 0.03`, on **U56 alone**. That single
cell is the live book's only matched-exposure win in the whole record. U56 is confounded: it is both a
different panel *and* the smallest panel by name count, and under the live weighting convention
(`gross / N_priced` per eligible name, gated-out weight to cash) the band is a **breadth** device — one
gated name moves realised gross by `1/56` on U56 and by `1/665` on SMALL. A contrast that shrinks like
`1/N` would have reproduced 1617's whole cross-panel ordering with no panel content at all.

## Construction
Two dials and no more: **N_NAMES** (uniform seeded draws without replacement from each panel's own
traded column set; ladder 20 / 36 / 56 / 100 / 136 / 300 truncated at each panel's size, plus the panel's
FULL set as the ALL rung) x **BAND c** {0.00, 0.03, 0.06, 0.10}. Published but not tuned: PANEL
{U56, B136, SMALL}, DRAW (24 per rung below ALL; 291 draws in total), COST {0, 10, 25, 50} bps.
Every band book is paired with its **own** de-gross twin — the same names with no gate, scaled by a
constant `k` solved so the twin carries the **same realised mean gross** to machine precision (`k` is
solved in closed form: inside a rebalance segment the scaled book's gross path is
`kGP / (kGP + 1 - kGF0)` with `P`, `F0` independent of `k`, gated at G11). **1,164 band books + 1,164
twins x 4 cost rungs = 4,656 rows, all published.**

## Replication first
The ALL rungs reproduce idea 1617 exactly, to the published digit:

| panel | dSharpe FULL | dSharpe OOS |
|---|---|---|
| U56 (56) | **+0.0827** | **+0.1499** |
| B136 (136) | **-0.0161** | **+0.0136** |
| SMALL (665) | **-0.0461** | **-0.0520** |

## The answer
**H0 (name-count) required mean dSharpe to DECREASE in N. It decreases at 9 of 48 ladder steps — 0 of 8
on U56, 1 of 16 on B136, 8 of 24 on SMALL.** The direction is the opposite of the hypothesis.

* **At the matched rung N = 56, 0 of 48 subsamples reach U56.** B136 draws land at FULL -0.0371
  (sd 0.0412), SMALL at -0.0851 (sd 0.0654), against U56's +0.0827: share >= U56 **0.000 / 0.000**
  (z **+2.91 / +2.57**); OOS **0.000 / 0.000** (z **+3.79 / +3.27**). Same at the plain 200d gate
  c = 0.00 (z +2.01 / +2.71 FULL, +2.23 / +3.50 OOS).
* **U56 subsampled DOWN shrinks the contrast**: c = 0.03 gives +0.0827 (N=56) -> +0.0610 (36) ->
  +0.0515 (20). A breadth law predicts growth.
* **SPY is not the mechanism.** U56 draws *without* SPY score +0.0592 against +0.0542 with it.

## Which leg carries it
Splitting band-minus-twin into its two legs settles the mechanism. The **drawdown credit is near
panel-invariant and flat in N above 56** (c = 0.03: U56 **+4.34 pp**, B136 +5.93, SMALL +6.45 — U56 gets
the *smallest* credit). The **CAGR cost is flat in N inside a panel and a ~3x effect across them**
(U56 **-0.72 pp/yr**, SMALL -1.46, B136 **-1.99**). The band does the same thing to drawdown everywhere;
it simply costs U56's names less return. There is no breadth content in either leg.

## Capital arm (both KEEP paths at every book and every twin)
Of 1,164 band books at the binding 10 bps: **19 clear 4a FULL, 5 clear 4b FULL, 3 clear 4b FULL *and*
OOS** (all U56, N=20, draws 3 and 18 at c = 0.03/0.10), and none of those 3 clears 4a. Their own matched
twins clear 4b FULL **19 (U56) / 53 (B136)** against the band books' 4 / 1 — **on the protocol's capital
bar the plain de-gross is the better book even where the band wins on Sharpe.** The 4b CAGR floor fails
on **0.996** of band books (DD cap only 0.069). Cost ladder: 4b FULL 6 / 5 / 4 / 0 at 0 / 10 / 25 / 50 bps.

## Rule 8 (2017-2026 read exactly once)
Three IS-only choosers x 3 panels. **0 of 9 picks clear 4a OOS and 0 of 9 clear 4b OOS**, every one on
the CAGR floor (8 of 9 pass the DD cap). The live inheritance is the best OOS contrast anywhere in the
run — U56 C_LIVE dSharpe **+0.1499** — and still delivers OOS **9.46% / 1.2769 / -12.05%** against
SPY **15.26% / 0.8738 / -33.72%** and a 10.68% floor. The 3 books that do clear 4b FULL&OOS are specific
random 20-name subsets of U56 that no chooser reaches: hindsight, recorded as such.

## Residue for the record
The band's **drawdown credit is a constant of the construction**, not a panel or breadth result, and
should stop being re-priced panel by panel. Its **return cost is the only panel-dependent leg**, so any
future claim that "the band works on panel X" is a claim about what the band costs X's names in return
and should be written that way.

Gates **19/19**. G1/G2/G3/G11 against `engine.backtest` at 0.000e+00 - 6.2e-15; G4 realised-gross match
0.000e+00; G6 no chooser statistic reads a row on or after 2017-01-01. RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched (rule 6).

**Survivorship (rule 9):** U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen
carried back to 2010 (54 names dropped at `max_1d_move >= 1.0`; 665 remain). The headline is a
band-minus-twin contrast inside one draw, over the same names on the same days at the same realised
exposure, so it is first-order immune; the 4b pass counts are not.

`research/backtests/2026-09-20_band-u56-panel-or-namecount_C.py`
