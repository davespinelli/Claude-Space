# Memo — the single 4b pass in idea 1172's grid (U56, N=10, H=21, W, 10 bps). PARK, do not enact.

1. **The cell.** U56 panel, CAND20 composite (21/252, 0/126, 0/63), eligibility 200d MA and
   max_vol 0.60, **top 10 slots, min hold 21 trading days**, equal weight at **gross 0.75**, cash
   sleeve, weekly rebalance, next-day execution, 10 bps.
2. **KEEP path: 4b.** Full sample **16.51% CAGR / 1.0878 Sharpe / −20.12% MaxDD**, halves
   **1.2067 / 0.9948**, turnover 7.74x/yr.
3. **Out of sample (rule 8, chosen on 2009–2016 by the IS-drawdown chooser, 2017–2026 read once):**
   **16.89% / 1.0574 / −20.12%** vs **SPY OOS 15.15% / 0.8684 / −33.72%**. All five 4b legs pass
   full-sample and all three OOS legs pass.
4. **4a: FAILS** (A_DD — RULES v2 draws down −12.05%, this book −20.12%).
5. **Exact RULES wording if it were ever enacted:** *"Each Friday close, rank every U56 name
   trading above its 200-day moving average with 20-day realised vol below 0.60 by the mean of its
   percentile ranks on 21→252d, 0→126d and 0→63d total return. Hold the top 10 at 7.5% of NAV
   each; a name once bought is held at least 21 trading days regardless of rank; the remainder of
   NAV is cash. Execute at the next day's close."*
6. **Why PARK and not KEEP — the binding leg is undecidable.** The 4b drawdown cap is 60% of SPY's
   33.72%, i.e. 20.23%. This book's **−20.12% clears it by 0.112 pp.** Idea 1083 measured the 90%
   width of a quantity of this kind on this tape at **4.1–7.2 pp**. The pass is inside its own
   measurement noise by a factor of roughly forty.
7. **It sits on this run's own boundary.** n=10 is the right-hand end of idea 1172's extended
   ladder, and this run's whole finding is that an extremum at a ladder end is a property of the
   ladder. Enacting a boundary cell on the strength of a run that exists to warn against boundary
   cells would be incoherent.
8. **Survivorship.** U56 is a current-constituent list; the CAGR, the Sharpe and therefore all
   five 4b legs are upper bounds, and the DD leg's 0.112 pp margin does not survive any plausible
   correction for it.
9. **What would settle it.** Re-price this cell against a point-in-time U56 membership, and walk
   n over {8, 10, 12, 15} x H over {15, 21, 30} to establish whether the pass is a cell or a
   region. One cell clearing by 0.112 pp is not a region.
10. **Recommendation: PARK.** No change to RULES.md, scan.py, bot.py or baseline.py. The idea's
    own verdict is KILL (outcome B, still truncated); this cell is an incidental by-product of the
    control end of its ladder and is recorded so a future run can find it, not so it can be traded.
