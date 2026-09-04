# Idea 83 — turnover-budget-instead-of-a-cost-assumption — **KILL**

Lane B, 2026-09-04. Script `2026-09-04_turnover-budget_B.py`, console `…_B.console.txt`, grid `…_B.grid.csv`.
176 reported points = 2 universes × 2 books × 22 arms-worth (11 arms) × 4 costs {0,5,10,25} bps, plus an exact
0.5 bp breakeven curve per arm. **All points reported; none picked on its own result.**

## The pre-registered question
Idea 11 proved cost enters the engine exactly as `r_t(c) = r_t(0) − turnover_t·c/1e4`, so a book's cost tolerance
is `1/turnover` up to a constant. Instead of *assuming* 10 bps, constrain the quantity the cost multiplies: cap
`Σ|Δw|` per rebalance at a budget `B`. **Does that buy more 4b margin per unit of forgone Sharpe than the
project's incumbent lever, reducing gross `g` (idea 66: an exact lever, ~1.0 pp CAGR per pp MaxDD, dSharpe 0.000)?**

Books: `CAND20` (idea 2's standing 4b KEEP) and `EWall` (idea 10's `B136/EWall`). Instruments: `budget-top`
(QUEUE's literal spec — largest |Δ| trades first, partial fill on the marginal one), `budget-pro` (same cap
reached pro-rata; the gross-preserving implementation control), `gross` (the incumbent). Two tuned parameters:
`B ∈ {0.10, 0.20, 0.40, ∞}` and `g ∈ {0.75, 0.65, 0.55, 0.45, 0.35}`. `B=∞ / g=0.75` is the shared control.
Engine-equivalence check: `budget=None` reproduces `engine.backtest` to `0.000e+00`.

## Answer: no — and the budget moves the wrong way on the risk axis

A turnover budget in these books budgets the **exits**. Most of the turnover is the 200d gate selling names that
fell through it; capping `Σ|Δw|` delays those sales, so drawdown gets *worse*, not better:

| instrument | dMaxDD (pp, mean / min / max) | dCAGR (pp) | dSharpe | d4b_slack |
|---|---|---|---|---|
| `gross` (16 arms) | **+5.80** / +2.04 / +10.39 | +3.91 | **−0.001** | −0.197 |
| `budget-pro` (12) | **−2.36** / −4.91 / +0.01 | −0.51 | +0.012 | −0.030 |
| `budget-top` (12) | **−5.07** / −11.76 / +0.85 | −1.53 | +0.016 | −0.095 |

(positive dMaxDD = drawdown removed; 10 bps, both universes, vs each book's own control)

So the two levers are not on the same side of the trade. `gross` **sells return to buy drawdown protection** at
0.677 pp CAGR per pp MaxDD (range 0.626–0.729 across all 16 arms — the tightest exchange rate the project has
measured, and Sharpe-neutral to 0.001, replicating ideas 66/74). A turnover budget **sells drawdown protection
to buy return**, earning only ~0.22 pp CAGR per pp of MaxDD given up (`budget-pro` 0.51/2.36; `budget-top`
1.53/5.07 ≈ 0.30). Read in the same direction, **raising gross buys return ~3× more efficiently than loosening
the exit schedule does**, and does it without touching Sharpe. The budget is dominated on its own axis.

## Cross-universe: zero budget arms survive
- `universe.json(56)`: 4b passes 31/88 points; 4 budget arms pass at 10 bps.
- `universe_broad(136)`: 4b passes 9/88; **0 of 48 budget points pass at 10 bps, 1 of 48 at any cost**
  (`CAND20/budget-pro0.4` at 0 bps only). The broad controls pass to 10.5 (`EWall`) and 7.5 bps (`CAND20`);
  **every** budget arm's 4b breakeven on broad is either 3.0 bps or NaN (fails even cost-free).
- No arm in the run — the two controls included — passes 4b on **both** universes at 10 bps. Sign flip, not noise.

## The one real positive, and why it is not a candidate
On `universe.json` the budget does exactly what the idea hoped, for the one book whose binding 4b bar is CAGR:
`EWall/control` breaks even at **7.0 bps**; `EWall/budget-pro0.1` at **20.0 bps** (TO 8.21x → 4.28x/yr), and at
the protocol 10 bps it *passes* 4b (11.2% / 1.082 / −18.7%, halves 1.111/1.064, OOS 1.135) where its control
fails on CAGR. `budget-top0.2` → 14.5 bps and `budget-pro0.2` → 11.0 bps likewise. **It does not replicate:** the
same three arms on `universe_broad` all go to NaN while that control rises to 10.5 bps. The mechanism is
conditional on which 4b bar binds — the budget only ever helps a CAGR-bound book, and `gross` is strictly
counterproductive there (all 32 gross arms fail on CAGR) — but one universe is not evidence.

## Walk-forward (rule 8) — B is not selectable
Selection fixed before any OOS number was read (`S-B`: highest 2009–2016 Sharpe among budget arms; ties → larger
B, then `pro`).

| universe | book | S-B pick | IS Sh | OOS CAGR / Sharpe / MaxDD | control OOS | SPY OOS |
|---|---|---|---|---|---|---|
| u56 | CAND20 | budget-top0.1 | 1.055 | 17.2% / **1.154** / −22.9% | 14.4% / **1.170** / −18.3% | 15.5% / 0.884 / −33.7% |
| u56 | EWall | budget-top0.1 | 1.121 | 12.6% / **1.065** / −21.2% | 11.4% / **1.114** / −15.9% | same |
| broad | CAND20 | budget-pro0.1 | 1.194 | 14.6% / **0.953** / −24.7% | 12.5% / 0.894 / −20.1% | same |
| broad | EWall | budget-top0.1 | 1.078 | 12.9% / **1.076** / −23.5% | 10.6% / 1.021 / −17.7% | same |

RULES v1 baseline OOS: 7.8% / 0.751 / −13.8% (u56), 6.0% / 0.581 / −21.2% (broad).
The IS-selected budget **loses to its own control OOS in 2 of 4 cases**, and buys its 2 wins with 4.6–5.8 pp of
extra OOS drawdown. Spearman(IS Sharpe, OOS Sharpe) over the 7 budget arms is **+0.143 / −0.071** on u56 and
+0.750 / +0.607 on broad — i.e. on the primary universe the selection rule points nowhere. Under PROTOCOL rule 8
a candidate that only wins in-sample is PARK at best; this one does not consistently win in-sample either.

## Binding rates (the grid was well-posed, not degenerate)
`B=0.40` binds on 2.2–11.0% of rebalances for CAND20 and 8.5–9.4% for EWall; `B=0.20` on 27–84%; `B=0.10` on
56–95%. So the three budgets span "barely active" to "almost always active" and the result is not an artefact of
a budget that never fires.

## Incidental finding worth carrying forward
`budget-top` (the QUEUE's literal spec) is **partly a disguised gross lever**: truncating a trade list is not
self-financing, so leaving sells unexecuted raises realised gross. On u56 `CAND20/budget-top0.1` realises 0.815
average gross against the control's 0.717 — which is most of its +2.65 pp CAGR and all of its −4.58 pp MaxDD.
This is idea 73's de-grossing artefact appearing from the other side. Any future turnover-constraint work should
use the pro-rata form, or gross-match explicitly, or it is measuring exposure and calling it turnover.

## Caveats
Survivorship: current constituents of both lists, one-directional. For a **turnover** study the direction is
adverse — a survivor panel never rotates out of a name that delisted, so realised turnover here is an
underestimate and every budget above is easier to meet than it would have been live. 2020 and 2022 are the only
real stress episodes in the sample. No RULES/scan/bot/baseline file was modified.
