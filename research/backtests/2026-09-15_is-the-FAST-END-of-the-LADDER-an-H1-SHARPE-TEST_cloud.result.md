# Idea 986 (cloud, 2026-09-15) — is the FAST END of the ladder an H1-SHARPE test the way the SLOW END is a DRAWDOWN test?

**ANSWER = NO. `L4_DD` is still the best single-leg reading at D/W (AGREE 0.730 / MCC 0.4025 vs
`L1_H1`'s 0.670 / 0.3328), and `L1_H1` is the ONLY failed leg on just 0.050 of D/W books against
`L4_DD`'s 0.388 at M/Q. What actually happens at speed is that 4b stops having a single-leg
reading at all — it becomes a multi-leg test. KILL for "the fast end is an H1-Sharpe test".
Second KILL, bigger: at EVERY one of the 18 (half × leg-definition) points the best single-leg
reading scores BELOW the majority-class base rate (lift −0.0032 … −0.2000), M/Q's celebrated
`L4_DD` included. Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`,
`baseline.py` untouched.**

## The grid

Rebuilt from scratch, not re-read: 3 panels {U56 56, B136 136, SMALL 664−52} × 5 books
{TOP05, TOP10, TOP20, EWELIG, BAND03} × 2 gross {CORE 0.75, EXT 1.00} × D/W/M/Q at **matched
gross** × every rebalance phase (1/5/21/63) = **2,700 phase-books** × 5 cost rungs =
**13,500 rows**, plus 36 rule-8 picks. Two tuned axes only — ladder half {FINE2 = D/W,
COARSE2 = M/Q, D, W, M, Q} × leg definition {REC, ISONLY, OOSLOC} — **all 18 points reported,
none selected**; all five cost rungs built and reported.

## Why fail rate could never answer this

Idea 984's number is a **fail rate**: `L1_H1` goes 0.293 (M/Q) → 0.580 (D/W). A leg can fail
0.58 of the time and be worthless as a reading if its failures do not line up with the 4b
verdict. So this run prices the reading itself: `AGREE` = P(leg verdict == 4b verdict), and,
because `AGREE` is inflated wherever 4b almost never passes, `MCC` (Matthews φ, base-rate
robust) and `lift` (AGREE − majority-class rate) beside it at every point.

## The census, 10 bps, cadence-balanced (REC legs)

| half | leg | fail | bind | **only** | modal (tie) | modal (strict) | **AGREE** | **MCC** | lift |
|---|---|---|---|---|---|---|---|---|---|
| D/W | `L1_H1` | 0.580 | 0.629 | **0.050** | 0.667 | 0.167 | 0.670 | 0.333 | −0.202 |
| D/W | `L2_H2` | 0.533 | 0.588 | 0.003 | 0.500 | 0.000 | 0.623 | 0.321 | −0.249 |
| D/W | `L3_OOS` | 0.560 | 0.615 | 0.000 | 0.500 | 0.000 | 0.650 | 0.330 | −0.222 |
| D/W | **`L4_DD`** | 0.640 | 0.707 | 0.097 | 0.500 | **0.333** | **0.730** | **0.403** | −0.142 |
| D/W | `L5_CAGR` | 0.483 | 0.530 | 0.130 | 0.333 | 0.000 | 0.573 | 0.281 | −0.299 |
| M/Q | `L1_H1` | 0.293 | 0.312 | 0.000 | 0.000 | 0.000 | 0.351 | 0.159 | −0.603 |
| M/Q | **`L4_DD`** | 0.879 | 0.933 | **0.388** | 0.667 | 0.667 | **0.937** | **0.669** | −0.016 |

Base rate (4b fails) 0.872 at D/W, 0.954 at M/Q. Every `fail` and `only` cell here reproduces
idea 984's committed table to 4 decimals (G3a below).

**Three things the fail rate hid.** (1) `L1_H1` never takes the reading: `L4_DD` beats it on
AGREE and on MCC at D/W. (2) `L1_H1`'s failures are almost never *decisive* — only-failed-leg
0.050, an eighth of `L4_DD`'s 0.388 at M/Q, so there is no fast-end mirror of the slow-end
object. (3) 984's "modal on half the D/W cells" is a **tie** artefact: under a strict outright
maximum `L1_H1` is modal on 0.167 of D/W cells and `L4_DD` on 0.333. 984 published a `modal`
row without naming its cell or tie rule; both rules are published here.

## Sensitivity — all 18 points

`L4_DD` is the best-AGREE and best-MCC leg at **15 of 18** points. `L1_H1` wins at exactly
three: **D alone**, under all three leg definitions (AGREE 0.767 / 0.800 / 0.733, MCC 0.308 /
0.000 / 0.378) — and at every one of those points it sits far below the 0.90 bar with lift
−0.200. The "single-leg reading" bar (AGREE ≥ 0.90) is cleared at only 6 of 18 points, all of
them M, Q or M/Q, all of them `L4_DD`, and none under the ISONLY leg definition. Across cost rungs the D/W best leg is `L4_DD` at 0/5/10 bps,
`L3_OOS` at 25 and `L5_CAGR` at 50 — it is never `L1_H1` at any rung.

## The second KILL, which is the one that matters for the record

**`lift` is negative at all 18 points** (best: M/Q `L4_DD` at −0.0163; Q at −0.0032). A rule
that predicts "4b fails" unconditionally beats the best single-leg reading everywhere on this
ladder, at both ends. `L4_DD`'s M/Q AGREE of 0.937 is 0.954-base-rate arithmetic, not a
finding. Only the MCC column carries real signal, and it separates the ends cleanly —
**M/Q 0.669 vs D/W 0.403** — so the honest statement is *"4b's DD leg discriminates roughly
1.7× better at M/Q than at D/W"*, not *"4b is a DD test at M/Q"* and certainly not *"4b is an
H1 test at D/W"*.

## Rule 8

36 picks = 3 panels × 4 cadences × 3 IS-only choosers, (book, gross) chosen on **2009–2016
alone**, 2017–2026 read once. **OOS 4b 4 of 36, OOS 4a 0 of 36.** All four 4b passes are one
object — **U56 / `BAND03` / gross 1.00, D 12.45% / 1.287 / −14.77% and W 12.67% / 1.276 /
−15.91%** — the same book ideas 973, 981, 982 and 984 each surfaced and each declined. **This
is the fifth arrival and the fifth refusal:** 4a fails on every panel because gross 1.00 buys
+34% full-sample CAGR (8.62% → 11.53% on U56/W) for +32% drawdown (−12.05% → −15.91%) at an
unchanged full-sample Sharpe (1.2009 → 1.2007). Comparands: **SPY OOS
15.21% / 0.8713 / −33.72%**; RULES v2 (live) full-sample Sharpe / MaxDD U56 1.2009 / −12.05%,
B136 1.0994 / −12.24%, SMALL 0.6637 / −13.89%. Full sample over the 120 phase-0 books at
10 bps: 4b **7**, 4a **0**.

## Gates — 7 of 8 PASS, printed before any result number

G0 `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on D/W/M/Q, 0 rows. G1 fast `Ctx` ≡
`engine.backtest` on returns AND turnover post warm-up, D and M, max|d| **2.498e-16**.
G2 `BAND03@0.75` ≡ `baseline.rules_v2_weights` **0.000e+00**. **G3a CROSS-RUN: idea 984's
published `fail` and `only` re-score rows reproduced on 14 of 14 cells, max|d| 4.34e-04
(rounding).** G4 matched gross: 30 (panel, book, gross) target matrices built once and reused
across all four cadences, so cadence cannot move the target by construction. G5 determinism
0.000e+00. G6 every rule-8 chooser IS-only, 0 disagreements under permuted OOS columns.
**G3b FAILS, stated not hidden:** 984's two `modal` rows (`L4_DD` M/Q 1.000, `L1_H1` D/W
0.500) do not reproduce under either tie rule at (panel, cadence) cells — this run reads
0.667/0.667 and 0.667/0.167. 984 published no cell or tie definition for that row, so this is
a **definitional** gap, not a numerical one; every number this run's answer rests on is in the
G3a set, which reproduces exactly.

## Survivorship (rule 9)

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is optimistic
and every leg fail rate is a LOWER bound. The object measured here is a **comparison between
two halves of one ladder** — same names, same tape, only the rebalance schedule moves — and is
very nearly immune. The rule-8 4b levels are read against SPY, which is not
survivorship-inflated, so every 4b PASS is an upper bound and every FAIL is understated.

## Limits, stated

`AGREE`/`MCC` are measured against the record's own 4b verdict, so they price a leg as a
*reading of 4b*, not as an economic fact. The `modal` cell is (panel, cadence) by choice; a
different cell could move that column and both tie rules are published because of it. SMALL's
664 columns include names with short histories, which is why its D/W books fail four and five
legs at once.

## Follow-ups filed

989 (does the MCC gap 0.669 → 0.403 survive a gross-matched, turnover-matched control?),
990 (is `lift < 0` at every point a property of this ladder or of the 4b bar itself?),
991 (`modal` needs a published cell and tie rule — the sibling of 984's cadence clause).
