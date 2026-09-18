# Idea 1284 — does a SECTOR or NAME CONCENTRATION CAP change the STANDING G=0.60 BOOK's 4b VERDICT?
lane cloud, 2026-09-18. **ANSWERED: NO — (C) THE CAP COSTS MORE THAN IT BUYS, AND (D) IT IS A
TUNING TRAP. KILL. The standing book stays UNCAPPED.**
Script: `research/backtests/2026-09-18_does-a-SECTOR-or-NAME-CONCENTRATION-CAP-change-the-STANDING-G-0.60-BOOK-s-4b-VERDICT_cloud.py`

## What was run
The record's single confirmed 4b candidate (U56, top N=20 by the frozen three-leg composite among
names above their own 200d MA with vol20 < 0.60, min-hold H=126, equal weight, **gross 0.60**,
weekly decide-Friday / trade-Monday) with two dials and nothing else moved:

* **DIAL 1 SECTOR CAP S ∈ {2, 3, 4, 6, 20}** — max slots from one of 13 static risk buckets
  (hand-assigned from public sector membership, written in the script, identical in every window,
  frozen — not a third dial). Binds on NEW ADDS only; min-hold is frozen. S=20 is OFF.
* **DIAL 2 NAME CAP C ∈ {0.05, 0.0625, 0.075, 0.10, 1.00}** — max weight of one name as a fraction
  of the book (×0.60 for NAV). Excess to CASH (de-gross, never re-spread). C=0.05 = 1/20 exactly,
  so it binds ONLY when fewer than 20 names are held. C=1.00 is OFF.

`(S=20, C=1.00)` is the standing book bit for bit. **Gate G2: it reproduces idea 1286's committed
U56 G=0.60 / 10 bps / t+1 row (12.5911% / 1.151737 / −15.5135%) to 3.6e-07.** G1: fast runner ==
`engine.backtest` to 2.08e-17. G0: bucket map covers 55/55 U56 investables. 5/5 gates pass.
210 cells = 3 panels × dials × costs {10, 25, 50} bps × fills {t+1, t+2}; 10 bps / t+1 is the
PROTOCOL rung and the only one any verdict is taken on. **All 210 cells are in `.grid.csv`.**

## Result 1 — no cap helps the leg it was supposed to help
U56, PROTOCOL rung. Uncapped book **12.59% / 1.1517 / −15.51%**, halves 1.2123 / 1.1121,
OOS 1.1826. SPY 15.13% / 0.8849 / −33.72%, OOS 0.8747.

| S | C | CAGR | Sharpe | MaxDD | H1 / H2 | OOS S | DD/SPY | bind rate | 4b |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 1.00 | 12.59% | 1.1517 | −15.51% | 1.2123 / 1.1121 | 1.1826 | 0.4601 | — | **PASS** |
| 4 | 1.00 | 12.10% | 1.1828 | −16.14% | 1.2743 / 1.1096 | 1.1951 | 0.4786 | 0.162 | PASS |
| 4 | 0.05 | 11.84% | 1.1766 | **−15.00%** | 1.2791 / 1.0921 | 1.1810 | 0.4450 | 0.162 / 0.038 | PASS |
| 6 | 1.00 | 12.28% | 1.1254 | −17.15% | 1.2078 / 1.0719 | 1.1401 | 0.5086 | 0.071 | PASS |
| 3 | 1.00 | 10.64% | 1.0842 | −17.80% | 1.1062 / 1.0727 | 1.1337 | 0.5280 | 0.286 | PASS |
| 2 | 1.00 | 9.20% | 1.0349 | −15.70% | 1.1046 / 0.9816 | 1.0451 | 0.4657 | 0.484 | FAIL (CAGR) |
| 20 | 0.05 | 12.35% | 1.1463 | −15.51% | 1.2170 / 1.0968 | 1.1700 | 0.4601 | 0.037 | PASS |

**Only 2 of the 24 capped U56 cells have a SHALLOWER MaxDD than the uncapped book**, and the best
of them (S=4, C=0.05) buys **+0.51 pp of MaxDD for −0.75 pp of CAGR and −0.0016 of OOS Sharpe**.
Over all 144 U56 capped cells: mean ΔMaxDD **−0.0083 (i.e. DEEPER)**, shallower at 26 of 144;
mean ΔCAGR **−0.0136, negative at 144 of 144**; mean ΔSharpe −0.0436, mean ΔOOS Sharpe −0.0539.
Tightening the sector cap is monotone destruction below S=4 (S=2 costs 3.3 pp of CAGR and
0.117 of Sharpe and still does not cut MaxDD). **The book's drawdown is not a concentration
event**, so the cheapest-looking drawdown lever on the table does not move the binding leg.

## Result 2 — rule 8: letting a chooser move the caps LOSES money out of sample
Both dials chosen on warm-up..2016 ONLY (highest IS Sharpe among cells passing the four
IS-computable 4b legs; fallback highest IS Sharpe), 2017–2026 read ONCE.

**Δ(OOS Sharpe) CHOOSER − FROZEN over 18 cells: mean −0.0100, SE 0.0029, t −3.45; positive 0,
negative 12, identical 6.** The chooser moved off the uncapped book at **18 of 18** cells and was
right at none of them. On U56 it picks S=4 / C=0.05 at every rung and loses −0.0016 to −0.0356.
On SMALL663 it "moves" to C=0.05, which never binds, so the OOS series is identical.
This is pre-declared outcome **(D)**: the in-sample ranking of the cap dial does not survive.

## Result 3 — the other two panels
* **B135** (no sector labels in repo → DIAL 2 only, stated not guessed): the name cap is shallower
  on MaxDD at 21 of 24 cells but costs CAGR at 24 of 24 and OOS Sharpe at 24 of 24
  (mean −0.0079). 4b 12/30, all failures `H2,DD`.
* **SMALL663** (house `max_1d_move >= 1.0` filter applied FIRST — 52 names dropped, 663 kept):
  the name cap **never binds once** (20 slots always fill out of 663), so all five cells are
  bit-identical. 4b **0/30**, every leg fails. Consistent with the record: this is not a
  small-cap book.
* **4a: 0 of 210 cells**, as rule 4 anticipates for any growth book against the live −12.05% book.

## Verdict
**KILL.** A sector cap and a name cap were the two cheapest untried drawdown levers on the
record's only confirmed 4b candidate. Neither changes its 4b verdict for the better: the
drawdown leg is essentially unmoved, CAGR falls at 144 of 144 U56 capped cells, and a rule-8
chooser allowed to set both dials loses OOS Sharpe at 12 of 18 cells and gains at none. The
standing book is carried **unchanged and uncapped**; nothing here is recommended to the Sunday
review, and no memo is filed because there is no KEEP candidate.

## Survivorship (rule 9)
U56 (55 investables) and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen.
Every absolute level (CAGR, Sharpe, MaxDD, and every 4a/4b verdict built on them) is an **UPPER
bound**. The quoted result is a set of WITHIN-grid differences — capped cell minus uncapped cell
on the SAME panel, same names, same dates — which are first-order immune to that bias. Only 2020
and 2022 are real stress in this tape, which is precisely why a drawdown lever is hard to price
here at all; that cuts AGAINST this run's ability to detect a cap that helps, and is stated as a
limitation of the KILL rather than an argument for it.
