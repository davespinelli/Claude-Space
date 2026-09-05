# KEEP-candidate memo — idea 178, lane C, 2026-09-05 (candidate only; NOT proposed for Sunday)

1. **The book.** `universe.json` (56 names), weekly, t+1, 10 bps, gross 0.75 spread equally over the
   names held: hold the top **n = 20** eligible names (above 200d MA, vol20 < 0.60) ranked by idea
   81's composite times the **12-1 momentum percentile rank** (`MOM`, book share m = 0.53).
2. **Why it is on the table.** It is not an in-sample argmax: PROTOCOL rule 8's IS-window 4b screen,
   run at the **published** bar coefficients on 2009–2016 only, **selects this book out of a
   98-book corpus**, and the 2017–2026 window then clears every 4b bar it is read against.
3. **Full sample** 12.32% CAGR / **1.0296 Sharpe** / −18.88% MaxDD, halves **1.1097 / 0.9711**,
   turnover 10.17×/yr, vs SPY 15.23% / 0.8890 / −33.72%, halves 0.9566 / 0.8340.
4. **4b margins (all five positive):** H1 +0.153, H2 +0.137, OOS +0.154, DD +1.35 pp (18.88% against
   the 20.23% cap), CAGR +1.66 pp (12.32% against the 10.66% floor). **4a FAILS** (MaxDD worse than
   RULES v1's −13.83%), so this is a 4b candidate only.
5. **Walk-forward (rule 8), the whole point:** chosen on 2009–2016, read once on 2017–2026 →
   **13.18% / 1.0355 / −18.88%**, against SPY 15.45% / 0.8820 / −33.72% and RULES v1
   7.73% / 0.7471 / −13.83%. It clears all four OOS-window 4b bars.
6. **Blocker 1 — one cost rung.** The screen that selects it does not fire at all at 25 bps
   (0 of 20 arm-cells), and 0 of 1003 corpus books clear 4b at 25 bps. The candidate is a 10 bps
   claim and must not be quoted without that rung.
7. **Blocker 2 — one panel.** On `universe_broad.json` the same screen picks `R6 @ m=0.27 (n=25)`
   instead (13.48% / 0.9879 / −19.76% OOS, also clearing); on the small panel the screen is empty
   and 0 of 98 books clear at any point. Survivorship (idea 54) makes all of this an upper bound.
8. **Blocker 3 — the missing control.** No random-selector arm was run (idea 151's warning). Until
   idea 198 supplies one, the screen's +0.0287 mean OOS Sharpe over 11 cells (t +1.92, 3-0-8) cannot
   be told apart from a generic de-concentration prior. **That is why this is a candidate, not a
   proposal.**
9. **Sibling candidate, weaker:** the same screen under idea 165's swapped coefficients picks
   `R6 @ m=0.15 (n=6)` — 18.62% / 1.0844 / −18.93%, OOS 1.0823 — higher return but **n = 6** and
   **16.3×/yr turnover**, which idea 124's book-size question and any real cost model both reject.
   Prefer the n = 20 book if either is ever taken forward.
10. **Exact RULES wording, if and only if idea 198 clears the random control** — replacing v1's
    §Selection, not amending it:

    > **Selection.** Each Friday close, rank every eligible name (last close above its 200-day
    > moving average and 20-day annualised volatility below 0.60) by the mean of its 12-1, 6-month
    > and 3-month return percentile ranks, halved for names not above the 200-day average, times its
    > 12-1 momentum percentile rank. **Hold the top 20**, equally weighted at **3.75% each (0.75
    > gross, remainder in cash)**, executed at the next session's close. No volatility scaler, no
    > leverage, no shorting. This rule is qualified to the 56-name `universe.json` list at execution
    > costs of 10 bps or less; it is unvalidated at 25 bps and on the small-cap panel.
