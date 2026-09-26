# INFO-2. Insider trading-plan terminations: pre-registration

Copied unchanged from `research/infoedge/PREREG.md` (written 2026-09-26, before any data was collected). The spec and the common rules are locked. Everything the data forced is under "Deviations" at the end, written before any return was computed.

## Common rules (all five tests), as locked

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

## INFO-2. Insider trading-plan terminations (public since 2023), as locked

- **Why the market might not see it:** since 2023, companies must say in their 10-Q/10-K when an officer or director adopts or terminates a Rule 10b5-1 trading plan (Item 408(a)). It is a few lines buried in "Other Information", recently XBRL-tagged (ecd taxonomy). A planned seller cancelling a sell plan early may know good news is coming. Adopting a large new sell plan may signal the opposite.
- **Events:** each disclosed termination, before its scheduled end date, of a plan that included sales by a CEO, CFO or director. Dated by the filing date of the 10-Q/10-K that disclosed it.
- **Primary:** abnormal return over trading days +1 to +60 after the filing date. Expected sign: positive. t is computed across events, clustered by filing month.
- **Secondary:**
  - new sell-plan adoptions in the top 20% by planned shares as a percentage of shares outstanding (expected negative);
  - companies under $2B.
- **Power warning:** only about 2.5 years of data. If fewer than 150 termination events exist, report the result as underpowered, still under the same verdict rule.

## Deviations and operational definitions

Written 2026-09-26 after collecting and classifying the events, before any stock return was computed.

### D1. Data source for the disclosures (forced)

- The companyfacts and frames APIs do **not** carry ecd facts (checked: Apple's companyfacts has only `dei` and `us-gaap`; `frames/ecd/...` and `companyconcept/.../ecd/...` return 404). The Item 408 tags are dimensional (one context per person), which those APIs drop.
- Source used instead: the SEC's **Financial Statement and Notes data sets** (2023q2 to 2026-08, 23 files), which carry every XBRL fact of every 10-Q/10-K, including `ecd:Rule10b51ArrTrmntdFlag`, `ecd:Rule10b51ArrAdoptedFlag`, `ecd:TrdArrIndName`, `ecd:TrdArrIndTitle`, `ecd:TrdArrAdoptionDate`, `ecd:TrdArrTerminationDate`, `ecd:TrdArrExpirationDate`, `ecd:TrdArrDuration`, `ecd:TrdArrSecuritiesAggAvailAmt` and `ecd:MtrlTermsOfTrdArrTextBlock`, with their dimension members.
- **Tagging was phased in.** Share of original 10-Q/10-K filings carrying any ecd Item 408 flag: about 33% of filings in 2023 H2, 60-80% in 2024, about 90% from February 2025 (`data/coverage_by_month.csv`). Most untagged filings never mention Rule 10b5-1 (trusts, funds, asset-backed issuers, and small companies not yet subject to Item 408). The untagged filings that do mention "10b5-1" (3,097, plus 218 filings missing from the data sets; found with EDGAR full-text search) are parsed from their text (D3).

### D2. Turning the tags into events (operational definitions)

- **One record per person-context.** Facts are grouped by filing and dimension context (the `Individual` / `TradingArr` members). Name and title are filled from the same person's other contexts in the same filing. A filing's undimensioned flags are treated as summary flags when the filing has person-level contexts.
- **Rule 10b5-1 terminations only** (`Rule10b51ArrTrmntdFlag = true`). Non-Rule 10b5-1 arrangements are a different instrument and are left out.
- **Mis-tagged "terminations".** A termination flag whose tagged termination date is after the filing date is the scheduled end of a newly adopted plan tagged with the wrong element (297 contexts); these are not terminations. A context flagged both adopted and terminated with an adoption date but no termination date is an adoption.
- **CEO, CFO or director** from the tagged title (or, if missing, the words after the person's name in the text): "chief executive", "CEO", "principal executive officer"; "chief financial", "CFO", "principal financial officer"; "director" (not "managing director", "director of ..."), "chair", "chairman", "board member". A person with several roles counts once.
- **"Included sales".** Excluded only when the person's text describes a purchase-only plan. When there is no text, the plan is assumed to include sales (almost all disclosed plans are sell plans).
- **Classification of every termination** (only information in the disclosing filing is used, so the classification is point-in-time), applied in this order:
  1. *Replacement / modification*: the same person (same dimension member or same first initial and last name) adopted a Rule 10b5-1 or other trading arrangement in the same filing, dated on or after the termination date; or the person's text says the plan was modified, amended, replaced or superseded. A modification is legally a termination plus a new adoption; the insider still intends to sell. **Excluded from the primary**, reported as a robustness line.
  2. *Expired / completed*: the text says the plan ended by its own terms, on completion or execution of all sales, or became fully exercised. **Excluded.**
  3. If a scheduled end date is tagged (`TrdArrExpirationDate`): early if the termination is more than 3 days before it, otherwise expired.
  4. If the text gives a scheduled end ("expire on", "until", "through", "scheduled to terminate", "would have expired") more than 3 days after the termination date: early.
  5. Text says "expired" / "natural expiration" with no early-termination wording: expired.
  6. Otherwise: **early** (the pre-registered event). A disclosed "termination" with no expiry wording is taken at face value.
- **Stale disclosures.** A termination dated more than 100 days before the end of the reporting period repeats an earlier disclosure; excluded (the first disclosure, if in the data, is the event).
- **One event per person per filing**; the same company-person-termination date disclosed again later keeps the first filing. Amendments (10-Q/A, 10-K/A) are not used.
- **Event date** = the EDGAR filing date of the 10-Q/10-K.

### D3. Text-parsed events from untagged filings (forced by D1)

- For the untagged filings that mention "10b5-1", the Item 408 passage is parsed from the document text: statements containing "terminat" after the boilerplate "adopted or terminated" is removed and negative sentences ("no director or officer ...") are dropped; person, title, termination date and the D2 classification are read from the statement.
- The same parser is first run on 200 tagged filings known (from XBRL) to contain a termination and 200 that do not. **Rule fixed in advance:** if the parser's precision for "this filing has an early termination by a CEO, CFO or director" is at least 80% on that validation sample, text-parsed events join the headline sample; otherwise they are reported only as a robustness line. The tagged-only result is reported in either case. The validation numbers are added below before any return is computed.
- **Validation result (before any return):** 400 filings; the XBRL answer has 71 filings with a primary-type event. First pass: the parser flagged 41, of which 34 agree (precision 83%, recall 48%). Of the 7 disagreements, 4 were replacements the parser misses (the same person adopted a new plan), 1 a subsidiary CEO, 1 a CFO whose XBRL title tag says only "Section 16 Officer" (the parser is right there), 1 a table header read as a name. A spot check of untagged filings then showed the parser reading non-Item-408 passages (SPAC trust terms, buyback "trading plans") and non-person "names" ("Initial Business Combination"). Three fixes, made before any return: the passage must mention "10b5-1" or "trading arrangement" (not just "trading plan"); a "name" containing words such as Agreement, Plan, Program, Board, Company is rejected; and a prose "termination" sentence must mention a plan ("10b5-1", "trading plan", "the plan", "pre-arranged" ...), which drops terminated employment terms that sit in the same Item 5. Re-validated: **precision 85% (34/40), recall 48% (34/71)**; for "any termination", precision 100%, recall 55%. Precision clears 80%, so **text-parsed events join the headline sample**, flagged `source = text`. Their main weakness (missed replacements) biases them towards including some modifications; the tagged-only line shows whether that matters. Details in `data/text_validation.csv`.

### D4. Returns

- **Window.** Day 0 is the last trading day on or before the filing date; the abnormal return is the buy-and-hold stock return from the close of day 0 to the close of day +60 minus the benchmark's buy-and-hold return over the same days (so it starts with the first trading day after the filing date). A stock that stops trading inside the window is assumed to earn the benchmark afterwards. Events whose day +60 is after the last price date (2026-09-25) are excluded (filings after 2026-07-01).
- **Benchmark (size and industry).** Universe: every 10-Q/10-K filer in the notes data sets with Yahoo prices. Market cap = Yahoo close x `dei:EntityCommonStockSharesOutstanding` from the company's latest filing (summed over share classes). Each month-end, stocks with price >= $1 are put into market-cap quintiles and Fama-French 12 industries (from SIC). The benchmark is the equal-weighted daily return of the event firm's size-by-industry cell (the event firm itself excluded); daily returns above +100% or below -75% are dropped from the benchmark as bad prints; a cell with fewer than 10 stocks falls back to the size quintile. IWM (under $2B) / SPY (the rest) is reported as a robustness line.
- **t-statistic.** Mean abnormal return across events divided by its standard error clustered by filing month (with the G/(G-1) small-sample factor).
- **Halves.** Events sorted by filing date and split at the median filing date.
- **Costs.** 0.2% per event subtracted from the mean, in the direction of the trade (for the adoption secondary, whose expected sign is negative, the trade is short, so the cost is added to the mean abnormal return).
- **Verdict statistic.** The mean abnormal return after the cost divided by the clustered standard error must reach 2.5 in the expected direction, and the gross mean must have the expected sign in both halves. The gross t is reported too.
- **Missing prices.** Events whose company has no Yahoo price are listed, and the headline is re-run with each missing event assigned -30% and +15%.
- **Robustness lines (information only, not the verdict):** tagged-only events; early plus replacements; days +2 to +60; IWM/SPY benchmark; 1%/99% winsorized abnormal returns; one event per filing.

### D5. Secondaries

- **Large sell-plan adoptions.** Rule 10b5-1 adoptions by any officer or director (Item 408 covers only officers and directors), not purchase-only, with a tagged `TrdArrSecuritiesAggAvailAmt`. Planned shares / shares outstanding from the same filing's cover page; ratios above 50% are tagging errors and dropped. "Top 20%" = the top fifth of that ratio across all adoption events in the sample (full-sample cutoff). Adoption events come from tagged filings only (text parsing does not read amounts reliably). Same window, benchmark, clustering and bar; expected sign negative.
- **Under $2B.** The primary events whose market cap on day 0 (close x cover-page shares) is below $2B.

### D6. Diagnostics added at the coordinator's request (before any INFO-2 return was computed)

INFO-5 found that a benchmark built only from companies that still have Yahoo prices is survivor-built and makes small stocks look bad on any date. Two lines are reported next to the headline. They do not change the verdict rule; if the headline passes but either line removes the effect, the answer says so.
- **Placebo dates.** For each priced primary event, 5 dates (seed 20260926) are drawn from trading days in the same calendar year, inside the stock's priced life, with a complete +60 window and at least 60 trading days from any of the company's own termination disclosures. The same benchmark code gives a placebo abnormal return; the line reports the placebo mean and event minus placebo (per event: its abnormal return minus the mean of its own placebos), t clustered by filing month. Also run for the under-$2B events and the top-20% adoptions (adoption placebos avoid the company's top-20% adoption filings).
- **IWM / SPY only.** The headline window against IWM (under $2B) or SPY (the rest), also with its placebo difference.
