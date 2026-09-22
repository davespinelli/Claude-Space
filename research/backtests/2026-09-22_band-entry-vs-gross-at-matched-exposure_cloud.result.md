# Idea 2233 — does the BAND ENTRY THRESHOLD alone move TIME IN MARKET more cheaply than GROSS does?

**ANSWERED = NO. KILL of the premise.** Script:
`research/backtests/2026-09-22_band-entry-vs-gross-at-matched-exposure_cloud.py`
(96 books x 3 cost rungs = 288 grid points, all reported in `.grid.csv`; pairs in `.pairs.csv`,
slopes in `.slopes.csv`, rule 8 in `.walkforward.csv`, full console in `.console.txt`).

1. **The slope law runs the wrong way, 6 of 6.** dCAGR per unit of MEAN REALISED EXPOSURE,
   OLS over each arm's own rungs at 10 bps: GROSS **0.1640 / 0.1503 / 0.0989** (U56 / B136 /
   SMALL, full sample) against b_in's **0.1107 / 0.1230 / 0.0484**; OOS **0.1809 / 0.1479 /
   0.0818** against **0.1059 / 0.1044 / 0.0061**. Gross is the steeper dial everywhere, so the
   book's missing return is **cheaper on the size, not on the band**.
2. **Gross is Sharpe-neutral; b_in is not.** Over 0.25..1.50 the U56 band book's Sharpe moves
   1.2010 -> 1.2000 (r = 1.000 on CAGR vs exposure) while b_in -0.02 .. +0.20 costs it
   1.2010 -> 1.0374. The entry edge buys its exposure cut by *changing which days are held*,
   and on the mega-cap panels those are days worth holding.
3. **Exactly matched exposure (not interpolated).** Mean exposure is linear in gross at a fixed
   band, so each b_in rung's de-grossed twin is SOLVED, g* = E(b_in)/occ(0.03), and run as a
   real book (the b_in = +0.03 pair reproduces itself to 4 decimals, the built-in check).
   BIN beats its twin on full CAGR **22 of 39**, on full Sharpe only **15 of 39** (U56 **1 of
   13**), on MaxDD 23 of 39, on OOS Sharpe 15 of 39.
4. **Every 4b pass in the grid is a GROSS pass.** 4 of 96 points clear 4b at 10 bps — U56 and
   B136, `b_in = 0.03` untouched, gross 1.00 and 1.25 — and **0 come from the BIN or MATCH
   arms**. 4a is **0 of 96** at 10 bps (6 of 192 at 25/50 bps, all SMALL/BIN at the tight end).
   The CAGR floor binds 90 of 92 fails; the DD cap binds 4. This re-confirms 2119 on a dial
   2119 never walked: the 4b verdict still turns **entirely on gross**.
5. **Rule 8 (dial chosen on the first half, second half read once): 0 of 9 arms reach 4b OOS.**
   The IS-Sharpe chooser picks the END of the gross ladder (g = 1.50) on all three panels —
   because IS Sharpe is flat in gross to ~0.001, the argmax is noise — and that pick blows the
   OOS DD cap on all three (-23.38% / -23.75% / -22.79% against 0.60 x SPY OOS = -20.23%).
   1 of 9 reaches 4a OOS (SMALL, BIN, b_in = +0.17: OOS 3.82% / 0.6750 / -7.96% against v2's
   4.56% / 0.6378 / -12.11%) — a Sharpe-and-drawdown 4a pass that gives up CAGR to get it.
6. **PARK, not KEEP, worth one line:** on SMALL only, at matched exposure, tightening b_in
   DOMINATES de-grossing on all four axes (CAGR, Sharpe, MaxDD, OOS Sharpe) at **5 of 7** rungs
   b_in >= +0.04 — median dSharpe +0.0062, dOOS_Sharpe +0.0086, dMaxDD +0.39 pp shallower. It
   still never reaches 4b: SMALL's CAGR floor (0.70 x SPY 14.03% = 9.82%) is 6 pp above
   anything the arm produces.
7. **No rules change.** RULES v2 clause 2's single +/-3% band stands; nothing here earns a
   Sunday review. U56 GROSS g=1.00 clears 4b full and OOS (11.53% / 1.2009 / -15.91%, OOS
   12.67% / 1.2760 / -15.91%) but is **not rule-8 reachable** — the IS chooser does not pick it
   — and it is the record's already-known gross-ladder cell, not a new book.

**Survivorship:** U56 and B136 are 2026 constituent lists held from 2008; SMALL is the current
sub-$2B screen held from 2010 (719 cached names less the 54 with `max_1d_move >= 1.0`, leaving
**665 investable**; SPY joined as benchmark only). Every level is an upper bound on what a
2009/2010 investor could have had. SPY is traded and carries no such bias, which is why the 4b
bar is taken against it.

**Costs/execution:** 10 bps per unit turnover headline (25 and 50 reported), weights decided at
close t and applied at t+1, weekly cadence, 260-row warm-up. Two tuned parameters only (b_in,
gross); all 288 grid points reported.
