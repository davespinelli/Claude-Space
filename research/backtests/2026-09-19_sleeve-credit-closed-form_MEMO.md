# MEMO — idea 1551 (lane C, 2026-09-19): the sleeve axis IS arithmetic, but not the committed arithmetic

1. **METHOD FINDING, not a RULES change.** Nothing on this grid is a KEEP candidate, nothing is
   proposed for enactment, and RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are
   untouched. What follows is a measurement convention for future runs.
2. **THE IDENTITY (exact).** The (SLEEVE, GROSS) book IS the weekly-rebalanced two-asset mix of
   the CORE book at gross 1.00 and the sleeve at weights (g, 1−g), charging 10 bps on the mix's
   own turnover vector. Max |daily net return| against the direct runner over all 60 cells:
   **1.110e-16**, CASH cells included. One branch is load-bearing: the 0% cash line pays no
   turnover, a traded sleeve does; omitting that breaks the identity by 6.0e-04 on day one.
3. **THE COMMITTED FORM IS NOT THAT IDENTITY.** `sbar x CAGR_sleeve` (idea 1358 clause 2, and the
   queue's wording of this idea) **under-predicts the credit at 45 of 45 cells**: MAE 0.1678,
   max 0.4322 pp/yr; it misses 6.5% of the credit on SHY, 17.1% on IEF, 43.7% on TLT.
4. **`sbar` IS `(1−g)`.** Max |sbar − (1−g)| over 45 cells = **0.00054**. The realised-weight
   refinement is worth 0.0004 pp/yr; the two forms stand or fall together.
5. **WHAT IS MISSING, IDENTIFIED.** A fixed-weight mix earns the weighted average of LOG growth
   rates, adding `g(1−g)(var_s/2 − cov(core, sleeve))` against a zero-variance residual.
   corr²(that term, the shortfall) = **0.9980**; adding it takes MAE 0.1356 → **0.0306 pp/yr**.
6. **PROPOSED CONVENTION for future runs (no protocol edit requested this week).** When a
   de-grossed book's sleeve credit is quoted without running the sleeve book, quote
   **`(1+CAGR_cash)·(1−g)·CAGR_s − Δdrag + g(1−g)(var_s/2 − cov)`**, or reconstruct exactly with
   the clause-2 identity. Do not quote `(1−g)·CAGR_s`; it is the low-volatility limit only.
7. **THE ERROR IS NOT NEUTRAL.** The omitted term penalises volatile sleeves, so a chooser built
   on the committed form rates duration as free return: C_CHEAP picks TLT on 3 of 3 panels for
   **−0.2514 OOS Sharpe** against doing nothing, where the exact chooser picks IEF/IEF/TLT for
   −0.0439 and reproduces the full-grid pick on 3 of 3 panels from 3 core books instead of 60.
8. **RESOLVABILITY, stated honestly.** Every scalar form's error sits inside its own paired
   block-bootstrap SE (mean 0.7492 pp/yr) at 45 of 45 cells, and re-reading the 4b CAGR leg with
   the predicted CAGR flips it at 1 of 45. **No committed verdict in the record moves.** The claim
   is that the form is wrong and one-signed at 45 of 45, not that the record mis-scored anything.
9. **THE DIAL IS STILL A KILL**, on a gross ladder wider than idea 1358's: the IS chooser never
   finds SHY, which is the ex-post best OOS cell on 3 of 3 panels. Idea 1498's 4a SHY pass
   re-appears here (SHY at g = 0.40, U56 and B136) and **fails the OOS re-read at both** — PARK.
10. Script `research/backtests/2026-09-19_is-the-SLEEVE-CREDIT-a-CLOSED-FORM-CORRECTION_C.py`;
    60 cells, 45 form comparisons, 60 reconstruction residuals, 12 rule-8 rows, GATES 23/23.
