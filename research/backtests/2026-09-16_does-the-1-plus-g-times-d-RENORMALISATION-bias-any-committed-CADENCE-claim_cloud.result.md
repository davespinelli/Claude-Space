# Idea 1087 (cloud lane, 2026-09-16) — does the `1 + g*d` RENORMALISATION bias any committed CADENCE claim?

**ANSWERED = YES, AND IT BITES HARDER ON A STEP THAN ON A LEVEL — but only on CONVERSION, which
is a CORRECTION to the queue's own premise.** `H_STEPLIN` and `H_STEPREC` both **FAIL**: the
cadence step is proportional to gross only to **11.83%** over {0.25 … 1.00} and **6.48%** over the
record's own {0.50, 0.75, 1.00}, against 1076's level residuals of 5.31% / 2.87% reproduced here
exactly — an **amplification of 2.259×**. On the record's own ladder that is a bias of up to
**4.36 bp/yr** (median 0.23 bp/yr) on a converted cadence gain, which moves **58 of 163 (0.356)**
committed cadence-gain figures beyond their own stated precision at the median cell and
**131 of 163 (0.804)** at the worst. Plus a **KILL of this run's OWN declared direction**
(`H_DIR` FAIL, both halves), published beside the right answer rather than replaced.
**No book proposed, no RULES change, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.**

Script
`research/backtests/2026-09-16_does-the-1-plus-g-times-d-RENORMALISATION-bias-any-committed-CADENCE-claim_cloud.py`,
8 CSVs, console log committed. **Gates 7 of 9. Hypotheses 5 of 8.**

---

## SELECTION

The cloud lane takes the FIRST eligible open idea. 1087 was the first line under `## Open` and its
text names no EDGAR / Form 4 / 8-K / options / spin-off / live-data source, so it runs in the
sandbox.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**TUNED 1 — CADENCE STEP**, 6 levels, all reported and never merged: `D->W`, `D->M`, `D->Q`,
`W->M`, `W->Q`, `M->Q`.
**TUNED 2 — GROSS RUNG**, 4 levels, all reported: {0.25, 0.50, 0.75, 1.00}. The record's own
ladder is {0.50, 0.75, 1.00}; 0.25 widens the curve and no verdict is read off it alone.

**REPORTED AXES, every point published:** panel {U56, B136}; book {TOP5, TOP10, TOP20, EWELIG,
BAND03} — idea 930/1076's own set, verbatim; cadence {D, W, M, Q}; source {LEADERBOARD, CHANGELOG,
QUEUE, RESULTMD}. **6 steps × 4 rungs × 10 (panel, book) cells = 240 published step-points**, off a
160-point turnover ladder that reproduces 1076's committed one to **7.1e-15** (G5).

## GATES — 7 of 9, printed before any result number

| gate | stat | verdict |
|---|---|---|
| G1 fast runner ≡ `engine.backtest` on returns AND turnover | 4.163e-16 | PASS |
| G2 cost linearity `net(c) == gross − turn·c/1e4` at 5 and 25 bps | 2.082e-17 | PASS |
| G3 SPY OOS triple vs committed (0.152102, 0.8711, −0.337173) | 2.976e-05 | PASS |
| G4 live RULES v2 full MaxDD vs committed −12.05% | 4.949e-05 | PASS |
| G5 CROSS-RUN `turn_yr` vs idea 1076's committed `linearity.csv`, 160 shared cells | 7.105e-15 | PASS |
| G6 CROSS-RUN 1076's committed level deviations 5.312e-02 / 2.87e-02 reproduce | 9.084e-06 | PASS |
| G7 determinism: the weight rows are a pure function of the panel | 0.000e+00 | PASS |
| **G8a DECLARED SIGN of `REL_step`** | mean **+8.766e-03** (POSITIVE) | **FAIL** |
| **G8b DECLARED MONOTONICITY of `step/g` in g** | **32 of 60** cells (0.533) | **FAIL** |

**G8 IS THIS RUN'S OWN DECLARATION FAILING, AND IT IS PUBLISHED, NOT PATCHED.** It was declared
before the run that `REL_step(g)` would be NEGATIVE *and* that `step/g` would be monotone
DECREASING in g. The two halves contradict each other: if `step/g` falls in g then at a low rung
it sits **above** its own `g = 1.00` reference, so `rel` is POSITIVE by construction. The tape
agrees with the stated mechanism and not with the stated sign. The monotonicity half fails on its
own terms too — 1076 found the LEVEL monotone on **40 of 40** cells, but differencing two monotone
curves of different curvature need not be monotone, and on this tape it is not (**32 of 60**).

## THE MECHANISM, STATED BEFORE ANY NUMBER

`engine.backtest` normalises the drifted holdings row by `V = 1 + g*d`, where `d` is the drift P&L
per unit of gross since the last decision. `d > 0` on average on this tape, so a larger `g`
deflates the held row more and pulls it back **toward** the target: turnover per unit of gross
**falls** in `g`. `d` accumulates between **decisions**, so its magnitude is a cadence quantity —
a quarterly book drifts ~63 trading days before it is asked to trade, a daily book one. The two
sides of a cadence step therefore carry residuals of different size and cannot cancel.

## THE ANSWER — THE STEP RESIDUAL, 240 PUBLISHED POINTS

Per-rung max |rel| over all 60 (panel, book, step) cells:

| rung | @0.25 | @0.50 | @0.75 | @1.00 |
|---|---|---|---|---|
| max \|rel\| STEP | 1.183e-01 | 6.480e-02 | 2.464e-02 | 0 (reference) |

`max |rel|` **STEP** full ladder **1.1831e-01**, record ladder **6.4801e-02**.
`max |rel|` **LEVEL** full ladder 5.3116e-02, record ladder 2.8691e-02 — 1076's committed numbers,
reproduced at G6 to 9.1e-06.
**AMPLIFICATION step / level: 2.227× (full ladder), 2.259× (record ladder).** `H_AMPLIFY` PASSES:
the queue's second clause — that the residual does not cancel on a difference — is confirmed in
direction and priced.

The worst cells are the same family 1076 found: **BAND03 `D->W` @ g = 0.50** reads rel +6.480e-02
on B136 and +5.684e-02 on U56, i.e. the slowest-turning book differenced against the fastest
cadence, exactly where drift between decisions has most room.

## THE BIAS ITSELF — what it costs to read a committed gain at another gross

`BIAS(g_from → g_to) = STEP(g_from) · g_to/g_from − STEP(g_to)`, in bp/yr at the binding 10 bps.

| ladder | n conversions | max \|rel\| | median \|rel\| | max \|bias\| | median \|bias\| |
|---|---|---|---|---|---|
| full {0.25…1.00} | 720 | 1.183e-01 | 4.943e-03 | **6.646 bp/yr** | 0.3063 bp/yr |
| record {0.50, 0.75, 1.00} | 360 | 6.480e-02 | 2.264e-03 | **4.357 bp/yr** | 0.2346 bp/yr |

By step, on the record's own ladder: `D->Q` max 4.357 bp (median step 233.58 bp), `D->M` 3.870
(211.61), `D->W` 2.669 (150.81), `W->Q` 1.689 (83.22), `W->M` 1.202 (61.20), `M->Q` 0.487 (23.30).
`D->W` carries the largest *relative* error (6.48e-02) and `D->Q` the largest *absolute* one.

## A CORRECTION TO THE QUEUE'S OWN PREMISE

The queue says: *"Every committed cadence comparison differences two books at one gross, so the
residual does not cancel."* Half right, and the distinction is the whole result:

1. **At the gross it was measured at, a cadence gain is EXACT.** It is the difference of two
   numbers the engine actually produced. No linearity is assumed, so there is no residual to
   cancel or fail to cancel. The queue's framing implies a bias where none exists.
2. **The residual enters the moment that gain is read at ANOTHER gross** — which is precisely what
   an unstamped figure invites, and 1076 measured that **0.924** of committed turnover/drag figures
   are unstamped. That is the quantity priced above, and on it the queue's second clause is right.

## DOES IT MOVE A PUBLISHED CADENCE GAIN BEYOND ITS OWN STATED PRECISION?

Census of the **30,615-unit** committed corpus (LEADERBOARD rows, CHANGELOG paragraphs, QUEUE
lines, every `*.result.md` by paragraph): **312** turnover/drag figures sit in a unit that also talks
about cadence — **20 STEP** (an explicit `X -> Y`), **143 MULTI** (≥ 2 cadences named), **149 ONE**
(a level, carried so the denominator is visible). The **163 cadence-gain figures** (STEP + MULTI)
are stamped with a numeric gross **10 times (0.061)** — consistent with 1076's record-wide 0.076,
and of the STEP tier **zero of 20** are stamped.

A figure states its precision by its last printed digit; half a unit there is the most it can be
claiming. Against the record-ladder bias:

| | n | moved |
|---|---|---|
| MOVED at the MEDIAN cell (bias 0.2346 bp/yr) | 58 of 163 | **0.356** |
| MOVED at the WORST cell (bias 4.3572 bp/yr) | 131 of 163 | **0.804** |
| NOT moved even at the worst cell | 32 of 163 | 0.196 |

By stated precision: every figure printed to 1 decimal or finer in bp/yr (58 of 163) is moved at
the median cell; the 73 printed to the nearest 0.1x and the 32 to the nearest 1x are not.
`H_PRECISION` **PASSES** — **0.644 of committed cadence gains survive the median bias** — but it
passes by a margin the figures themselves chose, not by anything about the tape: the record is
mostly safe here because it mostly prints coarse.

**THE HONEST LIMIT OF THIS CENSUS, stated rather than papered over:** 0.939 of these figures state
no gross, so neither the cell nor the rung a given committed figure came from is knowable. The bias
is therefore priced over the **whole** cell population and both the median and the max are
reported. Nothing above claims to match a figure to a cell.

## CADENCE RANK INVARIANCE — `H_RANK` PASSES

The cadence ordering by annual turnover reads `D > W > M > Q` at **all four** rungs in **10 of 10**
(panel, book) cells. No committed "M turns over less than W" claim can be reversed by the rung it
is read at. The residual moves sizes, never signs.

## RULE 8 AND BOTH KEEP PATHS

(cadence, gross) chosen **jointly on IS 2009-2016 Sharpe ALONE** over the 16 combinations per
(panel, book); OOS 2017-2026 read **once**.

Benchmarks: **U56** SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588/0.8207), OOS 15.21% / 0.8711
/ −33.72%; RULES v2 live full 8.62% / 1.2007 / −12.05% (halves 1.2322/1.1760), OOS 9.45% / 1.2762 /
−12.05%. **B136** SPY full 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72%; RULES v2 full
7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059 / −12.24%.

**4b full-sample on the IS pick 2 of 10. 4a on the IS pick 0 of 10. 4b OUT OF SAMPLE on the pick
1 of 10.** Whole 160-cell grid: **4b 11 of 160, 4a 0 of 160, 4b-OOS 16 of 160.** `H_WF` passes on
the single pick U56 `BAND03 M@1.00` (full 11.89% / 1.1729 / −18.81%, halves 1.219/1.135, OOS
12.81% / 1.2243 / −18.81%).

**NOTHING IS PROPOSED, AND NOTHING HERE IS NEW.** That pick is the live band construction at full
gross — the object committed in LEADERBOARD.md as `BAND03@g1.00` and **refused on 4a for drawdown
four times over**; 1076 committed its daily/weekly/monthly @1.00 OOS-4b picks in the same words one
run ago, and this run reproduces them. The next-strongest 4b pass on the grid, U56 `TOP20 M@0.75`
(full 15.28% / 1.2125 / −19.51%, OOS 17.53% / 1.3061 / −19.51%), is the record's single
most-claimed cell. Both paths are scored here because rule 4 requires it on every run, not because
this run found a book. **No memo written.**

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are **CURRENT-CONSTITUENT** panels. The census half of this run is a statement about
committed text and is unaffected. The tape half — turnover levels, the step residual, the
conversion bias, rule 8 — is flattered exactly as every other run on these panels is, and every 4b
count above is an **UPPER** bound. The residual itself is a ratio of two turnover figures drawn
from the same inflated tape, so the bias very largely cancels out of it; the 4b legs, measured
against SPY, a real index, get no such cancellation.

## FOLLOW-UPS FILED

1090 (is the STEP residual's NON-MONOTONICITY a BAND03 fact or a book-wide one — G8b failed on 28
of 60 cells and the worst cells are all one book), 1091 (how many committed cadence gains are
quoted to a precision FINER than the record can measure at all, i.e. finer than this run's median
conversion bias, and should the record round them), 1092 (does the same 2.26× amplification appear
on a COST-RUNG difference, the other quantity the record routinely differences at one setting).
