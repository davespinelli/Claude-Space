# Idea 1022 (lane B, 2026-09-16) — does `L4_DD`'s TOTAL SPLIT-POINT INERTIA survive a POST-2020 SPLIT?

**ANSWERED = NO. The inertia does not survive, and it was never a property of the leg — it was a property of 1013's window set.**
**But the leg still never DECIDES: once the episode leaves the OOS window `L4_DD` binds nothing at all.**

Tuned dials (2, exactly the ones the queue names, all points reported): END GRID {END_Q = 16 quarter-ends
2019-03-31…2022-12-31, END_Y = 4 year-ends} × PANEL {U56, B136}. Controls at every point: BAR {REC_FULL (the
record's own, SPY FULL-sample MaxDD), WIN (SPY's own OOS-window MaxDD)}, COST {0, 10, 25} bps, CLAIM SET
{SHELF 9 committed passes, GRID 36 never-memo-selected}, ANCHOR E = 2016-12-31. Start pinned at `px.index[260]`.

## Gates — 8 of 8 PASS (printed before any result number)
G1 6.939e-18 / 1.665e-16 · G2 0.000e+00 · G3 SPY OOS at 2016-12-31 15.2102% / 0.8711 / −33.7173% (max|d| 1.702e-04)
· G4 9/9 SHELF memo triples · G5 determinism 0.000e+00 over 2,295 rows · G6 IS purity 0 moved picks
· **G7 1013's two degeneracies reproduce on ITS grid: SPY |OOS MaxDD| range 6.66e-16, `L4_DD` constant 45/45**
· **G8 SPY's OOS trough is the 2020-03-23 crash iff E precedes it — 0 of 32 (panel × E) cells disagree.**

## What the split does to the cap
| E | SPY \|OOS MaxDD\| | trough | cap_WIN | cap_REC_FULL |
|---|---|---|---|---|
| 2019Q1–2019Q4 | 0.3372 | 2020-03-23 | 0.2023 | 0.2023 |
| 2020Q1–2021Q4 | 0.2450 | 2022-10-12 | 0.1470 | 0.2023 |
| 2022Q1 | 0.2128 | 2022-10-12 | 0.1277 | 0.2023 |
| 2022Q2–2022Q4 | 0.1876 | 2025-04-08 | 0.1125 | 0.2023 |

Range **0.1496** against 1013's **0.0000**, in a **single 0.0922 step at 2019-12-31 → 2020-03-31** (next largest
0.0321), identical on both panels. **H_BAR PASS, H_STEP PASS, H_CAPCUT PASS (0.556x).**

## What the split does to the leg and the verdict (END_Q, 10 bps, 45 books, record basis)
| leg | constant | pass rate | binds | pre-crash | post-crash | sole binder |
|---|---|---|---|---|---|---|
| L1_H1 | 1.0000 | 0.9556 | 0.0444 | 0.0444 | 0.0444 | 0.0375 |
| L2_H2 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L3_OOS | 0.7111 | 0.9625 | 0.0375 | 0.0000 | 0.0500 | 0.0250 |
| **L4_DD** | **0.8667** | 0.9667 | **0.0333** | **0.1333** | **0.0000** | 0.0333 |
| L5_CAGR | 0.5778 | 0.7736 | 0.2264 | 0.1944 | 0.2370 | 0.2181 |

`L4_DD` constant on **39/45** (record basis; all **6/0** flips FAIL→PASS) and **19/45** (OOS-window basis; **6
easier / 16 harder**) — **H_INERT FAIL, H_INERT_W FAIL**, panels straddle the bar (U56 0.8400, B136 0.9000,
**H_PANEL FAIL**). 4b verdict constant on only 21/45 (**H_VERDICT FAIL**), but that movement is carried by
`L5_CAGR` and `L3_OOS`, not the cap (**H_BIND FAIL**, +0.0481 against a +0.10 bar). All 9 committed SHELF passes
hold 4b at **15–16 of 16** post-2020 ends on the record's basis and only **7–14 of 16** on the OOS-window basis.

## Rule 8 (mandatory) at PROTOCOL's own split, pool GRID, 10 bps
| panel | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE / IS_LEGS | U56-band0.08-g1.00 | 11.99% | 1.162 | −19.05% | Y | n |
| U56 | IS_CAGR | U56-qroll-q0.17-w1008-d0.50 | 15.60% | 1.293 | −15.59% | Y | n |
| B136 | IS_SHARPE / IS_LEGS | B136-band0.08-g1.00 | 11.05% | 1.097 | −19.50% | Y | n |
| B136 | IS_CAGR | B136-qroll-q0.12-w1008-d0.50 | 14.30% | 1.157 | −17.31% | Y | n |
| U56 | SPY | comparand | 15.21% | 0.871 | −33.72% | — | — |
| U56 | RULES v2 (live) | baseline | 9.45% | 1.276 | −12.05% | — | — |
| B136 | SPY / RULES v2 | comparands | 15.33% / 7.88% | 0.877 / 1.106 | −33.72% / −12.24% | — | — |

OOS 4b 6 of 6, OOS 4a 0 of 6. Both KEEP paths over the 765-row 10 bps ladder: 4a **17 rows, 1 book**
(`B136-band0.08-g0.50`, at every end); 4b at the anchor **28 of 45**, over the 720 post-2020 rows **484**
(record basis) / **382** (OOS-window basis). **No new KEEP book is claimed** — this run prices an existing leg.

## Verdict
**KILL** "`L4_DD`'s total split-point inertia is a property of the leg" and **KILL** "the DD cap is
split-invariant". **KEEP a PROTOCOL rule 4 DD-CAP EPISODE STAMP clause, proposed not applied**:
`2026-09-16_dd-cap-episode-stamp-clause_B.memo.md`. RULES.md, PROTOCOL.md, `scan.py`, `bot.py`, `baseline.py`
unmodified (rule 6). Survivorship (rule 9): current-constituent panels, so levels are optimistic and the
measured instability is a LOWER bound.
