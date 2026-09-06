# Idea 154 — ew-band3-at-085-does-not-hold-on-broad (cloud lane, 2026-09-06)

**Verdict: KILL of idea 84's `ew-band3` at g = 0.85, with a correction to idea 90's own
number.** On a 121-point gross ladder (5× finer than idea 90's 25-point grid, comparable to
idea 84's 312-point one), run side by side over BOTH conventions and at 5, 10 AND 25 bps on
one harness, **g = 0.85 passes 3 of the 6 large-cap cells and fails all three broad cells on
the drawdown bar** — margins −0.0046 / −0.0054 / −0.0078 of gross MaxDD at 5 / 10 / 25 bps
(realised **−20.69% / −20.77% / −21.01%** against the −20.23% cap). The incumbent
`EWall + vol60-dg` at g = 0.75 is **6 of 6**, exactly as the queue stated. **But idea 90's
quoted broad ceiling of 0.7877 WAS partly a resolution artefact**: on the fine ladder the
broad `band3-rw` ceiling is **0.8252 / 0.8177 / 0.8102** at 5 / 10 / 25 bps — three to four
fine steps higher — and must be re-quoted. 0.85 still sits **0.0248–0.0398 of gross above it**,
i.e. 3–5 fine steps out, so the conclusion is unchanged and is now grid-independent.

**The convention fork settles more than idea 90 could see: under `dg`, g = 0.85 is not
inadmissible — it is UNREACHABLE.** The de-grossed band3 book cannot get there: at the
no-leverage ceiling m = 1.30 its realised mean gross is only **0.6924 (u56) / 0.6916 (broad)**,
because the sticky 3% band holds a large cash share for most of the sample. So idea 84's
"g = 0.85" is only a well-posed statement under `rw`, and under `rw` it dies on broad's
drawdown cap at every rung. `band3-dg` additionally fails broad's **CAGR floor** at every
reachable point at 5/10/25 bps (one 0-bps point passes) — idea 90's "EMPTY on broad",
reproduced and now explained.

## Checks — idea 90 reproduces exactly before any new number is read

Idea 94's simulator is imported, not re-implemented; idea 90's panel convention is copied
verbatim. Cost identity `net(c) = net(0) − turnover·c/1e4` and engine equivalence are both
**0.000e+00** on all three panels; idea 94's published `EWall + vol60-dg` u56 @10bps row comes
back as **11.58715% / 1.133 / −16.884%** against its published 11.587% / 1.133 / −16.884%.
Restricting this run's ladder to idea 90's own 0.05 m-grid and its own two rungs reproduces
**all four** of its published joint intervals:

| book + arm | idea 90 published | this run, idea 90's grid |
|---|---|---|
| EWall + `vol60-dg` | [0.6839, 0.7594] | **[0.6839, 0.7595]** |
| EWall + `band3-rw` | [0.7502, 0.7877] | **[0.7502, 0.7877]** |
| EWall + `vol60-rw` | [0.6753, 0.7127] | **[0.6753, 0.7127]** |
| EWall + `band3-dg` | EMPTY on broad | **EMPTY on broad** |

So the disagreement between ideas 84 and 90 is not an arithmetic error on either side. It is
resolution plus convention, and both are now measured.

## Q1 — the 4b admissible gross interval, 121 points, 4 arms, 3 panels, 4 rungs

**All 29 non-empty 4b intervals are contiguous (29 of 29)** — the interval is a real object at
0.01 resolution, not only at 0.05. Ceilings and floors at the queue's three rungs:

| arm | panel | 5 bps | 10 bps | 25 bps |
|---|---|---|---|---|
| `band3-rw` | u56 | [0.6453, **0.8627**] | [0.6603, **0.8627**] | [0.6978, **0.8552**] |
| `band3-rw` | broad | [0.6678, **0.8252**] | [0.6827, **0.8177**] | [0.7352, **0.8102**] |
| `vol60-dg` (incumbent) | u56 | [0.6623, 0.8708] | [0.6695, 0.8708] | [0.6767, 0.8636] |
| `vol60-dg` (incumbent) | broad | [0.6221, 0.7811] | [0.6294, 0.7811] | [0.6366, 0.7811] |
| `vol60-rw` | u56 | [0.6528, 0.8327] | [0.6603, 0.8252] | [0.6753, 0.8177] |
| `vol60-rw` | broad | [0.6228, 0.7277] | [0.6228, 0.7277] | [0.6378, 0.7202] |
| `band3-dg` | u56 | [0.6498, 0.6924] | [0.6552, 0.6924] | [0.6818, 0.6924] |
| `band3-dg` | broad | EMPTY | EMPTY | EMPTY |

**Small panel: 0 of 1452 rows pass 4b under any arm, convention, gross or rung** — the
eighteenth reproduction of idea 136.

## Q2 — the two contested points, 6 large-cap cells each

| arm | g = 0.75 (incumbent) | g = 0.85 (alternative) |
|---|---|---|
| `vol60-dg` | **6 / 6** | 3 / 6 (fails all 3 broad on DD) |
| `band3-rw` | **6 / 6** | **3 / 6 (fails all 3 broad on DD)** |
| `vol60-rw` | 3 / 6 (fails all 3 broad on DD) | 0 / 6 |
| `band3-dg` | 3 / 6 (unreachable; nearest g = 0.692) | 3 / 6 (unreachable; nearest g = 0.692) |

Every failure of the alternative on the large-cap pair is the **drawdown** bar; not one is a
Sharpe or CAGR bar. Raising gross from 0.75 to 0.85 buys +1.6 pp of CAGR on broad (11.73% →
13.27% at 10 bps) at 2.2 pp of MaxDD (−18.53% → −20.77%), which is exactly the ~1.0 pp-for-pp
exchange rate idea 66 published for de-grossing — the alternative is not a different book,
it is the same book with the dial turned past the cap.

**A by-product worth recording:** `band3-rw` at **g = 0.75** is also **6 of 6** and carries a
*wider* broad drawdown margin than the incumbent (+0.0170 vs +0.0083 at 10 bps), though the
incumbent beats it on broad CAGR and Sharpe (12.86% / 1.1381 / −19.41%, OOS 1.1231 vs 11.73% /
1.0690 / −18.53%, OOS 1.0760). So the salvageable form of idea 57's `ew-band3` is
**`rw` at 0.75, not `dg` and not 0.85** — and per idea 144 a re-dialled book is the same book,
so this is recorded, not proposed. No RULES change, no promotion, no memo.

## Q3 — how much of idea 90's ceiling was resolution

Mean |ceiling moved by the 5× finer grid| = **0.0113** of realised gross over 21 non-empty
cells (one coarse step ≈ 0.0375, one fine step ≈ 0.0075), i.e. **about 1.5 fine steps, never
more than 4**. The largest moves are `band3-rw` broad@10bps (+0.0300, the contested number),
`band3-rw` u56@25 (+0.0300) and `vol60-rw` u56@25 (+0.0300); `band3-dg` and several u56 cells
do not move at all. **Any published gross ceiling read off a 0.05 grid should be quoted with a
±0.03 band, and none of them should be compared to a target closer than that.** Idea 84's
0.85 clears that band on broad by 3–5 fine steps, so the KILL survives the correction.

## Q4 — rule 8 (interval read on 2009–2016 only, 2017–2026 read once)

Gross carries **no out-of-sample Sharpe content whatsoever**, on any arm or panel. The IS
interval's midpoint beats the do-nothing control (m = 1.00) by **+0.0000 mean OOS Sharpe over
19 non-empty cells**; the plain IS-Sharpe argmax gives **−0.0007**, winning 11.1% of 36 cells.
Best and worst individual deltas are +0.0009 and −0.0010. This is idea 66's "gross is an exact
lever with zero Sharpe content", now with a rule-8 stamp on it: **no in-sample gross-selection
rule can be worth writing into RULES.** Reference OOS levels at 10 bps: u56 `band3-rw` @0.75
1.2025 / `vol60-dg` @0.75 1.1857; broad `band3-rw` 1.0760 / `vol60-dg` 1.1222; small
`band3-rw` 0.5750 / `vol60-dg` 0.3045; RULES v1 baseline (full-sample Sharpe at 10 bps) u56
0.6642, broad 0.6350, small 0.6027; **SPY OOS 0.8820, full 15.23% / −33.72%, H1 0.957 /
H2 0.834**.

## Q5 — KEEP paths over all 5,808 rows

4b **578 / 5808**, 4a **3296 / 5808**. By panel: u56 354, broad 224, **small 0**. The 4b
failing-bar census is dominated by the **CAGR floor (2814 rows)** — the low-gross end of every
ladder — with DD-only failures at the high end (480). Highest-Sharpe 4b point at PROTOCOL's
10 bps on each large-cap panel: u56 `band3-dg` m=1.23 g=0.6552 (CAGR 10.68%, Sharpe 1.2055,
MaxDD −14.72%, OOS 1.2846, 2.2×/yr) and broad `vol60-dg` m=0.87 g=0.6294 (CAGR 10.74%, Sharpe
1.1382, MaxDD −16.37%, OOS 1.1231, 1.2×/yr). Neither is a new book and neither is cross-
universe: the u56 winner is the arm that is EMPTY on broad, and both sit on the CAGR floor
(margins **+0.0002** and **+0.0008** of CAGR) where a single bad year would evict them.

**Caveats.** Survivorship (idea 54): all three panels are current-constituent lists, which
flatters every long book here; the small panel additionally drops 44 names on `max_1d_move ≥
1.0`, a data screen and not a tradable rule. Idea 128: the IS window's SPY MaxDD is shallower
than the OOS window's, so every IS drawdown cap in Q4 admits too much. Costs are flat linear
bps on turnover, not spread-and-impact (idea 126). Two tuned parameters only — the gross dial
m and the cost rung; convention, arm and panel are reported axes and all appear at every point;
the 4b bar coefficients are PROTOCOL's published 0.70 / 0.60 and were not swept.

**Reproduction.** `python research/backtests/2026-09-06_ew-band3-at-085-does-not-hold-on-broad_cloud.py`
(373 s, 5,808 rows). Console in `.console.txt`, grid in `.grid.csv`, intervals in
`.intervals.csv`, the two contested points in `.verdict.csv`, rule 8 in `.walkforward.csv`.

**Follow-ups for the queue:** (236) re-quote every published gross ceiling in the record with
the ±0.03 coarse-grid band this run measures, and flag the ones whose verdict flips inside it;
(237) the `dg` reachability ceiling — for every gate the project uses, publish the maximum
realised gross the de-grossed form can attain at m = 1.30, since a target above it is not a
failing arm but an undefined one; (238) `band3-rw` at g = 0.75 is 6 of 6 with a wider broad DD
margin than the incumbent but lower CAGR and Sharpe — put the two head to head on idea 65's
cadence-insensitivity bar and idea 45's execution-lag test before either is called the safer
book.
