# Idea 359 — census: how many "band" rows changed the book's WIDTH, not its trading rule?

**Lane C, 2026-09-07. Verdict: SPLIT — the queue's METHOD is unusable on the record as
committed (5.3% of band rows are recoverable), but the QUESTION is answerable by
re-measurement and the answer is NO: 2 of 206 band rows (1.0%) sit on a construction that
changes the book's width. No KEEP: 4a 0/126 at every cost rung.**

## What was asked

Idea 349 found that a cell reported as a *band* can hold 7.6 names where its parent holds
19.1 — its ENTRY buffer `e` moves holdings (spearman −0.988) far more than turnover
(−0.298). The queue asked how many of the record's committed band rows are of that kind.

## [A] The census — and why the queue's own method cannot answer it

3,055 leaderboard data rows. 209 (6.8%) match the band lexicon; 3 are INTERVAL rows
("admissible gross band" — a parameter interval, not a banded rule), leaving **206
INSTRUMENT rows across 72 distinct scripts**.

The queue's literal instruction was to *recover mean holdings from the committed CSVs*.
On this record that is mostly impossible:

| | rows |
|---|---|
| INSTRUMENT band rows | 206 |
| ...whose script committed any CSV | 143 |
| ...with a holdings-like column anywhere | 18 |
| ...with a band-dial column anywhere | 101 |
| **...RECOVERABLE (both, in one CSV)** | **11 (5.3%)** |

**The record writes the dial 9× more often than it writes the width.** That is the run's
first finding and it is an infrastructure defect, not a modelling one.

## [A2] The literal recovery, where it is possible

The 11 recoverable rows resolve to 93 dial→holdings ladders inside committed CSVs.
Restricting to ladders whose *script name* itself carries a band cue (so the dial is a
band and not idea 318's width multiplier or idea 103's share multiplier) leaves 46:

- dial column `e` (entry buffer): **15/15 width-changing** — all from idea 349 and idea 357
- dial column `m` (no-trade band): **0/31 width-changing** — holdings identical to the last
  decimal at every `m`, on every panel and cadence

This is read straight out of numbers other runs committed, with nothing re-run, and it
agrees exactly with the re-measurement below.

## [B] Direct measurement — four band constructions, 126 cells

Book fixed at idea 331/349's convention (composite with the vol scaler OFF, RULES v1
eligibility, NORM weights g/k at g = 0.75, WEEKLY, next-day execution). Two tuned
parameters: the band dial and n ∈ {10, 20}. Panel, family and cost rung {0,10,25} bps are
reported axes; all 126 cells × 3 rungs are in `.grid.csv`.

| family | dial | width-changing cells | median \|ΔNames\|/parent | median ρ(dial,names) | median ρ(dial,turnover) | verdict |
|---|---|---|---|---|---|---|
| MAB-EWALL | b 0→0.12 | 0/3 | 0.036 | +0.143 | −1.000 | NEUTRAL |
| MAB-TOPN | b 0→0.12 | 0/6 | 0.003 | −0.829 | −1.000 | NEUTRAL |
| RANKX (exit buffer) | x 0→80 | 0/6 | **0.000** | 0.000 (names exactly constant) | −1.000 | NEUTRAL |
| RANKE (entry buffer) | e 0→12 | **6/6** | **0.524** | **−1.000** | −1.000 | **WIDTH-CHANGING** |

Pre-registered rule: WIDTH-CHANGING if |ΔNames|/parent > 5% at the family's largest
non-degenerate dial on a majority of (panel × n) cells. Three degenerate cells
(e ≥ n admits nobody, book holds 0 names) were dropped from the width reading and are
failed explicitly on both KEEP paths rather than passing on NaN comparisons.

**The mechanism is the slot cap, not the band.** Every construction whose slot count is
set independently of the dial — the k_t cap for RANKX, the hard top-n for MAB-TOPN, "hold
everything in band" for MAB-EWALL — is name-count-neutral. Only RANKE, where the buffer
can leave the cap unfillable, converts into concentration. So "is this band a width
change?" reduces to "can this dial starve the cap?", which is a property a reader can
check from the construction without running anything.

## [C] Attribution

| bucket | rows | construction verdict |
|---|---|---|
| MAB | 113 | NEUTRAL |
| RANKM (no-trade band) | 13 | NEUTRAL |
| RANKE (entry buffer) | 2 | **WIDTH-CHANGING** |
| UNATTRIBUTED | 78 | — |

**ANSWER: 2 of 206 (1.0%) width-changing, 126 (61.2%) neutral, 78 (37.9%) unattributable
from text.**

Robustness: MAB and RANKM are the only two buckets a reader could argue about (a string
like `BAND12` does not say whether 12 is a percentage or a rank). Both measure NEUTRAL, so
moving rows between them cannot change the answer. Only RANKE can, and its cue
("entry buffer" / "ENTRY side") is unambiguous.

Denominator warning, stated because the two numbers look contradictory: at the **ladder**
level 15 of 46 band-cued ladders (32.6%) are width-changing; at the **leaderboard-row**
level it is 2 of 206 (1.0%). Both are correct — idea 349 and 357 committed many ladders
each but few band-lexicon rows. The row-level number is the queue's literal question; the
ladder-level number is the better measure of how much *analysis* the record spent on a
width dial it called a band.

## [D] KEEP paths — all 126 cells

| rung | 4a | 4b |
|---|---|---|
| 0 bps | **0/126** | 53/126 |
| 10 bps | **0/126** | 35/126 |
| 25 bps | **0/126** | 20/126 |

No cell clears 4a at any rung: RULES v2 live (U56 Sharpe 1.206, H1 1.226 / H2 1.191,
MaxDD −12.1% at 10 bps) is not beaten by anything here. 4b failing bars at 10 bps:
H2 75, DD 68, OOS 58, H1 50, CAGR 38, DEGENERATE 3. Every 4b passer is on U56 or B136 and
reproduces a family the record already holds; **nothing here is proposed as a rules
change**. Flagged as a by-product for a dedicated run (new queue idea 360): U56 MAB-EWALL
at b = 0.12 clears 4b at 10 bps with CAGR 14.0%, Sharpe 1.226, MaxDD −19.4%, H1 1.261 /
H2 1.205, OOS 1.266 on only **1.93×/yr turnover** — but it fails 4a, and the census run is
not the place to price it.

## [E] Rule 8 walk-forward (dial chosen on ≤2016 IS Sharpe @10 bps; 2017–2026 read once)

21 (panel × family × n) cells. The IS chooser beats its own dial-0 anchor OOS in **15/21**,
mean regret vs the OOS-best dial **+0.0312**. Picks above SPY OOS (0.882): **11/21**.
Above RULES v2 OOS: **3/21** — B136 MAB-EWALL b=0.12 (1.162 vs 1.119), SMALL439 MAB-EWALL
b=0.12 (0.664 vs 0.568) and SMALL439 RANKE e=4 (0.585 vs 0.568); none on U56, where v2's
1.285 beats every pick. Panel OOS context:

| panel | best pick OOS Sharpe | anchor | SPY | RULES v2 |
|---|---|---|---|---|
| U56 | 1.266 (MAB-EWALL b=0.12) | 1.112 | 0.882 | 1.285 |
| B136 | 1.162 (MAB-EWALL b=0.12) | 1.065 | 0.882 | 1.119 |
| SMALL439 | 0.664 (MAB-EWALL b=0.12) | 0.535 | 0.882 | 0.568 |

The entry buffer is also the family an ex-ante chooser handles worst: RANKE carries 4 of the
6 largest regrets (SMALL439 n=20 +0.098, B136 n=10 +0.095, U56 n=10 +0.087, B136 n=20
+0.070; the other two are SMALL439 RANKX n=10 +0.112 and U56 MAB-TOPN n=20 +0.068), i.e.
the one construction that changes width is also the one whose dial is hardest to pick.

## Reproduction gates — all exact before any new number was read

| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` (returns, turnover) | 0.000e+00 / 0.000e+00 |
| G2 derived rung r(25) vs `backtest(cost_bps=25)` | 0.000e+00 |
| G3 `sel_buf(e=0,x=0)` nests the hard top-20 cut | 0 disagreements of 54,600 |
| G4 `band_state(b=0)` vs the hard 200d gate | 0.000e+00 |
| G5 reproduces idea 349's committed U56 e=0 rows (Sharpe_10) | 2.220e-16 |
| G6 reproduces idea 331's committed weekly U56 rows (Sharpe_10, names) | 0.000e+00 / 0.000e+00 |

## Proposed amendment (not applied — rules change only via Sunday review)

Add a `names` (mean holdings/day) column to every committed grid CSV, and quote mean
holdings on any LEADERBOARD row whose instrument can change the slot count. The record
currently writes the dial 9× more often than the width, which is the only reason this
question needed a re-run instead of a `pandas.read_csv`.

## Caveats

1. All three panels are current-constituent lists — **survivorship** — which flatters every
   momentum book; the levels are optimistic, the dial-differences much less so.
2. SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136
   and its rule-8 IS window is effectively 2010–2016.
3. [A] and [C] are **text classifications** of a hand-written leaderboard: reproducible but
   not authoritative. The full lexicon and every classified row are committed
   (`.census.csv`) so the call can be audited, and 37.9% of rows are reported as
   UNATTRIBUTED rather than being forced into a verdict.

## Files

`.py` · `.console.txt` · `.grid.csv` (126 cells × 3 rungs) · `.census.csv` (3,055 rows) ·
`.recovered.csv` (93 ladders) · `.ctx.csv` · `.walkforward.csv`
