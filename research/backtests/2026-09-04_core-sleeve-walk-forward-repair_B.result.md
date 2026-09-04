# Idea 67 — core-sleeve-walk-forward-repair (lane B, 2026-09-04)

**Verdict: the proposed repair is a KILL, and the walk-forward genuinely disagrees with
b = 0.25.** No IS drawdown cap — at any of five levels, under either of two IS objectives,
with or without idea 63's CAGR floor — selects b = 0.25 on `universe_broad.json`. 0 of 24
grid points (12 per universe) select b = 0.25 on **both** lists. The reason is not that the
IS window is benign; it is that **IS drawdown does not rank OOS drawdown**, so no cap on it
can discriminate. But the run also isolates what actually breaks the walk-forward, and it is
not b: it is the **QQQ core**. With a SPY core the same walk-forward passes.

Script: `research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py`
Console: `2026-09-04_core-sleeve-walk-forward-repair_B.console.txt`
Memo: `2026-09-04_core-sleeve-walk-forward-repair_B.memo.md`

Harness reproduces idea 63's published broad rows to the digit (top20 13.1%/0.958/-20.1%,
ew-all 10.7%/1.027/-17.7%, ew-band3 11.1%/1.064/-16.8%, top20 b=0.25 13.8%/1.016/-19.9%,
ew-band3 b=0.25 12.3%/1.086/-18.5%).

## Setup

Idea 63's arms, nothing re-tuned: books `v1`, `top20`, `ew-all`, `ew-band3` × b ∈ {0, 0.25,
0.50} × core ∈ {QQQ, SPY}, weekly, t+1, 10 bps, both universes (20 arms each). IS =
2009-01-13 → 2016-12-31, OOS = 2017-01-01 → 2026-09-03. Two tuned parameters, all points
reported: **IS objective** ∈ {IS Sharpe, IS Calmar} × **IS drawdown cap** ∈ {none,
SPY-relative 60% (idea 63's rule B), −20%, −15%, −12%, −10% absolute}.

## Finding 1 — the queue's premise about the IS window is wrong

The hypothesis was that 2009–2016 contains no severe bear, so a SPY-relative cap is too
loose. It does not hold: **SPY IS MaxDD is −22.1%, which is 65% of its OOS −33.7%.** The IS
window has a real bear (2011).

What is actually degenerate is the **cross-arm spread**. On broad, the 20 arms' IS drawdowns
span −9.0% to −13.6% (4.6pp); their OOS drawdowns span −17.2% to −22.0%. A cap has almost
nothing to bite on, and what it does bite is the wrong thing:

| Spearman rank corr across the 20 arms | broad | universe.json |
|---|---|---|
| IS Sharpe → OOS CAGR | **+0.84** | **+0.91** |
| IS Sharpe → OOS Sharpe | +0.63 | +0.65 |
| **IS Sharpe → OOS MaxDD** | **−0.19** | **−0.45** |
| **IS MaxDD → OOS MaxDD** | **+0.57** | **+0.20** |

IS Sharpe forecasts OOS *return* well and OOS *drawdown* perversely — the higher the IS
Sharpe, the deeper the OOS drawdown. So every Sharpe-maximising IS rule is pulled toward
precisely the arm that will breach the OOS drawdown cap, and the one statistic that could
stop it (IS MaxDD) carries a rank correlation of +0.20 with its own OOS counterpart on
universe.json. **The walk-forward's failure is a drawdown-forecasting failure, not a
calibration error.**

## Finding 2 — no cap picks b = 0.25 (hypothesis rejected)

Selection-rule grid, QQQ core, broad list — 12 points, all reported:

| IS objective | IS DD cap | selected arm | OOS CAGR / Sharpe / MaxDD | OOS 4b | b=0.25? |
|---|---|---|---|---|---|
| IS-Sharpe | none *(rule A)* | top20 b=0.50 | 14.4% / 0.991 / −22.0% | FAIL DD | no |
| IS-Sharpe | SPY-rel 60% *(rule B)* | top20 b=0.50 | 14.4% / 0.991 / −22.0% | FAIL DD | no |
| IS-Sharpe | −20% / −15% abs | top20 b=0.50 | 14.4% / 0.991 / −22.0% | FAIL DD | no |
| IS-Sharpe | −12% abs | ew-band3 b=0.50 | 13.7% / 1.050 / −21.0% | FAIL DD | no |
| IS-Sharpe | −10% abs | **v1** b=0.50 | 11.2% / 0.936 / −17.2% | PASS | no |
| IS-Calmar | none / SPY-rel / −20% / −15% / −12% | ew-band3 b=0.50 | 13.7% / 1.050 / −21.0% | FAIL DD | no |
| IS-Calmar | −10% abs | **v1** b=0.50 | 11.2% / 0.936 / −17.2% | PASS | no |

**10 of 12 points pick b = 0.50 and fail the OOS drawdown cap.** The two that pass do so by
switching *book* (to the low-return live rules), not by moderating b. On universe.json a
−10% cap does reach ew-band3 b=0.25 under both objectives — but that is the tightest cap on
the grid, it is the only one of 12 that does, and the same cap on broad picks `v1 b=0.50`.
**Zero grid points select b = 0.25 on both universes.**

Split stability, rule B, QQQ core, six IS end-years: **b = 0.50 at 5 of 6 splits on each
universe** (broad: 2013 v1, 2014 ew-all, 2015/2016 top20, 2017 ew-band3, all b=0.50, four of
them failing OOS DD; 2018 drops to b=0.00 and fails OOS CAGR). b = 0.25 is selected at one
split on universe.json (2018) and never on broad. This is not one arbitrary cut date.

## Finding 3 — the thing that breaks the walk-forward is the QQQ core, not b

Repeating the identical grid with a **SPY** core (idea 63's own hindsight control):

| universe | QQQ core: points passing OOS 4b | SPY core: points passing OOS 4b |
|---|---|---|
| broad | **2 of 12** (both by switching to v1) | **10 of 12** (2 select nothing at −10%) |
| universe.json | 12 of 12 | 10 of 12 (2 select nothing at −10%) |

With a SPY core, every rule that selects anything selects an arm that clears the OOS 4b
bars — `ew-band3 b=0.00` on broad (10 of 12 points), `top20 b=0.25 SPY` on universe.json (9
of 12). The QQQ core's IS optimum overshoots to b=0.50 because QQQ was the best-performing
liquid US index of the IS window as well as the OOS one; the SPY core has no such pull. This
confirms idea 63's own warning about the QQQ sleeve from the other direction: **4b could not
detect the hindsight tilt, but rule 8 does.**

## Finding 4 — what survives, on both KEEP paths

Cross-universe 4b at 10 bps (both lists must pass): 8 of 20 arms pass — `v1 b=0.50 QQQ`,
`top20 b=0.25` (QQQ and SPY), `ew-all b=0.25` (QQQ and SPY), `ew-band3 b=0.00`,
`ew-band3 b=0.25` (QQQ and SPY), `ew-band3 b=0.50 SPY`. Every b=0.50 QQQ arm fails on
drawdown on broad.

4a (vs the live RULES v1 book) is universe-dependent and worth flagging: on **broad**, where
v1's own MaxDD is −21.2%, 13 of 20 arms clear 4a including all the candidates; on
**universe.json**, where v1 draws down only −13.8%, **every arm fails 4a on drawdown** —
exactly the pathology PROTOCOL 4b was added to route around.

| arm (both universes, 10 bps) | u.json CAGR/Sh/DD | broad CAGR/Sh/DD | 4b both | rule 8 |
|---|---|---|---|---|
| ew-band3 b=0.00 | 11.3% / 1.136 / −15.1% | 11.1% / 1.064 / −16.8% | YES | **selected on broad (SPY-core grid), OOS passes** |
| **ew-band3 b=0.25 SPY** | 11.4% / 1.106 / −16.5% | 11.3% / 1.040 / −17.7% | YES | not selected, never rejected |
| ew-band3 b=0.25 QQQ | 12.4% / 1.142 / −16.2% | 12.3% / 1.086 / −18.5% | YES | selected only at a −10% cap on u.json |
| top20 b=0.25 QQQ (idea 63) | 13.5% / 1.120 / −18.5% | 13.8% / 1.016 / −19.9% | YES | **never selected by any of 24 points** |
| top20 b=0.50 QQQ (rule 8's pick) | 14.3% / 1.104 / −18.8% | 14.5% / 1.042 / **−22.0%** | no (DD) | selected 10/12 on broad, **fails OOS DD** |

Rule-8 headline (broad, rule B pick = `top20 b=0.50 QQQ`): OOS **14.4% / 0.991 / −22.0%**
vs SPY OOS 15.5% / 0.884 / −33.7% (cap −20.2%) and RULES v1 OOS 6.0% / 0.581 / −21.2%.
Better Sharpe than SPY, 1.8pp over the drawdown cap — idea 63's stated weakness, confirmed
and now explained.

## What this changes

- Idea 63's `b = 0.25` should **not** be carried forward as a QQQ-core candidate. It is a
  sample-wide-4b artefact that no out-of-sample selection rule reproduces.
- The defensible surviving arm is **`ew-band3` with a 0–25% SPY core** — idea 57's book,
  plus at most a quarter of it in plain beta. The walk-forward picks b=0.00 on broad and
  b=0.25 (top20 flavour) on universe.json; the two ends differ by ~1.0pp CAGR and ~1.0pp
  drawdown, so the sleeve is a small dial, not the edge.
- Proposed protocol note for Sunday review: **rank correlation between the IS statistic a
  selection rule maximises and its OOS counterpart should be reported alongside any rule-8
  result.** A walk-forward that maximises a statistic which anti-forecasts the binding
  constraint is not evidence either way, and that is what happened here.

## Honest limits

- Both universes are current constituents (survivorship). QQQ's IS-and-OOS dominance is
  itself partly that bias; the SPY-core control is the cleaner read.
- 20 arms is a small cross-section for rank correlations; the +0.20 IS→OOS drawdown figure
  on universe.json is indicative, not precise.
- Two tuned parameters (IS objective, IS drawdown cap), 12 points per universe per core, all
  reported. The b grid {0, 0.25, 0.50} is idea 63's and was not extended.
- 2026 is a partial year (through 2026-09-03).
