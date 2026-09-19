# MEMO — idea 1670 (lane cloud, 2026-09-19): the 1674 static-twin verdict SPLITS BY AXIS — the band's DRAWDOWN credit is panel-independent, its SHARPE credit is a U56 fact that is already gone at the live 10 bps rung

1. **WHAT WAS TESTED.** Idea 1674 (U56 only) killed the hypothesis that the clause-6 band book is a static equity/SHY mix: at MATCHED mean equity exposure the candidate was shallower in 20 of 20 and higher OOS Sharpe in 20 of 20. This run re-prices the IDENTICAL contest on B136 and SMALL, with **U56 carried as a replication control**. Two dials (panel, mix rung `a`); candidate gross `G` {0.50 … 1.00} is 1674's ladder, not re-tuned. **276 grid cells and 60 paired contrasts, every one published**, cost axis {0, 10, 25, 50} bps derived EXACTLY off the c=0 run (G14 = 0.000e+00). SMALL: 54 tickers with `max_1d_move ≥ 1.0` dropped (665 tradable), SHY joined from `data/prices.csv` as a benchmark sleeve (G9/G10).
2. **THE CONTROL REPLICATES 1674 TO FOUR DECIMALS.** U56 STATIC a = 0.60 @10 bps: **OOS 11.84% / 1.1899 / −17.98%** — 1674's figure exactly. Paired: dMaxDD shallower **20 of 20, mean +4.18 pp** (1674: +4.10); dSharpe_OOS > 0 **20 of 20, mean +0.1081** (1674: +0.1085); dCAGR > 0 **0 of 20, mean −1.10 pp** (1674: −1.07); turnover **2.84x vs 0.80x** (1674: 2.79x/0.80x). The residual gap is one construction difference, stated: 1674's candidate band-gated SHY as a 56th equity name via `rules_v2_weights`; this one reserves SHY for the defensive leg on all three panels so the contest is identical across them.
3. **THE DRAWDOWN HALF PORTS — CLEANLY, ON ALL THREE PANELS.** MaxDD shallower than the exposure-matched twin in **20 of 20 on U56 (+4.18 pp), 20 of 20 on B136 (+5.36 pp) and 20 of 20 on SMALL (+5.31 pp)** — 60 of 60. At matched average exposure the 200d band buys real drawdown, and it buys MORE of it off U56, not less.
4. **THE SHARPE HALF DOES NOT PORT. THIS IS THE RUN'S FINDING.** dSharpe_OOS > 0 in **20 of 20 on U56 (mean +0.1081)** but only **10 of 20 on B136 (mean −0.0193)** and **7 of 20 on SMALL (mean −0.0431)**. Both halves > 0: **10/20 U56, 2/20 B136, 0/20 SMALL.** 1674's 20-of-20 OOS Sharpe result is a U56 fact.
5. **AND THE MECHANISM IS TURNOVER, NOT THE TAPE.** Mean dSharpe FULL by panel × cost: at **0 bps** all three are positive (**+0.1039 / +0.0143 / +0.0100**); at the **live 10 bps rung** U56 is **+0.0742** while B136 is **−0.0183** and SMALL is **−0.0286**; at 50 bps all three are negative (−0.0451 / −0.1488 / −0.1835). The band's gross credit survives everywhere; its NET credit survives only where its turnover is cheapest. Candidate turnover runs **2.84x / 3.06x / 3.48x per year** against twins at **0.80x / 0.83x / 1.10x**.
6. **CAGR IS THE BILL, AND IT IS BIGGER OFF U56.** dCAGR > 0 in **0 of 20 on every panel**; mean **−1.10 pp (U56), −2.37 pp (B136), −1.74 pp (SMALL)**. At G = 0.75 / 10 bps the candidate pays **−0.84 / −2.10 / −1.46 pp** of CAGR for **+4.08 / +6.07 / +6.13 pp** of drawdown.
7. **RULE 8 — 1674's CANDIDATE PARTIALLY PORTS.** Six choosers fitted on rows ≤ 2016-12-31, 2017-2026 read once. `C_MEMO_STATIC` (the record's own pre-stated 2026-09-03 rule) clears 4b OOS **4 of 4 cost rungs on U56**, **3 of 4 on B136** (fails at 50 bps), **0 of 4 on SMALL**. `C_MEMO_CAND` clears **1/4, 2/4, 0/4**. `C_SHARPE`, `C_CAGR`, `C_CALMAR` and `C_LIVE` clear **0 of 12 on every panel**.
8. **THE B136 CONFIRMATION, IN FULL.** STATIC a = 0.60, weekly, 10 bps, B136: **FULL 11.85% / 1.1675 / −20.18%**, halves **1.2744 / 1.0733** vs SPY 0.9571 / 0.8249; **OOS 11.77% / 1.1521 / −20.18%** vs SPY OOS **15.26% / 0.8737 / −33.72%** (floor 10.68%, cap −20.23%) and the live book's 7.85% / 1.1017 / −12.24%. 4b FULL **and** OOS PASS at 0/10/25 bps; the OOS DD cap is cleared by **0.05 pp** — a hair, and it is reported as a hair. Turnover 0.91x/yr. **On SMALL the same rule gives 8.68% / 0.7462 / −28.30%, halves 0.9919 / 0.6299, OOS 8.11% / 0.6448 — 4b FAIL at every rung on both the Sharpe and the CAGR floor.**
9. **HEAD TO HEAD, THE HONEST SUMMARY.** The gated candidate (CAND G = 1.00) beats the static mix on U56 at 0/10 bps and loses it by 25 bps; on **B136 it is beaten at every rung ≥ 10 bps** (1.1178 vs 1.1675 at 10 bps) and on **SMALL at every rung except 0** — at **4.1x and 4.6x the turnover**. Off U56 the gate is unpaid trading.
10. **LIMITS AND ENACTMENT.** Survivorship (rule 9): all three panels are **current-constituent** lists, so every absolute level — both 4b passes included — is an **UPPER BOUND**; the candidate-minus-twin contrast is same-names/same-days/same-exposure and first-order immune. SMALL's pool additionally post-dates 2010 and carries the `data/SMALL_PANEL_README.md` caveats. SHY is a marked-to-market 1-3y Treasury sleeve that lost money in 2022, not a sweep rate. **NOTHING IS ENACTED** — PROTOCOL rule 6 reserves enactment for the Sunday review; RULES.md, scan.py, bot.py and baseline.py are untouched by this run.

## Exact RULES wording if the Sunday review adopts the 4b candidate (replaces clauses 1-3 wholesale)

> **Clause 1 (universe).** Every instrument in `research/universe.json` priced that day, excluding
> `BTC-USD` and `ETH-USD`, and excluding `SHY`, which is reserved for clause 3. **Scope: this rule
> is validated on the U56 and B136 panels only. It is NOT validated on sub-$2B names — idea 1670
> shows it fails path 4b on the SMALL panel at every cost rung — and may not be applied there.**
>
> **Clause 2 (equity leg).** Hold every clause-1 instrument at **0.60 / N** of NAV, where N is the
> number of clause-1 instruments priced that day. **No trend gate, no ranking, no volatility
> filter.** Rebalance weekly on the last trading day of the week, executed at the next close.
>
> **Clause 3 (defensive leg).** Hold the remaining **0.40** of NAV in `SHY`, rebalanced on the same
> weekly schedule. Never levered, never shorted, never re-spread into the equity leg.
>
> **Clause 4 (costs).** 10 bps per unit of turnover, charged on both legs. **At 50 bps the rule
> fails 4b OOS on B136; it is not authorised above 25 bps of round-trip cost.**
>
> The single parameter 0.60 is fixed by the 2026-09-03 rule — *the smallest equity weight whose
> MaxDD ≤ 60% of SPY's and CAGR ≥ 70% of SPY's* — evaluated on 2009-2016 data only and left
> untouched thereafter. It is the pick of `C_MEMO_STATIC` on **both** U56 and B136.
