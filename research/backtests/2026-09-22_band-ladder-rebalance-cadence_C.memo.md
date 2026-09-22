# KEEP-4b candidate memo — idea 2207 (lane C, 2026-09-22): the ladder core, now cadence-certified

1. **Cell.** U56, band 0.03, gross 1.00 — the live RULES v2 band with the exposure dial at full.
   Not a new book: 2119 published it weekly. What is new is that it is **cadence-invariant**.
2. **Cadence certificate.** It clears 4b (FULL and OOS) at **D, W, 2W and M**, at **10 and 25 bps**
   — 8 of 8 cadence x cost cells. It is the **only** cell of 25 to do so at both cost rungs.
3. **Numbers, W @10 bps.** FULL 11.53% / **1.2009** / −15.91% (halves 1.2282 / 1.1799);
   OOS 12.67% / **1.2760** / −15.91%. SPY 15.14% / 0.8851 / −33.72% (halves 0.9570 / 0.8264).
4. **Numbers, 2W @10 bps (the grid's argmax).** FULL 11.81% / **1.2141** / −15.99%
   (halves 1.2122 / 1.2184); OOS 13.10% / **1.3097** / −15.99%; turnover 2.01x/yr vs W's 2.35x.
5. **Margins at W @10 bps:** DD **+4.32 pp** under the −20.23% cap, CAGR **+0.93 pp** over the
   10.60% floor, both Sharpe halves clear. At 2W: DD +4.24 pp, CAGR +1.21 pp.
6. **Rule 8.** A legal IS-only chooser (IS Sharpe, IS Calmar, IS min-margin — all three agree)
   reaches this cell on U56 at both cost rungs, picking the **M** cadence: OOS 12.82% / 1.2252 /
   −18.81%, 4b OOS PASS. The zero-parameter MAXGROSS_W reaches the W cadence: 12.67% / 1.2760 /
   −15.91%, also PASS, with 2.9 pp less drawdown — **the fitting is worth −0.0075 OOS Sharpe.**
7. **Path 4a: FAILS.** MaxDD −15.91% against the live book's −12.05%, so 0 of 24 rule-8 picks
   clear 4a. This is a 4b-only candidate: more return and more drawdown than the live book.
8. **Where it does NOT hold.** On B136 the same cell passes 4b at only 2 of 8 cadence x cost cells
   (W and 2W @10 bps, CAGR margin +0.04 / +0.21 pp) and fails at D and M. Any adoption is a
   **U56 claim**, and the B136 weekly verdicts on this ladder are cadence artefacts.
9. **Exact RULES wording, if a Sunday review adopts it** (rule 6 — not adopted here):
   *"Hold every priced universe name whose close is above its 200-day moving average x 1.03,
   dropping it when the close falls below that average x 0.97 and holding the prior state in
   between, at 1.00/N of NAV where N is the number of names priced that day; weight gated out of
   the band is held as CASH and never re-spread. Rebalance on the last trading day of every second
   week, execute at the next close, long only, no leverage."* (Cadence W is the conservative
   alternative and passes identically; both are certified.)
10. **Caveats.** Survivorship: U56 is a current-constituent list, so 11.5–13.1% CAGR is optimistic
    and the −15.9% drawdown is flattering. The candidate's whole edge over the live book is the
    gross dial (0.75 → 1.00), which 2211 showed needs no in-sample data at all; and its CAGR
    margin over the 4b floor is under 1.3 pp, inside the range earlier runs found unresolvable at
    95% (2042 / 2090). **Recorded, not recommended for capital on this run's evidence alone.**
