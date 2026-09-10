# Idea 658 — publish p and n beside every WIDE flag in the record (cloud, 2026-09-10)

**KILL: the record's `wide_design_hint` flag carries no information about design width, and
design width carries no information about book quality. No RULES change, no book promoted, no
KEEP; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.** Two tuned parameters
and no more (CENSUSSET ∈ {COMMITTED, ALL}, WIDTHBAR ∈ {0.05, 0.10, 0.25, 0.50, 1.00}); panel,
cost rung, book form, ridge penalty, window length and forecast width are reported axes, never
chosen. Every grid point written to disk.

## Gates

* **G1** `fast_backtest` vs `engine.backtest` on the read window: returns **0.000e+00**,
  turnover **0.000e+00**. (The engine emits 2 NaN returns before warm-up, both at index < 260
  and outside every window read below.)
* **G2** the committed width-flag counts reproduce: idea 484's census **7** (published 7),
  idea 483's census **5** (published 5).
* **G5** no committed (tracked) file touched across the re-execution of PART B:
  `git status --untracked-files=no` identical before and after — **PASS**.
* **G3** is reported in the console for what it is; see §B.

## A. The census

3,155 committed CSV artefacts and 666 committed prose files scanned.

| | COMMITTED | ALL (+ prose) |
|---|---|---|
| width-flag sites | **30** (over 3 census files) | **42** |
| distinct named `.py` files | **18** | **18** |

## B. The runtime (p, n) — the table the queue asked the record to publish

Every named file was re-executed in a subprocess with `np.linalg.lstsq / pinv / solve` and
`np.polyfit` instrumented, every write inside the repo redirected to a scratch tree (G5), and
every fit call journalled per-call so a file that exceeds the 900 s budget still publishes what
it reached. **32 fit sites** are published with their p, their n and their per-call p/n — a
site's p/n is always maximised over that site's own calls, never `max(p)/min(n)` across
different fits, which could only overstate it.

**The measured spread is the finding.** Across the sites the flag calls "wide", the actual
design width runs from **p = 2 on n = 11,968 (p/n = 0.0002)** — the pool-mean file, four
orders of magnitude from anything that could overfit — to **p = 179 on n = 8 (p/n = 0.9853)**
and **p = 439 on n = 15..900 (p/n = 0.9877)**. One boolean is standing in for a quantity that
varies by a factor of about 5,000 across the very files it flags.

**12 of 30 committed sites cannot be measured at all** (`p_source` = halted / ast / unresolved):
the file halts on its own reproduction gate before reaching a fit, or does not reach one inside
the budget. Where re-execution reaches no fit, p is resolved statically by AST and n is
published as unknown rather than imputed. **That 40% of the record's own flagged sites can no
longer be executed to their fit is itself an answer about the record**, and it is why the
re-score below reports `measured` and `unmeasured` in every row.

**G3, idea 497's headline.** 497 reported that its three wide-and-unfolded files top out at
p = 6 on n = 162 (p/n 0.0370). It rebuilt those designs from committed artefacts rather than
re-executing them. Re-executing: two of the three halt on their own reproduction gates before
any fit, and the third (`does-the-cash-drag-share…`) reaches its `pinv` site only at the larger
budget, where it gives **p = 7 on n = 27..162, max per-call p/n 0.0741**. The p differs by the
intercept column (497 counts it out, this run counts it in) and the n by which sub-cell is read.
**497's conclusion — these three are not wide — survives this run intact and is if anything
understated**; what does not survive is the flag that put them in the population.

## The re-score — how many 'wide' labels survive?

All grid points (CENSUSSET × WIDTHBAR):

| CENSUSSET | p/n bar | sites | measured | unmeasured | survive | survive rate | files surviving |
|---|---|---|---|---|---|---|---|
| COMMITTED | 0.05 | 30 | 18 | 12 | 12 | 0.667 | 9 / 18 |
| COMMITTED | **0.10** | 30 | 18 | 12 | **9** | **0.500** | 6 / 18 |
| COMMITTED | 0.25 | 30 | 18 | 12 | 8 | 0.444 | 5 / 18 |
| COMMITTED | 0.50 | 30 | 18 | 12 | 8 | 0.444 | 5 / 18 |
| COMMITTED | **1.00** | 30 | 18 | 12 | **0** | **0.000** | 0 / 18 |
| ALL | 0.05 | 42 | 30 | 12 | 24 | 0.800 | 9 / 18 |
| ALL | 0.10 | 42 | 30 | 12 | 14 | 0.467 | 6 / 18 |
| ALL | 0.25 | 42 | 30 | 12 | 13 | 0.433 | 5 / 18 |
| ALL | 0.50 | 42 | 30 | 12 | 13 | 0.433 | 5 / 18 |
| ALL | 1.00 | 42 | 30 | 12 | 0 | 0.000 | 0 / 18 |

**At any bar a statistician would recognise, the flag is a coin flip** (exactly 50% of measured
COMMITTED labels at p/n ≥ 0.10, 44% at 0.25 and 0.50 — the flagged population has almost no
mass in between). **Not one site anywhere in the record reaches p ≥ n.**

**Rule 8, census leg.** WIDTHBAR chosen on the first half of the record by file date (split
2026-09-09, H1 29 sites / H2 13 sites), read once on the second half: the IS-maximising bar is
**0.05**, and its OOS survive rate is **0.9231 (12 of 13 measured)** against 0.7059 in sample.
The chosen bar does travel — but it travels to the *lowest* rung on the ladder, i.e. the bar
that flags almost everything, which is the same as having no bar.

## C. Does design width predict OOS book quality? No.

A width flag is a warning that a wide design overfits. That is a statement about books, so it
was tested on books. On each panel a weekly cross-sectional ridge forecast was fitted on a
rolling window of L weeks × N names (n = L·N rows) with p lagged-weekly-return predictors, and
the top-20 equal-weight book (the 2026-09-04 KEEP 4b form: no vol scaler, gross 1.00) held on
the forecast. p ∈ {1,2,4,8,16,32,64} × L ∈ {4,13,52,104} × lam ∈ {0.01,0.1,1.0} × 3 panels ×
3 cost rungs = **756 arm-rungs, all reported**; p/n spans 0.00003..0.29806.

**Spearman(p/n, OOS Sharpe): U56 −0.1453, B136 +0.0565, SMALL439 −0.6155, POOLED +0.0283.**
The sign is not even stable across panels, and the pooled statistic is indistinguishable from
zero. The IS-minus-OOS gap tells the same story: +0.3735 / −0.0407 / +0.6276, POOLED +0.1917.
**Within the range of widths the record actually contains, p/n does not order books.**

**Both KEEP paths: 4a 0/252, 4b 0/252, BOTH 0 — at 0, 10 and 25 bps, on all three panels.**
These are honestly bad books and the reason is turnover, not width: median **80.3 turns per
year** (range 55.3..93.4), so at 10 bps the form pays ~8%/yr in costs before it does anything.
Best arm at 10 bps is U56 p=2 L=4 lam=0.01: 14.1% / 0.877 / −31.0%, halves 0.79 / 0.96, against
RULES v2 8.63% / 1.2021 / −12.05% and SPY 15.15% / 0.8855 / −33.72%.

**Rule 8, book leg** ((p, L) chosen on 2009–2016 by IS Sharpe, 2017–2026 read once):
**beats RULES v2 OOS 0/9, beats SPY OOS 0/9, 4a 0/9, 4b 0/9**, regret against the hindsight-best
(p, L) of −0.065 to −0.447. The IS-chosen widths are p ∈ {1, 32}, L ∈ {4, 13}, p/n
0.00466..0.01898 — the selector does not choose narrow designs, which is the last thing that
would have rescued the flag.

## Proposal filed for the Sunday review, NOT adopted here

Retire `wide_design_hint` as a published column. A census that wants to say a design is wide must
publish that design's **p and its n** at the site it names — the instrumented re-execution used
here costs about a minute per file and produces the table in §B — and must say when it could not
measure them, which was 14 of 30 sites. Where a single number is wanted, it should not be a
boolean and it should not be p/n alone: §C shows p/n does not order books over the range the
record occupies, which is consistent with idea 498's independent finding that p/n is not the axis.

## Caveats

**DETERMINISM.** A file that exceeds the 900 s probe budget publishes what it reached inside it,
so for a timed-out file the fit-call **count** is machine-dependent and its (p, n) coverage is a
**lower bound**. The re-score turns only on each site's max p and min n, which are reached in
the first seconds of the fitting loops and were identical across runs at two budgets (1800 s and
900 s); the counts differ between those runs and are published as-is. The larger budget reaches
two extra files' fits, which is why §B quotes it for G3.

**SELF-REFERENCE.** The census reads the committed record as of this run, which by now includes
this sprint's own earlier artefact (idea 496's memo and lane B's idea-496 census, itself carrying
a `wide_design_hint` column). That is the record, so they are counted; they are named in
`.sites.csv` and a reader can exclude them.

**SURVIVORSHIP (PROTOCOL 9).** U56 and B136 are current-constituent lists; SMALL439 is the
sub-$2B screen with `data/small_meta.csv max_1d_move ≥ 1.0` dropped (44 tickers, idea 118), also
current constituents and back-filled only to 2010. Every level in §C is optimistic and none is a
tradable estimate. What is meant to survive is the within-panel contrast (p vs p, L vs L on the
same panel and window, read off identical books) and the census arithmetic in §A/§B, which is a
property of committed files and carries no survivorship at all. Ideas 38, 54 and 126 also apply.

Script `research/backtests/2026-09-10_publish-p-and-n-beside-every-WIDE-flag-in-the-record_cloud.py`;
artefacts `.sites.csv`, `.sites_pn.csv`, `.probe.csv`, `.joint.csv`, `.grid.csv`,
`.keeppaths.csv`, `.walkforward.csv`, `.console.txt`.
