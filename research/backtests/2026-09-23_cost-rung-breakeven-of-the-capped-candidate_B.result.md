# idea 2431 (lane B, run 47) — the capped candidate's COST BREAKEVEN. ANSWERED; no KEEP, one PARK.

1. **Question.** The record had killed every turnover device filed against the capped candidate's 3.51x/yr and
   asserted it "dies at 50 bps", but never published the breakeven. 808 rows: 2 panels x 2 books x 2 gross x a
   1-bp ladder 0..100. 13 of 13 gates. Cost is exactly linear (`engine.py:50`), so G1 verifies the whole ladder is
   bit-identical (max|d| 0.0e+00) to `engine.backtest(cost_bps=c)` at 10/25/50/100 — nothing here is interpolated.
2. **The premise was half wrong.** 4b passes **5 of 8 cells at 0, 10 AND 25 bps** and **1 of 8 at 50 bps**. The
   headline U56/CAP2/g0.75 book's exact 4b breakeven is **34 bps**, not 25. "Dies at 50" was right; "dies at 25" was not.
3. **Breakeven table (bps, last rung at which 4b holds).** U56/CAP2 g0.75 **34**, g1.00 **54**; U56/CAND g0.75 **49**,
   g1.00 never; B136/CAP2 g0.75 **33**, g1.00 never; B136/CAND g0.75 **35**, g1.00 never.
4. **The binding leg is the CAGR floor, not trading.** For the headline cell: `L_H1` 95, `L_H2` >100, `L_OOS` >100,
   `L_DD` >100, **`L_CAGR` 34**. Costs kill the book by dragging CAGR under 0.70 x SPY (15.23% -> floor 10.66%), while
   Sharpe still beats SPY in both halves and out of sample well past 90 bps. The other 3 cells fail on `L_DD` at 0 bps.
5. **The adoption bar (the deliverable).** Scaling turnover by `lam` at rung `c` is arithmetically the rung `lam*c`;
   G8 checks that against an independent lam-ladder (max|d| 0.75 bps < the 1.25 bps joint resolution). To clear **50 bps
   at current returns**: U56/CAP2 g0.75 needs **3.51x -> 2.42x (-31.0%)**, B136/CAP2 g0.75 **4.68x -> 3.13x (-33.0%)**,
   B136/CAND g0.75 **4.91x -> 3.48x (-29.0%)**, U56/CAND g0.75 **4.39x -> 4.33x (-1.5%)**. Live RULES v2 runs 1.77x / 2.01x.
6. **4a is structurally dead, not cost-killed.** 0 of 808 rows pass 4a — including at **0 bps**, and including the
   variant with the baseline pinned at 10 bps. No turnover device can rescue 4a; only 4b was ever in play.
7. **Rule 8.** gross fitted on <= 2016-12-31 only, 2017-2026 read once: **32 of 32 picks land on gross 0.75, 0 of 32 on
   gross 1.00**. Picks beat SPY's OOS Sharpe 32 of 32, the live baseline's 10 of 32; 24 of 32 pass full-sample 4b.
8. **PARK, not KEEP: U56/CAP2 at gross 1.00.** It is the only cell that clears 50 bps (breakeven 54 bps, lam* 1.095 —
   it could trade 9.5% MORE and still pass; 10 bps full 12.66%/1.2187/-17.28%, OOS 14.29%/1.2953/-17.28%). Raising gross
   buys cost tolerance precisely because the binding leg is CAGR. But rule 8 never picks it, so it is PARK.
9. **The bar is not a forward guarantee, and the run says so.** Walked forward, the breakeven itself moves a lot:
   IS-only -> OOS-only reads 3 -> 60, 15 -> 85, 22 -> 71, 40 -> 28, 25 -> 39 bps. Quote section G as a 2008-2026
   full-sample measurement of the committed book, never as a prediction of next year's tolerance.
10. **No RULES change is proposed and none is earned.** This run tunes nothing and adds no book; `RULES.md`, `scan.py`,
    `bot.py` and `baseline.py` are untouched. Rule 9 survivorship (current constituents) applies to both panels.
