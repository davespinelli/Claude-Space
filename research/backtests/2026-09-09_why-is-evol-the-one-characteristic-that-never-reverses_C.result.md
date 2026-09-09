# Idea 533 — why is `evol` the one characteristic that never reverses?

**Lane C, 2026-09-09.** Script `2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C.py`
(deterministic, seed 20260909, no network). Costs 10 bps, weekly, next-day execution.
**RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No KEEP, no memo.**

## VERDICT — ANSWERED / **KILL of the "genuine within-panel effect" reading**, and the premise is
## also **NOT UNIQUE**: `evol` is the VOL CHANNEL, i.e. a restatement of the book's own realised vol.

Three findings, in order of how much they change the record.

**(1) `evol` is by far the most collinear characteristic with the BOOK'S OWN realised vol — the
queue's suspicion is confirmed as fact.** Within-stratum corr(evol, book vol), full window:
EWall +0.736..+0.851, top10 +0.644..+0.748, top20 +0.066..+0.599 (median over all cells **+0.659**).
The other three: disp +0.419, breadth −0.256, corr +0.009. Pooled across the cap line evol reaches
**+0.930** on EWall. On an equal-weight-eligible book the two are close to the same variable by
construction, and that is exactly the book idea 295's quoted cell used.

**(2) The published within-stratum slope dies on the book where the collinearity is highest, and
the log-log arbitration kills it everywhere.** evol vs MaxDD, `none` → `partial` (|t| ≥ 1.96):

| arm | sig without control | with control | t without | t with | corr(evol, bookvol) |
|---|---|---|---|---|---|
| EWall | 4/4 | **0/4** | −8.74..−5.96 | +0.90..+1.94 | +0.736..+0.851 |
| top10 | 3/4 | 3/4 | −5.82..−1.62 | −3.74..+0.13 | +0.644..+0.748 |
| top20 | 3/4 | 3/4 | −5.43..−1.63 | −5.36..−0.70 | +0.066..+0.599 |

The linear control and the ratio control **disagree** (on EWall `ratio` returns +8.0..+8.9, the
opposite sign, because 1/bookvol dominates that specification, and DDnorm = MaxDD/bookvol keeps
t −4.3..−3.2), so neither is quoted alone. Drawdown is multiplicative in vol, so the run arbitrates
with the elasticity form `log|MaxDD| ~ log(char) + log(bookvol)` within stratum:

* raw: evol elasticity **+1.95..+2.53, t +7.4..+2.5, 10/12 cells non-zero**;
* holding log(book vol): **−0.858..+0.908, 4/12 non-zero, and not sign-stable across arms**
  (EWall −2.08, top20 +4.04) — on EWall 1/4;
* the mediator's own elasticity in the same fits: **+2.62..+2.78 (EWall), +0.18..+1.08 (top20)**.

Drawdown is a function of the book's realised vol; `evol` is how the panel delivers that vol.

**(3) Rule 8 separates the two cleanly, and it is the UNCONTROLLED relation that is stable.** Over
576 (outcome × char × strata × resid × arm) cells the IS verdict returns OOS in 379 (65.8%) and the
IS sign in 441 (76.6%). For evol vs MaxDD specifically: the **uncontrolled** slope's sign holds
IS→OOS in **12/12** cells (EWall t −12.49 → −7.44), while the **controlled** residue's sign holds
in 8/12 and on EWall only **1/4** (−2.13 → +2.45, a sign reversal). The part of `evol` that is the
book's vol survives out of sample; the part that is not, does not.

**(4) The queue's premise as worded is an overstatement.** Sign-keeping cells, full window, 36
each: **evol 31/36, breadth 30/36**, disp 18/36, corr 13/36. `evol` is not "the one characteristic
that never reverses" — breadth vs MaxDD keeps its sign in 12/12 cells too (9/12 significant), and
evol itself flips in 5 of 36 (4 on CAGR, 1 on Sharpe). What is true of evol and of nothing else is
that its **MaxDD** column never reverses AND stays significant in 10 of 12 cells.

## What this does and does not license

The book's realised vol is **downstream** of the panel: a higher-vol eligible set mechanically makes
a higher-vol book. Conditioning on it is a **mediator** control, not a confounder control. So the
honest statement is **"evol's drawdown content runs THROUGH the book's own vol"**, not "evol's
drawdown content is spurious". The distinction matters for how the record may quote it:

* **Not licensed:** "eligible-set vol carries within-panel information about drawdown beyond the
  book's own exposure." Four of four EWall cells lose significance, the elasticity loses its sign
  stability, and the OOS leg fails on that residue.
* **Licensed:** "a higher-vol eligible set produces a higher-vol book and therefore a deeper
  drawdown" — elasticity of |MaxDD| on the book's own vol +0.18..+2.78, sign-stable everywhere,
  and the only evol relation that survives rule 8 in all 12 cells.
* **Required alongside any future quote:** the ARM. The same characteristic, same panel, same
  resolution gives 4/4 or 0/4 depending on whether the book is equal-weight-eligible or top-n.
  Any published `evol` direction claim that does not name its book is not re-readable.

## Both KEEP paths, every arm-row, no selection

504 arm-rows (168 panels × 3 books), medians:

| arm | CAGR | Sharpe | MaxDD | Vol | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| EWall | 8.8% | 0.726 | −27.9% | 0.126 | 0.914 / 0.599 | 8.4% | 0.692 | −27.8% | 0/168 | 11/168 |
| top10 | 9.1% | 0.712 | −23.9% | 0.139 | 0.808 / 0.590 | 9.1% | 0.681 | −23.7% | 0/168 | 3/168 |
| top20 | 7.7% | 0.777 | −18.4% | 0.105 | 0.880 / 0.674 | 7.7% | 0.744 | −18.3% | 0/168 | 27/168 |
| RULES v2 (live, same panels) | 6.4% | 0.857 | −13.2% | — | 0.941 / 0.767 | 6.3% | 0.835 | −13.2% | — | — |
| SPY | 14.1% | 0.862 | −33.7% | — | 0.891 / 0.858 | 15.5% | 0.882 | −33.7% | — | — |

**4a passes 0/504 (0.0%); 4b passes 41/504 (8.1%).** No arm of this run is proposed as a book: the
object under test is a slope. Every one of the 41 4b passes sits at **q ≤ 0.50** and 35 of 41 at
q ≤ 0.25 (top20 alone: 27 passes, all at q ≤ 0.40, 22 at q ≤ 0.20), consistent with idea 285's
cap-mix result and with the standing 2026-09-04 KEEP 4b candidate; nothing here restates either.

## Reproduction gates (both against committed artefacts)

* **G1 PASS** — the 504 arm-rows reproduce idea 295's committed `.arms.csv` on all 42 shared numeric
  columns, max |Δ| **2.22e-16**.
* **G2 PASS** — the 432 pooled/within slope rows reproduce idea 295's committed `.slopes.csv`,
  max |Δ| b_pooled 9.7e-17, t_pooled 3.6e-15, b_within 1.0e-16, t_within 1.8e-15. The queue's
  quoted range is re-derived, not believed: evol vs MaxDD within t on EWall **−8.74..−5.96** (the
  queue quotes −8.7..−6.0); over all 12 cells it runs −8.74..**−1.62**, so the quoted range is the
  EWall column, not the cell set.

## Parameters, grid, artefacts

Two tuned parameters, both fully reported: **resid** ∈ {none, partial, residx, ratio} and
**strata** ∈ {3, 5, 7, 21} — 16 points per characteristic × outcome × arm × window, 2,880 grid rows.
`residx` is the queue's literal wording and reproduces `partial`'s slope by Frisch–Waugh with a
different t; both are printed. |t| bar fixed at 1.96 (idea 295's central bar, not tuned here).
Artefacts: `.arms.csv` (504 rows, book vol added), `.slopes.csv`, `.premise.csv`,
`.collinearity.csv`, `.grid.csv`, `.survival.csv`, `.loglog.csv`, `.walkforward.csv`,
`.keeppaths.csv`, `.console.txt`.

**SURVIVORSHIP:** both ends of the q ladder are CURRENT constituents of their screens (sub-$2B panel
and B136), so every level here is optimistic. The claims are about a within-stratum slope and its
behaviour under a control, not about a level; no cross-q level comparison is offered as tradable.

## Follow-ups filed

538 (name the ARM beside every characteristic direction claim), 539 (re-price the record's other
characteristic claims against the book's own vol), 540 (is `disp` the second vol channel).
