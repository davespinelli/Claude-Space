# MEMO — idea 2254 (2026-09-22, lane B): a rank-hysteresis buffer on the standing both-paths cell

**Status: KEEP-candidate (BOTH paths, 4a vs RULES v2 and 4b vs SPY) at <= 10 bps only — it STRICTLY
DOMINATES the 2026-09-20 Sunday review's candidate but does NOT cure the cost-fragility that
disqualified it.  The review's own filed question ("cut turnover toward the live book's 1.77x") is
answered NO: the buffer's turnover floor over the whole grid is 4.67x/yr, still 2.6x the live book.**

1. The book is the review's candidate (`u56 / S3-50 + band3-rw`, weekly, gross 0.75, t+1) with ONE
   change: the top-20 selection becomes a two-threshold buffer.  `K_in = K_out = 20` is the
   incumbent (gates G1a/G1b/G1c: held set identical on 263,648 name-days, weights exact off 46 tie
   days, return paths within 2.8e-4/day; G3 reproduces the review's re-run to 6.5e-4).
2. Rule 8 picks `K_in = 10, K_out = 30` by argmax IS Sharpe on 2009-2016 at **8 of 8** panel x cost
   cells — the pick does not move with panel or cost rung.
3. That book, u56 @10 bps: **12.55% / 1.3233 / -11.86%**, halves 1.4057 / 1.2531, turnover
   **5.62x/yr**, against the incumbent's 11.26% / 1.2626 / -11.63%, halves 1.2817 / 1.2466, 8.18x.
4. OOS (2017-2026, read once): **12.73% / 1.3031 / -11.86%** vs the incumbent's 11.70% / 1.2875 /
   -11.63%, the live RULES v2 book's 9.46% / 1.2767 / -12.05% and SPY's 15.29% / 0.8751 / -33.72%.
5. It clears 4a against the live book (both halves + MaxDD) and all five legs of 4b, full sample and
   OOS, at 5, 10 AND 25 bps OOS — but the FULL-SAMPLE promotion bar (4a AND beats-v2-OOS AND 4b) is
   **0 of 50 cells at 25 bps and 0 of 50 at 50 bps**, exactly as for the incumbent.
6. Turnover is bought, not free: over the u56 grid `corr(turnover, Sharpe) = -0.8557`, so every
   buffer cell that trades less also scores better; the cheapest cell still clearing the promotion
   bar at 10 bps is `15/40` at **4.97x** (-39% turnover, Sharpe 1.2849, MaxDD -11.40%).
7. The floor is structural: the cheapest cell on the whole grid (`30/56`, 4.67x) loses 4b on the
   **CAGR** leg (9.51% against a 10.60% floor).  CAGR binds in 96 of 98 4b-fail rows; DD in 1.
8. **PROPOSED RULES WORDING (NOT APPLIED — rule 6: Sunday review only; RULES.md untouched):**
   *Clause A.* Universe `research/universe.json` (56 names).  A name is ELIGIBLE on day t when its
   close is inside the 200-day band with hysteresis (IN above `ma*1.03`, OUT below `ma*0.97`,
   previous state in between, OUT before 200 closes exist).
   *Clause B.* Rank the ELIGIBLE names by the `scan.py` composite (21/252 momentum, 6m and 3m
   returns, each cross-sectionally percentile-ranked, averaged).  ADD a name to the equity leg the
   first rebalance its rank reaches **10**; HOLD it until the first rebalance its rank falls past
   **30**; nothing else enters or leaves.  Equal-weight the held set `h` at `0.75 / max(h, 10)` of
   NAV each.
   *Clause C.* Blend 50/50 with the diversifier sleeve (TLT / GLD / UUP: 3-signal momentum vote x
   60-day inverse-vol risk parity, zeroed outside the same band), then rescale the TOTAL to gross
   0.75.  The residual is CASH; do not re-spread it.
   *Clause D.* Rebalance weekly (`freq='W'`), decide at close t, execute at t+1.
9. **Why this is NOT proposable for promotion today.** The 2026-09-20 review disqualified the
   incumbent because its whole advantage lives at or below 10 bps, and 10 bps is inside this repo's
   own ledger-vs-Alpaca measurement error (2.1-16.0 bps on four sells, 2026-09-11).  A book trading
   5.62x/yr sits in exactly the same place.  The buffer moves the number 31% and the bar not at all.
10. **Limits.** u56 and broad are CURRENT constituents (PROTOCOL rule 9 / idea 54), so every CAGR
    level is optimistic and both 4b bars are easier than on a point-in-time panel; the turnover
    contrasts are same-tape / same-names and first-order immune, the pass counts are not.  Flat
    per-unit-turnover costs, no spread / impact / borrow.  One cadence (W), one delay (t+1), one
    blend (0.50), one band (3%), one gross (0.75), one MA length (200d).  Two tuned dials only.
    Evidence: `2026-09-22_rank-hysteresis-turnover-cut_B.py` / `.grid.csv` / `.walkforward.csv` /
    `.console.txt`.
