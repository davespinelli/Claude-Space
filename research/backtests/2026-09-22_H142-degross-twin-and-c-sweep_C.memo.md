# Idea 1472 (lane C, 2026-09-22) — KEEP-4b CANDIDATE, RECORDED AND **NOT RECOMMENDED** (PARK)

**The book.** U56, weekly, N = 20 held under a min-hold **H = 142** trading days, selected by the
live composite; the held names are ranked by trailing 126d beta to SPY (ascending) and weighted
`w_i = (G/n)(1 + c*z_i)`, `z_i = 1 - 2(rank_i - 0.5)/n`, **c = 0.50**, **G = 0.75**, lowest beta on
the cap side. Idea 1461's incidental candidate, re-priced here and replayed to 1.9e-4.

**At the live 10 bps rung.** FULL **15.47% / 1.2102 / -19.47%** (halves 1.3024 / 1.1579),
OOS 2017-2026 **17.25% / 1.2348 / -19.47%**, turnover 3.42x/yr, mean gross 0.75.
SPY 15.14% / 0.8852 / -33.72% (OOS 15.29% / 0.8753 / -33.72%); RULES v2 8.62% / 1.2012 / -12.05%.
**4b clears on all five legs, FULL and OOS** (CAGR +4.87 pp over the 10.60% floor, MaxDD +0.76 pp
inside the -20.23% cap). **4a fails** (MaxDD -19.47% vs the live book's -12.05%), as does every one
of the 150 cells.

**It is NOT the exposure scalar — the first band cell in the record that is not.** Against its own
CAGR-matched de-gross twin (the same names, the same days, gross scaled by k = 0.9223 so net CAGR
matches to 9.9e-10) it wins on **both** axes: MaxDD **+0.366 pp**, Sharpe **+0.0229**. All four
biting c rungs at U56/H=142 do. The beta ORDERING is doing the work, not the dispersion: against 20
rank-permutation twins holding the identical weight multiset, t(Sharpe) = **21.5**, t(MaxDD) =
**16.4**, and 0 of 20 permutations beat it on either axis.

**Why it is NOT recommended.** (a) **Rule 8 cannot reach it**: 0 of 4 legal IS-only choosers pick it
at 10 bps; the two Sharpe/leg choosers pick H = 142 **c = 0.00** (the plain anchor) and the
zero-parameter frozen incumbent is the only chooser with any OOS 4b passes (5 of 5, vs 0 for both
fitted choosers). (b) **The twin clears 4b in EXACTLY the same 55 of 150 cells — 0 flips in either
direction**: the band's edge is real but too small to move a verdict. (c) The edge is **panel- and
H-dependent and dies with cost**: dSharpe is +0.0180 at U56/H=142 but **-0.0166** at U56/H=126 and
**-0.0054** at B136/H=142, and the U56/H=142 DD edge turns negative by 50 bps (-0.396 pp).

**RULES wording, if a future Sunday review ever adopts it — exact text, NOT proposed now:**

> 3. Within the held set, rank the names by trailing 126-day beta to SPY, ascending, and weight
>    them `w_i = (gross / n) * (1 + 0.50 * z_i)` where `z_i = 1 - 2*(rank_i - 0.5)/n`; the lowest-beta
>    name takes the largest weight. Names are held for a minimum of 142 trading days.

**No RULES change is proposed by this run.** PROTOCOL rule 8 is not satisfied; the candidate is
recorded so a later run can test whether any legal chooser reaches it.
SURVIVORSHIP (rule 9): U56 is a current-constituent list, so every absolute level is an upper bound;
the twin contrasts are built over the same names on the same days and the bias cannot manufacture them.
