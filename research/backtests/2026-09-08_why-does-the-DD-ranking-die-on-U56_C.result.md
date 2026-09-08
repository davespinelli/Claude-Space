# Idea 422 — why does the DD ranking die on U56?  (lane C, 2026-09-08)

**VERDICT: ANSWERED — the queue's PREMISE is FALSIFIED. The DD ranking does not die on U56.
The `+0.051 (t +0.45, ns)` is a PANEL-LABEL partition artefact of idea 420's harvested census,
not a panel fact. On fresh prices, under idea 420's own construction, u56's within-cell MaxDD
transfer slope is +1.713 against broad136's +1.693 — the two panels are indistinguishable.**
No book promoted; no new KEEP candidate.

Script: `2026-09-08_why-does-the-DD-ranking-die-on-U56_C.py`
Outputs: `.grid.csv` (6,138 arm-rows, 198 cells, 66 panels), `.transfer.csv`, `.provenance.csv`, `.decomp.csv`,
`.cellslopes.csv`, `.walkforward.csv`, `.keeppaths.csv`, `.feasibility.csv`, `.console.txt`.

---

## 0. Where the +0.051 comes from (idea 420's committed CSVs, re-read)

Idea 420 split its census by the `panel` string each parent file happened to write. Those
strings are not panels — the 56-name universe appears under three spellings and the 136-name
universe under five:

| canonical panel | label spellings | census rows | fitted n | cells | slope | R2 | t | p |
|---|---|---|---|---|---|---|---|---|
| u56(56) | `U56`, `u56`, `universe.json(56)` | 9,687 | 6,822 | 833 | **+0.760** | 0.371 | **+3.135** | **0.002** |
| broad136 | `B136`,`BROAD136`,`broad`,`broad136`,`universe_broad(136)` | 9,638 | 6,867 | 818 | +1.039 | 0.484 | +7.222 | 0.000 |

The queue's `U56 +0.051` row is the **uppercase spelling only**: 242 fitted rows over 9 cells
from 17 files — **2.5% of that panel's 9,687 census rows**. The lowercase `u56` spelling of the
same panel, 6,580 rows, gives **+0.864 (t +3.15)**. Merging the spellings, the 56-name panel's
drawdown ranking is positive and significant at p = 0.002. **The contrast the idea was built on
is a partition of file-naming conventions.**

## 1. Reproduction on fresh prices (the queue's two panels, identical construction)

31-arm menu (ungated control + band x gross x cadence), IS <= 2016-12-31, OOS >= 2017-01-01,
rungs 0/10/25 bps. SPY held investable and held out, because idea 420's fresh grid kept it
investable on these two panels and the sub-panels below never do:

| panel | n | cells | slope | R2 | mean rho | top-quartile hit | level shift | frac worse | level ratio |
|---|---|---|---|---|---|---|---|---|---|
| u56 (SPY investable) | 93 | 3 | **+1.713** | 0.900 | 0.938 | 0.857 | -5.4 pp | 1.000 | 1.627 |
| u56 (ex-SPY) | 93 | 3 | **+1.719** | 0.906 | 0.949 | 0.857 | -5.4 pp | 1.000 | 1.633 |
| broad136 (SPY investable) | 93 | 3 | +1.693 | 0.919 | 0.955 | 0.857 | -6.1 pp | 1.000 | 1.719 |
| broad136 (ex-SPY) | 93 | 3 | +1.692 | 0.919 | 0.951 | 0.857 | -6.1 pp | 1.000 | 1.720 |

Per rung, u56 gives +1.739 / +1.719 / +1.683 at 0 / 10 / 25 bps against broad136's +1.698 /
+1.695 / +1.686. **There is no U56 deficit at any rung, and SPY's investability is worth
0.006 of slope.** (These levels sit above the census's ~1.0 because the 31-arm menu's
within-cell variance is mostly a gross dial, which scales drawdown near-linearly — the same
1.5x optimism idea 420 measured as `level_ratio`. Both panels are priced on the same menu, so
the comparison is fair; the LEVEL is menu-specific.)

## 2. The two tuned parameters, all 16 grid points (12 feasible)

Pool = 35 ETFs + 100 stocks from `universe_broad.json` (SPY is the benchmark, never
investable). `e` = target ETF share, `k` = name count, 6 seeds per point, 3 rungs;
one cell = one sub-panel x one rung, 31 arms. Infeasible points are the ones the ETF sleeve
cannot fill (`round(k*e) > 35`) and are reported as infeasible, not dropped.

**Within-cell MaxDD transfer slope:**

| e \ k | 20 | 35 | 56 | 100 |
|---|---|---|---|---|
| 0.00 (all stock) | +1.644 | +1.565 | +1.670 | +1.651 |
| 0.35 | +1.506 | +1.576 | +1.689 | +1.704 |
| 0.65 (U56's share) | +1.539 | +1.547 | infeasible | infeasible |
| 1.00 (all ETF) | **+1.384** | +1.566 | infeasible | infeasible |

**Top-quartile hit rate (base 0.25):**

| e \ k | 20 | 35 | 56 | 100 |
|---|---|---|---|---|
| 0.00 | 0.817 | 0.865 | 0.881 | 0.857 |
| 0.35 | 0.802 | 0.881 | 0.873 | 0.952 |
| 0.65 | 0.746 | 0.802 | — | — |
| 1.00 | **0.675** | 0.762 | — | — |

Pooled per-cell slopes give two clean, monotone ladders:

* by ETF share: **1.646 (e=0) / 1.628 / 1.560 / 1.452 (e=1)** — n = 57/72/36/21
* by name count: **1.549 (k=20) / 1.573 / 1.689 / 1.701 (k=100)** — n = 72/57/36/21

`per-cell slope ~ e + k`, clustered on sub-panel, n = 186 cells: **b_e = -0.142 (t -1.94)**,
**b_k = +0.0018/name (t +2.69)**, R2 0.170. On the 12 scope-level slopes: e alone R2 0.409,
k alone R2 0.467, both R2 0.639.

**Reading: both candidate dials are real and both point the way the idea guessed — an
all-ETF panel ranks drawdown worse (hit 0.675 vs 0.817 at k=20) and a wider panel ranks it
better — but the whole span of the surface is 1.38 to 1.70. Neither dial, nor both together,
can produce a slope near zero. They cannot explain a gap that does not exist.**

Note the design's own limit: at U56's actual composition (36 of 56 ETFs) the ETF sleeve is
nearly exhausted, so `e=0.65, k=56` is unbuildable from the pool — U56 is, up to the choice of
20 stocks, the *only* panel of its shape. The `e` and `k` dials are therefore partially
confounded at the top-right of the grid, and the ETF-only column stops at k=35.

## 3. Episode structure — 2020 is load-bearing everywhere, not on U56 specially

OOS drawdown recomputed with each episode's returns spliced out:

| scope | full | ex-2020 | ex-2022 | ex-both |
|---|---|---|---|---|
| all grid sub-panels | +1.584 | **+0.949** | +1.585 | +0.822 |
| REF u56 (ex-SPY) | +1.719 | **+1.189** | +1.719 | +0.967 |
| REF broad136 (ex-SPY) | +1.692 | **+0.939** | +1.692 | +0.840 |

Excising 2020-02-15..2020-05-31 removes ~40% of the transfer slope on every panel; excising
2022 removes **nothing** (1.584 -> 1.585, third decimal). The 2017-2026 drawdown ranking is a
COVID-crash ranking. That is a record-wide fact about the OOS window, and it is *weakest* on
u56 (1.189 surviving vs broad's 0.939) — the opposite of the queue's direction. It bears
directly on idea 321's warning that a 4b drawdown margin can be one episode's coin flip.

## 4. Rule 8 walk-forward (parameters chosen on the IS window only, read on 2017-01-01..)

Selectors: the instrument under test (IS-MaxDD argmax = shallowest in-sample drawdown), the
incumbent (IS-Sharpe argmax), the ungated control, and an OOS oracle as a ceiling.
`d_ORACLE` = the pick's OOS MaxDD minus the OOS-shallowest arm's (0 = the IS pick found it).

Reference panels, 10 bps:

| panel | selector | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | d_ORACLE | 4a_oos | 4b_oos |
|---|---|---|---|---|---|---|---|---|
| u56 (ex-SPY) | IS_MaxDD | b0.015-g0.50-M | 6.36% | 1.2639 | -8.67% | -0.67 pp | no | no |
| u56 (ex-SPY) | IS_Sharpe | b0-g1.00-M | 12.78% | 1.2832 | -15.54% | -7.55 pp | no | **yes** |
| u56 (ex-SPY) | control | control | 18.53% | 1.1399 | -29.10% | -21.1 pp | no | no |
| broad136 (ex-SPY) | IS_MaxDD | b0.015-g0.50-W | 5.30% | 1.1333 | -8.33% | -0.13 pp | no | no |
| broad136 (ex-SPY) | IS_Sharpe | control | 18.62% | 1.1022 | -32.71% | -24.5 pp | no | no |

Comparands on the same OOS window: **SPY 15.45% / 0.8820 / -33.72%**; RULES v2 on u56
1.2942 / -11.90%, on broad136 1.1206 / -12.18%.

Grid sub-panels, mean over 62 sub-panels per rung:

| rung | selector | OOS CAGR | OOS Sharpe | OOS MaxDD | d_ORACLE | 4a_oos | 4b_oos |
|---|---|---|---|---|---|---|---|
| 0 bps | IS_MaxDD | 5.23% | 1.0647 | -8.47% | **-0.67 pp** | 0.694 | 0.000 |
| 0 bps | IS_Sharpe | 15.30% | 1.0769 | -26.02% | -18.2 pp | 0.000 | 0.161 |
| 10 bps | IS_MaxDD | 5.11% | 1.0407 | -8.47% | **-0.63 pp** | 0.258 | 0.000 |
| 10 bps | IS_Sharpe | 15.24% | 1.0633 | -26.34% | -18.5 pp | 0.000 | 0.129 |
| 25 bps | IS_MaxDD | 4.93% | 1.0045 | -8.57% | **-0.65 pp** | 0.065 | 0.000 |
| 25 bps | IS_Sharpe | 16.03% | 1.0396 | -29.13% | -21.2 pp | 0.000 | 0.032 |

**The IS drawdown ranking is not merely orderable, it is nearly oracle-exact: across 62
sub-panels and 3 rungs the IS-MaxDD argmax lands within 0.63-0.67 pp of the OOS-shallowest arm
in the menu.** It works on U56 (-0.67 pp) as well as on broad136 (-0.13 pp) and on every ETF
share (-1.28 pp at e=0.65 k=20 down to -0.16 pp at e=1.00 k=20). What it does NOT do is
produce a capital-worthy book: the shallowest-drawdown arm earns 5.1% against SPY's 15.45%
and **fails 4b in 62 of 62 sub-panels at every rung** (the CAGR floor, as ideas 330/334 keep
finding). 4a_oos passes in 25.8% of sub-panels at 10 bps and collapses to 6.5% at 25 bps.

The only 4b_oos pass among the reference rows is the IS-Sharpe pick on u56 —
12.78% / 1.2832 / -15.54% — which is idea 420's already-committed by-product
(12.72% / 1.2750 / -15.49%) reproduced under a different baseline construction. **Nothing new
is promoted here.** Over all 792 walk-forward rows: 4a 168, 4b 33, 4a_oos 146, 4b_oos 26.

## 5. What the record should take from this

1. **The premise of idea 422 is void, and so is the fear behind idea 421's U56 column.** The
   56-name panel's IS drawdown ranking transfers at +0.760 (census, p 0.002) and +1.71
   (fresh grid). PROTOCOL's IS-window DD cap is enforceable on U56.
2. **A panel label in a harvested census is not a panel.** Idea 420's per-panel split
   partitioned 19,401 rows by free-text `panel` strings; two spellings of one universe gave
   +0.051 and +0.864. Any census that splits by a discovered label column should canonicalise
   first and report the label -> panel map. This is the second published claim (after idea
   410's) that turns out to be a corpus statement wearing a panel's name.
3. **Real but small:** ETF share depresses the drawdown ranking (-0.142 slope per unit share,
   t -1.94; quartile hit 0.817 -> 0.675 from all-stock to all-ETF at k=20) and name count
   raises it (+0.0018/name, t +2.69). Worth quoting beside a transfer slope; not worth a rule.
4. **2020 carries ~40% of the whole OOS drawdown ranking and 2022 carries none.** Any 4b
   drawdown verdict on the 2017-2026 window is largely a statement about one quarter.

PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py were not modified.
