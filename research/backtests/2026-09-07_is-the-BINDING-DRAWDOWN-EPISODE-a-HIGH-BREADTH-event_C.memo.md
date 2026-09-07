# Idea 350 by-product — U56 breadth-gated equal weight — **4b KEEP-candidate** (lane C, 2026-09-07)

1. **Book.** Equal-weight EVERY name in universe.json at 75% gross, weekly, next-day
   execution, 10 bps; cut half the gross to CASH while panel breadth (share of the 55
   non-SPY names above their own 200d MA, read at t, executed t+1) is below 0.40.
2. **Exact RULES wording, if the Sunday review promotes it.** *"Hold every priced
   instrument in the universe at 0.75/N of NAV, rebalanced weekly. Compute breadth E as the
   share of priced instruments trading above their own 200-day moving average. If E < 0.40
   at the close, hold 0.375/N of NAV in each name and the remaining 37.5% of NAV in cash
   from the next open; restore full weights the day after E ≥ 0.40. No ranking, no
   volatility filter, no hysteresis."*
3. **Numbers @10 bps** (2009-01-13 .. 2026-09-04): 11.79% / **1.1916** / **-18.82%**,
   halves 1.2351 / 1.1560, OOS(2017-) 12.52% / **1.2367** / -18.82%.
4. **vs SPY** 15.23% / 0.889 / -33.72% (halves 0.957 / 0.834, OOS 0.882) — 4b bars H1
   ✓ +0.278, H2 ✓ +0.322, OOS ✓ +0.355, DD ✓ 1.41pp inside the -20.23% cap, CAGR ✓ 1.13pp
   above the 10.66% floor. **vs live RULES v2** 8.66% / 1.2056 / -12.05% (OOS 1.285) — 4a
   FAILS on drawdown and (narrowly) on H2, as every growth book does.
5. **Cost-robust:** 4b-clean at 0 / 10 / 25 bps (1.2184 / 1.1916 / 1.1512), and so are two
   neighbouring cells (B=0.30 d=0.25 and d=0.50) — three of nine grid points survive all
   three rungs, so this is not a single-cell artefact.
6. **Rule 8 selects it unaided.** Choosing (B, depth) on 2009-2016 IS Sharpe alone, from a
   ten-item menu that includes gate-OFF, picks exactly B=0.40 / depth 0.50; OOS Sharpe
   1.237 vs 1.136 for its own ungated control, regret 0.009 against the OOS-best cell.
7. **The gate is what makes it 4b-legal.** The ungated control (75% gross EWALL) reads
   13.27% / 1.1240 / **-22.53%** and FAILS the DD cap; the gate pays 1.47pp of CAGR for
   3.71pp of drawdown, a ratio of 2.52 against the free-alternative numeraire of 1.70
   (idea 351's bar), so it is not a de-grossing dial in disguise.
8. **Single-panel — the main weakness.** On B136 the identical construction fails 4b at
   **0 of 9** gate cells at 10 bps (DD cap missed at every one, -20.1% to -23.7%); on
   SMALL439, 0 of 27 at every rung. Promote it, if at all, as a **large-cap-universe rule
   with the universe stated**, exactly as idea 39's memo demanded.
9. **Not new in kind.** Idea 48's causal-quantile breadth cash gate (12.2% / 1.131 /
   -12.7%, OOS 1.240) is the same family at a different threshold and was PARKed; the
   Sunday review should treat these as one candidate with two parameterisations, not two.
10. **Caveats.** universe.json is a current-constituent list (SURVIVORSHIP) and 36 of 56
    names are ETFs, so the drawdown LEVEL that clears the 4b cap is optimistic; the gate
    arms on 11.0% of days, so the H1/H2/OOS margins rest on a handful of episodes; and
    the DD margin is 1.41pp, one bad month wide.
