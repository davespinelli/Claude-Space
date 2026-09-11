# 4b memo — U56 QUANTILE-50 RESPREAD, monthly, gross 0.75 (lane B, 2026-09-11, idea 733-SIGNFLIP)

1. **What it is.** Hold, equal-weight, every U56 name in the TOP 50% by distance to its own 200-day
   moving average; spread `gross 0.75` across exactly those names (RESPREAD, not de-gross);
   rebalance monthly; 10 bps per unit turnover, next-day execution, no shorting, no leverage.
2. **How it got here.** It is NOT this idea's deliverable. It is one of the 324 imported books
   (ideas 298/301/535/538's population) this run rebuilt only to satisfy PROTOCOL rules 4 and 8;
   its dials were never tuned here — `(level, cadence)` were picked on IS Sharpe (≤ 2016) alone
   inside the U56/QUANTILE/RESPREAD arm and 2017–2026 was read once.
3. **Full sample (2009-01-13 →):** CAGR **15.47%**, Sharpe **1.2359**, MaxDD **−19.80%**,
   halves **1.3518 / 1.1454**. Realised turnover 3.11x/yr.
4. **OOS (2017-01-01 →, untouched):** CAGR **15.95%**, Sharpe **1.2164**, MaxDD **−19.80%**.
5. **vs SPY (the 4b comparand):** SPY 15.11% / 0.8835 / −33.72%, halves 0.9595/0.8211, OOS 15.24% /
   0.8721. Every 4b leg passes: H1 ✓, H2 ✓, OOS Sharpe ✓, MaxDD 19.80% ≤ 60%·33.72% = 20.23% ✓,
   CAGR 15.47% ≥ 70%·15.11% = 10.58% ✓. **4b PASS. 4a FAIL** (Sharpe below live RULES v2 in both
   halves; 0 of 324 books cleared 4a).
6. **vs the live book:** RULES v2 OOS Sharpe 1.2747 beats it (1.2164); this book's case is return,
   not risk-adjusted return — OOS CAGR 15.95% against the live book's 9.53%.
7. **vs its own control:** the cadence-matched no-gate equal-weight-all book at the same gross runs
   OOS Sharpe 1.1488, so the gate is worth **+0.068** OOS Sharpe. Its two neighbours (level 0.40 and
   0.60, same cadence) also pass 4b at OOS Sharpe 1.2403 / 1.2404, so the pick is not knife-edge.
8. **Exact RULES wording it would take, if a Sunday review ever adopted it.**
   > *Clause 2 (replacement).* Each month-end, rank every priced instrument by `close / MA200 − 1`.
   > Hold the top 50% by that rank, equal-weight, at `0.75 / k` of NAV where `k` is the number held.
   > Instruments outside the top 50% are not held; residual NAV is CASH. Orders are placed at the
   > next close. No ranking on momentum, no volatility filter, no hysteresis band.
9. **Why this run does NOT claim a KEEP.** Three standing objections in the record apply to this
   exact class and none was tested here: idea 679 (the 2026-09-04 4b candidate fails a
   **turnover-matched** base rate — this book turns 3.11x/yr against the control's far less),
   idea 463 (the edge over equal weight is a **cost-rung** fact), idea 672 (no swap against a
   gross-matched gated EW book). Until those three are re-run on this book it is **PARK**, not KEEP.
10. **SURVIVORSHIP.** U56 is current constituents with no delistings, so the CAGR level — the leg
    this book's whole case rests on — is inflated by an unmeasured amount. That alone bars a
    capital allocation on this evidence.

11. **AMENDED same day by idea 787 (lane B, whole-shelf equal-weight re-price) — READ BEFORE PROMOTING.**
    Re-scored against an equal-weight basket of its OWN panel (`B_EWW10`: U56 tradables, weekly,
    gross 1.00, the book's own 10 bps — 17.69% / 1.1237 / −29.09%, halves 1.2036 / 1.0598, OOS
    18.35% / 1.1308), this book's 4b pass does **not** survive. The QUANT-RESP family clears the bar
    on all three Sharpe legs across most of its level ladder — the gate is doing real work — but
    **never clears the CAGR floor and the DD cap together**: q0.50 (this memo's pick) misses the DD
    cap, and the only rung with enough return, q0.20 (19.63% CAGR, +7.25 pp over the floor), breaches
    it by **−4.42 pp**. On B136, q0.20 is the single cell clearing all three Sharpe legs and misses DD
    by −2.73 pp. Whole 82-cell shelf: **4b vs SPY 26, vs either equal-weight bar 0**; under rule 8 the
    IS pick for this family is q0.60 (U56) / q0.20 (B136) and both fail the bar on DD.
    Line 9's PARK stands, and its reason is now measured rather than owed: **PARK, not KEEP-candidate.**
    See `2026-09-11_does-ANY-standing-4b-candidate-clear-an-EQUAL-WEIGHT-bar_B.result.md`.
