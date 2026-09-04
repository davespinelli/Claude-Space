# Deep Value Desk — methodology

**Product:** individually researched stock ideas with the reasoning laid bare, tracked from publication. Research, not personalized advice: no position sizes, no "you should buy". Every note says what would prove it wrong.

## Philosophy (David's brief, Sep 4)
Edge cases have alpha. Look where big money can't or won't: small and mid caps ($100M–$5B), spin-offs, post-restructuring, index deletions, no analyst coverage, temporarily broken narratives, founder-led compounders that screen "expensive" on trailing numbers but cheap on unit economics. "Deep value" here means a large gap between price and a conservative estimate of intrinsic value; growth counts fully when it is real and funded by the business itself.

## Pipeline
1. **Screen** (`screen.py`, weekly, deterministic): SEC XBRL frames for every filer + prices. Value (FCF yield, EV/EBIT), quality (ROIC, net debt), growth (revenue yoy), capital allocation (share count change), plus falling-knife penalty. Output: 40 candidates in `CANDIDATES.md`.
2. **Edge-case overlay** (`edge_cases.py`, TODO): spin-offs (Form 10 filings), recent index deletions, post-emergence equities, insider cluster buying (Form 4), companies with zero analyst coverage (proxy: no estimates on yfinance), recent IPO busts (price < 50% of IPO within 24 months).
3. **Fetch** (`fetch_filings.py`, `fetch_transcript.py`): latest 10-K Items 1/1A/7, 10-Q MD&A, proxy comp+ownership, 6 months of 8-Ks with EX-99 exhibits, 12 months of Form 4s, earnings call transcript or prepared remarks. Plain text, LLM-ready, cached under `filings/TICKER/`.
4. **Deep dive** (agent, 1–3 per day): reads everything fetched and writes `notes/YYYY-MM-DD_TICKER.md` using `NOTE_TEMPLATE.md`. Verdict: PASS, WATCH, or IDEA with conviction 1–5. Only IDEAs go to `PICKS.md`.
5. **Track** (`track_picks.py`, daily via Actions): price since publication vs Russell 2000 (IWM) and SPY, for every IDEA and for PASSes too (so we learn from what we rejected).
6. **Review** (Sunday): what worked, what didn't, why; update the screen weights only with evidence.

## Honesty rules
- Cite the filing and page/section for every material claim. No claim without a source in the fetched documents.
- Valuation shows the assumptions; a note without a bear case is incomplete.
- Track everything published, including the losers, forever.
- Survivorship, small-cap liquidity, and the fact that backtested screens overstate live results are stated in each weekly summary.
