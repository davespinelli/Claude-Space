# Idea 1215 (lane C, 2026-09-18) — how many committed CENSUS HEADLINES have NEVER been TRACED TO A VERDICT?

**ANSWERED = (B) PARTLY TRACED — and the part that IS traced overwhelmingly reports NOTHING MOVED.**
Capital verdict **KILL (capital)** for any RULES change (4a passes **0 of 198** cells; SMALL passes
4b **0 of 66**), plus a **KEEP-4b re-confirmation** of the standing 2026-09-04 / 1294 incumbent and a
**second-panel 4b corroboration** on B136. No RULES change, no PROTOCOL edit (rule 6); RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Runtime 37.5s, offline, deterministic.
SELECTION: 1215 was the SECOND numbered item standing in '## Open' (1288 is lane A's), price-only.

## THE TWO DIALS AND NO MORE (rule 4)
`HEADLINE SET` {H_STRICT, H_LOOSE, H_NUM} x `TRACE RULE` {T_IDNUM, T_FRAC, T_ANY} = **9 cells,
all nine published** in `.trace.csv`. Reference cell (fixed before the run) = H_STRICT x T_IDNUM.
ARM B's `N` x `GROSS` grid is not a third dial: it is the record's own two published axes,
reported at **every one of its 198 cells**, argmaxed only by idea 1294's frozen rule-8 chooser.

## (A) THE CENSUS — 35,674 committed units under research/ (LEADERBOARD rows, CHANGELOG paragraphs, 1,233 .md files)

| HEADLINE_SET | TRACE_RULE | headlines | traced | share | NEVER traced | NONZERO | ZERO | AMBIG |
|---|---|---|---|---|---|---|---|---|
| H_STRICT | **T_IDNUM (ref)** | **2557** | **1014** | **0.3966** | **1543** | 126 | 219 | 669 |
| H_STRICT | T_FRAC | 2557 | 1440 | 0.5632 | 1117 | 126 | 87 | 1227 |
| H_STRICT | T_ANY | 2557 | 1825 | 0.7137 | 732 | 127 | 154 | 1544 |
| H_LOOSE | T_IDNUM | 4761 | 2043 | 0.4291 | 2718 | 253 | 473 | 1317 |
| H_LOOSE | T_FRAC | 4761 | 2807 | 0.5896 | 1954 | 210 | 175 | 2422 |
| H_LOOSE | T_ANY | 4761 | 3555 | 0.7467 | 1206 | 232 | 327 | 2996 |
| H_NUM | T_IDNUM | 8655 | 3550 | 0.4102 | 5105 | 441 | 797 | 2312 |
| H_NUM | T_FRAC | 8655 | 5224 | 0.6036 | 3431 | 360 | 316 | 4548 |
| H_NUM | T_ANY | 8655 | 6458 | 0.7462 | 2197 | 404 | 543 | 5511 |

**1,543 of 2,557** committed census headlines have **never** been followed to a verdict by any later
unit that names their idea. The traced share is stable in the headline dial (0.3966 / 0.4291 / 0.4102)
and moves only in the trace dial (0.3966 -> 0.7137), i.e. the record's traceability is a fact about
**how loosely you let a later unit count as a trace**, not about which headlines you harvest.

**AND THE TRACE USUALLY FINDS NOTHING.** Of the 1,014 traced at the reference cell only 345 read
unambiguously, and of those **219 report ZERO verdict movement against 126 NONZERO — 0.6348 of
followed alarms moved nothing.** The share is identical across every headline set (nonzero share of
traced 0.1243 / 0.1238 / 0.1242 at T_IDNUM), so this is a property of the record, not of the frame.
1207's and 1209's zero-change traces were **typical, not lucky**.

## (B) THE CAPITAL ARM — 198 real books, both KEEP paths at every cell
3 panels x N {5,10,15,20,25,30} x GROSS {0.30..0.80 step 0.05}. FROZEN at the incumbent's
construction: H = 126 min hold, weekly, t+1, 10 bps, above-200d + vol20 < 0.60, equal weights,
260-row warm-up. All three committed U56 anchors replay to **< 7e-4** (gates G4): N=20 g=0.75
15.79% / 1.1529 / -19.13%, N=20 g=0.65 13.66% / 1.1526 / -16.73%, N=15 g=0.60 13.67% / 1.1712 / -16.38%.

**4a passes 0 of 198.** **4b (full) passes 50 of 198** — U56 **25**, B136 **25**, SMALL **0** — the
same 25/25/0 split idea 1294 found over its wider gross range, so the passes live inside 0.30..0.80
and nothing was hiding at the ends. Among the 148 failures the binder is the CAGR floor alone on 58,
the DD cap alone on 32, both on 56 and the halves alone on 2. Annual one-way turnover 1.088..4.805.

## (C) RULE 8 — both dials chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE

| panel | pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | SPY OOS | RULES v2 OOS | 4a | 4b full | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|
| U56 | N=15 g=0.60 | 13.66% / 1.1706 / -16.38% | 1.2591 / 1.1149 | **15.12% / 1.1947 / -16.38%** | 15.28% / 0.8747 / -33.72% | 9.47% / 1.2781 / -12.05% | FAIL | **PASS** | **PASS** |
| B136 | N=25 g=0.60 | 13.07% / 1.0965 / -17.56% | 1.2770 / 0.9572 | **13.38% / 1.0624 / -17.56%** | 15.33% / 0.8769 / -33.72% | 7.88% / 1.1061 / -12.24% | FAIL | **PASS** | **PASS** |
| SMALL | N=25 g=0.40 (IS 4b set EMPTY — documented fallback) | 4.57% / 0.5238 / -20.22% | 0.7789 / 0.3351 | 3.60% / 0.4089 / -20.22% | 15.33% / 0.8769 / -33.72% | 4.47% / 0.6518 / -12.18% | FAIL | FAIL | FAIL |

U56's rule-8 pick **re-derives the standing incumbent independently** (idea 1294 chose N=15/g=0.60 on
a wider gross ladder; this run's narrower ladder and its own IS chooser land on the same cell). B136
reaches a **different breadth at the same gross** and also clears 4b in full and out of sample — the
first time the family has been certified on a second panel by an IS-only chooser. SMALL remains
**0 of 66**: on sub-$2B names this family is not a book at any (N, gross) rung tested.

## (D) THE CAPITAL VERSION OF 1215's OWN QUESTION — and it answers the OPPOSITE way
ALARM = a cell whose **IS joint 4b margin sits within a band of zero** (the thin-margin headline the
record publishes constantly). FOLLOWING it = reading the same cell out of sample. MOVED = IS 4b
verdict != OOS 4b verdict. All three bands published:

| band | ALL: n_alarm / n_calm | moved(alarm) | moved(calm) | lift |
|---|---|---|---|---|
| 0.5 pp | 22 / 176 | **0.5455** | 0.0909 | +0.4545 |
| 1.0 pp | 38 / 160 | **0.4737** | 0.0625 | +0.4112 |
| 2.0 pp | 70 / 128 | **0.3714** | 0.0156 | +0.3558 |

Per panel at 1.0 pp: U56 0.4211 vs 0.1489, B136 0.5263 vs 0.0638, SMALL 0 alarmed cells (its margins
are nowhere near the bar). **So in the money the alarm is worth following and in the text it is not:**
a thin-margin cell flips its 4b verdict out of sample roughly 8x as often as a calm one, while a
thin-margin *headline* followed in the record moved nothing 0.6348 of the time. Part of the capital
lift is **mechanical** — a margin near zero is by construction closer to crossing — so read the
lift as a floor on how much a thin-margin flag is worth, not as a discovery. The asymmetry is still
the finding: the record spends its census effort flagging text and almost never prices what it flags.

## CAVEATS
- The census is a TEXT MATCHER. H_STRICT's failure frame also catches gate tallies ("5 of 7 PASS"),
  which is exactly why all three headline sets are published and no verdict is read off one row.
- 669 of 1,014 traces are AMBIGUOUS (the tracing text carries both a zero and a non-zero token).
  The 0.6348 zero-share is over the 345 that read cleanly and should be quoted with its denominator.
- "Later" is ordered by committed date, falling back to idea number; units whose date and idea number
  are both unreadable cannot be ordered and cannot trace anything.
- SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents; delisted and acquired names are
  absent, which flatters every momentum book here. 2009-2026 is a US-large-cap-favourable regime and
  only 2020 and 2022 are real stress.
- 4a passes 0 of 198 and the live book's OOS Sharpe (1.2781 on U56) still beats every cell here; the
  4b case is a CAGR-and-drawdown case against SPY, not a Sharpe case against the live rules.

## ARTIFACTS
`.py` `.trace.csv` (9 census cells) `.census.csv.gz` (2,557 reference-cell headlines) `.grid.csv`
(198 books) `.walkforward.csv` `.alarm.csv` `.gates.csv` `.console.txt` `.memo.md`
