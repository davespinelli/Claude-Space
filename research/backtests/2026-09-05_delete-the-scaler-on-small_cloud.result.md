# Idea 120 — delete-the-scaler-on-small (cloud, 2026-09-05)

**Verdict: KILL, and the KILL is larger than the idea. Idea 119's +11.7 pp scaler premium lives
entirely in names the book cannot buy: it survives no liquidity floor. At a $5M ADV floor the
unscaled book earns NEGATIVE CAGR in all 20 (n,g) cells, 0 of 640 grid points pass 4b, and the
rule-8 walk-forward pick loses 9.2%/yr out of sample. The no-ranking control shows the decay is
in the panel itself: equal-weighting every name that passes the floor decays monotonically from
Sharpe 0.680 (no floor) to 0.413 ($1M) to 0.181 ($5M) to -0.166 ($20M).**

Script: `2026-09-05_delete-the-scaler-on-small_cloud.py`. 640 grid points + 16 control points +
12 cost-ladder points + 10 capacity rows, all reported. Two tuned parameters: n in
{3,5,10,20,40}, g in {0.25,0.50,0.75,1.00}. Panel: 439 sub-$2B names (44 dropped for
max_1d_move >= 1.0), SPY benchmark only, weekly, next-day, 10 bps.

## 0. Harness and reproduction
Vectorised simulator vs `engine.backtest`: max|diff| **1.4e-17**. Idea 119's unscreened pair
reproduces: scaler on 8.55%/0.628/-32.8% at 33.4x turnover, scaler off 18.18%/0.676/-39.8% at
21.5x — a **+9.64 pp / +0.048 / -11.9x** delta against idea 119's published +11.7 pp / +0.15 /
-11.8x (the CAGR and turnover gaps agree; the Sharpe gap is smaller here because this run starts
the evaluation at the 260-day warm-up and holds SPY out of the selectable set).
Live RULES v1 on this panel: 8.15%/0.603/-32.8%. SPY: 14.13%/0.862/-33.7%, halves 0.891/0.858,
OOS 0.882 — so 4b's bars are MaxDD >= -20.2% and CAGR >= 9.89%.

## 1. The premium does not survive tradeability (P1 CONFIRMED)
Scaler-off minus scaler-on dCAGR, ungated, matched gross, median over the 20 (n,g) cells:

| ADV floor | median dCAGR | median dSharpe | cells with dCAGR > 0 |
|---|---|---|---|
| none | **+5.35 pp** | +0.045 | **20/20** |
| $1M | +0.43 pp | -0.043 | 13/20 |
| $5M | **-2.22 pp** | -0.099 | **1/20** |
| $20M | -1.31 pp | +0.004 | 1/20 |

At n=5, g=0.75 the premium goes +9.64 pp (no floor) -> +4.56 ($1M) -> **-1.61** ($5M) -> -2.03
($20M). The sign flips between $1M and $5M. Idea 119's largest-single-component effect in this
project is a sub-$1M-ADV effect.

## 2. Nothing on the far side of the screen is investable (P2 CONFIRMED)
**0 of 640 grid points pass 4b** (20 pass 4a, all of them at the no-floor end). Every one of the
20 headline cells (floor $5M, ungated, scaler off, matched gross) has negative CAGR, from
-0.10% (n=40, g=0.25) to -13.95% (n=3, g=1.00), with drawdowns of -27% to -96%. The book is not
merely short of 4b's bars; it loses money.

## 3. Walk-forward (PROTOCOL rule 8) (P3 CONFIRMED)
(n,g) chosen on 2011-01-13..2016-12-31 only, at the pre-registered $5M floor; 2017-2026 read once.
- S1 (argmax IS Sharpe): n=20, g=1.00. IS Sharpe 0.241 vs SPY IS 0.832. **OOS -9.17%/-0.171/-83.4%**.
- S2 (argmax IS Sharpe subject to IS MaxDD <= 60% of SPY's): n=20, g=0.25. **OOS -1.56%/-0.174/-33.5%**.
- Benchmarks OOS: SPY 15.45%/0.882/-33.7%; live v1 on this panel 7.92%/0.581/-32.8%.
Both picks fail 4a and 4b. Costs do not rescue them: at 0 bps the n=5, g=0.75 anchor is still
-2.45%/0.068 and the S1 pick -2.73%/0.037.

## 4. The no-ranking control — it is the panel, not just the ranking
Equal-weighting **every** name that passes the floor (no composite, no ranking, no scaler, no
gate), at g=0.75:

| ADV floor | names held | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|---|
| none | 348 | 10.18% | 0.678 | -36.2% | 0.797 / 0.614 | 0.637 |
| $1M | 252 | 5.92% | 0.413 | -39.9% | 0.509 / 0.347 | 0.377 |
| $5M | 141 | 1.64% | 0.181 | -47.5% | 0.324 / 0.075 | 0.124 |
| $20M | 44 | -4.92% | -0.163 | -69.3% | 0.133 / -0.398 | -0.340 |

Return decays monotonically in the ADV floor with no ranking involved at all. On top of that the
unscaled ranking **subtracts** a further -6.15 pp of CAGR and -0.184 of Sharpe at the $5M floor
(1.64%/0.181 control vs -4.51%/-0.003 for the ranked n=5 book) — the same sign idea 82 found on
the large-cap panels.

## 5. Capacity (P4 REFUTED, in the book's favour, and it does not save it)
At the $5M floor the held names have median dollar ADV $14.5M (p25 $8.3M) at n=5, so $10M of
capital trades **5.6%** of a held name's ADV per rebalance, not the >10% predicted; at $100M it
is 56%. Unscreened, the same book holds names at $3.7M median ADV and trades 22.5% at $10M.
The screen does buy real capacity — it just buys it by removing the only names that paid.

## 6. Survivorship — this is the finding that should be quoted
`data/prices_small.csv.gz` is the **current constituent list** of a sub-$2B screen: every name in
it survived to 2026. The bias falls hardest on the smallest and thinnest names, which is exactly
the cohort the ADV floor removes. So the monotone decay in table 4 is what the bias predicts:
the illiquid survivors carry the whole return of this panel. The honest reading is not "small
caps stop working above $5M ADV" but **"the small panel's apparent edge is concentrated in the
part of the panel where its survivorship bias is largest, and the part that survives a
tradeability screen has no edge at all."** No level in this run is an achievable return, and
every prior small-panel row in this project (ideas 31, 38, 49, 50, 51, 54, 97, 119) inherits the
same exposure — which is idea 121's case, and this run is evidence for it.
