# Idea 824 — re-price the record's MATCHED-GROSS TWIN claims under WINMATCH (lane C, 2026-09-12)

**ANSWER: ON THE RECORD'S OWN VERDICT COLUMN (Sharpe), ZERO OF 432 OOS TWIN CLAIMS CHANGE SIGN —
AND EVERY FLIP THE CONVENTION DOES PRODUCE ANYWHERE IS AN ARM WHOSE GATE NEVER FIRED IN THE
WINDOW.** 714 of the 717 sign changes over every window × scope × rung in this run are NEVERFIRE
arms, for which WINMATCH makes the twin *literally the arm itself* (dSharpe identically 0, scored a
LOSS by the record's strict `win = dSharpe > 0`), while FULLMATCH hands the same arm a twin at a
different gross and returns a win by ≤ 1.31e-03 of Sharpe. **The record's twin wins on sub-windows
are not re-ranked by the matching sample; a class of them is revealed to be exact ties.**

Script: `2026-09-12_re-price-the-record-s-MATCHED-GROSS-TWIN-claims-under-WINMATCH_C.py`
(`.console.txt`, `.grid.csv`, `.claims.csv.gz`, `.decomp.csv`, `.rolling.csv`, `.premise.csv`,
`.walkforward.csv`). No RULES, PROTOCOL, scan.py, bot.py or baseline.py change. **Verdict: KILL for
capital** — no new book is proposed and none is promoted; the run is a correction to how the record
reads a comparand, plus one confirmation (below) of the candidate the record already holds.

## Gates (all read before any answer)
| gate | result |
|---|---|
| G1 `fast_run` == `engine.backtest` | max\|d\| **1.04e-17** PASS |
| G2 fast CAGR/Sharpe/MaxDD == `engine.metrics` | **0.00e+00** PASS |
| G3 0.01-gross-grid interpolation vs an EXACT twin run | \|dSharpe\| **2.01e-08** PASS |
| G4a U56 rebuilds the committed twin cells (dSharpe, win, twin_OOS) | **PASS**, max\|d\| 1.9e-03, **0 win flips** |
| G4b B136 | dSharpe 3.05e-03 PASS-side, **twin_OOS LEVEL 8.1e-03 FAILS the declared 6e-03 bar** — reported, not relaxed (idea 406 drift) |
| G4c SMALL439 | **FAIL — the panel no longer exists.** Committed rows are 439 tradable names; today's `data/prices_small.csv.gz` is 715 columns, 52 dropped, **663 tradable**. Idea 609's finding reproduced exactly. Today's SMALL is run as its own scope, never pooled into the headline. |
| G5 / H_ID WINMATCH ≡ FULLMATCH on the FULL window | max\|d dSharpe\| **0.00e+00** PASS |

Headline scope **REPRO2 = U56 + B136**, fixed by the gate before any answer was read.

## The grid — 6 claim windows × 2 conventions, every point printed (`.grid.csv`)
REPRO2, Sharpe verdicts, n = 432 per cell:

| window | rung | win FULLMATCH | win WINMATCH | flips | W→L | L→W | med \|Δ dSharpe\| |
|---|---|---|---|---|---|---|---|
| FULL (committed) | 0/10/25 | 0.8750 / 0.8565 / 0.7523 | identical | **0 / 0 / 0** | 0 | 0 | 0.0000 |
| IS (committed) | 0/10/25 | 0.4398 / 0.5000 / 0.4190 | 0.3426 / 0.2917 / 0.2106 | **42 / 90 / 90** | all | 0 | ≤ 0.0001 |
| OOS (committed) | 0/10/25 | 0.9398 / 0.9306 / 0.8935 | identical | **0 / 0 / 0** | 0 | 0 | 0.0000 |
| H1 (extension) | 0/10/25 | 0.4977 / 0.5463 / 0.4583 | 0.4005 / 0.3380 / 0.2500 | 42 / 90 / 90 | all | 0 | ≤ 0.0001 |
| H2 (extension) | 0/10/25 | 0.9213 / 0.9028 / 0.8588 | identical | 0 / 0 / 0 | 0 | 0 | ≤ 0.0001 |
| EP2022 (extension) | 0/10/25 | 0.1806 / 0.1250 / 0.0602 | identical | 0 / 0 / 0 | 0 | 0 | ≤ 0.0014 |

**Counted over the record's three COMMITTED twin windows × 3 rungs on REPRO2: 222 of 3,888 Sharpe
verdicts change sign (0.0571); over the sub-windows alone — IS and OOS, the only committed twin
claims a matching convention can move — 222 of 2,592 (0.0856).** On the FULL sample the two
conventions are the same object, so no full-sample twin claim in the record can move, and none does.

## Why, and it is not a summary statistic (`.decomp.csv`)
* **714 of 717 flips, everywhere in this run, are NEVERFIRE arms.** On the rolling census the same
  reading: **99.2% of IS-window flips and 88.6% of OOS-window flips** are arms whose gate never
  fires inside the window.
* **The largest \|dSharpe\| the FULLMATCH convention ever assigns to a flipped claim is 1.31e-03.**
* The reason nothing else moves: **a static long-only book's SHARPE is near-invariant to its gross.**
  On the 2022 episode the full-matched twin carries **20.1 pp more gross** than the arm actually held
  (Δg_eff −0.2008) and the twin's Sharpe moves by a median **6.2e-04** — zero verdicts flip.
  H_PREMISE is therefore **UNDECIDABLE on the data**: no arm on any panel has its two OOS twins
  separated by more than SEP = 1e-02 of Sharpe, so the committed column cannot be told apart by
  its values; the FULLMATCH construction is read off the 2026-09-10 script's source instead
  (`g_eff = g * mean(m)` computed once on the full sample, then sliced — lines 359-361).
* **This retro-explains idea 609's "biggest axis".** 609 read share_exact 0.322 → 0.102 and called
  the twin's matching sample larger than cost, window, step or panel. It is larger — as a count of
  strict inequalities. No Sharpe moved: never-firing arms became exact ties and a `>` test scored
  them as losses.

## The leg that is NOT free: CAGR
`dCAGR` scales with gross where Sharpe does not, so the convention is real on the record's CAGR
column: **OOS 32 of 432 sign changes at 10 bps (median \|Δ dCAGR\| 1.13e-03, i.e. 0.11 pp), IS 158
of 432** — and **none of the OOS CAGR flips are NEVERFIRE arms**; they are genuine arms whose margin
sits within 0.36 pp of zero. MaxDD: 10 of 432 OOS. A twin claim quoted on CAGR or MaxDD over a
sub-window needs its matching sample stated; a twin claim quoted on Sharpe does not.

## PROTOCOL rule 8 — run on the claim AND on the books
* **On the claim (read once):** rolling 756-day windows stepped 63 days; flip share on windows
  ending in the IS half **0.3686 → 0.0278** on windows ending in the OOS half, **\|Δ\| 0.3408 —
  H_R8CLAIM FAILS.** The convention sensitivity is an IS-window fact, and the decomposition says why:
  42.95% of arms never fire inside a 3-year IS window against 8.88% inside an OOS one.
* **On the books:** 648 arms × 3 rungs, dial chosen on IS by IS Sharpe alone, OOS read once.
  **4a: 3 of 648 at 0 bps, 0 of 648 at 10 and at 25.** 4b: 305 / 141 / 44 of 648. Rule-8 picks:
  **68 of 324 pass 4b, 3 of 324 pass 4a.** Comparands on the same OOS window: SPY
  **15.33% / 0.877 / −33.72%**; RULES v2 **9.47% / 1.278 / −12.05%** (U56), **7.88% / 1.106 /
  −12.24%** (B136), **3.75% / 0.560 / −13.89%** (SMALL). Median rule-8 pick OOS at 10 bps: U56
  12.35% / 1.157 / −18.01%, B136 11.01% / 1.021 / −17.69%, SMALL 3.98% / 0.353 / −34.39%.
  **0 of the 68 4b picks has its own twin verdict flipped by the convention.**

## H_CAND — the record's newest 4b KEEP-candidate survives the re-match
B136 breadth-QROLL q0.17 w252 depth 0.50 DAILY g1.00 (idea 609's by-product), 10 bps:
FULL 13.29% / 1.1336 / −15.19%, twin 1.0212 under **both** conventions; OOS 13.33% / 1.1897 /
−15.19%, dSharpe **+0.1798 FULLMATCH, +0.1798 WINMATCH** (g_eff 0.8908 → 0.8715). It beats its own
window-matched twin on FULL and OOS at 0, 10 and 25 bps — **H_CAND PASS**. Two caveats this run adds
to it: its IS dCAGR **changes sign** under the re-match (+0.33 pp → −0.01 pp) and its 2022 CAGR edge
shrinks from +3.44 pp to +0.75 pp, so the candidate's *return* edge on sub-windows is convention-
dependent even though its *Sharpe* edge is not. It is still not proposed here.

## Hypotheses
| | verdict | evidence |
|---|---|---|
| H_ID | PASS | 0.00e+00 on FULL |
| H_PREMISE | **UNDECIDABLE** | no arm's two OOS twins separated by > 1e-02 of Sharpe |
| H_FLIP | **PASS** | 0 of 432 at OOS / REPRO2 / 10 bps |
| H_SYM | FAIL (vacuous at the headline) | where flips exist they are **one-directional: 444 W→L, 0 L→W** on REPRO2 |
| H_MAG | PASS | median \|Δ dSharpe\| 0.0000, max 0.0003 |
| H_COSTINV | PASS | flip 0.0000 / 0.0000 / 0.0000 at 0 / 10 / 25 bps |
| H_PANELINV | PASS | U56 0.0000, B136 0.0000, SMALL 0.0000 |
| H_WINDOW | **FAIL** | IS 0.2083 vs OOS 0.0000 |
| H_CAND | PASS | beats its WINMATCH twin on FULL and OOS at every rung |
| H_R8CLAIM | **FAIL** | IS 0.3686 → OOS 0.0278, \|Δ\| 0.3408 |

## What should change (proposed for the Sunday review, not applied here)
1. A twin/matched-gross claim read on a SUB-WINDOW must state its matching sample. On Sharpe it
   does not matter; on CAGR and MaxDD it does, and the record does not currently distinguish.
2. **`win = dSharpe > 0` must not score an exact tie as a win.** 714 of 717 flips in this run exist
   only because a never-firing arm's FULLMATCH twin is a different book by construction. A twin
   comparison on a window where the gate never fires is not evidence about the gate; it should be
   reported as N/A, not as a win.

**SURVIVORSHIP:** all three panels are current-constituent lists (`data/SMALL_PANEL_README.md`);
every LEVEL here is optimistic and SMALL worst. A flip SHARE is a within-panel agreement rate and is
far less exposed. Nothing in this run is a capital claim.
