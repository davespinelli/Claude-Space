# Idea 737 — should PROTOCOL rule 3 state that the 4a comparand runs on the IDEA'S OWN PANEL?

lane C, 2026-09-11. Script: `2026-09-11_should-PROTOCOL-rule-3-state-that-the-4a-COMPARAND-runs-on-the-IDEA-S-OWN-PANEL_C.py`
(runtime 53 s). 10 bps, next-day execution, gross 0.75 on the book population. Two tuned
parameters — ROW SET (census tier) × CONVENTION (5 candidates) — every grid point published.

**ANSWER: YES, AND THE SENTENCE HAS TO SETTLE THREE CONVENTIONS, NOT TWO. The convention is
real but NARROW: it moves 0.76% of the committed 4a corpus, always in one direction, and NEVER
on U56. No RULES change, no book promoted, no KEEP claimed, no PROTOCOL edit applied
(rule 6 — Sunday review); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## G1 REPRODUCTION GATE — PASS (printed before any census number was read)

Idea 538's 162 cells / 324 books rebuilt from source and checked against idea 735's committed
`.grid.csv`: max |d| **9.7e-17** (CAGR) / **2.2e-16** (Sharpe, H1, H2, oSharpe) / **9.7e-17**
(MaxDD) / **3.6e-15** (turn_yr), bar 1e-9. **Both** published 4a columns reproduce **324/324** —
`p4a` (same-panel, 735's 9/324) and `p4a_538conv` (U56-reindexed, 538's 0/324). The comparand
split itself reproduces to **4.9e-05** against 735's 4-dp quotes: SMALL439 same-panel
0.5725 / −14.68% vs U56-reindexed 1.1689 / −12.05%; B136 1.1058 / −12.24% vs 1.2056 / −12.05%.

## THE COMPARAND LIBRARY (`.comparands.csv`) — the convention is a panel-strength import

| panel | SAMEv2 Sharpe / MaxDD | CROSSv2 Sharpe / MaxDD | SAMEv1 | CROSSv1 |
|---|---|---|---|---|
| U56 | 1.1998 / −12.05% | **1.1998 / −12.05% (identical)** | 0.6554 / −13.83% | **0.6554 / −13.83%** |
| B136 | 1.1058 / −12.24% | 1.2056 / −12.05% | 0.6350 / −21.19% | 0.6647 / −13.83% |
| SMALL439 | 0.5725 / −14.68% | 1.1689 / −12.05% | 0.5647 / −36.12% | 0.6477 / −13.83% |
| SMALL484 | 0.6146 / −12.09% | 1.1689 / −12.05% | 0.5230 / −44.83% | 0.6477 / −13.83% |

On U56 the two conventions are the *same object* (d = 0 exactly), so the whole question is
about the non-U56 panels. Off U56 the cross-panel form imports a large-cap book's 1.17–1.21
Sharpe as the bar a small-cap book must clear — the mechanism, stated plainly.

**A THIRD CONVENTION, NEW TO THE RECORD.** "Own panel" is itself ambiguous: `load_universe(...)`
returns SPY *inside* the frame, so `baseline.compare()` runs the comparand with SPY as an
investable name (SAMEv2), while idea 538's `panels()` drops it (SAMEv2_noSPY). The two differ
by 0.0012–0.0071 Sharpe and flip **1,079** committed rows (0.28%) — and SAMEv2_noSPY is the
convention **uniquely identified on more committed rows (9,917) than SAMEv2 (1,908)**.

## CENSUS (`.census.csv`, 1,018 blocks) — G2 coverage

3,452 committed CSVs scanned → **375 qualifying files / 433,949 rows** (a `panel` column with
≥2 panels, a 4a verdict column, and H1/H2/MaxDD). **386,109 rows (89.0%)** carry a panel label
rebuildable here (CANON); 47,336 rows sit on 3,191 labels this sandbox cannot reconstruct
(BSTK100 1,101, B80held 728, ETF36 680, …) and are counted as UNMAPPED, never guessed.

Identification is empirical — which candidate *reproduces the published pass/fail column*:
649 of 1,018 blocks (197,568 rows) are reproduced by ≥1 candidate, **117 blocks (29,774 rows)
by exactly one**. Uniquely identified rows: **CROSSv2 16,045 · SAMEv2_noSPY 9,917 · SAMEv2 1,908
· SAMEv1 1,904**. **188,541 CANON rows (48.8%) match no candidate at all** — non-standard
window, gross-matched or otherwise unrebuildable comparands: the record's 4a column is, for
about half of this corpus, not reconstructable from PROTOCOL alone. That is a finding, not a
gap in this run, and it is the honest limit on every count below.

## RESTATEMENT — B1 PASS (material), B2 PASS (one direction), B3 PASS (4b untouched)

| | rows | exposed (SAME≠CROSS) | cross-FAIL→same-PASS | cross-PASS→same-FAIL |
|---|---|---|---|---|
| ALL CANON | 386,109 | **2,949 (0.76%)** | 2,944 | 5 |
| U56 | 152,830 | **0 (0.00%)** | 0 | 0 |
| B136 | 143,985 | 1,462 (1.02%) | 1,457 | 5 |
| SMALL439 | 57,400 | 1,432 (2.49%) | 1,432 | 0 |
| SMALL484 | 31,894 | 55 (0.17%) | 55 | 0 |

The clean reading: of the **47 blocks / 16,045 rows uniquely identified as CROSS**, **889 rows
change verdict** when restated on the idea's own panel, every one of them FAIL→PASS; 70 blocks
/ 13,729 rows are already PROTOCOL-conformant. Worst-affected blocks are listed in full in the
console log (top: `does-the-record-quote-a-WINDOW-STAMP…_C.keeppaths.csv` SMALL439, 2,040 rows,
published 4a rate 0.0000 → 0.1363, 278 exposed). Same-panel is the **LOOSER** bar on every
exposed panel (+1.01% B136, +2.49% SMALL439, +0.17% SMALL484 — B2 PASS); the 5 reverse flips
all bind on the **H1 leg** (B136 same-panel H1 1.2291 > cross 1.2259), so the direction is a
tendency of the Sharpe legs, not an identity. 4b changes in **0** rows under all five
candidates (B3 PASS) — the capital-worthy path cannot be moved by this sentence.

**THE PRE-2026-09-06 RECORD IS 20× MORE EXPOSED.** The same census on the v1 pair reads
**58,529 rows (15.16%)** exposed (58,340 FAIL→PASS, 189 PASS→FAIL), because RULES v1's MaxDD is
wildly panel-dependent (−13.8% on U56 against −44.8% on SMALL484). Whatever wording is adopted,
it re-reads two orders of magnitude more of the old record than of the current one.

## RULE 8 — WF-A, 12 arms, (level, cadence) chosen on IS Sharpe 2010–2016 ALONE, 2017+ read ONCE

Picks' OOS CAGR **1.04%–24.02%**, OOS Sharpe **0.5655–1.2168**, OOS MaxDD **−3.38% to −35.07%**,
against the RULES v2 comparand OOS Sharpe **1.2747 (U56) / 1.1185 (B136, same-panel) / 0.5680
(SMALL439, same-panel)** — or **1.2747 / 1.2851 / 1.2851** under the cross-panel convention —
and SPY OOS **0.8721 / 0.8820** at 15.24% / 15.45% CAGR, −33.72% MaxDD. **Beats the comparand's
OOS Sharpe 7/12 same-panel but 0/12 cross-panel** (the convention's whole effect, out of
sample, in one line); beats SPY OOS 8/12. **4a 0/12 under BOTH conventions → B4 FAIL**: the
convention is material on the committed corpus and inert on these 12 fresh decisions, because
the DD and both-halves legs bind before the comparand choice does. 4b **1/12** —
`U56 QUANTILE x=0.50 M RESPREAD` (OOS CAGR 15.95%, OOS Sharpe 1.2164), which is one of the 16
books ideas 536/538/735 already published, reproduced, not new.

## BOTH KEEP PATHS on the 324-book audit population

4a: **SAMEv2 9/324 · SAMEv2_noSPY 9/324 · CROSSv2 0/324 · SAMEv1 72/324 · CROSSv1 48/324**.
4b: **16/324** (unchanged by the convention), all reproductions. Rule-8 leg 4a 0/12 both ways,
4b 1/12. **NO KEEP, no memo, nothing promoted.**

## PROPOSED PROTOCOL WORDING — a PROPOSAL, NOT APPLIED (rule 6, Sunday review only)

> Rule 3, appended: *"The comparand runs on the idea's own panel: `baseline.compare()` computes
> RULES v2 from the same `px` passed to the idea, SPY column included, over that panel's own
> evaluation window. A comparand computed on one panel and reindexed onto another is not a
> rule-3 comparand; a run that quotes one must label the column with the panel the comparand
> was computed on."*

The SPY clause is not decoration: without it the sentence leaves 9,917 uniquely-identified
committed rows sitting on the convention it does not name.

## CAVEATS

(i) SURVIVORSHIP (idea 54) — four current-constituent panels, no delistings, so every CAGR
LEVEL is inflated and both KEEP columns inherit it whole; the convention CONTRAST is a
comparand-minus-comparand difference on one panel and window and is largely immune. (ii) The
classifier recognises only comparands it can rebuild: 188,541 CANON rows match none and are
reported as UNIDENTIFIED, never assigned. (iii) EXPOSURE uses each row's published H1/H2/MaxDD
against the canonical-window comparand, so blocks with non-standard windows add noise to the
2,949; the 889 inside uniquely-CROSS blocks is the clean count. (iv) Five conventions over one
corpus are not independent evidence. (v) SMALL439 drops the 44 `max_1d_move >= 1.0` tickers
first, per idea 298.
