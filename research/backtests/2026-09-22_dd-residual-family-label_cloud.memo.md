# KEEP-4b CANDIDATE MEMO — U56 / MADIST / k=40 / gross 0.75, monthly (idea 2079, lane cloud, 2026-09-22)

1. **What it is.** An 80-book shelf cell reached by the *label-only* IS-only chooser (best family
   by mean IS MaxDD-on-beta residual over 2009–2016, then that family's median-ordered book).
   It is an incidental by-product: idea 2079's own question is answered NO (see `.result.md`).
2. **Numbers (U56, 10 bps, t+1, monthly).** FULL 10.86% / 1.194 / −13.55%, halves 1.18 / 1.21.
   OOS 2017–2026 (read once) 12.08% / **1.308** / −13.55%.  SPY 15.14% / 0.885 / −33.72%,
   halves 0.96 / 0.83, OOS 15.29% / 0.875 / −33.72%.  RULES v2 (live) 8.62% / 1.201 / −12.05%.
3. **Path 4b, FULL:** Sharpe > SPY in both halves (1.18 > 0.96, 1.21 > 0.83) ✓; MaxDD −13.55% ≤
   60% of SPY's −33.72% (bar −20.23%) ✓; CAGR 10.86% ≥ 70% of SPY's 15.14% (bar **10.60%**) ✓.
4. **Path 4b, OOS (rule 8):** Sharpe 1.308 > 0.875 ✓; MaxDD −13.55% vs bar −20.23% ✓;
   CAGR 12.08% ≥ bar 10.70% ✓.  **Path 4a: FAILS** — it does not beat the live v2 book's MaxDD
   (−13.55% vs −12.05%) and is one of 0 of 12 picks clearing 4a this run.
5. **Exact RULES wording if promoted** (replaces v2 clauses 2–5; clauses 1, 6, 7, 8 stand):
   *2. Membership gate: a name is IN on the decision day when `close / ma200 − 1` is defined
   (≥ 200 closes), the name is above its 200-day moving average, and its 20-day annualised
   volatility is below 0.60.  3. Selection: rank every IN name by `close / ma200 − 1`, highest
   first, and hold the top 40; if fewer than 40 are IN, hold all of them.  4. Sizing: each held
   name at `0.75 / 40` of current NAV (1.875%); unfilled slots stay in CASH — the book de-grosses
   and the gross is never re-spread.  5. Rebalance: on the last trading day of each month only.*
6. **Two dials, both reported not fitted here:** k = 40 and gross = 0.75 are the shelf's own
   ladder rungs, not values chosen to make this pass; every one of the 80 cells is in `.shelf.csv`.
7. **The thin leg.** The FULL CAGR margin is **0.26 pp** (10.86% against a 10.60% bar).  Any
   re-cut that moves SPY's full-sample CAGR up by a quarter point kills the pass.  The OOS CAGR
   margin is wider (1.38 pp) and the DD and Sharpe legs are not close on either window.
8. **The chooser's weak joint.** The "median-ordered book" tie-break sorts widths as strings
   (`"10","20","40","5","ALL"`), so the median of 20 is k=40, gross=0.75.  The chooser is legal
   and IS-only, but the specific cell it lands on is a sort-order artefact; a different tie-break
   reaches a different book.  Treat reachability as **one chooser, one convention**, not robust.
9. **Survivorship.** U56 is a current-constituent list.  Every level above is optimistic; the
   candidate has NOT been priced on a vintage-honest or admission-haircut panel (cf. open 2087).
10. **Recommendation: PARK, do not promote.**  Two independent weaknesses (a 0.26 pp CAGR leg and
    a convention-sensitive chooser) plus a 4a failure.  Before any Sunday review takes it: re-price
    at 25 and 50 bps and one extra day of lag, sweep k ∈ {20,30,40,ALL} × gross ∈ {0.50,0.75,1.00}
    with every point published, and re-run under at least one second legal IS-only chooser.
