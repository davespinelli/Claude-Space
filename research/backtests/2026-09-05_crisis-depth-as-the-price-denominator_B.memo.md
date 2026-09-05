# Memo — idea 117: price insurance per crisis, not per window (lane B, 2026-09-05)

1. Idea 97 published the u56 gate tier at **4.108 IS / 0.404 OOS** — a 10.2x swing. Both
   numbers reproduce here exactly on idea 94's imported simulator (engine diff 0.0).
2. Cause: the denominator is a **whole-window MaxDD**, which is one number set by the window's
   deepest crisis. IS holds a clipped 27-day GFC tail (-22.1%); OOS holds 2020 and 2022.
3. Confirmed as an elasticity on large caps: log(price) on log(window SPY MaxDD) slopes
   **-4.04 (u56)** and **-3.05 (broad)**; **+0.13 on the small panel, so this is not universal.**
4. Mechanism, with real variation in the regressor: protection scales with depth,
   **+0.161 pp per pp of SPY depth, t +15.07** over 2,400 arm-episodes.
5. Replacement: **premium** = annualised give-up on CALM days only; **protect(e)** = drawdown
   saved inside SPY episode e; **price(e) = premium / protect(e)**, medianed within a depth bin.
6. It travels: median |log10(IS/OOS)| falls **0.455 → 0.184** (bar was ≤0.227), better in
   **92 of 109** arms, z = +7.18. The u56 gate tier's 10.2x becomes **0.93x (DEEP), 1.34x (SHALLOW)**.
7. **RULES wording (exact, for PROTOCOL rule 4, not RULES.md):** *"Any drawdown price (pp of
   CAGR per pp of MaxDD) must be quoted per crisis episode at a stated depth — SPY
   peak-to-trough episodes of the window, SHALLOW/DEEP split at 20 pp — with the premium
   measured on calm days only. A price whose denominator is a whole-window MaxDD may not be
   compared across windows or panels."*
8. Second clause, newly falsifiable: **the per-name trailing stop's protection does not scale
   with crisis depth (+0.012, t +1.46)** while the gate (+0.179) and the DD control (+0.320) do.
9. Rule 8: selecting on the episode price does **not** beat idea 94's selector (mean OOS regret
   +0.425 vs +0.337; dOOS Sharpe -0.016). It is a reporting statistic, not a selector.
10. **No book KEEP.** 4b @10 bps: u56 10 arms, broad 4, small 0; none on all three panels. 4a
    passes are the known small-panel pathology. Nothing here changes the live book.
