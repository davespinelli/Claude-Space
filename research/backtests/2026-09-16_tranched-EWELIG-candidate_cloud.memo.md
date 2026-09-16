# Memo — the tranched `EWELIG` 4b candidate, in tradable wording (idea 975, cloud lane, 2026-09-16)

1. **Status.** A standing PROTOCOL **4b** candidate (964's, rule-8 clean) that has now survived a
   gross-, width- and cadence-matched rotating null: **0 of 200 draws certify** at Q and at M.
   **This lane does NOT recommend promotion.** Rule 6 permits one rules change per week via Sunday
   review; this memo puts the candidate on file in exact form so the decision can be made on the
   wording rather than on a description of it.
2. **Exact RULES wording, if it were ever promoted:**
   *"Hold every instrument whose close is above its 200-day moving average and whose 20-day
   realised volatility is below 60% annualised, equally weighted at 0.75 of NAV divided by the
   number of such instruments, with gated-out weight held as CASH and never re-spread. Split NAV
   into 63 equal tranches. Tranche i rebalances on the i-th trading day counted back from each
   quarter-end (i = 0 … 62, clipped to the first day of the quarter), decided at that close and
   applied at the next open. Costs 10 bps per unit turnover."*
3. **What it delivers, rule 8, OOS 2017–2026 read once:** CAGR **12.29%**, Sharpe **1.1201**,
   MaxDD **−20.14%**, against SPY 15.21% / 0.8713 / −33.72% and the live RULES v2 book
   (full-sample Sharpe 1.2009, MaxDD −12.05%). Full sample 11.59% / 1.1067 / −20.14%,
   H1 1.2030 / H2 1.0333.
4. **Reason 1 not to promote — it clears no 4a, anywhere.** 0 of 402 books in this run, subject
   and null alike. Its Sharpe and its drawdown are both worse than the live book's, so promoting
   it would trade 1.2009/−12.05% for 1.1201/−20.14% in exchange for CAGR.
5. **Reason 2 — the margin is 0.0879 pp.** |OOS MaxDD| 20.1424% against a cap of 20.2304%. The
   pass is one bad quarter from not existing.
6. **Reason 3 — it wins on one leg and loses on the rest.** Inside its own matched null its OOS
   MaxDD percentile is 1.000 but its OOS Sharpe percentile is **0.060** and its OOS CAGR
   percentile **0.000**: a random basket of the same width, gross and cadence out-earns it.
7. **Reason 4 — the tranche gain reverses.** +0.0873 OOS Sharpe over its own canonical at Q,
   **−0.0445 at M**, while the null's gain is positive at both. The construction is not what makes
   it work; the quarterly cadence happening to suit it is.
8. **What the null DID establish, and it is worth keeping:** the 4b bar is not reachable by chance
   here. A matched rotating coin flip certifies **0 of 400** and its only failed leg is `L4_DD` on
   200 of 200 draws at both cadences. The eligibility gate is a **drawdown instrument**, not a
   return instrument.
9. **Evidence.** Gates 10 of 11; G3b reproduces 964's `pass4b_share` 0.412698 exactly and G3c its
   0.0880 pp DD margin to 5.8e-05 pp; G3a fails at 1.727e-04 against a 1e-09 bar, carried entirely
   by `turn_per_yr` (every return metric agrees to ≤ 3.03e-05) and attributed in the result file
   to a restatement of `data/prices.csv`. Script:
   `2026-09-16_price-the-QUARTERLY-TRANCHE-against-a-ROTATING-NULL_cloud.py`.
10. **Survivorship (rule 9).** U56 is a current-constituent list, so the CAGR and drawdown levels
    in §3 are optimistic and the 4b pass is an UPPER bound. `RULES.md`, `PROTOCOL.md`, `scan.py`,
    `bot.py` and `baseline.py` are untouched by this run.
