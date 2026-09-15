# Idea 679 (cloud lane, 2026-09-15) — is-the-4a-MaxDD-leg-passable-at-all-without-de-grossing

**ANSWERED, and the queue's framing needs one correction. At the record's own gross rung the answer
is NO — 0 of 151 committed 4a passers survive at matched gross, the DD leg failing in 100% of them.
But 4a's DD leg is not unpassable; it is a GROSS THRESHOLD. Below ~0.50 gross on B136, matched-gross
4a passes exist (83 of 4,320 draw-books). VERDICT: KILL for capital — no book promoted — with a
PROTOCOL wording PROPOSED under rule 6 and NOT applied.**
RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script `..._cloud.py`; console `..._cloud.console.txt`;
data `..._cloud.{census,survivors,arms,draws,walkforward,hypotheses}.csv[.gz]`.

## Gates
| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` (B136, n=20, g=0.75, MATCH) | max\|d\| **1.388e-17** PASS |
| G2 503's committed grid loads at its published shape (6000 × 172); NOM gross ≤ MATCH gross at every n | PASS |
| G3 / H_REPRO re-derived 4a off the committed grid | **NOM 151 vs 503's published 145; MATCH 0 vs 0** — **DIFFERS** |
| G4 determinism (a LEG-2 cell recomputed) | \|dSharpe\| **0.000e+00** PASS |
| G5 live RULES v2 comparand printed on each panel before any arm was scored | PASS |

**G3 is a partial miss and is reported as one.** The MATCH count reproduces exactly (0 = 0); the NOM
count is **151 here against 503's published 145**. The cause is the comparand, not the books: this
run recomputes the RULES v2 4a bars off today's price cache (B136 halves 1.2348 / 0.9658, MaxDD
-12.24%), and 503 ran on a cache four days older. Six borderline draws cross the bar. Every number
below is therefore **this run's own re-derivation**, and the queue's test is unaffected — the
survivor count is 0 under either denominator.

## LEG 1 — the queue's own test, on 503's committed 72,000 book-rows (zero new backtests)
**Committed NOM 4a passers: 151. Surviving with gross held at nominal: 0 (0.0%). H_SURVIVE PASS.**

| what kills them at matched gross | count |
|---|---|
| DD alone | 63 |
| H2 + DD | 47 |
| H1 + DD | 23 |
| H1 + H2 + DD | 18 |

**The DD leg is among the failures in 151 of 151 = 100.0%** (H_DDLEG PASS). The passers are all
B136 sub-panels (111 at k=20, 40 at k=40; **none at k=80**, where more names are eligible and the
form de-grosses less), and all sit at n ≥ 15 — 83 of them at n=40.

What the pass costs, median over the 151:

| | NOM (as published) | MATCH (same book, gross at nominal) |
|---|---|---|
| realised gross | **0.3471** (46.3% of the 0.75 nominal) | 0.7484 |
| MaxDD | **-8.73%** | -18.96% |
| Sharpe | 1.1696 | 1.1322 |
| **CAGR** | **6.14%** | **12.93%** |

The 4a DD bar is -12.24% (B136) / -12.18% (SMALL484). **The pass is bought with return: the passing
form earns 6.14%/yr where the same names at nominal gross earn 12.93%.**

## LEG 2 — the gross-rung sweep, full panels (216 arms: 2 panels × 6 rungs × 6 n × 3 forms)
**4a passes: 0 of 216.** Not one full-panel CAND-n book clears 4a at any rung in any form.
The DD leg alone is a clean step function of gross, and **the step is in the identical place in all
three forms**:

| panel | DD leg passes at gross | fails at gross |
|---|---|---|
| B136 | 0.10, 0.25, 0.40 | **0.50**, 0.75, 1.00 |
| SMALL663 | 0.10, 0.25 | **0.40**, 0.50, 0.75, 1.00 |

NOM, MATCH and BLEND break at the same rung on each panel — the DD leg does not care how the
exposure is reached, only what it is. **H_RUNG PASS** (0 MATCH-form 4a passes at g ≥ 0.50).

4b passes exactly **one** cell (B136, g=0.75, n=40) in each form — e.g. MATCH 11.99% / 0.9868 /
-19.11% (its NOM twin 11.87% / 0.9995 / -19.11%) — and that same cell fails 4a on **all three legs** (H1, H2, DD). **H_4B_SPLIT PASS**: the
two KEEP paths disagree precisely at the rung the live book runs.

## LEG 3 — the sub-panel draw population, 25,920 books (120 draws of k=40 per panel, seed 679)
This leg exists because LEG 2 cannot test the cash blend: on a full panel n_elig ≥ n almost always,
so NOM barely de-grosses and no NOM 4a cell exists. The record's passers are k-name draws.

**This leg corrects the queue's premise.** Matched-gross 4a passes DO exist:

| panel / form | 4a passes at g = 0.10 / 0.25 / 0.40 / 0.50 / 0.75 / 1.00 (of 720 each) |
|---|---|
| B136 NOM | 34 / 34 / 33 / 29 / 8 / 0 |
| **B136 MATCH** | **23 / 24 / 24 / 12 / 0 / 0** |
| B136 BLEND | 23 / 24 / 24 / 22 / 5 / 0 |
| SMALL663 NOM | 5 / 5 / 5 / 3 / 2 / 1 |
| **SMALL663 MATCH** | **0 / 0 / 0 / 0 / 0 / 0** |

**83 matched-gross 4a passes on B136**, all at g ≤ 0.50, none at 0.75 or 1.00. So the correct
statement is not "4a's DD leg is unpassable at matched gross" but **"4a's DD leg is a gross
threshold at roughly 0.40–0.50 on B136 and below 0.25 on SMALL663, and the record's single rung
(0.75) sits above it."** That is why 503 saw 0 of 36,000. DD-leg pass *rates* show the threshold
directly — B136 MATCH: 1.000 / 0.996 / 0.656 / 0.143 / 0.000 / 0.000.

### The cash-blend control — H_BLEND FAILS, and that is a finding
Of the **159** draw-books where the de-grossing NOM arm clears 4a:
- the **static cash blend** at the same realised mean exposure clears it at **58 / 159 = 36.5%**
- the **matched-gross** arm clears it at **51 / 159 = 32.1%**

**The de-grossing is therefore NOT a pure exposure dial.** Holding the same average exposure
statically reproduces only 4.4pp more of the passes than holding full gross does; roughly **63% of
the NOM passes survive neither control**. The `w = GROSS/n` form de-grosses exactly when fewer names
are eligible — i.e. it is an eligibility-count market-state timer, not just a smaller book. The run
pre-registered the opposite expectation and it is recorded as failed.

## Rule 8 walk-forward — the rung chosen on 2009–2016 alone, 2017–2026 read once
72 picks (2 panels × 3 forms × 6 n × 2 choosers). C1 (argmax IS Sharpe) picks **g = 1.00** every
time; C2 (smallest rung with IS MaxDD ≤ 60% of SPY's) picks **g = 0.10** every time.

| panel | OOS comparands (2017-01-01 → 2026-09-11) |
|---|---|
| B136 | RULES v2 **7.88% / 1.1059 / -12.24%**; SPY **15.33% / 0.8767 / -33.72%** |
| SMALL663 | RULES v2 **3.75% / 0.5600 / -13.89%**; SPY **15.33% / 0.8767 / -33.72%** |

**OOS 4a: 0 of 72. OOS 4b: 0 of 72.** H_WF PASS. Neither chooser lands on a book that clears either
path out of sample on a full panel — the C1 end is too levered for the DD leg, the C2 end too small
for the CAGR leg.

## Hypothesis table
| H_REPRO | H_SURVIVE | H_DDLEG | H_RUNG | H_BLEND | H_4B_SPLIT | H_WF |
|---|---|---|---|---|---|---|
| **FAIL** (151 vs 145; MATCH 0 = 0) | PASS | PASS | PASS | **FAIL** | PASS | PASS |

## Verdict and what should change
**KILL for capital.** No book is promoted; this is a path-definition result. The script's
pre-registered verdict rule (H_SURVIVE ∧ H_RUNG) returns "ANSWERED-NO"; **that wording is too strong
given LEG 3 and is corrected here**: the DD leg is passable at matched gross, but only below a gross
threshold the record has never published, and never at the rung the record actually uses.

**PROPOSED PROTOCOL WORDING (rule 6 — NOT applied):** PROTOCOL 4a, drawdown leg — "MaxDD no worse
than the live rules" must be quoted beside the arm's **realised mean gross** and beside the live
rules' own. A 4a pass whose arm holds materially less than the comparand is an **exposure pass** and
must be labelled one; the matched-gross reading of the same book is to be published beside it. On
the record as it stands this relabels **151 of 151** committed 4a passes.

**SURVIVORSHIP (rule 9):** B136 is `universe_broad.json`'s current constituents; SMALL663 is the
current sub-$2B screen with the 52 `max_1d_move ≥ 1.0` tickers dropped first (715 → 663 names).
Both are survivor lists, so every MaxDD level here is understated and the 4a DD leg is **easier**
than it would be on a point-in-time panel — the negative findings are conservative, and the
matched-gross passes found in LEG 3 are, if anything, optimistic.
