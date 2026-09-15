# MEMO — U56 / MOM top-20% / MONTHLY / gross 0.50 (idea 885, cloud lane, 2026-09-15)

1. **What passed.** PROTOCOL path **4b** at the pre-declared cell (10 bps, next-day fills, monthly
   k=0): full **13.69% / 1.185 / −18.31%**, halves **1.305 / 1.120**, OOS 2017+ **15.07% / 1.176 /
   −18.31%**, against SPY **15.13% / 0.885 / −33.72%** (halves 0.959 / 0.824, OOS 15.27% / 0.874 /
   −33.72%) and RULES v2 live **8.64% / 1.208 / −11.90%** (OOS 9.49% / 1.286 / −11.90%). All five
   legs true: H1 +0.346, H2 +0.296, OOS +0.302, DD +1.92 pp under the −20.23% cap, CAGR +3.10 pp
   over the 10.59% floor. Path **4a FAILS** (MaxDD −18.31% vs the live book's −11.90%), as it does
   for all 720 books here at this gross.
2. **Exact RULES wording, were it ever adopted** (it is **NOT** proposed for adoption):
   *"Universe: the 56 names of `research/universe.json`. Each trading day compute, for every name
   priced today and yesterday, MOM = close[t−21]/close[t−252] − 1. On the last trading day of each
   month, let n be the number of names priced that day and k = round(0.20 × n); hold the k names
   with the highest MOM at 0.50/k of NAV each (11 names at 4.55% on a full panel), and the
   remaining 50% of NAV in CASH. No eligibility filter, no 200-day gate, no volatility scaler.
   Fills next day, 10 bps per unit turnover."*
3. **Turnover / gross:** 2.78× NAV per year; realised gross 0.503 (target 0.50).
4. **Calendar-offset robustness — the check ideas 805/806 ask for, and this book passes it.**
   Over all **21 month-end offsets** the book passes 4b at **21 of 21**; CAGR spans 12.35–13.79%,
   Sharpe 1.084–1.200 (spread 0.116), MaxDD −18.48%…−16.38% (spread 2.10 pp). It is not a date.
5. **Cost-rung robustness:** 4b passes at **0, 10 and 25 bps** (25 bps: 13.21% / 1.148 / −18.33%).
6. **Rule 8 is satisfied with an IS-only selector.** Choosing (gross, q) on 2009–2016 alone by
   "max IS CAGR subject to IS MaxDD ≤ 60% of SPY's IS MaxDD" picks g=0.50, q=0.20 with no sight of
   2017+, and the pick passes 4b out of sample. **The selector matters more than the book**: the
   rival IS selector (argmax IS Sharpe) walks to gross 1.00 in 24 of 24 cells and lands on a 4b
   pass **0 times**, because the DD leg fails there. 7 of 72 IS-only selections land on a 4b pass,
   all 7 from the DD-capped selector.
7. **Why this memo does NOT propose a RULES change.** Idea 879 already established that gross is
   not an edge dial — it slides one scalar between 4b's CAGR floor and its DD cap — and this run
   reproduces that from the other side: across the whole grid the 4b passes sit **only** at gross
   0.375–0.50 (33 of 720 books), the CAGR leg rejects everything below and the DD leg everything
   above. A pass found by walking that dial is the dial working, not an edge appearing.
8. **Base rate.** The record's own unselected 4b rate on U56/B136 arms is 12–18% (idea 883's 2,304
   arms). This run's IS-selected rate is 7/72 = 9.7% — **at or below** the base rate, so nothing
   here is evidence against chance at the level of a single book.
9. **It does not out-earn or out-Sharpe what it is measured against.** OOS CAGR 15.07% vs SPY's
   15.27%; OOS Sharpe 1.176 vs the live book's 1.286. It clears 4b because the floor is 70% of SPY
   and the cap is 60% of SPY's drawdown, not because it beats either comparand outright.
10. **Caveats for any live decision.** SURVIVORSHIP: `universe.json` is the CURRENT constituent
    list, so CAGR is biased upward and both 4b level bars are easier here than point-in-time.
    2020 and 2022 are the only real stress episodes in the window. The weekly and quarterly
    siblings of this book pass only 4/5 and 46/63 of their offsets. Rule 6: any rules change is a
    Sunday-review decision and this memo is not a proposal.
