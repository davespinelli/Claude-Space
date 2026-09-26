# Do federal contract awards that nobody announced move small-cap stocks? (INFO-3)

*Generated 2026-09-26 by `research/infoedge/info3_awards/s8_report.py` from `results.json`. Pre-registration and every deviation: `PREREG.md` in this folder.*

## The short answer

**Yes by the pre-registered rule, but not a usable edge.** Awards worth at least 2% of a small listed company's market value, with no 8-K from the company around the award, were followed by an average abnormal return of +1.78% over the 20 trading days after the award became public (after 0.2% cost), t = 2.76 (clustered by month); the bar was t >= 2.5 with a positive sign in both halves. The required placebo check fails: the same stocks on random non-event days in the same years earned +0.62%, so the award windows beat them by only +1.18% (t = 1.53), -0.10% in the first half. Buy-and-hold returns give +0.83% (t = 1.39), companies worth $50M or more show +0.25% (t = 0.42), and the pessimistic survivorship bound flips the sign. The average comes from nano-cap stocks and a general small-stock drift, not from the awards.

| Test | Answer | Events | Mean abnormal return, days +1..+20, after 0.2% cost | t (clustered by month) | First half | Second half |
|---|---|---|---|---|---|---|
| Primary: award >= 2% of market cap, no 8-K within 5 trading days | Yes | 861 (119 cos.) | +1.78% | 2.76 | +0.72% (n=430) | +2.83% (n=431) |
| Secondary: award >= 5% of market cap | No | 388 (67 cos.) | +2.16% | 2.39 | +1.86% (n=194) | +2.47% (n=194) |
| Secondary: civilian agencies only | No | 406 (65 cos.) | +1.17% | 1.17 | +1.38% (n=203) | +0.96% (n=203) |

Abnormal return = stock total return minus IWM total return, summed over trading days +1 to +20 after the public date. Halves split at the median public date (2017-12-18).

## Events

| | Civilian | DoD | Total |
|---|---|---|---|
| No 8-K within 5 trading days ("unannounced") | 645 | 665 | 1,310 |
| 8-K within 5 trading days ("announced") | 463 | 387 | 850 |
| All | 1,108 | 1,052 | 2,160 |

These are priced events with a complete 20-day window, 144 companies, before the same-company overlap rule (an event within 20 trading days of the same company's previous event is dropped inside each test). Companies with no usable Yahoo price add 2,118 more events at 126 companies (screened on public float); they enter only the survivorship bounds below.

## Read this first: how the awards are dated

- DoD awards (awarding agency Department of Defense) are dated action date + 90 days, the pre-registered rule, after checking that USAspending really holds DoD records back 90 days from the action date (on 2026-09-26 it had ~11,000-15,000 DoD actions for each of 25-26 June 2026 and none for 27-29 June). Of 1,105 qualifying DoD actions, 19 were entered into FPDS even later than that and are dated by their FPDS approval instead.
- Civilian awards are dated by their FPDS approval date + 1 business day (1,384 of 1,384 qualifying civilian actions; 0 not found in FPDS use the pre-registered action date + 5 business days). Median lag from signing to public date: 2 days; 18% took more than 10 days and 11% more than 30, because agencies report late. The pre-registered +5 business days would have used those before they were public.
- Caveat 1: DoD itself announces contracts of about $7M and up (currently $7.5M) on defense.gov on the award day, so many large DoD awards are public long before USAspending shows them. The DoD test therefore measures the reaction three months after awards that were often already public; it cannot say whether the first announcement moved the stock.
- Caveat 2: 'no 8-K within 5 trading days' is the pre-registered filter, but companies also announce awards by press release without an 8-K, and in the next 10-Q; neither is checked, so 'unannounced' overstates how hidden an award was.
- Caveat 3: USAspending labels each recipient and parent identifier with its current name. A parent's point-in-time identity is kept, but where the parent is the recipient itself only exact name matches to a listed company are used.

## Mapping precision

- 50 of 50 randomly drawn event actions were mapped to the right listed company (precision 100%, 95% interval 93-100%).
- By match type: exact 50/50.
- Beyond the random draw, every parent-to-company pair behind a candidate award (about 160) was read before any return was computed; four parent names that clearly belonged to someone else were blocked (GRAHAM GROUP LTD, INNOVATE! INC, THE MILLENNIUM GROUP INTERNATIONAL LLC, and ITT CORPORATION rows after the 2011 split). A few single events with a stale parent label or a SPAC matched before its merger remain (e.g. CVR Energy/Wynnewood 2011, Southland 2022), so true precision is a little below the sample's 100%.
- Coverage is incomplete in the other direction: subsidiaries that report themselves as their own parent are matched only when their name equals the listed company's, so some awards to acquired or renamed units are missed.

## How much to trust it

**Primary.** Gross mean +1.98% (t = 3.07), median +0.38%, 51% of events positive; buy-and-hold version +0.83% (t = 1.39). Survivorship bounds (every missing-company event, 810 of them, and every window cut short by a delisting (0), set to -30% / +15%): -13.72% (t = -22.21) / +8.09% (t = 21.54).

**>= 5%.** Gross mean +2.36% (t = 2.61), median +0.85%, 52% of events positive; buy-and-hold version +0.53% (t = 0.62). Survivorship bounds (every missing-company event, 421 of them, and every window cut short by a delisting (0), set to -30% / +15%): -14.68% (t = -17.96) / +8.74% (t = 17.11).

**Civilian only.** Gross mean +1.37% (t = 1.37), median -0.71%, 46% of events positive; buy-and-hold version +0.54% (t = 0.57). Survivorship bounds (every missing-company event, 320 of them, and every window cut short by a delisting (0), set to -30% / +15%): -12.66% (t = -13.92) / +7.18% (t = 12.04).

For information only (not part of the verdict):

| Sample | Events | Mean after cost | t |
|---|---|---|---|
| DoD only, unannounced | 485 | +2.47% | 3.11 |
| Announced (8-K within 5 trading days) | 610 | +1.88% | 1.76 |
| All events regardless of 8-K | 1,283 | +1.62% | 2.58 |
| Unannounced, market cap >= $50M | 581 | +0.25% | 0.42 |
| Unannounced, award >= 10% of market cap | 201 | +3.27% | 2.38 |

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

