## Required robustness lines (coordinator), next to the headline

| Sample | Events with a placebo | Placebo: same stocks, random non-event days, same year (after cost) | Event minus placebo | t of the difference | First half / second half of the difference |
|---|---|---|---|---|---|
| Primary | 728 | +0.62% (t = 1.38) | +1.18% | **1.53** | -0.10% / +2.45% |
| >= 5% of market cap | 297 | +0.19% (t = 0.28) | +2.20% | 1.70 | +0.02% / +4.33% |
| Civilian only | 325 | +0.29% (t = 0.57) | +0.89% | 0.67 | +1.74% / +0.04% |

(b) The headline is already measured against IWM only: no size-and-industry benchmark was built, so there is no survivor-built benchmark in this test. The survivorship problem here sits elsewhere, in the companies that have no Yahoo price at all (below).

**Plainly: the headline passes the pre-registered bar, but the placebo line kills it.** The same small contractors beat IWM by +0.62% over random 20-day windows in the same years, and the award windows beat those placebo windows by only +1.18% (t = 1.53), with nothing at all in the first half (-0.10%). What passes is mostly "tiny contractor stocks drifted above IWM in 2018-2026", not an award effect.

## Where the average comes from

- **Only in companies under $50M.** Events at companies worth $50M or more (581 of them): +0.25% after cost, t = 0.42, placebo difference +0.05% (t = 0.06): nothing. Under $50M (285 events): +4.92%, t = 3.42, but placebo difference +3.43% (t = 1.91), still short of the bar.
- **Penny-stock outliers.** The median event earned +0.38%; 51% of events were positive. The largest windows are nano caps (Astrotech +196% in 2018 at a $7.6M market value; Bantec +113% summed daily, -81% buy-and-hold, at a $0.3M market value). Winsorising the top and bottom 1% cuts the mean to +1.52%.
- **Summed vs compounded returns.** The pre-registered measure sums daily abnormal returns. Compounded (buy-and-hold) returns minus IWM give +0.83% after cost, t = 1.39. The gap is what summing does to very volatile, thinly traded stocks.
- **Concentration.** 861 events at 119 companies; the largest (DLH Holdings) is 11% of events. Clustering by company instead of month gives t = 3.04; dropping DLH leaves the mean at +1.87%.
- **DoD vs civilian.** The strength is in DoD awards dated 90 days late (+2.47%, t = 3.11, placebo difference +2.24%, t = 2.32); civilian awards dated on their actual release show +1.17%, t = 1.17. A DoD award three months old, often already announced by DoD on defense.gov, is not "news nobody saw"; a delayed drift there more plausibly reflects the same small-stock drift.

## Survivorship

810 more primary events belong to 112 mapped companies with no usable Yahoo price (acquired or delisted: NCI, ManTech, Engility, KEYW, Dynamics Research, Arotech, Great Lakes Dredge & Dock, Black Box and others); almost as many as the 861 priced ones. Under research/oplev's -30% / +15% applied to each 20-day window, the mean becomes -13.7% / +8.1%, which says only that these companies are too many to ignore. Scaled to a 20-day window (-2.8% / +1.1%), the primary becomes -0.53% (t = -1.55) or +1.36%: **the sign flips under the pessimistic bound.** Some "former" companies may never have traded on an exchange (e.g. employee-owned CH2M Hill files with the SEC); they sit in this missing group.

## For picking stocks

Do not buy small federal contractors because USAspending shows a large award they did not 8-K. Above $50M of market value there is no effect at all. Below $50M the average is driven by a few penny stocks and by a general drift that shows up on random days too. Civilian awards, the only ones that are truly fresh when they appear in the database, show nothing reliable.
