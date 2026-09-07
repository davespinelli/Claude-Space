# Idea 358 — does the EXIT buffer stay name-count NEUTRAL under a flat cap?

**Cloud lane, 2026-09-07. Verdict: KILL of the queue's premise — idea 349's exit reading is NOT a
cap-convention artefact. The +0.058 mean marginal Sharpe and the 15/15 positive count SURVIVE
under both alternative cap rules (FLAT +0.0572 15/15, UNCAP +0.0444 15/15), and the OOS column
gets STRONGER, not weaker (KT +0.0387 13/15 → FLAT +0.0426 15/15 → UNCAP +0.0443 15/15). What is
a cap-convention property is the NAME-COUNT NEUTRALITY alone: drop the cap and the same buffer
adds +7.67 names (spearman(x, names) +0.956). Rules unchanged. No new KEEP-candidate — the one 4b
cell that leads the grid is a bit-exact reproduction of idea 349's own committed row.**

Script `2026-09-07_does-the-EXIT-buffer-stay-name-count-NEUTRAL-under-a-flat-cap_cloud.py`;
console `.console.txt`; data `.grid.csv` (54 cells x 3 rungs = 162 reported rows), `.ctx.csv`,
`.marginals.csv`, `.match.csv`, `.walkforward.csv`. Runtime 51 s.

## Pre-registration

Book fixed at idea 349/331's convention and never tuned: top-20 eligible by the RULES v1
composite with the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60), NORM
weights `w_i = g/k` at g = 0.75, next-day execution, **weekly**, **entry buffer fixed at e = 0**.

Exactly two tuned parameters — the **cap rule** and the **exit buffer x**:

| cap rule | slot cap each rebalance | |
|---|---|---|
| `KT` | `k_t = |{rank <= n}|` | idea 349/331's convention — a drifter occupies a top-n slot |
| `FLAT` | `n` | the queue's literal ask |
| `UNCAP` | none | drifters held IN ADDITION to the fresh top-n |

`x in {0, 5, 10, 20, 40, 80}`; `x = 0` is the plain hard rank cut under every cap rule.
3 x 6 = **18 cells x panel {U56, B136, SMALL439} x rung {0, 10, 25} bps = 162 rows, all printed
and committed**. Panel and rung are REPORTED axes, not tuned choices.

`UNCAP` was added because — see [B0] — the queue's FLAT cap turns out to be very nearly the same
cap as `k_t`, so on its own it cannot answer the question being asked. `UNCAP` is the only
convention under which a drifter is not absorbed, i.e. the only one under which the neutrality
CAN break. It costs no third parameter: the cap rule is one dial with three levels.

## Reproduction gates — 5 of 5, before any new number was read

| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` (returns, turnover) | max\|dr\| **0.000e+00**, max\|dturn\| **0.000e+00** |
| G2 derived rung `r(25) = r(0) - turnover*25/1e4` vs `backtest(cost_bps=25)` | max\|d\| **0.000e+00** |
| G3 `sel_x(x=0)` nests `sel_hard(20)` | KT **0**, UNCAP **0** disagreements on 975/975/870 weekly rebalance days; FLAT 5/7/0, every one on a tie-overhang day (asserted) |
| G4 `sel_x(cap=KT, x)` == idea 349's own `sel_ex(e=0, x)`, imported from its committed script | **0 disagreements** at all 6 x on all 3 panels |
| G5 KT rows vs idea 349's committed `.grid.csv` (e=0) | \|dSharpe\|, \|dCAGR\|, \|dMaxDD\|, \|dturn\|, \|dOOS\|, \|dnames\| all **< 1e-12**, 18/18 cells |

G5 is what makes the KT column of this run idea 349's published column, not a re-estimate of it:
the KT summary row below (**+0.0577, 15/15, spearman(x, names) 0.000**) is its published reading
to four decimals.

## [B0] The FLAT cap is not the different cap the queue thought it was

Holdings = `min(cap, |holdable|)`, and `|holdable| <= n_elig`, so `cap_KT = |{r<=n}|` and
`cap_FLAT = n` coincide except where **rank ties** move the count off n (average-rank convention:
three names tied at positions 19-21 all get rank 20, so `|{r<=20}| = 21`; two tied at 20-21 get
20.5, so `|{r<=20}| = 19`). Cap-rule SEED days — ties with names to spare — are **88/975 (U56),
92/975 (B136), 14/870 (SMALL439)**; only 5/7/0 of them are overhangs.

At `x = 0` the book is memoryless and that is the whole difference (5/7/0 differing rebalances).
At `x > 0` the buffer **carries a divergence forward**, so a handful of tie days becomes 154-664
differing rebalances and up to **0.037 of Sharpe** (B136, x=40). That is a path artefact of the
tie convention, not a mechanism — but it is large enough that **any published band cell is
reproducible only under the cap convention it was run with**, which is worth a line in PROTOCOL.

## [B1] The queue's actual question: does the exit reading survive?

Marginal dSharpe against the `x = 0` hard cut, 10 bps, pooled over the three panels (15 cells):

| cap rule | mean dSharpe | positive | mean dOOS | OOS positive | mean dnames | spearman(x, names) |
|---|---|---|---|---|---|---|
| `KT` (idea 349's) | **+0.0577** | **15/15** | +0.0387 | 13/15 | **+0.000** | **0.000** (constant) |
| `FLAT` (the ask) | **+0.0572** | **15/15** | +0.0426 | **15/15** | +0.048 | 0.113 |
| `UNCAP` | **+0.0444** | **15/15** | **+0.0443** | **15/15** | **+7.673** | **+0.956** |

Per panel, mean dSharpe: U56 +0.045/+0.034/+0.032, B136 +0.053/+0.062/+0.041, SMALL439
+0.076/+0.076/+0.061 (KT/FLAT/UNCAP) — **5/5 positive in all nine panel-by-cap blocks**.
`spearman(x, turnover)` is **-0.562 under all three caps**: the buffer is a turnover dial
whatever the cap. The neutrality itself is the only thing the cap owns.

## [B2] Head to head, UNCAP minus KT at the same x

UNCAP beats KT on full-sample Sharpe **5/15** (mean **-0.0132**) and on OOS Sharpe **9/15**
(mean **+0.0057**), while holding **+7.67 more names** and trading **+1.32x/yr more**. Dropping
the cap therefore buys nothing and costs CAGR at every point (-0.24% to -1.94%).

## [C] Is the UNCAP margin just width? No — the opposite of the entry dial

Each UNCAP cell against the plain top-n' hard cut whose mean holdings is nearest to it (a derived
comparand, not a tuned parameter): UNCAP beats its **holdings-matched** hard cut **14/15**
(mean **+0.0491**), OOS **11/15** (mean **+0.0283**), at **9.43 vs 13.89x/yr** turnover. So even
in the convention where the exit buffer DOES widen the book, the width is not what pays — which
is exactly the reverse of idea 349's finding for the entry buffer, whose margin was width.

## [D] Rule 8 walk-forward (x chosen on IS Sharpe <= 2016-12-31, 2017+ read once)

Mean OOS Sharpe over the 27 (panel x cap x rung) cells: **KT 0.8761, UNCAP 0.8580, FLAT 0.8559**
— the parent's cap wins the menu. The IS chooser beats the do-nothing `x = 0` control **20/27**
(mean **+0.0538**), one of the record's rarer wins for selection. The cap rule changes the pick in
**2 of 9** panel-rung cells. OOS Sharpe > SPY's 0.882 in **16/27**; > RULES v2 in **3/27**
(all three SMALL439 cells, where the live book's OOS is 0.568).

Best walk-forward cell, U56 / KT / 10 bps, x* = 40: OOS Sharpe **1.189**, CAGR **14.34%**,
MaxDD **-15.27%**, against SPY OOS 0.882 / 15.45% / -33.72% and RULES v2 OOS 1.285 / 9.53% /
-12.05%. Worst, SMALL439 / UNCAP / 25 bps: OOS 0.422, CAGR 5.66%, MaxDD -35.90%.

## KEEP paths, all 162 rows

**4a: 0/54 at every rung** (the idea-136 pathology — the live book's -12.05% drawdown is
unreachable for a 20-name equity book). **4b: 29/54 at 0 bps, 20/54 at 10, 15/54 at 25**, by cap
9/6/5 (KT), 9/7/5 (FLAT), 11/7/5 (UNCAP). Every 10-bps passer but two is on U56.

The grid leader is **U56 / KT / x=40**: 12.73% CAGR, Sharpe 1.127, MaxDD -15.27%, halves
1.183/1.089, OOS 1.189, c* = 46 bps. It is not a new candidate — G5 asserts it equal to idea
349's committed `e=0, x=40` row at < 1e-12. The best genuinely NEW forms, FLAT x=40 (1.100, OOS
1.165, c* 34) and UNCAP x=40 (1.101, OOS 1.150, c* 27), are **dominated by their KT twin on
Sharpe, OOS and breakeven**, so neither is promotable. Memo written for the record.

## Caveats

(1) All three panels are current-constituent lists — **SURVIVORSHIP** — which flatters every
momentum book; CAGR levels are optimistic, the x- and cap-DIFFERENCES much less so. (2) SMALL439
starts 2010-01-04 (eval from 2011-01-13), so its halves are not the same calendar halves as
U56/B136, and the 44 tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` are dropped
before anything runs. (3) rule 8's IS window is 2008-2016 on U56/B136 but effectively 2011-2016
on SMALL439. (4) 4a is judged against RULES v2 as `baseline.compare` does.
