# Idea 11 — cost-sensitivity — **KILL for RULES v1; the standing KEEP survives only to 5 bps cross-universe**

Script: `research/backtests/2026-09-04_cost-sensitivity_cloud.py` ·
console: `2026-09-04_cost-sensitivity_cloud.console.txt` ·
42 reported points (2 universes × 3 books × {0,5,10,15,25,50,100} bps) plus a continuous
0.5 bp breakeven curve per (universe, book). No tuned parameters: v1's (n=5, w=0.15) are the
live rules, CAND20's n=20 / 75% gross are idea 2's published choices, EWall has none.

## Harness
Reproduces idea 2's published KEEP row to the decimal (12.7% / 1.093 / −18.3%, halves
1.088/1.103) and the live v1 row (6.5% / 0.666 / −13.8%, halves 0.641/0.692 vs published
6.5% / 0.67 / −13.8%, 0.64/0.69).

The cost curve is **exact, not interpolated**: in `engine.backtest` the held-weight path
drifts on asset returns and the target weights are cost-free, so
`r_t(c) = r_t(0) − turnover_t·c/1e4` identically. Verified against the engine at 5/10/25/50
bps on all 3 books × 2 universes: **max |analytic − engine| = 0.000e+00**. Every breakeven
below is a solved crossing on a 0.5 bp grid.

## The answer to the queued question

**Turnover is the whole story, and v1 has the most of it by 2–3×:**

| book | turnover u56 | turnover broad | drag @10bps | dSharpe / 10 bps (u56 / broad) |
|---|---|---|---|---|
| **v1 (live)** | **23.6×/yr** | **29.4×/yr** | **2.36% / 2.94% per yr** | **−0.225 / −0.265** |
| CAND20 (idea 2 KEEP) | 9.6×/yr | 13.8×/yr | 0.96% / 1.38% | −0.084 / −0.099 |
| EWall (idea 10) | 8.2×/yr | 8.3×/yr | 0.82% / 0.83% | −0.083 / −0.080 |

**RULES v1 dies at cost levels no realistic execution avoids.** On universe.json its CAGR
goes 9.0% (0 bps) → 7.7% (5) → 6.5% (10) → 5.2% (15) → 2.8% (25) → **−3.1% (50)** → −13.9%
(100); on broad, 9.6% → 8.0% → 6.4% → 4.9% → 1.8% → **−5.4%** → −18.4%. Breakevens:

| test | v1 u56 | v1 broad | CAND20 u56 | CAND20 broad | EWall u56 | EWall broad |
|---|---|---|---|---|---|---|
| Sharpe > SPY | **0.0 bps** | **0.5 bps** | 34.0 | 16.5 | 29.0 | 27.0 |
| CAGR > SPY | never | never | never | never | never | never |
| CAGR > 0 | **36.5 bps** | **31.0 bps** | 133.5 | 99.0 | 130.0 | 133.0 |
| passes 4b | never | never | **24.5 bps** | **7.5 bps** | 7.0 | 10.5 |
| passes 4a (v1 at same cost) | — | — | never | never | never | 300+ |

**Cost is not what kills v1 — v1 is already dead at zero cost.** It fails 4b at 0 bps on both
lists (u56: H1 and CAGR; broad: H2, OOS and CAGR) and never beats SPY on CAGR at any cost.
What cost adds is the speed of the collapse: at 50 bps v1 is a **losing** strategy with a
−46.8% / −62.9% max drawdown, i.e. the drawdown is manufactured entirely by fees.

**The finding that matters for capital: the standing 4b KEEP survives to 5 bps, not 10.**
Cross-universe 4b (pass on BOTH lists) holds for CAND20 and EWall at 0 and 5 bps and for
neither at 10 bps — 4 of 21 grid points. CAND20's cross-universe breakeven is **7.5 bps**
(broad binding: H2 at 8 bps, then OOS at 11), EWall's is **10.5 bps** (CAGR floor at 11 bps
on broad, 8 bps on u56). PROTOCOL's own 10 bps assumption therefore sits *on top of* the
candidate's margin rather than inside it, and idea 2's KEEP is a 5 bp-execution claim.

## Rule 8 (walk-forward), chosen on 2009–2016 and read once on 2017–2026
S1 and S2 both select **CAND20@0bps** on universe.json → OOS 15.5% / 1.248 / −18.2%, clears
every OOS 4b bar. On broad, S1 picks CAND20@0bps (14.1% / 0.993 / −20.0%, clears) and S2
picks EWall@0bps (11.6% / 1.103 / −17.3%, clears). Spearman(IS Sharpe, OOS Sharpe) = **+0.990**
(u56) and **+0.962** (broad) — unsurprising, since cost is a deterministic monotone shift, and
it is the cleanest demonstration in this repo that rule 8 has power when the varied parameter
is real rather than noise.

The pre-registered rule-8 cost question — *is in-sample cost tolerance an unbiased estimate of
out-of-sample cost tolerance?* — answers **no, and not even consistently signed**. Cost at
which Sharpe(book) ≤ Sharpe(SPY), IS vs OOS: CAND20 20.0 → 46.0 bps on u56 (**+26**) but
24.0 → 10.5 on broad (**−13.5**); EWall 18.0 → 37.5 (**+19.5**) and 27.5 → 26.5 (**−1.0**).
A cost budget fitted on one window is worth ±15–25 bps, which is larger than the candidate's
entire margin.

## Caveats
Survivorship: current constituents of both lists, one-directional, and it points the wrong way
for a cost study — a survivor panel understates the rotation a live book would have paid to
exit names that later delisted, so every breakeven above is optimistic. The model is also a
pure proportional cost: no spread/impact term, no borrow, no partial fills, and turnover is
measured as Σ|Δw| at the rebalance, which is what the engine charges.

## Suggested RULES wording (for Sunday review, not applied here)
> *Execution assumption.* Any book proposed under path 4b must pass 4b on **both**
> `universe.json` and `universe_broad.json` at the cost actually achievable, and its
> **cross-universe 4b breakeven cost must be reported**. A book whose breakeven is below
> 15 bps is not capital-worthy without a measured execution cost, because the walk-forward
> spread on that breakeven is ±15–25 bps.

**Verdict: KILL for RULES v1 (fails 4b at every cost including zero; edge over cash gone by
31–36.5 bps).** The cost curve for the candidate books is a documented result, not a KEEP:
no new book was proposed here.
