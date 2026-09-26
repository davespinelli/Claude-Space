# Information-advantage tests: pre-registration

Written 2026-09-26, before any data was collected.

David's brief: "Imagine that you need to have an information advantage: test things the market doesn't see, not just numbers but other things that correlate to an advantage."

## Lesson from the last month

Public numbers get priced within days. That covers filings, management commentary and state data (research/oplev, research/nowcast/gaming): seven tests, seven No's.

So every idea here must meet at least one of these conditions:
- it lives in text or records that standard datasets don't carry;
- it needs two sources joined together that nobody joins;
- it has only been public for a short time.

## Common rules (all five tests)

- **Point in time.** A signal is usable only from the first trading day after the date it became public. For a registry or database that publishes with a delay, that is the publication date, not the event date. If the publication date is unknown, use a conservative assumed lag, stated in Deviations before any return is computed.
- **Returns.**
  - Measure: the stock's return minus the return of a size-and-industry benchmark. If no benchmark can be built, use IWM for companies under $2B and SPY for the rest.
  - Source: daily prices from Yahoo (throttled; empty results can mean rate limiting). Record every company excluded for lack of prices, and run the -30% / +15% bounds for missing companies as in research/oplev.
- **Costs.** Report results after 0.5% a year, or 0.2% per event for event studies.
- **Verdict bar: t >= 2.5**, not 2.0. We are testing five ideas at once; at 2.0, one of them would pass by luck about a fifth of the time. A result must also have the pre-registered sign in both halves of the sample to be a Yes. Anything else is No; report it regardless.
- **Data forcing a change.** Record it in a "Deviations" section of that test's own PREREG before computing any return. If a test is infeasible (the data don't exist, or can't be dated), say so and stop. Do not swap in a different idea.
- **Shared rate limits:**
  - SEC EDGAR: at most 2 requests a second per test (five tests share one IP and SEC's 10-a-second limit), User-Agent "Claude Space research dspinjr@gmail.com".
  - Yahoo: throttle and retry.
- **Output.** research/infoedge/<test>/ holds scripts, data/ (small cleaned files), cache/ (gitignored) and RESULTS.md, with the plain-English answer first and the style of research/oplev/RESULTS.md.

## INFO-1. Hidden customer links

- **Why the market might not see it:** a small supplier's big customer is named only in its 10-K text ("Walmart accounted for 23% of net sales"). When the customer's stock moves on news, investors in the supplier are slow to connect the two (Cohen and Frazzini's "economic links"). Small caps whose links exist only in text are where the delay should be longest.
- **Links:**
  - From every 10-K filed 2010 onward, extract named customers at 10% or more of revenue, using full-text search plus parsing.
  - Map customer names to listed companies with an alias list of large US-listed companies.
  - A link is active from the 10-K's filing date until the next 10-K.
- **Signal:** the month-t return of the supplier's linked customers (average if several).
- **Test:**
  - Each month-end, rank suppliers with at least one listed customer by that signal.
  - Take suppliers in the top fifth minus those in the bottom fifth, equal-weighted, and measure the spread in month t+1.
  - Primary statistic: NW(6) t >= 2.5, with the same sign in both halves.
  - Secondary: suppliers under $2B only; value-weighted; links where the customer share is 20% or more.

## INFO-2. Insider trading-plan terminations (public since 2023)

- **Why the market might not see it:** since 2023, companies must say in their 10-Q/10-K when an officer or director adopts or terminates a Rule 10b5-1 trading plan (Item 408(a)). It is a few lines buried in "Other Information", recently XBRL-tagged (ecd taxonomy). A planned seller cancelling a sell plan early may know good news is coming. Adopting a large new sell plan may signal the opposite.
- **Events:** each disclosed termination, before its scheduled end date, of a plan that included sales by a CEO, CFO or director. Dated by the filing date of the 10-Q/10-K that disclosed it.
- **Primary:** abnormal return over trading days +1 to +60 after the filing date. Expected sign: positive. t is computed across events, clustered by filing month.
- **Secondary:**
  - new sell-plan adoptions in the top 20% by planned shares as a percentage of shares outstanding (expected negative);
  - companies under $2B.
- **Power warning:** only about 2.5 years of data. If fewer than 150 termination events exist, report the result as underpowered, still under the same verdict rule.

## INFO-3. Government contract awards nobody announced

- **Why the market might not see it:** federal contract awards appear on USAspending/FPDS, but many small contractors never announce them. An award that is large relative to a small company's market value is material news sitting in a government database.
- **Events:**
  - new prime awards, or modifications, of at least 2% of the recipient's market cap;
  - recipient mapped to a US-listed parent under $2B (through UEI/DUNS parent names plus an alias list);
  - no 8-K from the company within 5 trading days either side.
- **Public date:** civilian agencies' action date + 5 business days; DoD awards action date + 90 days, because DoD data is held back. If the actual publication date can be found in FPDS/USAspending fields, use it instead, and record which in Deviations.
- **Primary:** abnormal return over trading days +1 to +20 after the public date. Expected sign: positive. Same bar.
- **Secondary:** awards of 5% or more of market cap; civilian only.

## INFO-4. Quiet clinical-trial registry changes

- **Why the market might not see it:** biotech companies update ClinicalTrials.gov records (primary completion date pushed back, enrollment cut, status changed to suspended, terminated or withdrawn), sometimes weeks before saying anything. The registry keeps a dated history of every version.
- **Events:**
  - trials sponsored by US-listed companies under $5B;
  - a record version that delays the primary completion date by 6 months or more, cuts target enrollment by 25% or more, or moves status to suspended, terminated or withdrawn;
  - no 8-K from the sponsor within 5 trading days before the version date.
  - Public date = the version date in the registry history + 1 trading day, or the posting date if the history distinguishes them.
- **Primary:** abnormal return over trading days +1 to +20. Expected sign: negative. Same bar.
- **Secondary:** Phase 2/3 trials only; companies under $1B.
- **Feasibility first:** confirm the record history, with its dates, can be retrieved for thousands of trials. If not, stop and say so.

## INFO-5. Insider gifts

- **Why the market might not see it:** officers and directors report stock gifts (Form 4 code G). Gifts to charity or family, timed at high prices, maximise the tax deduction and can reflect private knowledge. Gifts attract little attention compared with open-market sales.
- **Data:** SEC Form 3/4/5 bulk data sets, already cached at data/sec_cache/form345, from 2006 on.
- **Events:** gifts by an officer or director worth at least $1M, or at least 1% of the donor's holdings, dated by Form 4 filing date. Also report on the gift date, for information only; the verdict uses the filing date.
- **Primary:** abnormal return over trading days +1 to +60 after the filing date. Expected sign: negative. Same bar.
- **Secondary:** gifts in December; CEO/CFO gifts; companies under $2B; the pre-filing window (gift date to filing date), for information only.
