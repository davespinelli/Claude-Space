# Idea 61 — gate-instrument-speed-curve (cloud, 2026-09-06)

**ANSWERED, and the answer is NEITHER of the queue's two options: there is no interior optimum
and slower is NOT always better. Flip rate has a FLOOR — below ~0.5 flips/tkr/yr the gate is
strictly worse in all four (book × convention) pools — and above it the curve is flat to within
±0.05 of Sharpe with an argmax location that is noise (median plateau 2 of 17 arms). Idea 4's
ordering does not survive as a curve: Spearman(flips, Sharpe) is 14 negative / 10 positive
across the 24 cells (mean −0.106) and +0.081 out of sample. Rules unchanged; one PARK
by-product. 4a 2/408 (both on the small panel), 4b 41/408, none of them a rule-8 pick.**

## Gates
- `fast_backtest_g` vs `engine.backtest`: **6.9e-18**; vs idea 171's: **0.0**.
- LIVE RULES v2 on U56 @10bps reproduces exactly: 8.66% / 1.2056 / −12.05%, halves 1.2259/1.1908.
- **P1 holds.** Idea 4's published flip rates re-derive with its own `trend()` code: band3
  **1.75** (published 1.77), abs **5.65** (5.75), 200d **7.44** (7.55), both **7.92** (8.06) —
  every one within 0.15 flips/tkr/yr.
- `gate_state(BAND, 0.00)` is asserted identical to `gate_state(STALE, 1)`; the two families
  share the bare 200d gate rather than approximating it.

## Q2 the speed axis (P2 **holds**, 9/9 family × panel)
Three families, one speed dial each, spanning **0.26 – 8.60 flips/tkr/yr** — exactly the
~0.5–8 the queue asked for. BAND b ∈ {0, .02, .03, .05, .08, .12, .20}; STALE k ∈ {1, 5, 21, 63,
126, 252} trading days; ABS deadband d ∈ {0, .05, .10, .20}. Flip rate is measured per
ticker-year on priced days, monotone decreasing in the dial in every family × panel.

## Q3 the curve (17 arms × 2 books × 2 conventions × 3 panels × 2 rungs = 408, all reported)
- **P3 FAILS.** `ew-all` @10bps `dg`: Spearman(flips, Sharpe) = **+0.421** (B136), **+0.652**
  (U56) — *faster* is better there, the opposite of idea 4's ordering read as a curve. Under
  `rw` it is −0.428 / +0.092. The sign is a property of the **convention**, not the book.
- **P4 holds directionally**: `top20` @10bps runs −0.296/+0.055 (`dg`) and −0.178/−0.229 (`rw`)
  — weaker and unstable, as idea 4 said.
- **P5 FAILS, and its failure is not evidence of an optimum.** 20/24 argmaxes are interior — but
  with 17 arms **15/17 = 88.2% of positions are interior by construction**, so 83.3% is *below*
  the noise expectation. The plateau test (idea 128) is the honest reading: a median of **2 of
  17** arms sit within 0.02 Sharpe of the cell argmax, spanning a median 0.44 flips/tkr/yr.
- **The one shape that survives** is the pooled, level-differenced curve. Each cell's 17 Sharpes
  minus that cell's mean, bucketed by flip rate:

| book/conv | <0.5 | 0.5–1 | 1–2 | 2–4 | 4–9 |
|---|---|---|---|---|---|
| ew-all/dg | **−0.0518** | +0.0047 | +0.0050 | +0.0280 | −0.0069 |
| ew-all/rw | **−0.0034** | +0.0508 | +0.0173 | −0.0218 | −0.0578 |
| top20/dg | **−0.0418** | +0.0000 | +0.0105 | +0.0129 | +0.0016 |
| top20/rw | **−0.0402** | +0.0051 | +0.0089 | +0.0108 | −0.0009 |

The `<0.5` bucket is the **worst in 4 of 4** pools. That is a floor, not an optimum.

## Q4 is the curve a gross ladder? (idea 277's control, run this morning)
**No — and the check is exact.** Re-reading every point against the un-gated constant-gross
ladder at its own realised mean gross leaves Spearman(flips, Sharpe) **unchanged to 4 dp in all
24 cells**, which is precisely idea 277's identity (the ladder's Sharpe span is 0.0013–0.0039,
so subtracting it cannot re-rank anything). Every cell's Sharpe range (0.109–0.295) exceeds that
floor by 30–200×. **P6 FAILS**: pinning gross under `rw` shrinks the Sharpe range by only
+6.8%/+10.1%/+28.7%/+32.3% on the large-cap cells and *widens* it 81% on SMALL439/ew-all. The
speed axis is real information; it is just not orderable.

## Q5 rule 8 (**P7 holds**)
IS-Sharpe chooser beats do-nothing in **3 of 24** cells, mean OOS Sharpe **0.845 vs the live
book's 0.967** (SPY 0.882) — the **13th** selection-loses instance in the record. It also loses
to the pre-registered **slowest arm** (0.845 vs 0.883, wins 10/24). Out of sample the speed
relationship is gone: mean Spearman(flips, OOS Sharpe) **+0.081**, negative in 9/24. Mean
Spearman(IS, OOS) over the 17 arms **+0.144**.

## Q6/Q7 KEEP paths
**4a 2/408** — both `ew-all/dg/BAND 0.05` on SMALL439, where the live book is weak, not a real
win. **4b 41/408**, all on U56 (32) and B136 (9), none on the small panel. The binding bar over
the 367 failures is **DD** (119 alone, 296 including it) then CAGR. Read out of sample: **41 of
41 beat SPY**, **0 of 41 beat the live book**, and **0 of 41 are the rule-8 pick of their own
cell** — the passes are real and unselectable.

**PARK by-product** (memo: `2026-09-06_band12-ewall-rw_PARK_MEMO.md`): `EWall + band12-rw` on
U56 clears 4b at **both** cost rungs (14.02% / **1.2264** / −19.42%, halves 1.261/1.205, OOS
**1.2662**) at **1.93x/yr** turnover and +0.1024 gross-matched dSharpe — the best OOS Sharpe in
the run. It fails 4b on B136 on the **DD cap alone** (−21.74% vs −20.23%) and no honest chooser
picks it, so it is PARKed, not KEPT.

## Caveats
SURVIVORSHIP runs **against the slow arm** here — a wide band is slow to exit a name a
delisting-aware panel would kill — so a survivorship-free panel would push the whole curve toward
the fast end and make the floor finding *stronger*, not weaker. Stated, not adjusted. The small
panel is secondary (the 200d gate is inverted there, ideas 39/49/136). Flip rate is counted on
gate state, not on trades; turnover is reported beside it. Costs are flat linear bps. BAND b=0
and STALE k=1 are the same gate, so the 17 arms are not 17 independent draws.

## What the record should carry
Flip rate is a **floor variable, not a design variable**. The reportable statement is "keep the
gate above ~0.5 flips/tkr/yr", not any argmax.
