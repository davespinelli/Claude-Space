# Memo — idea 124 by-product: u56 TOP40 + band3-rw, a 4b KEEP-candidate (PARK) — 2026-09-07 cloud

1. **PARK, do not promote.** It is one row selected post-hoc from 224, it fails 4b on the broad
   panel (DD at 10 bps; H2 + DD at 25), and the rule-8 selector does not pick it below tau=1.00.
2. Numbers, u56 @ 10 bps: CAGR **11.36%**, Sharpe **1.211**, MaxDD **-15.66%**, halves
   **1.250/1.186**, OOS Sharpe **1.276**. SPY 0.889 (0.957/0.834), OOS 0.882, MaxDD -33.72%.
3. 4b margins: H1 +0.294, H2 +0.352, OOS +0.394, DD +4.57 pp, CAGR +0.70 pp — every bar clears,
   the CAGR bar by the least. At 25 bps it still passes (Sharpe 1.155, OOS 1.219).
4. **4a vs RULES v2: FAIL** (as do all 224 rows) — the live book's -12.05% drawdown is
   unreachable for a 40-name equity book.
5. Exact RULES wording, were it ever adopted: *"Rank the panel by the v1 composite (no vol
   scaler). Each week hold the 40 best-ranked names that are inside the 200d +/-3% band, at
   0.75/40 of NAV each; a name outside the band is not held and its weight stays in cash.
   Execute at the next close."*
6. As an insurance instrument it buys **5.91 pp** of drawdown for **2.31 pp** of CAGR — rate
   **0.390**, cheaper than idea 94's static-gross lever at 0.57 and than its own TOP20 twin.
7. Its denominator is ADMISSIBLE on all three of idea 122's axes (D1, D2, D3 at every tau), which
   is why the rate above may be quoted at all.
8. Caveat inherited from idea 94: the `rw` convention holds the per-name weight at 0.75/40
   regardless of how many names the band admits, so this book **de-grosses in bear markets** —
   part of its drawdown margin is exposure, not selection.
9. SURVIVORSHIP: universe.json is a current-constituent list; the 11.36% CAGR is optimistic. The
   within-cell differences (dCAGR, dMaxDD) are far less exposed.
10. Next test before it could be anything: the gross-ladder control (does a static de-gross reach
    -15.66% MaxDD at a higher CAGR?) and a broad-panel repair, per idea 94's own dominance test.
