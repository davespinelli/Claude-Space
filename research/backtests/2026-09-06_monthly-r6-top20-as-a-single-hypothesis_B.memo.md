# AMENDMENT memo — idea 182 (lane B), to the KEEP-candidate memo of the same date

This does **not** withdraw the cloud lane's KEEP-candidate. It replicates it independently
and adds one measurement that changes what the Sunday review should write down.

1. **Replication holds.** Independent simulator, control [F] vs `engine.backtest` at t+1:
   1.4e-17 on returns, 0.000e+00 on turnover, all three panels. Idea 173's published cell
   reproduces to 3.6e-05. The 9 u56 cells (5/10/25 bps × t+1/t+5/t+7 fill) all clear 4b
   full-sample and 4b-OOS, and 399 of 400 composition draws pass at a different seed.
2. **Clause 7 of the KEEP memo is wrong as written.** "MONTHLY is a k=1 calendar block, so it
   has exactly one phase" conflates block alignment with schedule anchoring. A monthly rule
   has ~21 possible trade-date anchors; the book prices exactly one of them (month-end).
3. **Measured.** Decision-to-fill gap held FIXED at one bar, whole schedule slid 0..7 bars,
   u56 @10 bps: MaxDD **-17.88% .. -20.39%** (range 2.51pp), Sharpe 1.0631 .. 1.1628,
   **4b passes 7 of 8**; phase 1 fails the drawdown cap outright at -20.39%.
4. **The margin is inside that band.** The published t+1 cell clears the -20.23% cap by
   1.42pp. Moving the trade one day later costs 1.58pp. Over all ten (gap, phase) cells
   measured, MaxDD spans -17.61% .. -24.41% and the cap sits inside the span.
5. **Control [G1]:** a 5-bar stale signal traded on the month-end bar IS a 5-bar delayed fill
   with the schedule slid back 4 bars (1.4e-17). The two lanes never disagreed about data —
   only about which reading of "one-week lag" was being priced.
6. **What this does NOT overturn:** scope (0/9 broad, 0/9 small), 4a failing everywhere,
   turnover 4.82x/yr, the rule-8 cadence result, the survivorship caveat, "do not tune it".
7. **Recommendation:** adopt as proposed, or hold — but adopt it as a **7-of-8** claim, not as
   a rule with a drawdown margin. Do not re-anchor the rebalance day to improve the margin;
   that would be fitting the exact statistic this memo says is noisy.
8. **Sizing implication:** anyone sizing off the -18.81% figure should size off roughly -20.4%,
   the worst phase of the identical rule, before adding live slippage.
9. **Open follow-up for the queue:** price all ~21 month anchors, not 8, and on broad as well —
   if the phase band is that wide for every monthly book in the record, the record's monthly
   drawdown claims need a phase column (cf. ideas 187/221/220).
10. **Script:** `research/backtests/2026-09-06_monthly-r6-top20-as-a-single-hypothesis_B.py`
    (controls [F] 1.4e-17 / 0.000e+00, [G1] 1.4e-17; 45 cells, 400 draws, 8 phases).

---

## Exact RULES wording — the two deltas to the proposed v2 text

Everything in the cloud lane's proposed RULES v2 stands except clauses 6 and 8, which should
read:

> 6. **Rebalance:** on the last trading day of each calendar month only. On that day, sell every
>    holding not in the new top 20 and buy every new entrant, then reset all positions to 3.75%
>    of NAV. There is no weekly rebalance and no top-up band. **The month-end anchor is part of
>    the rule and is not to be re-chosen: the identical rule anchored 1-8 trading days later
>    spans -17.88% to -20.39% full-sample MaxDD and fails the acceptance drawdown cap at one of
>    those eight anchors (idea 182B).**
>
> 8. **Trade price:** last close in the report (paper fill, no slippage modeled; note this as a
>    known bias). Backtested at 10 bps per unit turnover with next-day execution; the rule also
>    clears its acceptance bars at 25 bps and at a one-week delayed fill of the same month-end
>    decision. **It does NOT clear them if the signal itself is a week stale (-22.52% MaxDD at
>    5 bars, -24.41% at 7): the month-end close must be scored and traded on the same schedule.**
