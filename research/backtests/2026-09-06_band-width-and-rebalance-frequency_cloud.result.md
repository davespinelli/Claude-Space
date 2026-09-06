# Idea 59 — band width vs rebalance frequency: is the band doing anything the cadence isn't?

**ANSWERED: YES, but it is the SMALLER half, and the two do not add. No new book, no RULES change;
RULES.md, scan.py, bot.py, baseline.py untouched.** 96 grid points (6 band widths x weekly/monthly x
`rw`/`dg` x U56/B136 x 10/25 bps) plus a 32-cell separation panel, all in `..._grid.csv`,
`_effects.csv`, `_speed.csv`, `_separation.csv`, `_walkforward.csv`, `_keeppaths.csv`. Two tuned
parameters (band width, cadence); convention, cost rung and the separation panel are reported axes.

1. **Both instruments pay, and by similar amounts.** Against the plain 200d gate at weekly cadence:
   a 3% band buys **+0.0515** mean Sharpe (8/8 cells, +0.0126..+0.1176); monthly cadence at a 0% band
   buys **+0.0717** (8/8, +0.0380..+0.1310). The cadence is the larger of the two everywhere but U56
   @10 bps `rw`.
2. **They are not additive — they are substitutes.** `band3 + monthly` minus the better of the two
   alone is **-0.0189** mean and negative in **7 of 8** cells (worst -0.0403). Idea 57's "the
   monthly-re-evaluated gate performed as well as either" was the whole story: there is one effect
   with two handles, and pulling both wastes one.
3. **The separation panel says the trade schedule is the real half.** Holding the gate's state
   *identical* and moving only the rebalance W -> M: **+0.0370** mean Sharpe, **15 of 16** cells.
   Holding the trades fixed and slowing only the gate's *sampling* W -> M: **-0.0176** mean, positive
   in only **2 of 16**. Making a gate slower by looking at it less often does not work.
4. **What the band adds that speed alone does not.** At matched flip rate (band3 1.743 vs a
   monthly-sampled 200d 1.754 on U56; 2.024 vs 1.885 on B136) the band is worth **+0.0152** mean
   Sharpe, 6 of 8 cells. Hysteresis is a genuinely different instrument from sampling — but the
   margin is a third of the cadence's, and it flips sign on the two `dg`/monthly cells.
5. **Flip rate is not the design variable.** Spearman(flips, Sharpe) over the band sweep runs
   **-1.0 to +1.0** across the 8 (panel x cost x conv) cells with no stable sign, reproducing idea
   61's finding on a second dial.
6. **The ungated control keeps winning at matched gross.** On B136 `rw`, ungated/W beats every gated
   arm's step (+0.0652 @10 bps, +0.1624 @25 bps vs 200d/W). The gate only beats no-gate under `dg`
   on U56 (-0.0481 for ungated), i.e. through de-grossing — idea 277/282's channel again.
7. **Rule 8** ((band, cadence) chosen on IS <= 2016, 2017-2026 read once): the chooser sits at a grid
   end (widest band or ungated) in **6 of 8** cells and its OOS Sharpe beats the pre-registered
   constant `band3/weekly` in **4 of 8**, mean **-0.0025**. A coin flip: no selectable edge on this
   dial, the record's standing pattern.
8. **KEEP paths @10 bps: 4a 2/48, 4b 13/48** (9 U56, 4 B136, **all** under `rw`; `dg` fails the 4b
   CAGR floor in 24/24). Binding bars over the 35 4b failures: CAGR 20, DD 16 — no half or OOS bar
   ever binds on these panels.
9. **The two 4a passes are the live book with SPY removed from the held set**: `dg`/band3/weekly is
   RULES v2 by construction, and dropping SPY from the tradable columns is worth **+0.0070** Sharpe
   on U56 (1.2127 vs 1.2056, MaxDD -11.90% vs -12.05%) and **+0.0020** on B136. Free and directional,
   but inside noise — recorded as hygiene, not as a book.
10. **PARK by-product (4b pass, 4a fail):** U56 `rw` band 2% monthly — **12.94% CAGR / 1.1878 Sharpe /
    -18.32% MaxDD**, halves 1.2258/1.1636, **OOS 1.2368** vs SPY 0.8820, turnover 2.98x/yr. Exact
    wording if it were ever promoted: *"Each month-end, hold every instrument whose close is more than
    2% above its 200-day moving average (and keep holding until it closes more than 2% below) at
    0.75/N of NAV, N = instruments admitted that month; weights applied at the next close."* It fails
    4a against RULES v2 on drawdown (-18.3% vs -12.1%) and the rule-8 chooser never picks it, so it is
    a PARK. **SURVIVORSHIP:** B136 is current constituents only (PROTOCOL rule 9).
