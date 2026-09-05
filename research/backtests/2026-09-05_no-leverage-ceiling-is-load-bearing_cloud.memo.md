# Idea 148 — the no-leverage ceiling IS load-bearing, and only through the CAGR floor

**Verdict: ANSWERED — premise CONFIRMED, mechanism isolated, and it is narrower than idea 144 implied.**
No new book, no KEEP candidate, no RULES change. One proposed PROTOCOL reporting clause.

1. **57 of 306 4b verdicts (18.6%) are decided by where the ceiling is put**, not by either bar, over
   the legal range c = 0.75 .. 1.3333 (1.3333 x 75% target = 100% gross = PROTOCOL rule 2's actual
   boundary). 16 books pass at every legal ceiling; 233 pass at none.
2. **The ceiling is load-bearing exclusively through the CAGR floor.** Of the 57 ceiling-decided
   KILLs at c = 0.75, **57 fail the CAGR floor** and 55 fail *only* the floor; **0 fail the DD cap**
   at any ceiling. With the floor deleted (phi = 0) the ceiling-decided count is **0 at all 6 deltas
   and all 13 ceilings** — the clause has no independent bite.
3. **Idea 144's own ceiling was nearly harmless; the principle is not.** Moving c from 1.30 to the
   legal 1.3333 changes **1** verdict. Moving it to 1.00 changes 15; to 0.75, 57. The published
   number was safe by luck of placement, not by construction.
4. **4a is completely ceiling-insensitive**: 184 of 306 books pass FAMILY-4a at *every* ceiling.
   The interaction is a 4b-only phenomenon.
5. Reproduction before any new number: H.run vs engine.backtest max|diff| **0.000e+00**; idea 94's
   published EWall+vol60-dg u56@10bps row exact (11.587% / 1.133 / -16.884%); idea 129/131's POINT
   census exact (**306 rows / 29 pass4b / 27 floor-only**); idea 144's floor-exclusion claim exact
   (**51 -> 37**). Idea 144's "binds in 54 of 306" did **not** reproduce under any of three readings
   (set reaches the ceiling 9; verdict differs c=1.00 vs 1.30 14; family-Sharpe argmax at 1.30 106) —
   reported as unreproduced, not reconciled.
6. Rule 8 (choose on 2009-2016, evaluate 2017-2026): every family ceiling beats the no-screen control
   on OOS Sharpe (+0.032 paired, best c=1.20 at 0.710) and the m-pinned screen by +0.010, but **all
   are far below SPY's 0.882**; OOS CAGR 6.4-8.9% vs SPY 15.45%, MaxDD -17 to -22% vs SPY -33.7%.
   Raising the ceiling buys CAGR and pays drawdown at a near-constant rate and moves Sharpe ~0.
7. Every grid point printed: 13 ceilings x 7 phi x 6 delta = 546 verdict sets; 7,956 backtests.

**Proposed PROTOCOL clause (for the Sunday review, not applied here).** Rule 4b, add:
> When a book is judged over its own gross family (idea 144's convention), the family's upper bound
> is a *bar*, not a construction detail. Quote it with every FAMILY verdict as
> `m_max = <value> (= <gross>% gross)`, and report the verdict at the no-leverage boundary
> (100% gross) alongside it. Where the two differ, the verdict was set by rule 2, not by rule 4b.

**Caveats.** Survivorship: all three panels are current-constituent lists; the small panel drops the
44 tickers with max 1-day move >= 1.0 (439 of 483 kept) and excludes delisted/acquired names — a
one-directional upward bias. Idea 128: the IS window's SPY MaxDD (-22.1%) is shallower than the OOS
window's (-33.7%), biasing every IS screen toward too much gross. Idea 38: u56/broad are on a
calendar-day index. The two `ebud` arms take an absolute turnover budget and are not pure exposure
rescales. Grid resolution is 0.05 in m (0.0375 of gross).
