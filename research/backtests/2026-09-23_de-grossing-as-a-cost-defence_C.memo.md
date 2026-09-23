# 4a KEEP-CANDIDATE MEMO — idea 2443 (lane C, run 51, 2026-09-23) — FILED, **NOT RECOMMENDED**

1. **The candidate.** The standing capped candidate (`CAP2`) run at **gross G = 0.40** instead of the
   committed 0.75, on panel **U56** (`research/universe.json`), weekly, t+1, 10 bps, SHY sweep.
2. **Full sample** (2009-01-13..2026-09, warm-up skipped): **CAGR 7.16% / Sharpe 1.3375 / MaxDD
   -8.15%**, halves **1.3510 / 1.3350**, turnover **2.32x/yr**. Live RULES v2: 1.2052 (1.2262 /
   1.1897), MaxDD -12.05%, 1.77x/yr. SPY: 15.23% / 0.8897 / -33.72%.
3. **Out of sample (2017-2026, read once):** **7.92% / 1.4072 / -8.15%** against the live book's
   1.2839 and SPY's 0.8831 (SPY OOS CAGR 15.45%).
4. **Path 4a is cleared** with the baseline priced at the same rung, at **0, 10, 25 and 50 bps**
   (breakeven **68 bps**; 36 bps with the baseline pinned at the protocol's 10), and it is **JOINT
   both-panel 4a on BOTH books at 0 / 10 / 25 bps** (B136 breakeven 40 bps).
5. **Rule 8 endorses it:** `G` fitted on warm-up..2016-12-31 only by two pre-stated IS choosers,
   2017-2026 read once — **32 of 32 picks land on G = 0.40**, beating the live baseline OOS 32 of 32
   and SPY OOS 32 of 32 at mean OOS Sharpe 1.2497 vs the committed cell's 1.1435.
6. **It fails path 4b on `L_CAGR` alone, by -3.50 pp** (7.16% against the 10.66% floor = 0.70 x SPY),
   a wider miss than lane B run 50's `FIX w* = 0.0125` candidate (-2.26 pp). 0 of 404 rows at
   G = 0.40 pass 4b at any of the 101 rungs.
7. **EXACT RULES WORDING IF EVER ADOPTED** (two clauses touched, nothing else; version bump to v3
   and a CHANGELOG entry required by rule 6):
   - **Clause 4 (Sizing) replaced by:** "Each IN name is held at `min(0.40 / N_in, 0.020)` of current
     NAV, where `N_in` is the number of names IN on the decision day. Round shares down to whole
     units. All NAV not held in IN names is held in **SHY**; if SHY is itself OUT it is held in cash.
     Do not re-spread a capped name's excess weight over the other IN names."
   - **Clause 5 (Rebalance) second sentence replaced by:** "...and reset every position to
     `min(0.40 / N_in, 0.020)` of NAV, sweeping the residual to SHY."
8. **RECOMMENDATION: DO NOT ADOPT.** This is the committed candidate with `G` turned down; it adds
   no new clause and no new information. Its 4a pass is bought by **holding less**, not by trading
   better: `turnover / G` is flat to cv 0.133 and `CAGR / G` to cv 0.116 across the whole ladder.
9. **The blocking fact, published as its own number:** over 2424 rows, **4a passes 249 and 4b passes
   458 and NO row passes both.** Every 4a pass sits at `G <= 0.55`; every 4b pass at `G >= 0.70`.
   4a's drawdown clause rewards de-grossing and 4b's CAGR floor punishes it, so a 4a pass reached by
   lowering `G` moves the book **away** from the path that governs real capital.
10. **Status:** filed for the record, superseding lane B run 50's weaker 4a candidate on every axis
    except adoptability, where both are the same answer — **no**. The live book, the standing 4b
    candidate, its `L_DD` leg and its 3.51x turnover blocker are all unchanged.
