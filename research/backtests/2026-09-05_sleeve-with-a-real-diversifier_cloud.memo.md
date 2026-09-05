# Memo — the wording a `top20 + 50% S4` rule would take (NOT adoptable this week)

1. **Status: PARK.** This is the wording the Sunday review would need *if* idea 101's
   pre-registered fixed-gross run reproduces the numbers below. It is not a KEEP: the 4b pass
   depends on a third dial (exposure) that this run did not pre-register.
2. **Eligible set.** Each week, every name above its 200-day moving average with 20-day realised
   vol under 0.60.
3. **Equity sleeve (75% of the book's risk weight).** Hold the top 20 eligible names by the v1
   composite computed **without** the `/sqrt(vol20)` scaler, equally weighted.
4. **Diversifier sleeve (25% of the book's risk weight).** Hold TLT, GLD, DBC and UUP at
   inverse-60-day-vol risk parity, each scaled by its own trend vote: the fraction of
   {12-1 month, 6 month, 3 month} returns that are positive.
5. **Mix.** Blend the two sleeves 50/50 by target weight, then **rescale the blended row to 100%
   of capital**. Long only, no leverage — the rescale never exceeds 1.00.
6. **Cadence and execution.** Rebalance weekly on the last trading day; weights decided at close
   t are executed at close t+1. Costs assumed 10 bps per unit turnover.
7. **Measured (2009-01→2026-09, 10 bps, both universes):** universe.json 11.8% CAGR / 1.149 Sharpe
   / −14.2% MaxDD, halves 1.099 / 1.197, OOS (2017+) 1.236; universe_broad.json 12.2% / 1.063 /
   −15.6%, halves 1.173 / 0.961, OOS 1.020. SPY 15.2% / 0.889 / −33.7%.
8. **Against idea 2's standing candidate.** It gives up 0.9pp of CAGR on both universes and buys
   4.1pp / 4.5pp of MaxDD and +0.057 / +0.106 of Sharpe — an exchange rate of **0.20–0.22pp of
   CAGR per pp of MaxDD**, level with the cheapest instrument on idea 94's menu (band3-rw at 0.18)
   and unlike it also Sharpe-positive.
9. **Blocking before adoption:** (a) the full 5/10/15/20/25 bps ladder at fixed g = 1.00, which
   this run did not do; (b) idea 65's cadence-insensitivity bar; (c) idea 102 — whether the sleeve
   is TLT in a falling-rate sample.
10. **Survivorship / regime caveat must ship with the rule:** both equity panels are current
    constituents, and the sleeve's one materially positive year (2022) is also the only year its
    duration vote was short.
