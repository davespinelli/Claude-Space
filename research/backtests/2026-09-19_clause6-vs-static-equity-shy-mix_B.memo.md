# MEMO — idea 1674 (lane B, 2026-09-19): the clause-6 candidate is NOT a static mix, and the thing that clears 4b under rule 8 has no trend rule in it at all

1. **WHAT WAS TESTED.** Ideas 1498/1555 made the SHY residual the record's only Sharpe-lifting device (4a PASS, U56/LIVE band 0.03, G 0.75, F 1.00). Its twin is not a de-gross: it is a **STATIC equity/SHY mix held at the candidate's own MEAN equity exposure**. Two dials — candidate gross `G` {0.50 … 1.00} and static equity weight `a` (8 published rungs **plus** the exposure-matched value solved per `G` by bisection to 2.3e-06) — **92 cells, every one published**, cost axis {0, 10, 25, 50} bps derived exactly off the c=0 run (gate G1 = 0.000e+00). 8 of 8 gates pass, including G2: clause 6 changes only the SHY line of `baseline.rules_v2_weights` (0.000e+00).
2. **THE HYPOTHESIS IS KILLED — the band is not a static mix.** Candidate minus exposure-matched twin over 20 (G, cost) pairs: **MaxDD shallower in 20 of 20** (mean **+4.10 pp**, +4.00 pp at the live G=0.75/10 bps) and **OOS Sharpe higher in 20 of 20** (mean **+0.1085**). The 200d band buys real drawdown at matched average exposure.
3. **AND IT IS PAID FOR, IN THE TWO CURRENCIES THAT MATTER.** **CAGR is lower in 20 of 20** (mean **−1.07 pp**; −0.83 pp at G=0.75) and turnover is **2.79x/yr against the twin's 0.80x**. The full-sample Sharpe edge is **cost-fragile**: +0.0740 at 10 bps, +0.0294 at 25 bps, **−0.0452 at 50 bps**, and it reverses in **5 of 5** G rungs at 50 bps. Both halves positive in only **10 of 20** — the H1 leg is already negative at 25 bps.
4. **RULE 8, AND IT IS THE RUN'S REAL FINDING.** Six choosers fitted on rows ≤ 2016-12-31, 2017-2026 read once. `C_SHARPE`/`C_CALMAR` pick CAND 0.50 (0/10 bps) then STATIC 0.40 (25/50) — **0 of 8 clears 4b OOS** (CAGR floor). `C_CAGR` picks STATIC 1.00 — fails the DD cap at 4 of 4. **`C_MEMO_STATIC`** — the record's OWN pre-stated 2026-09-03 rule ("smallest dial whose MaxDD ≤ 60% of SPY's and CAGR ≥ 70% of SPY's"), applied to IS rows only — picks **a = 0.60** at 0/10 bps and **a = 0.65** at 25/50, and **clears 4b OOS at 4 of 4 cost rungs**. `C_MEMO_CAND` picks CAND 1.00 at 0 bps (4b OOS PASS) but falls back to CAND 0.75 at 10/25/50 bps and **fails 4b OOS at 3 of 4** — the gated family's memo pick is cost-unstable, the ungated family's is not.
5. **THE KEEP-4b CANDIDATE (path 4b, rule-8 legitimate, ONE tuned parameter).** STATIC a = 0.60, weekly, 10 bps: **FULL 11.28% / 1.1728 / −17.98%**, halves **1.2353 / 1.1255** against SPY's 0.9570 / 0.8249; **OOS 11.84% / 1.1899 / −17.98%** against SPY OOS **15.26% / 0.8737 / −33.72%** (floor 10.68%, cap −20.23%). It clears 4b **FULL and OOS at 0, 10, 25 AND 50 bps** — turnover **0.88x/yr**. There is no trend rule, no ranking and no vol filter in it: it is every U56 name equal-weighted at 60% of NAV with 40% in SHY.
6. **HEAD TO HEAD WITH THE GATED BOOK.** CAND G=1.00 (band + clause 6) beats it on every axis at 10 bps — 11.73% / 1.2203 / −15.64% vs 11.28% / 1.1728 / −17.98% — at **4.2x the turnover**, and **loses 4b FULL at 50 bps (1.0622)** where the static mix still passes (1.1356). The gate is worth roughly 0.05 of Sharpe and 2.3 pp of drawdown per 2.8x/yr of extra trading, and that trade stops paying somewhere between 25 and 50 bps.
7. **PATH 4a IS CLEARABLE WITH NO DEVICE AT ALL.** The exposure-matched twin of CAND 0.50 (a ≈ 0.347, ungated) clears 4a at all four cost rungs: 7.06% / 1.2664 / −11.25%, halves 1.3135 / 1.2362 against the live book's 1.2276 / 1.1805, MaxDD shallower. 19 of 92 cells clear 4a and **8 of them carry no gate**.
8. **HONEST LABEL: THIS IS DE-RISKING, NOT ALPHA — AND IT IS A STATEMENT ABOUT THE 4b BAR.** The candidate's CAGR (11.28%) is **3.84 pp BELOW SPY**. It clears 4b only because 4b asks for 70% of SPY's return at 60% of SPY's drawdown, which any sufficiently diversified de-grossed book delivers in a 17.7-year equity bull sample. Idea 1600's deflation applies in full: nothing here forecasts anything.
9. **LIMITS.** Survivorship (rule 9): U56 is a **current-constituent** list, so every absolute level — including the 4b pass — is an **UPPER BOUND**; the candidate-minus-twin contrast is same-names/same-days/same-exposure and is first-order immune, the 4b pass is **NOT**. SHY is a marked-to-market 1-3y Treasury sleeve that lost money in 2022, not a sweep rate. One panel (U56) only — portability to B136/SMALL is filed as idea 1670; the band's timing-vs-frequency decomposition as idea 1666.
10. **NOTHING IS ENACTED.** PROTOCOL rule 6 reserves enactment for the Sunday review; RULES.md, scan.py, bot.py and baseline.py are untouched by this run.

## Exact RULES wording if the Sunday review adopts the 4b candidate (replaces clauses 1-3 wholesale)

> **Clause 1 (universe).** Every instrument in `research/universe.json` priced that day, excluding
> `BTC-USD` and `ETH-USD`, and excluding `SHY`, which is reserved for clause 3.
>
> **Clause 2 (equity leg).** Hold every clause-1 instrument at **0.60 / N** of NAV, where N is the
> number of clause-1 instruments priced that day. **No trend gate, no ranking, no volatility
> filter.** Rebalance weekly on the last trading day of the week, executed at the next close.
>
> **Clause 3 (defensive leg).** Hold the remaining **0.40** of NAV in `SHY`, rebalanced on the same
> weekly schedule. Never levered, never shorted, never re-spread into the equity leg.
>
> **Clause 4 (costs).** 10 bps per unit of turnover, charged on both legs.
>
> The single parameter 0.60 is fixed by the 2026-09-03 rule — *the smallest equity weight whose
> MaxDD ≤ 60% of SPY's and CAGR ≥ 70% of SPY's* — evaluated on 2009-2016 data only and left
> untouched thereafter.
