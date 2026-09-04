# MEMO to the Sunday review — `EWall + vol60-dg` (4b) and the insurance tier statement

1. **What passed.** `EWall + vol60-dg` — equal-weight every universe name whose 20-day
   annualised vol is below 0.60, at 75% gross, weekly, excluded names held in CASH (no
   reweighting) — passes PROTOCOL **4b on both universes at both 10 and 25 bps**:
   u56 11.6%/1.133/−16.9% (halves 1.156/1.113, OOS 1.186), broad 12.4%/1.138/−18.7%
   (halves 1.255/1.027, OOS 1.122), against SPY 15.2%/0.889/−33.7% (0.957/0.834, OOS 0.882).
2. **Turnover 1.36–1.39x/yr** — a third of idea 57's `ew-band3` (4.3–4.8x) and a fifth of a
   200d-gated book (7.6–7.8x). It is the cheapest-to-run 4b book the project has produced.
3. **No trend filter at all.** The whole 4b pass comes from a short-horizon volatility gate.
   This is the first candidate that does not rely on a moving average, which matters because
   ideas 38/49/51 found the 200d gate is *inverted* on small caps.
4. **It is Sharpe-neutral-or-positive against its own ungated control** (+0.009/+0.000/
   +0.016/+0.007 across the four cells) while cutting MaxDD by 5.6–6.7 pp. No other
   instrument in the run does both.
5. **Confirmed alongside it:** idea 57's `ew-band3` (= `EWall + band3-rw`) passes 4b in all
   four cells too, at 25 bps as well as 10 — an independent replication on a second harness.
6. **The blocker.** The 0.60 threshold is inherited from live RULES v1 and was fitted
   historically on overlapping data. This run tuned exactly one parameter (the instrument
   family) and did not re-derive 0.60. **Do not adopt before the sweep in queued idea 95.**
7. **Also on the table, 4a:** `EWall + band3-dg` beats live RULES v1 on all three axes at
   once on both universes at both costs (8.7% vs 6.45% CAGR, 1.206 vs 0.664 Sharpe, −12.1%
   vs −13.8% MaxDD, 1.8x vs 23x turnover). It fails 4b only on the CAGR floor.
8. **Proposed RULES wording, universe/eligibility clause (only if idea 95 confirms 0.60):**
   > *Eligibility.* A name is eligible in week t if its 20-day annualised volatility,
   > measured at the close of the last trading day of week t−1, is below 0.60. No trend
   > filter is applied. *Sizing.* Hold every eligible name at equal weight, total gross
   > 75% of NAV; the weight of any excluded name is held in cash and is not redistributed.
   > *Cadence.* Decide at the weekly close, execute at the next close.
9. **Proposed RULES wording, drawdown-budget clause (adoptable now, it is a statement of
   fact not a fitted rule):**
   > *Drawdown budget.* When exposure must be reduced, reduce it with a per-name
   > eligibility gate first, a static gross multiplier second, and a book-level drawdown
   > rule last. Per-name trailing stops are not a drawdown instrument: measured on matched
   > books and matched days they increase maximum drawdown in 10 of 12 cells. The price of
   > any one gate against another is not stable out of sample and must not be quoted.
10. **Not claimed.** Both universes are current-constituent lists; the calendar-day index
    bug (idea 38) is unfixed; no result here has been checked against a delisting-aware
    panel (idea 54). The 4b levels are optimistic; the within-cell deltas are what this run
    stands behind.
