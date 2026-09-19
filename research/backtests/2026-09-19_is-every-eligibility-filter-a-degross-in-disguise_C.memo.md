# PARK memo — idea 1617 (lane C, 2026-09-19): the MAXVOL 0.60 book that clears 4b FULL *and* OOS

**Status: PARK, not KEEP.** The book below clears every 4b leg on the full sample AND out of
sample on TWO panels at 0/10/25/50 bps, but **no legal IS-only chooser reaches it** (4 choosers x
3 panels = 12 picks, 0 land on it; rule 8 therefore says PARK). It is recorded here so the cell is
auditable, not adopted. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are unmodified.

**Exact RULES wording, if it were ever adopted** (it replaces clauses 2-4 of RULES v2 only):
> 2. **Membership gate:** a name is IN on the decision day if its 20-day realised volatility,
>    annualised as `close.pct_change().rolling(20).std() * sqrt(252)`, is **below 0.60**. A name
>    with fewer than 20 closes, or with no price that day, is OUT. There is **no 200-day moving
>    average band, no volatility-scaled score and no momentum ranking.**
> 3. **Selection:** hold every IN name. No top-N cut, no ranking.
> 4. **Sizing:** each IN name is held at `0.75 / N` of current NAV, where `N` is the number of
>    universe names **priced** that day (not the number IN). Names that are OUT are not held and
>    their weight stays in cash — the book de-grosses; gross is never re-spread.
> Clauses 1, 5-8 of RULES v2 are unchanged (weekly rebalance, no intra-week trading, 10 bps).

**Numbers (U56, 2009-01..2026-09, weekly, t+1, 10 bps).** 11.52% / 1.1279 / −16.88%, halves
1.158 / 1.101; **OOS 2017-2026 12.04% / 1.1765 / −16.88%**. 4b bars: CAGR floor 10.59% ✓, DD cap
−20.23% ✓, SPY halves 0.957 / 0.825 ✓, SPY OOS 0.8738 ✓. Live RULES v2: 8.62% / 1.2011 / −12.05%
(it fails 4b on the CAGR floor alone). Turnover 1.39x/yr, realised mean gross 0.7199, 51.9 names.
B136 replicates (12.24% / 1.1291 / −18.70%, OOS 11.80% / 1.1058); SMALL fails every leg.

**Why it is only a PARK.** (a) Rule 8: C_SHARPE picks RANKCUT 0.75 (U56) / MAXVOL 0.45 (B136,
SMALL), C_MEMO picks BASE / MAXVOL 1.00 / BASE, C_LIVE and C_BASE choose nothing — 0 of 12 reach
m = 0.60, and choosing a filter on IS rows costs **−0.0831** of pooled OOS Sharpe versus choosing
none. (b) Its Sharpe is NOT an edge: against a constant de-gross of the unfiltered book matched on
the same REALISED mean gross (0.7199, matched to 1.4e-15), dSharpe is **+0.0089** at 10 bps and
**negative at 25 and 50**. Its whole 4b pass rests on **dMaxDD +4.81 pp** — the twin misses the DD
cap at −21.69% — so this is a drawdown claim, and idea 1511 measured the paired DD-contrast SE at
2.93 pp, i.e. 4.81 pp is under two SEs. (c) Survivorship: U56/B136 are current-constituent lists,
so the absolute CAGR is an upper bound and the 4b CAGR leg is the leg most exposed to it.
