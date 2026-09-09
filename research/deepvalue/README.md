# Deep Value Desk — methodology

**Product:** individually researched stock ideas with the reasoning laid bare, tracked from publication. Research, not personalized advice: no position sizes, no "you should buy". Every note says what would prove it wrong.

## Philosophy (David's brief, Sep 4)
Edge cases have alpha. Look where big money can't or won't: small and mid caps ($100M–$5B), spin-offs, post-restructuring, index deletions, no analyst coverage, temporarily broken narratives, founder-led compounders that screen "expensive" on trailing numbers but cheap on unit economics. "Deep value" here means a large gap between price and a conservative estimate of intrinsic value; growth counts fully when it is real and funded by the business itself.

## Pipeline
1. **Screen** (`screen.py`, weekly, deterministic): SEC XBRL frames for every filer + prices. Value (FCF yield, EV/EBIT), quality (ROIC, net debt), growth (revenue yoy), capital allocation (share count change), plus falling-knife penalty. Output: 40 candidates in `CANDIDATES.md`.
2. **Edge-case overlay** (`edge_cases.py`, TODO): spin-offs (Form 10 filings), recent index deletions, post-emergence equities, insider cluster buying (Form 4), companies with zero analyst coverage (proxy: no estimates on yfinance), recent IPO busts (price < 50% of IPO within 24 months).
3. **Fetch at universe scale** (`fetch_all.py`, weekly `--full` / nightly `--incremental` via Actions): reads `universe_under2b.csv` (every non-financial operating company, $50M–$2B cap, revenue > $20M, ADV > $1M — written by `screen.py --universe-out`) and runs the fetchers below for all of them, globally rate-limited to 8 SEC req/s. State lives in `filings/MANIFEST.json`: newest accession per form type, so `--incremental` costs one submissions request per unchanged ticker instead of ~28. Alpha Vantage full transcripts are rationed 24/run down the ranked list (free tier is 25/day); everything else falls back to the SEC 8-K Item 2.02 press release.
4. **Offline distribution**: cloud agents can reach only github.com and PyPI, so Actions builds `filings_bundle.tar.gz` (`bundle.py`, excludes `raw/`) and publishes it to the rolling `filings-latest` release. Agents run `bash research/deepvalue/fetch_bundle.sh` to pull and unpack it. `filings/` and the tarball are gitignored; only `MANIFEST.json`, `universe_under2b.csv`, `candidates.csv` and `CANDIDATES.md` are committed.
5. **Fetch, per ticker** (`fetch_filings.py`, `fetch_transcript.py`): latest 10-K Items 1/1A/7, 10-Q MD&A, proxy comp+ownership, 6 months of 8-Ks with EX-99 exhibits, 12 months of Form 4s, earnings call transcript or prepared remarks. Plain text, LLM-ready, cached under `filings/TICKER/`.
6. **Triage** (`triage_pack.py` + `TRIAGE_PROMPT.md`, agent, cheap): a 25k–40k character pack per ticker (screen row, meta, Form 4 summary, latest earnings release, MD&A overview, Item 1, transcript) that an agent reads for ~10k tokens and scores 1–10 in `TRIAGE.md`, with the paragraph in `triage/notes/`. Work is claimed from `TRIAGE_QUEUE.md` via `triage_queue.py next N --lane X`. Scores of 8+ graduate to the deep dive.
7. **Deep dive** (agent, 1–3 per day): reads everything fetched and writes `notes/YYYY-MM-DD_TICKER.md` using `NOTE_TEMPLATE.md`. Verdict: PASS, WATCH, or IDEA with conviction 1–5. Only IDEAs go to `PICKS.md`.
8. **Track** (`track_picks.py`, daily via Actions): price since publication vs Russell 2000 (IWM) and SPY, for every IDEA and for PASSes too (so we learn from what we rejected).
9. **Review** (Sunday): what worked, what didn't, why; update the screen weights only with evidence.

## Honesty rules
- Cite the filing and page/section for every material claim. No claim without a source in the fetched documents.
- Valuation shows the assumptions; a note without a bear case is incomplete.
- Track everything published, including the losers, forever.
- Survivorship, small-cap liquidity, and the fact that backtested screens overstate live results are stated in each weekly summary.

## Screen v2: quality-growth (adopted Sep 8, 2026 after discussion with David)
The first 82 deep dives showed two things: the cheapest names on the value screen were cheap for a reason the filings revealed in ten minutes, and the genuinely mispriced ones were hidden behind GAAP artefacts (impairments, discontinued operations) that the screen misread. `screen_v2.py` therefore replaces the value composite as the reading queue:

- **Growth is a gate.** Revenue OR normalised operating profit must be up in the last fiscal year and not down in the latest quarter year over year. Growth bought with share issuance (>15% share growth) does not count.
- **Profit is normalised.** GAAP operating income + reported impairments, taxed at 25%. Primary valuation metric: EV / normalised after-tax operating profit (EV/NOPAT), ceiling 20x.
- **Debt is a gate.** Net debt / normalised EBITDA above 4x is excluded, 3–4x penalised; net cash passes. Untagged debt: total liabilities minus cash is the upper bound and can only exclude, never earn a "net cash" label. Profit growth only counts if revenue is not falling more than 10%.
- **Financials are in.** Banks, brokers, insurers, holdcos: P/E, P/TBV, ROTE, tangible BVPS growth (gates: growing, P/E ≤ 12 or P/TBV ≤ 1.2, equity ≥ 5% of assets; profit above 40% of equity or P/E under 4 is flagged as a likely one-off). REITs and real-estate operators: P/FFO ≤ 15, FFO growing, total liabilities ≤ 80% of assets (this excludes most mortgage REITs by design). Industrial metrics are never applied to them.
- **Score among qualifiers** = 0.45 cheapness (EV/NOPAT) + 0.25 growth + 0.15 FCF yield + 0.15 normalised ROIC, −0.10 leverage band, +0.05 GAAP-artefact flag, −0.05 untagged debt.
- Outputs: `QUALITY.md` (ranked industrials + GAAP-artefact watchlist + exclusion reasons), `FINANCIALS.md`, `universe_v2.csv` (every row with an `exclude_reason`). `universe_under2b.csv` is rewritten in v2 rank order with the legacy columns so the fetchers keep working.
- Deep-dive lanes (cloud hourly, local 3x/day) read QUALITY.md / FINANCIALS.md in rank order; every note now opens with a six-line **Desk stats** block: revenue trend, normalised after-tax profit with each adjustment named, EV / normalised after-tax profit, leverage (or P/E, P/TBV, ROTE for financials), growth sustainability, and what the screen got wrong.
- The value triage (`TRIAGE.md`, 489 rows) is retained as history and as the fallback queue; the triage routines are off.
