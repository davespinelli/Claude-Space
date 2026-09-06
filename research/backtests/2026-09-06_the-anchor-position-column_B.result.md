# idea 183 — the-anchor-position-column (lane B, 2026-09-06)

**VERDICT: KILL as a trading rule; the schema column is DELIVERED and back-filled. The idea's own
premise survives only in a weaker, two-sided form than idea 173 implied.**

## Controls (asserted before any new number was read)

* **[a]** `fast_backtest` == `products/backtester/engine.backtest` to **1.4e-17** (returns) and
  **5.6e-16** (turnover) at W, **2.8e-17 / 1.0e-15** at M, on the 49-name complete-history slice of
  the live universe; `cad_mask` == `engine.rebalance_mask` at both. The engine's own 2 pre-warm-up
  NaN bars (its `shift(1)` is not re-filled) are counted and excluded explicitly.
* **[b] the decisive control.** The back-fill scanner, pointed at idea 173's committed `.grid.csv`,
  reproduces its committed `.anchorposition.csv` on **all 90 rows** to **2.6e-16** on
  `d_anchor / d_low / d_high` and exactly on `i_anchor / K`, and re-derives its published headline
  constants **0.74** and **0.32**. The scanner is therefore the same instrument idea 173 used.

## Deliverable 1 — the schema

`.schema.md` defines three mechanical columns: **ANCHOR-POS** (`i/K`, the control's 1-based position
on the ordered grid), **ANCHOR-EDGE** (1 if `i ∈ {1,K}`), **ANCHOR-RANK** (rank of the control's own
outcome, 1 = best). ANCHOR-POS and ANCHOR-RANK are deliberately separate: *where it sits* is not
*how it did*, and idea 173's result conflates them.

## Deliverable 2 — the back-fill (the count idea 183 asks for)

570 committed CSVs; 243 carry an OOS Sharpe column; **29 files yield 10,593 auditable ladders**
(K ≥ 3, one row per grid value, and the grid contains RULES v1's own incumbent — a grid that does
not contain the incumbent is recorded unauditable, never re-anchored onto its nearest point).

| dial | files | ladders | anchor | EDGE share | at low edge | median ANCHOR-RANK | median d_anchor |
|---|---|---|---|---|---|---|---|
| GROSS | 8 | 858 | 0.75 | 4.4% | 1.5% | 4 / 10 | +0.0000 |
| COUNT | 2 | 134 | 5 | 4.5% | 4.5% | 2 / 5 | −0.0136 |
| CADENCE | 3 | 1517 | W | **79.4%** | **79.4%** | 2 / 5 | −0.0281 |
| COST | 16 | 7402 | 10 bps | 0.3% | 0.3% | 2 / 5 | −0.0299 |
| BAND | 2 | 24 | 0.00 | 100% (by construction) | 100% | 3 / 3 | +0.0447 |
| SLEEVE | 2 | 658 | 0.00 | 100% (by construction) | 100% | 3 / 3 | +0.1003 |

**THE ANSWER: 1,951 of 10,593 auditable ladders (18.4%) had the control at a grid edge; on the five
headline dials — the ones the record actually argues about — it is 1,248 of 2,509, or 49.7%.**
Restricted to the 1,656 ladders where the claim was actually made (a uniform ladder draw beats the
control in expectation), 1,067 (64.4%) were edge-anchored.

The driver is CADENCE: **79.4% of the record's cadence ladders start AT W**, so RULES v1's own
weekly cadence has no faster neighbour to be averaged against, and every "slower beats weekly"
sentence in the record is measured from the low edge of its own grid.

**The pooled 3.50x over-representation ratio is a Simpson artefact and is NOT claimed.** COST supplies
7,402 of 10,593 ladders at a 0.3% edge share, and BAND/SLEEVE are edge-anchored 100% of the time
because RULES v1 has neither dial. Stratified on the five headline dials the ratio is **0.81x** — an
edge anchor is *not* more likely to have been beaten. The finding is the level, not the ratio.

## Deliverable 3 — the re-anchoring sweep (51,764 rows)

Sorting by the anchor's **outcome rank** forces beat-rate 0.000 at rank 1 and 1.000 at rank K; that
table is printed as a tautology check only and is not scored. The non-forced statement is by **grid
coordinate**:

| anchor placed at | RANDOM beats it | mean d_random | mean d_oracle |
|---|---|---|---|
| grid pos 1 (low edge) | 0.166 | −0.0483 | +0.0317 |
| grid middle | 0.211 | −0.0069 | +0.0732 |
| grid pos K (high edge) | **0.864** | +0.0652 | +0.1452 |
| the TRUE anchor | 0.156 | −0.0198 | +0.0602 |

**Moving only the control, on otherwise byte-identical ladders, swings "a random draw beats the
control" by 0.698.** The record's dials are predominantly *increasing* in their grid coordinate, so
the cheap control to nominate is the HIGH end — not the low end idea 171 happened to use.

**The bias is two-sided, and P4 missed in the informative direction.** Median claimed margin with the
anchor at an edge is 0.0389 vs 0.0666 at the middle — a ratio of **0.58x**, not the >1.5x predicted.
Because the record's edge anchors sit predominantly at the LOW end of increasing dials, where the
anchor is often the ladder's *best* point, an edge control is on average **harder** to beat. A reader
cannot even sign the bias without the position, which is a stronger argument for publishing the
column than the one-sided story idea 183 assumed.

## Deliverable 4 — fresh live sweep, 75 backtests, 3 panels × 3 dials

| panel | dial | K | anchor | ANCHOR-POS | ANCHOR-RANK | d_anchor (OOS) | argmax |
|---|---|---|---|---|---|---|---|
| U56 | GROSS | 9 | 0.75 | 5/9 | 5/9 | −0.0003 | 1.35 |
| U56 | COUNT | 9 | 5 | 2/9 | 7/9 | +0.1225 | 40 |
| U56 | CADENCE | 7 | W | 3/7 | 3/7 | −0.0851 | 6W |
| ETF36 | GROSS | 9 | 0.75 | 5/9 | 5/9 | −0.0003 | 1.35 |
| ETF36 | COUNT | 9 | 5 | 2/9 | 8/9 | +0.1984 | 30 |
| ETF36 | CADENCE | 7 | W | 3/7 | 4/7 | +0.0044 | 6W |
| SMALL439 | GROSS | 9 | 0.75 | 5/9 | 5/9 | +0.0001 | 1.35 |
| SMALL439 | COUNT | 9 | 5 | 2/9 | 8/9 | +0.0314 | 10 |
| SMALL439 | CADENCE | 7 | W | 3/7 | 2/7 | −0.0942 | 6W |

GROSS is flat to 4 decimals across a 9x range (confirming idea 173); COUNT is where RULES v1's n=5
is badly placed — rank 7/9, 8/9, 8/9 — and its position (2/9) is the near-low-edge case idea 183
warns about. CADENCE's argmax is 6W on all three panels, consistent with ideas 175/187.

## Rule 8 walk-forward (parameters on ≤2016-12-31, 2017-01-01.. read once)

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | vs RULES v1 | vs SPY |
|---|---|---|---|---|---|
| ANCHOR (RULES v1 incumbent) | 11.19% | 0.6667 | −28.11% | −0.0160 | −0.2153 |
| IS-PICK (ladder argmax on IS) | 10.91% | **0.7025** | −24.45% | +0.0198 | −0.1795 |
| ORACLE (not implementable) | 14.25% | 0.8151 | −31.17% | +0.1324 | −0.0669 |
| RULES v1 | 10.87% | 0.6827 | −24.16% | | |
| SPY | 15.45% | 0.8820 | −33.72% | | |

**The column carries no OOS Sharpe.** All 9 fresh ladders have an interior anchor, so the
interior-anchor filter removes 0 of them and its OOS delta is exactly 0.0000 by construction; the
IS-PICK-minus-ANCHOR gap is +0.0359, inside the ±0.05 band pre-registered as "no content". On the
archival corpus, edge-anchored controls have a *higher* mean OOS Sharpe (0.8373) than interior ones
(0.7583), which is a statement about which books get run at edges, not about the filter's skill.
Nothing beats SPY out of sample here.

## KEEP paths on all 75 fresh points

**4a 7/75, 4b 3/75** — all three 4b passes are U56 COUNT at n ∈ {15, 20, 30}, and n=20 is also what
rule 8 picks in-sample (OOS 1.1775). It fails the universe change (ETF36 0.9049 OOS with H1 0.749 <
SPY; SMALL439 0.4873) and is idea 182's already-PARKed U56 top-20 book under a different score and
cadence, which idea 144 says is the same book. **PARKed and memo'd (`.memo.md`), not proposed.**

## Predictions scorecard

| | prediction | actual | |
|---|---|---|---|
| P1 | controls [a] and [b] hold | 1.4e-17 / 2.6e-16, 0.74 & 0.32 re-derived | **HIT** |
| P2 | EDGE share ≥ 25% | 18.4% pooled (49.7% on headline dials) | **MISS** |
| P3 | grid-position beat-rate spread > 0.50 | 0.698 | **HIT** |
| P4 | edge margin > 1.5x middle margin | 0.58x — bias is two-sided | **MISS** |
| P5 | rule 8 \|IS-PICK − ANCHOR\| < 0.05 | 0.0359 | **HIT** |
| P6 | no new 4b beyond a re-parameterisation | 3/75, all one known U56 book | **HIT** |

## Caveats

* Only ladders **committed as CSV with the dial in a column** are visible. A claim whose ladder lives
  in prose or a console dump is counted unrecoverable, never as interior.
* ANCHOR-POS is defined on the grid **as run**. A grid designed around the incumbent looks interior
  by construction — a fact about the designer, and the reason the column must be published rather
  than inferred.
* COST is in the registry because 10 bps is a PROTOCOL constant, but a cost ladder is not a
  control-beating claim in the ordinary sense; BAND and SLEEVE anchor at 0.00 and are edge-anchored
  by construction. The headline count is stated with and without all three.
* Survivorship: U56 / ETF36 / SMALL439 are current-constituent lists (idea 54,
  `data/SMALL_PANEL_README.md`). Paired position comparisons are unaffected; no level is attainable.
* Idea 126: t+1 execution only, 10 bps only on the fresh sweep.

## Files

`.py .console.txt .backfill.csv .reanchor.csv .claims.csv .perdial.csv .position.csv .ladder.csv
.freshpos.csv .keep.csv .walkforward.csv .schema.md .memo.md`
