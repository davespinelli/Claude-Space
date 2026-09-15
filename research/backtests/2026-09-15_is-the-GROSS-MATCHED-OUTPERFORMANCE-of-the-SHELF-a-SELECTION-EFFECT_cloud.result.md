# Idea 873 — is the gross-matched outperformance of the shelf a selection effect?

**Cloud lane, idea 2 of 2, 2026-09-15.** Script
`2026-09-15_is-the-GROSS-MATCHED-OUTPERFORMANCE-of-the-SHELF-a-SELECTION-EFFECT_cloud.py`.
PROTOCOL: 10 bps, next-day execution, no shorting, no leverage. Rules files untouched.

## Answer — the question splits in two, and the two halves answer differently

**NO for the outperformance. YES for the shelf.** The 6-of-8 is *not* an artefact of measuring a
set in the window it was chosen on — it survives out of the selection window. But the shelf is
*not an ex-ante constructible set*: its own selection rule, run on an honest window, reaches only
**2 of its 8 books**. You could not have held the 6-of-8.

### 1. The lift survives the honest constraint (H_REAL PASS, but thinly)

Selection rule restated mechanically as the thing that put each book on the shelf — PROTOCOL 4b
(Sharpe > SPY in both halves, MaxDD ≥ 0.60 × SPY's, CAGR ≥ 0.70 × SPY's) — run on the selection
window alone, evaluated only afterwards. Headline cell (window ..2016-12-31, gross bucket NARROW
0.70–0.85, PATH comparand, 10 bps), pool 12 books:

| arm | selected beats own gxSPY | unselected, same bucket | LIFT |
|---|---|---|---|
| EX POST (the memos' information set) | 5/5 (100.0%) | 4/7 (57.1%) | **+42.9 pp** |
| EX ANTE (selection window only) | 3/3 (100.0%) | 6/9 (66.7%) | **+33.3 pp** |

H_SELECTION (lift_exante < +25 pp) **FAIL**; H_REAL **PASS** at +33.3 pp. Median evaluation-window
CAGR gap vs gxSPY: ex-ante selected **+1.94%**, unselected **+0.26%**.

**This PASS is thin and the run says so.** The ex-ante arm rests on **n_sel = 3**. At the same
cell the CONST comparand gives **+0.0 pp**. Across the 9 tuned cells the ex-ante lift is below the
25 pp bar in **5 of 9** (NARROW ..2013 +0.0, WIDE ..2013 +8.3, ALL ..2013 +15.1, WIDE ..2019 +21.3,
ALL ..2019 +23.3) and above it in 4 (NARROW ..2016 +33.3, WIDE ..2016 +30.0, ALL ..2016 +29.1,
NARROW ..2019 +42.9). The sign is positive in 9 of 9 under PATH but negative in 4 of 9 under CONST.
So: a positive lift, of the right order as the ex-post one, that is **not robust to the comparand
convention and not resolvable at these sample sizes**. All 36 grid points are published
(`.grid.csv`).

### 2. The shelf is not reachable ex ante (H_REACHABLE FAIL, 2 of 8)

| selection window | committed SHELF books clearing 4b on that window alone |
|---|---|
| ..2013-12-31 | **2 of 8** — `b136-r620-gross065-W`, `u56-quantile50-respread-M` |
| ..2016-12-31 *(headline)* | **2 of 8** — same two |
| ..2019-12-31 | **1 of 8** — `b136-r620-gross065-W` |

Bar was ≥ 5 of 8. Missed at every window: `u56-v2band-gross100`, `u56-band008-gross100`,
`u56-top20-band-m20`, `u56-marsrespread-gross075`, `b136-qroll-q012-w1008-d050-g100`,
`u56-k8-qroll-q017-w1008-d100-g100`. Six of the eight memo-backed books are objects the record's
own KEEP rule would not have produced without the post-2017 tape.

### 3. Why those two facts are not in tension

Asked of the committed shelf directly, at the ..2016-12-31 split it beats its own PATH-matched
SPY **7 of 8 on the evaluation window** (8 of 8 at ..2013, 7 of 8 at ..2019) — so the 6-of-8 is
genuinely not a re-reading of the window the memos were written on. The defect is upstream of the
measurement: the *set* only exists because someone with the whole tape wrote eight memos. Restrict
to the two books the rule could actually have found, and they go **2 of 2** — a real but
two-observation result.

## Rule 8 walk-forward

IS = ..2016-12-31, OOS = everything after. Selector = the ex-ante 4b set, tie-broken by highest
IS Sharpe, per panel. OOS read once.

| pick (IS Sharpe) | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1/H2 | gxSPY gap | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 `u56-quantile50-respread-M` (1.247) | 15.90% | 1.230 | −19.46% | 1.430 / 1.013 | **+4.43%** | FAIL | **PASS** |
| B136 `b136-r620-gross065-W` (1.254) | 14.52% | 1.040 | −19.43% | 1.116 / 0.962 | **+4.39%** | FAIL | **PASS** |
| SPY (U56) | 15.27% | 0.874 | −33.72% | 0.980 / 0.759 | — | — | — |
| RULES v2 live (U56) | 9.49% | 1.286 | −11.90% | 1.421 / 1.138 | — | — | — |

SMALL panel: **the ex-ante rule selects no book at all** — nothing to read.

H_WF: 4b **PASS**, 4a **FAIL** (both picks sit below the live book's Sharpe in at least one half
and draw down far deeper). The U56 pick reproduces lane B's committed OOS triple for the same book
to the printed digit (15.90% / 1.230 / −19.46%).

## Verdict

**KILL for capital — nothing new is promoted.** The two books the ex-ante rule reaches are
*already* on the shelf with committed memos, so this run adds no KEEP candidate and writes no new
memo; it re-derives them from a pre-registered IS-only selection, which is worth having as
confirmation and is not a new claim. No PROTOCOL edit is proposed or applied (rule 6). RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

**What the record should stop saying:** that the shelf's 6-of-8 gross-matched win rate is evidence
the shelf's *selection* works. The win rate is real out of window; the selection is not
reproducible — **2 of 8**. Any future citation of the 6-of-8 should carry the 2-of-8 beside it.

## Gates (printed before any new number was read)

- **G1** all **8 of 8** SHELF books reproduce their committed memo triples (worst |dCAGR| 0.0030,
  |dSharpe| 0.0102) — PASS
- **G2** gxSPY at constant g = 1.00 == SPY, max|d| **0.000e+00** — PASS
- **G3** PATH comparand's realised mean gross == the book's own, max|d| **0.000e+00** — PASS
- **G4** fast metrics == `engine.metrics()`, |d| **0.000e+00** — PASS
- **G5 CROSS-RUN** idea 868's published full-sample counts rebuilt from this run's own arms:
  SHELF **6/8**, same-bucket GRID **3/12**, whole ladder **16/54** — all three exact — PASS
  (868's ex-post lift: 75.0% − 25.0% = +50.0 pp)

62 books (8 SHELF + 54 GRID, imported from the same committed builders 868 used) × 2 rungs ×
3 windows × 2 comparands; runtime 458 s.

**SURVIVORSHIP:** U56 / B136 / SMALL are current-constituent lists; the small panel additionally
drops every ticker with `max_1d_move >= 1.0` per `data/small_meta.csv`. Every CAGR, Sharpe and
MaxDD *level* above is optimistic — for the books and for the comparands alike — which is why the
reported quantity is a difference of two beat-rates. The rule-8 table reads levels and is exposed
in full.
