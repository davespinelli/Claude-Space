# Idea 633 — is FLIP1 already dead at 10 bps?  (lane C, 2026-09-10)

**VERDICT: ANSWERED / the queue's premise is KILLED. No KEEP-candidate, no memo, no RULES
change. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.**

Script: `research/backtests/2026-09-10_is-FLIP1-already-dead-at-10-bps_C.py`
Artefacts: `.console.txt` `.census.csv` `.files.csv` `.grid.csv` `.sweeps.csv` `.ladder.csv`
`.decomp.csv` `.paired.csv` `.walkforward.csv` `.keeppaths.csv`

Two tuned parameters and no more (PROTOCOL 4): **RUNG** ∈ {0, 2.5, 5, 7.5, 10, 15, 20, 25, 40}
bps and **FAMILY** ∈ {band, gross, n} — the queue's own two.

---

## The question, and the answer in one line

The queue asserted that idea 408's neighbour-flip rate (16.0% → 6.7% → 0.0% across 0/10/25 bps)
means *every* fragility statistic the record computes is measuring something costs have already
removed at the protocol rung. **It does not.** On the record's own committed corpus the flip
rate at 10 bps is **12.65%**, *higher* than the 7.98% at 0 bps. Idea 408's monotone collapse is
a property of its own 150-point grid — whose 4b pass count went 31 → 5 → 0 — not a record law.

## Gates (all pass, run before any new number is read)

| gate | what it establishes | result |
|---|---|---|
| **G0** | idea 408R's 16.0 / 6.7 / 0.0 reproduced from **its own** `.cols.csv` | exact; and the pass count beside it is **31 → 5 → 0** |
| **G1** | `fast_backtest` vs `engine.backtest`, cost 0 | max\|dret\| 1.04e-17, max\|dturn\| 2.22e-16 |
| **G2** | hosts nest `baseline.rules_v2_weights` / `rules_v1_weights` | 0.000e+00 / 0.000e+00 |
| **G3** | the arithmetic FLIP1 rests on, synthetically | all-fail and all-pass **both score 0 flips**; flips ≤ 2×boundaries always |
| **G4** | one backtest re-priced at nine rungs == nine engine runs | max\|dret\| 1.04e-17 |

G0 already contains half the answer: at 25 bps the parent's grid has **no passing point at
all**, so its FLIP1 = 0 is arithmetic, not evidence about fragility.

## What FLIP1 actually is

A point is FLIP1 iff it sits next to a **boundary of the pass region**. For a sweep of `G`
points with `B` boundaries, `flip_count ≤ 2B`, and `B = 0` — an **all-pass or an all-fail
sweep** — forces FLIP1 = 0 with no reference to robustness. G3 demonstrates that the perfectly
robust sweep and the completely worthless one are *indistinguishable* under this statistic.
That gives the decomposition the whole file turns on, which is an identity, not a model:

```
flip_rate  =  mixed_weight  ×  (flip rate | mixed)
d(flip)    =  (w₁−w₀)·c₀      +      w₁·(c₁−c₀)
                MIXED leg            WITHIN leg
```
`H_FRAGILITY` (costs smooth the surface) predicts the WITHIN leg carries the fall.
`H_DEPOPULATION` (costs empty the pass region) predicts the MIXED leg does.

## Part B — the census the queue asked for

2,919 committed CSVs read; 525 carry a 4b verdict column; **149** are usable dial sweeps with a
declared rung → **15,194 sweeps / 86,859 grid points**. Every exclusion is written out
(`.files.csv`): 203 no declared rung, 127 no numeric dial with ≥3 values, 46 no cell with ≥3
distinct dial values. Cell keys exclude every verdict-family column by rule — grouping by
`pass4a` would sort a grid by an outcome and fabricate boundaries.

Where the record actually publishes (share of sweep points): **10 bps 31.6%, 25 bps 31.0%,
0 bps 12.4%**, 5 bps 9.0%, 50 bps 5.5%, rest ≤ 6%.

| rung | points | pass share | mixed share | flip rate | flip \| mixed |
|---|---|---|---|---|---|
| 0 | 10,783 | 0.188 | 0.196 | **7.98%** | 33.2% |
| 5 | 7,825 | 0.158 | 0.160 | 5.90% | 27.5% |
| **10** | 27,476 | 0.178 | 0.265 | **12.65%** | 43.1% |
| 15 | 5,378 | 0.162 | 0.140 | 6.01% | 47.0% |
| 25 | 26,912 | 0.092 | 0.152 | 7.41% | 40.9% |
| 50 | 4,765 | 0.069 | 0.048 | 1.99% | 35.7% |

The pooled 0-vs-10 comparison mixes different files, so the load-bearing read is like-for-like:
the **42 files that publish the same dial family at both rungs**. There the rate does fall,
7.98% → 5.87% → 3.89% (0/10/25), **but it does not die**, and per file:

- flip rate **falls in 22 files, rises in 7, unchanged in 13**;
- **6 of 42 files** score exactly zero at 10 bps — and **all 6 were already zero at 0 bps**.
  **Not one committed file in the record loses its flips by moving from 0 bps to the protocol
  rung.** That is the sharpest available refutation of "already dead at 10 bps".

## Part D — the mechanism: depopulation, not smoothing

| corpus | rung | flip 0 bps | flip @rung | Δ | MIXED leg | WITHIN leg |
|---|---|---|---|---|---|---|
| LIKEFORLIKE | 10 | 7.98% | 5.87% | −0.0212 | **−0.0152 (72%)** | −0.0060 |
| LIKEFORLIKE | 25 | 7.98% | 3.89% | −0.0410 | −0.0268 | −0.0142 |
| FRESH | 10 | 2.84% | 2.84% | 0.0000 | 0.0000 | **0.0000** |
| FRESH | 25 | 2.84% | 1.42% | −0.0142 | **−0.0142 (100%)** | **0.0000** |

On the fresh, cost-controlled grid the flip rate conditional on a boundary is **flat at 13.3%
across all nine rungs** — the within leg is identically zero — while the mixed share falls
22.2% → 22.2% → 11.1%. At file level the same: mean conditional rate **0.456 (0 bps) vs 0.459
(10 bps)**, a change of **+0.003**. Costs do not smooth the verdict surface; they delete the
region that has a surface.

**Only FLIP1 and window width die this way.** THIN and margin are defined at every point,
passing or not, and they survive a depopulated pass region: on the fresh ladder `thin_rate`(τ=1)
moves 4.26% → 2.84% → 2.13% and the median thin ratio actually *rises* 15.04 → 17.02 → 19.39.
Median window width is 0 at every rung on this grid. So the queue's three named statistics are
not one family: two of them are pass-region-conditional and one is not.

**Caveat, stated not buried:** the fresh grid's mixed subsample is tiny (2 sweeps of 9 at
0 bps). It is a clean mechanism demonstration on a grid whose spacing and rungs this file
controls; the 86,859-point census is where the statistical weight is.

## Part E — rule 8 and both KEEP paths

Choose on 2009–2016 only, evaluate 2017–2026 untouched. Three choosers per (panel, dial, rung),
27 cells per chooser: **PLAIN** (argmax IS Sharpe), **ROBUST** (argmax IS Sharpe among points
that are neither IS-FLIP1 nor IS-THIN, falling back to PLAIN), **WINDOW** (midpoint of the
widest IS-4b run, abstaining to RULES v2 when there is none).

ROBUST differs from PLAIN in **2 of 9 cells at 10 bps** — the fragility filter is very nearly
inert — and buys **+0.0001 of OOS Sharpe** for it (0.8872 vs 0.8871), while costing 0.19 pp of
OOS CAGR (12.23% vs 12.42%). Pooled over all nine rungs: PLAIN 0.8766, ROBUST 0.8767, WINDOW
0.9791 — and WINDOW's number is abstention, not skill (it abstains to RULES v2 in essentially
every cell; `vs_base` = −0.0001).

Every chooser loses to the live book out of sample. OOS 2017–2026 references:

| | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| RULES v2 (live) U56 / B136 / SMALL439 | 1.3124 / 1.1504 / 0.6071 | 9.71% / 8.21% / 4.14% | −11.9% / −12.2% / −14.3% |
| SPY | 0.8758 | 15.32% | −33.7% |
| PLAIN @10 bps (mean of 9 cells) | 0.8871 | 12.42% | −32.5% |
| ROBUST @10 bps | 0.8872 | 12.23% | −32.2% |

**KEEP paths on all 1,269 fresh grid points:** 4b passes **3/141 at the protocol rung**
(27 across the nine rungs), 4a passes **2/141** (24 across rungs). Every 4b passer is the top
of the **gross** ladder (U56 g=0.95/1.00, B136 g=1.00), binding on the **CAGR floor** by
+0.0007 to +0.0097 — idea 585's g-band ladder, which the record already owns and which this
file does not re-claim. The two 4a passers are SMALL439 band points clearing a SMALL439
baseline whose own OOS Sharpe is 0.607. **No KEEP claimed, no book promoted.**

## What the record should take from this

Report-only, not written into PROTOCOL by this run:

1. **A neighbour-flip count is not a fragility statistic.** It is bounded by the number of pass
   boundaries a sweep has, so an all-fail sweep and an all-pass sweep score identically.
   Any published FLIP1 rate must carry its **pass count and mixed share** beside it, or the
   reader cannot tell robustness from an empty pass region.
2. **Idea 408's 16.0 → 6.7 → 0.0 should be quoted as a statement about its own grid's pass
   count (31 → 5 → 0), not as a statement about cost rungs.**
3. **The "0-bps artefact" charge is not supported.** Only 12.4% of the record's committed sweep
   points are published at 0 bps, and on that subset flips are *fewer* than at 10 bps.

## SURVIVORSHIP (PROTOCOL 9)

B136 and SMALL439 are **current-constituent lists** — names delisted, acquired or dropped from
the screen are absent — so their absolute levels are biased up and no CAGR/Sharpe here is a
tradable estimate. SMALL439 drops the 44 names with `data/small_meta.csv max_1d_move >= 1.0`
first. Only the within-panel rung-against-rung contrasts, taken on identical books, are meant
to survive that. SPY is priced cost-free at every rung (the record's convention, and the
conservative choice: charging SPY would lower the 4b bar as the rung rises and manufacture
passers at exactly the rungs this file reports as empty).
