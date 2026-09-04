# Memo — idea 67: retire the QQQ core, keep `ew-band3` + 0–25% SPY core (2026-09-04, lane B)

1. Idea 63's `b = 0.25 QQQ` core is **not** walk-forward reproducible: 0 of 24 IS selection
   points (2 objectives × 6 drawdown caps × 2 universes) pick it; 10 of 12 on broad pick
   `b = 0.50 QQQ`, which fails the OOS drawdown cap by 1.8pp (−22.0% vs −20.2%).
2. Cause: IS Sharpe ranks OOS CAGR at +0.84/+0.91 but OOS MaxDD at **−0.19/−0.45**, and IS
   MaxDD ranks OOS MaxDD at only +0.57/+0.20. No IS drawdown cap can fix this.
3. With a **SPY** core the same grid passes OOS 4b at 10 of 12 points on broad and 10 of 12
   on universe.json. The QQQ core, not the sleeve fraction, is what breaks rule 8.
4. Surviving arm, both universes, 10 bps, weekly, t+1: `ew-band3` + 25% SPY core —
   **u.json 11.4% / 1.106 / −16.5% (H1 1.11, H2 1.11); broad 11.3% / 1.040 / −17.7%
   (H1 1.13, H2 0.96)**. Passes 4b on both; passes 4a on broad, fails 4a on u.json (DD).
5. The b = 0.00 end (idea 57's book, 11.3%/1.136/−15.1% and 11.1%/1.064/−16.8%) is what the
   broad walk-forward actually selects. b is a ~1pp CAGR / ~1pp drawdown dial, not the edge.
6. **Exact RULES wording, if adopted at a Sunday review:**
   > Each Friday close, hold every universe name whose price is above its 200-day moving
   > average by more than 3% (a name once held stays held until price falls more than 3%
   > below the 200-day average) and whose 20-day annualised volatility is below 60%,
   > equal-weighted, at 56.25% of book. Hold 18.75% of book in SPY. The remaining 25% stays
   > in cash. Execute at the next session's close.
7. That is gross 75% total: 0.75 × (1 − b) equal-weight sleeve + 0.75 × b SPY, with b = 0.25.
8. **Do not adopt the QQQ variant.** It scores better in-sample on every measure and is the
   only variant rule 8 rejects — the textbook signature of a hindsight instrument.
9. Two tuned parameters here (IS objective, IS drawdown cap); the book's own parameters
   (3% band, b) are idea 57's and idea 63's, not re-fitted in this run.
10. Survivorship: both universes are current constituents, so every level is an upper bound;
    b = 0 is the conservative choice if the sleeve is judged an unearned beta tilt.
