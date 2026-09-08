# idea 204 — is-the-pool-sign-the-whole-selector-story  (lane B, 2026-09-08)

**Verdict: ANSWERED / SPLIT. The queue's CONCLUSION is CONFIRMED and its proposed INSTRUMENT is
KILLED.** "Does selection help" was indeed the wrong question — but not because the pool's sign
explains the selector's sign. The regression idea 204 asks for is an *algebraic identity* and
cannot fail; the testable residual is `lift`, and on `lift` selection buys ~0 while every selector
still loses to doing nothing. No RULES change, no book promoted, no KEEP claimed; RULES.md,
scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

## Gates (all PASS, quoted before any result)
| gate | value |
|---|---|
| G1 `fast_backtest` vs `engine.backtest`, returns / turnover | u56 6.939e-18 / 1.735e-16 · broad 1.041e-17 / 1.804e-16 · small 6.939e-18 / 1.110e-16 |
| G5 cost-rung identity `r(c) = r(0) − turnover·c/1e4` vs a live 25-bps `engine.backtest` | **0.000e+00** on all three panels |
| G2 the decomposition identity `sel_d == pool + lift`, 7,356 claim rows | **1.110e-16** |
| G4 comparand-invariance of `lift` across C_CONTROL / C_V2 / C_SPY | **0.000e+00** |
| G3 corpus-A provenance: pools with exactly one `control` arm | **72 / 72** |
| live RULES v2 @10 bps, u56 | 8.66% / 1.2056 / −12.05% (OOS 9.53% / 1.285 / −12.05%) |

## The structure the queue did not notice
For any selector K picking arm a\* from pool P against comparand C,

```
sel_d = M_OOS(a*) − M_OOS(C)          pool = mean_P M_OOS(a) − M_OOS(C)
lift  = M_OOS(a*) − mean_P M_OOS(a)   ⇒   sel_d ≡ pool + lift        (G2: 1.11e-16)
```

so idea 204's regression of `sel_d` on `pool` is a regression of (X+Y) on X. Its slope is
1 + cov(lift,pool)/var(pool); it cannot return a null and a slope near +1 with a big R² is
arithmetic. **Its R² measures how much the COMPARAND moves across pools, not how much the pool
explains the selector:**

| corpus | comparand kind | n | median R² | median slope | share \|slope−1\|<0.35 |
|---|---|---|---|---|---|
| A (the record's own poolable grid) | FIXED (SPY / live book) | 24 | **0.8850** | +1.0633 | 0.958 |
| A | the pool's OWN control | 12 | **0.2555** | +0.6815 | 0.167 |
| B (fresh dial pools) | FIXED | 54 | 0.6949 | +0.9112 | 0.593 |
| B | the pool's OWN control | 27 | 0.5464 | +0.8804 | 0.333 |

Same claim rows, same selectors — the statistic swings by 0.63 of R² purely with the comparand.
It is not identified without one, which reaches idea 398's open question from a new direction.

## Q3 — does the pool's sign explain the selector's sign?
Against a **fixed** comparand, overwhelmingly yes and vacuously so: sign agreement 0.90–0.99,
`|pool| > |lift|` in 78–99% of rows. Against the pool's **own control**, the shared term is
differenced out and it collapses: agreement 0.53–0.72, pool decides 16–50%.

## Q4/Q6 — the residual, and PROTOCOL rule 8 (IS ≤ 2016-12-31 fitted, 2017–2026 read once)
36 walk-forward cells per selector (3 panels × 4 dial families × 3 rungs), d(OOS Sharpe):

| selector | IS lift | OOS lift | t | vs do-nothing | t | vs RULES v2 | vs RULES v1 | vs SPY |
|---|---|---|---|---|---|---|---|---|
| K_Sharpe | +0.0706 | +0.0075 | +0.52 | **−0.0312** | −1.53 | −0.0312 | +0.3597 | +0.0715 |
| K_CAGR | +0.0591 | +0.0027 | +0.21 | **−0.0360** | −1.88 | −0.0360 | +0.3549 | +0.0667 |
| K_Sortino | +0.0696 | +0.0056 | +0.38 | **−0.0331** | −1.60 | −0.0331 | +0.3578 | +0.0696 |
| K_Calmar | +0.0648 | +0.0110 | +0.70 | **−0.0277** | −1.21 | −0.0277 | +0.3632 | +0.0750 |
| K_MaxDD | +0.0021 | +0.0177 | +1.04 | **−0.0210** | −1.27 | −0.0210 | +0.3699 | +0.0817 |
| K_Vol | −0.0392 | +0.0058 | +0.34 | **−0.0329** | −2.04 | −0.0329 | +0.3580 | +0.0698 |
| K_TO | +0.0138 | −0.0115 | −0.60 | **−0.0502** | −2.74 | −0.0502 | +0.3407 | +0.0525 |
| **K_MEDIAN** | +0.0101 | **+0.0205** | **+2.73** | **−0.0182** | −2.53 | −0.0182 | +0.3727 | +0.0845 |
| K_ANTI (control) | −0.0624 | −0.0471 | −2.65 | **−0.0858** | −4.11 | −0.0858 | +0.3051 | +0.0169 |

**All 9 selectors lose to do-nothing out of sample, and 6 of 9 have a POSITIVE mean OOS lift while
doing it.** The pool's own OOS mean sits **−0.0387** below the do-nothing control (t −3.56,
negative in 22 of 36 pools) and no selector's lift covers that deficit. This is idea 196's exact
shape (+lift over RANDOM, −delta vs do-nothing) at 36 cells per selector rather than one.

The only selector with a reliably positive OOS lift is **K_MEDIAN — the one that refuses to
optimise** (+0.0205, t +2.73, 28/36 wins) — and it loses to do-nothing anyway.

## Three further readings
1. **The comparand is worth up to 0.9280 of Sharpe and `lift` is worth 0.000e+00 of it.** The same
   pick publishes at −0.031 vs the live book, +0.072 vs SPY and +0.360 vs RULES v1. Everything
   contested in a published selector claim lives in the pool term.
2. **`lift` on CAGR is an exposure reading.** On the GROSS dial every selector's OOS-Sharpe lift is
   ±0.0012 (Sharpe is gross-invariant, idea 311) while its OOS-CAGR lift is the family's largest
   (±0.0356). A positive CAGR lift over a gross-scalar pool measures leverage, not skill.
3. **IS lift RANKS but does not DELIVER, and even the ranking is family-specific.** Pooled
   slope(OOS lift ~ IS lift) +0.4665 (t +6.87), but mean OOS lift is +0.0074 (t +1.39); per family
   the slope FLIPS: GROSS −0.580, WIDTH −0.564, CADENCE +0.568, GATE +0.984.
4. **Idea 205's column is causal on dial pools** (independent corroboration by a different route):
   `pool_OOS ~ pool_IS` over 36 pools gives R² 0.9125, slope +1.153, **sign agreement 100%** —
   against lane B's 86.1% on the overlay corpus. The column's causality is a property of the pool
   family, not a constant.

## KEEP paths (PROTOCOL 4a / 4b) — scored because PROTOCOL requires it, nothing promoted
| scope | rung | n | 4a vs v2 | 4b full | 4b OOS | BOTH |
|---|---|---|---|---|---|---|
| corpus-B arms | 0 / 10 / 25 bps | 69 | 1 / 1 / 1 | 7 / 7 / 4 | 8 / 7 / 5 | **0 / 0 / 0** |
| walk-forward picks | 0 / 10 / 25 bps | 108 | 3 / 3 / 3 | 12 / 12 / 8 | 12 / 8 / 8 | **0 / 0 / 0** |

Six arms clear 4b full *and* OOS at 10 bps (u56 g=1.000, u56 n=20, u56 n=40, u56 gate=vol60, broad
n=80, broad gate=vol60); all are restatements of the record's standing gross/width ladder passes in
the same book form idea 423 priced, none clears 4a, and **no arm and no pick clears both paths at
any rung.** 4b binding bar over the 207 arm-rows: CAGR 106, H2 38, H1 36, DD 27 (OOS: CAGR 107,
H2 69, DD 21, H1 10).

## Prediction scorecard (pre-registered)
- P1 the regression is an identity (|slope−1|<0.35 for >90% of rows) — **REJECTED as written**;
  the split is the finding (0.705 fixed-comparand vs 0.282 own-control).
- P2 sign agreement > 70% — **CONFIRMED** (mean 0.750, range 0.534–0.994).
- P3 no selector's mean lift reliably > 0 — **REJECTED**, by exactly one selector, K_MEDIAN.
  Power check passes: K_ANTI −0.0471, t −2.65.
- P4 `lift` invariant to the comparand — **CONFIRMED** at 0.000e+00.
- P5 IS lift does not predict OOS lift — **REJECTED** (slope +0.4665, t +6.87), but the level is
  not delivered and the slope flips sign by family.

## What PROTOCOL should take from this (proposal only; no clause is changed here)
Publishing `pool` beside a selector claim (idea 205's ADOPT-as-reporting) is not enough, because
`sel_d` and `pool` share the comparand and move together by construction. The decision-relevant
number is `lift = M(pick) − mean_P M(a)`, which is invariant to the comparand at machine precision
and is the only part a selector can affect. **A selector claim should quote `lift` and the pool's
`mean − control`, not `sel_d` alone.** On this evidence `lift` is ~0 for every optimising selector
and the pool's deficit to do-nothing is what every published "selection helps" sentence is
actually reporting.

## Caveats carried
Survivorship (idea 54) on all three panels — every level is flattered, every statistic quoted here
is a paired within-panel contrast. 36 corpus-B and 98 corpus-A pools are not that many independent
observations (books and arms overlap heavily inside a panel; corpus A double-counts P_ALL against
P_S1); per-panel, per-family and per-rung breakdowns are in the console and CSVs. Corpus A is read
at face value from a committed grid: it is idea 205's poolable population, not a census of the
record's prose. On corpus B the do-nothing arm of all four families **is** RULES v2 by construction
(max |sel_d(C_CONTROL) − sel_d(C_V2)| = 0.000e+00), so corpus B has two distinct comparands, not
three. t+1 execution, PROTOCOL's 10 bps rung reported alongside 0 and 25.

Files: `.console.txt`, `.gridB.csv` (207 arm-rows), `.claims.csv` (7,660), `.regression.csv`,
`.lift.csv`, `.walkforward.csv` (324), `.keeppaths.csv`.
