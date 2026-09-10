# Idea 594 — census the record for MaxDD comparisons that are EXACT TIES

**Cloud lane, 2026-09-10. Verdict: SPLIT — the CENSUS is DELIVERED and it RELOCATES the problem.** Ties are real and large *in aggregate* (196 489 of 924 699 published MaxDD/Calmar comparison cells, **21.25%**, at |Δ| < 1e-12) but they are **not spread through the record**: **58.7% of the 477 artefacts that carry a comparison have ZERO ties**, the **median per-file tie share is 0.0000%**, and **10 draw/bootstrap artefacts carry 69.1% of all ties**. Idea 592's two halves are both right and this run supplies the missing middle: the tie problem is a property of **enumerated draw populations**, not of the record's book-vs-book comparisons. Exposure is measured from the source: of **1 104** committed MaxDD/Calmar comparison sites, a tie is a **PASS at 815 (73.8%)**, a **FAIL at 261 (23.6%)** and a **FLIP at 18 (1.6%, 9 files)** — the np.sign channel idea 592 named is the *rarest* convention in the record, and PROTOCOL's own two legs (`>=` on 4a, `<=` on 4b's DD cap) are in the PASS majority. No RULES change, no book promoted; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script: `research/backtests/2026-09-10_census-the-record-for-MaxDD-comparisons-that-are-EXACT-TIES_cloud.py`
Data: `.census.csv` (1 212 comparison groups), `.sites.csv` (1 104 source sites), `.population.csv` (990 rows), `.population_restated.csv`, `.walkforward.csv` (54), `.console.txt`.

## Design

Two tuned parameters, as the queue allows, **every value reported**: metric set {MAXDD} / {MAXDD, CALMAR}; tie bar {1e-12, 1e-9, 1e-6, 1e-4, 1e-3} (1e-12 = the queue's, and the headline). Three readings, kept apart because they answer different questions: **A** published DELTA columns (`dMaxDD`, `d_OOS_MaxDD`, `dMaxDD@25`…), **B** published arm-vs-control LEVEL PAIRS in the same row (two columns differing only by a book-role token; window tokens IS/OOS/H1/H2 are *not* roles, so `IS_MaxDD` vs `OOS_MaxDD` is never counted), **C** an AST walk over 541 committed scripts for every `Compare` / `np.sign` site naming MaxDD or Calmar. A and B are **upper bounds** in ideas 276/286/523's sense: a column pair is a *name*, not proof a human quoted it.

**Gates, all PASS, printed before any result was read.** G1 derived cost rung vs live `engine.backtest(25)` **0.000e+00**. G2 idea 84's ungated EWALL U56 g=0.85 @10 bps 11.755% / 1.046 / −17.894% / H 1.07 / 1.03 vs committed 11.8% / 1.05 / −17.9% / 1.07 / 1.04. G3 local `maxdd()` vs `engine.metrics()['MaxDD']` **0.000e+00**. G4 the census machinery on a *planted* artefact with a known answer (1 pair found, IS/OOS not paired, `flip_` column excluded, 1 tie @1e-12 and 2 @1e-9, 2 delta ties).

## Q1 — the census, and the weighting that changes what it means

| reading | groups | files | cells | ties @1e-12 | share |
|---|---|---|---|---|---|
| A published delta columns | 328 | 189 | 636 189 | 155 975 | **24.52%** |
| B published arm-vs-control pairs | 881 | 335 | 288 438 | 40 514 | **14.05%** |
| both | 1 212 | 477 | 924 699 | 196 489 | **21.25%** |

The bar barely matters: 1e-12 → 1e-3 moves the share only 21.25% → 22.57%, i.e. **ties in this record are EXACT, not near-misses** — a scale-free result the queue's choice of 1e-12 did not have to be right about. Adding Calmar to the metric set moves nothing (Calmar columns are 3 of 1 212 groups — the record almost never publishes a Calmar comparison). **But the cell-weighted share is not the record's tie rate**: file-weighted it is **7.83%**, the median artefact's is **0.00%**, 280 of 477 artefacts have no tie at all, and the ten heaviest — `is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B2` (72.7% of 40 773), `is-the-EMPTY-POOL-RATE…_B` (41.2%), `clause-11b-draw-count-by-enumeration_cloud` (57.5%), the three `book-size-floor-for-any-quoted-price` bootstraps, `re-state-every-IS-DRAWDOWN-BAR…` (80.5%) — carry **135 818 of 196 489 ties on 435 747 of 924 699 cells**. Every one of them is a **draw / bootstrap / enumeration** artefact. Two published pair *shapes* carry the pair-side ties almost alone: `MaxDD_OOS vs ctrl_MaxDD_OOS` (24 580 of 48 474) and `OOS_MaxDD_pick vs OOS_MaxDD_best` (6 026 of 19 466) — the second is a **selector regret** column, where a tie means "the IS pick *was* the OOS best", a legitimate and meaningful zero, not an artefact.

## Q2 — what the published convention DOES with a tie (source, not inference)

1 104 comparison sites in 402 files: `>=` **579 (PASS)**, `<=` **211 (PASS)**, `>` **172 (FAIL)**, `<` **85 (FAIL)**, `==` **23 (PASS)**, `np.sign` **18 (FLIP)**, `in`/`not in` 10 (undecidable, reported as such), `!=` 3. So a tie is a **PASS 73.8% / FAIL 23.6% / FLIP 1.6%** of the time. The FLIP channel is confined to **9 files** (`gross-matched-turnover-constraints_B`, `how-many-published-gate-claims-are-flat-in-gross_cloud`, `is-the-sign-test-worth-anything-on-the-small-panel_cloud`, `two-same-day-runs-disagree-on-D3_B` and five others). **Consequence for PROTOCOL:** 4a's MaxDD leg (`MaxDD >= base MaxDD`) and 4b's DD cap (`|MaxDD| <= 0.60·|SPY MaxDD|`) both count a tie as a PASS — that is a *convention*, it is the record's majority one, and it is nowhere written down. Idea 520's "state the unit on every bar" applies here as "state the tie side on every bar".

## Q3 — does the record's own construction produce ties? (fresh, PROTOCOL-compliant)

972 arm-vs-control comparisons — EWALL(G) base book, 3 clause forms (BREADTH, SPYTR, VOL) × 3 levels × 3 depths × 2 cadences × 2 gross × 3 cost rungs × 3 panels (U56, B136, SMALL439), each against **its own** ungated parent at the same gross and rung. **55 ties (5.66%)**, and the mechanism is exact:

- **P(struct | tie) = 1.0000**, **P(tie | struct) = 0.9649**, **P(tie | ¬struct) = 0.0000**, where `struct` = the clause applied **no de-gross and paid no switch cost inside the control's binding drawdown episode** (peak→trough), so the arm/control equity *ratio* is constant across the episode. The 2 structural non-ties are arms whose own MaxDD is set on a *different* episode. This is idea 592's BIND==0 predicate at **100% of ties** — its 83.26% was the shuffle population's number, and the shortfall was the shuffles, not the predicate.
- Ties are a **panel and clause fact**: U56 BREADTH 29/108 and SPYTR 14/108, B136 6+6, **SMALL439 0 of 324** — a deep, permanently-drawn-down panel never gives a clause a binding episode to miss. VOL clauses tie **0 times on any panel** (they fire in exactly the episodes that set the drawdown).
- **Restatement:** prices rounded to 2 decimals (median relative move 3.26e-05 on U56, 0 on the other two): **0 of 972 tie labels move.** Real ties here are structural and stable — the opposite of the shuffle population's 166 unstable labels — while `sign(dMaxDD)` still changes on **39 of 972** rows (median |dMaxDD| shift 8.86e-06), i.e. the instability lives in the *near*-ties, which is precisely why a three-way label (idea 595) is the right fix and a tighter bar is not.

## KEEP paths and rule 8 (nothing promoted)

**4a 0 / 972. 4b 167 / 972. BOTH 0.** Of the 167 4b passes, **48 sit on a parent that already passes 4b** and 119 do not — but every one of the 119 is a **gross = 1.00** arm on U56 or B136 whose ungated parent fails 4b **on the DD cap** (parent MaxDD −20.7% / −22.8%, `fail4b = DD` at 0 and 10 bps): the clause buys ~2 pp of drawdown and the cap flips. That is the DD cap doing the cutting (ideas 530/531), not a timing edge, and none of them clears 4a. Rule 8, 54 chooser cells (level+depth on IS Sharpe ≤ 2016, OOS read once): the IS pick beats **doing nothing** on OOS Sharpe in **39/54**, beats SPY OOS in 32/54, and beats **RULES v2 OOS in 3/54**; mean regret **−0.076**. On SMALL439 the picks are negative against their own parent in 8 of 18 cells (worst −0.374). **No book promoted, no RULES change.**

SURVIVORSHIP: all three panels are current-constituent lists (SMALL439 = the sub-$2B panel less the 44 names with `max_1d_move >= 1.0`), so CAGR and drawdown *levels* are optimistic; the arm-vs-control contrasts and the tie counts are the durable part.

## What the record should do with this

1. **Ties are a draw-population problem.** Any file that enumerates draws, shuffles or bootstraps and then signs a MaxDD difference needs the three-way label; the record's ordinary book-vs-book files do not (median 0.00%).
2. **The tie side of every bar belongs in PROTOCOL**, next to idea 520's unit: 4a and 4b currently pass ties, by majority convention, silently.
3. **`OOS_MaxDD_pick vs OOS_MaxDD_best` ties are not errors** — they are the selector finding the best cell, and any census of "published ties" that does not separate regret columns from arm-vs-control columns will over-count by ~6 000 cells.
