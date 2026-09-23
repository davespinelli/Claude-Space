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
