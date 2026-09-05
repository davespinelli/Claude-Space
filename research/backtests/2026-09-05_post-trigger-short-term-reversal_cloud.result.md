# Idea 125 — post-trigger-short-term-reversal — **KILL**

Script: `research/backtests/2026-09-05_post-trigger-short-term-reversal_cloud.py`
Console: `…_cloud.console.txt` · Grid: `…_cloud.grid.csv` (144 arm-rows + 24 control rows) ·
Walk-forward: `…_cloud.walkforward.csv` · Event study: `…_cloud.eventstudy.csv`

## The question
Idea 96 measured, as a by-product of killing a per-name trailing stop, that a name which has
just broken 15%/25% off its trailing high earns **+0.57% to +2.21% the next day** against an
unconditional +0.06%/day. This run asks whether that is a tradable signal: buy the triggered
names equal-weight, hold H days. Two tuned parameters (D ∈ {0.15, 0.25}, H ∈ {1, 5, 10}),
three panels (u56, broad-136, small-439), four cost rungs (0/10/25/50 bps), two sizing
conventions, every one of the 144 points reported.

## Result 1 — the signal is REAL and replicates on all three panels
Forward return after a fresh break of −D off the 252d high, vs the unconditional mean over the
same days (no costs, diagnostic):

| panel | D | h=1 excess | t | h=5 excess | h=10 excess | t(h=10) | n events |
|---|---|---|---|---|---|---|---|
| u56 | 0.15 | +0.155 pp | +4.07 | +0.191 | +0.156 | +5.01 | 2 386 |
| u56 | 0.25 | **+0.463 pp** | +5.12 | +0.674 | **+1.521** | +8.12 | 1 199 |
| broad | 0.15 | +0.159 pp | +7.30 | +0.242 | +0.215 | +9.64 | 6 552 |
| broad | 0.25 | **+0.437 pp** | +8.63 | +0.517 | **+1.167** | +12.09 | 3 247 |
| small | 0.15 | +0.056 pp | +5.12 | +0.058 | +0.064 | +9.16 | 21 818 |
| small | 0.25 | +0.115 pp | +6.01 | +0.043 | +0.027 | +7.46 | 17 817 |

**18 of 18 cells positive**, t +4.07 to +12.09. Idea 96's by-product is confirmed as a
standalone statistic on a fresh construction (fresh crossings only, SPY excluded, trading-day
index verified).

## Result 2 — on the large-cap panels it is crash beta, not a reversal premium
Split by SPY's own drawdown state (h=1, D=0.25): u56 **+0.947%** inside SPY dd ≤ −10% vs
**+0.077%** outside; broad **+0.940%** vs **+0.012%**. Roughly **92% of the large-cap effect
lives inside market drawdowns** — the queue's own pre-registered prior, confirmed. The small
panel is the exception and is genuinely different: **+0.193% vs +0.180%**, i.e. a broad
short-term reversal that does not need a crash, but only a third the size.

## Result 3 — none of it survives contact with a cost model
- **0 of 144 arm-rows pass 4b.** 7 of 144 pass 4a, all at 25/50 bps where RULES v1 itself has
  gone to a negative Sharpe — passes by baseline collapse, not by merit.
- Only **14 of 144 arms beat their own panel's EWall control on Sharpe, and every one of the
  14 is at the 0 bps rung.** At 10 bps and above, **0 of 108** arms beat a do-nothing
  equal-weight book.
- The horizon where the signal is strongest is the one that cannot be traded. H=1 turns over
  **20–357× per year**; at 10 bps the H=1 arms run −0.08 to −0.56 Sharpe (u56 D=0.15/H=1:
  −0.3% CAGR / −0.080; small D=0.15/H=1: −7.6% CAGR / −0.557 at 184×/yr).
- The only respectable arms are H=10, which is the horizon at which the signal per day is
  smallest (+0.065 to +0.212 pp/day) and the book has decayed into lagged long exposure
  (mean gross 0.28–0.75, 15–49 names). Best 10 bps arm anywhere is broad D=0.15/H=10/dgN10:
  **12.8% / 0.949 / −26.0%**, against the same panel's EWall control at **14.2% / 1.124 /
  −25.4%** — strictly dominated on all three, at zero effort.

## Result 4 — rule 8 does not rescue it
(D,H) chosen on IS Sharpe (≤2016) alone, evaluated untouched on 2017–2026, 24 cells:
- Every cell picks **H=10** (large caps) — the walk-forward correctly refuses the signal's own
  horizon.
- OOS beats the EWall control in **3 of 24** cells, all at 0 bps. Beats SPY in **4 of 24**,
  all at 0 or 10 bps on broad only. Beats RULES v1 in 17/24, which at 25/50 bps is a
  statement about v1's cost sensitivity, not about this book.
- Headline 10 bps OOS: u56 D=0.25/H=10 **4.3% / 0.464 / −18.0%**; broad D=0.15/H=10 **13.4% /
  0.935 / −26.0%**; small D=0.25/H=10 **9.4% / 0.570 / −46.1%** — against SPY OOS
  **15.5% / 0.882 / −33.7%** and EWall OOS 1.104–1.140 (large caps).

## Verdict: **KILL**
The effect is real, large, highly significant and reproducible on three panels — and it is not
a strategy. Its economic content is that the market pays you for owning beta at the moment beta
is cheapest (92% of it on large caps is inside a −10% SPY drawdown), and the only way to
harvest it is at a turnover of 20–357×/yr, which costs 2–36 pp of CAGR a year at the
protocol's own 10 bps. Stretching the holding period to make the costs bearable dilutes the
signal until the book is a worse version of equal-weighting the panel. There is no gross,
threshold or holding period in the grid where it clears 4b, and the do-nothing control beats
it at every rung above zero cost.

**Standing implication for the project:** this closes idea 96's loose end. The +0.57..+2.21%
number should be cited as a *mechanism* explaining why one-day-lagged stop exits have the wrong
sign — never as an unexploited edge.

## Caveats, carried
- **Survivorship, and it bites this idea hardest.** All three panels are current-constituent
  lists; the small panel is the 483-name sub-$2B screen minus the 44 tickers with
  `max_1d_move ≥ 1.0` in `data/small_meta.csv` (439 names). Names that fell 25% off their high
  and then went to zero are absent by construction, which is exactly the cohort a
  buy-the-break book would have held. The bias runs *for* this idea, so the KILL is if
  anything understated.
- Idea 38's calendar-day-index warning was **checked, not assumed**: all three caches are now
  trading-day clean (0 weekend rows, 0 rows with >70% flat prices, 251/yr). This matters more
  here than anywhere else in the project because H=1 is the construction most exposed to
  ffilled non-trading rows; on the current caches there is no artefact to correct.
- Costs are charged as `turnover × bps` outside the compounding loop (the engine's convention),
  so the 0 bps rung is a strict upper bound on what any execution could achieve, not a target.
