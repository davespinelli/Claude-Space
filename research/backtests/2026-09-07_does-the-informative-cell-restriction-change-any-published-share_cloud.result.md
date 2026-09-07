# Idea 393 — does the informative-cell restriction change any published share?

**2026-09-07, cloud.  Verdict: ANSWERED — YES, it changes them, and TWO published readings
REVERSE — but the census's own headline is a COVERAGE DEFECT: 131 of 191 in-scope shares
(68.6%) cannot be checked at all.  Rules unchanged; no new KEEP (4a 0/54 at both cost
rungs; 4b 11/54 @10 bps, 0/54 @25, and every one of the 11 is an overlay on the NF20 twin
of the record's already-standing 2026-09-04 4b row).**

Script `2026-09-07_does-the-informative-cell-restriction-change-any-published-share_cloud.py`;
artefacts `.degeneracy.csv` (196 predicates), `.census.csv` (191 in-scope shares),
`.grid.csv` (54 live cells), `.walkforward.csv` (36 rows), `.console.txt`.

## Definitions, fixed before anything was read

* **DEGENERATE CELL** (c\* predicate) := every c\* value entering the predicate is `0.0`,
  i.e. every side already fails at zero cost.  This is idea 335's own definition, verbatim.
* **DEGENERATE CELL** (fail-bar tally) := a cell with **no failing bar** (a pass) inside
  the denominator.  A genuine failure at zero cost is *not* degenerate — it is the thing
  being counted.
* **Degeneracy is per-PREDICATE, not per-file.**  Over idea 335's twelve c\* columns, 50 of
  90 rows are zero everywhere, but its published 4b/full share's own denominator loses
  **51**.  A per-file count would have got the anchor wrong.
* **In scope** = CSTAR-PREDICATE + CSTAR-OTHER + FAILBAR.  **KEEP-PASS** shares ("4b
  16/180") and **GATE** shares ("max|diff| = 3.6e-15 on 42/42 rows") are the controls:
  a KEEP-pass denominator is the whole grid *by design*, and a gate is a claim about
  arithmetic, not about cells.  Counting either would have inflated the census.

## Gates (all printed in [0] before any new number)

| gate | what | result |
|---|---|---|
| G1 | `fast_bt` == `engine.backtest` on returns **and** turnover at 0 and 25 bps | `0.000e+00` |
| G2 | book-level overlay at OFF (`m == 1`) == the parent | `0.000e+00` |
| G3 | Sharpe invariance of the gross dial, a ∈ {0.25..1.00} × c ∈ {0,10,25} | `2.220e-16` |
| G4 | the standing 2026-09-04 KEEP-4b row (`46 N n=20`; published 12.7% / 1.09 / -18.3%, halves 1.09/1.10) at fixed n=20 | **12.66% / 1.092 / -18.31% (1.09/1.10) — EXACT** |
| G5 | **load-bearing.** An independent rebuild of idea 335's **54 book-level cells** reproduces its committed `.grid.csv` on **all twelve** c\* columns | **`3.553e-15`** |
| G6 | the restriction reproduces idea 335's published shares on all three windows | full 80/90→51→39→29/39→10 **EXACT**; IS 87/90→77→13→10/13→3 **EXACT**; OOS 73/90→51→39→22/39→17 **EXACT** |

G5 is what licenses the audit: the census's arithmetic **is** the record's arithmetic, so
a restatement is a correction and not a second opinion.  The 36 per-name cells of idea
335's grid (MABAND, STOP) are excluded from G5 **by name, not by outcome** — they are not
rebuilt here.

**G6 by-product — the record's own share is tie-sensitive at one cell.**  The published
OOS 73/90 needs a `1e-9` tie tolerance: `U56 g0=0.75 VOLCAP 0.25` has `c*_ov − c*_ct =
1.4e-14`, and a strict `<=` reads it as a violation, moving 73/90 → 72/90 and 22/39 →
21/39.  A c\* equality that survives only inside float noise is not an equality anybody
can trade.

## [B] The degeneracy map — 64 CSVs, 196 predicates

| group kind | predicates | cells | degenerate | with ANY degenerate cell | **WHOLLY degenerate** |
|---|---|---|---|---|---|
| PAIRED (an inequality's two sides) | 28 | 2280 | 1644 (**72.1%**) | 26/28 | **12** |
| SINGLE (one c\* column) | 132 | 11895 | 4714 (39.6%) | 94/132 | **30** |
| FAILBAR | 36 | 5607 | 1513 (27.0%) | 12/36 | **1** |

**43 of the record's 196 c\*/fail-bar predicates are wholly degenerate** — every cell
`0 ≤ 0`, so any share published over them is empty of content by construction.  Idea 335
said this about its own 4a column and stopped there; the same restriction finds **40 more
such predicates elsewhere in the record**, chiefly the 4a columns of ideas 335 and 394,
which are silent for the same reason: no arm in either grid beats RULES v2 at zero cost.

## [C] The restatement table — every checkable share whose denominator loses cells

| source | predicate (recovered) | published | restated | move |
|---|---|---|---|---|
| idea 335 `.result.md`:47 | `cstar_ov_4a_full <= cstar_ct_4a_full` | 90/90 | **EMPTY** (0 informative) | the share carries nothing |
| CHANGELOG:3 (idea 335) | `cstar_ov_4b_full <= cstar_ct_4b_full` | 80/90 (88.9%) | **29/39 (74.4%)** | −14.5 pp |
| CHANGELOG:3 (idea 335) | `cstar_ov_4b_oos <= cstar_ct_4b_oos` | 73/90 (81.1%) | **22/39 (56.4%)** | −24.7 pp |
| QUEUE:115 (idea 335 parents) | `cstar4b >= 10` | 1/6 (16.7%) | **1/2 (50.0%)** | +33.3 pp |
| CHANGELOG:12 (idea 356) | `cstar_full >= 20` | 9/42 (21.4%) | **9/14 (64.3%)** | **+42.9 pp — CROSSES 50%** |
| QUEUE:152 (idea 356) | `cstar_full < 20` | 33/42 (78.6%) | **5/14 (35.7%)** | **−42.9 pp — CROSSES 50%** |
| CHANGELOG:12 (idea 356) | `cstar_full == 0` | 28/42 (66.7%) | 0/14 (0.0%) | **TAUTOLOGICAL** — the predicate *is* the degeneracy definition |
| CHANGELOG:3 (idea 335 walkforward) | not recovered | 13/60 | ?/23 | denominator loses 37 |

**The consequential pair is idea 356's.**  The record's reading — *"most priced books have
a cost budget below 20 bps"* (33 of 42, 78.6%) — is a statement about 42 cells of which
**28 have `c* = 0`**, i.e. books that fail 4b before a single basis point of cost is
charged.  Those cells are below 20 bps for a reason that has nothing to do with cost.
Restricted to the 14 books that survive at zero cost, the share is **5/14 (35.7%)**: a
**minority**, and its complement — *a 20-bps budget or better* — goes from 21.4% to
**64.3%**.  The published sign of the majority claim is an artefact of the denominator.

Predicates were recovered by matching the published numerator against a **fixed library of
~40 predicates**, declared before any share was read and identical for every share, so a
recovery is a match and not a fit; every recovered predicate is printed with its source
line so it can be checked by hand.

## [A] Coverage — the census's real headline

12 682 k/N shares in 395 committed files.  By nearest governing token: OTHER 8378,
KEEP-PASS 3572, GATE 541, CSTAR-OTHER 72, FAILBAR 68, CSTAR-PREDICATE 51.
**191 in scope**, in 26 files, 158 of them re-quotes in CHANGELOG/QUEUE/LEADERBOARD.

| tier | what is recoverable | n | share |
|---|---|---|---|
| **R1 RESTATABLE** | a sibling CSV carries the predicate's own columns AND the denominator matches | **11** | 5.8% |
| R2 CSV-BACKED | such a CSV exists but no denominator matches | 49 | 25.7% |
| R0 NO-CSV | the parent committed no c\* column | 45 | 23.6% |
| R0 UNATTRIBUTED | a digest re-quote whose owning idea cannot be read off the entry | 86 | 45.0% |

**8 of the 11 checkable shares (72.7%) sit on a degenerate denominator, and 1 is wholly
degenerate.**  If that rate held over the 131 unauditable shares the record would be
carrying roughly 95 mis-stated c\* shares — but it cannot be checked, and this run does
not claim it.  What it does claim is the direction: **every share the record CAN check
turned out to need checking.**  This is idea 378's finding in a second column: the record
quotes over cell sets it does not commit.

**Proposed amendment (same shape as idea 378's):** any published k/N over c\*, breakeven or
fail-bar cells must carry its **informative-cell count** beside it, and its parent must
commit the c\* column it was computed over.  Both are one column each; without them the
restriction is unapplicable, which is what 68.6% above measures.

## [D] Live re-pricing and rule 8 — the audit is anchored to real backtests

54 cells (3 book-level families × 3 dials × 3 gross rungs × 2 panels), 10 bps and 25 bps.
U56 SPY 15.23% / 0.889 (H1 0.957 / H2 0.834 / OOS 0.882) / −33.72%; RULES v2 @10 bps
8.66% / 1.206 / −12.05% (OOS 9.53% / 1.285 / −12.05%).

| rung | 4a | 4b |
|---|---|---|
| @10 bps | **0/54** | **11/54** |
| @25 bps | **0/54** | **0/54** |

First failing 4b bar over the 43 failures @10 bps: H2 24, CAGR 23, OOS 19, DD 12, H1 5.

**Rule 8 walk-forward** (dial chosen on 2008–2016 only, by IS c\*_4b and separately by IS
Sharpe@10 — the record's convention; 2017–2026 read once, 36 rows):

| panel | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|
| U56 | 13.28% | 1.145 | −15.69% | 9.53% / **1.285** / −12.05% | 15.45% / 0.882 / −33.72% |
| B136 | 10.98% | 0.860 | −17.97% | 7.98% / **1.119** / −12.24% | 15.45% / 0.882 / −33.72% |

Every walk-forward arm loses to RULES v2 on OOS Sharpe on both panels, and B136's mean
arm loses to SPY as well.  Consistent with idea 335 and idea 392: the 11 4b passes @10 bps
are overlays on the NF20 twin of the standing 2026-09-04 candidate, none of them a new
book, and all of them gone at 25 bps.  **No KEEP; no rules change.**

## Caveats

1. `universe.json` (56) and `universe_broad.json` (136) are **current-constituent** lists —
   **survivorship**; absolute CAGRs are optimistic on both, and B136 *contains* U56, so two
   panels is not two independent samples.
2. The census restates only what a parent committed.  R0 shares are **counted, not fixed**,
   and that count is the result — not an estimate of how many are wrong.
3. Denominators are matched **by value** (N == rows in a cell set).  A coincidental match is
   possible; every match is printed with its source line so it can be checked by hand, and
   gate-language shares are excluded by their own wording before matching.
4. c\* is a breakeven, not a return.  A book with a high c\* and a bad level is still a bad
   book, and [D] reports the levels beside it.
