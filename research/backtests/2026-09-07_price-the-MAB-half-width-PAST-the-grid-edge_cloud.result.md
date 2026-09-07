# Idea 390 — price the MAB half-width PAST the grid edge (cloud, 2026-09-07)

**Verdict: MIXED (pre-registered reading). No KEEP. The grid-edge flag clears on 2 panels and relocates on 2.**

Book: idea 387 leg-C / idea 389 verbatim — `score(vol_scale=False)` ranked inside the 200d
collar, top n=20, equal weight at 0.75 gross, weekly, next-day execution. Only the dial
moved: b in {0.00, 0.03, 0.06, 0.12, **0.20, 0.30, 0.50**} plus a **gate-OFF** arm, on
4 panels (U56, B136, SMALL439, ETF36) x 3 cost rungs. 96 cells, all reported in `.grid.csv`.
Two tuned parameters: b and the panel.

## 1. The structural point, stated before the numbers and then confirmed

`baseline.band_state(px, b)` is a **hysteresis collar**: IN above `ma*(1+b)`, OUT below
`ma*(1-b)`, previous state in between, starting OUT. Widening b does **not** interpolate
towards "no gate" — it interpolates towards "never change state", whose fixed point from an
OUT start is **permanent exclusion**. The b -> infinity limit of this instrument is an
**all-cash book**, not a gate-off book.

Confirmed by the mechanism columns (b=0 -> b=0.50): `in_share` (share of priced name-days
held IN) 0.675 -> 0.181 on U56 and 0.662 -> **0.062** on ETF36; ETF36 `cash_days`
0.0% -> **12.0%** and mean names held 18.0 -> **2.1**. Gate-off is therefore a separate arm
the b ladder cannot reach, and a widest-rung argmax is **not** evidence for turning the
gate off.

## 2. Where the argmax actually is (@10 bps, full-sample Sharpe)

| panel | b=0 | 0.03 | 0.06 | 0.12 | 0.20 | 0.30 | 0.50 | OFF | argmax |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 1.064 | 1.090 | 1.079 | **1.130** | 1.075 | 1.102 | 1.068 | 1.105 | **0.12 (interior)** |
| B136 | 0.943 | 0.949 | 0.930 | 0.972 | 0.959 | 0.953 | **1.105** | 0.942 | 0.50 (new edge) |
| SMALL439 | 0.450 | 0.451 | 0.430 | 0.436 | 0.448 | 0.429 | **0.513** | 0.424 | 0.50 (new edge) |
| ETF36 | 0.673 | 0.764 | 0.755 | **0.856** | 0.783 | 0.559 | 0.222 | 0.855 | **0.12 (interior)** |

- Interior argmax on **2/4** panels @10 bps (6/12 across all cost rungs); the curve turns
  down by b=0.50 on the same 2.
- **Gate-OFF beats the whole b ladder on 0/4 panels @10 bps** (1/12 across all cost rungs,
  ETF36 @0 bps by +0.025). The "the instrument is simply turn the gate off" hypothesis is
  rejected.
- On B136 and SMALL439 the argmax is at 0.50, the new widest rung — idea 240/256's
  grid-edge flag is **not retired, it relocated**.

## 3. Idea 387's standing U56 candidate survives — on a nearly flat ladder

U56 b=0.12 @10 bps: CAGR 13.89%, Sharpe 1.130, MaxDD -18.72%, H1/H2 1.077/1.180, OOS
Sharpe **1.2384**. It beats every wider rung (0.20 -0.055, 0.30 -0.028, 0.50 -0.062) and
gate-OFF (-0.025), clears **4b at 0, 10 and 25 bps**, and the rule-8 IS chooser still picks
it. **4a fails** (MaxDD -18.7% vs RULES v2's -12.1%).

**Caveat that belongs next to that claim:** the entire 8-rung U56 Sharpe spread is
**0.0662**, and the curve is non-monotone (b=0.20 sits *below* b=0.30). The interior peak is
a wiggle, not a ridge; the honest reading of U56 is that the dial is close to inert and 0.12
is the top of the noise.

## 4. What the new rungs buy, and why 4b refuses it

The three new rungs contribute **zero** 4b passers on any panel at any cost rung. All 15
passing cells in the run are U56 or B136 at b <= 0.12 or gate-OFF. 4a passes **0/96**.

Widening b buys CAGR and pays in drawdown — U56 12.79% -> 19.19% CAGR against
-18.31% -> -29.57% MaxDD — which is exactly the trade 4b's DD cap (60% of SPY's -33.72%,
i.e. -20.23%) exists to refuse. Failing bars @10 bps: H2 22, DD 20, H1 17, CAGR 16, OOS 14.

The best new-rung cell is **B136 b=0.50 @10 bps** (17.77% / 1.105 / -23.67%, H1/H2
1.174/1.039, OOS 1.124): it **fails 4b on the DD bar alone** and fails 4a. It is a turnover
story, not a selection story — turnover halves (14.31 -> 6.85 x/yr) and `in_share` falls
0.674 -> 0.209 while names held barely move (19.7 -> 18.3). The wide collar freezes the
book; it does not pick better names.

## 5. Rule 8

b chosen on IS 2008-2016 Sharpe @10 bps, 2017-2026 read once, three grid scopes:

| scope | above SPY OOS | above RULES v2 OOS | above b=0 anchor | mean regret | 4b |
|---|---|---|---|---|---|
| old grid (<=0.12) | 3/4 | 0/4 | 3/4 | +0.0107 | 1/4 |
| b-ladder (to 0.50) | 3/4 | 1/4 | 3/4 | +0.0361 | 1/4 |
| ladder + gate-OFF | 2/4 | 1/4 | 3/4 | +0.0622 | 1/4 |

Widening the grid changed the chooser's pick on **1 of 4** panels (B136, 0.12 -> 0.50) and
that one change paid **+0.2249** of OOS Sharpe (mean +0.0562 over 4 panels). Putting
gate-OFF on the chooser's menu makes it **worse**: OFF wins the IS beauty contest on U56 and
ETF36 and loses OOS both times.

## 6. Gates

G1/G2 `fast_backtest` vs `engine.backtest` **0.000e+00** on returns and turnover at 0 and 25
bps. G3 `band_state(b=0)` == `px > ma200` on **0/242,015** where the MA is defined. **G4 all
48 incumbent cells reproduce idea 389's committed `grid.csv` to max|d| 3.553e-15** — this run
is a strict superset of the published grid. G5 the gate-OFF arm is all-True wherever a price
exists.

## 7. Caveats

1. **SURVIVORSHIP** — all four panels are current-constituent lists. SMALL439 is the
   sub-$2B screen with `max_1d_move >= 1.0` names dropped, as required; its 4b CAGR floor is
   tested in the book's favour.
2. ETF36 is a 36-name subset of B136 — four panels is not four independent samples.
3. Widening b changes the eligible set, not the gross: `weights_from` always re-spreads 0.75
   gross over whatever is held, so a thinner collar **concentrates** until the eligible set
   empties, at which point the book goes to cash. Both regimes appear in the run (B136/SMALL439
   in the first, ETF36 in the second).
