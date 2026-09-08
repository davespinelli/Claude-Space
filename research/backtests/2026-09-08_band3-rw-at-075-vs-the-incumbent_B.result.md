# Idea 238 — band3-rw-at-075-vs-the-incumbent (lane B, 2026-09-08)

**Verdict: KILL of the queue's question as posed — NEITHER book may be called the safer
book — plus a CORRECTION to idea 154's published margin gap, which is 80% a gross-matching
artefact.** No RULES change, no KEEP: both contenders pass 4a in **0 of 80** grid points
and neither beats the live RULES v2 book out of sample. `RULES.md`, `scan.py`, `bot.py`,
`baseline.py` and `PROTOCOL.md` untouched.

Script `research/backtests/2026-09-08_band3-rw-at-075-vs-the-incumbent_B.py` (21 s).
Outputs: `.console.txt`, `.grid.csv` (480 rows), `.cadenceswing.csv`, `.lagprice.csv`,
`.walkforward.csv`.

## Design

Contenders fixed in advance: `EWall + band3-rw` vs the incumbent `EWall + vol60-dg`, both
at gross 0.75, weekly. Grid = gate {band3, vol60} × conv {rw, dg} — **exactly two tuned
parameters** — plus a NOGATE always-invested control, run over cadence {D, W, M, Q} ×
lag {1d, 1w} × cost {5,10,15,20,25} bps on **both** large-cap panels (u56, B136), both
primary. All 480 points reported. Costs are analytic from one zero-cost run per
(book, panel, cadence, lag); the mirrors `band3-dg` / `vol60-rw` are carried so neither
contender borrows the other convention's hindsight.

**Reproduction gates, all binding, run before any new number:**

| gate | result |
|---|---|
| [a] `fast_bt` + analytic cost vs `engine.backtest` (both panels, W/1d/10 bps) | max\|diff\| **0.000e+00** |
| [b] `band3-rw` u56 W/1d/10 bps vs idea 94/97 | 12.25%/1.1609/−17.71% **PASS** |
| [b] `vol60-dg` u56 W/1d/10 bps vs idea 97 | 11.59%/1.1333/−16.88% **PASS** |
| [c] `band3-rw` broad dd-margin vs idea 154's +0.0170 | **+0.0170 PASS** |
| [c] `vol60-dg` broad dd-margin vs idea 154's +0.0083 | **+0.0153 MISMATCH** → diagnosed below |

## A gross-matching problem found in flight

Gate [c] fails on one side only, and the cause is not arithmetic. Under `rw` the gross is
pinned, so nominal 0.75 **is** realised 0.75; under `dg` it floats down with the gate, so
nominal 0.75 realises only **0.7230** on broad. Idea 154 matched the two books on
**realised** gross, i.e. it ran the incumbent at a nominal **0.7780**. Re-running the
incumbent at that nominal reproduces idea 154's quoted row:

| reading | broad, W/1d/10 bps | dd-margin |
|---|---|---|
| `band3-rw` nominal = realised 0.7500 | 11.73% / 1.0690 / −18.53% | **+0.0170** (published +0.0170) |
| `vol60-dg` nominal 0.7500 → realised 0.7230 | 12.36% / 1.1381 / −18.70% | **+0.0153** |
| `vol60-dg-rg75` nominal 0.7780 → realised 0.7500 | 12.83% / 1.1381 / −19.36% | **+0.0087** (published +0.0083) |

So idea 154's headline gap of **0.0087** is **0.0017** once the two books are matched on
nominal gross — **80% of the gap is the matching convention, not the gate.** Both matchings
are defensible; the run therefore carries **both** and requires every verdict below to hold
under each. The rematched arm's nominal is pinned by an identity, not chosen for
performance, and is excluded from the rule-8 chooser pool for that reason.

## [BAR-65] cadence insensitivity — the incumbent wins the swing, both books fail the bar

SWING = max − min full-sample Sharpe over {D, W, M, Q} within a (panel, lag, cost) cell.

| book | mean SWING | worst | best |
|---|---|---|---|
| `vol60-dg-rg75` | **0.0282** | 0.0551 | 0.0085 |
| `vol60-dg` | **0.0283** | 0.0559 | 0.0085 |
| NOGATE (control) | 0.0325 | 0.0564 | 0.0137 |
| `vol60-rw` | 0.0356 | 0.0804 | 0.0046 |
| `band3-rw` | **0.0642** | 0.1166 | 0.0290 |
| `band3-dg` | 0.1593 | 0.2154 | 0.0846 |

`band3-rw` has the smaller swing in **1 of 20** (panel, lag, cost) cells under **both**
gross matchings — the incumbent is the cadence-stabler book by better than 2×, and
`band3-rw` is the only contender worse than the do-nothing NOGATE control.

The bar's second clause is **degenerate for every book**, independently reproducing idea
65's own KILL: of the cells where a book passes 4b at the incumbent weekly cadence, the
number that keep the verdict at **all** of D/M/Q is **0 of 15** for `band3-rw`, **0 of 15**
for `vol60-dg`, **0 of 15** for `vol60-dg-rg75`, and 0 of 5 for `vol60-rw`. So neither
contender passes BAR-65, and `band3-rw` additionally loses its comparative clause 1–19.

## [BAR-45] execution lag — the ordering REVERSES

1w = 4 extra trading days of staleness on top of PROTOCOL's t+1. Mean over the 40
(panel, cadence, cost) cells:

| book | dCAGR/yr | dSharpe | dMaxDD (worst) | 4b passes lost |
|---|---|---|---|---|
| `band3-rw` | +0.263% | +0.0083 | **−0.85%** (−2.87%) | **10 of 24** |
| `vol60-dg` | −0.186% | −0.0261 | −1.39% (−3.34%) | **5 of 20** |
| `vol60-dg-rg75` | −0.195% | −0.0261 | −1.43% (−3.46%) | 10 of 20 |
| NOGATE placebo | −0.008% | −0.0005 | **−0.00%** | 0 of 0 |

`band3-rw` takes the **shallower** drawdown deepening in **30 of 40** cells under both
matchings — the sub-clause where idea 154's ordering does survive — but it **loses more of
its own 4b verdicts to the week of staleness** than the nominally-matched incumbent (41.7%
vs 25.0%). Neither retains its verdict in every cell, so both **FAIL** BAR-45. The placebo
confirms the effect is gate timing, not a return tax.

## Both KEEP paths, all 480 points

| book | 4a | 4b | u56 4b | B136 4b | cross-universe 4b |
|---|---|---|---|---|---|
| `band3-rw` | **0/80** | 39/80 | 25/40 | 14/40 | **14/40** |
| `vol60-dg` | **0/80** | 35/80 | 20/40 | 15/40 | **15/40** |
| `vol60-dg-rg75` | **0/80** | 30/80 | 20/40 | 10/40 | 10/40 |
| `vol60-rw` | 0/80 | 15/80 | 15/40 | 0/40 | 0/40 |
| `band3-dg` | 2/80 | 0/80 | 0/40 | 0/40 | 0/40 |
| NOGATE | 0/80 | 0/80 | 0/40 | 0/40 | 0/40 |

4a is empty for both contenders at every cadence, lag and rung — idea 136's pathology
again (nothing beats the live low-vol book on drawdown). The 4b footprints are within
**one cell** of each other and **the ordering flips with the gross matching**: `band3-rw`
leads 39–35 on totals but trails 14–15 cross-universe, and leads 39–30 / 14–10 against the
realised-gross reading. First-failing bar over all books: DD 295, CAGR 81, H2 10, OOS 2.

At PROTOCOL's own cell (W, 1d, 10 bps) both contenders pass 4b on both panels — the
"6 of 6 large-cap cells" shape the queue quoted is confirmed — and neither passes 4a.

## Rule 8 walk-forward (IS 2009–2016, OOS 2017–2026 read once, 40 cells per panel)

The IS chooser between the four (gate, conv) books is **panel-dependent**: it takes
`band3-rw` in 19/40 u56 cells and `vol60-dg` in **37/40** B136 cells.

| | u56 | B136 |
|---|---|---|
| mean OOS Sharpe `band3-rw` | **1.1523** | 1.0653 |
| mean OOS Sharpe `vol60-dg` | 1.1271 | **1.0710** |
| mean OOS Sharpe IS-Sharpe pick | 1.1455 | 1.0710 |
| mean OOS CAGR `band3-rw` / `vol60-dg` | **13.19%** / 11.89% | **12.32%** / 11.85% |
| mean OOS MaxDD `band3-rw` / `vol60-dg` | **−19.50%** / −19.62% | **−21.78%** / −21.93% |
| SPY OOS | 15.45% / 0.8820 / −33.72% | same |
| RULES v2 OOS Sharpe | **1.2851** | **1.1185** |

Both books beat SPY's OOS Sharpe in **40/40** cells on both panels; **neither beats the
live RULES v2 book** (`band3-rw` 0/40 on both panels; `vol60-dg` 0/40 u56, 6/40 B136).
Head to head OOS, `band3-rw` wins MaxDD in 30/40 (u56) and 34/40 (B136) and CAGR in 40/40
(u56) / 33/40 (B136), but Sharpe in only 23/40 and 25/40 — the same split the two bars
show.

## What survives

1. **Neither book is "the safer book."** `band3-rw` is the shallower-drawdown book (OOS
   MaxDD 30/40 and 34/40; lag deepening 30/40, both matchings); the incumbent is the
   cadence-stabler book (19/20, both matchings). The two bars the queue named point in
   opposite directions, so idea 154's ordering stands as a **single-cadence, single-lag**
   reading only and must be quoted that way.
2. **Idea 154's margin gap needs a matching stamp.** +0.0170 vs +0.0083 is a
   *realised*-gross comparison; at matched *nominal* gross it is +0.0170 vs +0.0153. Any
   future quote of a `dg`-vs-`rw` margin should name which gross is held fixed.
3. **Idea 65's bar is degenerate here too** — 0 of 45 weekly 4b passes survive D/M/Q across
   the three readings — a third independent reproduction of its own KILL.

SURVIVORSHIP: both universe lists are current constituents, so absolute CAGRs are
optimistic. Every comparison holds names, days, base book and gross fixed and moves only
cadence, lag, cost, the gate and the matching convention.
