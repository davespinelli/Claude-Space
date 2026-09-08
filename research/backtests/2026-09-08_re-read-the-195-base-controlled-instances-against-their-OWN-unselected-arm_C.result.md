# Idea 446 — re-read-the-195-base-controlled-instances-against-their-OWN-unselected-arm (lane C, 2026-09-08)

**SPLIT. The queue's premise is WRONG in its arithmetic and RIGHT in its consequence.** 195 is
the count of *all* SHAPE-W BROAD instances, not of `base_*`-controlled ones: `base_*` accounts
for **22 instances over 22 files**, and the record's dominant book-control is `v1_*` (**65**),
then `v2_*` (**40**), then `base_*` (22), then `live_*` (2) — **129 book-controlled instances
over 108 files**, of which **50 carry no unselected-arm reading anywhere in the record**. But
re-priced against their own ladder, those instances' pooled margin falls from **+0.141
[+0.074, +0.209]** to **+0.039 [+0.021, +0.057]** (shift **−0.102 [−0.164, −0.046]**, CI
excluding zero at all six P1×P2 points), and **30 to 39 of 87–91 published instance verdicts —
33.3% to 43.7% — change SIGN.** On live prices the same swap moves the mean margin by
**−0.234** (comparand `v2`) or **+0.281** (comparand `v1`): the record's most-used control is
also its most flattering one. No KEEP (0 of 4 on 4a-vs-v2, 0 of 4 on 4b). `RULES.md`,
`scan.py`, `bot.py`, `baseline.py` untouched.

Script: `research/backtests/2026-09-08_re-read-the-195-base-controlled-instances-against-their-OWN-unselected-arm_C.py`
Artefacts: `.console.txt`, `.premise.csv` (all 195 W instances with their control prefix),
`.recovery.csv` (every book-controlled file, admitted or rejected with reason, + certificate),
`.cells.csv` (9 480 re-priced cells), `.instances.csv` (all 18 grid points), `.flips.csv`
(per-instance published vs re-priced verdict), `.boot.csv`, `.livegrid.csv` (234 books),
`.walkforward.csv` (36 cells × 5 vocabularies), `.keeppaths.csv`.

Two tuned parameters: **P1** ladder-recovery rule ∈ {SHARED-KEYS, DROP-ARM}; **P2** unselected
arm ∈ {LADDER-MEAN, LADDER-MEDIAN, EXCL-MEAN}. All 6 reported, each at 3 reproduction-certificate
thresholds (18 rows). Idea 229's `census()`, vocabularies, admitted shapes, six live ladders and
their declared incumbents, IS/OOS split, costs, cadence, gross, panels and t+1 execution are
imported, not re-chosen.

## (1) Parent reproduced exactly, then the premise audited

| | instances | files | cells | pooled mean margin |
|---|---|---|---|---|
| STRICT (this run) | 104 | 69 | 5 302 | −0.00202 |
| STRICT (idea 229 published) | 104 | 69 | 5 302 | −0.00202 |
| BROAD (this run) | 237 | 119 | 19 308 | +0.15330 |
| BROAD (idea 229 published) | 237 | 119 | 19 308 | +0.15330 |
| shapes BROAD | W 195 / L 42 | | | (parent: W 195 / L 42) |

The 195 SHAPE-W BROAD instances by the control column they actually use:

| control column | instances | family |
|---|---|---|
| `v1_OOS_Sharpe` | **65** | BOOK |
| `v2_OOS_Sharpe` | **40** | BOOK |
| `ctl_OOS_Sharpe` | 34 | ARM |
| `base_OOS_Sharpe` | **22** | BOOK |
| `anchor_OOS_Sharpe` | 17 | ARM |
| `ctrl_OOS_Sharpe` | 13 | ARM |
| `live_OOS_Sharpe` | 2 | BOOK |
| `control_` / `null_` | 1 / 1 | ARM |

**BOOK-controlled 129 over 108 files; ARM-controlled 66 over 64 (= idea 229's STRICT W count).**
The queue's "195 … have `base_*` as their only control" conflates the shape count with the
prefix count; the correct target set is the 129, and the sharpest subset is the **50 instances
(50 files) whose file carries no arm control at all** — those have no unselected-arm reading
anywhere in the record.

## (2) Ladder recovery — coverage and a reproduction certificate, both published

| P1 | files attempted | recovered | cells on a ≥2-arm ladder | median ladder | certificate (mean) | files at 100% |
|---|---|---|---|---|---|---|
| SHARED-KEYS | 108 | **60 (55.6%)** | 6 129 | 16 arms | **96.2%** | 57 / 60 |
| DROP-ARM | 108 | **71 (65.7%)** | 9 480 | 17 arms | **96.7%** | 68 / 71 |

The *certificate* is the honesty check the recovery needs: does the recovered ladder actually
contain the selected arm's own published OOS Sharpe? It does in ~96–97% of cells, so the ladder
being re-priced against is the ladder the selection ran over, not a guess. Rejections, published
rather than hidden (DROP-ARM): 17 files have no committed `<stem>.grid.csv`, 12 have a grid
with no `OOS_Sharpe` column, 6 match no ≥2-arm group, 2 have no structural column outside the
cell key. **34.3% of book-controlled files cannot be re-read at all**; their published verdicts
stand unaudited and are counted as such, never as passes.

## (3) How many published verdicts move — all 18 grid points

| P1 | cert | P2 | inst | cells | mean vs BOOK | mean vs ARM | win book | win arm | **FLIPS** | flip % | shrink % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SHARED-KEYS | 0% | LADDER-MEAN | 73 | 6 129 | +0.14209 | +0.04644 | 63.0% | 78.1% | 25 | 34.2% | 58.9% |
| SHARED-KEYS | 0% | LADDER-MEDIAN | 73 | 6 129 | +0.14209 | +0.03192 | 63.0% | 49.3% | 30 | 41.1% | 52.1% |
| SHARED-KEYS | 0% | EXCL-MEAN | 73 | 6 129 | +0.14209 | +0.05013 | 63.0% | 78.1% | 25 | 34.2% | 58.9% |
| SHARED-KEYS | 50% | LADDER-MEAN | 70 | 6 093 | +0.14846 | +0.04807 | 64.3% | 78.6% | 24 | 34.3% | 58.6% |
| SHARED-KEYS | 50% | LADDER-MEDIAN | 70 | 6 093 | +0.14846 | +0.02739 | 64.3% | 48.6% | 29 | 41.4% | 51.4% |
| SHARED-KEYS | 50% | EXCL-MEAN | 70 | 6 093 | +0.14846 | +0.05200 | 64.3% | 78.6% | 24 | 34.3% | 58.6% |
| SHARED-KEYS | 100% | LADDER-MEAN | 69 | 6 051 | +0.15289 | +0.04874 | 65.2% | 78.3% | 23 | 33.3% | 59.4% |
| SHARED-KEYS | 100% | LADDER-MEDIAN | 69 | 6 051 | +0.15289 | +0.02826 | 65.2% | 49.3% | 29 | 42.0% | 50.7% |
| SHARED-KEYS | 100% | EXCL-MEAN | 69 | 6 051 | +0.15289 | +0.05273 | 65.2% | 78.3% | 23 | 33.3% | 59.4% |
| DROP-ARM | 0% | LADDER-MEAN | 91 | 9 480 | +0.13626 | +0.03830 | 62.6% | 74.7% | 35 | 38.5% | 54.9% |
| DROP-ARM | 0% | LADDER-MEDIAN | 91 | 9 480 | +0.13626 | +0.03087 | 62.6% | 52.7% | 39 | **42.9%** | 49.5% |
| DROP-ARM | 0% | EXCL-MEAN | 91 | 9 480 | +0.13626 | +0.04056 | 62.6% | 75.8% | 32 | 35.2% | 58.2% |
| DROP-ARM | 50% | LADDER-MEAN | 88 | 9 444 | +0.14113 | +0.03931 | 63.6% | 75.0% | 34 | 38.6% | 54.5% |
| DROP-ARM | 50% | LADDER-MEDIAN | 88 | 9 444 | +0.14113 | +0.02723 | 63.6% | 52.3% | 38 | 43.2% | 48.9% |
| DROP-ARM | 50% | EXCL-MEAN | 88 | 9 444 | +0.14113 | +0.04172 | 63.6% | 76.1% | 31 | 35.2% | 58.0% |
| DROP-ARM | 100% | LADDER-MEAN | 87 | 9 402 | +0.14456 | +0.03974 | 64.4% | 74.7% | 33 | 37.9% | 55.2% |
| DROP-ARM | 100% | LADDER-MEDIAN | 87 | 9 402 | +0.14456 | +0.02792 | 64.4% | 52.9% | 38 | **43.7%** | 48.3% |
| DROP-ARM | 100% | EXCL-MEAN | 87 | 9 402 | +0.14456 | +0.04218 | 64.4% | 75.9% | 30 | 34.5% | 58.6% |

**The flip rate never leaves 33.3%–43.7% across every P1, P2 and certificate threshold**, and
the pooled shift never leaves −0.096 … −0.122. Bootstrap over instances (2 000 draws, cert ≥ 50%):

| P1 | P2 | inst | mean vs BOOK [95% CI] | mean vs ARM [95% CI] | shift [95% CI] |
|---|---|---|---|---|---|
| SHARED-KEYS | LADDER-MEAN | 70 | +0.14846 [+0.073, +0.225] | +0.04807 [+0.025, +0.071] | **−0.10071 [−0.170, −0.033]** |
| SHARED-KEYS | LADDER-MEDIAN | 70 | +0.14846 [+0.068, +0.223] | +0.02739 [+0.004, +0.050] | −0.12213 [−0.199, −0.049] |
| SHARED-KEYS | EXCL-MEAN | 70 | +0.14846 [+0.064, +0.221] | +0.05200 [+0.029, +0.076] | −0.09614 [−0.163, −0.027] |
| DROP-ARM | LADDER-MEAN | 88 | +0.14113 [+0.074, +0.209] | +0.03931 [+0.021, +0.057] | **−0.10240 [−0.164, −0.046]** |
| DROP-ARM | LADDER-MEDIAN | 88 | +0.14113 [+0.074, +0.205] | +0.02723 [+0.008, +0.047] | −0.11356 [−0.177, −0.047] |
| DROP-ARM | EXCL-MEAN | 88 | +0.14113 [+0.068, +0.211] | +0.04172 [+0.023, +0.062] | −0.09961 [−0.162, −0.037] |

**R2 is only half-confirmed and the caveat matters.** The arm reading does *not* collapse to
idea 229's STRICT ≈ 0: it lands at **+0.027 … +0.052 with a CI that excludes zero**. That is not
evidence that selecting works — it is the price of the control. A *ladder mean* averages in the
ladder's clearly bad rungs, so it is a weaker comparand than a declared incumbent, which is
usually a defensible arm. Idea 229's −0.0015 is measured against declared incumbents; this run's
+0.04 is measured against ladder averages. **The two are consistent, and the ordering
book ≫ ladder-average > declared incumbent is the finding**, reproduced independently on prices
in §4.

The biggest movers are all `v1`-controlled: `weak-dominance-bands-as-the-calibration-output_C`
+0.4930 → −0.0069, `sleeve-moves-the-frontier_cloud` +0.4796 → −0.0044,
`gross-dispersion-not-gross-level_cloud` +0.4336 → −0.0023,
`gross-as-the-missing-third-bar_B` +0.4024 → −0.0118,
`book-size-floor-for-any-quoted-price_cloud` +0.3880 → −0.0020,
`cagr-floor-calibration_B` +0.3743 → −0.0132. Three move the other way
(`is-a-class-member-just-its-own-ladder-point_B2` −0.0138 → +0.2065,
`correlation-as-the-sleeve-design-variable_B` −0.0337 → +0.1459,
`trend-filter-by-market-cap_B` −0.0386 → +0.0067), so this is a re-reading, not a demolition:
58.6% of the non-flipping instances merely SHRINK.

## (4) Rule 8 on live prices — the same swap, on prices this run computed

Idea 229's pre-registered 36-cell corpus (3 panels × 2 costs × 6 dials, 234 books), choice on
IS ≤ 2016-12-31, 2017–2026 read once, re-priced under five vocabularies:

| control vocabulary | mean margin | chooser wins | 95% CI (cells) |
|---|---|---|---|
| S0 = declared incumbent arm | **+0.07138** | 17/36 | [+0.026, +0.122] |
| ladder MEAN (hold every arm) | +0.03520 | 23/36 | [+0.007, +0.070] |
| ladder MEDIAN arm | +0.01898 | 15/36 | [−0.011, +0.050] |
| book = RULES **v2** | **−0.16217** | **5/36** | [−0.227, −0.098] |
| book = RULES **v1** | **+0.35272** | **29/36** | [+0.244, +0.458] |

**The comparand, not the selector, decides the verdict.** Naming `v1` adds **+0.281** of Sharpe
to the margin; naming `v2` subtracts **−0.234**. The same 36 choices read as "the chooser wins
29 of 36" or "the chooser wins 5 of 36" depending only on which live book the author wrote into
the CSV — and the record's most-used book control is `v1` (65 of 129 instances), the weaker one.
Sign agreement with the incumbent-arm reading: **v2 66.7%, v1 55.6%**, ladder-mean 72.2% — a
33–44% live disagreement rate that lands on top of the record's 33.3–43.7% flip rate, two
corpora agreeing without being fitted to each other.

Both KEEP paths, pooled equal-weight over the 36 cells, t+1, 10 bps rung shown for baselines.
4b bars off the pooled SPY: H1 > 0.959, H2 > 0.834, OOS > 0.882, |MaxDD| ≤ 20.23%, CAGR ≥ 10.66%.

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a v2 | 4a v1 | 4b | failing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 IS-Sharpe chooser | 8.53% | 0.922 | −17.12% | 1.044 / 0.811 | 8.13% | 0.879 | −17.12% | False | True | **False** | H2\|OOS\|CAGR |
| S0 do nothing (incumbent arm) | 6.50% | 0.806 | −15.28% | 0.938 / 0.687 | 6.12% | 0.756 | −15.28% | False | True | **False** | H1\|H2\|OOS\|CAGR |
| LADDER-MEAN (hold every arm) | 7.13% | 0.840 | −16.18% | 0.948 / 0.743 | 6.91% | 0.810 | −16.18% | False | True | **False** | H1\|H2\|OOS\|CAGR |
| ORACLE (OOS argmax — not a rule) | 7.84% | 0.909 | −15.72% | 0.990 / 0.837 | 7.84% | 0.904 | −15.72% | False | True | False | CAGR |
| **SPY** | 15.23% | 0.889 | −33.72% | 0.959 / 0.834 | 15.45% | 0.882 | −33.72% | — | — | — | — |
| **RULES v2 (live) pooled** | 6.96% | 1.021 | −10.92% | 1.084 / 0.961 | 6.95% | 1.038 | −10.92% | — | — | — | — |
| RULES v1 pooled | 4.90% | 0.539 | −18.54% | 0.616 / 0.474 | 5.12% | 0.546 | −18.54% | — | — | — | — |

**0 of 4 on 4a-vs-v2, 0 of 4 on 4b, and 4 of 4 on 4a-vs-v1** — the last line is the whole point
in miniature: every book in the table, including "do nothing", clears the bar when the bar is
v1 (pooled Sharpe 0.539, H1/H2 0.616/0.474) and none clears it when the bar is v2. Nothing here
is capital-worthy: all four fail SPY's H2 and the 4b CAGR floor.

## Verdict

**SPLIT — premise corrected, consequence CONFIRMED.** The 195 figure is a shape count, not a
`base_*` count (`base_*` = 22 instances / 22 files; the real book-controlled set is 129 over 108
files, dominated by `v1_*` 65 and `v2_*` 40, with 50 instances carrying no arm reading anywhere).
Of those, 60–71 files re-read against their own recovered ladder at a 96%+ reproduction
certificate, and **33.3%–43.7% of published instance verdicts change sign at every one of the 18
grid points**, with the pooled margin shifting **−0.102 [−0.164, −0.046]**. On live prices the
comparand swings the same 36 choices by −0.234 (v2) to +0.281 (v1), turning "wins 5 of 36" into
"wins 29 of 36". No KEEP on either path.

## What this run proposes (for the queue, not adopted here)

1. **PROTOCOL should require the control column to be NAMED BY FAMILY, not by prefix.** A
   walk-forward file's comparand is either an ARM of the same ladder or a BOOK; the two answer
   different questions and differ by 0.10–0.28 of Sharpe. Requiring `arm_ctl_OOS_*` vs
   `book_v1_OOS_*` makes every future census exact instead of prefix-guessed.
2. **`v1` should be retired as a comparand.** Pooled Sharpe 0.539 with halves 0.616/0.474 makes
   it the record's most flattering bar; 65 of 129 book-controlled instances use it. Any run
   quoting a v1 margin should quote the v2 margin beside it, or say why v1 is the right question.
3. **Every selection result should publish its ladder.** 34.3% of book-controlled files could not
   be re-read because no `<stem>.grid.csv` (or none with `OOS_Sharpe`) was committed. A one-line
   requirement — commit the arm ladder with per-arm OOS metrics — makes the whole class auditable.
4. The 50 instances with **no arm control anywhere** are the priority back-fill: only 23 of the
   50 files recover a ladder here (20 under SHARED-KEYS), so **27 published verdicts still rest
   on a book comparand alone**, with no arm reading available anywhere in the record.
