# Idea 231 — the-gap-vs-tilt-rule-as-a-leaderboard-column (lane B, 2026-09-08)

**SPLIT: the question is ANSWERED and the queue's conditional FAILS. No tilt/gap ratio stops the
over-firing — at every one of the 20 thresholds swept, under both detection rules, the published
pair still over-fires. The pair does NOT belong beside a published argmax. A single
parameter-free replacement does: the MATCHED margin, which is exact on 8,529 of 8,529 cells.**

Two tuned parameters only: **p1** = the detection rule for "a swept dial inside a committed grid
CSV" (STRICT / LOOSE), **p2** = the ratio threshold *t*. All grid points of both reported.

## Corpus

Scanned all 1,824 committed `research/backtests/*.csv`. A cell is one complete
(dial value × cost rung) rectangle carrying a Sharpe column.

| p1 | cells | files | distinct dial columns | actual re-ranks | degenerate gap (≤0) |
|---|---|---|---|---|---|
| STRICT (one row per cell) | 8,529 | 95 | 30 | 1,653 (19.4%) | 651 |
| LOOSE (duplicates median-collapsed) | 9,748 | 110 | 33 | 1,808 (18.5%) | 951 |

**Reproduction gate:** idea 228's own 12 cells re-read by this scanner match its committed
`.mechanism.csv` to **max |gap diff| 2.0e-16, max |tilt diff| 3.0e-16**, with its predictions
agreeing 12/12 and its actual re-ranks 12/12.

## 1. Idea 228's headline generalises — as a necessary condition only

| p1 | predictor | TP | FP (over-fire) | FN (miss) | TN | accuracy | precision | recall |
|---|---|---|---|---|---|---|---|---|
| STRICT | PUBLISHED `tilt > gap` | 1,651 | **681** | 2 | 6,195 | 0.9199 | 0.7080 | **0.9988** |
| STRICT | MATCHED (parameter-free) | 1,649 | **2** | 4 | 6,874 | **0.9993** | 0.9988 | 0.9976 |
| LOOSE | PUBLISHED | 1,806 | **721** | 2 | 7,219 | 0.9258 | 0.7147 | 0.9989 |
| LOOSE | MATCHED | 1,804 | **2** | 4 | 7,938 | **0.9994** | 0.9989 | 0.9978 |

Idea 228's "necessary, not sufficient" holds at 700x its evidence: recall 99.88%, but **29.2% of
its firings are false alarms** (681 of 2,332).

## 2. The queue's question, answered: there is no such ratio

Sweeping *t* over {0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2, 3, 4, 5, 7.5, 10, 20,
50, 100, 1e9} — every point in `.threshold.csv`:

* **FP > 0 at every threshold, including t = 1e9** (STRICT 15 over-fires survive there, LOOSE 17).
* Best precision anywhere on the sweep is **0.8442 at t = 4 (STRICT)** / 0.8503 (LOOSE), where
  recall has already collapsed to **0.4785** — 862 of the 1,653 real re-ranks missed.
* The classes overlap by a factor of 234: **min(ratio | re-rank) = 0.9375** vs
  **max(ratio | no re-rank) = 219.19** (LOOSE 298.53).
* AUC(ratio) = **0.9705** (LOOSE 0.9732). The ratio *ranks* well and *separates* badly — a
  reminder that a high AUC is not a threshold.

## 3. Why: it is a PAIRING error, not a magnitude error

`tilt` takes the maximum lift over all names; `gap` takes the distance to the *single*
runner-up. **In 679 of the 681 over-fires (99.7%) the max-tilt name and the min-gap name are
different names.** Pairing them per name gives the MATCHED margin
`max_d [ lift_d − (S(best,c_lo) − S(d,c_lo)) ]`, which has **6 errors in 8,529 cells, and all 6
are machine-epsilon ties** (|gap| and |tilt| both < 1e-9; 646 such tied cells exist). Outside
ties: **0 errors.** No threshold is involved, so no threshold can be tuned.

Stated plainly: MATCHED is the arithmetic the published pair approximates — under exact linearity
of Sharpe in the rung it is an identity, not a forecast. Its content as a column is therefore
*not* predictive power; it is that **the curvature the non-linear Sharpe denominator leaves
behind never flips an argmax anywhere in the record.**

## 4. Free result — two rungs are the whole ladder

The endpoint rungs alone (c_lo, c_hi) reproduce the full ladder's re-rank verdict in
**8,529 / 8,529 cells (LOOSE 9,748 / 9,748)**. 35 cells (LOOSE 41) do carry an argmax at an
interior rung that appears at neither endpoint, but never one that changes the verdict. Every
intermediate rung in every committed cost ladder is redundant for argmax stability.

## 5. PROTOCOL rule 8 — live walk-forward (gate on 2009-2016, 2017-2026 read once)

Idea 228's four dials (n, band g, vol cap, cadence k) × three panels × 7 rungs = 665 points;
cost identity |engine@10bps − (gross − turn·c/1e4)| = **6.9e-18 / 6.9e-18 / 1.4e-17**.

* IS gate: PUBLISHED **TP 4, FP 0, FN 0, TN 8** over the 12 (panel, dial) cells; MATCHED identical.
* **Trusting "gate says safe" cost exactly +0.0000 OOS Sharpe** — 0 of 56 safe cells had a moved
  IS argmax. **Half the firings were wasted work**: 14 of 28 fired rung-cells picked the 0-bps arm anyway.
* OOS Sharpe, mean over 84 cells: rung-aware **0.8248**, naive-0bps 0.7834, do-nothing 0.8071,
  random 0.7765, oracle 0.8767. Rung-aware − naive **+0.0414**; rung-aware − do-nothing **+0.0177**;
  **naive − do-nothing −0.0237** (a cost-blind chooser is worse than not choosing).
* At 10 bps (12 cells): rung-aware OOS Sharpe **0.8636**, CAGR 17.61%, MaxDD −32.40%; naive 0.8292 /
  16.69% / −31.37%; do-nothing 0.8578 / 15.15% / −28.47%. Comparands OOS: RULES v1 **0.7471** (U56) /
  0.5763 (B136) / 0.5540 (SMALL484); RULES v2 **1.2851 / 1.1185 / 0.6629**; SPY **0.8820**
  (CAGR 15.45%, MaxDD −33.72%).

## 6. KEEP paths (all 665 Part B points)

**4a 50 / 665 — U56 0 of 217** (drawdown, on every point). **4b 12 / 665, all U56**;
**B136 0 / 224 and SMALL484 0 / 224** — another reproduction of idea 136 (no 4b pass off U56).
4b failing bars
(sole + joint): DD 639, H2 404, OOS 378, H1 302, CAGR 186. These counts reproduce idea 228's
exactly, and the 12 passing U56 cells are its already-PARKed n=40 / max_vol arm, not a new book.
**No KEEP.** Full-sample bests at 10 bps: U56 V=5.0 Sharpe 1.147 (1.216/1.104), CAGR 19.07%,
MaxDD −25.37%, OOS 1.171; B136 K=4 Sharpe 1.057 (1.265/0.884); SMALL484 V=5.0 Sharpe 0.790.

## 7. Declared limitations

* PUBLISHED and MATCHED are scored **in-sample on the archive** — the "actual re-rank" label is
  read from the same rungs of the same CSV. Part B is the only out-of-sample test and it is 12 gates.
* The corpus is what the record happened to sweep: 30 dial columns over 95 files, unevenly
  weighted (one file can contribute hundreds of cells), so the cell counts are not independent
  observations and no p-value is claimed anywhere above.
* Cells with a degenerate gap (651 STRICT / 951 LOOSE, i.e. a tie at the top at c_lo) have
  ratio 0 or ∞ by construction; they are reported, not dropped, and they are where all 6 MATCHED
  errors live.
* RULES.md, scan.py, bot.py, baseline.py untouched.

## Verdict

**SPLIT — question answered, no book.** Idea 228's pair is confirmed as a necessary condition and
**killed as a leaderboard column**: no ratio threshold exists at which it stops over-firing, because
its failure is a mis-pairing, not a magnitude. The exact single-number replacement (MATCHED margin,
computable from two rungs) is offered for Sunday review as a PROTOCOL reporting clause, **not** as a
rules change.
