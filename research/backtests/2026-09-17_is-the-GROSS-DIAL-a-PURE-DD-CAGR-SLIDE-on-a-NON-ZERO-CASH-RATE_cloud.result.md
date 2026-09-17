# Idea 1193 — is the GROSS DIAL a PURE DD/CAGR SLIDE on a NON-ZERO CASH RATE?  **KILL**

Run 2026-09-17, lane cloud, idea 1 of 2. Script:
`research/backtests/2026-09-17_is-the-GROSS-DIAL-a-PURE-DD-CAGR-SLIDE-on-a-NON-ZERO-CASH-RATE_cloud.py`
Book = the 2026-09-04 KEEP 4b book (composite, NO vol scaler / above-200d / N=20 / equal weight /
weekly / 10 bps / next-day execution). Grid = 8 gross rungs x 5 cash rates x 2 panels = 80 points,
all reported in `.ladder.csv`; 2 tuned params only (gross rung, cash rate).

## The answer: it depends entirely on which Sharpe the record means, and neither reading is a dial worth turning

| U56 | cash 0% | 2% | 4% | 5.4% | SHY (1.32%/yr realised) |
|---|---|---|---|---|---|
| SH0 rung spread (rf=0, the record's convention) | 0.0009 (**0.08%** of mean) | 0.2841 (22.8%) | 0.5691 (42.3%) | 0.7686 (**54.3%**) | 0.1841 (15.2%) |
| SH_ex rung spread (excess return vs the same cash) | 0.0009 (0.08%) | 0.0014 (0.14%) | 0.0019 (0.21%) | 0.0022 (**0.27%**) | 0.0009 (0.09%) |
| SH0 argmax rung | 0.90 | 0.30 | 0.30 | 0.30 | 0.30 |
| SH_ex argmax rung | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 |

B136 reads the same (SH0 0.74% -> 52.1% of mean; SH_ex 0.74% -> 1.19%).

1189's degeneracy is reproduced exactly at cash = 0 (0.08% of mean, vs its published 0.561% median
over its own cells). Turning cash on does **not** make gross a live risk-adjusted dial: on excess
returns the spread stays under 0.3% of its mean at every rate on U56 and under 1.2% on B136. What
moves is the *rf=0 convention alone*: with the sleeve earning c, SH0 = mu/sigma + c(1-g)/(g*sigma),
which is monotone decreasing in g by construction. So the 54% spread is a de-risking identity, not
a selection signal — its argmax is the smallest rung on the ladder at every non-zero rate, and would
be smaller still if the ladder went lower. A dial whose optimum is "hold as little equity as
possible" is not a portfolio claim.

## Rule 8 walk-forward (rung chosen on H1 by each criterion, H2 read once): 0 of 20 cells pass 4b

| U56 cell | pick | OOS CAGR | OOS SH0 | OOS MaxDD | base SH0 / DD | SPY CAGR / SH0 / DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| cash 0%, either crit | 0.90 | 17.94% | 1.095 | -23.00% | 1.177 / -12.05% | 14.76% / 0.823 / -33.72% | no | no |
| cash 4%, SH0 | 0.30 | 9.01% | 1.620 | -7.87% | 1.429 / -11.96% | 14.76% / 0.823 / -33.72% | **yes** | no |
| cash 4%, SH_ex | 1.00 | 20.14% | 1.105 | -25.37% | 1.429 / -11.96% | 14.76% / 0.823 / -33.72% | no | no |
| cash 5.4%, SH0 | 0.30 | 10.10% | 1.804 | -7.81% | 1.517 / -11.92% | 14.76% / 0.823 / -33.72% | **yes** | no |
| cash SHY, SH0 | 0.30 | 7.33% | 1.311 | -8.01% | 1.275 / -11.47% | 14.76% / 0.823 / -33.72% | **yes** | no |

The SH0 criterion picks gross 0.30 and then misses 4b's CAGR floor by 5-7pp; the SH_ex criterion
picks gross 1.00 and busts the DD cap (-25.4% against -20.23%). 6 of 20 walk-forward cells clear 4a
(all of them the minimum-gross pick against a low-return live book — 4a's own known failure mode),
**0 of 20 clear 4b**. KILL.

## Secondary finding worth carrying: 4b's CAGR leg is cash-rate-dependent and no memo states a rate

Full-sample 4b passes on U56 go 6 -> 6 -> 8 -> 10 (of 8 rungs each) as the assumed cash rate goes
0% -> 2% -> 4% -> 5.4%; B136 goes 0 -> 4 -> 4 -> 5. The mechanism is one-sided: the book's cash
sleeve is credited while the fully-invested SPY comparand is not, so the CAGR floor (>= 70% of SPY)
slides down the ladder — the failing boundary moves 0.6 -> 0.5 -> 0.4. The **DD cap boundary does
not move at all** (0.70 passes, 0.80 fails at every one of the five rates, both panels). So every
committed 4b verdict in the record carries an unstated cash-rate assumption on exactly one of its
four legs, and the record's implicit 0% is the *strictest* choice.

The incumbent's own gross of 0.75 sits inside that pinch: on U56 the last passing rung is 0.70
(MaxDD -18.18%) and the first failing rung is 0.80 (-20.60%) against a cap of -20.23%, at every
cash rate. That is the same boundary idea 1257 found decided at 3.6e-05.

## Caveats
Survivorship: U56 and B136 are current constituents. SHY is a 1-3y Treasury ETF (~1.9y duration),
a total-return proxy for the short rate, not a bill — it carries duration P&L, which is why its
realised 1.32%/yr understates the period's average bill yield. Flat rungs are applied at 252 d/yr
with no reinvestment path. No rung below 0.30 was walked; the SH0 argmax is a ladder endpoint.
