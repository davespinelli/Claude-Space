# Idea 121 — liquidity-screened-small-panel (cloud, 2026-09-05)

**Verdict: ANSWERED — a $1M ADV floor is proposed as a PROTOCOL clause on a pre-registered
capacity criterion, and it moves 7 of 48 small-panel verdicts, all of them 4a passes going to
fail and all of them in the unscaled-ranked family. But the two findings the project actually
cites from this panel do NOT dissolve: the eligibility gate still destroys 3.6-4.9 pp/yr of
CAGR at every floor on the ladder with the sign never flipping (P1 REFUTED), and the four-way
gate ordering survives intact at the proposed floor (P2 REFUTED). No book passes 4b at any
floor (P3 CONFIRMED) and every rule-8 pick loses badly to SPY out of sample (P4 CONFIRMED).
So: the floor is a real reporting requirement and it deletes every 4a claim this panel has
produced, but it is not a general solvent for the panel's findings — idea 120's scaler
premium was unusually fragile, not typical.**

Script: `2026-09-05_liquidity-screened-small-panel_cloud.py`. 192 grid points (4 floors x 3
gross x 16 books), 48 capacity rows, 12 Claim-A contrasts, 12 four-way orderings, 8 walk-forward
picks, 24 cost-ladder points, 48 verdict-movement rows — all reported, none selected on.
Two tuned parameters: n in {5,10,20,40}, g in {0.50,0.75,1.00}. Floor, book family, gate
composition and cost rung are reported at every value. Panel: 439 sub-$2B names (44 dropped
for `max_1d_move >= 1.0`), SPY as benchmark column only, weekly, next-day execution, 10 bps.

## 0. Harness and reproduction
Vectorised simulator vs `engine.backtest`: max|diff| **1.4e-17**. Live RULES v1 on this panel
8.15%/0.603/-32.8% (OOS 7.92%/0.581/-32.8%, turnover 33.4x/yr) — identical to idea 120's
figure. SPY 14.13%/0.862/-33.7%, halves 0.891/0.858, OOS 15.45%/0.882/-33.7%, so **4b's bars
are MaxDD >= -20.2% and CAGR >= 9.89%**. Idea 119's held-name ADV percentiles recompute at
**p25 $1.35M / p50 $4.59M** on the ranked n=20 book against its published p25 $0.87M / p50
$4.33M — the same order of magnitude, the gap being idea 119's narrower book. Independent
cross-run check: the equal-weight-everything-above-the-floor control reproduces idea 120's
no-ranking ladder to three decimals (Sharpe **0.678 / 0.413 / 0.181 / -0.163** at
none / $1M / $5M / $20M; idea 120 published 0.678 / 0.413 / 0.181 / -0.166).

## 1. The proposed floor (capacity only, no return input) — $1M
Criterion fixed before any return was read: *the smallest ladder floor at which $10M of capital
trades <= 10% of the **p25** held-name 20-day median dollar volume, in the narrowest book the
project publishes on this panel (ranked n=20)*.

| floor | R20 p25 held ADV | % of that name's ADV traded per rebalance at $10M | |
|---|---|---|---|
| none | $1.35M | **17.6%** | fail |
| **$1M** | **$3.06M** | **7.3%** | **PASS — proposed** |
| $5M | $7.68M | 2.5% | pass |
| $20M | $25.06M | 0.9% | pass |

The narrower books are far worse unscreened: **R5 trades 137% of its p25 name's daily ADV** at
$10M with no floor, and still 38% at a $1M floor. R10 is 46% / 17%. The equal-weight books are
never capacity-constrained (0.1-1.9% at $10M) because they spread $10M over 141-348 names — so
the floor binds on *concentration*, not on the panel.

## 2. What the floor costs in level — the panel's return is in the thin names
Equal-weight-everything, g=0.75, by floor: **10.18% / 5.92% / 1.64% / -4.92%** CAGR and
**0.678 / 0.413 / 0.181 / -0.163** Sharpe, on **348 / 252 / 141 / 44** mean names. This is
monotone and steep, and it is the reason the floor matters: 4.3 pp of the unscreened book's
CAGR is in names below $1M of ADV and a further 4.3 pp is between $1M and $5M.

**This decay is not evidence that thin small caps earn more.** The panel is a current-constituent
screen; its missing cohort (delisted, bankrupted, acquired 2010-2025) is concentrated in exactly
the thin names the floor removes, so the floor and the survivorship bias are *positively
correlated* and the two effects cannot be separated on this data. The honest statement is that
the unscreened level is uninterpretable, not that the screened level is the truth.

## 3. Claim A survives the floor (P1 REFUTED)
`EWgate` minus `EWall` — the finding, quoted five times in the QUEUE, that the RULES v1
eligibility gate *destroys* ~5.4 pp/yr on small caps:

| floor | dCAGR @ g=0.75 | dSharpe | dMaxDD | names all -> gated | sign negative in |
|---|---|---|---|---|---|
| none | **-6.52 pp** | -0.342 | -3.81 pp | 348 -> 141 | 3/3 gross |
| $1M | **-4.87 pp** | -0.268 | -2.54 pp | 252 -> 105 | 3/3 |
| $5M | **-4.03 pp** | -0.263 | -5.00 pp | 141 -> 59 | 3/3 |
| $20M | **-3.56 pp** | -0.285 | -7.89 pp | 44 -> 17 | 3/3 |

Negative in **12 of 12** cells, and dSharpe is essentially flat in the floor (-0.34 to -0.26).
At 0 bps, where the claim was originally made, dCAGR is -5.31 pp unscreened and **-3.70 pp at
the proposed floor** — so the gate is not paying for itself in turnover either (it raises
turnover from 1.7x to 13.4x/yr while losing CAGR *and* drawdown). P1 predicted the effect would
more than halve; it attenuates by 25% and keeps its sign everywhere. **The small-cap trend
inversion is not a sub-$1M-ADV artefact.**

## 4. Claim B: the ordering holds at the floor, the magnitudes do not reproduce (P2 REFUTED)
Four-way gate decomposition at n=40, scaler on. Published (idea 38/56): none 0.797 > 200d 0.693
> vol60 0.524 > both 0.441, spread 0.356.

| floor | none | 200d | vol60 | both | ordering |
|---|---|---|---|---|---|
| none | 0.576 | 0.565 | 0.497 | 0.537 | none>200d>both>vol60 — **inversion vol60<both** |
| **$1M** | 0.358 | 0.348 | 0.323 | 0.312 | **published order holds exactly** |
| $5M | 0.084 | 0.022 | 0.049 | -0.022 | none>vol60>200d>both — **inversion 200d<vol60** |
| $20M | -0.216 | -0.341 | -0.371 | -0.438 | published order holds |

Two things are true at once and both belong in the record. (i) The *direction* the claim is
quoted for — the vol20 half hurts more than the 200d half — reproduces at three of four floors,
including the proposed one, so the floor does not overturn it. (ii) The published *levels and
spread* do not reproduce under this run's conventions (gross-matched weights per idea 81,
439-name panel, trading-day index, 260-day warm-up): the spread is 0.080 here versus 0.356
published, i.e. **the four gates are four times closer together than the row that indicts the
vol20 gate implies**. The ordering is stable; the size of the indictment is not, and the size is
what the QUEUE cites. That is a convention finding, not a liquidity finding, and it is the
sharper of the two.

## 5. Verdict movement — the deliverable (7 of 48)
4a and 4b verdicts at floor $0 versus the proposed $1M floor, over 16 books x 3 gross:

| moved | book/gross | 4a $0 -> $1M | why |
|---|---|---|---|
| YES | `EWall` g=0.50 | True -> **False** | Sharpe 0.679 -> 0.413 |
| YES | `R5u` g=0.50 | True -> **False** | 0.669 -> 0.454 |
| YES | `R10u` g=0.50 | True -> **False** | 0.699 -> 0.315 |
| YES | `R20u` g=0.50, g=0.75 | True -> **False** | 0.752 -> 0.333/0.336 |
| YES | `R40u` g=0.50, g=0.75 | True -> **False** | 0.609 -> 0.284/0.286 |

**All 7 of the panel's 4a passes are at floor $0 and none survives $1M** (4a passes by floor:
7 / 0 / 0 / 0). Six of the seven are the ungated, unscaled ranked family — idea 119/120's book —
which is the family idea 120 already killed on a $5M floor; this run shows it dies at $1M, and
that its 4a pass was the same thin-name effect. **4b never moves because it is never passed:
0 of 192 points at any floor.** Median effect of the floor across all 48 cells: dCAGR -3.10 pp,
dSharpe -0.222.

## 6. Rule-8 walk-forward at every floor (P4 CONFIRMED)
(n,g) chosen on 2011-01-13..2016-12-31 only over the ranked family, OOS 2017-2026 read once.
S1 = argmax IS Sharpe; S2 = same subject to 4b's IS drawdown cap.

| floor | S1 pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | vs SPY OOS | vs v1 OOS |
|---|---|---|---|---|---|
| none | R20 g=1.00 | 0.770 | 3.61% / **0.286** / -45.1% | 15.45% / 0.882 / -33.7% | 7.92% / 0.581 / -32.8% |
| $1M | R20 g=1.00 | 0.632 | 1.28% / **0.163** / -49.5% | " | " |
| $5M | R20 g=1.00 | 0.320 | -2.71% / **-0.026** / -52.5% | " | " |
| $20M | R5 g=1.00 | 0.224 | -16.88% / **-0.608** / -86.8% | " | " |

Every pick loses to SPY and to the live book out of sample, and **OOS Sharpe falls monotonically
in the floor** — the tradeable version of this panel is worse than the untradeable one at every
rung. S2 is **empty at every floor >= $1M**: no ranked cell clears 4b's in-sample drawdown cap
once thin names are removed. Selection is not the problem; the panel is.

## 7. Costs
g=0.75, 0 / 10 / 25 bps. `EWall` is cost-insensitive (10.37 / 10.18 / 9.89% unscreened;
6.20 / 5.92 / 5.50% at $1M) because it turns over 1.7-2.6x/yr. `EWgate` (13-14x/yr) goes
5.06 / 3.67 / 1.61% and 2.50 / 1.05 / **-1.07%** — negative at 25 bps at the proposed floor.
`R20` goes 6.31 / 3.89 / 0.36% at $1M. Nothing here is cost-robust except the book with no
gate and no ranking, which is also the book with no edge over SPY.

## 8. What this does and does not license
- **Does:** a PROTOCOL reporting clause (memo has exact wording), and the deletion of all seven
  4a passes the small panel has produced.
- **Does not:** rehabilitate or condemn the panel's *signed* findings wholesale. Claim A survives.
  Claim B's ordering survives while its magnitude turns out to be a weighting-convention artefact.
  Idea 120's scaler premium remains the only published small-panel finding that the floor
  actually reverses.
- **Open, and now sharper:** the four-way gate spread being 4x narrower under gross-matched
  weights than published is an idea-81 exposure that belongs on the queue in its own right, and
  it is not about liquidity at all.

## Caveats
Survivorship on a current-constituent panel, positively correlated with the floor itself
(section 2) — this is the binding limitation and the floor does not fix it, which is why the
proposed clause is a reporting requirement plus a stated default, not a change to
`load_universe`. Volume is share volume x close, not consolidated tape; the 20-day median is a
proxy for ADV and ignores auction/closing-cross capacity, which is where a real small-cap book
would trade. Capacity is measured as one rebalance's trade in one name against one day's ADV;
a real implementation would spread it, so the %-ADV column is an upper bound on the constraint
and a lower bound on the cost. 10 bps is assumed flat across floors, which flatters the thin
names — the honest version would slope costs down with ADV and would make section 2's decay
shallower and section 3's gate cost larger. Only 2020 and 2022 are stress episodes in the OOS
window. No file outside `research/backtests/` was modified.
