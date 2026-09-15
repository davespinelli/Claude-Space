# Idea 891 — does the MARGIN-OVER-SPREAD clause EMPTY THE SHELF on the record's COMMITTED 4b passes?

**ANSWERED: NO. It empties two thirds of it, not all of it — 3 of 9 committed 4b passes survive, and
all 9 are bound by the SAME leg (DD). Idea 879's "18 of 18 flip" does NOT reproduce as "none
survive" on the real record. KILL for capital (no new book; the clause is a screen, not an edge).**
Cloud lane, 2026-09-15, idea 1 of 2. Gates 4/4.

## Gates (printed before any new number was read)
| gate | result |
|---|---|
| G1 all 9 SHELF books reproduce their committed memo triple | **PASS** (worst dCAGR 0.0027, dSharpe 0.0240, dMaxDD 0.0109 — `u56-top20-band-m20`) |
| G2 k=0 offset mask == `engine.rebalance_mask` | **PASS** (elementwise) |
| G3 `fast_run(k=0)` vs `engine.backtest` | **PASS**, max abs return diff **8.674e-18** |
| G4 SPY comparand vs the record's committed triple | **PASS** — 15.13% / 0.885 / −33.72% vs 0.1513 / 0.886 / −0.3372 |

## What was priced
The clause idea 879 proposed: a 4b leg counts only if `margin at the published calendar / spread of
the same statistic across the whole rebalance calendar >= 1`, and a book survives only if that holds
on **every** leg. Priced here on the record's **committed, memo-backed 4b passes** (9 books: 861's
8-book shelf plus idea 879's own `u56-top20-g065-M`, 2026-09-15), each walked over its own cadence's
offsets (k = 0…4 weekly, k = 0…20 monthly; k = 0 is the published calendar). Comparands are held at
their own conventions: SPY has no rebalance calendar, and RULES v2 is scored on the live book's
weekly calendar, not the candidate's. 514 (set × book × offset × rung) cells in `.arms.csv`; every
grid point reported. Tuned dials: **pass set** (SHELF headline / GRID control) × **offset grid**.
Cost rung {10, 25} bps and the 21-sleeve ENSEMBLE are reported controls, not dials.

## 1. The headline — the clause is discriminating, not empty and not vacuous
All 9 committed passes pass 4b at their own published calendar. **7 of 9 pass at every offset of
their own cadence**; 2 do not (`u56-band008-gross100` 4/5, `u56-quantile50-respread-M` 4/21). But
passing everywhere is not the clause: the clause asks whether the margin is bigger than the spread,
and there **3 of 9 survive** at 10 bps:

| book | min-ratio | binding leg | DD margin / spread | clause |
|---|---|---|---|---|
| u56-k8-qroll-q017-w1008-d100-g100 | **1.925** | DD | +5.439 / 2.825 pp | **PASS** |
| u56-v2band-gross100 | **1.792** | DD | +4.319 / 2.410 pp | **PASS** |
| b136-r620-gross065-W | **1.040** | DD | +0.797 / 0.766 pp | **PASS** |
| b136-qroll-q012-w1008-d050-g100 | 0.970 | DD | +2.915 / 3.005 pp | FAIL |
| u56-marsrespread-gross075 | 0.918 | DD | +1.583 / 1.724 pp | FAIL |
| u56-top20-g065-M | 0.485 | DD | +3.121 / 6.434 pp | FAIL |
| u56-band008-gross100 | 0.535 | DD | +1.180 / 2.206 pp | FAIL |
| u56-top20-band-m20 | 0.465 | DD | +1.922 / 4.137 pp | FAIL |
| u56-quantile50-respread-M | 0.157 | DD | +0.478 / 3.046 pp | FAIL |

Median min-ratio **0.918**. `H_EMPTY` (0 survivors) **FAILS**: 879's synthetic ladder result is
stronger than the record's own. Note what the survivor list is: the two highest ratios are the
record's **least tuned** books — the live-rules band at full gross, and the k=8 QROLL gate — while
idea 879's own freshly-selected `u56-top20-g065-M` lands at **0.485**, i.e. its published 3.12 pp DD
margin is less than half its own 6.43 pp calendar spread.

## 2. The binding leg is DD on 9 of 9 — the one unanimous result in the run
`H_DD` **PASSES**, and unanimously: every one of the nine books' smallest ratio is the drawdown leg.
The Sharpe legs are not close to binding (H1 ratios 1.31–5.07, H2 1.58–10.01, OOS 1.84–11.18) and
the CAGR leg binds on none (1.04–4.58). 879 measured the DD leg's calendar spread at 5.8× the CAGR
leg's on its ladder; on the committed shelf the DD spread is **0.77–6.43 pp against CAGR's
0.41–1.55 pp**, same ordering, every book. Whatever else the clause is, it is a drawdown clause.

## 3. The clause's answer moves with the cost rung — `H_RUNG` FAILS
Survivors at 10 bps: `b136-r620-gross065-W`, `u56-k8-qroll-q017-w1008-d100-g100`,
`u56-v2band-gross100`. At 25 bps: the first drops out (3 → 2). Its 10-bps ratio is **1.040** — the
clause's bar cuts through it. A screen whose verdict on a book turns on 15 bps of assumed cost is
not measuring calendar robustness at that book; it is measuring the distance to a bar.

## 4. Rule 8 (PROTOCOL rule 8) — choose on 2009–2016, evaluate on 2017+ untouched
Both IS-only choosers (max IS min-ratio; max IS Sharpe, the control) pick the **same** SHELF book,
`b136-r620-gross065-W`, with no sight of the OOS window:

| | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| pick, OOS 2017+ | **14.52%** | **1.040** | **−19.43%** |
| SPY, OOS 2017+ | 15.33% | 0.877 | −33.72% |
| RULES v2 (live), OOS 2017+ | 7.88% | 1.106 | −12.24% |

OOS **4b PASS**, OOS **4a FAIL**, full-sample 4b PASS, full-sample clause PASS (1.04). The GRID
control's chooser picks `B136-band0.08-g1.00`: OOS 11.05% / 1.097 / −19.50%, OOS 4b PASS, OOS 4a
FAIL — but full-sample clause **FAIL** at min-ratio 0.34, so the IS min-ratio does not carry to the
full sample there. Across all 45 books the IS and full-sample clause verdicts agree **33/45**
(`H_WF` PASS at the majority bar, and that is a weak bar: 12 of 45 books change side).

## 5. The control the clause cannot price
The record's 21-sleeve calendar **ENSEMBLE** (2026-09-15 lane C) reproduces its memo exactly here —
11.68% / 1.177 / −19.07%, halves 1.230 / 1.135, OOS 12.70% / 1.230 / −19.07%, DD margin **+1.165 pp**
against the memo's stated 1.16 pp. Its calendar spread is **zero by construction**, so its ratio is
infinite on every leg and it passes the clause without its margin ever exceeding a spread. That is
the clause's own loophole, and it is also the only honest way out of it: the book that holds all 21
calendars has no calendar to be wrong about.

## 6. GRID control
36 never-memo-selected ladder books, 19 pass 4b at k=0, **9 survive the clause** (median min-ratio
of the passes 0.970, max 1.925). Binding legs there are mixed — DD 10, H2 4, H1 3, CAGR 2 — so the
DD unanimity in §2 is a property of the **selected** shelf, not of book space.

## 7. 4a
0 of 9 committed passes clear path 4a at k=0, so 0 survive the clause on that path. Unchanged from
the record.

## Verdict — **KILL for capital**
No new book, no rules change proposed, nothing promoted. The run answers the queue's question and
one thing more: the clause is a real screen (it retires 6 of 9 committed passes, including the
record's newest) but it is **not** the empty-shelf result 879's synthetic population predicted, its
own verdict is cost-rung-dependent at the margin, and the one construction that passes it cleanly
does so by having no calendar at all. The three survivors are already memo-backed; this run adds a
robustness column to them, not a capital claim.

**SURVIVORSHIP:** U56 (`research/universe.json`) and B136 (`research/universe_broad.json`) are
CURRENT-constituent lists, so every CAGR and MaxDD level above — the books' and both comparands' —
is optimistic. The reported object is a ratio whose numerator and denominator are computed on the
same biased panel, which is the part that survives the bias; no level here is a capital claim.

Artifacts: `.py`, `.console.txt`, `.arms.csv` (514 cells), `.clause.csv`, `.walkforward.csv`.
Modifies nothing. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.
