# Idea 874 — does the record's 4b DD CAP have the SAME two-questions problem as the CAGR FLOOR? (lane B, 2026-09-15)

**ANSWER = NO, AND THE QUEUE'S PREMISE IS REFUTED TWICE OVER. The same convention swap that idea
868 measured as a CONCESSION on the CAGR floor (9 books FAIL→PASS) is an ANNIHILATION on the DD
cap (26 PASS→FAIL; the DD leg alone goes 0 of 62 at PROTOCOL's own κ=0.60), and the two legs move
DISJOINT books — Jaccard 0.000, floor flips gbar 0.33–0.53, cap flips gbar 0.65–0.94. KILL for
capital.**

No RULES change, no book promoted, no KEEP claimed; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched (rule 6). One PROTOCOL line is PROPOSED, NOT APPLIED.

SELECTION: taken as the LAST Open idea carrying a PRICE leg. 896 / 895 / 894 / 877 / 876 sit
below it and carry standing SKIP notes as prose censuses with no book to price, so none can carry
this run's mandatory rule-8 walk-forward.

## Design
868's own 62 books — the 8 memo-backed SHELF books and the 54-book mechanical GRID ladder on
U56 / B136 / SMALL — **imported, not re-typed**, from the lane-C builders 868 itself imported.
Each priced at 2 cost rungs against 3 comparand conventions × 6 cap fractions =
**2,232 verdict cells, all published**. Two tuned parameters, the two the queue names:
**convention** and **cap fraction κ**.

| convention | comparand | what it asks |
|---|---|---|
| CURRENT | `r_SPY,t` | PROTOCOL's own — absolute capital terms |
| CONST | `gbar · r_SPY,t` | matched to time-averaged realised gross |
| PATH | `g_t · r_SPY,t` | matched day by day to the book's own exposure |

MaxDD is taken on each comparand's **own compounded equity curve**, never scaled from SPY's.
That distinction is measured, not assumed: median(CONST_DD − gbar·SPY_DD) = **−0.599%** on the
GRID (max 1.113%).

## Gates (printed before any new number was read)
G1 CAGR/Sharpe 8 of 8 within 1.00 pp / 0.10 · **G1 DD leg 7 of 7 memo'd MaxDDs within 2.00 pp**
(one shelf memo published no MaxDD) · G2 0.000e+00 · G3 0.000e+00 · G4 0.000e+00 ·
**G5 CROSS-RUN: this run reproduces 868's COMMITTED `gaps.csv` on all 62 books to 9.7e-17** —
which is what makes "the same books, the same direction" a measurement here rather than an
assertion. All PASS.

## The answer: same swap, opposite sign, disjoint books
4b count at PROTOCOL's own κ=0.60 / φ=0.70, 10 bps, 62 books:

| swapped leg | CURRENT | CONST | PATH |
|---|---|---|---|
| **DD leg (this run)** | 26 | 16 | **0** |
| CAGR leg (868's, recomputed here) | 26 | 35 | 35 |
| both legs together | 26 | 16 | **0** |

**H_DIR PASS 26 of 26.** Every verdict the DD swap moves under PATH moves PASS→FAIL; every one
868's floor swap moved went FAIL→PASS. The queue's "same direction" is refuted, and it is refuted
by arithmetic, not by luck: gross-matching *lowers* a comparand's CAGR (loosening a floor) and
*shallows* its drawdown (tightening a cap). One convention cannot fix both legs.

**H_SAME FAIL at Jaccard 0.000.** The two swaps move **disjoint** book sets — 26 DD flips and 9
CAGR flips with zero overlap in 35. The floor's flips are the low-gross books (gbar 0.332–0.527,
all GRID band-g0.50/0.75); the cap's are the high-gross ones (gbar 0.650–0.944, **all 8 SHELF
books included**). So the defect 868 found and the defect priced here are not one defect seen
twice; they are two, and they bind on opposite halves of the same ladder.

**H_TWO FAIL as declared, PARTIAL underneath.** Pooled ρ(gbar, DD slack) is −0.622 under CURRENT
and −0.095 under PATH — same sign, so the pre-registered opposite-orders bar fails as printed.
Per panel the shape *is* there on the two large-cap panels (U56 −0.429 → **+0.280**, B136 −0.518
→ **+0.162**) and is absent on SMALL (−0.969 → −0.905), whose 18 books hold the pooled sign.
Reported
FAIL on its own bar; the per-panel split is published rather than substituted for it.
868's CAGR leg on the identical books, for contrast: **+0.535 → −0.619**, a clean reversal.

**H_EASY PASS +48.0 pp.** The record's premise from 662 / 866 / 676 holds: under CURRENT at
κ=0.60 the DD leg passes **17 of 17** GRID books with gbar < 0.70 and **13 of 25** with gbar ≥
0.85. The cap is mechanically easy for a de-grossed book — which is exactly why swapping its
comparand to that book's own gross is not a correction but a double charge: de-grossing already
bought the shallow drawdown, and the gross-matched cap then demands a further 40% off it.

**The bar is unsatisfiable at PROTOCOL's own fraction.** Under PATH the DD leg passes **0 of 62**
at κ=0.60 and 0 of 62 at 25 bps. From the published ladder, holding stringency constant would
need κ ≈ **0.80–1.00** on the GRID (PATH 0.389 → 0.704 across that span, against CURRENT's 0.648
at 0.60) and **κ = 1.00** on the SHELF. A comparand swap is not free on either leg.

## Rule 8 (2009–2016 chosen, 2017+ read once)
**H_WF PASS 60 of 62**: the book-minus-PATH DD gap keeps its sign across the split (SHELF 8/8,
GRID 52/54; medians IS +5.48% / OOS +4.56% on the SHELF). The IS-only DD screen is **one-directional**
exactly as idea 878 found: false positives **0 of 62**, IS-fail-but-OOS-pass 20 of 62.

IS-only selector (highest 2009–2016 Sharpe per panel), OOS read once, 10 bps, t+1, weekly:

| panel | book | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b | 4b w/ PATH DD |
|---|---|---|---|---|---|---|---|
| U56 | `u56-quantile50-respread-M` | **15.90%** | **1.230** | −19.46% | FAIL | **PASS** | FAIL |
| B136 | `b136-r620-gross065-W` | 14.52% | 1.040 | −19.43% | FAIL | **PASS** | FAIL |
| SMALL | `SMALL-band0.08-g1.00` | 5.44% | 0.599 | −18.73% | FAIL | FAIL | FAIL |

Comparands on the U56 window: SPY full **15.13% / 0.885 / −33.72%**, OOS **15.27% / −33.72%**;
RULES v2 (live) full **8.64% / 1.208 / −11.90%**, OOS **9.49% / 1.286 / −11.90%**. On B136: SPY
full 15.16% / 0.886 / −33.72% (OOS 15.33%); RULES v2 full 7.98% / 1.101 / −12.18% (OOS 7.88% /
1.108).

Both U56 and B136 picks are **already-committed shelf books with published memos**
(`2026-09-11_u56-quantile50-respread-M_4b_B_MEMO.md`,
`2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md`), reproduced here inside G1, so **no new memo is
written and nothing new is proposed**. 4a fails on both (MaxDD −19.46% against RULES v2's
−11.90%), which is the standing pattern: 4b passes, 4a does not.

## PROTOCOL line — PROPOSED, NOT APPLIED (rule 6)
*A 4b leg may not have its comparand re-based without re-calibrating its own threshold. Gross-
matching lowers a comparand's CAGR and shallows its drawdown, so the identical swap loosens the
CAGR floor and tightens the DD cap; at PROTOCOL's published φ=0.70 / κ=0.60 it admits 9 books on
one leg and rejects 26 disjoint books on the other, and the DD leg becomes unsatisfiable (0 of
62). Any proposal to gross-match 4b must state both legs' thresholds together and publish the
book sets each moves.*

## Honest limits
- SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops 52
  tickers with max_1d_move ≥ 1.0), so every drawdown LEVEL here is optimistic — the books' and
  the comparands' alike. The flip counts are same-tape differences and are unaffected.
- The 62 books are 868's, by design, so the two runs' flip sets are comparable; they are not a
  random sample of anything, and the GRID's gross distribution (median gbar 0.839) is what sets
  the pooled ρ that fails H_TWO.
- κ ≈ 0.80–1.00 is read off the published ladder, not fitted; no third parameter was tuned.

**Verdict: KILL for capital.** The queue's question is answered NO, and the useful part of the
answer is that 4b has two comparand defects, not one, and they bind on disjoint halves of the
record's own ladder.
