# PARK memo (4b pass, rung NOT resolvable) — U56 WEEKLY BAND 0.08 AT GROSS 0.75, idea 921, 2026-09-22 cloud

1. **What it is.** The live RULES v2 band book with ONE dial moved: hysteresis band 0.03 -> 0.08;
   gross 0.75, weekly cadence and de-gross-to-cash all unchanged.
2. **Reached under rule 8** by IS_LEGS over this run's 72-book U56 weekly corpus (IS 2009–2016
   chose, 2017–2026 read exactly once); idea 2109 reached the identical cell the same day by
   IS_MINMARG over a different corpus.
3. **FULL (10 bps):** 13.16% / 1.1734 / −19.70%, halves 1.2655 / 1.1113.
4. **OOS 2017–2026 (10 bps):** 14.04% / 1.1769 / −19.70% vs SPY 15.29% / 0.875 / −33.72%.
5. **4b legs:** H1 1.2655 > 0.957, H2 1.1113 > 0.826, OOS 1.1769 > 0.875, MaxDD −19.70% inside
   the −20.23% cap, CAGR 13.16% above the 10.60% floor. PASS on FULL and on OOS.
6. **Cost headroom, measured the way this idea argues for:** five-leg closing price **62.9 bps**,
   window price 62.9 bps (they coincide — this book closes on L4_DD, a leg the window sees).
7. **4a FAILS** (MaxDD −19.70% against the live book's −12.05%, Sharpe 1.173 vs 1.201): 4b path
   only, per PROTOCOL rule 4's note that 4a kills every growth idea.
8. **WHY PARK AND NOT KEEP: the RUNG is chooser-dependent.** Three legal IS-only choosers pick
   three different rungs of the same ladder on the same tape, all clearing 4b OOS — IS_MINMARG
   0.08 (here and in 2109), idea 2101's 0.10, idea 2109's IS_LEGS 0.12. The **DD margin is only
   +0.53 pp**, so idea 914's clause (a margin must exceed the book's own rebalance-offset
   spread, ~3 pp on comparable books) is **not met on the DD leg**; the CAGR margin is +2.56 pp
   FULL / +3.34 pp OOS. **No new candidate is filed** — this is the band ladder the record has
   already recorded twice, re-reached from a third direction.
9. **Survivorship (rule 9):** U56 is a current-constituent list; the LEVELS are optimistic. Rule
   6: nothing in RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was modified.
10. **Exact RULES wording if a Sunday review ever promotes this rung:**
    *"Clause 2 (band): hold every name whose close is above its 200-day moving average by more
    than 8% (IN) and drop it when the close falls more than 8% below that average (OUT); between
    those lines keep the previous state, and treat a name with fewer than 200 closes as OUT.
    Hold each IN name at 0.75/N of NAV, N = instruments priced that day; weight released by an
    OUT name goes to cash and is never re-spread. Rebalance weekly."*
