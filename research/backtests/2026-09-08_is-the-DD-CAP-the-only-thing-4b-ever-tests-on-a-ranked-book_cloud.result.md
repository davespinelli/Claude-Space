# Idea 459 — is-the-DD-CAP-the-only-thing-4b-ever-tests-on-a-ranked-book (cloud, 2026-09-08)

**SPLIT. The queue's statistic REPLICATES — on a ranked book that clears 4b, the DD cap is what it
clears on, and the Sharpe excess over its own un-ranked control is ~zero or negative. The queue's
implied reading — "the DD cap is the only thing 4b tests" — is FALSIFIED: on the un-ranked control
the CAGR floor binds just as hard, from the opposite side of the same gross dial, and the two bars
are jointly INFEASIBLE on all three panels. No RULES change, no book promoted, no KEEP claimed;
RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.**

Gates first, all PASS: `fast_bt` vs `engine.backtest` on returns AND turnover **0.000e+00**; the
cost-rung identity `net(25) = net(0) − turnover·25/1e4` vs a live `backtest(cost_bps=25)`
**0.000e+00**; TOP-n nests `baseline.rules_v1_weights` (n=5, g=0.75) at **0.000e+00**; the EWALL
control nests RULES v2's un-ranked weighting off its band gate at **0.000e+00**.

## PART A — census of the committed record (read, never re-simulated)

2,002 committed CSVs scanned (this run's own outputs excluded); **447 carry a machine 4b verdict
column, 148 also a fail-reason column; 547,717 rows, 81,571 4b PASSES (14.9%)**. Of the passes,
3,835 are classifiable RANKED and 6,245 UN-RANKED from their own labels; **71,491 are UNKNOWN and
are counted, never guessed** — that is the census's real limit, and it is published, not hidden.
LEADERBOARD.md prose, counted coarsely and labelled as coarse: 3,732 table rows, 2,154 name 4b,
457 claim a 4b PASS/KEEP, of which 153 (33%) also name an un-ranked control.

- **Coverage (P1 HIT).** Of 3,706 ranked passes in machine-comparable files, only **1,833 (49.5%)
  have a matched un-ranked control at the same panel/gross/cost inside their own file**. Half the
  record's ranked 4b passes cannot be checked against a control at all.
- **The queue's statistic (P2 HIT).** Over those 1,833 pairs the ranked pass's Sharpe excess over
  its control is **mean −0.1338, median −0.1421 (sd 0.1044, range −0.3756..+0.2287)**, and
  **1,617 of 1,833 (88.2%) are ≤ 0**. The control ALSO passes 4b beside 600 of them.
- **The queue's exact claim.** Excess ≤ 0 *and* a control failing 4b on `DD` and nothing else:
  **102 of 1,833 (5.6%)**. The strong form is real but is a minority of the record; the weak form
  (no Sharpe edge) is the majority result.
- **Binding-bar census.** 122,199 failing rows carry a reason; 41,846 (34.2%) name a single bar.
  **DD 20,662 (49.4%) and CAGR 18,048 (43.1%) are the whole story** (H1 4.6%, H2 2.8%, OOS 0.2%).
  Split by kind, the sign reverses: **RANKED rows fail on DD alone 59.9% of the time; UN-RANKED
  rows fail on CAGR 64.8%** and on DD alone only 33.0%. 4b tests a *different bar* on the two
  kinds of book.

## PART B — fresh corpus, control by construction (3 panels × 6 widths × 3 gross × 2 rungs, weekly, next-day)

Panels: u56 (56×4,699d), broad136 (136×4,699d), small439 (440×4,194d, the 44 `max_1d_move ≥ 1.0`
names dropped first). Two tuned parameters only: n ∈ {5,10,20,30,40,ALL} and g ∈ {0.50,0.75,1.00};
cadence fixed weekly, cost rung reported not tuned. All 108 grid points in `.grid.csv`.

- **Ranked 4b passes: 2 of 90.** Both are u56 TOP40 g=1.00 (10 and 25 bps). **Both (100%) have
  Sharpe excess ≤ 0 over their own control and both clear on the DD cap alone** — the control
  fails 4b on `DD` and nothing else. Excess: **−0.0002 @10bps, −0.0781 @25bps**.
- **Un-ranked controls: 0 of 18 pass 4b.** Their sole-bar failures are `DD` (8) and `CAGR` (4) on
  u56/broad136 — P3 HIT (2/3 panels DD-modal); on small439 nothing is sole-bar because the Sharpe
  bars fail too.
- **Counterfactual screens (P4 HIT).** Delete the DD cap → **4 ranked passes** (vs 2). Add a
  clause requiring a Sharpe edge over the matched un-ranked control → **0 ranked passes**. There
  is no ranked book on this grid that clears 4b *and* beats its own control.
- **The 4b-clearing point, quoted in full and NOT claimed as a KEEP.** u56 TOP40 g=1.00 @10bps:
  **12.68% / 1.1242 / −18.16%**, halves **1.091 / 1.157**, OOS(2017+) **1.249**, vs SPY 15.23% /
  0.889 (0.957/0.834) / −33.72%, OOS 0.882, and vs RULES v2 (live) OOS 1.285. It clears 4b's
  letter at both rungs, but its control reads **1.1245** — it earns **−0.0002** of Sharpe for its
  ranking — and rule 8's own IS chooser does not select it (below). Filed as **PARK**, not KEEP.
- **4a: 0 of 108 grid points.** No arm beats live RULES v2 in both halves with no worse MaxDD.

## Rule 8 (params on IS ≤ 2016-12-31, 2017–2026 read once) — P5 MISS

| panel @10bps | IS pick | OOS CAGR / Sharpe / MaxDD | best un-ranked control | RULES v2 | SPY |
|---|---|---|---|---|---|
| u56 | n=ALL g=1.00 | 18.47% / 1.135 / −29.18% | same point | 9.53% / 1.285 / −12.05% | 15.45% / 0.882 / −33.72% |
| broad136 | n=ALL g=1.00 | 18.59% / 1.101 / −32.72% | same point | 7.98% / 1.119 / −12.24% | 15.45% / 0.882 / −33.72% |
| small439 | n=20 g=1.00 | 4.87% / 0.362 / −36.99% | 12.88% / 0.636 / −45.96% | 3.85% / 0.568 / −14.68% | 15.45% / 0.882 / −33.72% |

The chooser picks the **un-ranked control on 2 of 3 panels**, beats its control OOS on **0 of 3**,
beats SPY on 2 of 3 and RULES v2 on 0 of 3. At 25 bps it picks un-ranked on 3 of 3. The one
ranked pick (small439 n=20) costs **−0.274 of OOS Sharpe and −8.0 pp/yr** against its control.

## The mechanism (post-hoc diagnostic, declared as such; no verdict rests on it)

Sharpe is gross-invariant, so only the DD cap and the CAGR floor can move with g. A 9-step scan of
g ∈ [0.20, 1.00] locates each bar's boundary:

| panel @10bps | control (n=ALL): DD clears | CAGR clears | window | TOP40: DD clears | CAGR clears | window |
|---|---|---|---|---|---|---|
| u56 | g ≤ 0.60 | g ≥ 0.70 | **EMPTY** | g ≤ 1.00 | g ≥ 0.90 | [0.90, 1.00] |
| broad136 | g ≤ 0.50 | g ≥ 0.60 | **EMPTY** | g ≤ 0.80 | g ≥ 0.90 | EMPTY |
| small439 | g ≤ 0.30 | g ≥ 0.80 | **EMPTY** | g ≤ 0.50 | (never) | EMPTY |

**Windows non-empty in 3 of 36 (panel × width × rung) cells, and in 0 of 6 control cells.** 4b on
an un-ranked book is a two-sided squeeze with no admissible gross: de-gross to clear DD and the
CAGR floor bites. Concentration's only contribution is to push the DD boundary out (u56: 0.60 →
1.00) at zero Sharpe. So the DD cap is not "the only thing 4b tests" — it is one of two bars that
bind from opposite ends, and on ranked books it happens to be the one that gives.

## Caveats carried

- **SURVIVORSHIP (idea 54):** u56, broad136 and the sub-$2B panel are current-constituent lists
  with no delistings. Every arm inherits it equally, so the paired ranked-minus-control contrasts
  that carry this answer are largely protected; every LEVEL quoted (and therefore every 4b
  verdict) is biased upward and none is a tradable estimate. No book is proposed.
- Census rows are not independent (shared books, panels, rungs across files; many files publish
  several rungs of one simulation). Counts are counts; no p-value is computed over them.
- A 4b verdict is a function of SPY's numbers over the *same* window, so verdicts from files with
  different samples are not strictly commensurable. Part B fixes the window per panel and quotes
  SPY's bars beside every arm.
- 71,491 of 81,571 committed passes are label-UNKNOWN. The Part-A splits are statements about the
  10,080 classifiable passes, not about the whole record.
- Idea 144: a re-dialled book is the same book. Nothing here proposes a new signal.

Artefacts: `.console.txt` `.census_files.csv` `.census_pairs.csv` `.census_bars.csv` `.grid.csv`
`.bars.csv` `.window.csv` `.walkforward.csv` `.params.csv`
