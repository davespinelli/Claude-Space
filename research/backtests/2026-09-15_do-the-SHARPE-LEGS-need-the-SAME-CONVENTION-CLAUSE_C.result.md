# Idea 893 — do the SHARPE LEGS need the SAME CONVENTION CLAUSE? (lane C, 2026-09-15)

**ANSWERED: THE QUESTION IS MIS-ADDRESSED. The clause is not a property of the LEG, it is a
property of the (leg, COMPARAND) pair. The same 47 books, the same calendars, the same spreads:
against SPY the committed half-sample Sharpe claims cost the clause NOTHING (0 of 18 fail, median
ratio 2.95, min 1.31); against the LIVE book the identical claims cost it 13 of 18 (median ratio
0.637, min 0.006). And the clause cannot be applied to a Sharpe leg ex ante anyway — its own
denominator REVERSES the H1/H2 ordering between offset grids, and the IS→OOS rank correlation of
the statistic is −0.003. KILL for capital.** No new book, no KEEP claimed, no memo; `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched (rule 6). One PROTOCOL line is
**PROPOSED, NOT APPLIED**. Gates 5/5.

## Selection

Taken as the **SECOND open idea** in QUEUE.md (892 is lane A's). Read as a **priced** census, not a
prose one: the record's committed half-sample Sharpe claims *are* the `H1 / H2` pair
`baseline._row` publishes for a book, turned into verdict legs by PROTOCOL rule 4 on both paths.
So the books are rebuilt and walked over their own rebalance calendars, which gives the run a real
price leg, a rule-8 walk-forward and both KEEP paths.

## Design

Clause (idea 879's, priced by idea 891 on the DD/CAGR legs):
`ratio = |margin at k=0| / (spread of the same statistic across the offset grid)`, a published leg
verdict survives only if `ratio ≥ 1`. A **FAIL** verdict is as much a claim as a PASS, so both
directions are priced.

- **Tuned param 1 — CLAIM SET (3, all reported):** `SHELF` (the 9 committed memo-backed 4b passes
  — 861's 8-book shelf plus idea 879's `u56-top20-g065-M` — **imported** from the committed lane-C
  builder, not re-typed), `GRID` (861's 36 never-selected ladder books), `LIVE` (RULES v2 at live
  settings on both panels; its 4a self-claim is the degenerate case and is labelled as such).
- **Tuned param 2 — OFFSET GRID (3, all reported):** `FULL` (own cadence, every offset: 5 weekly /
  21 monthly — 879's and 891's own), `HALF` (0–2 / 0–10), `ALT` (even k only).
- **Reported, never tuned:** panel (U56/B136), comparand (SPY = the 4b legs, RULES v2 live = the
  4a legs), cost rung (10/25 bps), window (FULL/IS/OOS), leg (H1, H2; DD/CAGR/OOS carried).
- 534 arms, 282 clause cells, every margin / spread / ratio / flip count / published verdict /
  clause verdict written out. 10 bps, next-day fills, no shorts, no leverage, 260-day warm-up.
- Comparands are held at their **own** conventions: SPY has no rebalance calendar, and RULES v2 is
  scored on the live weekly calendar, not the candidate's. Only the **book's** calendar moves.

## Gates — five, all PASS, printed before any hypothesis was read

| gate | result |
|---|---|
| G1 every SHELF book reproduces its committed memo triple | **PASS** (worst dCAGR 0.0027, dSharpe 0.0240, dMaxDD 0.0109 — `u56-top20-band-m20`) |
| G2 `offset_mask(k=0)` == `engine.rebalance_mask` | **PASS**, elementwise |
| G3 `fast_run(k=0)` vs `engine.backtest` | **PASS**, max abs return diff **1.388e-17** (bar 1e-9) |
| G4 **cross-run**: idea 891's committed `.clause.csv` Sharpe-leg cells rebuilt from this run's own arms | **PASS**, 108 cells, max abs diff **4.441e-16** (bar 1e-6) |
| G5 SPY comparand vs the record's committed triple (0.1513 / 0.886 / −0.3372) | **PASS**, max dev **0.0015** |

## 1. The headline — same legs, same spreads, two opposite answers

Headline cell (SHELF, FULL, 10 bps). The **spread column is literally identical** between the two
tables — it is a property of the book's calendar. Only the numerator changes.

| book | H1 margin | H1 spread | H1 ratio | H2 margin | H2 spread | H2 ratio | clause |
|---|---|---|---|---|---|---|---|
| **vs SPY (the 4b legs)** | | | | | | | |
| u56-top20-band-m20 | +0.1349 | 0.1029 | 1.311 | +0.2656 | 0.1336 | 1.988 | PASS |
| u56-top20-g065-M | +0.2558 | 0.1863 | 1.373 | +0.3736 | 0.2344 | 1.594 | PASS |
| b136-qroll-q012-w1008-d050-g100 | +0.2264 | 0.0617 | 3.668 | +0.2102 | 0.1331 | 1.579 | PASS |
| u56-marsrespread-gross075 | +0.2131 | 0.0976 | 2.184 | +0.2018 | 0.1032 | 1.956 | PASS |
| u56-quantile50-respread-M | +0.3684 | 0.1318 | 2.795 | +0.3237 | 0.1081 | 2.994 | PASS |
| u56-k8-qroll-q017-w1008-d100-g100 | +0.1795 | 0.0616 | 2.913 | +0.4792 | 0.1175 | 4.079 | PASS |
| u56-v2band-gross100 | +0.2739 | 0.0850 | 3.221 | +0.3526 | 0.0352 | 10.013 | PASS |
| b136-r620-gross065-W | +0.3829 | 0.1146 | 3.342 | +0.1299 | 0.0402 | 3.231 | PASS |
| u56-band008-gross100 | +0.2834 | 0.0559 | 5.072 | +0.2417 | 0.0696 | 3.475 | PASS |
| **vs RULES v2 live (the 4a legs)** | | | | | | | |
| u56-v2band-gross100 | +0.0005 | 0.0850 | **0.006** | −0.0007 | 0.0352 | **0.021** | FAIL |
| u56-top20-g065-M | −0.0176 | 0.1863 | 0.094 | +0.0203 | 0.2344 | 0.086 | FAIL |
| u56-band008-gross100 | +0.0100 | 0.0559 | 0.180 | −0.1117 | 0.0696 | 1.605 | FAIL |
| b136-r620-gross065-W | +0.1076 | 0.1146 | 0.939 | −0.0100 | 0.0402 | 0.248 | FAIL |
| u56-marsrespread-gross075 | −0.0603 | 0.0976 | 0.618 | −0.1515 | 0.1032 | 1.468 | FAIL |
| u56-quantile50-respread-M | +0.0950 | 0.1318 | 0.721 | −0.0296 | 0.1081 | 0.274 | FAIL |
| b136-qroll-q012-w1008-d050-g100 | −0.0488 | 0.0617 | 0.791 | +0.0704 | 0.1331 | 0.529 | FAIL |
| u56-top20-band-m20 | −0.1385 | 0.1029 | 1.345 | −0.0877 | 0.1336 | 0.656 | FAIL |
| u56-k8-qroll-q017-w1008-d100-g100 | −0.0938 | 0.0616 | 1.523 | +0.1259 | 0.1175 | 1.071 | PASS |

`H_SPY` **PASSES as declared** (0 of 18 fail at all three offset grids at the headline rung);
it **breaks** once the 25-bps cost control is added (4 of 18) — reported, not used to move the bar.
`H_LIVE` **FAILS** its own bar: median 4a ratio **0.637** (bar < 0.50) and **13/18 = 72.2%** fail
(bar ≥ 90%). The pre-registered bar was too strong; the direction is unambiguous and the magnitude
is not. The extreme case is `u56-v2band-gross100`, whose published 4a Sharpe legs sit
**0.0005 and −0.0007** Sharpe points from the live book against calendar spreads of 0.085 and 0.035
— ratios of 0.006 and 0.021, i.e. the sign of that book's "4a FAIL" verdict is a **date**.

Across all 47 books (`.census.csv`, 36 rows, every point published): at FULL/10 bps the 4b Sharpe
claims fail the clause **10 of 72** on GRID and **0 of 18** on SHELF; the 4a Sharpe claims fail
**44 of 72** and **13 of 18**.

## 2. Idea 879's H1/H2 asymmetry does not reproduce as a leg property

`H_ASYM` **FAILS** and `H_SPREAD` **PASSES at the headline cell only** — median spread H1 0.0773 vs
H2 0.1077, which clears the 0.75× bar by 4%. It does not survive the other dial level:

| offset grid | median spread H1 | median spread H2 | reading | books with sprH1>sprH2 |
|---|---|---|---|---|
| FULL | 0.0773 | 0.1077 | H1 quieter | 16/47 (34.0%) |
| HALF | 0.0674 | 0.0447 | **H1 NOISIER** | 33/47 (70.2%) |
| ALT | 0.0351 | 0.0796 | H1 quieter | 10/47 (21.3%) |

**The clause's own denominator reverses the H1/H2 ordering depending on how densely the calendar is
sampled.** And the flip counts 879 reported do not carry either: at FULL/10 bps this run's 47 books
flip **H1 8, H2 0** on the 4b comparand (**reversed** vs 879's "H1 0, H2 152") and **H1 35, H2 63**
on the 4a comparand (879's direction). Same books, same calendars — the ordering is set by the
comparand, not by which half of the sample the leg reads.

## 3. `H_SAME` — the queue's title question, answered both ways and honestly

At the headline grid point the binding 4b leg is **DD on 9 of 9** SHELF books, reproducing idea
891's unanimous result exactly. `H_SAME` passes only on **dial movement**: 3/9 books become
Sharpe-bound at ALT/10 bps, 2/9 at HALF/10 bps, 4/9 at every 25-bps cell. So: on the record's own
published cell the Sharpe legs do **not** need the clause DD needs; one dial step away, a third to
a half of the shelf disagrees. That instability is the finding, not the count.

## 4. Rule 8 — choose on 2009–2016, read 2017+ once (`H_WF` **FAILS**)

Spearman ρ(IS Sharpe-leg min-ratio, OOS min-ratio) over the 47 books = **−0.003** (bar +0.50); the
clause verdict agrees IS vs OOS on **10 of 47 (21.3%)** (bar 50%). **The clause cannot be applied to
a Sharpe leg before the outcome window is read** — knowing a leg's margin beat its calendar spread
in sample tells you nothing about whether it does out of sample.

Declared IS-only selector (highest IS Sharpe-leg min-ratio) and the record's control selector
(highest IS Sharpe), OOS read once:

| selector | set | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|
| IS min-ratio | SHELF | `u56-quantile50-respread-M` | **16.06%** | **1.218** | −19.75% | **PASS** | FAIL |
| IS min-ratio | GRID | `B136-qroll-q0.17-w504-d0.50` | 12.95% | 1.116 | −17.31% | **PASS** | FAIL |
| IS min-ratio | LIVE | `B136-RULESv2-live` | 7.88% | 1.106 | −12.24% | FAIL | FAIL |
| IS Sharpe (control) | SHELF | `b136-r620-gross065-W` | 14.52% | 1.040 | −19.43% | **PASS** | FAIL |
| IS Sharpe (control) | GRID | `B136-band0.08-g1.00` | 11.05% | 1.097 | −19.50% | **PASS** | FAIL |
| IS Sharpe (control) | LIVE | `U56-RULESv2-live` | 9.46% | 1.277 | −12.05% | FAIL | FAIL |

Comparands OOS: **SPY 15.27% / 0.874 / −33.72%** (U56), 15.33% / 0.877 / −33.72% (B136);
**RULES v2 (live) 9.46% / 1.277 / −12.05%** (U56), 7.88% / 1.106 / −12.24% (B136).
SHELF pick full sample: 15.39% / 1.226 / −19.75%, halves 1.327 / 1.147.

**Unselected base rate** over all 47 books at k=0, 10 bps: 4b PASS 28/47 (59.6%), 4a PASS 1/47
(2.1%), Sharpe-leg clause PASS 37/47 (78.7%), all-leg clause PASS 22/47 (46.8%). Both picks are
already-memo'd books; nothing new is promoted.

## 5. Verdict

| hypothesis | result |
|---|---|
| `H_SPY` | **PASS** as declared (3 offset grids, headline rung); breaks at 25 bps |
| `H_LIVE` | **FAIL** (median 0.637 vs bar 0.50; 72.2% fail vs bar 90%) — direction right, magnitude overstated |
| `H_ASYM` | **FAIL** |
| `H_SPREAD` | **PASS** at the headline cell only; reverses at HALF |
| `H_SAME` | **PASS** on dial movement, **FAIL** on the record's published cell (DD binds 9/9) |
| `H_WF` | **FAIL** (ρ = −0.003, 21.3% agreement) |

**KILL for capital.** No book is proposed and none is promoted: this run prices an existing clause
on existing committed claims.

## 6. PROPOSED, NOT APPLIED (rule 6 — Sunday review decides)

> A margin/spread clause must name its **comparand** as well as its leg. On this record the same
> half-sample Sharpe spread supports the 4b (vs SPY) legs at median ratio 2.95 and destroys the 4a
> (vs live-book) legs at median 0.637. A leg-wide clause is therefore not well posed; and since the
> statistic's IS→OOS rank correlation is −0.003, no clause on a Sharpe leg can be applied ex ante.
> What IS publishable today, at no cost to any committed claim, is the **spread beside the margin**:
> print `H1 / H2` with their own rebalance-calendar spreads, so a reader can see that
> `u56-v2band-gross100`'s 4a Sharpe legs sit 0.0005 from the live book against a spread of 0.085.

## Survivorship

U56 and B136 are **current-constituent** panels. Dead names are absent, so every LEVEL above is
optimistic and the 4b CAGR floor is easier to clear than on a point-in-time panel. This run's
object — the spread of a leg across equally arbitrary calendars, and the ratio of a margin to it —
is a **within-book** quantity and far less exposed to that bias than the levels are; the levels in
the rule-8 table are not corrected for it.

## Outputs

`.arms.csv` (534) · `.clause.csv` (282) · `.asym.csv` (12) · `.census.csv` (36) ·
`.walkforward.csv` (6) · `.gates.csv` (5) · `.console.txt` · this file.
Script: `research/backtests/2026-09-15_do-the-SHARPE-LEGS-need-the-SAME-CONVENTION-CLAUSE_C.py`
(21.9 s, deterministic, no network).
