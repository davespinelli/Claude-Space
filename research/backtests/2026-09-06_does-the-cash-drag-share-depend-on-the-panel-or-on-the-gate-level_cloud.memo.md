# Memo to Sunday review — idea 298 by-product: the QUANTILE-MA book on U56 (PARK, evidence not proposal)

1. **What it is.** A 4b-clearing book fell out of idea 298's control family: gate IN the top 50% of
   live names by distance above the 200d MA, equal weight, 75% gross, MONTHLY, cash for the rest.
2. **Numbers (U56, 2009-01-13 → 2026-09-04, 10 bps, next-day).** CAGR **15.53%**, Sharpe **1.2400**,
   MaxDD **−19.80%**, halves **1.3459 / 1.1581**, OOS Sharpe **1.2237**.
3. **Bars it clears.** SPY 15.23% / 0.8890 / −33.72%, halves 0.9566 / 0.8340, OOS 0.8820 → needs
   H1>0.957, H2>0.834, OOS>0.882, MaxDD ≥ −20.2%, CAGR ≥ 10.66%. All five pass; DD by 0.4pp only.
4. **It was chosen out-of-sample-clean.** Rule 8: (level, cadence) picked on IS Sharpe ≤2016-12-31
   inside its arm; 2017-2026 read once. Regret vs the arm's OOS-best cell −0.0256.
5. **Why PARK, not KEEP.** The QUANTILE family was pre-registered as a *reported* dimension, so
   selecting it is a third dial this run did not declare. Two dials is the protocol ceiling.
6. **It does not replicate off U56.** B136's own IS pick in the same arm fails 4b on the DD cap;
   SMALL439's fails all five bars. 4b passes: 13 U56, 3 B136, 0 SMALL439 of 324 books.
7. **It does not beat the live book.** 4a is 0/324: RULES v2 is Sharpe 1.2056 at MaxDD −12.05%,
   and this book's −19.80% is 7.75pp worse. It is a higher-return, higher-risk alternative.
8. **Exact RULES wording, if a future run pre-registers the family as a dial and it survives:**
   *"Clause 2 (alternative form, QUANTILE-MA): each month, rank every instrument priced that day by
   px/ma200 − 1. Hold the top ⌈0.50 · N⌉ at 0.75/⌈0.50 · N⌉ of NAV each, N = instruments priced that
   day; the remaining 25% of gross and every un-held name's weight go to CASH. No vol filter, no
   score, no hysteresis band. Rebalance monthly on the last trading day; execute at the next close."*
9. **What would have to be true to promote it.** Pre-register family ∈ {QUANTILE, MA-THRESH} and
   x as the two dials, drop cadence to the record's weekly default, and require the 4b pass on
   U56 **and** B136 with MaxDD clearing the cap by more than 1pp.
10. **Survivorship.** U56 is current constituents with no delistings; every number in lines 2–3 is
   a level claim and inherits that bias whole. Do not treat line 2 as a tradable expectation.
