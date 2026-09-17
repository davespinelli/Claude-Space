# Idea 1156 (lane cloud, 2026-09-17) — can a SPLIT-HALF claim be made REGIME-CHECKABLE without a THIRD TAPE?

**ANSWERED = NO. NO CHEAP REPAIR SERVES, AND THE TWO CHEAPEST CANNOT EVEN BE ASKED THE
QUESTION.** Scored in the pre-declared order the outcome is **(D) NEITHER**: the record's
committed split-half rows are **not repairable in place** — they need re-running on a
fraction ladder or they need withdrawing. Verdict **KILL** as a capital finding (4a 0 of 81
rung books, and the single 4b-passing pick out of 18 is the standing anchor book, not a new
candidate) and **KILL** as a schema finding.

No RULES change, no book promoted, no PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`,
`engine.py`, `scan.py`, `bot.py` and `baseline.py` untouched.

SELECTION: this lane takes the LAST eligible open idea; 1156 stood last under `## Open` and
is not EDGAR / Form 4 / 8-K / options / spin-off / live-data.

## The two dials and no more (rule 4 — and the queue names both)
`REPAIR` {P_HALF, P_OVERLAP, P_QUARTERS, P_BLOCK} × `STATISTIC` {CAGR, VOL, SHARPE, MAXDD,
ULCER, CALMAR} = **24 cells, every one published** at every one of the 81 rung books —
1,944 rows in `.grid.csv`.

| repair | segments | lengths | what it is |
|---|---|---|---|
| P_HALF | 2 | n/2 | the status quo |
| P_OVERLAP | 3 | n/2 | half-length windows at tape offsets 0, 1/4, 1/2 — the falsification control |
| P_QUARTERS | 6 | n/2, n/4 | halves plus quarters |
| P_BLOCK | 8 | n/2, n/6 | halves plus 3 blocks inside each half (the queue's "within-half block spread as the regime term") |
| **P_FULL** *(reference, not a dial value)* | **29** | **six** | 1158's committed resolved target: the count-matched ratio on the finest fraction ladder L8 = {1,2,3,4,5,6,8} |

NOT dials: PANEL {U56, B136, SMALL}; the four dial ladders that are the grid's books
(CADENCE, GROSS, H, N = 27 rung books per panel, 81 total, 1148's grid); the WITHIN
statistic (count-matched all-pairs mean |difference|, 1158's); the census; the rule-8
choosers. Tape PINNED at 2026-09-15.

## (1) 1148's PREMISE, PROVED AS ARITHMETIC RATHER THAN ASSERTED (gate G6)

Distinct sub-tape **lengths** yielded, measured on every one of the 81 books:

`P_HALF [1] · P_OVERLAP [1] · P_QUARTERS [2] · P_BLOCK [2] · P_FULL [7]`

**P_HALF and P_OVERLAP yield exactly one length on all 81 books, so their BETWEEN term is a
contrast over a single point and is undefined — 486 of 486 cells, by construction, not by
sample.** Their ratio column is NaN throughout and is printed as `undef`; the run does not
hide the undefinedness behind a number.

**The falsification control behaved as pre-declared.** P_OVERLAP triples the number of
segments and buys real resolution in the WITHIN term — and buys **nothing at all** in the
BETWEEN term, because three windows of the same length are still one length. Publishing
more halves is not a repair. Outcome (E) did not fire.

## (2) THE TWO SATISFIABLE REPAIRS DO NOT LAND

Landing := |r_repair − r_FULL| / |r_FULL| ≤ 0.25 (1158's bar, verbatim), over 486 (panel ×
book × statistic) cells:

| repair | cost | satisfiable | LANDS | rate | median gap | median ratio | median ref |
|---|---|---|---|---|---|---|---|
| P_HALF | 2 | 0/486 | 0 | 0.000 | undef | undef | 3.6219 |
| P_OVERLAP | 3 | 0/486 | 0 | 0.000 | undef | undef | 3.6219 |
| P_QUARTERS | 6 | 486/486 | 135 | **0.278** | 0.4425 | 4.3719 | 3.6219 |
| P_BLOCK | 8 | 486/486 | 198 | **0.407** | 0.3423 | 4.5781 | 3.6219 |

Both are well under the 0.5 majority bar, and both read **high** — the cheap segmentations
systematically overstate the ratio (median 4.37 and 4.58 against the reference's 3.62),
because a two-length contrast is a smaller BETWEEN term than a six-length one.

**One statistic is the exception and it is the headline one.** Landing rate by statistic:

| stat | P_QUARTERS | P_BLOCK |
|---|---|---|
| CAGR | 0.173 | 0.444 |
| VOL | 0.123 | 0.309 |
| SHARPE | 0.123 | 0.309 |
| **MAXDD** | 0.469 | **0.728** |
| ULCER | 0.407 | 0.556 |
| CALMAR | 0.370 | 0.099 |

**P_BLOCK lands on MAXDD at 0.728 and on nothing else above 0.556**, and it is *worst of all
four* on CALMAR (0.099). A clause of the form "a split-half MAXDD claim may be repaired with
a within-half block spread" is the only wording this grid supports, and it is a
statistic-specific clause, not the general one the queue asked about.

## (3) AND THEY DO NOT *ORDER* — the leg that decides capital

A cheap repair earns its place only if it **ranks books** the way the expensive one does.
Spearman rho across each (panel, statistic) cell's 27 rung books, repair vs P_FULL:

| repair | ORDERS (rho ≥ 0.50) | rate | median rho |
|---|---|---|---|
| P_HALF | 0/18 | 0.000 | undef |
| P_OVERLAP | 0/18 | 0.000 | undef |
| P_QUARTERS | **0/18** | 0.000 | **0.2376** |
| P_BLOCK | **4/18** | 0.222 | **0.3641** |

P_QUARTERS clears the bar at **not one of the eighteen cells**. P_BLOCK clears four and is
sign-unstable across them: B136/CAGR **+0.905** against U56/CALMAR **−0.628** and
U56/SHARPE **−0.252**. A repair that ranks books backwards at some cells and forwards at
others is not a cheap version of the full re-run; it is a different measurement.

## (4) SERVES — all three legs, majority on each

| repair | cost | SATISFIABLE | LANDS majority | ORDERS majority | **SERVES** |
|---|---|---|---|---|---|
| P_HALF | 2 | NO | no | no | **NO** |
| P_OVERLAP | 3 | NO | no | no | **NO** |
| P_QUARTERS | 6 | YES | no | no | **NO** |
| P_BLOCK | 8 | YES | no | no | **NO** |

**OUTCOME (D) NEITHER.** A split-half claim cannot be made regime-checkable without the
third tape.

## (5) THE CENSUS — how much of the record this covers

1,608 committed CSVs in `research/backtests` carry a split-half column pair
(`H1`/`H2`, `IS_*`/`OOS_*`, `first_half`/`second_half`), **1,822,671 rows in all**. Of those
files, **41 (0.0255)** carry any column with ≥ 2 distinct sub-tape lengths and could price
the length axis in place; **1,567 files covering 1,752,420 rows cannot.** 1148 committed
"0 of 2,140,569"; this run's file set and its column test are its own, so the figure is
published **beside** 1148's, not substituted for it — and it is the more generous of the
two (it finds 41 files 1148's test did not credit, and still leaves 96.1% of the rows
unrepairable).

## (6) RULE 8 AND BOTH KEEP PATHS — 81 rung books, 18 picks, all published

Parameters chosen on 2009-2016 only; 2017-2026 read once. 10 bps, next-day execution.

Benchmarks (pinned tape, post-warm-up): **SPY** U56 15.10% / 0.8829 / −33.72% (halves
0.9588/0.8207), OOS 15.21% / 0.8711 / −33.72%. **LIVE RULES v2** U56 8.62% / 1.2008 /
−12.05%, OOS 9.46% / 1.2763; B136 7.98% / 1.0993 / −12.24%; SMALL 4.30% / 0.6637 / −13.89%.

**4a: 0 of 81 rung books and 0 of 18 picks.** 4b full 16 of 81, 4b OOS 17, BOTH 15
(U56 10/27, B136 6/27, **SMALL 0/27 on every path**) — the same grid and the same counts as
idea 1187's run today, as it must be, since the books are identical.

**An unsatisfiable repair silently becomes no repair at all.** `CH_P_HALF` and
`CH_P_OVERLAP` have no ratio to minimise, so they fall back to IS Sharpe and pick **exactly
what `CH_ISSHARPE` picks at 3 of 3 panels** (U56 N=40, B136 N=8, SMALL H=252). Publishing a
split-half "regime check" beside a book selection is operationally indistinguishable from
not doing one.

**A cheap repair's chooser agrees with the expensive one at 0 of 12 (panel, repair) cells.**
`CH_P_FULL` picks N=10 / N=5 / N=25; `CH_P_QUARTERS` picks N=5 / H=63 / CADENCE=M;
`CH_P_BLOCK` picks CADENCE=W / H=63 / N=30. The repair choice is a live capital fork and
never lands where the reference does.

**1 of 18 picks passes 4b (full and OOS) and it is not a new candidate**: U56 `CH_P_BLOCK`
picks `CADENCE=W`, which *is* the standing anchor book N=20 / H=126 / gross 0.75 / weekly
(15.58% / 1.1397 / −19.13%, OOS 16.97% / 1.1644 / −19.13%) — 936's book, already the
record's incumbent, reached here by a route that agrees with nothing else. It fails 4a.

## Gates — 8 of 8 PASS
G1 fast runner ≡ `engine.backtest` (1.39e-17). G2 committed U56 W/H126/N=20 triple
(4.12e-05). G3 committed SPY OOS triple (1.70e-04). G4 live RULES v2 MaxDD ≡ −12.05%
(4.95e-05). G5 1157/1158's committed full-tape MaxDD levels on all three panels (7.17e-06).
**G6 1148's premise as arithmetic — P_HALF and P_OVERLAP yield exactly one length on all 81
books (dev 0.000e+00).** **G7 1158/1187's committed SMALL/MAXDD resolved target 1.173714
lies inside this run's per-book P_FULL range [1.1147, 1.5473]** — published as an interval
and *not* asserted as an equality, because 1158 pooled all four ladders' books before taking
medians while this run reads one book at a time; the cell is a superset check and is labelled
as one. G8 the segmentation and every ratio deterministic over 648 re-reads (0.000e+00).

THE VINTAGE, PUBLISHED NOT ABSORBED: G2/G3 on the UNPINNED file read 1.62e-03 and 2.89e-03.

## Survivorship
The SMALL panel is current constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`): `data/small_meta.csv` lists 715 tickers, **52 dropped** for
`max_1d_move >= 1.0`, **663 names + SPY served** over 4,198 bars (2010-01-04 .. 2026-09-11).
Its levels are **optimistic** and every 4a/4b count on it is an **UPPER bound** — which
makes SMALL's 0/27 on every path the one count here that needs no discount.
