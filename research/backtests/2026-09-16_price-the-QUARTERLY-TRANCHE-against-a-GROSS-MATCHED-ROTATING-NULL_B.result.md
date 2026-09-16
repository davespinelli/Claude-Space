# Idea 975-TRANCHE (lane B, 2026-09-16) — price-the-QUARTERLY-TRANCHE-against-a-GROSS-MATCHED-ROTATING-NULL

**ANSWERED = THE SUBJECT'S PASS SURVIVES ITS OWN TRANCHED NULL (base rate 0.000 of 200, both
conventions) BUT SURVIVES ON THE DRAWDOWN LEG ALONE — AND THE TRANCHE *IS* A PASSABILITY DEVICE A
COIN FLIP COLLECTS, JUST NOT IN THE SUBJECT'S CELL. PARK CONFIRMED for 964's tranche (now measured
rather than asserted), plus KILL ×2.** Nothing promoted. No RULES change, no PROTOCOL edit applied
(rule 6); `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## The grid

2 panels {U56, B136} × 3 books {EWELIG, BAND03, TOP20} × gross 0.75 (fixed by the question) ×
{M 21, Q 63} phases × 2 estimators {CANON = phase 0, FPORT = the tranche} × 5 cost rungs
= **120 REAL rows**, against **36,000 NULL rows** (2 null conventions × 200 draws on U56 / 100 on
B136 × the same cells and rungs) and **12 rule-8 picks**. Two tuned axes only — DRAWS
{50/100/200, nested} and CADENCE {M, Q} — all points reported, none selected. 2,035 s.

## The answer, in the subject cell (U56 / EWELIG / CORE 0.75 / Q / 10 bps)

| | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|
| REAL tranche (964's object) | **12.29%** | **1.120** | **−20.14%** | PASS | fail |
| REAL canonical (phase 0) | 11.52% | 1.033 | −22.21% | fail `L4_DD` | fail |
| tranched null, median of 200 | 13.56% | 1.134 | −21.90% | — | — |
| SPY | 15.21% | 0.8713 | −33.72% | — | — |
| RULES v2 (live), U56 | 9.45% | 1.276 | −12.05% | — | — |

**H_BASE PASS at 0.000** — not one of 200 gross-matched tranched coin flips clears 4b, under
*either* null convention. The subject's pass is outside its null.

**And that is the whole of the good news.** Per-leg the null passes `L1_H1` 1.000, `L2_H2` 1.000,
`L3_OOS` 1.000, `L5_CAGR` 1.000 and **`L4_DD` 0.000**: the null's base rate is zero because of the
drawdown leg *alone*. Against its own null the book sits at the **0.090 percentile on OOS Sharpe**
(empirical p **0.9104** — 91% of coin flips earn a higher OOS Sharpe), the **0.000 percentile on
OOS CAGR** (every one of 200 coin flips earns more; median 13.56% vs the book's 12.29%) and the
**1.000 percentile on |OOS MaxDD|**. The tightest of 200 null draws still draws down 21.55%,
against a 4b cap of 0.60 × |SPY −33.72%| = **−20.23%**, which the book clears by **0.09 pp**.
So the subject is a low-return, low-drawdown object whose only distinction from a coin flip is a
9-basis-point margin on one leg.

## The mechanism the question asked about is REAL — in the other cell

Tranching lifts the null's own 4b base rate (FPORT minus CANON, 10 bps, ROTP) by:

| panel | book | cad | null CANON | null FPORT | lift |
|---|---|---|---|---|---|
| U56 | TOP20 | **Q** | 0.110 | **0.680** | **+0.570** |
| U56 | TOP20 | **M** | 0.815 | **1.000** | **+0.185** |
| U56 | EWELIG | M | 0.025 | 0.000 | −0.025 |
| U56 | EWELIG | Q (subject) | 0.000 | 0.000 | +0.000 |
| U56 / B136 | BAND03, EWELIG | M,Q | 0.000 | 0.000 | 0.000 |
| B136 | TOP20 | M / Q | 0.060 / 0.030 | 0.000 / 0.000 | −0.060 / −0.030 |

On **U56/TOP20/Q** the tranche moves the null's median OOS Sharpe 0.935 → 1.120 and its median
|OOS MaxDD| **22.20% → 20.13%**, crossing the fixed −20.23% cap: the null's `L4_DD` pass rate goes
**0.175 → 0.680**. **The REAL TOP20/Q tranche (15.48% / 1.121 / −24.24%) still FAILS 4b while 68%
of its own gross-matched coin flips pass it.** H_LIFT and H_DD FAIL *as pre-registered* because
they were read in the subject cell, where the lift is +0.000 and 0.03 pp — and that is the finding:
**the tranche buys passability only where the phase-books actually differ.** `EWELIG` holds
essentially every eligible name, so its 63 quarterly phase-books are already 0.951 correlated and
averaging them removes nothing; `TOP20` holds 20 of 56 and its phase-books are 0.939 correlated,
which is enough for the tranche to buy 2.1 pp of drawdown.

## The number the record should carry away

Idea 980's headline best pick — **U56 / M / `TOP20` @ 0.75, OOS 16.68% / 1.283 / −19.51%** —
reproduces here to the basis point and is **2 of this run's 2 OOS 4b passes**. Its own
gross-matched coin flip clears 4b **0.815** of the time (200 draws; 0.770 under 926's ROT
convention, which independently reproduces idea 964's committed **0.800** for the same cell from a
different code path), and its **tranched** coin flip clears it **1.000** of the time. The book is
genuinely good on return — 0.995 percentile on OOS Sharpe, **1.000 on OOS CAGR** — but it is at
the **0.005 percentile on drawdown**, and the cell is one where 4b is nearly free. It is the exact
mirror of the subject: the subject passes on drawdown alone against a null that cannot, this one
passes on return in a cell where the null passes anyway.

## Rule 8 (PROTOCOL rule 8) — 12 picks, (book, estimator) chosen on 2009–2016 alone

**OOS 4b 2 of 12, OOS 4a 0 of 12**; full sample over the 24-row 10 bps REAL grid, 4b **5**, 4a **0**.
Both OOS 4b passes are the same object, U56/M `TOP20` CANON, whose null base rate is 0.815.

| panel | cad | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a | own null 4b | binding leg |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | M | IS_SHARPE | BAND03 CANON | 9.55% | 1.224 | −14.38% | fail | fail | 0.000 | `L5_CAGR` |
| U56 | M | IS_CAGR / IS_LEGS | TOP20 CANON | 16.68% | 1.283 | −19.51% | **PASS** | fail | **0.815** | — |
| U56 | Q | IS_SHARPE / IS_LEGS | EWELIG CANON | 11.52% | 1.033 | −22.21% | fail | fail | 0.000 | `L4_DD` |
| U56 | Q | IS_CAGR | TOP20 FPORT | 15.48% | 1.121 | −24.24% | fail | fail | **0.680** | `L4_DD` |
| B136 | M | all three | TOP20 CANON | 15.55% | 1.000 | −26.11% | fail | fail | 0.060 | `L4_DD` |
| B136 | Q | IS_SHARPE / IS_CAGR | TOP20 FPORT | 14.97% | 0.950 | −26.03% | fail | fail | 0.000 | `L4_DD` |
| B136 | Q | IS_LEGS | EWELIG CANON | 10.97% | 0.969 | −24.44% | fail | fail | 0.000 | `L4_DD` |

Comparands: **SPY OOS 15.33% / 0.8769 / −33.72%**; RULES v2 (live) U56 OOS 9.45% / 1.276 /
−12.05% (full Sharpe 1.201, MaxDD −12.05%), B136 OOS 7.88% / 1.106 / −12.24% (full 1.099 /
−12.24%).

**H_RULE8 FAIL.** The IS-only choosers pick the tranche in **3 of 12** (bar 0.75) and **no chooser
at U56/Q picks it**: given only 2009–2016, `IS_SHARPE` and `IS_LEGS` both take `EWELIG` **CANON**,
the phase-0 book that fails 4b on `L4_DD`. **964's tranche is not selectable out of sample** — that
is the operative reason it stays PARK, and it is now measured rather than asserted. Only 0.167 of
the picks beat their own null's base rate.

## Both KEEP paths (PROTOCOL rule 4), every REAL book at 10 bps

**4a: 0 of 24.** Gross 0.75 against the live book's −12.05% MaxDD is not close on any cell.
**4b: 5 of 24** — U56/EWELIG M (both estimators), U56/EWELIG Q FPORT (the subject), U56/TOP20 M
(both estimators). Applying ideas 926/942's base-rate clause (a 4b pass whose own gross-matched
null clears the same bar more than 5% of the time is not a pass), the two U56/TOP20/M rows become
PARK at null 0.815 and 1.000, leaving three: U56/EWELIG M CANON (12.97% / 1.215 / −17.01%,
null 0.025), U56/EWELIG M FPORT (12.35% / 1.171 / −17.63%, null 0.000) and the subject.
**None is promoted.** All three fail 4a; all three are chosen by no rule-8 chooser; and the
percentile reading says what they are — U56/EWELIG/M FPORT beats **1.000** of its null on OOS
Sharpe and **0.000** of it on OOS CAGR. These are low-return, low-vol books that clear a drawdown
cap, not books with an edge.

## H_CORR FAIL — and the failure retires an objection rather than raising one

The run carried two null conventions because a tranche of *independent* coin flips would be better
diversified than anything the real tranche can build. **That worry is wrong, measurably.** Mean
pairwise phase-book correlation, REAL vs ROTP (phase-coherent) vs ROT (926's verbatim, independent
per phase):

| panel | book | cad | REAL | ROTP | ROT |
|---|---|---|---|---|---|
| U56 | EWELIG | Q | 0.9507 | 0.9426 | 0.9426 |
| U56 | TOP20 | Q | 0.9385 | 0.9021 | 0.9022 |
| B136 | TOP20 | M | 0.9621 | 0.8996 | 0.9008 |

**ROT and ROTP are indistinguishable (max |ROTP − ROT| = 0.0012 over all 12 cells)** and both sit
within 0.0625 of the real book. The common market factor dominates: holding a different random
subset of the same 56 large caps does not decorrelate the phase-books. H_CORR fails only on its
second clause (ROT ≥ 0.10 *below* REAL), which is the clause that said 926's null would be unfair.
**It is not.** Every headline above is convention-free, and future runs need not carry the
phase-coherence caveat.

## Gates: 7 of 9 PASS, printed before any result number

G0 `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on M and Q, **0 rows**. G1 fast `Ctx` ≡
`engine.backtest` on returns AND turnover, **2.082e-17 / 9.159e-16**. G2 `band_book(0.03,0.75)` ≡
`baseline.rules_v2_weights` **0.000e+00**. G5 GROSS MATCH: null realised gross ≡ the book's
**1.110e-16**, holding count **0**. G6 determinism **0.000e+00**. G7 nesting (the 50-draw
statistics are the first 50 seeds of the 200-draw grid) **0.000e+00**. G8 tranche identities —
one-phase FPORT ≡ CANON **0.000e+00**, mean-of-net ≡ the summed-gross/summed-turnover accumulator
**3.469e-18**.

**G3 and G4 FAIL on the letter, and the cause is the panel, not the code.** G3 replays idea 964's
committed `.grid.csv` on **60 of 60** shared rows with **0 4b-verdict flips** but max|d|
**1.412e-02**; G4 reproduces 964's subject row as 12.29% / 1.120 / −20.14% against its published
12.31% / 1.121 / −20.14%, max|d| **1.230e-03**, over a 5e-4 bar. The column-by-column split
localises it exactly: every **in-sample** quantity reproduces to machine precision (`IS_CAGR`
1.175e-07, `IS_Sharpe` 1.507e-06, `MaxDD` 4.432e-08), and every quantity that reads the OOS window
or the full sample moves by 1e-4 to 1e-2. The panel gained **one trading day** between 964's run
(2026-09-15) and this one (2026-09-16), which shifts the halves split by one row: **SPY's own OOS
CAGR moves 15.27% → 15.21% and its OOS Sharpe 0.8741 → 0.8713** in the committed files themselves,
the same shift the 2026-09-16 cloud run (idea 980) published. This is idea 890's
growing-panel reproduction defect, observed again on a third corpus; it is reported as a FAIL,
not excused, and it means **no cross-day G3/G4 gate in this record can be met on any
full-sample or OOS column** — only on in-sample ones.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are current-constituent lists, so every CAGR and drawdown **level** is optimistic. The
measured object is a *difference* between a book and a coin flip drawn from the SAME panel on the
SAME tape at the SAME gross. A coin flip drawn from a survivor panel is a **better** book than one
drawn in real time, so **every null base rate above is an UPPER bound** — which cuts AGAINST this
run's own H_LIFT and FOR H_BASE, i.e. against the suspicion the run was built to test, not for it.
Turnover is reported but **not** matched (926 matches gross, not turnover): the subject's real
tranche trades 1.79/yr against the null tranche's median 2.43/yr, so at 10 bps the null pays ~6 bp/yr
more — again a bias against the null and against H_LIFT.

## Verdicts

1. **PARK stands for 964's quarterly tranche**, now on a measured basis: base rate 0.000 of 200,
   but 0.090 percentile on OOS Sharpe, 0.000 on OOS CAGR, and unselectable by every IS-only
   chooser at its own (panel, cadence).
2. **KILL for reading a tranched 4b pass as evidence of skill without its per-leg null
   percentiles.** In the subject cell four of five legs are free (null pass ~1.000) and the entire
   verdict is one leg the null never clears.
3. **KILL for the U56/`TOP20` tranche as a 4b object at either cadence** — null base rate 0.680
   (Q) and 1.000 (M).

Follow-ups filed: 998, 999, 1000 (995-997 were taken by the cloud lane in the same hour — idea 932's numbering defect again).
