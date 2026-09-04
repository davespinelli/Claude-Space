# Memo — idea 40's only KEEP: two 4a passes I recommend AGAINST adopting (lane B, 2026-09-04)

1. Two of 21 grid points pass PROTOCOL **KEEP path 4a**: the no-scaler book at n=8 / 75% gross with a
   book-level drawdown control at **D=6%** (7.1% / Sharpe 0.722 / MaxDD -12.1%, halves 0.690/0.753)
   and at **D=8%** (7.4% / 0.700 / -13.8%, halves 0.713/0.694).
2. Both clear 4a legitimately: Sharpe above RULES v1 (0.641/0.692) in both halves, MaxDD no worse
   than v1's -13.8%. Margins are thin (0.05 / 0.06 of Sharpe).
3. Both fail **every** 4b test: CAGR 7.1%/7.4% against a 10.7% floor, H1 0.690/0.713 and H2
   0.753/0.694 against SPY's 0.957/0.837, OOS Sharpe 0.767/0.758 against SPY's 0.884.
4. Mechanism disqualifies them anyway: the rule holds the book at half exposure on **75% and 66% of
   all days**. It is a permanent de-leveraging that happens to flatter Sharpe, not a tail control.
5. The same base book with **no overlay** (n=8, 75%) returns 13.8% / 0.932 / -17.9%. The overlay
   buys 5.8pp of drawdown for 6.7pp of CAGR and 0.21 of Sharpe — a bad trade at any size.
6. Adopting either would repeat exactly the failure 4b was written on Sep 4 to prevent: passing
   because the live book is weak, not because the rule is good.
7. **Recommendation to the Sunday review: do not adopt. Record as a documented 4a pass, rejected.**
8. If the review disagrees and wants it, the exact RULES wording would be: *"Each day, compute the
   book's cumulative return peak since inception. If the book's drawdown from that peak exceeds 6%,
   halve every target position weight (gross 75% → 37.5%) from the next close, and hold the halved
   book until the book's equity makes a new all-time high, at which point restore full weights from
   the next close. Selection, the 200d and vol20<0.60 filters, top-8 equal weight and the Friday
   rebalance are unchanged; the /sqrt(vol20) term is removed from the composite."*
9. The rest of idea 40 is a KILL: no point passes 4b, and QUEUE idea 22 is answered negatively.
10. The one thing worth carrying to the review is the **breadth gate**, not this: 9 points, ~1pp of
    CAGR for ~4pp of drawdown, walk-forward pick n=3/B=30% at OOS 23.8% / 1.081 / -20.6% vs SPY
    15.5% / 0.884 / -33.7% — a PARK that misses 4b's drawdown cap by 0.4pp. Do not tune it to fit.
