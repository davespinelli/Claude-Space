# Idea 579 — does-the-DRAWDOWN-a-vol-cap-BUYS-ever-clear-the-4b-DD-LEG-on-its-own (lane C, 2026-09-09)

**Verdict: ANSWERED — YES, the 4b DD leg is buyable, and the thing that buys it is CASH.
One 4b passer survives rule 8 and is PARKed (not KEEPed) with a memo. All five pre-registered
nulls were refuted or failed; every one of the 1,692 clause cells is in `.grid.csv`.**

Script `2026-09-09_does-the-DRAWDOWN-a-vol-cap-BUYS-ever-clear-the-4b-DD-LEG-on-its-own_C.py`,
110 s, deterministic, offline. Artefacts: `.grid.csv` (1,728 rows), `.ddonly.csv`, `.family.csv`,
`.mono.csv`, `.walkforward.csv`, `.gates.csv`, `.console.txt`.

## Gates (all PASS, before any finding was read)

| Gate | What | Result |
|---|---|---|
| G1 | numpy runner == `engine.backtest` on a **claused** book (VOLCAP(0.40)+CASH(0.80), MA20/W), returns AND turnover, all 3 panels | max **3.89e-16** vs bar 1e-12 — PASS |
| G2 | idea 311's 36 committed g=0.75 rows (3 panels x 6 forms x 2 cadences x 6 metric columns) | U56 **2.22e-16**, B136 **2.22e-16**, SMALL439 **8.33e-17** — PASS. U56 was pre-registered a 5e-3 bar because `data/prices.csv` is refreshed daily (idea 312/311's documented revision); it in fact reproduced to machine precision today, so no vintage allowance was used. |
| G3 | null-dial identity: every clause at its no-op dial reproduces its parent's return path | **0.000e+00** on all six families vs bar 1e-15 — PASS. The clause plumbing is a pure overlay. |

## The population

Idea 311's 36 pre-registered books at gross 0.75: 3 pass 4b, 33 fail, and **16 fail on the DD
leg ALONE** — books whose H1, H2 and OOS Sharpe all beat SPY and whose CAGR clears the floor,
held out of 4b by drawdown and nothing else. Their DD gap to the bar (0.60 x SPY's −33.72%
= −20.23%) runs from **−1.14 pp** (U56 MA20/W) to **−8.28 pp** (B136 TOP10/M).

## The five pre-registered hypotheses

| | Hypothesis | Result | Number |
|---|---|---|---|
| H_MAIN | no clause cell clears 4b under a failing parent | **REFUTED** | 141 of 1,551 |
| H_DDONLY | no clause repairs a DD-only parent without breaking another leg | **REFUTED** | **16 of 16** |
| H_CASH | no signal family beats plain cash at matched MaxDD | **REFUTED (barely)** | 1 of 5 (MKT, +0.226 pp median) |
| H_MONO | the DD purchase is ordered by the dial | **FAILS** | min 61.1% vs bar 90% |
| H_OOS | no walk-forward pick clears 4b out of sample | **REFUTED** | 1 of 6 |

## Finding 1 — the DD leg is buyable, and cash buys it

All 16 DD-only parents have at least one clause that repairs the DD leg **and still clears all
five 4b legs**. But the agent that does the repairing is the null, not a signal:

* **14 of 16** are repaired by **plain static de-gross (CASH) alone**.
* 15 of 16 are also repaired by a signal clause, and in 15 of 16 at least one such signal cell
  sits above the cash line at its own MaxDD — but see Finding 3 for what that survives.
* Of the 538 DD-repairing cells under those parents, the leg that breaks instead is
  **CAGR in 281** (52%), and only **141** break nothing at all.

This is the DD-side restatement of idea 311's result about the gross ladder. Because the three
4b Sharpe legs are g-invariant, a book that fails 4b on DD alone can be walked into compliance
by holding cash until the CAGR floor bites. **The 4b DD cap is therefore a dial placement, not
an edge test** — the same loophole idea 317 exposed on the blend side, reached from drawdown.

## Finding 2 — the price of drawdown, matched at MaxDD

Every cell is priced against its own parent's 20-point cash ladder interpolated to the cell's
own MaxDD: `edge = CAGR(clause) − CAGR(cash at the same MaxDD)`, pp/yr. Positive means the
clause bought that drawdown more cheaply than cash could.

| family | cells | median | mean | p90 | max | share > 0 | med DD gain (pp) | med CAGR cost (pp) |
|---|---|---|---|---|---|---|---|---|
| CASH (null) | 720 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0% | 10.005 | 5.456 |
| VOLCAP | 216 | **−1.828** | −2.468 | −0.346 | 1.023 | **3.8%** | 7.610 | 6.852 |
| VT | 216 | 0.000 | −0.048 | 1.559 | 3.059 | 46.5% | 4.726 | 2.638 |
| MKT | 180 | **+0.226** | −0.388 | 2.194 | 4.185 | 53.3% | 4.508 | 3.306 |
| DDSTOP | 180 | −0.463 | −0.944 | 0.795 | 3.602 | 18.6% | 0.000 | 2.002 |
| BREADTH | 180 | −0.168 | −0.301 | 2.841 | 4.945 | 45.7% | 3.727 | 3.017 |

**Idea 314's own clause is the worst of the six.** VOLCAP buys drawdown at a median 1.83 pp/yr
*worse* than simply holding the cash, and beats cash in 3.8% of its 216 cells. Its median DD
gain (7.61 pp) is large — idea 314's "41 of 48 cut MaxDD" is reproduced in spirit — but the
gain is bought at a median 6.85 pp of CAGR, more than de-grossing to the same MaxDD would cost.
Only MKT has a positive median, and at +0.226 pp/yr it is inside the noise; its *mean* is
negative (−0.388), i.e. its distribution is a few good cells and a long bad tail.

**H_MONO fails, and it fails informatively.** CASH (100.0%), VOLCAP (97.8%) and VT (97.8%) order
MaxDD by their dial almost perfectly — they are risk dials. DDSTOP (79.2%) and BREADTH (61.1%)
do not: their "dial" changes *which regimes* the book sits out, so tightening it can make
drawdown worse. Those two are regime bets wearing a risk-dial costume, which is exactly why
they show the fattest right tails (BREADTH max edge +4.945) and can't be trusted on them.

## Finding 3 — rule 8: the cheapness does not walk forward

Family and dial chosen on 2009/2011–2016 only; 2017–2026 read once. Selection reads only the IS
columns of the same grid; the winner's weights are rebuilt and re-run (rebuild check
|dIS_Sharpe| = 0.00e+00 on all five picks).

| panel | selector | IS pick | OOS CAGR / Sharpe / MaxDD | OOS 4b fails | IS edge → OOS edge |
|---|---|---|---|---|---|
| U56 | WF-A max IS Sharpe | TOP10/M + MKT(200) | 12.92% / 0.8761 / −21.23% | H2,OOS,DD | +2.291 → **−2.323** |
| U56 | WF-B max IS edge, IS-4b passers | **TOP10/M + VT(0.10)** | **11.40% / 1.0095 / −18.77%** | **— (passes)** | +3.409 → **−1.901** |
| B136 | WF-A | TOP20/M + BREADTH(0.70) | 7.29% / 0.6558 / −18.45% | H1,H2,OOS,CAGR | +0.908 → **−4.386** |
| B136 | WF-B | EWall/W + VT(0.20) | 12.89% / 1.1003 / −22.85% | DD | +2.804 → +0.482 |
| SMALL439 | WF-A | MA-DG/M + VOLCAP(0.20) | 0.00% / 0.0152 / −1.03% | H1,H2,OOS,CAGR | +0.051 → −0.244 |
| SMALL439 | WF-B | — | selector empty: no cell clears all five IS 4b legs | — | — |

Benchmarks on the same OOS window: **SPY** 15.45% / 0.8820 / −33.72%; **RULES v2** on U56
9.53% / 1.2851 / −12.05%, on B136 7.98% / 1.1185 / −12.24%, on SMALL439 3.85% / 0.5680 / −14.68%.

**The decisive number: the matched-DD edge keeps its sign out of sample in 1 of 5 picks, median
IS +2.291 pp → median OOS −1.901 pp.** The statistic that says "this clause bought drawdown
cheaply" is an in-sample artefact. Even the one book that clears 4b out of sample was, out of
sample, **1.90 pp/yr worse than simply de-grossing its own parent to the same MaxDD**.

## The one 4b passer — PARKed, not KEEPed

WF-B on U56 picks **TOP10 monthly + VT(0.10)** and it clears 4b on the full sample *and* on the
OOS window, with family and dial chosen in-sample only:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | turnover |
|---|---|---|---|---|---|---|
| TOP10/M + VT(0.10) | 13.00% | 1.157 | −18.77% | 1.369 / 0.961 | 1.010 | 4.39x/yr |
| unclaused parent TOP10/M | 18.66% | 1.141 | −25.03% | 1.328 / 1.013 | 1.046 | 5.69x/yr |
| SPY | 15.23% | 0.889 | −33.72% | 0.957 / 0.834 | 0.882 | — |
| RULES v2 (live) | 8.66% | 1.206 | −12.05% | 1.226 / 1.191 | 1.285 | — |

4b legs, full sample: H1 1.369 > 0.957 ✓, H2 0.961 > 0.834 ✓, OOS 1.010 > 0.882 ✓,
MaxDD −18.77% ≥ −20.23% ✓, CAGR 13.00% ≥ 10.66% ✓. **4a: FAIL** — it loses to the live book on
Sharpe in both halves and OOS (1.010 vs 1.285).

**It is recorded as a 4b KEEP-candidate and recommended PARK for three stated reasons:**

1. **Rule 4 breadth.** WF-B searched 564 IS cells per panel over *four* axes (form x cadence x
   family x dial). Only family and dial were declared tuned; form and cadence were declared
   reported axes and then selected on anyway by the walk-forward. That is more than PROTOCOL
   rule 4's two parameters at the selection stage.
2. **Its own selection statistic reverses.** IS edge +3.409 pp → OOS edge **−1.901 pp**. Out of
   sample this book is dominated by plain de-grossing of the same parent to the same MaxDD, so
   the VT clause is not what earned the pass.
3. **It is a dial placement.** On the VT ladder for this exact parent, 4b passes at 0.10 and
   0.12 and fails at 0.06, 0.08, 0.15 and 0.20 — **2 of 6 dial points**, idea 311's DIAL class.

It also survives on only 1 of 3 panels, and 0 of the 170 passing clause cells are on SMALL439
(consistent with idea 575's 0/100).

## Answer to the queue's question

> "is there any DD-buying clause whose CAGR cost is small enough that the pair clears 4b where
> the unclaused book fails? If none, the 4b DD leg cannot be bought and should be read as a
> book-form constraint."

**There is — 141 of them — so the DD leg is NOT a book-form constraint.** But the correct
reading is the opposite of a discovery: the leg is bought by *holding cash*, which every book
can do, so passing it certifies gross placement rather than any risk-management skill. No
signal family buys drawdown reliably more cheaply than cash (VOLCAP is 1.83 pp/yr worse at the
median and beats cash in 3.8% of cells), and the cheapness that does appear in-sample flips
sign out of sample in 4 of 5 walk-forward picks.

## Suggested protocol follow-up (for Sunday review, not applied here)

The DD leg has the same loophole idea 317 found in the blend: it can be cleared by de-grossing
rather than by edge. A candidate wording, in the spirit of the proposed rule 4c: *a 4b pass may
not be claimed at a gross/exposure placement unless the book also clears 4b at the neighbouring
points of whatever dial sets its exposure* — which would have failed this candidate (2 of 6),
and would have failed 52 of the 170 passing cells that are CASH cells.

RULES.md, scan.py, bot.py and baseline.py were **not** modified. No rules change is proposed.
SURVIVORSHIP: B136 and SMALL439 are current constituents only; U56 is `research/universe.json`,
a list fixed today, so its levels are also biased up relative to what was investable in 2009.
