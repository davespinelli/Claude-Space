# Idea 1048 (lane C, 2026-09-16) — does ANY committed EXPONENT or SCALING claim state its own RESOLUTION?

**ANSWERED = NO.** Of the **43** valued exponent/scaling claims in the record proper
(LEADERBOARD.md + CHANGELOG.md), **0** state a width on the exponent's own value; corpus-wide
**1 of 104**, and that one is yesterday's *proposed* clause memo (1044's), not a result. Two
classifier hits in the record proper both fail the audit: 1012's `SE(L) fits a log-log slope of
-0.5110` raises the SE flag because **SE is the fitted Y-VARIABLE**, and the other quotes a
±0.02 band on Sharpe flatness. **10 of 43 state a SPREAD across cells — a dispersion, not a
resolution. 31 of 43 state nothing.**

## The queue's premise is a DRAW-COUNT fact, not a TAPE fact — KILL

1044's `0.67–0.73 wide at 90%` is read by the queue as what "an exponent fitted on this tape"
costs. On the **same tape**, 1012's exponent bands **0.0429** at 90% — **16x tighter**. The
mechanism control (reported, no bar) walks the replications per ladder rung by exact nesting of
the same 1,000 draws, TAPE basis, U56, BLOCK21:

| draws/rung | 1000 | 250 | 60 | 15 | 4 | 2 |
|---|---|---|---|---|---|---|
| 90% width of b | 0.0418 | 0.0887 | 0.1715 | 0.3317 | 0.8969 | 2.2498 |

The width falls as `1/sqrt(k)` (0.0418·√(1000/60) = 0.171 against the measured 0.1715) and
crosses 1044's band **between k = 15 and k = 4**. 1044's width is what **about five
replications per length** buys, not what this tape allows.

## What 1012's exponents actually resolve — three KILLs and a CONFIRM

* **CONFIRM (G4):** 1012's committed `.ladder.csv` reproduces on its own seed stream over **522
  SE cells, max |d| 8.33e-17**, and its three published exponents to **4.65e-05** (SPY −0.5110,
  median book −0.5003, i.i.d. control −0.4943).
* **KILL three exponents:** pairwise |d| of those three is **0.0060 / 0.0107 / 0.0167** against a
  90% width of **0.0429** — **0 of 3 distinguishable**. The record printed one measurement three
  times (**H_SAME FAIL**).
* **KILL the fourth decimal:** the width supports **1** decimal; the record prints **4**
  (**H_DIGIT FAIL**).
* **KILL "measured, not asserted" as a claim of separation:** **−0.5 sits inside the 90% interval
  in 2 of 2** re-derived panel cells (**H_SQRT FAIL**). 1012's `H_SCALE PASS` survives — the law
  is confirmed in expectation — but nothing in the record distinguishes its exponents from the
  theory value they confirm.

## The three bases (H_BASIS PASS, and the ordering is the prediction)

U56 / BLOCK21 / 90%: **OLS 0.0291 < REDRAW 0.0404 < TAPE 0.0429**, max/min **1.47** (bar ≤ 1.50).
The fit's own residual interval — the one an author gets for free — understates the tape width by
**32%**, because the six rungs are read off one tape and OLS assumes they are not.

## Gates 9 of 9 PASS; hypotheses 2 of 6

G1 fast runner ≡ `engine.backtest` (6.94e-18 / 1.67e-16) · G2 pools 18/18 GRID + 9 SHELF ·
G3 SPY OOS 15.21% / 0.8711 / −33.72% (max |d| 1.70e-04) · **G4 cross-run above** · G5 determinism
0.0 · **G6 zero-truth control: median b −0.5020 against a truth of exactly −0.5, one-tape interval
/ across-tape spread 1.119** · G7 census stamp (1,990 files, 46,145,011 bytes,
file_list_sha `8e2a6ae39e6a0d4b`) · G8 extraction order-independent over 2,122 rows ·
**G9 audit coverage: 9 hits, 9 adjudicated, 0 unadjudicated.**
PASS: H_RESOLVE (0.0429 ≤ 0.10), H_BASIS. FAIL: H_ANY, H_SAME, H_SQRT, H_DIGIT — every failure
measured and reported.

## Rule 8 and both KEEP paths — nothing promoted

Picks made on 2009-01-13..2016-12-31 **alone**, 2017–2026 read once, 3 IS-only choosers × 2
panels × 3 rungs. At 10 bps: U56 `band0.08@1.00` **11.99% / 1.1615 / −19.05%**, U56
`qroll-q0.17-w1008-d0.50` **15.60% / 1.2933 / −15.59%**, B136 `band0.08@1.00` **11.05% / 1.0974 /
−19.50%**, B136 `qroll-q0.12-w1008-d0.50` **14.30% / 1.1572 / −17.31%**. Comparands: **SPY OOS
15.21% / 0.8711 / −33.72%** (U56), 15.33% / 0.8767 / −33.72% (B136); **RULES v2 (live) @10 bps
full 8.62% / 1.2007 / −12.05%** (halves 1.232 / 1.176), OOS 9.45% / 1.2762 / −12.05%.
**OOS 4b 18 of 18, OOS 4a 0 of 18**; full-sample ladder 4b 54 of 108, 4a 2 of 108.
**Nothing promoted** — the question moves no price verdict.

## Limits, stated

The STRICT regex is conservative (an exponent-family keyword plus a decimal within 60 characters),
so **104 valued claims is a LOWER bound** and the "states nothing" share is measured on the subset
most favourable to the record. Only the 1012 family is re-derivable from a committed definition;
every other claim carries a **TRANSFERRED** width, an order-of-magnitude statement and not a
re-derivation, and the two populations are never summed. The TAPE null is a stationary block-21
resample, which keeps short-range dependence and destroys regime structure, so every width here is
a **LOWER** bound. The width itself is a 100-rep estimate and carries about ±0.001 (0.0429 in the
headline block against 0.0418 in the draw control, same object, different seeds). The audit is a
judgement on 9 rows, each printed with its reason in `.audit.csv` so it can be disagreed with.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists, so every rule-8 CAGR and
drawdown LEVEL is optimistic and every 4b count an UPPER bound. The census arm is a census of
committed text and inherits its sources' bias. A survivor panel raises the Sharpe level, hence the
SE of a Sharpe, hence every width reported here in the same direction. SPY is a real index series
and is not inflated.

**PROPOSED, NOT APPLIED (rule 6):** `2026-09-16_exponent-resolution-clause_C.memo.md`.
