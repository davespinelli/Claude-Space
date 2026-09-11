# Idea 562 — price the ENGINE DRIFT leg on every published arm-minus-arm decomposition
**Lane B, 2026-09-11.** Script: `2026-09-11_price-the-ENGINE-DRIFT-leg-on-every-published-arm-minus-arm-decomposition_B.py`
Verdict: **ANSWERED / KILL of the "a published pp-leg is content" reading at the small end — no KEEP.**

## What was measured
`engine.backtest` holds a TARGET only on rebalance days; in between it renormalises each book by
ITS OWN total (`cur = growth / tot`). Two arms holding a shared name at the *same target* therefore
hold it at *different weights* between rebalances. That residue is an engine artefact, not a
property of either arm. Using idea 559's own pair (MA-THRESH vs MOM-D at exact daily depth), the
shared-name leg was split exactly into

* `DRIFT_pp` — shared names whose targets are EQUAL (|T_A − T_B| ≤ 1e-15): pure renormalisation, and
* `MRES_pp` — shared names whose targets differ: the depth-match residual,

with `ADD + DROP + BOTH = arith` and `BOTH = DRIFT + MRES`. Grid: 3 panels × 5 theta ×
2 constructions × 4 cadences = 120 arm pairs, 480 books (2 arms × 2 handlings), gross pinned at the
live 0.75, 10 bps (0 and 25 derived exactly and reported). 2 tuned params: **cadence × panel**.

## Gates (all pre-registered, all PASS)
| gate | what | result | bar |
|---|---|---|---|
| G0 | `run()` vs `engine.backtest` (returns, turnover AND the held-weight matrix) on 3 panels × D/W/Q | **0.000e+00** | 1e-12 |
| G1 | derived cost rung vs a fresh run at that rung | **0.000e+00** | 1e-15 |
| G2 | `DRIFT_pp` at cadence D over 60 splits | **0.000e+00** | exactly 0 |

G2 is structural, not empirical: at D the engine sets held == target on every bar, so the drift leg
is zero by construction. The residue that survives at D is the depth-match residual (max |MRES_pp|
**0.0042 pp/yr**, exact-match day share 0.9883) — **not** drift. This is the correct reading of idea
559's "EXACTLY 0 at cadence D".

## A. The drift floor
max |DRIFT_pp| (pp/yr), native handling, over all panels/theta/constructions:

| cadence | median | p90 | **max (the floor)** |
|---|---|---|---|
| D | 0.0000 | 0.0000 | **0.0000** |
| W | 0.0011 | 0.0071 | **0.0765** |
| M | 0.0027 | 0.0154 | **0.0579** |
| Q | 0.0058 | 0.0668 | **0.1374** |

Idea 559 published max **0.0766** pp/yr at cadence W on a 9-theta grid; this run's independent
5-theta grid reads **0.0765** — an unplanned cross-reproduction of the only number 559 quoted for
this channel. Drift is **92.2%** of the shared-name leg at W/M/Q (`|DRIFT| ≥ |MRES|` in 0.9222 of
splits), i.e. BOTH ≈ DRIFT once the match is daily.

The floor is a **construction** fact, not a panel fact: max |DRIFT_pp| over W/M/Q is **0.1374 under
RESPREAD vs 0.0164 under DEGROSS** (8.4×), because a de-grossed book divides by the panel count both
arms share, so the targets that drift apart are smaller. By panel the W floor runs U56 0.0765 /
B136 0.0095 / SMALL439 0.0101.

## B. The census — how many published legs are inside it
66 committed CSVs carry a pp/yr leg column; **41,441 published leg values**, 5 of them STRICT files
(carrying ADD/DROP/BOTH). Cadence is stated on the row for only **41.8%** of values; the rest are
read at the record's default cadence W.

* all values: **8,916 / 41,441 = 21.51%** inside their own (cadence, panel) floor
* **5.63% of all values are exactly 0.0** (degenerate arms — 559's QUANTILE-D cells, where the two
  books are identical); those are trivially inside at D, where the floor is exactly zero
* **nonzero values: 6,583 / 39,108 = 16.83%** inside — STRICT tier **9.98%**, WIDE tier 19.52%
* the leg the idea was aimed at is mostly safe: **nonzero `BOTH_pp` 96 / 1,485 = 6.46%** inside
* the alarm is concentrated in the *small* legs: `jensen_pp` 35.9%, `COST_pp` 34.3% inside; the big
  ones are clean — `DROP_pp` 0.84%, `net10_pp` 2.3%, `sel_geo_pp` 3.0%, `arith_pp` 3.2%, `ADD_pp` 4.7%
* by file, only 559's own `.legs.csv` has a majority of its BOTH values inside (274/486 = 56.4%);
  the record's other four STRICT files read 2.5–4.1%
* worst-case reading (every value judged against the widest floor, Q = 0.1374): STRICT 30.28% inside

## C. The book leg — is the drift channel worth capital?
Every book run twice: **DRIFT** (native) vs **RTT** (the same cadence targets restored daily, paying
10 bps on the extra turnover). 240 matched pairs.

* DRIFT beats RTT on full-sample Sharpe in **46.7%** of pairs, **median +0.0000**; on CAGR 32.1%,
  median +0.0000. RTT buys **1.10x/yr** of extra turnover = 0.11 pp/yr of cost at 10 bps.
* it is a cadence fact: median dSharpe 0.0000 (D, identical by construction) / −0.0006 (W) /
  −0.0005 (M) / **+0.0279 (Q)**; DRIFT wins 90–95% of Q pairs and 0% of SMALL439's W/M pairs.
* **but it flips KEEP verdicts at the knife-edge:** 3 of 240 books change a verdict on this axis
  (1× 4a, 2× 4b), and **all three are the 4b DD cap**: U56 −0.12/DEGROSS/M/MOM-D reads MaxDD
  −20.25% (DRIFT, fails the −20.23% cap) vs −20.12% (RTT, passes); U56 0.06/RESPREAD/M/MA-THRESH
  −20.41% vs −20.15%. A 0.13–0.26 pp drawdown difference, worth ~0.000 of Sharpe, decides the
  published 4b verdict.

## D. Both KEEP paths (all 480 books, 10 bps)
**4a 11/480, 4b 24/480, BOTH 0/480.** At 0 bps 32/28; at 25 bps 2/12. The 4b failing-bar histogram
is DD 168 / CAGR 57 / everything-fails 96. The 24 4b passers are MA-THRESH and MOM-D gate books on
U56/B136 at theta −0.12, 0.00 and 0.06 — the same arms, panels and thetas idea 563 ran one day
earlier on a 9-theta × 3-gross grid and declined. Nothing here is a new book; the drift/RTT axis
moves none of them except the two DD knife-edges above. **No KEEP-candidate, no memo.**

## E. Rule 8 (cadence, panel chosen on IS Sharpe alone; 2017+ read once)
40 selector cells (arm × construction × handling × theta), each picking one of 12 (cadence, panel)
points. Picks beat RULES v2 on OOS Sharpe **7/40**, beat SPY **39/40**, clear all OOS 4b legs
**2/40** (both are B136/−0.12/DEGROSS/W/MOM-D, the DRIFT and RTT twins of idea 563's own book).

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| rule-8 picks (mean of 40) | **12.19%** | **1.0879** | **−19.33%** |
| RULES v2 baseline (mean of the picked panels) | 8.62% | 1.1898 | −12.06% |
| SPY | 15.36% | 0.8778 | −33.72% |

Cadence picked Q 20 / M 16 / W 4; panel B136 23 / U56 17. Where the selector is free to choose the
handling it takes DRIFT in 170/240 cells (70.8%) and gains **+0.0093** of mean OOS Sharpe for it
(0.8879 vs 0.8786) — i.e. the IS window cannot distinguish the two either.

## Verdict
**KILL of the reading that a small published pp-leg carries content.** The engine drift leg is real,
exactly zero at daily cadence, and bounded by 0.0765 (W) / 0.0579 (M) / 0.1374 (Q) pp/yr on this
grid — and **one in six nonzero published leg values in the record (one in ten of the strict
set-decomposition legs) is smaller than the artefact measured in its own units**. The specific leg
idea 559 worried about is mostly fine (6.5% of BOTH values inside); what is not fine is the habit of
quoting jensen and cost legs at 0.03–0.09 pp/yr as if they were content, and of publishing a leg
with no cadence stated (58.2% of values) when the floor moves 2.4× across cadences.

**Proposed PROTOCOL line (for Sunday, not adopted here):** *any published arm-minus-arm leg must
state its cadence and construction, and quote the drift floor for that (cadence, construction)
beside it; a leg inside its floor is reported as "not distinguishable from renormalisation", never
as an effect.*

As capital the channel is worth nothing (46.7% win rate, median +0.0000 Sharpe) except at quarterly
cadence, where letting weights drift is worth +0.0279 of median Sharpe — mostly the 1.10x/yr of
turnover it does not pay.

**SURVIVORSHIP:** B136 and SMALL439 are current constituents only; dead names are absent and CAGR
levels are inflated. The drift leg is an arm-minus-arm quantity inside one panel at identical depth,
where the bias very largely cancels; the KEEP columns and the rule-8 levels are NOT protected.
