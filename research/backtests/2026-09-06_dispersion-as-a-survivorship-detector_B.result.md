# Idea 83 — dispersion-as-a-survivorship-detector (lane B, 2026-09-06)

**Verdict: ANSWERED, and the QUEUE's hypothesis is REFUTED. The premise holds — a wider
draw really is a more winning draw (corr(sd, W) = +0.567) — but the inference drawn from
it does not: dispersion keeps 62% of its univariate R² and a t of +5.87 once each name's
own full-sample return is regressed out, so it is NOT a survivorship thermometer and
idea 78's test C is NOT contaminated in the way supposed. KILL for the thermometer
reading. No RULES change, no new KEEP-candidate, no memo. Nothing in RULES.md, scan.py,
bot.py or baseline.py touched.**

Script `research/backtests/2026-09-06_dispersion-as-a-survivorship-detector_B.py` ·
console `…_B.console.txt` · CSVs `.draws` `.regressions` `.mechanism` `.cells` `.walkforward`

## Reproduction gate (run before any new number was read)

Idea 78's seeds, draws, panel, gate, gross, cadence and costs were **imported unchanged**,
so the analysis sits on the table it analyses. All 150 sub-panels were re-drawn from
`SEED_B + k` and all 450 books re-run:

| check | this run | published |
|---|---|---|
| U56/CAND20 | 12.6597% / **1.09214** / −18.3083%, halves 1.08828/1.10155 | 12.7% / 1.092–1.093 / −18.3%, halves 1.088/1.102–1.103 |
| U56/RULES v1 | 6.4531% / **0.66418** / −13.8278% | 6.5% / 0.664–0.666 / −13.8% |
| all 17 numeric columns of idea 78's `gridB.csv`, 300 rows | max abs diff **8.3e-17 … 7.1e-15** | — |
| `f4a` / `f4b` verdict strings | identical in **300 / 300** rows | — |

**REPRODUCTION PASS.** Window 2009-01-13 → 2026-09-04 (4,439 days). SPY 15.23% / 0.889 /
−33.72%, halves 0.957/0.834, OOS 0.882. RULES v1 on B136 6.39% / 0.635 / −21.19%, OOS 0.576.
4b bars: MaxDD ≤ 20.23%, CAGR ≥ 10.66%, H1 > 0.957, H2 > 0.834, OOS Sharpe > 0.882.

## The control, and a defect fixed on the way

`W` = the mean **annualised** log return of a draw's own constituent names — name returns
only, no book, no gate, no ranking, no costs. Annualised over each name's **own listed
history**, because 12 of B136's 136 columns list after the window opens (ABBV ANET AVGO
META NOW PANW PLTR TSLA UBER XLC XLRE ZTS; MMC is empty in the cache) and they contain the
panel's largest winners — PLTR is the panel's best name at +0.491/yr. A common-window `W`
silently drops all 13, i.e. under-measures winner-content on exactly the names that
manufacture it. Both are reported; the common-window variant `W_cw` correlates +1.0000 with
the primary on the 123 names where both exist. `W_max` (the draw's single best name) is
carried as a second control because a 20-name momentum book can be carried by one name.
Panel-wide: mean 0.1472 (15.85%/yr), sd 0.0876, min UNG −0.316, max PLTR +0.491;
corr(full, IS) over names +0.860.

## 1. The premise is TRUE (T2)

A wider draw is a more winning draw, in every cell:

| | pooled | k=20 | k=40 | k=80 |
|---|---|---|---|---|
| Spearman(sd, W) | **+0.473** | +0.495 | +0.442 | +0.661 |
| Pearson(sd, W) | **+0.567** | +0.593 | +0.495 | +0.613 |
| Spearman(sd, W_max) | +0.522 | +0.424 | +0.477 | +0.390 |
| Spearman(sd, W_IS) | +0.302 | +0.327 | +0.219 | +0.566 |
| Spearman(W, CAND-20 Sharpe) | +0.324 | +0.429 | +0.225 | +0.414 |

and `W` on its own predicts draw Sharpe at R² 0.155, t +5.22. The queue's mechanism is
real and measurable. Nothing here is in dispute.

## 2. The inference is FALSE (T3 — the decisive test)

Pre-registered bar, written before the number was read: *if dispersion is a thermometer,
partial R²(Sharpe | W) falls below a third of the univariate R² and |t| falls below 2.*

**n = 20, pooled over all 150 draws:**

| y | R²(sd) | t | R²(W) | t | **pR²(sd \| W)** | **t** | kill | t on W given sd | sd \| W, W_max |
|---|---|---|---|---|---|---|---|---|---|
| CAND-20 Sharpe | 0.3062 | +8.08 | 0.1554 | +5.22 | **0.1899** | **+5.87** | **0.620** | +1.43 | **+6.92** |
| EWall Sharpe | 0.3437 | +8.80 | 0.1834 | +5.76 | **0.2129** | **+6.30** | **0.619** | +1.76 | +6.38 |
| ranking premium | 0.0620 | −3.13 | 0.0379 | −2.41 | 0.0295 | −2.11 | 0.475 | −0.81 | −1.32 |

**The bar is missed on both legs and in every cell.** `kill` never falls below 0.36 for a
book Sharpe (range 0.50–0.87 at n=20), against a bar of 0.33; `t_sd|W` is above 2 in
**3 of 3** k-cells for CAND-20, **3 of 3** for EWall, and 2 of 3 for CAND-5 — with the
candidate count held **exactly** at k in each. Adding `W_max` as a second control makes sd
*stronger*, not weaker (+6.92 vs +5.87). The common-window control gives the same answer
(pR² 0.2147, t +6.34).

**And the conditioning runs the other way.** With sd in the regression, `W`'s own t falls
from +5.22 to **+1.43** and drops under 2 in 6 of the 8 CAND cells. Dispersion explains
winner-content better than winner-content explains dispersion. Roughly **38%** of
dispersion's univariate R² is winner-content; 62% is not.

The queue was right about the *premium* — sd's relationship to the ranking gap is
0.062 → 0.030 and never mattered. But it was already near-nil before the control, so
nothing there was contaminated either.

## 3. Rule 8 — the thermometer's own prediction, tested (2009-16 fit, 2017-26 read once)

If dispersion were a thermometer, the residualised column S5 would keep whatever OOS skill
the raw column S2 has. It does not. SPY OOS 0.882; do-nothing (full B136 CAND-20) OOS
12.49% / **0.892** / −20.05%.

| selector | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | regret vs do-nothing | z within cell | 4b |
|---|---|---|---|---|---|---|---|
| S0 do-nothing | — | 12.49% | 0.892 | −20.1% | — | — | H2 |
| S1 IS-Sharpe argmax | k20 d19 | 8.37% | 1.105 | −10.5% | +0.213 | +0.97 | CAGR |
| S2 DISPERSION (max IS sd) | k20 d39 | 9.03% | **1.184** | −9.4% | **+0.292** | +1.66 | CAGR |
| S3 COUNT (max IS n_elig) | k80 d26 | 12.00% | 0.953 | −19.6% | +0.061 | +0.22 | **—** |
| **S5 RESID-DISP (sd \| W_IS)** | k20 d16 | 5.99% | 0.956 | −12.7% | **+0.064** | −0.31 | H2,CAGR |
| **S6 WINNERNESS (max IS W)** | k20 d12 | 6.06% | **0.775** | −12.0% | **−0.117** | −1.86 | H2,OOS,CAGR |
| S4 random sub-panel | k40 d35 | 10.30% | 0.984 | −17.6% | +0.092 | −0.11 | CAGR |

Two readings, both against the thermometer. **S5 keeps 22% of S2's edge** and lands
*below* its own cell mean (z −0.31) — stripping winner-content out of dispersion destroys
the selector rather than purifying it. **S6, the pure survivorship proxy, is the only
selector in the table that loses to doing nothing** (−0.117, z −1.86): pointing a selector
straight at winner-content is the worst thing available, which is what a genuine thermometer
would *not* look like. Selector-input skill over the 150 draws (Spearman with OOS Sharpe):
IS Sharpe +0.217, IS sd **+0.194**, IS sd|W_IS +0.232, IS W_IS **+0.074**, IS n_elig −0.262.

The honest caveat on the other side: S2's +0.292 is inside its own cell's noise (z +1.66,
cell sd 0.116) and **S2 still fails 4b on the CAGR floor**, as do S1, S4, S5 and S6. The
only 4b pass is S3's, which idea 78 already showed is its cell's 46% base rate. **No
selector here is promotable**; the run distinguishes hypotheses, it does not produce a rule.

## 4. Both KEEP paths — all 450 books

| book | N | 4a | 4b |
|---|---|---|---|
| CAND-20 | 150 | 146 | 40 |
| CAND-5 | 150 | 32 | 2 |
| EWall | 150 | 98 | 45 |
| **total** | **450** | **276** | **87** |

4b failing-bar census: H2 233, DD 203, CAGR 194, OOS 176, H1 121, pass 87. Every pass is a
random sub-panel of B136 already inside idea 78's published grid — nothing new is
proposed, and a random k=80 sub-panel clearing 4b at a **46%** base rate is a fact about
the bar, not about the book (idea 78's finding, reproduced). The 4b verdict itself
separates on **sd** (Welch t +4.14 at n=20) about twice as strongly as on **W** (+2.28),
which is the same asymmetry as §2 at the verdict level.

## What this establishes

1. **Dispersion is not a survivorship thermometer.** 62% of its univariate R² against draw
   Sharpe survives regressing out each name's own realised return, at t +5.87, in 3 of 3
   count-matched cells. The pre-registered bar was missed on both legs.
2. **Idea 78's test C is clean on this axis.** Its dispersion columns may be read as
   published; the contamination the queue suspected is not there. Idea 54's survivorship
   concern is untouched by this and stands — it is about the *panel*, not about this column.
3. **The confound points the other way.** Conditioning on dispersion halves winner-content's
   own t; conditioning on winner-content leaves dispersion's largely intact.
4. **Nothing is promotable.** No new KEEP-candidate, no memo, no RULES wording proposed.

## Limitations, stated

- **Survivorship is the premise under test, not a caveat to it.** `universe_broad.json` is
  current constituents and one-directional; this run measures how much of a published
  diagnostic that bias accounts for and cannot remove it. A draw's `W` is the realised
  return of names *already known to have survived*, so `W` under-states true winner-content
  and the control is conservative — which makes a **surviving** sd coefficient the weaker
  claim and a *killed* one the stronger. The result went the surviving way, so this
  limitation cuts against the finding and is stated rather than argued around.
- `W` is one scalar per draw. A draw is a set of 20–80 names; mean and max are two summaries
  of it, not the whole composition. A name-by-name fixed-effect design would be stronger and
  is not run here.
- Only 150 draws, 50 per k, on one panel (B136) — idea 78's grid, imported so the
  reproduction gate could bind. Nothing is claimed for other panels.
- Two tuned parameters (k, n), both idea 78's; **no parameter of this run is tuned**, and
  all 6 (k, n) cells and all 450 books are reported.
- The gate is inverted on small panels (ideas 39/49) and idea 128's shallow IS drawdown
  window biases every selector in §3 identically.
