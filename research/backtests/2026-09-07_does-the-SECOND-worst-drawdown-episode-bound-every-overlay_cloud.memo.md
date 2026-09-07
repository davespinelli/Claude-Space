# MEMO — 4b KEEP-candidate: EWALL + 12% vol target (idea 374 by-product, 2026-09-07 cloud)

1. **RULES wording (exact).** *Hold every priced name in the universe at `g/N` of NAV, `g = 0.75`,
   `N` = names priced that day, rebalanced weekly. Multiply every weight by
   `k_t = min(1, 0.12 / sigma_{t-1})`, where `sigma_{t-1}` is the annualised 20-day standard
   deviation of the book's own daily returns through the prior close. Un-invested weight is CASH;
   never lever (`k_t <= 1`). No ranking, no trend filter, no vol-eligibility screen.*
2. **What it is.** RULES v2's un-gated parent (no 200d band) with one exposure dial: a 12% realised-
   vol target on the book, not on the names. Two moving parts total (`g`, `t`).
3. **Numbers, U56 @10 bps:** 11.68% / 1.202 / -15.82%, halves 1.287 / 1.126, OOS 1.212,
   turnover 1.39x NAV/yr, realised mean gross 0.700.
4. **Numbers, B136 @10 bps:** 11.95% / 1.205 / -14.76%, halves 1.344 / 1.073, OOS 1.183,
   turnover 1.46x, gross 0.692. SPY: 15.23% / 0.889 / -33.72%, halves 0.957/0.834, OOS 0.882.
5. **4b PASS on both panels at 0, 10 and 25 bps** (6/6 cells). Tightest bar is the CAGR floor:
   margins +1.17/+1.02/+0.79 pp (U56) and +1.45/+1.29/+1.04 pp (B136) at 0/10/25 bps; DD slack
   4.1-5.5 pp. **4a FAILS** (DD, plus H2 on U56) — RULES v2 draws -12.05% and earns 8.66%.
6. **Not a gross-ladder point (ideas 311/351).** Against the static-gross ladder solved to its own
   realised mean gross (residual <= 6.6e-06): Sharpe 18/27, OOS Sharpe 18/27, MaxDD **27/27**;
   matched ladder points clear 4b **0/27**, the overlay 16/27. It buys ~5.3 pp (U56) / ~8.8 pp
   (B136) more drawdown than the same exposure bought statically, at *positive* Sharpe.
7. **Rule 8 selects it.** IS <= 2016 Sharpe over the full 23-point overlay menu picks `t=0.12` in
   6/6 U56+B136 EWALL cells (`t=0.15` at B136 @25 bps, also 4b), beats its own base book OOS 6/6,
   beats live RULES v2 OOS 4/6, regret 0.036-0.070.
8. **Scope limit — large caps only.** On SMALL439 it fails 4b at every rung (0.557/0.437 @10 bps)
   and *loses* to its own matched-gross ladder point (dSharpe -0.083 to -0.173). Do not generalise.
9. **Caveats.** Current-constituent panels (survivorship). CAGR sits ~3.5 pp below SPY: this is a
   drawdown-halving book, not a return book, and the CAGR floor is the bar that would break first
   if the next decade's SPY CAGR is higher. The vol target de-grosses to ~0.70 mean, so ~5 pp of
   NAV sits in cash on average and earns nothing here (no cash yield modelled — conservative).
10. **Recommendation: PARK-to-KEEP for Sunday review, not an immediate rules change.** It is the
    first two-panel, three-rung, rule-8-selected 4b candidate in the record whose edge survives the
    gross numeraire. Before it replaces RULES v2 it wants one confirmation run: the `t` dial swept
    finer (0.09-0.18) with `g` held at 0.75 on both panels, plus 1-day-delayed execution, to check
    that `t=0.12` is interior rather than a grid artefact (ideas 240/328's grid-edge flag).
