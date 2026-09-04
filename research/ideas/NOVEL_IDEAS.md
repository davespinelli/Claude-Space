# Novel strategy ideas for David's review (Sep 4, 2026)

Criteria: not a standard factor; exploits something an LLM-plus-EDGAR pipeline can do that a spreadsheet quant cannot, or a structural edge in small caps that big money cannot harvest. Each has: the edge hypothesis, why it may be unexploited, data we already have or can build, a test design, and an honest risk. Ratings: **Novelty** (1–5), **Testability now** (1–5), **My prior** that a real edge exists (low / medium / high).

## A. Filings-text signals (LLM-native; nobody scores these systematically for small caps)

### A1. Risk-factor churn
Hypothesis: the *change* in Item 1A between consecutive 10-Ks (new risks added, old ones deleted, wording hardened from "may" to "has") predicts negative drift; companies whose risk section shrinks or softens outperform. Big shops do this for large caps with NLP; nobody reads 485 small-cap 10-Ks. We now have the text for all of them and can diff year over year.
Test: diff Item 1A year over year, score added/removed/hardened sentences with an LLM rubric, long bottom-decile churn / short top-decile, hold 12 months. Novelty 4 · Testability 4 (we need prior-year 10-Ks, one more fetch) · Prior: medium.

### A2. "Quiet 8-K" drift
Hypothesis: 8-K Items 1.02 (termination of material agreement), 2.04 (triggering events), 3.01 (delisting notice), 4.01 (auditor change), 5.02 (officer departure "to pursue other opportunities") in micro-caps are under-read for days. An agent reads every 8-K within hours of filing and classifies severity; the position is taken before the market fully reacts. Reverse for good-news items (1.01 new contract, 8.01 buyback).
Test: event study on the last 5 years of 8-K items for the 485 universe, abnormal returns days 1–20 by item and LLM severity score. Novelty 3 · Testability 5 (EDGAR daily index) · Prior: medium for the bad-news side (drift after bad news is well documented), low for good news.

### A3. Guidance-language drift across calls
Hypothesis: a systematic drop in management's confidence language between consecutive earnings releases/calls (hedging words, fewer numbers, more "macro") precedes guidance cuts by a quarter. Test with press releases (we have 100% coverage) and transcripts as they accumulate. Novelty 3 · Testability 4 · Prior: medium.

### A4. Auditor and comment-letter signals
Hypothesis: SEC comment letters (CORRESP/UPLOAD filings on EDGAR) about revenue recognition or going concern, and auditor changes to a smaller firm, precede restatements and drawdowns; conversely, companies that resolve comment letters quickly outperform. Novelty 4 · Testability 4 (public on EDGAR) · Prior: medium.

### A5. Proxy pay-for-performance mismatch
Hypothesis: small caps where CEO pay rises while TSR falls (from DEF 14A pay-versus-performance tables, mandatory since 2023) underperform; those with pay cut after bad years outperform. Novelty 3 · Testability 4 · Prior: low-medium.

## B. Structural edges where big money cannot play

### B1. Index-deletion liquidity vacuum
Hypothesis: when a stock is deleted from the Russell 2000 (June reconstitution) or S&P 600, forced selling by index funds pushes it below fair value; the reversal in the following 3–6 months is larger for names with no analyst coverage and low float. Documented for additions; the deletion side in micro-caps is under-researched. Novelty 3 · Testability 3 (need reconstitution lists; FTSE Russell publishes preliminary lists each June) · Prior: medium-high.

### B2. Odd-lot tender offers and Dutch auctions
Hypothesis: small-cap self-tenders at a premium with odd-lot priority are near-riskless for small accounts; institutions cannot scale them. Not a "strategy" for $100k in size but a steady income stream: catalog every SC TO-I filing, compute the premium and odd-lot terms. Novelty 2 · Testability 5 · Prior: high but capacity-limited (a few hundred dollars per event).

### B3. Post-spin-off parent vs. child divergence
Hypothesis: the classic edge is "buy the spin-off"; the less-studied edge is the *parent* after a spin-off of a low-margin unit (margin re-rating) versus the child when the child is loaded with debt. Test both legs from our Form 10 calendar. Novelty 3 · Testability 4 (idea 36 builds the data) · Prior: medium.

### B4. Post-reorganization equities
Hypothesis: equities emerging from Chapter 11 (fresh-start accounting, no analyst coverage, holders are former creditors who want out) underperform for 3 months then outperform for 2 years. Data: 8-K Item 1.03 and 3.03, fresh-start language in 10-K. Novelty 3 · Testability 3 · Prior: medium (documented in academic work but rarely implemented).

## C. Cross-asset and options signals in small caps

### C1. Credit-equity divergence
Hypothesis: for small caps with public bonds or loans, when bond prices fall while equity is flat (or vice versa), the bond market is usually right. Data problem: bond prices (TRACE) are not free in bulk; a partial proxy is the price of the company's converts (often listed) and the equity. Novelty 4 · Testability 2 · Prior: medium-high but data-gated.

### C2. Skew as an insider-information proxy
Hypothesis: unusual put skew or call-OI build in small caps ahead of 8-K events indicates informed trading; combine with Form 4 blackout calendars. Requires the options cache we started today (idea 35) to accumulate; no free history. Novelty 4 · Testability 2 now, 4 in six months · Prior: medium.

### C3. IV-RV spread harvesting around small-cap earnings
Hypothesis: small-cap options are systematically overpriced into earnings because market makers cannot hedge illiquid names; selling straddles with strict sizing collects the premium. Real, but it is a short-volatility strategy with fat tails; not for the $100k without hard limits. Novelty 2 · Testability 3 · Prior: high on average, ruinous on tails.

## D. Using our own Deep Value Desk as a signal

### D1. Research-verdict long/short
Hypothesis: our IDEA/WATCH/PASS verdicts contain information. A market-neutral basket of long IDEAs and short PASSes (or short the names where the screen said "net cash" but the filings showed leverage) isolates the value of *reading*. This is the cleanest way to prove whether the desk is worth $100k. Novelty 5 (nobody else has this dataset) · Testability grows daily · Prior: unknown, which is exactly why it must be tracked.

### D2. Screen-vs-filing discrepancy short
Hypothesis: companies that screen cheap only because XBRL tags are wrong or one-off items inflate earnings (the RIGL, MPAA, UPBD cases) attract quant value money that later exits; they underperform other "cheap" names. We can flag these mechanically now (eq_flag, debt_note). Novelty 4 · Testability 4 · Prior: medium.

## E. Attention and coverage

### E1. Zero-coverage plus rising insider ownership
Hypothesis: small caps with no sell-side coverage, rising insider ownership (from proxy tables year over year), and positive FCF outperform when coverage initiates or a strategic buyer appears. Data: DEF 14A ownership tables (we fetch them), coverage proxy from yfinance analyst counts. Novelty 3 · Testability 4 · Prior: medium-high.

### E2. 13F crowding unwind
Hypothesis: small caps where a few concentrated holders (from 13F/13D) own most of the float suffer when one exits; identify "one-seller-from-a-cliff" names to avoid or short, and "nobody-owns-it" names to own. Data: 13F is free on EDGAR quarterly. Novelty 3 · Testability 3 · Prior: medium.

## My ranking for the next two weeks (highest expected value per compute)
1. **D1** — start today; it costs nothing and it is the proof of the desk.
2. **A2** quiet-8-K drift — data is free and daily; if it works it is also an alert system for the desk.
3. **B1** index-deletion reversal — the June 2026 reconstitution just happened; deletions are 2 months old, prime window.
4. **A1** risk-factor churn — needs one more fetch (prior-year 10-K) then it is pure LLM work, which is our comparative advantage.
5. **E1** zero-coverage + insider ownership — easy overlay on the triage queue.
Park until data exists: C1, C2. Capacity-limited but free money for a small account: B2.
