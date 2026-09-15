# Memo for the Sunday review — idea 675, 4b KEEP-candidate (lane B, 2026-09-15)

> **Read this beside the cloud lane's confirmation memo for the same idea, which landed first and
> whose PARK is the verdict on the record.** Two independent implementations agree to 1e-4 on the
> window ([0.6242, 0.8337] vs [0.6241, 0.8337], W 0.2094 vs 0.2095) and on the 25 bps break. Both
> memos propose nothing; this one adds the cost closing prices and the midpoint argument below.

1. **This does not promote a new book.** U56/CAND20 is the record's **already-committed 2026-09-04
   KEEP 4b candidate**. This run answers whether its 4b pass is a knife edge. It is not.
2. **The pass window is 0.2094 of gross wide** — `g ∈ [0.6242, 0.8337]` at 10 bps, bisected to 1e-4,
   21 of 150 rungs. Idea 670's "passes at exactly one rung of eight" is a **rung-spacing artefact**:
   its 0.60 and 0.85 rungs straddle the window's boundaries by 0.024 and 0.016.
3. **Do NOT re-tune the gross.** The window's midpoint is **0.7289**; the live constant **0.75** sits
   0.021 from it with margins **+0.126 / +0.084**. 0.75 is already ~the maximal-margin point.
4. **Rule 8 (2009–2016 only, OOS read once):** 3 of 3 U56 choosers at 10 bps clear 4b out of sample,
   including **PICK-LIVE, which fits nothing** — OOS **14.335% / 1.1233 / −18.308%**, halves
   1.235/1.011, vs SPY OOS 15.272% / 0.8740 / −33.717% and RULES v2 9.464% / 1.2772 / −12.055%.
5. **Path 4a is 0 of 600.** CAND20's Sharpe is ~0.14 below the live band book's at every rung and
   gross moves Sharpe by 0.0015 across the whole ladder. **4b is the only path.**
6. **FRAGILITY 1 — cost.** The five-leg 4b pass closes at **21.8 bps** (2.2x PROTOCOL's rung), not
   at the window's 34.9 bps: at 25 bps the window is still 0.098 wide with 0.75 inside it, yet the
   H1-Sharpe leg fails at 0/150 rungs. Turnover is **11.01x/yr**, so this book's verdict is a
   statement about the assumed cost.
7. **FRAGILITY 2 — no in-sample pass.** The IS 5-leg 4b set on U56 is **0 of 150 rungs** (L1 fails
   everywhere). A chooser standing in 2016 had nothing to pick; the walk-forward above works only
   because the choosers select on the DD-cap × CAGR-floor window, not on an IS 4b pass.
8. **NOT portable.** On B136 the 4b pass closes at **6.1 bps**, below PROTOCOL's own 10 bps rung —
   4b at g=0.75, 10 bps is FALSE there. The pass is a U56 fact.
9. **RULES wording, if and only if the review adopts it** (it replaces clause 3's constant only;
   nothing else in RULES v2 changes): *"Clause 3 (gross). Hold the book at gross G = 0.75 of NAV.
   G is fixed, not fitted: it lies inside the measured 4b window [0.62, 0.83] and within 0.02 of
   its midpoint. Do not re-tune G. This clause is void if realised round-trip cost exceeds 20 bps
   per unit turnover."* **Recommendation: adopt no change this week.** The candidate is unchanged
   in substance; only an objection to it has been removed.
10. **Survivorship (PROTOCOL 9):** U56 is a current-constituent list, so every CAGR and drawdown
    level above — the book's, RULES v2's and SPY's alike — is optimistic and both 4b bars are easier
    than on a point-in-time panel. Nothing here justifies real capital ahead of the live record.
    Cross-run limit: idea 670's committed grid does **not** reproduce on the Sharpe family
    (gate G3b FAIL, ~5e-4 uniform, a price-vintage effect); the two metrics this memo's window rests
    on, CAGR and MaxDD, reproduce at 9.9e-05 (G3c PASS).
