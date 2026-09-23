# Operating-leverage commentary dataset

**The question.** When management says "operating leverage" in an SEC filing or an earnings release, does anything follow, such as wider margins or a better stock? This folder holds the commentary side of that study: every 2010-2026 filing that uses the phrase, a firm-by-quarter table of those mentions, a hand check of how clean the matches are, and a first descriptive look. A separate job is building the financials and returns panel. The last section explains how to join the two.

Built 2026-09-23 from SEC EDGAR full-text search. Every number below comes from the files in this folder. The full tables are in `descriptive_stats.md` and `stats/`.

---

## 1. What we collected

**Source.** EDGAR full-text search (`efts.sec.gov/LATEST/search-index`). We ran exact-phrase queries over 8-K, 10-Q and 10-K filings (amendments included and flagged), filed 2010-01-01 to 2026-09-23. Each phrase was run separately, so every row records which phrase matched. The search indexes each document inside a filing separately. A match therefore points to a specific file: the 10-Q itself, or the EX-99.1 earnings release attached to an 8-K.

**Search hits (matched files) by phrase and form:**

| phrase | 8-K | 10-Q | 10-K | all | distinct filings | distinct companies |
|---|---:|---:|---:|---:|---:|---:|
| "operating leverage" | 18,985 | 7,500 | 5,041 | 31,526 | 29,600 | 3,659 |
| "positive operating leverage" | 2,392 | 422 | 232 | 3,046 | 2,722 | 308 |
| "negative operating leverage" | 189 | 111 | 67 | 367 | 344 | 78 |
| "operating deleverage" | 29 | 36 | 19 | 84 | 84 | 18 |
| "incremental margin" | 1,182 | 605 | 388 | 2,175 | 2,118 | 497 |
| "incremental margins" | 785 | 252 | 298 | 1,335 | 1,301 | 336 |
| "fixed cost absorption" | 1,054 | 1,022 | 435 | 2,511 | 2,427 | 387 |
| "fixed-cost leverage" | 751 | 570 | 294 | 1,615 | 1,572 | 286 |

In total, 4,079 companies (CIKs) matched at least one phrase, across 35,861 filings. For every phrase and form, the sum of the per-slice totals equals the total the search engine reports. The check is in `fetch_totals_check.csv`.

**Where the broad phrase shows up.** 42% of "operating leverage" hits are in 8-K Item 2.02 exhibits (earnings releases, call transcripts, results decks). Another 17% are in other 8-K EX-99 exhibits, mostly investor-day decks. The remaining 39% are in the 10-Q or 10-K document itself.

**Supplementary direction phrases (not in the original list).** The hand check showed two problems:
- "positive operating leverage" is almost entirely bank language.
- Industrial companies usually signal direction with a modifier instead, such as "improved operating leverage" or "reduced operating leverage".

We therefore also pulled 17 direction phrases into `tone_mentions.csv.gz`, which has the same layout:
- Positive: *improved, improving, favorable, increased, better, greater, higher* operating leverage, plus "operating leverage *on/from higher*".
- Negative: *reduced, lower, unfavorable, less, decreased* operating leverage, "*loss of / lack of* operating leverage", and "operating leverage *on lower*".

Together they matched 6,559 files at 1,366 companies. The largest are "improved operating leverage" with 2,468 files and "reduced operating leverage" with 395. Every one of these files is also in the "operating leverage" set, which confirms the search index is internally consistent.

---

## 2. How clean is it? (precision check)

We fetched the matched documents, stripped the HTML and read the text around the phrase by hand. Every snippet, label and one-line reason is in `precision_sample.md`, `precision_sample_10k.md` and `precision_sample_validation.md`.

**Random sample of 40 "operating leverage" files (all companies, all forms):**

| label | n | share |
|---|---:|---:|
| (a) management describing its own operating leverage as positive or improving | 32 | 80% |
| &nbsp;&nbsp;&nbsp;of which *realized* ("margins rose because of operating leverage") | 14 | 35% |
| &nbsp;&nbsp;&nbsp;of which *forward* ("we expect / will drive operating leverage") | 15 | 38% |
| &nbsp;&nbsp;&nbsp;of which *model claim* ("our model has significant operating leverage") | 3 | 8% |
| (b) negative or deleveraging | 2 | 5% |
| (c) risk-factor or other boilerplate | 2 | 5% |
| (d) bank or financial-company usage | 4 | 10% |
| (e) other | 0 | 0% |

Five of the 40 files came from financial companies (SIC 6000-6999). Four of those were (d) and one was (c). Among the 35 non-financial files, 32 (91%) were genuine (a).

**Do we need to exclude financials? Yes.** Banks use "positive operating leverage" as a routine metric: revenue growth minus expense growth. They account for:
- 29.9% of all "operating leverage" filings;
- 86.6% of "positive operating leverage" filings (banks alone, SIC 60, are 81.2%).

Without the financials filter, the tone field `net_tone` (positive minus negative phrase counts) mostly measures bank reporting habits. Insurers also use the phrase in an unrelated sense: premiums divided by equity.

**Do we need to strip risk-factor sections? Mostly not, if 10-Ks are handled with care.** The random sample contained no risk-factor hits. Because 10-Ks were under-represented in it, we drew 20 more files from 10-Ks only:
- 5 were (a).
- 6 were (c): 2 risk factors, 3 SPAC boilerplate, and 1 non-GAAP definition.
- 6 were (d).
- 3 were (e).

Boilerplate is therefore mainly a 10-K problem, and much of it is SPAC template language. SPACs are excluded by the SIC filter plus a name filter, because one SPAC carried a software SIC code. In 8-Ks and 10-Qs, boilerplate appeared rarely: once in a forward-looking-statements legend, once in a seasonality footnote and once in a non-GAAP definition.

**Recommended event definitions** (both in `clean_events.csv.gz`, one row per company and filing):

1. **`clean_events` (broad):** the filing matched "operating leverage", and all of the following hold:
   - it is an original filing, not an amendment;
   - the match is in an 8-K EX-99 or 8-K main document, a 10-Q, or a 10-K (main document or EX-13);
   - the company's SIC is known and outside 6000-6999;
   - the company name does not look like a SPAC;
   - the filing matched none of the negative phrases.

   This gives 19,128 filings from 2,678 companies. Scored on the 69 hand-labelled files that fall in it, 90% are (a). Only 43%, however, are *realized* statements; the rest are forward-looking or pitch language.

2. **`kicking_in == True` (strict, the recommended "management says operating leverage is kicking in" event):** a broad event that meets two further conditions:
   - it comes from an 8-K or a 10-Q, the timely channels;
   - the same filing contains a positive direction cue: "positive operating leverage", or one of the positive modifiers listed in section 1.

   This gives 3,575 filings from 967 companies (1,965 from 8-Ks and 1,610 from 10-Qs). On the 14 labelled files that fall in it, 86% are (a) and 64% are realized.

3. **`clean_negative_events.csv.gz`:** filings that would otherwise qualify but matched a negative phrase. This gives 1,134 filings from 226 companies. Treat it as noisy. Only 2 of the 5 labelled files in it were true negatives. The rest were conditional wording ("to lessen unfavorable operating leverage") or a risk factor.

These scores rest on a few dozen files each. A 90% share measured on 30 files has a 95% confidence interval of roughly 74-98%. Precision was checked only for "operating leverage" and its derived events. The other phrases were not hand-checked. Their industry mix, below, suggests "incremental margin" often carries a utility or midstream meaning.

---

## 3. What the counts show

**Usage has roughly doubled as a share of companies.** The share of companies filing a 10-K or 10-Q that also said "operating leverage" that year:

| year | share of filers |
|---|---:|
| 2010 | 6.2% |
| 2015 | 8.0% |
| 2020 | 9.5% |
| 2021 | 11.2% |
| 2025 | 12.0% |
| 2026 to Sep 23 | 15.4% |

The 2026 figure is a partial year. On a like-for-like January 1 to September 23 basis, 1,059 companies used the phrase in 2026, against 704 in 2025, a rise of 50%. This is not a change in search coverage. Over the same windows:
- neutral phrases were flat or falling: "gross margin" appeared in 1,670 10-Ks in 2025 and 1,648 in 2026, and "economies of scale" in 933 and 866;
- "operating leverage" rose from 306 to 408 10-K hits and from 336 to 457 10-Q hits.

The rise is broad: software, semiconductors, medical devices and banks all increased. That fits the recent run of management commentary on AI and efficiency, but we have not verified the cause.

**2020 was not a spike in talk. It was a silence, with a tone flip.**
- The number of companies saying "operating leverage" fell from 406 in 2020 Q1 to 248 in 2020 Q2, the low point of 2019-2023.
- Companies with a `kicking_in` event fell to 27 in 2020 Q2.
- Companies with a negative event rose to 22 in 2020 Q1 and 24 in 2020 Q3, the two highest quarters of 2019-2023.
- The exact phrases "negative operating leverage" and "operating deleverage" barely registered: 16 companies in 2020.
- The clear 2020 signal is in "fixed cost absorption", which nearly doubled as plants idled: 83 8-K and 88 10-Q filings in 2020, against 45 and 48 in 2019.

**2021 was the step-up year. 2022 was not a spike.**
- Companies using the phrase rose from 678 to 885 in 2021, and `kicking_in` companies reached 74 in 2021 Q3, when only 2 companies had a negative event. That stayed the quarterly record until 2026: 97 in 2026 Q2 and 110 so far in 2026 Q3.
- 2022 was flat at 871 companies, 10.9% of filers. "Incremental margin" in 8-Ks peaked at 109 filings in 2022.
- The negative-event count peaked in 2024, at 108 filings from 44 companies; 24 companies had one in 2024 Q4, equal to the 2020 Q3 high.

**Usage is concentrated by sector.** By share of "operating leverage" filings:

| 2-digit SIC | sector | filings | companies |
|---|---|---:|---:|
| 60 | banks | 17.2% | 305 |
| 73 | business services and software | 16.1% | 622 (the most companies) |
| 36 | electronics and semiconductors | 6.1% | |
| 35 | machinery | 5.1% | |
| 38 | instruments and medical devices | 4.6% | |

These top five sectors make up 49.1% of all filings.
- "Fixed cost absorption" is a manufacturing term: chemicals and pharma, semiconductors, transport equipment, machinery and food. Only 2.9% of its filings come from financials.
- "Incremental margin" is led by utilities (14.5%), machinery (12.0%) and software (9.6%).

**The same companies say it quarter after quarter.**
- Overall, 5.6% of active company-quarters contain a mention.
- A company that mentioned "operating leverage" in one quarter mentions it again the next quarter 63.0% of the time.
- A company that uses the phrase at some point, but did not in a given quarter, mentions it the next quarter only 7.3% of the time.
- Year to year, the repeat rate is 61.4%, measured over 10,103 company-years.
- 30.4% of companies used the phrase in just one quarter. The 22% of companies with 9 or more mention-quarters account for 67% of all mention company-quarters.
- Nine companies mention it in all 66 full quarters: Principal Financial, TE Connectivity, Allstate, Martin Marietta, Investors Title, PNC, State Street, Choice Hotels and ITW. Some text is recycled almost word for word for years; Saia's 10-K strategy paragraph ("we gain operating leverage by growing volume and density...") is nearly identical in 2011 and 2026.

**Implication for the study.** Level variables such as "mentions operating leverage" mostly capture a company's reporting habit. The informative event is probably the *change*: a company's first mention, or first `kicking_in`, after a long gap. `mentions_by_cik_quarter.csv.gz` combined with `filer_presence_by_cik_quarter.csv.gz` makes that easy to build.

---

## 4. How to join this to a firm-year returns panel (no look-ahead)

1. **Key on CIK.** Every table here uses `cik` as a plain integer without leading zeros. If the returns panel is keyed on ticker or PERMNO, map it to CIK with a *historical* link, such as the CRSP/Compustat CIK link. Do not use today's `company_tickers.json` for that mapping, because tickers get reused. A company keeps its CIK through name changes, and a de-SPAC keeps the SPAC's CIK. The `display_name` strings sometimes show present-day tickers, so never join on them.
2. **Date every mention by `file_date`,** the EDGAR filing date. Do not use `period_ending` or the calendar quarter. `file_date` is the business day EDGAR accepted the filing; filings accepted after 5:30 pm ET get the next business day. Earnings-release 8-Ks are furnished on the day of the press release or a little later, so `file_date` is never *before* the news was public. Treat a mention as usable from the **next trading day after `file_date`**.
3. **Aggregate over a trailing window that ends before the return window starts.** For a firm-year row whose returns start on `formation_date` (for example, four months after fiscal year-end, so the 10-K is out):

```python
import pandas as pd
ev = pd.read_csv("research/oplev/commentary/clean_events.csv.gz", parse_dates=["file_date"])
x = panel[["cik", "fiscal_year", "formation_date"]].merge(
        ev[["cik", "adsh", "file_date", "kicking_in", "event_channel"]], on="cik", how="left")
x = x[(x.file_date < x.formation_date) &                       # strictly before: no look-ahead
      (x.file_date >= x.formation_date - pd.Timedelta(days=365))]
sig = x.groupby(["cik", "fiscal_year"]).agg(n_clean=("adsh", "nunique"),
                                            n_kicking_in=("kicking_in", "sum"),
                                            last_event=("file_date", "max"))
panel = panel.merge(sig, on=["cik", "fiscal_year"], how="left").fillna({"n_clean": 0, "n_kicking_in": 0})
```

The same pattern works on `mentions.csv.gz`, for example restricted to `phrase_group == "ol_any"`, or on the quarterly table using its `first_file_date_*` columns.

4. **A missing row means zero only if the company was filing.** The firm-quarter table has a row only where at least one phrase matched. `filer_presence_by_cik_quarter.csv.gz` lists every company-quarter with a 10-K, 10-Q or 8-K on EDGAR (486,623 rows). Use it to tell a quarter with no mention apart from a company that was not filing at all.
5. **Margin tests.** A 10-Q or 10-K statement that "margins rose on operating leverage" describes a period that has already ended. To test whether *more* expansion follows, compare margins for fiscal periods that end **after** `file_date` with those that end before it, not the period the filing reports on.
6. **Financials and SPACs.** The clean tables already drop them. If you use `mentions.csv.gz` directly, filter `is_financial == False`. For headline results, also drop rows with missing `sic` (202 of 43,048 rows).

---

## 5. Files

| file | what it is |
|---|---|
| `mentions.csv.gz` | 43,048 rows, one per (cik, accession, file_date, form, file name, phrase), deduplicated. Includes `display_name`, `sic`/`sic2`/`is_financial`, `items` (8-K item numbers), `doc_role` (`main` / `ex99` / `ex13_annual_report` / `other_exhibit`), `is_ex99`, `is_main_doc`, `is_earnings_8k` (8-K with Item 2.02), `is_amendment`, `phrase_group`, and `url` to the matched file. |
| `tone_mentions.csv.gz` | Same layout for the 17 supplementary direction phrases (7,584 rows). |
| `mentions_by_cik_quarter.csv.gz` | 28,631 company x calendar-quarter rows (quarter of `file_date`). Counts are **distinct filings** per group: `ol_any` (phrase 1), `ol_positive` (2), `ol_negative` (3 or 4), `incremental` (5), `absorption` (6). Also `net_tone` = positive minus negative; the location splits `ol_any_release` / `ol_any_8k_other` / `ol_any_10q` / `ol_any_10k`; `tone_pos_mod`, `tone_neg_mod` and `net_tone_broad` from the supplementary phrases; and `ol_clean`, `ol_kicking_in`, `ol_clean_negative`. It carries `first_file_date_*` columns for exact dating, plus `sic`, `sic2` and `is_financial`. |
| `clean_events.csv.gz` / `clean_negative_events.csv.gz` | The recommended events: one row per (cik, accession), with `file_date`, `event_channel`, `is_earnings_release`, `pos_phrase`, `pos_modifier`, `pos_cue` and `kicking_in`. |
| `filer_universe_by_year.csv`, `filer_universe_by_quarter.csv`, `filer_presence_by_cik_quarter.csv.gz` | Denominators from the EDGAR quarterly master index. These include SPACs, which inflate 2021-22. |
| `precision_sample*.md` / `.csv`, `precision_labels*.csv`, `precision_eval.csv` | The hand check: snippets, labels and scoring. |
| `descriptive_stats.md`, `stats/*.csv` | All descriptive tables. |
| `fetch_audit.csv`, `fetch_totals_check.csv` | Per-slice and per-phrase reconciliation of the search results. |
| `cache/` | Raw search JSON (`fts/`, 46 MB), fetched documents (`docs/`, 135 MB) and master indexes (`full-index/`, 219 MB). |

**Rerun** (from `Claude Space/`; everything is cached, so the runs make no network calls):

```
.venv/bin/python research/oplev/commentary/fetch_mentions.py --offline   # rebuilds all mention tables
.venv/bin/python research/oplev/commentary/fetch_universe.py             # filer denominators
.venv/bin/python research/oplev/commentary/precision_check.py [--sample random|tenk|validation]
.venv/bin/python research/oplev/commentary/describe.py
```

To extend the date range, change `END_DATE` in `fetch_mentions.py` and run it without `--offline`.

---

## 6. Search quirks and how they were handled

- **10,000-hit cap.** A single query returns at most 10,000 hits, and asking for results past that point returns HTTP 500. "Operating leverage" in 8-Ks has 18,985 hits in total, and the full-range query just reports "10,000 or more". We therefore queried each calendar quarter separately (1,608 slices; the largest held 527 hits). The code splits a slice further by month or day if it ever hits the cap. The capped series was reconciled against 17 separate yearly totals.
- **Paging bug.** Results come back sorted by relevance, 100 per page. When relevance scores tie, a page can repeat one hit and silently skip another. This happened in 5 of the 1,608 quarterly slices. The code detects it (unique hits fewer than the reported total), re-fetches the slice month by month and takes the union. All slices now reconcile exactly.
- **Rate limits.** We held requests to 7.5 per second. About 130 transient failures (HTTP 429 or 5xx responses, or timeouts) were retried with exponential backoff, and none failed permanently.
- **How exact phrases match.** Matching works on words, is case-insensitive and does not stem:
  - "incremental margin" and "incremental margins" are separate queries, and a document can match both;
  - hyphens split words, so "fixed-cost leverage" also matches "fixed cost leverage", and "fixed cost absorption" also matches "fixed-cost absorption".
- **What the form filter returns.** Searching a form returns its amendments too (8-K/A 275 rows, 10-K/A 184, 10-Q/A 96). They are flagged `is_amendment` and dropped from the clean events. No 10-KT transition reports came back.
- **PDF copies.** 468 phrase hits are PDF courtesy copies, and 405 of them duplicate an HTML hit in the same filing. Hit counts at the file level include these duplicates; every filing-level count (firm-quarter table, events) does not.
- **Missing or odd fields.**
  - `sics` is empty on 202 mention rows (0.5%).
  - `items` exists only for 8-Ks.
  - `period_ending` is the report period for 10-Q and 10-K, and the event date for 8-Ks.
  - 757 rows come from filings with several co-registrant CIKs; each CIK gets its own row.
  - Some earnings releases are filed under Item 7.01, 8.01 or only 9.01 rather than 2.02, so `is_earnings_8k` understates releases. Of the 18,657 "operating leverage" 8-K EX-99 files, 13,230 are in Item 2.02 filings. That is why the clean events keep every 8-K EX-99.
- **Coverage.** Every year from 2010 to 2026 has hits, with no gaps. Apple's and Microsoft's 10-K and 10-Q filings for 2023-2026 were all found, 15 of 15 each. The search covers only text that the SEC indexes; exhibits the SEC does not index, and earnings calls that were never filed, are invisible here.
- **Section detection.** A heuristic that labels "which Item a match sits in" was unreliable: it was fooled by cross-references such as "see Item 1A" and was wrong on 2 of 20 files. It is kept in the precision CSVs only. No row is filtered by section.
