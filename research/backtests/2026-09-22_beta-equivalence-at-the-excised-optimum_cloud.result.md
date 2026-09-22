# Idea 916 (lane cloud, 2026-09-22) — the record's "NOT A BETA CAP" verdicts at the excised optimum

**ANSWER, in three parts.  (a) The verdict FLIPS, and by a lot — but on SMALL, not where the
record looked.  (b) Idea 912's headline MOVE (B136 0.4366 -> 0.6104) does NOT reproduce on an
independently built shelf and, worse, the fitted cap is an INTERVAL, not a point, so a b*
quoted to four decimals is over-read on every panel.  (c) The cap SOURCE is not bookkeeping: on
U56 it is the difference between a 4b candidate and nothing.**

Script: `2026-09-22_beta-equivalence-at-the-excised-optimum_cloud.py` (offline, deterministic).
Tuned dials, exactly two: CAP SOURCE (DECLARED 0.60 / FIT_FULL / FIT_EXC) x PANEL (U56 / B136 /
SMALL).  Reported, not tuned: a 48-book shelf per panel (BAND 4x4, TOPN 4x4, VOLTGT 4x4 — the
record's own families), costs 0/10/25/50 bps, cap grid 0.05..1.50 step 0.01, execution t+1,
warm-up 260, IS <= 2016-12-31, OOS >= 2017-01-01 read once.  **All 576 book-cost rows are in
`.books.csv` and all 36 admission rows in `.capgrid.csv`.**

Excision convention: the 2020 CALENDAR YEAR's rows are dropped from the book, from SPY and from
the SPY-derived 4b cap alike, and the remainder compounded through the gap.  It moves SPY's worst
decline from −33.72% (24d, 2020) to −24.50% (196d, 2022) and the 4b DD cap from −20.23% to
−14.70%, reproducing idea 912's starting point exactly.

## (1) THE FITTED CAP — the move is smaller than the record thinks, and partly unresolvable

| panel | b* WITH 2020 (agree) | maximising interval | b* EXCISED (agree) | maximising interval | b* on IS 2009–16 |
|---|---|---|---|---|---|
| U56 | 0.5400 (1.0000) | [0.54, 0.60] | 0.5700 (0.9583) | [0.57, 0.63] | 0.5300 |
| B136 | 0.5700 (0.9375) | [0.57, 0.58] | 0.5400 (0.9583) | [0.54, 0.54] | 0.5800 |
| SMALL | 0.2100 (0.9375) | [0.21, 0.33] | 0.4100 (0.9583) | [0.41, 0.41] | 0.4900 |

b* rises on 2 of 3 panels (U56 +0.03, SMALL +0.20) — but **FALLS on B136**, the very panel idea
912 measured, and my with-2020 B136 fit is 0.5700, not 912's 0.4366.  The fitted cap is a
SHELF object: change the 48 books and it moves by more than the excision does.

**Read the plateau before the move.** The maximising cap is an interval on every panel and
window (widths 0.06 / 0.01 / 0.12 with 2020; 0.06 / 0.00 / 0.00 excised).  On U56 the two
intervals OVERLAP by 0.03, so U56's "+0.03 move" is inside the resolution of its own fit and is
**not a measurement**.  Only 2 of 3 panels give a resolvable move (GATE G2b).  PROTOCOL's
declared 0.60 lies inside the maximising interval on **1 of 3** panels with 2020 and **1 of 3**
excised — the declared number is not the fitted one, on either reading.

**And rule 8 has been fitting the crash-free cap all along.** The IS window 2009–2016 contains no
2020, so a cap fitted under rule 8 is already an excised cap: b*(IS) = 0.53 / 0.58 / 0.49 at
agreement 0.958 / 0.979 / 0.938.  The with-2020 fit is the outlier, not the excised one.

## (2) THE FLIP CENSUS — the verdict flips decisively, on SMALL

Agreement between `beta <= cap` and the 4b DD leg, over 48 books at 10 bps:

| panel | record's reading (declared 0.60, with 2020) | at the excised optimum | MCC before -> after |
|---|---|---|---|
| U56 | **1.0000** | 0.9583 | +1.0000 -> +0.9075 |
| B136 | 0.9167 | **0.9583** | +0.8284 -> +0.9178 |
| SMALL | **0.6667** | **0.9583** | +0.4880 -> +0.9129 |

Book by book: on SMALL the predicate disagreed with the DD leg on **16 of 48** books under the
record's reading and on **2 of 48** at the excised optimum — **14 verdicts flip to agreement**.
On B136, 2 flip to agreement and 0 the other way.  On U56, 0 flip to agreement and 2 flip AWAY
— because on this shelf U56's DD leg was ALREADY exactly a beta cap with 2020 in (agreement
1.0000, MCC +1.0000), so there was no "not a beta cap" verdict there to rescue.

So the honest restatement of the record's verdict is: **"the 4b DD leg is not a beta cap" was
never a statement about beta; it was a statement about which panel and which crash.**  At the
excised optimum the leg is a beta cap to 0.9583 on all three panels at once — the only reading
on which the three panels agree.

## (3) THE CAP AS CAPITAL — rule 8, OOS read once

Admission rule: keep books with **IS** beta <= cap (legal, IS-only), then the legal IS-only
max-IS-Sharpe chooser; 2017–2026 read once.  At 10 bps:

| panel | cap source | cap | admitted | pick | FULL | OOS | 4b |
|---|---|---|---|---|---|---|---|
| U56 | DECLARED | 0.60 | 36 | top5_g0.75 | 27.3% / 1.208 / −26.8% | 29.8% / 1.168 / −26.8% | **FAIL** |
| U56 | FIT_FULL | 0.54 | 34 | top5_g0.50 | 17.96% / 1.202 / −18.48% | **19.69% / 1.161 / −18.48%** | **PASS** |
| U56 | FIT_EXC | 0.57 | 34 | top5_g0.50 | 17.96% / 1.202 / −18.48% | **19.69% / 1.161 / −18.48%** | **PASS** |
| B136 | all three | 0.54–0.60 | 29–34 | top10_g0.50 | 14.87% / 1.116 / −18.81% | 14.90% / 1.004 / −18.81% | **PASS** |
| SMALL | DECLARED / FIT_FULL / FIT_EXC | 0.60 / 0.21 / 0.41 | 29 / 8 / 21 | volt0.12 at g 0.75 / 0.25 / 0.50 | 5.2% / 0.596 / −30.8% .. 1.8% / 0.597 / −11.1% | 0.365–0.367 Sharpe | FAIL |

**The cap source moves the pick on 2 of 3 panels (GATE G5), and on U56 it moves it across the
4b line:** PROTOCOL's own declared 0.60 admits a gross-0.75 book that fails the DD leg at −26.8%,
while either fitted cap admits the gross-0.50 twin that passes.  5 of 9 admission-rule books
clear 4b FULL+OOS; **4a is 0 of 9** at every rung.  Counts are identical at 0/10/25/50 bps.

## WHAT THIS TEST CANNOT DO (stated, not repaired)

One shelf (48 books, three families), one excision window (the 2020 calendar year), one beta
estimator (full-window OLS on daily returns, no lead/lag), one split point.  Beta here is a
FULL-window scalar, so it cannot see a book whose beta moves; a rolling-beta cap is a different
object and is untested.  All three panels are current-constituent lists and SMALL is the worst
(names sub-$2B today that have priced since 2010; the 54 tickers with `max_1d_move >= 1.0` were
dropped first), so survivors' drawdowns are systematically shallow, which pushes a fitted cap
DOWN — the direction tested here is if anything understated.

## RESIDUE (not a rules change; rule 6)

(1) Every committed b* in the record should carry its maximising INTERVAL: on this evidence
0.4366 and 0.6104 can be the same measurement, and on U56 they demonstrably are.
(2) The record's "not a beta cap" verdict should be re-stated as panel-and-crash-specific; at
the excised optimum the agreement is 0.9583 on all three panels.
(3) PROTOCOL 4b's declared 0.60 is not the fitted cap on 2 of 3 panels, and on U56 it is the cap
that misses the 4b candidate — a Sunday review that ever wants a beta clause should fit it, not
declare it.
