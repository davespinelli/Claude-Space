# Memo — idea 1174 (lane C, 2026-09-17): U56 / N=20 / MIN HOLD H=26. RECOMMENDATION: **PARK.**

1. **The book.** U56 (research/universe.json), weekly, gross 0.75, 10 bps, next-day execution.
   CAND20 composite (21/252, 0/126, 0/63 rank-averaged, halved when below the 200d MA), eligible
   only above the 200d MA and below 60% annualised 20d vol; hold 20 slots, cap INF, equal weight
   `0.75 / n_held`; **a name once bought may not be dropped for 26 trading days.**
2. **Numbers.** Full 14.96% / Sharpe 1.1560 / MaxDD −19.95%, halves 1.178 / 1.148. OOS 2017–
   16.95% / 1.2192 / −19.95%. Turnover 5.68x/yr. Against U56 SPY 15.06% / 0.8814 / −33.72%
   (OOS 15.15% / 0.8684) and live RULES v2 8.60% / 1.1980 / −12.05% (OOS 9.42% / 1.2714).
3. **KEEP path.** **4b, full sample AND out of sample**: Sharpe beats SPY in both halves
   (1.178 > 0.960, 1.148 > 0.817) and OOS (1.2192 > 0.8684); MaxDD 19.95% ≤ 0.60 × 33.72% =
   20.23%; CAGR 14.96% ≥ 0.70 × 15.06% = 10.54%. **4a: FAILS** (0 of 288 cells clear 4a).
4. **Exact RULES wording if it were ever enacted** (it should not be, see 6): *"Selection: rank
   every eligible name by the CAND20 composite and hold the top 20 at 0.75/20 of NAV each.
   Minimum hold: a name bought at a rebalance may not be sold for 26 trading days, even if it
   leaves the top 20 or the eligibility gate; it is sold at the first weekly rebalance on or
   after its 26th trading day held. Gated-out weight goes to cash — do not re-spread."*
5. **Why it is interesting.** H=26 is a rung **the record has never measured** — it appears in
   zero of 242 committed H-axis units — and it carries **5 of this run's 17 4b passes**, as many
   as H=21. The whole H=26 column clears 4b at N = 12, 15, 20, 25 and 30.
6. **Why PARK and not KEEP. No IS-only chooser reaches it.** On 2009–2016 alone it ranks **105th
   of 144 U56 cells by IS Sharpe**; the rule-8 chooser allowed the full 16-rung ladder picks
   N=15 / H=90 instead and gives back 0.036 of OOS Sharpe against the coarse-ladder pick. The
   cell is selected with full-sample knowledge, which is precisely what PROTOCOL rule 8 exists
   to refuse.
7. **The finer ladder is not free.** Mean OOS Sharpe of the IS-Sharpe chooser: L3 1.0273,
   L7 1.0095, LFINE 0.9713 — **buying resolution on the hold axis costs 0.0559.**
8. **Runner-up, same verdict.** U56 / N=8 / H=83: 19.07% / 1.1158 / −20.17%, OOS 22.48% /
   1.1962 / −20.17%, turnover 3.67x/yr — the highest CAGR of the nine new cells, and 138th of
   144 on IS Sharpe. Worse on rule 8, not better.
9. **Survivorship (PROTOCOL rule 9).** U56 is a CURRENT-CONSTITUENT list; every level here is
   optimistic and the 4b pass is an UPPER bound. The MaxDD leg clears by 0.28 pp, inside that bias.
10. **Recommendation: PARK.** Re-test only if a chooser that does not see the future can be shown
    to reach an H=26-class rung — e.g. on a rolling IS window (filed as idea 1183). **NOTHING
    ENACTED**; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
