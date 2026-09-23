# MEMO — idea 2423, the ZERO-sweep variant of the standing 4b candidate (lane cloud, run 49, 2026-09-23)

1. **What passed.** U56 / CAP2 / gross 0.75 / weekly / t+1 / 10 bps with the residual earning **0%**:
   CAGR **11.30%**, Sharpe **1.2343**, MaxDD **-15.18%**, halves 1.2761 / 1.2037, OOS (2017-2026) CAGR
   **12.33%** / Sharpe **1.2914**. SPY over the same window: 15.23% / 0.8897 / -33.72%, OOS Sharpe 0.8831.
2. **Which path.** **4b** — Sharpe > SPY in both halves (1.2761 > 0.9566 and 1.2037 > 0.8353) and out of sample (1.2914 > 0.8831); MaxDD -15.18% vs 0.60 x SPY's -33.72% = -20.23%;
   CAGR 11.30% vs 0.70 x 15.23% = 10.66%. **4a is 0 of 384** — this family never beats the live book on 4a.
3. **Why it is filed and not adopted.** It is not a new rule: it is the STANDING candidate with the sweep
   removed, and the committed SHY version passes 4b too (11.62% / 1.2687 / -14.81%). It is filed because it
   is the HONEST bound — the number that owes nothing to a bond market — and because it is 22.4% cheaper.
4. **Turnover.** 2.72x/yr vs the SHY version's 3.51x and the live book's 1.77x. The sweep leg is itself
   traded; removing it removes trading the book never needed. The turnover blocker is smaller, not solved.
5. **Rule 8 (the reason the dial is not a dial).** 64 IS-only picks over (sweep, gross) fitted on
   <= 2016-12-31: IEF 25 / TLT 20 / TIP 11 / LQD 8 / **SHY 0 / ZERO 0**, mean OOS Sharpe 1.0922 against the
   committed cell's 1.1383. An operator who tuned this dial in-sample would have bought duration and lost.
6. **The failure mode it rules out.** TLT passes 4b in 1 of 64 rows and LQD in 0 of 64, with `L_DD` binding
   in 63 and 64 of those failures. The pass is NOT a disguised duration bet; duration breaks it.
7. **Survivorship (rule 9).** U56 is the CURRENT constituents of `universe.json` held from 2008, so the
   absolute level and the `L_CAGR` leg are biased upward. The ZERO-vs-SHY contrast is same-tape,
   same-decided-weights and first-order immune; the absolute 4b verdict is not.
8. **Exact RULES wording if it were ever adopted** (clause 3 replacement, NOT proposed this week):
   > 3. CASH SLEEVE. The un-invested residual `1 - sum(w)` is held in cash at 0% and is NOT swept into any
   > instrument. No fixed-income ETF is bought to hold the residual.
   Clauses 1, 2 and 4 of RULES v2 (universe, the 200d +/-3% band with hysteresis, `w_i = min(gross/N_in, 2%)`
   at gross 0.75, weekly rebalance, t+1 execution) are unchanged.
9. **What would have to be true to adopt it.** The turnover gap to the live book (2.72x vs 1.77x) is still
   the open blocker, and the record has now killed six devices against it (2328, 2351, 2391, 2404, 2408, 2415).
10. **No change made.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched (rule 6); the
    live book is unchanged. Script: `research/backtests/2026-09-23_sweep-instrument-decomposition_cloud.py`.
