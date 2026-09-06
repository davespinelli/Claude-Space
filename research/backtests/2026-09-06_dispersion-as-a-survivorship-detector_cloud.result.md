# Idea 83 — dispersion-as-a-survivorship-detector (cloud, 2026-09-06)

Script: `research/backtests/2026-09-06_dispersion-as-a-survivorship-detector_cloud.py`
Outputs: `.draws.csv` (1200 draw-rows), `.regressions.csv`, `.by_n.csv`, `.walkforward.csv`, `.console.txt`

**Verdict: ANSWERED — the thermometer hypothesis is REFUTED. Idea 73's test C is not
contaminated. Dispersion as a panel selector is a KILL.**

## What was run
Idea 73's test C re-run under its own code (imported, seed 20260904, 150 draws), then the
control the queue asks for. Two tuned dimensions, both reported exhaustively: draw size
{20, 36, 60} × ranked n {5, 10, 20}; cost rungs 10 and 25 bps; corpora B136 (idea 73's) and
SMALL484 (the max_1d_move ≥ 1.0 screen applied first, 483 tradable).

Two controls, because "winner content" has a hindsight version and an observable one:
- **HIND** — the draw's mean full-sample (2009–2026) name CAGR. Look-ahead **by design**; it
  is a diagnostic for contamination, never a trading input.
- **OBS** — the same computed on 2009–2016 only, knowable at the walk-forward boundary.

**Gate [B] passed before anything new was read**: at (B136, size 36, n 10, 10 bps) the run
reproduces idea 73's three published R2s — CANDg-n10 level **0.433** (published 0.43),
EWall level **0.331** (0.33), ranking premium **0.085** (0.08).

## The queue's suspicion has a real basis — and it is not enough
On B136, dispersion **is** winner content to a large degree: Spearman(disp, HIND) = **+0.47
/ +0.48 / +0.53** across the three draw sizes (t +6.5 to +7.6). A high-dispersion draw
really does hold more of the names that went on to win.

But the slope survives the control in **0 of 8 cells** by the rule fixed before the run
(|kept| < 0.5 **and** controlled |t| < 2.0):

| corpus | size | y = EWall Sharpe | raw slope (t) | HIND-controlled (t) | kept |
|---|---|---|---|---|---|
| B136 | 20 | | +1.42 (6.06) | +0.73 (3.01) | 51% |
| B136 | 36 | | +1.98 (8.56) | +1.59 (6.01) | 80% |
| B136 | 60 | | +2.10 (8.87) | +1.57 (5.78) | 75% |
| SMALL484 | 36 | | +0.11 (0.35) | +0.23 (0.77) | — |

The OBS control removes even less (kept 69–87% on B136). And on idea 73's *actual* test C
statistic — the ranking premium — the control makes the dispersion slope **stronger**, not
weaker: kept **126–166%**, controlled t up to **+6.8**, because winner content pushes the
premium the *other* way (control slope −0.64 to −1.17, t up to −5.5). Rich panels make
equal-weight look good, so conditioning on them *sharpens* the dispersion signal in the gap.

## The real finding is where the relationship dies
It dies on **SMALL484 — the panel with the worst survivorship**, which is the exact
opposite of the thermometer prediction. There the raw dispersion slope is **+0.11 (t 0.35,
R2 0.0008)** on EWall Sharpe and **+0.08 (t 0.63, R2 0.003)** on the premium, i.e. nothing,
while winner content alone is highly significant (control slope +4.18, t **+5.00**). Its
Spearman(disp, HIND) is **−0.09**: on the small panel dispersion is not even correlated with
winning. So idea 73's level relationship is a **large-cap-panel phenomenon**, not a
survivorship artefact — a thermometer would read hottest where the bias is worst.

## Idea 82 re-confirmed on the way past
The mean ranking premium is **negative at all 9 (size, n) cells** — −0.001 to −0.185, most
negative at n = 5 (−0.11 / −0.16 / −0.18 as the draw widens). Ranking still subtracts value.

## Rule 8 — turning the diagnostic into a selector (IS 2009–2016 only, OOS read once)
Panels ranked on their **2009–2016 dispersion alone**, top decile bought, 2017–2026 read
once. Benchmarks: SPY OOS 15.45% / **0.882** / −33.7%; RULES v1 OOS 5.94% / **0.576** /
−21.2%; the full 135-name B136 EWall book 10.60% / **1.020** / −17.7% (passes 4a *and* 4b).

- **DISP-hi** beats a random panel in **6/8 cells**, mean **+0.023** OOS Sharpe — ahead of
  the incumbent IS-Sharpe picker (**+0.002**) and level with the IS-name-CAGR picker (+0.020).
- It **inverts on SMALL484**: DISP-hi −0.025, and the *bottom* decile wins (+0.031).
- Primary cell (B136, 36, 10 bps): DISP-hi lifts the 4b rate to **26.7%** (random 18.7%) but
  drops the 4a rate to **46.7%** (random 62.0%) — it buys SPY-relative Sharpe with drawdown.
- Every decile mean loses to simply holding the whole panel (0.989 vs **1.020**).

So the selector is small, panel-dependent, sign-flipping on the panel that needs it most,
and dominated by the do-nothing book. **KILL as a selector.**

## Consequences for the record
- **Idea 73's test C stands.** Its dispersion → premium regression is not a restatement of
  which winners a draw happened to contain; controlling for that strengthens it.
- **Idea 54's survivorship concern is not answered by this**, and is not weakened by it.
  What this run shows is that dispersion cannot be *used* to detect the bias — it is
  uncorrelated with winner content exactly on the panel where the bias is largest.
- The honest summary of idea 73's headline is unchanged: dispersion moves the LEVEL of both
  books far more than the gap between them (R2 0.33/0.43 vs 0.09), and most of that level
  effect really is "this panel went up" — but "this panel went up" is not the same variable
  as "this panel had high dispersion", and the two can be separated.

## Caveats
- SURVIVORSHIP: both corpora are current-constituent lists. This run measures how much of a
  published statistic their missing delistings explain; it cannot measure what the missing
  names would have done, and a delisting-aware panel could still overturn the answer
  (idea 54 remains open).
- The HIND control is deliberately look-ahead. It is valid as a contamination diagnostic and
  invalid as anything else; nothing in the walk-forward uses it.
- Draws are without replacement from one panel, so draw statistics are not independent; the
  t-statistics above are ordinary OLS t's and overstate significance to that extent. The
  verdict does not turn on a marginal t.
- 150 draws per cell (idea 73's count), one seed. Idea 219's split-half finding says a
  single seeded draw set can flip a verdict; the margins here (t 2.8–6.0 vs a 2.0 bar) are
  wider than that, but the seed was not varied.
- 10 bps and 25 bps only; weekly, t+1 execution throughout.
