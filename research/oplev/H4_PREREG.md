# H4 pre-registration: does management saying "operating leverage is kicking in" predict returns?

Written 2026-09-23, after H1-H3 were reported and before any H4 return was computed. Nothing below may change once the first H4 return is computed. Anything added later goes in a section marked "added after results".

## Data

- Signal: `commentary/clean_events.csv.gz`. It is already non-financial, SPAC-free and precision-checked; drop rows with missing `sic`. Negative events: `commentary/clean_negative_events.csv.gz`. Filing presence: `commentary/filer_presence_by_cik_quarter.csv.gz`.
- Returns, universe and machinery: exactly as in H1-H3 (`run_tests.py`):
  - June formation 2011-2025, July-to-June holding, priced, >= $50M, non-financial;
  - the same `clean_returns` rule and delisting scenarios (-30% / +15%);
  - equal-weighted headline, t-stat = mean / (sd / sqrt(n)) on monthly spread returns, Newey-West 6 reported beside it.
- Join key: `cik`. A mention is usable only if `file_date` < the portfolio's formation date (strictly before), per commentary/README section 4.

## Hypotheses

**H4a (primary, carries the verdict).**
- Signal group S: at each formation, companies with at least one clean event where `kicking_in` is True and `file_date` falls in the 365 days before formation.
- Control group N: companies in the universe with no clean event of any kind in that window, and at least one filing in `filer_presence` during it.
- Test: S minus N, equal-weighted monthly spread.
- Answer: **Yes** only if t >= 2.0 on the headline spread. Otherwise **No**. This is the same bar as H1-H3.

**H4b (secondary): a first mention after a silence.**
- S is restricted to companies whose first `kicking_in` event comes after at least 8 calendar quarters with no "operating leverage" mention of any kind (`mentions_by_cik_quarter`), while filing in at least 6 of those 8 quarters.
- Same N, same test, same bar. Reported as secondary.

**H4c (secondary): negative commentary.**
- Signal: companies with a clean negative event in the window, against N.
- Expected sign: negative. Answer Yes only if t <= -2.0.

**H4d (fundamentals, no verdict).**
- Next fiscal year's change in operating margin (median) and revenue growth for S versus N.
- Use fiscal periods ending after `file_date` (README point 5), in the same table format as H1-H3.

## Robustness reported for every test (does not change the verdict)

- First half (formations 2011-2017) and second half (2018-2025).
- Matched: spreads within size tercile x 2-digit SIC cells, averaged with S-count weights. This matters because companies that talk about operating leverage skew larger and toward software, banks (already excluded) and industrials.
- Value-weighted.
- Delisting scenarios (-30% / +15%) with missing shares for S and N.
- Raw returns without the bad-print rule.
- Company counts in S per formation year. Years with fewer than 20 S companies stay in and are flagged.
- Top group after 0.5% a year of costs, against the equal-weighted universe, IWM and SPY.

## Plain-English line required

Each H4 test ends with a "For picking stocks" sentence, as H1-H3 do.

## Deviations

Written 2026-09-23 13:50 EDT, before any H4 return was computed (only group membership counts had been looked at). Nothing above this section was changed. Items 1-2 are forced by the data; items 3-8 record how an ambiguous line was read, so the reading is fixed before the results are known.

1. **H4b cannot be checked before 2012.** `mentions_by_cik_quarter` and `filer_presence` both start in 2010 Q1, so eight quiet quarters can only be verified for an event filed in 2012 Q1 or later. A company whose first in-window `kicking_in` event is earlier cannot be confirmed as a first mention after silence and is left out of H4b's S (it stays in H4a's S and never enters N). As a result H4b has no portfolio for the June 2011 formation, and the June 2012 formation uses only events filed January to June 2012. H4b covers formations 2012-2025; its first half is 2012-2017.
2. **Filing presence is quarterly, not daily.** "At least one filing in `filer_presence` during the window" is read as at least one 10-K, 10-Q or 8-K in calendar quarters Q3 of t-1 through Q2 of t, the four quarters that make up the 365-day window. The few days of the window that fall in Q2 of t-1 are not counted.
3. **Formation date.** The portfolio is formed at the June close, so the formation date is the last weekday of June t (no exchange holiday falls on it in 2011-2025). The window is formation date minus 365 days <= `file_date` < formation date, so a filing dated on the formation day is not used (README section 4, point 2: usable from the next trading day).
4. **Control group N.** "No clean event of any kind" means no row in `clean_events.csv.gz` (either value of `kicking_in`) and no row in `clean_negative_events.csv.gz` with `file_date` in the window. Universe companies with only non-`kicking_in` clean events are in neither S nor N for H4a and H4b.
5. **H4b's silence test.** The eight quarters are the eight calendar quarters before the calendar quarter of the company's first `kicking_in` event in the window. "No operating leverage mention of any kind" means `ol_any`, `ol_positive` and `ol_negative` are all zero (or there is no row) in `mentions_by_cik_quarter` for each of them; "filing" means a row in `filer_presence`. A mention earlier in the same calendar quarter as the event is not checked (the spec works in calendar quarters).
6. **Matched version.** Size terciles use each June's market-cap breakpoints from the priced universe. A cell is formation year x size tercile x 2-digit SIC. Each month, the spread is the average of the cells' S-minus-N equal-weighted spreads, weighted by the cell's number of S companies at formation, over cells with at least one S and one N return that month. The same weights applied to S and N separately give matched S and N returns, so years won can be counted. Missing companies have no market cap and are not in this version.
7. **Missing-company scenarios.** Missing companies (pass the fundamentals filters, no price) are put in S or N by the same `cik` and date rules, including the presence rule for N, and the -30% / +15% scenarios are run exactly as `run_tests.py` runs them (all missing companies, and only those with public float >= $50M).
8. **H4d timing.** N has no event date, so the S-versus-N comparison has to be aligned to the formation date. It uses the H1-H3 fields: fiscal year CY t (the year after formation) against CY t-1. Every fiscal year in CY t ends in July of t or later, after every `file_date` used, which satisfies README point 5 for the forward year; this is checked in the data. The base year CY t-1 ends before some events and after others (a 10-Q or release filed during that fiscal year); the share is reported. To give H4d a headline number, the S-minus-N difference in medians is also computed year by year (mean, t across years, years S ahead), as H2b's fundamental check was.
9. **Verdict.** As written above: t >= 2.0 (H4c: t <= -2.0) on the headline equal-weighted spread gives Yes, anything else No. Unlike H1-H3 there is no "Mixed" label; the robustness lines are reported but do not change the answer.

## Added after results

Written 2026-09-23 after the H4 returns were computed. It corrects a factual statement in Deviations item 8 and changes no definition or number.

- Deviations item 8 says every fiscal year in CY t ends in July of t or later. In the data, companies with June 30 fiscal year-ends have CY t ending on June 30 of t, the formation day or one to two days after it (48 of the 708 checkable H4a company-years, 587 of 14,266 in N). Each of these still ends after every `file_date` used, because `file_date` is strictly before the formation date, so the README point 5 condition holds in all 708 checkable H4a cases.
