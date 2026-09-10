# Idea 667 — does the record quote a WINDOW STAMP beside any metric it publishes?

**Lane C, 2026-09-10. ANSWERED: NO — almost never. SPLIT on the consequence, KILL for capital.
No RULES change, no PROTOCOL change, no book promoted, no KEEP claimed.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Tuned parameters, exactly two per PROTOCOL 4: **stamp form** (ROWSPAN / ROWANY / FILEHEAD /
FILENAME) × **metric** (Sharpe / CAGR / MaxDD / OOS_Sharpe). All 16 grid points reported.
Panels, books, dials, cost rungs and the 40-point span grid are reported axes, never selected on.

## Gates (pre-registered, run before any analysis number was read)

| gate | what | result |
|---|---|---|
| G1 | `fast_run` vs `engine.backtest` (U56 BAND @0bps), returns / turnover | **0.000e+00 / 0.000e+00** |
| G2 | cost identity `r(c) = r0 − turnover·c/1e4` vs engine @10bps | **0.000e+00** |
| G3 | `band_book(0.03,0.75)` vs `baseline.rules_v2_weights` | **0.000e+00** |
| G4 | end-drift equivalence: re-run truncated panel vs slice full-sample returns, k∈{1,2,5,21} | **0.000e+00** at every k |
| G5 | the CHANGELOG datum | **reproduced exactly — see below** |
| G6 | census partition exact at all 16 grid points | **PASS** |

**G5 is itself the result in miniature.** Today's cache (2026-09-09) prices live RULES v2 on U56 at
CAGR 8.6317% / Sharpe **1.2021** / MaxDD −12.0549% / H 1.2309/1.1798, reproducing idea 664's
same-day committed row exactly. Truncate the identical book to **2 trading days earlier**
(2026-09-04) and it reads CAGR 8.6601% / Sharpe **1.2056** — the CHANGELOG's 2026-09-08 row to
**dSharpe +0.0000**. The same book, the same rules, the same code; the only difference is where the
sample stopped, and nothing in either artefact says where that was. (Caveat, idea 406/399:
`data/prices.csv` is re-downloaded daily with auto-adjusted closes, so this residual mixes
END-DRIFT with the U56 RESTATEMENT channel.)

## A1 — the census (the queue's first ask)

Of **1,575** committed CSVs that publish a Sharpe (3,101 CSVs scanned; this run's own artefacts
excluded so a re-run is idempotent):

| stamp form | Sharpe | CAGR | MaxDD | OOS_Sharpe |
|---|---|---|---|---|
| **ROWSPAN** (per-row start+end or asof) | **10 (0.63%)** | 10 (0.64%) | 10 (0.70%) | 7 (0.58%) |
| **ROWANY** (any stamp-lexicon column, deliberately over-permissive) | 89 (5.65%) | 81 (5.19%) | 65 (4.55%) | 40 (3.33%) |
| **FILEHEAD** (a date or year span anywhere in the file's own family) | 1,415 (89.8%) | 1,406 (90.1%) | 1,280 (89.5%) | 1,093 (91.1%) |
| **FILENAME** (a date in the filename) | **1,575 (100%)** | 1,560 (100%) | 1,430 (100%) | 1,200 (100%) |

Corpus-wide, the explicit date-stamp column names occur **38 times in 12,954 distinct column
names**: `start` 17, `end` 15, `vintage` 6, `is_start` 1.

Prose artefacts: **LEADERBOARD.md** publishes a Sharpe in 1,599 rows, of which **9 (0.6%)** carry a
full date span and 313 (19.6%) a year span — **1,286 carry neither**. **CHANGELOG.md**: 325
entries, 11 (3.4%) full date span, 183 (56.3%) year span, 142 neither.

**The record stamps the RUN date on 100% of its artefacts and the SAMPLE window on 0.63% of them.**
That gap is the finding. A year span ("2017–2026") does not date a number to a trading day, which
is the resolution at which A2 shows the number moves.

## A2 — what a missing stamp is actually worth, and a correction to idea 664

Idea 664's WINDOW family mixes six cost rungs and three cadences in with its span variants. A cost
rung is not a window. Measuring the **pure** span channel — same book, same rung, same cadence,
only the slice moves (5 start conventions × 8 end truncations = 40 points, 3 panels × 3 books):

| bar (pooled mean of per-cell p50 \| p90) | CAGR | Sharpe | MaxDD | H1 | H2 |
|---|---|---|---|---|---|
| END alone (cache growth) | 0.0006 \| 0.0024 | **0.0037** \| 0.0160 | 0.0000 | 0.0078 \| 0.0416 | 0.0107 \| 0.0371 |
| START alone (warm-up convention) | 0.0039 \| 0.0092 | **0.0201** \| 0.0576 | 0.0000 | 0.0682 \| 0.1479 | 0.0229 \| 0.0430 |
| **PURE span** | 0.0034 \| 0.0096 | **0.0179 \| 0.0625** | **0.0000** | 0.0489 \| 0.1530 | 0.0183 \| 0.0611 |
| CONTAM664 (664's construction, reproduced) | 0.0040 \| 0.0176 | **0.0396** \| 0.1967 | 0.0106 | 0.1123 \| 0.4788 | 0.0788 \| 0.3282 |
| BOOK (different books, same slice) | 0.0506 \| 0.0982 | **0.0484** \| 0.1227 | 0.0853 | 0.0651 \| 0.1580 | 0.0470 \| 0.1333 |

**The queue's premise, inherited from 664, is FALSIFIED.** 664 reported a window bar (0.0355)
*larger* than its between-book bar (0.0235). Reproduced here its construction reads 0.0396 — but
**de-contaminated, the pure-span bar is 0.0179 against a BOOK bar of 0.0484**: a window is worth
**0.37×** a book, not more than one. Most of 664's "window" bar was cost rungs and cadence.

Two sub-results worth carrying: the **START convention is 5.4× the END channel** (0.0201 vs 0.0037)
— the record's exposure is the warm-up convention, not the growing cache — and **MaxDD's pure-span
bar is exactly 0.0000** on every panel and book, because the max drawdown sits in the sample
interior and trimming either edge cannot reach it. Drawdown claims need no stamp.

## A3 — re-pricing the record's published comparisons (the queue's second ask)

Exact zeros excluded throughout (53,161 delta values, 9,957 comparand gaps): a published delta of
exactly 0.0 is not a distinction being drawn.

| population | Sharpe | CAGR | MaxDD | OOS_Sharpe |
|---|---|---|---|---|
| **A3c DELTA** — the record's explicit `d<metric>` columns, share below the pure-span p50 bar | **0.3411** (n 65,716) | 0.3402 | 0.0494 | 0.2509 |
| … below its p90 | 0.6478 | 0.4880 | 0.0940 | 0.5617 |
| **A3b COMPARAND** — within-row arm-vs-benchmark gaps (control) | 0.1298 | 0.0472 | 0.0113 | 0.0742 |
| **A3a ADJACENT** — within-file adjacent gaps (declared weak, size-dominated) | 0.9842 | 0.9793 | 0.0357 | 0.9741 |

**Headline: the record publishes 79,178 explicit Sharpe-family delta values across 169 files;
32.57% of them are smaller in absolute value than the pure-span p50 bar and 63.31% smaller than its
p90. Exactly one of those 169 files carries a per-row window stamp.** The A3b control — the same
metric, comparisons whose two sides share a window *by construction* — sits at 0.0965. The exposure
is in the deltas, not in the counting.

The honest reading of that number: those deltas are internally consistent *within* the run that
produced them. What they are not is **portable**. A reader — the next run, the Sunday review — who
re-derives a published gap on a different cache or a different warm-up convention gets a different
number, and for a third of the record's Sharpe deltas the difference is the size of the gap itself.
G5 is that failure happening, once, on the live book, in the CHANGELOG.

## A4 / A5 — and what the stamp does NOT endanger

**PROTOCOL verdicts are robust to the missing stamp.** Over 153 arm-rungs × 40 span points
(6,120 rows): 4a at the house span **0/153**, 4b **3/153**, BOTH **0/153**; span alone flips the 4b
verdict in **0 of 5,967** moved rows and the 4a verdict in **7 (0.12%)**, all seven on the START
channel, none on END at any k up to 63 trading days. The binding 4b bar is the CAGR floor in 104 of
153 rows, the DD cap in 38.

**Rule 8 (PROTOCOL 8), dial chosen on 2009-2016 alone, 2017-2026 read once, 27 true-window picks
and 1,053 drifted-window picks:** an unstamped IS window flips the pick in **13.39%** of cells
(END 10.05%, START 9.26%; band 9.12% / n 17.38% / gross 13.68%), and the flip rate is flat in k out
to 10 days (7.4–8.9%) then jumps to **25.9% at k=21 and 30.4% at k=63**. **The flips cost nothing:
mean ΔOOS Sharpe +0.0027, median +0.0005, and 50.35% of flips help.** Window noise moves the choice
without informing it. True-window picks beat the live book OOS in **5 of 27** and SPY in **16 of
27**; 3 of 27 are the OOS oracle, mean regret +0.0652.

**No KEEP.** The 3 4b passes are one arm — U56 equal-weight-all at gross 0.65 (10 bps: CAGR 11.46%,
Sharpe 1.121, MaxDD −19.75%, H 1.193/1.065, OOS 1.132) — a reported axis point from the standing
`RECOMMENDATION` Finding-2 family, and **rule 8 never picks it: 0 of 120 span variants select
gross 0.65 on U56, all 120 pick gross 1.00.** It fails 4a on both halves. A 4b pass that the
protocol's own selector cannot reach is not a candidate.

## Predictions, scored

Q1 ✅ (0.63% < 3%). Q2 ✅ (100% FILENAME vs 0.63% ROWSPAN). Q3 **half wrong** — the pure bar is
smaller than 664's, as predicted, but it lands *below* the between-book bar, which reverses 664's
published ordering rather than merely shrinking it. Q4 ✅ (32.57% > 25%, control 9.65%). Q5 ✅
(13.39% flips, +0.0027). Q6 ✅ (no KEEP; the one 4b arm is inherited and rule-8-unreachable).

## Caveats carried

SURVIVORSHIP (idea 54): all three panels are current constituents, SMALL439 worst. The corpus is
this repository's committed artefacts only; a file stating its window in prose the regexes miss is
scored UNSTAMPED, and the ROWSPAN→FILEHEAD gap (0.63% → 89.8%) brackets that error from both sides.
ROWANY over-counts on purpose (`window` in this record usually names a 4b bar-window, not a date).
MaxDD is one number off one path (idea 321). Idea 126: t+1 execution, no lag band. Idea 38:
u56/broad carry the calendar-day index. A0's header pass was run before the predictions were
written and says so in the script.

## What the record should do about it (report-only; PROTOCOL changes are Sunday-review business)

Publish `start` and `end` beside every metric column, and quote the evaluated span in every
LEADERBOARD row. It costs two columns. The evidence that it is worth two columns is G5 and the
32.57%; the evidence that it is not urgent is A4's 0-of-5,967. **Reporting defect, not a rule
defect.**

Script: `research/backtests/2026-09-10_does-the-record-quote-a-WINDOW-STAMP-beside-any-metric-it-publishes_C.py`
