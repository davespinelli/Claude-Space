# Idea 944 (cloud, 2026-09-15) — ANSWERED = NO for "EVERY" / KILL for the universal claim

**Question.** Idea 938 found all 18 of 25 failing monthly offsets of U56 CORE/TOP20 fail on L4_DD
alone. Is the 4b drawdown cap the binding leg for *every* offset-fragile book, and which 4b
statistic is a coin flip on the rebalance date?

**The premise splits in two, and the halves answer differently.**

**Half one holds — MaxDD is the phase-fragile statistic.** Over 144 cells (6 books × 3 panels × 2
phase grids × 4 cost rungs, 1,872 scored books), the **leg flip rate** — the share of cells where a
leg's verdict is not unanimous across its own phase family, with nothing changed but the rebalance
date — runs **L4_DD 36.1%** (DOM21 47.2%, DOW5 25.0%), L2_H2 20.8%, L3_OOS 20.8%, L1_H1 18.1%,
L5_CAGR 13.9%. The whole 4b verdict flips on the rebalance date in **22.9% of cells, 31.9% of the
monthly ones**. The **coin-flip index** (phase support ÷ median distance to the leg's own bar) is
**MaxDD 1.216, above 1.0 in 57.6% of cells**; every other statistic sits below 0.80 (H1 0.766, H2
0.742, OOS Sharpe 0.685, CAGR 0.623). Median MaxDD support 6.245 pp against CAGR's 1.767 pp.

**Half two does not hold.** Over the 1,705 failing (cell, phase) rows the plurality signature is
**all five legs failing at once (30.4%)**, with L4_DD alone second at 21.8% and L4_DD anywhere at
79.9%. 938's clean "18 of 18 on L4_DD alone" is a property of U56/TOP20 — a book whose other four
legs pass comfortably — not of the bar. The leg *ranking* is not stable across grids either
(H_GRID FAIL), though L4_DD tops both.

**The census (835,403 committed 4b FAIL rows across 680 files, tree 574d5b8).** Only 125,090
(15.0%) carry a readable binding leg; **710,313 (85.0%) carry none at all**. Among the readable
ones: all five 26.4%, L5_CAGR alone 18.2%, **L4_DD alone 15.8%**, L4_DD anywhere 60.5%. That 15.8%
is the number *after* a measurement fix that is itself a finding: the record writes the same leg as
`L4_DD`, `DD`, `DDCAP` and `L4_DDcap`, joined by `+`, `,`, `|` or `/`. One alphabet reads L4_DD-alone
at **1.9%**; two at **14.7%**; all five at **15.8%**, with 10 unmapped rows of 125,090.

**A record defect found and priced (G3b).** The committed `CORE/TOP20` holds the top n at a fixed
g/n, so a day with fewer than n eligible names de-grosses (1,124 of 4,704 U56 days). Ideas 931 and
945 ran a **re-spread g/k(t)** variant while calling it the committed book. Same tape, same day,
canonical monthly @10 bps: **TOP20 14.69% / 1.2023 / −19.51% vs TOP20R 15.28% / 1.2120 / −19.51%**,
dCAGR **+0.0059** — exactly the miss both runs reported against the 0.005 cross-run bar. Neither was
a data-vintage effect. Both variants are carried side by side through this whole run.

**Rule 8.** Phase chosen on 2009–2016 by IS Sharpe, 2017–2026 read once, beside the canonical phase.
**IS-chosen: OOS 4b 18 of 144, 4a 0 of 144, mean OOS Sharpe 0.7566. Canonical: 4b 23 of 144, 4a 0 of
144, mean 0.7798.** Choosing the rebalance date in sample costs **−0.0232 of OOS Sharpe and 5 of 23
4b passes**. The IS chooser picks canonical in only 12 of 144 cells; where it deviates it wins out
of sample in **45 of 132 (34.1%)**. Best OOS cell per panel: U56 `TOP20R` DOW5 @0 bps phase 3,
17.10% / 1.305 / −17.51% (4b PASS, 4a FAIL); B136 `EWELIG` DOW5 @0 bps phase 1, 12.07% / 1.155 /
−16.46% (4b PASS); SMALL `BAND03` DOM21 @0 bps phase 0, 4.30% / 0.616 / −16.56% (4b FAIL). Against
SPY OOS 0.874 / 0.877 Sharpe and RULES v2 OOS 9.66% / 1.302 / −12.03%. **4a is 0 of 288.**

**Gates 9 of 9 PASS**, including an exact cross-run reproduction of idea 938's committed DOM21
numbers (MaxDD −0.2295..−0.1489, CAGR spread 1.95 pp, 16 of 21 FAIL all on L4_DD alone).

**Nothing promoted. No RULES change, no PROTOCOL edit (rule 6).** Proposed for Sunday review: *any
published 4b FAIL must name its binding leg in the canonical `L1_H1 … L5_CAGR` alphabet, and any 4b
verdict on a book whose phase family was not run must carry the note that it was read at one
rebalance date.* Measured cost: 710,313 of 835,403 rows would need the first clause; the second
would bite on 22.9% of cells.

**SURVIVORSHIP.** U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52
tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown level is
optimistic and both 4b bars are easier here than on a point-in-time panel. The phase contrasts are
same-tape, same-names, same-rule comparisons with only the rebalance date moved, and the flip rates
and coin-flip indices are differences within a cell, so they are far less exposed than the levels.
