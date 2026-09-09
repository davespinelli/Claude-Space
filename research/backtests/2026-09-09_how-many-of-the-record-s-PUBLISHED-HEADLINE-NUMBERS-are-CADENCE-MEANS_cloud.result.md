# Idea 577 — how many of the record's published headline numbers are cadence means? (cloud, 2026-09-09)

**Verdict: ANSWERED, with a KILL of the method the question implies.** The collapse is real and
record-wide, it is measurable, and it is NOT mainly a *cadence* problem — it is a *panel* problem.
The "which of these are the PUBLISHED ones" leg is uninformative and is reported as such rather
than dressed up.

## What was run
Every committed `research/backtests/*.csv[.gz]` — **2,558 files, 0 unreadable**. A *census cell* is a
(file, metric column, reporting axis) triple where the axis carries 2–20 levels inside that file, so the
file's pooled mean of that metric — the single number a memo quotes — is an average over levels a
trader must choose between. Axes are exactly the four the queue names: **cadence** {cadence, cad, freq},
**cost** {cost, bps, cost_bps, rung}, **seed** {seed, draw, rep}, **panel** {panel, universe, uni}. Gross, n,
band, book and family are deliberately NOT axes here. **21,454 cells from 1,323 files**; 1,183 files carry
no (axis, metric) pair at all. Two tuned parameters only: RSTAR (all 6 grid points reported) and the
numeric-match precision (all 5 reported).

## B1 — the collapse rate (all grid points, nothing selected)

| RSTAR | cells > RSTAR | rate | files |
|---|---|---|---|
| 1.25 | 10,680 / 21,454 | 49.8% | 1,164 / 1,323 |
| 1.50 | 7,764 | 36.2% | 1,051 |
| **2.00** | **4,281** | **20.0%** | **873** |
| 3.00 | 1,693 | 7.9% | 569 |
| 5.00 | 736 | 3.4% | 338 |
| 10.00 | 357 | 1.7% | 200 |

**One in five collapsed headline numbers moves by more than 2x at its own cells, and 66% of the
files that publish such a number publish at least one.** Idea 51R's 2.7x is not an outlier; it sits just
inside the record's 92nd percentile of collapsed cells.

## B2 — sign flips
**477 / 21,454 = 2.2%** of collapsed cells have levels of OPPOSITE SIGN (200 files). For these the
headline's *direction*, not just its magnitude, is an artefact of the mix.

## The axis that actually does the damage is PANEL, not cadence

| axis | cells | > 2x | signflip | median ratio |
|---|---|---|---|---|
| **panel** | 11,343 | **30.5%** | 3.0% | **1.626** |
| cadence | 1,845 | 14.8% | 2.2% | 1.148 |
| cost | 7,801 | 6.6% | 1.3% | 1.143 |
| seed | 465 | 6.5% | 0.2% | 1.118 |

The queue's premise (idea 314's "cadence mean") is **confirmed but under-drawn**: cadence collapse
runs at 14.8%, while **panel collapse runs at 30.5% — more than twice the rate — on 6x as many cells**,
with a median ratio of 1.63 against cadence's 1.15. Cost rungs and seeds are comparatively safe.
By metric family: **sharpe 25.1%, turnover 26.1%, CAGR 22.9%, MaxDD 8.2%** — MaxDD is by far the
most transportable thing the record quotes, Sharpe and CAGR the least.

## B3 — the published-surface leg is UNINFORMATIVE, and that is the honest result
Matching each headline's rendering against `LEADERBOARD.md` + `CHANGELOG.md`:

| precision | matched cells | > 2x inside matches | corpus > 2x | renderings per distinct token |
|---|---|---|---|---|
| 2dp | 21,233 (99.0%) | 19.9% | 20.0% | 35.99 |
| 3dp | 19,674 (91.7%) | 19.8% | 20.0% | 17.30 |
| pct1dp | 16,681 (77.8%) | 20.4% | 20.0% | 21.39 |
| pct2dp | 7,883 (36.7%) | 20.8% | 20.0% | 5.66 |
| ALL | 21,234 (99.0%) | 19.9% | 20.0% | 19.08 |

At every precision, 5.7 to 36 census cells share each matched token — numeric matching cannot
attribute a published figure to the file that produced it, and at 2dp it matches essentially
everything. **KILL the numeric-match method.** What it does establish, negatively but cleanly: the
published subset shows **no enrichment whatsoever** (19.8–20.8% vs the corpus 20.0%), so the memos
are neither better nor worse than the CSVs behind them. Answering "how many *published* numbers"
by name would require the memo prose to cite its own cell, which the record does not currently do.

## Rule 8 — WF-CENSUS (threshold chosen on the IS half, OOS half read once)
Split at the median commit date **2026-09-07**: IS 13,777 cells / 883 files, OOS 7,677 cells / 440 files.

| RSTAR | IS rate | OOS rate | delta |
|---|---|---|---|
| 1.25 | 47.0% | 54.7% | +7.7 pp |
| 1.50 | 33.0% | 42.0% | +9.0 pp |
| **2.00 (IS-chosen)** | **19.1%** | **21.4%** | **+2.3 pp** |
| 3.00 | 7.8% | 8.0% | +0.2 pp |
| 5.00 | 3.3% | 3.8% | +0.5 pp |
| 10.00 | 1.5% | 1.9% | +0.3 pp |

RSTAR* = 2.0 is chosen on IS alone as the smallest grid value with IS rate ≤ 20%; **OOS read once = 21.4%
vs IS 19.1%, TRANSPORTS** (bar |delta| ≤ 10 pp). The rate is a stable property of how the record is
written, not of one week's files.

## Rule 8 — WF-BOOK (the reference, since this idea nominates no weights)
10 bps, weekly, next-day execution.

| panel | book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| U56 | RULES v2 (live) | 8.6% | 1.204 | -12.1% | 1.231 | 1.183 | 9.5% | 1.282 | -12.1% |
| U56 | RULES v1 | 6.4% | 0.661 | -13.8% | 0.643 | 0.680 | 7.7% | 0.741 | -13.8% |
| U56 | SPY | 15.2% | 0.887 | -33.7% | 0.959 | 0.829 | 15.4% | 0.879 | -33.7% |
| B136 | RULES v2 (live) | 8.0% | 1.106 | -12.2% | 1.229 | 0.984 | 8.0% | 1.119 | -12.2% |
| B136 | RULES v1 | 6.4% | 0.635 | -21.2% | 0.756 | 0.532 | 5.9% | 0.576 | -21.2% |
| B136 | SPY | 15.2% | 0.889 | -33.7% | 0.957 | 0.834 | 15.5% | 0.882 | -33.7% |

The live book fails 4b on both panels for the **same single leg, CAGR** (U56 8.6% vs the 10.6% floor;
B136 8.0% vs 10.7%). **4a and 4b are vacuous for a record audit: no arm is nominated, no KEEP is
claimed, no memo is written.** RULES.md, scan.py, bot.py and baseline.py are untouched.

## Idea 314's own exemplar, reproduced by the general machinery
The vol-cap work's own committed CSVs are among the collapsed cells, and their worst axis is panel,
not cadence: `oSharpe` reads a headline of **+0.800** over a panel axis whose cells are
**U56 1.188 / B136 1.090 / SMALL439 0.121 — a 9.82x spread**; `oCAGR` +7.21% over
**10.77% / 9.75% / 1.10% — 9.76x**.

## What this licenses
A concrete, cheap convention, offered for the Sunday review and NOT applied here: **any headline
figure quoted from a CSV that carries a panel or cadence axis must name the axis and cell it was read
at, or quote the range.** The measured cost of not doing so is a 1-in-5 chance the number is off by
more than 2x, and a 1-in-45 chance its sign is wrong.

Script: `2026-09-09_how-many-of-the-record-s-PUBLISHED-HEADLINE-NUMBERS-are-CADENCE-MEANS_cloud.py`
Outputs: `.cells.csv.gz` (all 21,454), `.grid.csv` (all 30 grid points), `.published.csv.gz`, `.walkforward.csv`, `.console.txt`
