# Memo — idea 84, for the Sunday review (2026-09-04, lane B)

1. **KILL idea 83's two-branch lever rule.** The CAGR floor binds 6 of 8 standing-candidate
   cells, so the branch assignment is near-degenerate; and the Sharpe bars are g-invariant in
   all 24 (cell, cost) triples (max Sharpe spread 0.0061 over g = 0.40→1.00), so "DD-bound →
   cut g" and "CAGR-bound → raise g" are one lever in two directions, not two branches.
2. **Idea 83's CAGR branch names the wrong instrument.** The entry-only budget is
   CAGR-neutral by construction (it saves cost but raises cash): d_CAGR +0.01..+0.20pp across
   every CAGR-bound cell, against the 0.26pp gap it was asked to close. Gross moves it +3.7pp.
3. **The third branch idea 83 lacks:** on the one Sharpe-bound cell no lever converts it —
   best improving move +0.0027 over 20 arms. Only a book change fixes a Sharpe-bound book.
4. **RULES clause to adopt (replaces "quote one instrument"):**
   *"Gross exposure g is a policy dial with no Sharpe content. 4b's drawdown cap and CAGR
   floor both sit on that dial and therefore define an interval [g_min, g_max] for any book;
   set g inside the interval that holds on BOTH universes at 10 AND 25 bps, and if the
   interval is empty or a Sharpe bar (H1, H2, OOS) fails, change the book — no exposure or
   turnover setting can repair it."*
5. **KEEP-candidate (4b), by-product:** idea 57's `ew-band3` at **g = 0.85** — the project's
   first arm to pass 4b full AND out-of-sample on BOTH large-cap universes at 5, 10 and 25 bps.
   u56 12.8%/1.136/-17.1% (halves 1.113/1.160, OOS 14.4%/1.234); broad 12.6%/1.064/-18.9%
   (halves 1.163/0.971, OOS 12.7%/1.073); 5.5x/5.8x turnover. It also passes 4a on broad.
6. **This answers idea 58.** The published g = 0.75 version dies at 25 bps on the CAGR floor
   (10.5%/10.3% vs a 10.68% bar); cost eats CAGR, and gross is the CAGR lever, so raising g
   repairs exactly the bar that breaks. The band is not what needed fixing.
7. **g = 0.85 is rule-8 selected, not fitted:** the 4b-aware IS rule (2009–2016 only) picks
   g = 0.85 on both universes. Pure argmax-IS-Sharpe picks g = 1.00 on u56, which breaks the
   DD cap on broad. Cross-universe interval: [0.75,0.90] at 5/10 bps, [0.80,0.90] at 25.
8. **Exact RULES wording if adopted:** *"Hold every instrument whose price is above its
   200-day moving average by more than 3%, and drop it when it falls more than 3% below
   (hysteresis band; state persists between crossings), excluding any name with vol20 ≥ 0.60.
   Equal weight, 85% gross, weekly rebalance."* No ranking, no vol scaler, no score.
9. **Do not adopt yet.** Survivorship is one-directional on both lists; the broad 25 bps
   window is only 0.10 wide; 2020 and 2022 are the only real stress tests; and the Sep 3 memo's
   ≥8 weeks of live tracking still stands before any real capital.
10. **Recommended Sunday action:** adopt clause 4 into PROTOCOL/RULES as the exposure rule
    (it costs nothing and kills a whole class of future lever tuning), and carry
    `ew-band3 @ g=0.85` as the single standing 4b candidate, retiring ideas 2, 46 and 72's
    arms — each fails cross-universe 4b at 25 bps and C2 fails on broad at 10 bps.
