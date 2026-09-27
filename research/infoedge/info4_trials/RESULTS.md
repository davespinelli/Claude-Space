# INFO-4. Quiet clinical-trial registry changes: results

*Generated 2026-09-26 by `research/infoedge/info4_trials/write_results.py`. Pre-registration, feasibility notes and every deviation: `PREREG.md` in this folder (see the process note at the end about a pilot run). Every number below is in `results.json`.*

## The short answer

**Feasible: yes.** ClinicalTrials.gov keeps a dated copy of every version of every record, and it can be downloaded without an account. 8,922 trial histories were pulled (all but 0 of the 8,141 trials whose sponsor has stock prices).

**Primary test: No.** After a quiet registry change (completion date pushed back 6+ months, enrollment target cut 25%+, or trial suspended/terminated/withdrawn, with no 8-K), the sponsor's stock did -0.33% versus similar-size health-care peers over the next 20 trading days (t = -0.47; first half -0.43%, second half -0.23%; 2,062 events). That does not clear the bar (t <= -2.5 and negative in both halves). The same companies on random dates in the same year did +0.02% against the same benchmark, so the event-minus-placebo difference is -0.12% (t = -0.15). Against IWM/SPY alone the events did -0.34% (t = -0.39).

| Line (days +1 to +20 after the posting date) | Mean | Clustered t | First half | Second half | Events |
|---|---|---|---|---|---|
| **Primary**: quiet changes, sponsor under $5B, vs size-and-industry peers | -0.33% | -0.47 | -0.43% | -0.23% | 2,062 |
| Event minus placebo (same stocks, random dates, same benchmark) | -0.12% | -0.15 | +0.76% | -1.00% | 2,021 |
| Placebo alone (same stocks, random dates) | +0.02% | 0.06 | -0.71% | +0.76% | 2,021 |
| vs IWM (under $2B) / SPY only | -0.34% | -0.39 | -0.33% | -0.34% | 2,062 |
| Event minus placebo, both vs IWM/SPY | -0.34% | -0.33 | +0.32% | -0.99% | 2,021 |
| vs XBI only | -0.22% | -0.32 | +0.33% | -0.77% | 2,062 |
| Secondary: Phase 2/3 trials only | -0.37% | -0.45 | -0.11% | -0.64% | 1,349 |
| Secondary: sponsor under $1B | -0.77% | -0.88 | -0.59% | -0.95% | 1,440 |

Missing companies (listed at the time, no Yahoo price today): about 732 quiet events (26% of the would-be sample). If every one of them lost 30%: -8.10% (t = -9.96); if every one gained 15%: +3.69% (t = 6.25).

Costs: shorting after each event would earn +0.13% per event after 0.2% costs (before borrow fees, which for small biotechs are often far larger).

## Feasibility: can the registry history be pulled?

- The public ClinicalTrials.gov API (v2) serves only the current version of each record; it has no history endpoint.
- The website's "History of Changes" tab reads two internal endpoints: one lists every version of a trial (number, date, overall status, which sections changed); the other returns the whole record as it stood at any version, including the date that version was **posted**. robots.txt explicitly allows crawlers on these endpoints.
- A request with no cookies gets "403 Forbidden" (0 of 10 succeeded in the logged check). Any public ClinicalTrials.gov response (for example the v2 API) sets the site's ordinary `ncbi_sid` session cookie, and with it the endpoints answer normally (10 of 10). The scripts keep cookies like any HTTP client, send the project User-Agent, and never impersonate a browser or solve a challenge.
- AACT (the Duke/FDA copy) needs an account for both database access and downloads, and holds snapshots rather than version histories. No account was created.
- Cost: about 11 requests per trial at up to 2.9 a second, roughly 12 hours for the whole set, with two network outages along the way.

## What was measured

1. Every industry-sponsored interventional trial updated since 2015: 91,130 current records (v2 API).
2. Lead-sponsor names mapped to SEC registrants (current and since-delisted names from EDGAR indices): 1,205 companies kept; 1,144 passed the loose under-$5B download screen; 763 have Yahoo prices.
3. Histories for 12,075 trials of those companies: all 8,141 trials of priced sponsors were attempted (8,141 downloaded, 0 still failing after one retry and excluded; list in `data/history_exclusions.csv`), and a random 20% of the 3,934 trials of sponsors with no price today (used only for the missing-company bounds, scaled up).
4. Changes between consecutive versions; public date = the version's posting date; one event per company per posting date; an event is quiet if no 8-K (6-K for foreign issuers) was filed from 5 trading days before the version date through the posting date.
5. Abnormal return = buy-and-hold return over trading days +1 to +20 minus the average buy-and-hold return of other sponsor companies in the same industry group and size band.

### Event counts

| | Delay 6+ months | Enrollment cut 25%+ | Suspended / terminated / withdrawn | Total |
|---|---|---|---|---|
| Trial-level changes posted 2015 to Aug 2026 | 4,728 | 270 | 1,466 | 6,464 |
| ... attributed to a listed sponsor at the time | 3,815 | 222 | 1,303 | 5,340 |
| Company-date events | 3,495 | 220 | 1,147 | 4,706 |
| ... with an 8-K/6-K in the window (dropped) | 1,369 | 79 | 554 | 1,944 |
| ... quiet and priced | 1,928 | 134 | 527 | 2,503 |
| ... quiet, priced, under $5B (**primary sample**) | 1,567 | 113 | 453 | 2,062 |

An event can carry more than one type, so the type columns can add up to more than the total.

Company-date events by price status: priced 4,304; missing (listed, no Yahoo price) 348; not listed at the time 54; too recent 0.

By type (primary sample):

| Type | Mean | Clustered t | First half | Second half | Events |
|---|---|---|---|---|---|
| Completion date pushed back 6+ months | -0.52% | -0.71 | -0.39% | -0.64% | 1,567 |
| Enrollment target cut 25%+ | +0.88% | 0.49 | +0.70% | +1.06% | 113 |
| Suspended / terminated / withdrawn | -0.90% | -0.62 | -1.33% | -0.47% | 453 |
| Status change only (no other change that day) | -0.10% | -0.06 | -0.64% | +0.45% | 410 |

### Posting lag

The date shown in the history is the submission/QC date; the version is posted later: median 2 days, 90th percentile 8, 95th 21 (84,443 versions posted since 2015). All events are dated at the posting date, so a model that dated them at the history date would be using information before it was public.

## Mapping precision

- 50 randomly drawn sponsor-to-SEC matches were checked by hand (`data/mapping_spotcheck.csv`): 50 of 50 correct (same company or its subsidiary, including renamed registrants). Matching rules: exact normalised name; looser "core" name and single-dictionary-word names only with a health-care SIC code.
- 50 randomly drawn primary events were also checked (registry sponsor name on that version vs the stock used): 50 of 50 correct (`data/event_spotcheck.csv`).
- Point in time: the sponsor is the one named in the version itself, and a change is only attributed to a stock if the registrant had used that name by 120 days after the posting date (so a private company that later reverse-merged into a listed shell is not attributed to the shell).

## How much to trust it

| Robustness line | Mean | Clustered t | First half | Second half | Events |
|---|---|---|---|---|---|
| Literal 8-K window (5 days before the version date only) | -0.70% | -1.05 | -1.15% | -0.25% | 2,384 |
| Daily-rebalanced peer benchmark | -1.01% | -1.51 | -0.90% | -1.13% | 2,062 |
| Raw return, no benchmark | +0.36% | 0.34 | +0.13% | +0.59% | 2,062 |
| Excluding foreign issuers | +0.16% | 0.22 | -0.10% | +0.42% | 1,886 |
| Including events with an 8-K in the window | -0.69% | -1.32 | -1.14% | -0.24% | 3,490 |
| Only events with an 8-K in the window | -1.22% | -1.70 | -2.27% | -0.17% | 1,428 |
| Event minus placebo, XBI benchmark | -0.33% | -0.40 | +0.38% | -1.03% | 2,021 |

By year (primary):

| Year | Events | Mean abnormal return |
|---|---|---|
| 2015 | 74 | -1.48% |
| 2016 | 105 | +0.53% |
| 2017 | 89 | +0.81% |
| 2018 | 117 | -1.47% |
| 2019 | 160 | +1.51% |
| 2020 | 156 | -1.73% |
| 2021 | 216 | -2.56% |
| 2022 | 244 | +0.26% |
| 2023 | 273 | +1.11% |
| 2024 | 235 | -1.78% |
| 2025 | 249 | +0.23% |
| 2026 | 144 | +0.39% |

## Caveats

- **Survivor-built prices and peers.** Yahoo only has symbols that still trade. About 26% of the would-be sample belongs to companies that have since been acquired or delisted; the -30%/+15% bounds show how much that could move the answer. The peer benchmark is built from the same survivors, which is why the placebo line matters: it measures how the same stocks do on ordinary dates against that benchmark.
- **Partial download for price-less sponsors.** Only a random 20% of their trials were pulled, so their count in the missing-company bounds is an estimate.
- **Universe chosen by today's sponsor name.** A trial whose current sponsor is a large company (for example after an acquisition) was not downloaded, even if a small listed company sponsored it earlier.
- **8-K screen is coarse.** Any 8-K counts as disclosure, whatever it says; a trial change announced in a press release without an 8-K, or in a 10-Q, still counts as quiet.
- **Short-side frictions.** The expected trade is a short in small biotechs; borrow costs and availability are not modelled beyond the 0.2% per event.
- **Size figures** combine XBRL share counts with Yahoo prices and a hand-checked ADS rule for foreign issuers; errors mostly affect which size band an event falls in, not the return.

## Process note (read before relying on the pre-registration)

- On 2026-09-26 at 07:45 a pipeline test ran the full event study on the partial download that existed then (155 primary events). It wrote returns to results.json, but the agent sent the output to /dev/null and read only the event and peer counts. At 07:57 PREREG deviation 10 (download order: priced sponsors first) was edited. That edit changes which trials were downloaded first, not how any event or return is defined.
- At 19:18, after the full download, prepare_companies.py was corrected to price each company on its main US listing rather than an OTC line where both exist (for example ResMed RMD rather than RSMDF, Abivax ABVX rather than AAVXF). ADS ratios for those 15 companies were recomputed. This is a data correction and is not in PREREG.md.
- Before this final run, the coordinator looked at the 07:45 pilot summary (primary +2.1%, t = 1.11, No). Nothing in PREREG.md or the return code was changed after that.
- The final run below uses every history downloaded, including one retry pass for failed downloads. Trials that still failed are listed in data/history_exclusions.csv.

## Files

- `PREREG.md` spec, feasibility and deviations; `results.json` every number; `data/event_returns.csv` event-level returns; `data/placebo.csv`; `data/trial_changes.csv`, `data/changes_mapped.csv`; `data/sponsor_map*.csv`, `data/mapping_spotcheck.csv`; `data/excluded_no_price.csv` (companies with no Yahoo price); `data/history_exclusions.csv` (trials whose history could not be downloaded).
- Pipeline: `pull_universe.py` -> `build_sec_names.py` -> `map_sponsors.py` -> `i4_subs.py`, `i4_facts.py`, `i4_px.py` -> `build_universe.py` -> `prepare_companies.py` -> `i4_ads.py` -> `size_screen.py` -> `i4_hist.py` (resumable, sharded) and `i4_retry.py` -> `detect_changes.py` -> `build_events.py` -> `run_event_study.py` -> `write_results.py`.
