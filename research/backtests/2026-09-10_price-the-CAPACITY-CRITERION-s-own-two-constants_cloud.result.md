# Idea 647 — price-the-CAPACITY-CRITERION-s-own-two-constants (cloud, 2026-09-10)

**ANSWERED, with a correction to the clause PROTOCOL was about to adopt. The criterion does not
have two constants — it has ONE (`k = ticket / bar`), exactly and by construction. Read at idea
121's own pair the criterion selects $0.50M, NOT the $1M idea 121 proposes, and $1M is selected by
2 of 45 satisfiable pairs (4.4%). Over the grid the selected floor spans 7 ladder rungs ($0M–$20M)
and the resulting book spans 0.98 of OOS Sharpe. The floor loses to no floor at all
(−0.0838 mean OOS Sharpe, winning 2 of 12 cells). 4a 0/96, 4b 0/96 — no KEEP-candidate.**

Script `2026-09-10_price-the-CAPACITY-CRITERION-s-own-two-constants_cloud.py`; outputs
`.txt .ladder.csv .capacity.csv .grid.csv .books.csv .spread.csv .wf.csv`. Two tuned parameters,
exactly the queue's: **TICKET** ∈ {$1, 2, 5, 10, 20, 50, 100}M × **BAR** ∈ {2, 5, 7.5, 10, 15, 20,
25}% → 49 pairs × 2 instruments = **98 selections, every one reported**. The 8-rung floor ladder,
the book (EWALL/EWGATE/RANK20) and the cost rung (10/25 bps) are reported axes. Construction is
idea 427 lane B's, verbatim where load-bearing (panel, `fast_bt`, the matched share floors s*(F),
`weights`, `capacity`).

## Gates (all pass)

| gate | result |
|---|---|
| G1 | `fast_bt` vs `engine.backtest` (EWall, floor $0): **1.39e-17** gross / **9.02e-17** turnover |
| G2 | idea 121's published EWall CAGR ladder (none/$1M/$5M/$20M) 10.18 / 5.92 / 1.64 / −4.92% reproduces to **0.003 pp** |
| G3 | idea 121's unscreened RANK20 participation **17.62%** against its published 17.6% (|diff| 0.02 pp) |

## 1. The clause has ONE constant, not two — and the collapse is exact

`participation = per_trade_frac × ticket / p25_ADV`, so `participation ≤ bar` is
`per_trade_frac / p25_ADV ≤ bar / ticket`: the criterion can only see the **ratio**. Measured
across all 98 cells, the number of distinct floors selected per (instrument, ticket/bar) group is
**max 1** — the collapse is exact, not approximate. The 49 pairs are **28 distinct ratios**, and
those 28 ratios select only **7 distinct floors**. Idea 121's pair is **k = $100M**.

    k ($M):   4    5   6.7    8   10  13.3   20   25  26.7  33.3   40   50  66.7   80  100  133  200 …1000  ≥1333
    DV floor: 0    0     0    0    0     0    0    0     0     0    0    0  0.25 0.25  0.5    1    5 …  20  unsatisfiable

**PROTOCOL should adopt (or reject) one number, `ticket/bar`, and should never present the ticket
and the bar as two independent choices — varying them jointly at fixed ratio is a no-op.**

## 2. Idea 121's own pair does not select idea 121's floor

| instrument | ($10M, 10%) selects | idea 121 proposes |
|---|---|---|
| DV (dollar floor) | **$0.50M** | $1M |
| VOLSH (matched share floor) | **$0.50M** | $1M |

DV participation is 17.62% at $0M, 11.27% at $0.25M and **9.41% at $0.50M** — the bar is already
met one rung below the proposed clause. Idea 121 published $1M because its own ladder had no
$0.25M/$0.50M rungs; idea 427 added them. **This is idea 646's ladder-resolution finding arriving
from the constants side, and it is worse than a resolution artefact: the clause value is wrong at
the clause's own constants.** $1M is selected by only **2 of 45** satisfiable DV pairs (4.4%);
**13 of 98** pairs are unsatisfiable on this ladder (no rung reaches the bar).

## 3. The sensitivity, published (what the queue asked for)

DV, selected floor in $M, `--` = unsatisfiable:

| ticket \ bar | 2.0% | 5.0% | 7.5% | 10.0% | 15.0% | 20.0% | 25.0% |
|---|---|---|---|---|---|---|---|
| $1M | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $2M | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 |
| $5M | 5 | 0.5 | 0.25 | 0 | 0 | 0 | 0 |
| **$10M** | 10 | 5 | 1 | **0.5** | 0.25 | 0 | 0 |
| $20M | 20 | 5 | 5 | 5 | 1 | 0.5 | 0.25 |
| $50M | -- | 20 | 10 | 10 | 5 | 5 | 5 |
| $100M | -- | -- | -- | 20 | 10 | 10 | 5 |

VOLSH is in `.grid.csv` and differs at three cells only (it tops out at the $10M-equivalent rung).
**Doubling either constant moves the clause by a factor of 10** ($10M→$20M at 10% takes the floor
from $0.5M to $5M; $10M→$50M takes it to $10M). A clause stated to one significant figure in
either constant is not a clause.

## 4. What that sensitivity costs the book (PROTOCOL 4)

Every ladder rung × 3 books × 2 cost rungs = **96 rows, all committed**. Monotone damage, replicating
idea 427: EWALL DV @10 bps CAGR runs **+10.18% ($0M) → +7.05% ($0.5M) → +5.92% ($1M) → −4.92%
($20M)** and Sharpe/OOS **0.68/0.64 → 0.47/0.45 → 0.41/0.38 → −0.16/−0.34**. Across the floors the
grid can select, the spread of the selected book is **15.10 pp of CAGR, 0.841 of Sharpe and 0.977
of OOS Sharpe** (EWALL/DV/10 bps; ≥0.28 OOS on all 12 book × instrument × rung cells). **That is
the price of the two constants and it is larger than any effect the clause is meant to protect.**

## 5. Rule 8: the capacity floor does not walk forward (PROTOCOL 8)

The floor is chosen on 2010–2016 only and 2017–2026 is read once, under three choosers:
**A** = idea 121's criterion at its own pair, read on the IS window alone; **B** = IS Sharpe;
**C** = no floor.

* A selects **$0.50M** in 12 of 12 cells (IS and full-sample selection agree, so the criterion is
  at least stable in time).
* **A and B never agree (0 of 12 cells).**
* Mean OOS Sharpe: **A 0.2452, B 0.3074, C 0.3289.** The capacity floor costs **−0.0838** against
  no floor at all and **−0.0623** against choosing the floor on IS Sharpe; **it beats the
  no-floor control in 2 of 12 cells.**
* **KEEP paths: 4a 0/96 and 4b 0/96, BOTH 0** at both cost rungs. Comparands: SPY 14.13% / 0.8615 /
  −33.72% (OOS 0.8820); RULES v2 @10 bps 3.80% / 0.5710 / −14.70% (OOS 0.5665).

## Recommendation for the Sunday review

**Do not adopt idea 121's ADV clause as written.** If PROTOCOL wants a capacity clause it must
(a) state the single constant `k = ticket/bar` rather than two, (b) state the ladder it is solved
on, because the answer moves a full rung per rung added, and (c) carry the measured cost: on the
only panel with cached volume the floor the criterion selects is worth **−0.08 OOS Sharpe** against
no floor. A clause that costs return, never clears either KEEP path, and whose value swings 10x on
a 2x change in an unswept constant is not ready to be a rule.

## Concurrent replication (record convention 320R)

A lane B run answered idea 647 the same day while this one was in flight; the two were written
independently and **agree on every load-bearing number**. Both find the ratio collapse EXACT (they
measure the linearity residual at 1.7e-18 over 128 points spanning 40 ratios, 0 disagreements
within a ratio; this file asserts max 1 distinct floor per ratio group over 98). Both find idea
121's $1M is not what its own criterion selects, and **their 8-rung answer is this file's $0.50M
exactly** — on a 33-rung refined ladder they solve it at **$0.412M**, i.e. the finer the ladder the
further the clause value drifts, which sharpens §2 rather than softening it. Both report 4a 0 and
4b 0 (their 192 rows, this file's 96) and both find the floor losing to the no-floor control out of
sample (their pick beats no-floor 0/24; this file's 2/12, same sign).

Their run reaches three things this one does not, and they are corrections to take:
**(i)** the participation κ is **not monotone in the floor on VOLSH**, so "the smallest passing
rung" needs an explicit up-set check — this file's `select_floor` takes the min of the passing set
and would mis-state a non-monotone instrument; **(ii)** the criterion's IS-only answer matches its
full-sample answer on only **110 of 128** pairs (85.9%) — this file tested that at idea 121's own
pair alone, found 12/12 agreement, and would have over-read a grid-wide claim from it;
**(iii)** the **p25 quantile is a third unswept constant** and moves the selected rung on 29 of 64
pairs when read at p50 — this file flags it as a caveat but does not measure it. On the shared
claim the two lanes are one result: the clause has one constant, its published value is wrong at
its own constants, and it costs return.

## Caveats

* **SURVIVORSHIP (PROTOCOL 9).** SMALL439 is a current-constituent screen of sub-$2B names since
  2010 with the 44 `max_1d_move ≥ 1.0` names dropped, and it is the **only panel with cached
  volume** (U56/broad136 volume is queue idea 429 and needs network), so every level here is an
  upper bound on a tradable estimate. The load-bearing quantity is the floor-minus-floor contrast
  inside one panel.
* The VOLSH rows are indexed by the **DV-equivalent rung**: each is the share floor s*(F) that
  matches that dollar rung's admission rate to ≤0.5 names/day (idea 427's calibration, asserted).
* `capacity()` is idea 121's construction verbatim, including its choice of the **p25** held-name
  ADV and a single-rebalance ticket; those two conventions are not swept here and are a third and
  fourth unstated constant. The ratio collapse in §1 holds whatever they are.
* The ladder is idea 427's 8 rungs. §2's correction is a statement about that ladder's resolution;
  a finer ladder would move the selected floor again, which is the point.
