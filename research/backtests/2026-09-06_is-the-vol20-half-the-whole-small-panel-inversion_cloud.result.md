# Idea 282 — is the `vol20 < 0.60` half the whole small-panel inversion?

**ANSWERED: NO — the inversion is joint, and the vol half is the larger of two independently
negative halves. Not a KEEP. No RULES change; RULES.md, scan.py, bot.py, baseline.py untouched.**
80 grid points (5 vol ceilings x trend on/off x rw/dg convention x 2 panels x 0/10 bps), all reported
in `..._grid.csv` / `_halves.csv` / `_walkforward.csv` / `_keeppaths.csv`. Two tuned parameters (vol
ceiling, trend switch); convention and cost rung are reported axes, never chosen.

1. **Idea 60's attribution reproduces to 2 dp.** SMALL439, EWall @0.75 gross, weekly, 0 bps, `rw`:
   vol half alone (trend off, 0.60 vs off) **-4.261 pp/yr**, trend half alone (no vol cap)
   **-2.788 pp/yr**, both **-5.31 pp** (idea 60 published -5.3121). The halves are sub-additive
   (sum -7.05 vs joint -5.31); vol is **60.4%** of the summed damage.
2. **The queued hypothesis fails.** Deleting the vol filter entirely does not restore the trend gate:
   the trend half is negative at **every one of the 5 vol ceilings**, in both conventions and both cost
   rungs, on SMALL439 (rw @10bps: -1.55 / -1.19 / -1.79 / -2.54 / -3.70 pp and -0.139 / -0.079 /
   -0.108 / -0.129 / -0.175 Sharpe at caps 0.30 / 0.45 / 0.60 / 0.90 / off). The trend gate is
   inverted on sub-$2B names on its own terms.
3. **New, and it bears on the large-cap book: at matched realised gross the 200d gate subtracts on
   U56 too.** Under `rw` (constant 0.75 gross) the trend half is -0.032 to -0.178 Sharpe at all 5
   ceilings @10 bps. It is positive only under `dg` at loose caps (+0.043 at 0.90, +0.048 at off),
   where the gate cuts mean gross 0.75 -> 0.53. Idea 277's channel: the gate's apparent large-cap
   value is **exposure reduction, not information**.
4. **The vol half on U56 is ~zero at matched gross** with no trend gate (+0.0017 Sharpe @10 bps) and
   -0.042 with one — idea 60's by-product holds on a second construction.
5. **Every argmax is a grid end** (vol cap `off` maximises CAGR in 8/8 panel x conv x cost blocks;
   Sharpe is U-shaped on SMALL439 with the tightest cap 0.30 beating 0.45/0.60). Idea 256's shape.
6. **Rule 8** (arm chosen on IS <= 2016 by IS Sharpe, 2017-2026 read once): the chooser picks
   do-nothing (no gate) in 6 of 8 cells. On SMALL439 its best OOS Sharpe is **0.647 vs SPY 0.882** —
   **0 of the 20 small-panel arms @10 bps beat SPY OOS** (best 0.6367); where the chooser deviates
   (0 bps, off/0.30) it loses to do-nothing by **-0.188 Sharpe / -5.76 pp CAGR**: another
   selector-loses-to-a-constant instance (idea 60 logged the 14th).
7. **KEEP paths @10 bps: 4a 0/40. 4b 5/40, all on U56, 0 on SMALL439.** Binding bars over the 35
   failures: CAGR 29, H2 21, H1 20, OOS 20, DD 18.
8. **Best cell (PARK, not KEEP):** U56 `rw`, trend OFF, volcap 0.60 — 12.22% CAGR / **1.1301** Sharpe /
   -18.35% MaxDD, halves 1.1448 / 1.1180, OOS **1.1852** vs SPY 0.8820, turnover 1.89x/yr.
   Exact wording if it were ever promoted: *"Each rebalance week, hold every instrument whose 20-day
   annualised volatility is below 0.60 at 0.75/N of NAV, N = eligible instruments that week; no trend
   filter, no ranking; weights applied at the next close."*
9. **Why PARK.** It fails 4a against the live RULES v2 (1.2056 Sharpe, -12.05% MaxDD) on both halves
   and on drawdown, and the rule-8 chooser never selects it (picks no-gate in 4/4 U56 cells, whose
   own OOS is 1.1404 and which fails 4b on drawdown by 2.2 pp). A 4b pass that the project's own
   pre-registered selector cannot find is not a book.
10. **SURVIVORSHIP:** SMALL439 is current constituents of a sub-$2B screen only (44 of 483 tickers with
    `max_1d_move >= 1.0` dropped first). The bias flatters the **un-gated** arm most — dead names are
    missing precisely from the beaten-down cohort the gates exclude — so the measured gate damage on
    the small panel is an **upper** bound, and this run does not overturn that caveat.
