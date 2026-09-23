# Does operating leverage predict stock returns? Pre-registered study

*Generated 2026-09-23 by `research/oplev/run_tests.py`. Portfolios formed each June 2011-2025 from SEC filings, held July to June; returns 2011-07-01 to 2026-06-01 (180 months). Every number below is in `results.json`.*

## The short answer

| Test | Answer | Top minus bottom, per year (equal-weighted) | t-stat | Years top won |
|---|---|---|---|---|
| H1. Operating-leverage level | No | +2.7 points | 1.35 | 9 of 15 |
| H2a. Fixed-cost share | No | +3.3 points | 1.79 | 9 of 13 |
| H2b. Fixed costs plus accelerating sales (operating leverage "kicking in") | No | +1.2 points | 0.79 | 8 of 13 |
| H3. Margin expansion on growing sales | No | -0.9 points | -0.08 | 8 of 15 |
| H4a. Management says operating leverage is kicking in | No | +0.4 points | 0.48 | 8 of 15 |
| H4b. The same, said for the first time after two quiet years | No | +3.8 points | 1.13 | 8 of 14 |
| H4c. Negative operating-leverage commentary (expected to lag) | No | +0.1 points | 0.39 | 8 of 15 |

"Top minus bottom" is the difference between the two groups' compound annual returns; the t-statistic is computed on the monthly return differences (2.0 is the pre-registered bar). The two can differ in sign when the gap is near zero. H2 needs four years of history, so it covers the 13 formations from June 2013. Benchmarks over the same months: equal-weighted study universe 13.2% a year, IWM 10.5%, SPY 14.2%.

For the H4 rows, "top" is the companies whose management made the statement and "bottom" is universe companies that said nothing about operating leverage in the year before formation; H4b starts with the June 2012 formation. Details in the H4 section at the end.

In one line each: **H1** No (+2.7 points a year, t = 1.35, 9 of 15 years). **H2a** No (+3.3 points a year, t = 1.79, 9 of 13 years). **H2b** No (+1.2 points a year, t = 0.79, 8 of 13 years). **H3** No (-0.9 points a year, t = -0.08, 8 of 15 years).

## Read this first: the missing-company problem

The universe is built from every company that filed with the SEC at the time, including ones that later disappeared. Yahoo only has prices for symbols that still trade, so companies that were later acquired or delisted usually have no price and cannot be held. Across all years, 15,200 firm-years pass the fundamental filters but have no price, against 20,867 that can be held: 42.1% of the would-be universe is missing (31.6% counting only companies whose last reported public float was at least $50M, a stand-in for the size filter we cannot apply without a price). The problem is worst in the early years, when the most companies have since vanished:

| Formation (June) | Universe (priced, >= $50M) | Missing: passes filters, no price | Missing share | Missing with float >= $50M | Not yet listed (Yahoo history starts later; excluded) |
|---|---|---|---|---|---|
| 2011 | 870 | 1,367 | 61% | 460 (35%) | 160 |
| 2012 | 982 | 1,640 | 63% | 972 (50%) | 174 |
| 2013 | 1,001 | 1,561 | 61% | 935 (48%) | 155 |
| 2014 | 1,078 | 1,459 | 58% | 894 (45%) | 139 |
| 2015 | 1,120 | 1,382 | 55% | 926 (45%) | 127 |
| 2016 | 1,151 | 1,240 | 52% | 869 (43%) | 126 |
| 2017 | 1,254 | 1,117 | 47% | 770 (38%) | 108 |
| 2018 | 1,339 | 1,021 | 43% | 708 (35%) | 107 |
| 2019 | 1,422 | 927 | 39% | 661 (32%) | 94 |
| 2020 | 1,468 | 804 | 35% | 566 (28%) | 102 |
| 2021 | 1,720 | 768 | 31% | 501 (23%) | 122 |
| 2022 | 1,819 | 708 | 28% | 536 (23%) | 70 |
| 2023 | 1,846 | 592 | 24% | 417 (18%) | 63 |
| 2024 | 1,877 | 378 | 17% | 269 (13%) | 61 |
| 2025 | 1,920 | 236 | 11% | 162 (8%) | 63 |

One symptom: the priced universe itself returned 13.2% a year equal-weighted against 10.5% for IWM, which holds the losers too. If every missing company is assumed to have lost 30% in its year, the universe return drops to -6.8% (-2.6% counting only float >= $50M); at +15% it is 14.4%. So absolute returns in this study flatter reality; the tests below compare groups against each other, which is what can survive this, provided the missing companies are spread evenly across groups. They are not quite: in every quintile sort the two extreme fifths lose more companies than the middle ones, because unusual companies are the ones that get acquired or fail. Each test below reports the missing share at the top and the bottom of the sort, and re-runs the headline spread assuming every missing company lost 30% in its year (a typical delisting for poor performance) or gained 15% (a typical takeover premium).

## H1. Operating-leverage level

**Question.** Do companies with high operating costs per dollar of assets (Novy-Marx's measure of operating leverage) earn higher stock returns?

**Answer: No.** The highest-operating-leverage fifth did not reliably beat the lowest fifth (t = 1.35, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** The highest-operating-leverage fifth returned 13.6% a year against 10.9% for the lowest fifth, a gap of +2.7 points a year; the top group was ahead in 9 of 15 holding years. $10,000 held for the 180 months would have become $67,713 in the top group and $47,267 in the bottom one, before costs. Monthly spread t-statistic 1.35 (Newey-West 1.36).

**How much to trust it.**

- First half (formations 2011-2017): +2.2 points a year (t = 0.70; top ahead in 4 of 7 years). Second half (2018-2025): +3.0 points a year (t = 1.17; top ahead in 5 of 8 years).
- Within industries (2-digit SIC): +2.9 points a year (t = 2.01; top ahead in 12 of 15 years).
- Small caps (< $2B): +1.9 points a year (t = 0.61; top ahead in 8 of 15 years). Large caps (>= $2B): +2.5 points a year (t = 1.19; top ahead in 11 of 15 years).
- Value-weighted (secondary): +2.5 points a year (t = 0.91; top ahead in 8 of 15 years).
- Missing companies: 47.6% of the would-be top group and 43.4% of the would-be bottom group have no price. Spread with missing firms excluded +2.7 points, t = 1.35; if every missing firm lost 30%: -0.8 points, t = -0.76 (only those with public float >= $50M: +2.7 points, t = 2.13); if every missing firm gained 15%: +1.5 points, t = 1.19 (+1.6 points, t = 1.16). **The sign changes across these assumptions.** Under -30% for float >= $50M missing firms the t-statistic reaches 2, but not under the others, so no assumption turns the answer into a robust yes.
- Raw Yahoo returns, no bad-print rule: -1.8 points a year (t = -0.56; top ahead in 7 of 15 years); raw returns with only the single largest held monthly return removed: +3.2 points a year (t = 1.50; top ahead in 8 of 15 years).
- The top group after 0.5% a year of trading costs: 13.0% a year vs 13.2% for the equal-weighted universe (-0.1 points, t = 0.11) and 10.5% for IWM (+2.5 points, t = 1.58).

**Fundamental sanity check (next fiscal year, CY t vs CY t-1).**

| Group | Next-year change in operating margin (median, pts) | Next-year revenue growth (median) | Change in revenue growth (median, pts) |
|---|---|---|---|
| Q1 | -0.18 | 8.9% | -0.3 |
| Q2 | +0.20 | 8.2% | -1.4 |
| Q3 | +0.30 | 7.0% | -1.9 |
| Q4 | +0.29 | 5.7% | -1.8 |
| Q5 | +0.15 | 5.2% | -1.8 |

**For picking stocks.** Do not buy a stock because it runs a lot of operating cost through a small asset base. High-OL stocks did a little better in most cuts, but the headline gap did not clear the bar, and it turns negative (-0.8 points) if every missing company is assumed to have lost 30%. The version closest to Novy-Marx's original (sorting within industries) is borderline at +2.9 points a year, t = 2.01: at most a weak tilt, not a selection rule.

Annualised return by quintile (Q1 = lowest signal, Q5 = highest):

| | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| Equal-weighted | 10.9% | 12.7% | 13.7% | 14.6% | 13.6% |
| Value-weighted | 14.4% | 18.6% | 16.2% | 12.3% | 16.9% |
| Industry-neutral EW | 11.1% | 13.4% | 13.5% | 14.3% | 14.0% |

## H2a. Fixed-cost share

**Question.** Do companies whose costs are mostly fixed (they barely move when sales move) earn higher returns?

**Answer: No.** The most-fixed-cost fifth did not reliably beat the most-variable-cost fifth (t = 1.79, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** The most-fixed-cost fifth returned 15.4% a year against 12.1% for the most-variable-cost fifth, a gap of +3.3 points a year; the top group was ahead in 9 of 13 holding years. $10,000 held for the 156 months would have become $64,441 in the top group and $44,247 in the bottom one, before costs. Monthly spread t-statistic 1.79 (Newey-West 1.48).

**How much to trust it.**

- First half (formations 2011-2017): +1.4 points a year (t = 0.68; top ahead in 4 of 5 years). Second half (2018-2025): +4.4 points a year (t = 1.67; top ahead in 5 of 8 years).
- Within industries (2-digit SIC): +3.7 points a year (t = 2.37; top ahead in 10 of 13 years).
- Small caps (< $2B): +5.3 points a year (t = 1.89; top ahead in 8 of 13 years). Large caps (>= $2B): +1.7 points a year (t = 1.18; top ahead in 7 of 13 years).
- Value-weighted (secondary): +1.4 points a year (t = 0.61; top ahead in 6 of 13 years).
- Missing companies: 43.8% of the would-be top group and 40.5% of the would-be bottom group have no price. Spread with missing firms excluded +3.3 points, t = 1.79; if every missing firm lost 30%: +0.6 points, t = 0.58 (only those with public float >= $50M: +1.6 points, t = 1.39); if every missing firm gained 15%: +2.6 points, t = 2.09 (+2.8 points, t = 2.03). The sign does not change across these assumptions. Under +15% for all missing firms and +15% for float >= $50M missing firms the t-statistic reaches 2, but not under the others, so no assumption turns the answer into a robust yes.
- Raw Yahoo returns, no bad-print rule: +3.5 points a year (t = 1.91; top ahead in 9 of 13 years); raw returns with only the single largest held monthly return removed: +3.5 points a year (t = 1.91; top ahead in 9 of 13 years).
- The top group after 0.5% a year of trading costs: 14.8% a year vs 13.2% for the equal-weighted universe (+1.6 points, t = 1.26) and 10.5% for IWM (+4.3 points, t = 2.41).

**Fundamental sanity check (next fiscal year, CY t vs CY t-1).**

| Group | Next-year change in operating margin (median, pts) | Next-year revenue growth (median) | Change in revenue growth (median, pts) |
|---|---|---|---|
| Q1 | +0.57 | 5.2% | -0.4 |
| Q2 | +0.07 | 6.5% | -1.6 |
| Q3 | +0.00 | 7.2% | -1.7 |
| Q4 | +0.20 | 6.4% | -1.4 |
| Q5 | +0.55 | 5.8% | -0.4 |

**For picking stocks.** The closest call of the four. Equal-weighted returns rise step by step from the most-variable-cost fifth (12.1%) to the most-fixed-cost fifth (15.4%) and the gap stays positive under every delisting assumption, but it misses the pre-registered bar, is weak in the first half, and is small in value-weighted terms (+1.4 points). Whatever premium exists lives in small caps, where trading costs are highest. Treat a high fixed-cost share as a risk trait to know about, not an edge to buy.

Annualised return by quintile (Q1 = lowest signal, Q5 = highest):

| | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| Equal-weighted | 12.1% | 12.7% | 13.4% | 14.2% | 15.4% |
| Value-weighted | 15.2% | 19.1% | 16.0% | 15.6% | 16.6% |
| Industry-neutral EW | 12.8% | 12.5% | 12.7% | 14.1% | 16.5% |

## H2b. Fixed costs plus accelerating sales (operating leverage "kicking in")

**Question.** When sales growth speeds up at a company whose costs are mostly fixed, do profits jump and does the stock outperform?

**Answer: No.** The high-fixed-cost, accelerating-sales group did not reliably beat the average of the other eight groups (t = 0.79, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** The high-fixed-cost, accelerating-sales group returned 14.8% a year against 13.5% for the average of the other eight groups, a gap of +1.2 points a year; the top group was ahead in 8 of 13 holding years. $10,000 held for the 156 months would have become $59,812 in the top group and $52,112 in the bottom one, before costs. Monthly spread t-statistic 0.79 (Newey-West 0.67).

**How much to trust it.**

- First half (formations 2011-2017): -0.6 points a year (t = -0.03; top ahead in 3 of 5 years). Second half (2018-2025): +2.3 points a year (t = 0.94; top ahead in 5 of 8 years).
- Within industries (2-digit SIC): +3.0 points a year (t = 1.82; top ahead in 9 of 13 years).
- Small caps (< $2B): -0.2 points a year (t = 0.21; top ahead in 7 of 13 years). Large caps (>= $2B): -0.2 points a year (t = 0.19; top ahead in 4 of 13 years).
- Value-weighted (secondary): -0.2 points a year (t = 0.16; top ahead in 5 of 13 years).
- Missing companies: 40.9% of the would-be top group and 35.8% of the other eight groups (average) have no price. Spread with missing firms excluded +1.2 points, t = 0.79; if every missing firm lost 30%: -1.2 points, t = -0.76 (only those with public float >= $50M: -0.3 points, t = -0.02); if every missing firm gained 15%: +1.5 points, t = 1.03 (+1.4 points, t = 0.94). **The sign changes across these assumptions.** No assumption lifts the t-statistic to 2, so the answer does not flip.
- Raw Yahoo returns, no bad-print rule: -0.8 points a year (t = -0.21; top ahead in 7 of 13 years); raw returns with only the single largest held monthly return removed: +0.9 points a year (t = 0.68; top ahead in 8 of 13 years).
- The top group after 0.5% a year of trading costs: 14.2% a year vs 13.2% for the equal-weighted universe (+1.0 points, t = 0.74) and 10.5% for IWM (+3.6 points, t = 2.00).

**Other pre-registered cuts of the returns.** High vs low fixed costs among accelerating firms: +2.1 points a year (t = 1.03). The pure interaction, (high-FCS accelerating minus high-FCS slowing) minus (low-FCS accelerating minus low-FCS slowing): -3.1 points a year on average (t = -1.19).

**Does the mechanism show up in the fundamentals?** Median change in operating margin over the next fiscal year: +0.78 percentage points for the high-fixed-cost, accelerating group vs +0.14 for all other groups; the group ranked 1 of 9 and was ahead of the rest in 12 of 13 years (t = 4.46). Difference-in-differences in margin change: +0.11 points. All cells (FCS tercile then acceleration tercile, 1 = low): 11: +0.16 | 12: +0.18 | 13: +0.55 | 21: -0.29 | 22: +0.08 | 23: +0.27 | 31: +0.28 | 32: +0.08 | 33: +0.78.

**For picking stocks.** Operating leverage does kick in inside the accounts: these companies' margins widened by a median +0.78 points the next year against +0.14 for everyone else. But most of that comes from the sales acceleration itself (the extra from high fixed costs, the difference-in-differences, is only +0.11 points), and the stocks earned no reliable premium. Spotting the setup in last year's filings is not an edge; you would have to anticipate the acceleration before it is reported.

Annualised equal-weighted return by cell:

| FCS tercile \ acceleration tercile | 1 (slowing) | 2 | 3 (accelerating) |
|---|---|---|---|
| 1 (variable costs) | 10.2% | 13.9% | 12.6% |
| 2 (middle) | 11.9% | 13.8% | 13.9% |
| 3 (fixed costs) | 16.0% | 15.1% | 14.8% |

## H3. Margin expansion on growing sales

**Question.** Among companies with growing sales, do the ones whose operating margin widened the most keep outperforming (the market under-reacts), or is it already in the price?

**Answer: No.** The biggest-margin-expansion fifth did not reliably beat the biggest-margin-contraction fifth (t = -0.08, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** The biggest-margin-expansion fifth returned 10.4% a year against 11.3% for the biggest-margin-contraction fifth, a gap of -0.9 points a year; the top group was ahead in 8 of 15 holding years. $10,000 held for the 180 months would have become $44,170 in the top group and $50,160 in the bottom one, before costs. Monthly spread t-statistic -0.08 (Newey-West -0.07).

**How much to trust it.**

- First half (formations 2011-2017): -5.3 points a year (t = -1.53; top ahead in 3 of 7 years). Second half (2018-2025): +2.7 points a year (t = 0.93; top ahead in 5 of 8 years).
- Within industries (2-digit SIC): -0.1 points a year (t = 0.24; top ahead in 8 of 15 years).
- Small caps (< $2B): -1.8 points a year (t = -0.27; top ahead in 7 of 15 years). Large caps (>= $2B): +0.3 points a year (t = 0.44; top ahead in 7 of 15 years).
- Value-weighted (secondary): -2.2 points a year (t = -0.24; top ahead in 7 of 15 years).
- Missing companies: 49.8% of the would-be top group and 46.4% of the would-be bottom group have no price. Spread with missing firms excluded -0.9 points, t = -0.08; if every missing firm lost 30%: -0.6 points, t = -0.37 (only those with public float >= $50M: -0.1 points, t = 0.08); if every missing firm gained 15%: +1.1 points, t = 0.79 (+0.7 points, t = 0.51). **The sign changes across these assumptions.** No assumption lifts the t-statistic to 2, so the answer does not flip.
- Raw Yahoo returns, no bad-print rule: -0.9 points a year (t = -0.08; top ahead in 8 of 15 years); raw returns with only the single largest held monthly return removed: -0.9 points a year (t = -0.08; top ahead in 8 of 15 years).
- The top group after 0.5% a year of trading costs: 9.9% a year vs 13.2% for the equal-weighted universe (-3.3 points, t = -0.86) and 10.5% for IWM (-0.6 points, t = 0.22).

**Fundamental sanity check (next fiscal year, CY t vs CY t-1).**

| Group | Next-year change in operating margin (median, pts) | Next-year revenue growth (median) | Change in revenue growth (median, pts) |
|---|---|---|---|
| Q1 | +0.70 | 9.3% | -4.0 |
| Q2 | -0.04 | 7.3% | -2.2 |
| Q3 | +0.01 | 6.9% | -3.5 |
| Q4 | +0.17 | 8.2% | -5.1 |
| Q5 | +1.01 | 13.4% | -17.6 |

**For picking stocks.** Last year's margin expansion is already in the price. The biggest expanders did keep improving (median margin change next year +1.01 points vs +0.70 for the biggest contractors), yet their stocks did no better. Do not buy a company just because its profits grew faster than its sales last year.

Annualised return by quintile (Q1 = lowest signal, Q5 = highest):

| | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| Equal-weighted | 11.3% | 16.3% | 13.8% | 10.9% | 10.4% |
| Value-weighted | 19.5% | 16.6% | 13.4% | 14.2% | 17.3% |
| Industry-neutral EW | 12.1% | 13.7% | 13.4% | 13.0% | 12.0% |

## Caveats

- **Coverage.** The universe holds 870 to 1,920 companies a year (median 1,339); 2,317 distinct companies in all. 92.9% of universe firm-years report an operating-income line (us-gaap OperatingIncomeLoss); the rest cannot be sorted and sit only in the universe benchmark. XBRL tagging only became mandatory for smaller companies in mid-2011, so the June 2011 formation (fiscal 2010 data) under-represents small companies, and fixed-cost share needs four years of history, so H2 starts with the June 2013 formation.
- **Missing companies.** See the table at the top. Missing firms are placed into quintiles using their own fundamentals and the breakpoints of the priced firms. Value-weighted results exclude them in every scenario (no market cap).
- **Frames alignment and look-ahead.** The SEC frames API files each fiscal year under the calendar year it overlaps most, so "CY2015" includes fiscal years ending as late as June 2016. Firm-years whose fiscal year ended after the last day of February of the formation year are dropped (a 10-K may not be filed by the end of June otherwise). For the firms used, the gap from fiscal year-end to formation is at least 4 months (median 6): about six months for December year-ends, which are most firms, but only four to five for January and February year-ends (mostly retailers), so "at least six months" is not true of every firm.
- **Restated numbers.** Frames returns the value from the most recent filing that reported a period, so 93.7% of the revenue figures used come from a filing made after the formation year (usually the comparative column of a later 10-K). Where a later filing restated or reclassified the number, the study uses information that was not available on the formation date. A spot check of 145 random firm-years against each company's first-filed 10-K found revenue differing by more than 1% in 5.5% of cases (median difference 0.00%) and operating income differing by more than 1% of revenue in 3.3%. In the same sample 95.2% of the revenue figures had been filed in a 10-K before the formation date; the rest first appear in a later 10-K (late filers, or a company's first tagged 10-K after a listing).
- **Industry codes** are each company's current SIC code, not the code at the time.
- **Market caps** use SEC share counts times Yahoo's June close, put on the same split basis with Yahoo's split history (2,306 split records, including Yahoo's spin-off adjustments); us-gaap share counts, which later filings restate for splits, are put on the basis of the filing that supplied them (2,921 filing dates looked up). A share count is used only if it agrees within 3x with another source (when two agree) and implies a market cap between 0.2% and 100x the larger of revenue and assets, which catches 1,000x tagging errors. Residual errors remain for a few dozen firm-years (for example BeOne Medicines, whose SEC count is ordinary shares while Yahoo prices the ADS, and a few post-bankruptcy share cancellations); 2.7% of universe firm-years have a reported public float below 10% of the computed market cap, some because the float is mis-tagged. These errors only touch the $50M filter, the $2B size split and value weights, not equal-weighted returns. Foreign private issuers (20-F/40-F filers, 550 registrants) are excluded because their share counts and ADS prices are on different bases.
- **Price errors.** Yahoo monthly data for small stocks contain bad prints. 54 one-month 10x round trips and 96 monthly returns above +1,000% were set to missing across all symbols, fixed before any portfolio was computed. Only 7 of these stock-months fell in stocks the study actually held: Chord Energy's November 2020 +30,991% (a bankruptcy splice: Oasis Petroleum's old shares were cancelled, so the jump never happened to a holder), Phunware's January-February 2019 round trip, Healthier Choices' 2023 round trip, and two genuine spikes that the rule also drops, GameStop's +1,625% in January 2021 and Urban One's +1,446% in June 2020. Each test reports the spread on raw returns too. Where the raw number has the opposite sign (H1, H2b), the Chord Energy month is the cause: it sits in the comparison group, and with only that month removed the raw spreads have the same sign as the cleaned ones.
- **Costs.** Only the top-group comparison deducts costs (0.5% a year). Small-cap spreads would shrink further after real bid-ask costs.
- **Several tests at once.** Four pre-registered hypotheses, each cut several ways. With that many looks, one t-statistic near 2 is weak evidence on its own; the verdict rule asks for consistency across halves, industries and delisting assumptions for that reason.

## Files

- `research/oplev/build_panel.py` data build (SEC frames, submissions, filing indexes, Yahoo), cached in `research/oplev/cache/`
- `research/oplev/run_tests.py` the pre-registered tests; `md_writer.py` renders this file
- `research/oplev/check_restatements.py` restatement spot check
- `research/oplev/panel.parquet` firm-year panel
- `research/oplev/results.json` every number; `research/oplev/quintile_returns.csv` monthly returns per quintile and cell, plus IWM and SPY

<!-- H4 section: generated by run_h4.py from results_h4.json; a rerun replaces everything below -->

## H4. Management commentary

**Question.** When management says in an earnings release or a 10-Q that operating leverage is kicking in, does the stock go on to beat companies that said nothing about it? Pre-registered in `H4_PREREG.md` before any H4 return was computed:

- **H4a (primary, carries the verdict):** companies with at least one "kicking in" statement in the 365 days before the June formation (an 8-K or 10-Q that uses "operating leverage" with a positive direction cue, from the precision-checked `commentary/` dataset) against silent companies: universe companies with no clean operating-leverage filing of any kind, positive or negative, in that window that were filing with the SEC.
- **H4b:** only companies for which that statement was the first operating-leverage mention after at least eight quiet calendar quarters (while filing in at least six of them).
- **H4c:** companies with negative operating-leverage commentary; expected to lag.
- **H4d:** do margins and sales actually improve the next fiscal year? No verdict.

Same universe, returns, bad-print rule and delisting scenarios as H1-H3. A statement counts only if its EDGAR filing date is strictly before the formation date (the last weekday of June); companies are matched on SEC CIK, so no ticker mapping is involved. The bar is t >= 2.0 on the equal-weighted monthly spread (t <= -2.0 for H4c), and unlike H1-H3 the robustness lines do not change the answer. The silent group holds 719 to 1,544 companies a year. Companies that talk about operating leverage are somewhat larger (median market cap $2.4B for the H4a group vs $1.9B for silent companies), hence the matched size-and-industry version.

**Deviations from the pre-registration**, all written into `H4_PREREG.md` before any H4 return was computed: (1) the mention and filing records start in 2010, so two quiet years can only be verified for statements from 2012 on; H4b has no portfolio in the June 2011 formation and counts only January-June 2012 statements for June 2012, so it covers 14 formations; (2) filing activity is recorded by calendar quarter, so "filing during the window" means a 10-K, 10-Q or 8-K in the four calendar quarters from July of t-1 to June of t. Items 3-9 there fix how ambiguous lines were read (formation date, the control group, the silence test, the matched version, the missing-company scenarios, H4d timing, the verdict rule). One factual correction was added after the results (see H4d); it changes no definition or number.

### H4a. Management says operating leverage is kicking in (primary)

**Answer: No.** Companies whose management said operating leverage was kicking in did not reliably beat silent companies (t = 0.48, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** Companies whose management said operating leverage was kicking in returned 13.5% a year against 13.2% for silent companies over the same 180 months, a gap of +0.4 points a year; the group that said it was ahead in 8 of 15 holding years. $10,000 held for the 180 months would have become $67,179 in the group that said it and $64,139 in the silent group, before costs. Monthly spread t-statistic 0.48 (Newey-West 0.50).

**How much to trust it.**

- First half (formations 2011-2017): +1.1 points a year (t = 0.61; ahead in 5 of 7 years). Second half (2018-2025): -0.3 points a year (t = 0.12; ahead in 3 of 8 years).
- Matched within size tercile x 2-digit SIC cells, each cell's gap weighted by its number of signal companies (98% of signal companies share a cell with a silent company in the median month): +0.2 points a year (t = 0.41; ahead in 8 of 15 years).
- Value-weighted: -2.1 points a year (t = -0.50; ahead in 5 of 15 years).
- Missing companies: 34.9% of the would-be signal group and 42.5% of the would-be silent group have no price. Spread with missing firms excluded +0.4 points, t = 0.48; if every missing firm lost 30%: +3.1 points, t = 2.99 (only those with public float >= $50M: +0.9 points, t = 1.07); if every missing firm gained 15%: +0.4 points, t = 0.61 (+0.4 points, t = 0.56). The sign does not change across these assumptions. The t-statistic gets past 2 only under -30% for all missing firms (t = 2.99, the hypothesised direction). That comes from the silent group: it has the larger missing share, and more of its missing companies are small (36% report a public float below $50M or none, against 21% in the signal group), so a blanket -30% pulls it down more. Counting only missing companies with float >= $50M, the t-statistic is 1.07. By the pre-registered rule these lines do not change the answer.
- Raw Yahoo returns, no bad-print rule: -1.4 points a year (t = -0.57; ahead in 7 of 15 years); raw returns with only the single largest held monthly return removed (CHRD in 2020-11, which sits in the silent group): +0.0 points a year (t = 0.28; ahead in 7 of 15 years).
- Company counts: 35 to 88 signal companies per formation (852 company-years, 415 distinct companies) against 719 to 1,544 silent ones. No year has fewer than 20.
- The group that said it after 0.5% a year of trading costs: 13.0% a year vs 13.2% for the equal-weighted universe (-0.2 points, t = 0.15), 10.5% for IWM (+2.5 points, t = 1.54) and 14.2% for SPY (-1.3 points, t = 0.09).

**For picking stocks.** Do not buy a stock because management says operating leverage is kicking in. The statement does line up with wider margins the next year (H4d below), but the stocks did no better than those of companies that said nothing: +0.4 points a year, ahead in 8 of 15 years, +0.2 points against silent companies of the same size and industry, and -2.1 points value-weighted. By the time the statement is in a filing, the improvement appears to be in the price.

### H4b. The same, said for the first time after two quiet years

**Answer: No.** Companies saying it for the first time after two quiet years did not reliably beat silent companies (t = 1.13, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** Companies saying it for the first time after two quiet years returned 18.0% a year against 14.2% for silent companies over the same 168 months, a gap of +3.8 points a year; the first-mention group was ahead in 8 of 14 holding years. $10,000 held for the 168 months would have become $101,472 in the first-mention group and $64,563 in the silent group, before costs. Monthly spread t-statistic 1.13 (Newey-West 1.10).

**How much to trust it.**

- First half (formations 2012-2017): +15.0 points a year (t = 2.29; ahead in 5 of 6 years). Second half (2018-2025): -3.7 points a year (t = -0.62; ahead in 3 of 8 years).
- Matched within size tercile x 2-digit SIC cells, each cell's gap weighted by its number of signal companies (98% of signal companies share a cell with a silent company in the median month): +5.2 points a year (t = 1.21; ahead in 9 of 14 years).
- Value-weighted: -2.6 points a year (t = -0.08; ahead in 6 of 14 years).
- Missing companies: 36.8% of the would-be signal group and 42.5% of the would-be silent group have no price. Spread with missing firms excluded +3.8 points, t = 1.13; if every missing firm lost 30%: +0.9 points, t = 0.63 (only those with public float >= $50M: -0.8 points, t = -0.17); if every missing firm gained 15%: +0.1 points, t = 0.26 (+0.1 points, t = 0.24). **The sign changes across these assumptions.** No assumption moves the t-statistic past the bar, so the answer does not flip.
- Raw Yahoo returns, no bad-print rule: +1.8 points a year (t = 0.49; ahead in 8 of 14 years); raw returns with only the single largest held monthly return removed (CHRD in 2020-11, which sits in the silent group): +3.4 points a year (t = 1.04; ahead in 8 of 14 years).
- Company counts: 4 to 25 signal companies per formation (165 company-years, 158 distinct companies) against 719 to 1,544 silent ones. Years with fewer than 20 signal companies, kept in and flagged: 2011 (0), 2012 (5), 2013 (9), 2014 (5), 2015 (7), 2016 (8), 2017 (4), 2018 (14), 2019 (14), 2020 (13), 2022 (10), 2023 (19), 2025 (11). Statements before 2012 cannot be checked for two quiet years, so 16 companies in the 2011-2012 formations that might qualify are left out (Deviations item 1).
- The first-mention group after 0.5% a year of trading costs: 17.4% a year vs 14.2% for the equal-weighted universe (+3.2 points, t = 0.99), 11.4% for IWM (+6.0 points, t = 1.68) and 14.9% for SPY (+2.5 points, t = 0.91).

**For picking stocks.** The "first time in two years" version looks better on paper (+3.8 points a year) but does not clear the bar, rests on a handful of stocks a year, and all of the gain comes from the 2012-2017 formations (+15.0 points a year, t = 2.29, with only 4 to 9 stocks a year); in the 2018-2025 formations the group trailed silent companies by 3.7 points a year. One strong half among many cuts is the kind of result chance produces. Not a rule to trade; at most a question to re-test once more filings have accumulated.

### H4c. Negative operating-leverage commentary

**Answer: No.** Companies with negative operating-leverage commentary did not reliably lag silent companies (t = 0.39; the pre-registered bar was -2.0), and in fact came out slightly ahead.

**Size of the effect (equal-weighted, the pre-registered headline).** Companies with negative operating-leverage commentary returned 13.3% a year against 13.2% for silent companies over the same 180 months, a gap of +0.1 points a year; the negative-commentary group was ahead in 8 of 15 holding years. $10,000 held for the 180 months would have become $64,736 in the negative-commentary group and $64,139 in the silent group, before costs. Monthly spread t-statistic 0.39 (Newey-West 0.38).

**How much to trust it.**

- First half (formations 2011-2017): +1.6 points a year (t = 0.64; ahead in 4 of 7 years). Second half (2018-2025): -1.2 points a year (t = -0.01; ahead in 4 of 8 years).
- Matched within size tercile x 2-digit SIC cells, each cell's gap weighted by its number of signal companies (100% of signal companies share a cell with a silent company in the median month): -1.8 points a year (t = -0.30; ahead in 8 of 15 years).
- Value-weighted: -2.8 points a year (t = -0.50; ahead in 7 of 15 years).
- Missing companies: 33.0% of the would-be signal group and 42.5% of the would-be silent group have no price. Spread with missing firms excluded +0.1 points, t = 0.39; if every missing firm lost 30%: +3.0 points, t = 2.02 (only those with public float >= $50M: +0.5 points, t = 0.52); if every missing firm gained 15%: -0.3 points, t = 0.16 (-0.4 points, t = 0.08). The sign does not change across these assumptions. The t-statistic gets past 2 only under -30% for all missing firms (t = 2.02, the opposite direction to the hypothesis). That comes from the silent group: it has the larger missing share, and more of its missing companies are small (36% report a public float below $50M or none, against 18% in the signal group), so a blanket -30% pulls it down more. Counting only missing companies with float >= $50M, the t-statistic is 0.52. By the pre-registered rule these lines do not change the answer.
- Raw Yahoo returns, no bad-print rule: -1.7 points a year (t = -0.30; ahead in 7 of 15 years); raw returns with only the single largest held monthly return removed (CHRD in 2020-11, which sits in the silent group): -0.3 points a year (t = 0.26; ahead in 8 of 15 years).
- Company counts: 7 to 33 signal companies per formation (256 company-years, 104 distinct companies) against 719 to 1,544 silent ones. Years with fewer than 20 signal companies, kept in and flagged: 2011 (7), 2012 (11), 2013 (15), 2014 (11), 2015 (12), 2016 (14), 2017 (15), 2018 (19), 2019 (13), 2020 (17), 2022 (15).
- The negative-commentary group after 0.5% a year of trading costs: 12.7% a year vs 13.2% for the equal-weighted universe (-0.5 points, t = 0.19), 10.5% for IWM (+2.2 points, t = 1.01) and 14.2% for SPY (-1.5 points, t = 0.13).

**For picking stocks.** Negative operating-leverage commentary did not mark a stock to avoid: those companies kept pace with silent ones (+0.1 points a year, ahead in 8 of 15 years). Their margins slipped slightly the next year (median -0.13 points against +0.09, not reliably year by year; H4d), but that was no return signal. Few companies say it (a median of 15 a year), so the test is also weak.

### H4d. Do margins follow? (fundamentals, no verdict)

**Next fiscal year, CY t vs CY t-1, the same measure as H1-H3.**

| Group | Company-years with next-year data | Next-year change in operating margin (median, pts) | Next-year revenue growth (median) | Change in revenue growth (median, pts) |
|---|---|---|---|---|
| Said it is kicking in (H4a) | 785 | +0.73 | 9.1% | -3.7 |
| First time after two quiet years (H4b) | 151 | +1.26 | 9.2% | -2.2 |
| Negative commentary (H4c) | 230 | -0.13 | 5.5% | -0.2 |
| Silent (control) | 15,685 | +0.09 | 6.2% | -1.3 |

Year by year, against silent companies: the H4a group's median margin change was ahead in 14 of 15 years (average yearly gap in medians +0.80 points, t = 3.92), and its median revenue growth ahead in 13 of 15 years (average yearly gap in medians +3.2 points, t = 5.39). H4b margin change: ahead in 12 of 14 years (average yearly gap in medians +1.63 points, t = 2.39). H4c margin change: ahead in 7 of 15 years (average yearly gap in medians -0.40 points, t = -1.55).

Timing (README point 5): the forward fiscal year ends after the company's last statement in the window in 100% of the 708 H4a company-years where its end date is on file (48 of them are June 30 year-ends that close on or just after the formation date, a correction to Deviations item 8 recorded in `H4_PREREG.md`). For 59% of H4a company-years the first statement came before the base year (CY t-1) had ended, so some of the improvement being described is already in the base year; the next-year change measures only what came after.

**For picking stocks.** The statement is informative about the business, not the stock. Companies that said operating leverage was kicking in widened margins by a median +0.73 points the next year against +0.09 for silent companies, ahead in 14 of 15 years. They also grew sales faster (9.1% against 6.2%), so the margin gain goes hand in hand with faster growth, as in H2b. Use the phrase as a prompt to study a company's cost structure, not as a reason to buy: H4a shows the stocks earned nothing extra for it.

**Files.** `research/oplev/run_h4.py` computes H4 and writes this section and the H4 rows of the short-answer table; every H4 number is in `research/oplev/results_h4.json`. `run_tests.py` rewrites this file without H4 (its own numbers in `results.json` are untouched by H4), so run `run_h4.py` after it. H4 adds three return tests to the four above; the multiple-testing caveat applies with more force.
