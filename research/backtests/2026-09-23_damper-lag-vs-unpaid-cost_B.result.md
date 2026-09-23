# idea 2404 (lane B, run 43) — does the DAMPER's MaxDD/CAGR change come from LAG or from UNPAID COST?

**ANSWERED = BOTH, AND THE SPLIT IS CLEAN AND OPPOSITE BY METRIC. CONFIRM of run 39's CAGR
attribution; the MaxDD damage is PURE LAG and cost NEVER explains any of it. NO NEW CANDIDATE,
NO RULES CHANGE.** 1344 published rows, **18 of 18 gates pass**, 20s, offline caches only.

## The instrument: an exact algebraic split, not a regression
This record prices every book as `priced(rung) = r0 - turnover x rung/1e4`, so the damper's two
channels separate **exactly**. From ONE damped pass and ONE undamped pass, four books at every rung:

| book | holdings | bill | isolates |
|---|---|---|---|
| `U` (anchor) | undamped | undamped | — |
| `LAG` | **damped** | undamped | the holdings path alone |
| `COST` | undamped | **damped** | the unpaid bill alone |
| `D` (run 39's book) | damped | damped | both |

`(D - U) == (LAG - U) + (COST - U)` on the return series to **1.39e-17** (G14, 336 cells), and at
0 bps `LAG == D` and `COST == U` at **0.000e+00** (G15) — so the 0 bps column IS pure lag by
construction. CAGR/Sharpe/MaxDD are non-linear in the path, so their three deltas are published
**with the interaction residual**, never asserted to add up. Dials: `lam` {1.00 … 0.10} x `gross`
{0.50, 0.75, 1.00} and no others (G8). Reported never selected on: books {CAP2, CAND}, panels
{U56, B136}, rungs {0, 10, 25, 50} bps, weekly, band 0.03, t+1, SHY sweep phi = 1.00. Three
committed headlines reproduced externally: idea 2336's CAP2 U56 (3.95e-05), idea 2300/2332's CAND
U56 (3.04e-06) and **idea 2391's own `lam = 0.40` headline 11.79% / 1.2538 / -16.92%, OOS 12.98% /
1.3091, 2.34 turns/yr (3.69e-05, G3b)**.

## Run 39's headline, audited (lam = 0.40, 10 bps, live gross 0.75)

| cell | dCAGR total | = LAG | + COST | + inter | **cost share** | dMaxDD total | = LAG | + COST |
|---|---|---|---|---|---|---|---|---|
| U56 / CAP2 | +0.1697 pp | +0.0396 | **+0.1300** | +0.0002 | **77%** | -2.1072 pp | **-2.1652** | +0.0200 |
| U56 / CAND | +0.3289 pp | +0.1418 | **+0.1869** | +0.0002 | **57%** | -1.1334 pp | **-1.1954** | +0.0626 |
| B136 / CAP2 | +0.2235 pp | +0.0322 | **+0.1912** | +0.0001 | **86%** | -2.4266 pp | **-2.5005** | +0.2267 |
| B136 / CAND | +0.3531 pp | +0.1435 | **+0.2094** | +0.0002 | **59%** | -2.3308 pp | **-2.4055** | +0.0765 |

**Run 39 was right about the CAGR and never looked at the drawdown.** "The un-traded distance is
un-charged" explains **57-86%** of the CAGR gain at the live rung. It explains **none** of the
drawdown: the COST channel's effect on MaxDD is *positive* (a smaller bill can only help), and the
whole 1.1-2.5 pp of drawdown damage is the holdings path.

## Census over all 288 damped cells — the two channels behave completely differently
`LAG`'s CAGR contribution is **rung-invariant** by construction and reads it: median +0.0736 /
+0.0732 / +0.0726 / +0.0716 pp at 0 / 10 / 25 / 50 bps. `COST`'s scales linearly with the rung:
median **+0.0000 / +0.1396 / +0.3470 / +0.6880 pp** (ratio 1 : 2.49 : 4.93 against 1 : 2.5 : 5).
Cells where `|LAG| > |COST|` on CAGR: **72/72 at 0 bps, 9/72 at 10, 0/72 at 25 and 50** — above the
live rung the damper's return gain is *entirely* a cost rebate. On MaxDD the ordering inverts:
`|LAG| > |COST|` in **71/72, 67/72, 50/72** cells at 10 / 25 / 50 bps, and **MaxDD is worsened by
the COST channel in 0 of 288 cells** at any rung. Pure-lag drawdown damage is monotone in the dial
(U56/CAP2, 0 bps): **-0.12 / -0.39 / -1.15 / -2.10 / -3.31 / -4.91 pp** at lam 0.85 → 0.10, against
a pure-lag CAGR of **+0.001 → +0.077 pp**. The damper buys a linear-in-cost rebate with a real,
monotone, *un-refundable* drawdown.

## What that does to the KEEP paths — the counterfactuals tell the story
Joint both-panel 4b at the live gross (4 rungs, max 4), CAP2: the incumbent `lam = 1.00` is **3/4**;
`COST` (rebate only, no lag) holds **3/4 → 4/4 → 4/4 → 4/4** all the way down to lam 0.10 while
`LAG` (lag only, no rebate) **collapses 3/4 → 3/4 → 0/4 → 0/4** — and the real book `D` tracks
**LAG**, not COST: 3/4 at 0.55, 4/4 at 0.40, then **0/4 at 0.25 and 0.10**. CAND is the same shape
(`COST` 4/4 at every lam ≤ 0.40, `D` 0/4 below 0.55). `L_DD` and `L_CAGR` are the only binding legs
anywhere (0 bps: L_DD 100, L_CAGR 112, L_H1/L_H2/L_OOS all 0). `D`'s single 4/4 cell at lam = 0.40
is therefore a rebate artifact sitting one notch above a cliff the lag channel drives.

## Rule 8 (walk-forward) is the independent kill
(`lam`, `gross`) fitted on ≤ 2016-12-31 only, 2017-2026 read ONCE, 32 picks: **0 of 32 carry a
full-sample 4b pass**, only **6 of 32 land on the undamped incumbent**, **23 of 32 land on lam =
0.10** — the setting whose joint both-panel 4b is 0/4 — and **32 of 32 pick gross 0.50**, which is
below the 4b CAGR floor by construction. At 10 bps, U56/CAP2's pick (0.10, 0.50) reads OOS
**9.74% / 1.3040 / -12.88%** against the undamped anchor's **12.77% / 1.3318 / -14.81%**, live
RULES v2's **10.21% / 1.3636** and SPY's **15.45% / 0.8831**; B136/CAP2's pick reads OOS **9.50% /
1.2053 / -14.74%** against the anchor's **11.65% / 1.0936**, RULES v2's **8.57% / 1.1908** and SPY's
**15.26% / 0.8737**. An in-sample chooser reliably buys the cost rebate and reliably eats the lag.

## Caveats
Current-constituent survivorship in `universe.json` and `universe_broad.json` (rule 9). 2009-2026 is
one regime; only 2020 and 2022 are real stress. SMALL is not priced: ideas 2318 / 2322 / 2326 / 2343
each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there to decompose. The 4a
baseline is priced at the row's own rung here (2391/2412 pinned it at 10 bps); the 10 bps column is
identical under both conventions. Non-linearity of CAGR/Sharpe/MaxDD means the three deltas are
approximate as an *attribution* even though the return identity is exact — the interaction residual
is published on every cell and is ≤ 0.0005 pp on CAGR everywhere and ≤ 0.153 pp on MaxDD at worst.

## AMENDMENT to the record (no RULES.md change; nothing here is a Sunday-review item)
Idea 2391's claim "the un-traded distance is un-charged" should be recorded as **CONFIRMED for CAGR
and INAPPLICABLE to MaxDD**. Any future turnover device in this record should publish its
**0 bps column** beside its headline: that column is the device's pure holdings-path bill, it is
the leg (`L_DD`) this family actually dies on, and it is free to compute from the same pass.
