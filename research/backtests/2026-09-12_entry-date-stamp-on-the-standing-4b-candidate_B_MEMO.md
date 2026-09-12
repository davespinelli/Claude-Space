# MEMO — AMENDMENT to the standing 4b candidate's memo. NOT a new candidate, NOT a RULES change.

1. **What this amends.** `2026-09-11_u56-band003-gross100_4b_B_MEMO.md` — the band book at the
   **live** band 0.03 with gross 1.00 (`rules_v2_weights(px, band=0.03, gross=1.00)`, U56, weekly,
   10 bps), the record's only zero-tuned-parameter 4b candidate. Idea 829 (lane B, 2026-09-12).
2. **The memo reproduces.** Gates 3 of 3 PASS on the 2026-09-12 prices vintage: full
   **11.54%/1.2017/−15.91%** vs published 11.52%/1.1996/−15.91%; OOS **12.70%/1.2775/−15.91%** vs
   12.66%/1.2740/−15.91%; SPY 15.16%/0.8861/−33.72%. Nothing in points 1–7 of that memo changes.
3. **What is new.** Its 4b pass was only ever read on ONE window. Over **4,520** entry-date windows
   (4 horizons × 2 spacings × every monthly/quarterly entry), scoring 4b **window-locally against
   SPY over the same window**, the joint pass share is **0.3977 (3y) / 0.5610 (4y) / 0.6513 (5y) /
   0.9344 (7.5y)** at monthly entries — all 8 grid points reported in `…_B.grid.csv`.
4. **The risk legs ARE entry-date robust.** Sharpe beats SPY in **152 of 152** five-year windows
   (and 122 of 122 at 7.5y). The DD cap fails in only 11 of 152, all one consecutive 2013 entry
   block whose windows end in 2018 — the sample's shallowest 5-year SPY drawdown (−13.02%, cap
   −7.81%) — missing by **0.58 pp**. No window fails on Sharpe.
5. **The CAGR floor is what is fragile.** All 31 CAGR-leg failures sit in windows where SPY
   compounded **9.70%–22.15%/yr**. The book's own CAGR barely moves across windows (median
   10.65%–11.03% at every horizon); it is the comparand that moves. Every failing entry date is
   **2009-01-13 … 2017-06-16**; pass share for entries ≥ 2015-01-01 is **0.9750** (78 of 80).
6. **Point 6 of the memo (the RULES wording) is unchanged and its direction is now confirmed
   twice.** Raising gross 0.75 → 1.00 lifts the entrant pass share from **0.1184 to 0.6513** at the
   headline and wins at **8 of 8** grid points — an entry-date-robust reason for the one line the
   memo proposes to change. Sharpe is flat across gross to 0.0001, so gross buys CAGR and
   drawdown only, as caveat (a) already said.
7. **Add this stamp to any promotion.** The candidate clears 4b *with a holding horizon attached*:
   ~0.65 of 5-year entrants and ~0.93 of 7.5-year entrants. Below 4 years it is a coin flip.
   Quote the horizon, not a bare "4b PASS".
8. **Rule 8 on this run's own parameter FAILS and is reported as unselectable:** IS pass
   0.2500/0.2083/0.0278/0.3333 against OOS 0.5375/0.8088/0.9643/1.0000; the IS-chosen H = 1890
   rests on 6 windows because a 7.5-year window cannot close inside 2009–2016. |OOS − IS| = 0.6667
   vs a 0.10 bar, in the generous direction at every horizon. The ladder is monotone in horizon.
9. **New caveat (d), and it bounds every 4b verdict in the record:** this sample contains **zero**
   SPY windows of 3 years or longer with a negative CAGR (0 of 4,520). The 4b CAGR floor has never
   been tested against a flat or falling benchmark, and the DD cap is generous exactly when SPY
   crashes and binding when SPY is calm.
10. **No action.** 4a still FAILS (−15.91% vs the live book's −12.05%). No book is proposed or
    promoted, no RULES/PROTOCOL/baseline/scan/bot edit is made, and the Sunday review remains the
    only place the live rules may change (rule 6). Caveats (a)–(c) of the original memo stand.
