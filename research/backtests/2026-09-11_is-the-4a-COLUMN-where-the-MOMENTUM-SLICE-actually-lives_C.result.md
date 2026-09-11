# IDEA 767 — is the 4a COLUMN where the MOMENTUM SLICE actually lives?

Lane C, 2026-09-11. **KILL of the reading. No KEEP candidate, no RULES change.**
`RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## The question

Idea 563 priced the daily-depth-matched momentum slice (MOM-D) as a book and found the
head-to-head against the MA slice a coin toss on Sharpe (40.3% of 648 pairs). Its KEEP
columns split, though: of the 33 books on its 1,296-point grid that passed **path 4a**
(beat the LIVE BOOK), **20 were MOM-D and all 33 were DEGROSS**, while **4b** (beat SPY)
went MA-THRESH 21 / MOM-D 15. The queue's reading: the momentum slice "lives in the 4a
column". This run re-cuts that column directly on the momentum slice and asks whether any
of the 20 survives rule 8.

## What was run

* **Leg A — the direct re-cut.** The momentum slice on its **own** depth (top
  `ceil(q × rankable)` names by 12-1 momentum, recomputed daily, **no MA gate anywhere**),
  `q ∈ {0.05, 0.10, 0.20, 0.30, 0.50}`, gross `{0.50, 0.75, 1.00}`, 3 panels
  (U56 55, B136 135, SMALL439 439). **360 books**, all in `.grid.csv`.
* **Leg B — rule 8 on leg A.** `(cadence, construction)` picked on **IS Sharpe alone**
  (start..2016-12-31), OOS 2017+ read **once**; 4a re-scored out of sample, strict
  (both OOS halves + DD) and lenient (OOS Sharpe + DD). 45 picks, `.walkforward.csv`.
* **Leg C — the 20 themselves.** Idea 563's exact MOM-D 4a-passing cells rebuilt
  (B136 θ 0.00 / −0.06; SMALL439 θ 0.30 / 0.20 / 0.12 / 0.06), 144 books, then the same
  rule-8 selector run inside each `(panel, θ, gross)` cell. `.the20.csv`, `.keeppaths.csv`.
* **Leg D — gross-matched control (derived, not tuned).** Every 4a passer re-scored against
  **SPY held at that book's own realised mean gross**, remainder cash. `.control.csv`.

**Tuned parameters: exactly 2** — cadence `{D,W,M,Q}` × construction `{RESPREAD, DEGROSS}`.
Panel, depth/θ and gross are reported axes, never selected over. 10 bps per unit turnover,
next-day execution; 0 and 25 bps derived exactly off the same held path and reported.

## Gates (all pre-registered, all pass)

| gate | what | residue | bar |
|---|---|---|---|
| G0 | `fast_run` vs `engine.backtest` returns **and** turnover, every panel, D and W | **0.000e+00** | 1e-12 |
| G1 | idea 563's committed MOM-D grid rebuilt here, 144 matched books, 6 columns | **2.220e-16** | 1e-09 |
| G2 | derived cost rung vs a fresh run at that rung | **0.000e+00** | 1e-15 |
| G3 | depth identity, `held == ceil(q × rankable)` every day | **0.000e+00** | 0 |

G1 reproduces **all 20** of idea 563's MOM-D 4a passes exactly (per panel: B136 2.220e-16,
SMALL439 9.714e-17). The 20 are a real feature of the grid, not a bookkeeping error.

## The answer

**None of the 20 survives rule 8, and the 4a column is a gross artefact, not a slice.**

1. **The 20, read out of sample.** OOS-4a **STRICT 0/20**; lenient 13/20.
2. **The 20, reachable at all.** The `(cadence, construction)` an IS-Sharpe selector would
   have picked inside the book's own cell equals the 4a-passing dial in only **10/20**.
3. **Both together — picked *and* passing OOS-4a: 0/20.** The intersection is empty.
   Of the 18 cells containing a 4a pass, picks pass OOS-4a strict **0/18** (lenient 9/18),
   4b **1/18**.
4. **The direct re-cut splits perfectly on construction, not on the slice.** 44/360 books
   pass 4a and **all 44 are DEGROSS** (RESPREAD 0/180); 20/360 pass 4b and **all 20 are
   RESPREAD** (DEGROSS 0/180). **BOTH = 0.** 4a passers run mean gross 0.10 (SMALL439) —
   i.e. ~90% cash — at 0.6–4.7% CAGR; the binding 4b bar over the failures is CAGR (220).
5. **Rule 8 on the direct re-cut** leaves **6/45** picks passing OOS-4a strict, every one of
   them SMALL439 DEGROSS at 4.9–19.4% mean gross, 1.0–3.4% OOS CAGR. Picks beat RULES v2
   OOS Sharpe 15/45 and SPY 30/45, but the two sets are disjoint by panel: SMALL439 beats
   the book 15/15 and SPY 0/15; U56 and B136 beat SPY 30/30 and the book 0/30.
6. **The control settles it.** A **gross-matched SPY blend beats every one of those 6 on OOS
   Sharpe** (0.8820 vs 0.7159–0.7405), on **both** OOS halves (0.9748/0.7820 vs
   0.9588/0.5375 … 0.9171/0.5156) **and** on OOS drawdown (−1.86% vs −2.35% at matched
   gross). Across all 64 full-sample 4a passers, only **7/64** beat their own gross-matched
   index on Sharpe (all B136/U56, none SMALL439), and **the trivial control itself passes 4a
   in 57/64** of the same comparisons.

The 4a bar is RULES v2 **on the idea's own panel**, and on SMALL439 that bar is weak
(Sharpe 0.5710, OOS 0.5665, OOS-H2 0.1704). Cutting gross until drawdown clears it is
enough to pass 4a with no selection skill at all — which is what 57/64 says. The momentum
slice does not live in the 4a column; **cash does**.

## Numbers vs the comparands

| leg | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| best OOS-4a survivor (SMALL439, q=0.10, DEGROSS/M, gross 1.00) | 1.84% | 0.7309 | −4.67% | 2.00% | 0.7405 | −4.67% |
| gross-matched SPY control (same 9.78% mean gross) | — | — | — | 1.56% | **0.8820** | −3.69% |
| RULES v2, SMALL439 (4a bar) | 3.80% | 0.5710 | −14.70% | 3.84% | 0.5665 | −14.70% |
| RULES v2, U56 / B136 | 8.63% / 8.03% | 1.2069 / 1.1078 | −11.90% / −12.18% | 9.48% / 7.98% | 1.2834 / 1.1206 | −11.90% / −12.18% |
| SPY (4b bar) | 15.11% | 0.8835 | −33.72% | 15.24% | 0.8721 | −33.72% |

**SURVIVORSHIP:** B136 and SMALL439 are current constituents only. CAGR levels are inflated
and the 4a bar carries the same bias; the 4b (SPY) bar and the leg-D control do not, which
is why the control read is the one to trust here.

## Verdict

**KILL.** 0 of the 20 survives rule 8; 4a and 4b on the momentum slice are disjoint sets
separated entirely by construction (gross), not by the slice; and a gross-matched index
beats every OOS-4a survivor on Sharpe, on both OOS halves and on drawdown. No KEEP path,
no book, no RULES change.

## Follow-on for the queue

* 4a's MaxDD leg admits any sufficiently de-grossed book against a weak same-panel bar —
  census how many committed 4a passes in the record are held by books running < 25% mean
  gross, and re-score each against its own gross-matched index.
* SMALL439's RULES v2 comparand has OOS-H2 Sharpe 0.1704 against OOS-H1 0.9166; every
  SMALL439 4a verdict in the record rests on that half.
