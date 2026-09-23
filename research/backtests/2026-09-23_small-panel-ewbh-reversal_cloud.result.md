# idea 2524 (lane cloud, run 70, 2026-09-23) — DOES THE CAPPED CANDIDATE'S EWBH FAILURE REVERSE ON THE SMALL-CAP PANEL?

**ANSWERED = NO, AND THE PANEL AXIS IS CLOSED. On SMALL the book carries 4b-PROTO in 0 of 64
book-rows under SPY, 0 of 64 under EWBH and 0 of 64 under EWRB, and path 4a in 0 of 64 —
every single grid point fails, at every cap, every gross and every rung.** The one thing that
does reverse is the *comparand*, not the verdict: the survivorship premium flips sign
(EWBH minus SPY = **-5.15 pp of CAGR on SMALL** against **+10.01 pp on U56** and **+7.19 pp on
B136**), so EWBH becomes the EASIER benchmark there and 4b-STRICT goes 0 of 64 (U56, B136) to
**6 of 64** (SMALL). It buys nothing, because the book itself collapses on small caps: Sharpe
**1.2687 -> 0.6689** and MaxDD **-14.81% -> -33.31%** at the committed cell.

Script: `research/backtests/2026-09-23_small-panel-ewbh-reversal_cloud.py` (33 of 33 gates pass,
48 s, offline on the committed caches). Rows `.rows.csv` (960 scorings), books `.books.csv`,
walk-forward `.walkforward.csv`, gates `.gates.csv`, console `.log.txt`.

## What was asked
Idea 2516 killed all 21 committed capped-family 4b passes by replacing SPY with EWBH(panel) — but
it priced that kill on U56 and B136 only, the two panels with the largest current-constituent
premium. SMALL is drawn from a sub-$2B screen whose equal-weight buy-and-hold should be far
weaker, so the 200d band gate has the most room to earn its keep exactly where the record has
always scored it 0 of N. A pass here would be the record's first 4b that is not a megacap
survivorship artefact; a failure closes the axis.

**G5: the 54 `max_1d_move >= 1.0` tickers are dropped from `data/small_meta.csv` BEFORE anything
is computed** — 667 columns left (665 investable + SPY benchmark + SHY sweep), 4203 rows,
15.7 years scored. DIAL 1 per-name cap {0.005, 0.010, 0.020 = CAP2, INF = CAND}; DIAL 2 gross
{0.75, 1.00}. **Two tuned parameters, no more.** Published, never selected on: panels {SMALL,
U56, B136}, the COMMON WINDOW (megacap panels re-scored on SMALL's own 2010-2026 dates so all
three are read on the same tape), cadence {W, M}, rungs {0, 10, 25, 50} bps, band 0.03, MA 200d,
SHY sweep phi = 1.00. 5 arms x 64 book-rows x 3 comparands = **960 published scorings**.

## The committed cell (cap 0.020, g 0.75, W, 10 bps)

| window / panel | book | CAGR | Sharpe | MaxDD | Vol | H1 / H2 | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|---|---|
| **OWN / SMALL** | **CANDIDATE** | **8.05%** | **0.6689** | **-33.31%** | 12.81% | 0.789 / 0.611 | 7.91% | 0.6126 |
| OWN / SMALL | live RULES v2 | 4.26% | 0.6596 | -14.13% | | 0.806 / 0.548 | 3.63% | 0.5458 |
| OWN / SMALL | SPY | 14.03% | 0.8570 | -33.72% | 17.02% | 0.903 / 0.841 | 15.29% | 0.8751 |
| OWN / SMALL | EWBH(SMALL) | 8.88% | 0.5374 | -42.30% | 19.33% | 0.860 / 0.355 | 6.02% | 0.3808 |
| OWN / SMALL | EWRB(SMALL) | 13.00% | 0.7030 | -44.41% | 20.35% | 0.964 / 0.574 | 11.47% | 0.5939 |
| OWN / U56 | CANDIDATE | 11.62% | 1.2687 | -14.81% | 8.99% | 1.303 / 1.246 | 12.77% | 1.3318 |
| OWN / B136 | CANDIDATE | 11.82% | 1.1180 | -17.10% | 10.49% | 1.260 / 0.990 | 11.65% | 1.0936 |

The same rule on the same dates is a different animal on small caps: **half the Sharpe, 2.2x the
drawdown, 3.6 pp less CAGR**, and it loses to plain SPY on four of five 4b legs.

## The verdict — 4b by panel and comparand (64 book-rows per arm)

| window / panel | SPY PROTO / STRICT | EWBH PROTO / STRICT | EWRB PROTO / STRICT | 4a |
|---|---|---|---|---|
| **OWN / SMALL** | **0 / 0** | **0 / 6** | **0 / 0** | **0 of 64** |
| OWN / U56 | 19 / 6 | 0 / 0 | 3 / 0 | 28 of 64 |
| OWN / B136 | 11 / 8 | 0 / 0 | 1 / 0 | 6 of 64 |
| COMMON / U56 | 20 / 7 | 1 / 0 | 4 / 1 | 28 of 64 |
| COMMON / B136 | 12 / 12 | 0 / 0 | 2 / 0 | 4 of 64 |

On SMALL the first-binding PROTO leg is `L_H1` (52 of 64 under SPY, 47 under EWBH, 61 under EWRB)
and `L_DD` fails **64 of 64 under every comparand**: the book's own -33.31% drawdown cannot clear
0.60 x SPY's -33.72% (-20.23%) or 0.60 x EWBH's -42.30% (-25.38%). The gate does not protect a
small-cap panel; it rides it down.

## The reversal, measured (share of 64 rows the candidate leads, 4b-STRICT legs)

| window / panel | comparand | Sharpe H1 | Sharpe H2 | Sharpe OOS | MaxDD no worse | CAGR no lower | median dCAGR pp | median dSharpe | median dMaxDD pp |
|---|---|---|---|---|---|---|---|---|---|
| **OWN / SMALL** | **EWBH** | 26.6% | 93.8% | 92.2% | 62.5% | **42.2%** | **-0.19** | +0.1145 | +3.26 |
| **OWN / SMALL** | **EWRB** | 4.7% | 43.8% | 40.6% | 67.2% | **0.0%** | **-4.05** | -0.0459 | +5.05 |
| OWN / U56 | EWBH | 56.2% | 93.8% | 95.3% | 100.0% | 0.0% | -16.55 | +0.1507 | +31.89 |
| OWN / B136 | EWBH | 43.8% | 29.7% | 42.2% | 100.0% | 0.0% | -10.58 | -0.0077 | +12.10 |

**The survivorship premium, the thing 2516 measured, flips sign on SMALL:**

| window / panel | EWBH CAGR | SPY CAGR | d CAGR pp | EWBH MaxDD | 4b CAGR floor SPY -> EWBH | 4b DD cap SPY -> EWBH |
|---|---|---|---|---|---|---|
| **OWN / SMALL** | 8.88% | 14.03% | **-5.15** | -42.30% | 9.82% -> **6.22%** | -20.23% -> **-25.38%** |
| OWN / U56 | 25.24% | 15.23% | +10.01 | -44.19% | 10.66% -> 17.67% | -20.23% -> -26.52% |
| OWN / B136 | 22.32% | 15.12% | +7.19 | -33.00% | 10.59% -> 15.62% | -20.23% -> -19.80% |

Both 4b legs move in the book's FAVOUR on SMALL — the CAGR floor drops 3.6 pp and the DD cap
loosens 5.2 pp — and it still passes nothing. The CAGR leg does stop binding (`L_CAGR` fails 8 of
64 under EWBH on SMALL against 64 of 64 on U56), which is the reversal the idea predicted, but
`L_H1` and `L_DD` take over.

**EWRB is the fairer of the two comparands here and it kills hardest.** EWBH can only hold names
already priced on day one, and on SMALL that is **388 of 665 names (58.3%)** against 88.9% (U56)
and 90.3% (B136) — a third of the panel is invisible to it. EWRB holds every priced name,
rebalanced weekly at 2.01x/yr turnover and charged the book's own rung: **13.00% / 0.7030 /
-44.41%**, and the candidate's CAGR is lower in **64 of 64 rows** against it with a median gap of
-4.05 pp.

## Rule 8 walk-forward (dials fitted on warm-up..2016-12-31, 2017-2026 read ONCE)
SMALL's cache starts 2010-01-04, so its IS window is ~6 years against ~7 on the megacap panels —
stated, not adjusted for. 16 picks per arm (2 cadences x 4 rungs x 2 IS-only choosers).

| arm | picks | OOS CAGR | OOS Sharpe | OOS MaxDD | > live | > SPY | > EWBH | > EWRB | full 4b SPY / EWBH |
|---|---|---|---|---|---|---|---|---|---|
| **OWN / SMALL** | 0.005/1.00 in 12 of 16 | **6.93%** | **0.4920** | **-39.07%** | 5/16 | **0/16** | 14/16 | **0/16** | **0/16 / 0/16** |
| OWN / U56 | 0.005/0.75 in 16 of 16 | 4.76% | 1.5501 | -6.60% | 16/16 | 16/16 | 16/16 | 16/16 | 0/16 / 0/16 |
| OWN / B136 | 0.005/0.75 in 16 of 16 | 7.73% | 1.1642 | -12.10% | 12/16 | 16/16 | 12/16 | 14/16 | 0/16 / 0/16 |
| COMMON / B136 | 0.005/0.75 in 12 of 16 | 8.65% | 1.1328 | -13.79% | 10/16 | 16/16 | 13/16 | 13/16 | 3/16 / 0/16 |

**OOS on SMALL, the numbers rule 8 asks for: pick 6.93% / 0.4920 / -39.07%, against the live
RULES v2 baseline on the same panel 3.63% / 0.5458 / -14.13% and SPY 15.29% / 0.8751 / -33.72%.**
The pick beats SPY's OOS Sharpe **0 of 16 times** and EWRB's **0 of 16**; it beats EWBH's 14 of 16
only because EWBH(SMALL) OOS is 6.02% / 0.3808 / -42.30%, which is not a benchmark worth clearing.
**Full-sample 4b on the pick: 0 of 16 under both comparands on every arm.**

A second rule-8 finding, reported because it is not selected on: on every arm the IS choosers pick
the **smallest** cap (0.005) — on U56 that turns the book into a cash fund (OOS CAGR 4.76% at
Sharpe 1.55 and MaxDD -6.60%), the same de-grossing pathology idea 2520 found under the absolute
cap. Fitting the cap is a return give-up dressed as a Sharpe win.

## Verdict
**KILL — and the panel axis is closed.** 2516's EWBH kill is panel-independent: it does not
depend on the megacap survivorship premium, because on the one panel where that premium is
NEGATIVE the book still carries 0 of 64 PROTO passes under every comparand and 0 of 64 on path 4a.
The 6 of 64 STRICT passes under EWBH(SMALL) are the record's first non-zero EWBH strict count for
this family and they are reported in full, but they are bought entirely by the comparand getting
worse (EWBH(SMALL) Sharpe 0.5374, H2 0.355) rather than by the book getting better, and they
vanish against EWRB, the comparand that holds the two-fifths of the panel EWBH cannot see.
No RULES change, no new candidate.

## Caveats
**Survivorship (rule 9 and `data/SMALL_PANEL_README.md`) — the small panel is the worst offender
in this repository.** It is the CURRENT constituent list of a sub-$2B screen: only companies still
listed, still public and still under $2B today, so every name survived 2010-2026 by construction
and the acquired, taken-private, bankrupted and delisted small caps of that window are simply
absent. Returns are biased upward and drawdowns shallow, which makes this a *generous* test that
the book still fails — the true small-cap result is worse than what is printed here. EWBH and
EWRB carry the identical contamination on the identical tape and days, so the candidate-vs-EWBH
contrast is differenced clean; the SPY columns are not and are kept for protocol continuity only.
SMALL's 6-year IS window is shorter than the megacap panels'. Nothing in this run licenses a
small-cap book for real capital.
