# Idea 2034 (lane cloud, 2026-09-20) — IS THE 4b VERDICT ITSELF A 2020 ARTEFACT ONCE THE SPY BAR IS HELD FIXED?

**ANSWERED — YES, ALMOST ENTIRELY. The published census move `4b 187 -> 80 of 420` is a
BENCHMARK ARTEFACT: with the bar frozen the excision LOSES NOTHING (187 of 187 published passes
survive, 100.0%) and would in fact ADD passes. Plus an incidental DUAL-PATH KEEP-candidate.**

Script `research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.py`; evidence
`.grid.csv.gz` (20,160 scored rows), `.attribution.csv`, `.legs.csv`, `.survival.csv`,
`.standing.csv`, `.barshift.csv`, `.costladder.csv`, `.walkforward.csv`, `.gates.csv`,
`.log.txt`, `.console.txt`.

## What was priced

Idea 2022's exact 420-cell vol-target corpus (3 panels x t in {0.08, 0.10, 0.12, 0.16, 0.20} x
T in {W, M} x 14 refresh cells = CAL R in {D, W, M, Q} + DRIFT h in 10 rungs), rebuilt verbatim
(same runners, sigma L=20 d=0, warm-up 260, IS <= 2016-12-31, OOS >= 2017-01-01, 10 bps
headline, t+1, gross capped at 1.00), then scored on a full **3 x 4 cross**:

* **BOOK TAPE** in {FULL, CRASH_PT (2020-02-19 -> 2020-03-23, 24 days), CRASH_WIDE (-> 2020-04-30,
  51 days)} — which days the BOOK is measured on.
* **BAR** in {FULL, CRASH_PT, CRASH_WIDE, ABS} — which days the BENCHMARK (SPY and live RULES v2)
  is read on, **independent of the book's tape**. `ABS` freezes ONE vector (U56's FULL-tape SPY
  and live-v2 legs) and applies it to every panel and tape.

Idea 2022's convention is the **diagonal** of that cross (bar == book tape). The two off-diagonal
cells are what the record had never computed:

| | bar FULL | bar EXCISED |
|---|---|---|
| **book FULL** | 187 (published baseline) | **BAR effect alone** |
| **book EXCISED** | **BOOK effect alone** | 80 (published excised census) |

**Nothing new is tuned.** `t` and `h` (calendar family: `t` and `R`) are ideas 1799/2022's two
inherited dials and the only ones a chooser spends. REPORTED, not tuned, every grid point
published: BAR convention (the axis under test), crash window, trade cadence, panel, cost
{0, 10, 25, 50} bps.

## Gates — 11 of 11 pass

| Gate | Value |
|---|---|
| G0 sample >= 10y | 18.7y |
| G1 `bt_cal` diagonal == `engine.backtest` (returns / turnover) | 0.000e+00 / 0.000e+00 |
| G2 cost identity vs a fresh engine run at 10 / 25 bps | 0.000e+00 |
| G3 reproduces the standing VOLTGT memo (U56 + B136) | max abs d = 4.605e-05 |
| G4 DRIFT h=0 == CALENDAR R=D, 30 cells | 0.000e+00 |
| G5 the 420-cell corpus is rebuilt at full size | 420 |
| G6 reproduces idea 2022's published census EXACTLY | 4b 187 / 80 / 89, 4a 40 / 0 / 0 |
| G7 reproduces 2022's disclosed SPY bar shift (U56) | -33.72% -> -24.50% |
| G8 gross never levered | max 1.000000 |
| G9 both crash windows non-empty on every panel | 24 / 51 days |

## V1 — ATTRIBUTION (10 bps, 420 cells). VERDICT: **BENCHMARK-ARTEFACT**

| metric | crash | base | excised (2022) | total | **BAR** | **BOOK** | interaction | bar share |
|---|---|---|---|---|---|---|---|---|
| keep4b_full | CRASH_PT | 187 | 80 | -107 | **-178** | **+79** | -8 | 69.3% |
| keep4b_full | CRASH_WIDE | 187 | 89 | -98 | **-125** | **+67** | -40 | 65.1% |
| keep4b (full+OOS) | CRASH_PT | 187 | 80 | -107 | -184 | +79 | -2 | 70.0% |
| keep4b_oos | CRASH_PT | 225 | 80 | -145 | -208 | +43 | +20 | 82.9% |
| keep4a | CRASH_PT | 40 | 0 | -40 | **-40** | **+9** | -9 | 81.6% |
| keep4a | CRASH_WIDE | 40 | 0 | -40 | -40 | +1 | -1 | 97.6% |
| keep4a_oos | CRASH_PT | 54 | 0 | -54 | -54 | +10 | -10 | 84.4% |

The BOOK effect is **positive on every metric and every window**: with the benchmark frozen,
deleting the 2020 crash makes **MORE** cells pass, not fewer (+79 on 4b, +9 on 4a). The entire
published collapse, and more, is carried by the bar. The `4a 40 -> 0` line is the extreme case:
**100% of it is the bar** (the book effect is +9, the interaction -9).

The sign and the dominance hold at every cost rung (keep4b_full, CRASH_PT):
0 bps BAR -165 / BOOK +53; 10 bps -178 / +79; 25 bps -164 / +58; 50 bps -127 / +63.

**Why.** Excising 24 days moves the BAR far more than the BOOK because the book's vol target
already cut gross into the crash, so its worst drawdown sits outside the excised window while
SPY's does not. On U56 the cap `0.60 x SPY MaxDD` tightens **-20.23% -> -14.70%** and the floor
`0.70 x SPY CAGR` rises **10.59% -> 12.54%**, while the standing cell's own MaxDD is unchanged at
**-19.39%** on the full tape (`.barshift.csv`, `.standing.csv`).

## V2 — WHICH LEG FLIPS, AND UNDER WHICH EFFECT (10 bps, CRASH_PT)

| leg | passing at base | lost by BAR alone | lost by BOOK alone | mean margin move: bar / book |
|---|---|---|---|---|
| L1_H1 | 343 | 0 | **6** | +0.0125 / -0.0097 |
| L2_H2 | 274 | **195** | 0 | -0.3669 / +0.2488 |
| L3_OOS | 278 | **62** | 0 | -0.3356 / +0.2218 |
| L4_DD | 239 | **129** | 0 | -0.0553 / +0.0297 |
| L5_CAGR | 266 | **87** | 0 | -0.0203 / +0.0145 |

**Four of the five legs lose ZERO cells to the book and hundreds to the bar.** Only L1_H1 loses
anything at all to the book (6 cells of 343), and it is the one leg whose bar move is favourable.
Every mean margin move has the two effects pointing in **opposite directions**.

## V3 — SURVIVAL OF THE 187 PUBLISHED PASSES

| crash | bar = FULL | bar = ABS | bar = OWN (2022's) |
|---|---|---|---|
| CRASH_PT | **187 / 187 (100.0%)** | **187 / 187 (100.0%)** | 77 / 187 (41.2%) |
| CRASH_WIDE | **187 / 187 (100.0%)** | **187 / 187 (100.0%)** | 86 / 187 (46.0%) |

Not one published 4b pass is falsified by the excision once the bar is held fixed, under either
window and under either freezing convention. The standing KEEP-4b candidate (`VOLTGT t=0.10,
T=M, R=M`) clears 4b full and OOS at **11 of its 12** (book tape x bar) cells on U56 and **11 of
12** on B136; the only failures are the pure BAR-only counterfactuals (book FULL / bar excised),
which is the artefact itself. Its excised-book statistics **improve** (U56 13.31% / 1.2437 /
-19.39% -> 14.73% / 1.3954 / -13.57%).

## V4 — RULE 8 (parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE)

288 picks = 3 panels x 3 book tapes x 4 bars x 2 trade cadences x 2 families x 2 legal IS-only
choosers (`CH_ISSHARPE` = argmax IS Sharpe; `CH_ISMINLEG` = argmax min IS 4b-leg slack).

| book tape | bar | 4b FULL+OOS | 4a | reaches the standing cell |
|---|---|---|---|---|
| FULL | FULL | **10 / 24** | 1 / 24 | 2 / 24 |
| FULL | ABS | 10 / 24 | 0 / 24 | 2 / 24 |
| FULL | CRASH_PT | 0 / 24 | 0 / 24 | 2 / 24 |
| FULL | CRASH_WIDE | 2 / 24 | 0 / 24 | 2 / 24 |
| CRASH_PT | FULL | 16 / 24 | 2 / 24 | 2 / 24 |
| CRASH_PT | CRASH_PT | 7 / 24 | 0 / 24 | 2 / 24 |
| CRASH_WIDE | FULL | 16 / 24 | 2 / 24 | 2 / 24 |
| CRASH_WIDE | CRASH_WIDE | 7 / 24 | 0 / 24 | 2 / 24 |

The chooser's PICK never depends on the bar convention at 2 of 24 (it reaches the standing cell
at the same rate everywhere); only the VERDICT does. On the tape capital is actually deployed on
(FULL book, FULL bar) **`CH_ISMINLEG` reaches the standing cell on both large panels at T=M and
it clears 4b full and OOS** — the record's repeated "the cell clears, the chooser does not" does
not hold for this chooser.

**INCIDENTAL — A DUAL-PATH KEEP-CANDIDATE (4a *and* 4b), reached by a legal IS-only chooser.**
`CH_ISMINLEG` on **B136, T=W, DRIFT** picks `t = 0.10, h = 0.08` and that cell clears **BOTH**
KEEP paths on the full tape at 10 bps — the first 4a pass in this family the record has seen:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| **idea (B136, t=0.10, h=0.08, W, 10 bps)** | **12.51%** | **1.2286** | **-11.81%** | 1.3171 / 1.1415 | 13.01% / 1.2928 / -11.81% |
| RULES v2 baseline (live) | 7.96% | 1.0972 | -12.24% | 1.2296 / 0.9669 | 7.85% / 1.1017 / -12.24% |
| SPY | 15.12% | 0.8844 | -33.72% | 0.9571 / 0.8249 | 15.26% / 0.8737 / -33.72% |

4a: H1 +0.0875, H2 +0.1746, MaxDD +0.43 pp better. 4b: all five legs positive
(+0.3600 / +0.3166 / +0.4191 / +8.42 pp / +1.92 pp). Turnover 3.13/yr, 19.8 refreshes/yr, mean
gross 0.777, never levered. Both paths survive 25 bps (4a fails at 50 bps, 4b holds).
Memo: `research/backtests/2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`.

## What it changes

1. **The record must stop quoting "4b 187 -> 80" as evidence against the vol-target family.**
   Any future excision claim must publish the BAR / BOOK / INTERACTION split; a raw census move
   across a re-estimated benchmark is not a statement about the book. This extends idea 2038's
   companion-statistic requirement from the OOS margin to the CENSUS.
2. The standing KEEP-4b candidate keeps its status, now with the 2022 excision objection removed.
3. A new dual-path (4a + 4b) KEEP-candidate is filed for Sunday review.

**Survivorship.** U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first, 54 dropped). Every CAGR
and drawdown LEVEL is optimistic and both 4b bars are easier here than on a point-in-time panel.
The BAR-vs-BOOK contrast is same-tape / same-names / same-grid with only the SCORING convention
moved, so it is first-order immune; the PASS COUNTS are not. The SMALL cache grew 439 -> 665
names on 2026-09-20, so SMALL counts are not comparable with earlier SMALL numbers. The
dual-path cell is 1 of 24 picks on one panel — a multiple-comparison caveat applies and the
memo states it.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.
