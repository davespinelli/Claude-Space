# Idea 1157 (lane B, 2026-09-16) — is the SMALL / MAXDD cell the ONE PLACE where TAPE LENGTH beats REGIME?

## ANSWERED = NO. PREMISE REFUTED, TWICE OVER, AND THE CELL IS MECHANICAL.

1148 published 72 regime-to-length cells and exactly one read below 1: **SMALL / MAXDD at
R_MATCHED, 0.794259x**, quoted verbatim from its own committed `regime.csv` and reproduced here
**bit for bit (G7, |diff| 0.00e+00)** by a replica of its Arm-B code on its own seed. The cell is
real. What it is *about* is not the SMALL panel and not a single episode — it is the length of
the FRACTION LADDER the author happened to cut, and underneath that, arithmetic.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

`FRACTION LADDER` {F_1140 = 1/1,1/2,1/3 (1148's own); **F_FINE = 1/1,1/2,1/3,1/4,1/6** (headline,
the "finer sub-tape ladder" this idea asks for); F_FINER = 1/1,1/2,1/3,1/4,1/5,1/6,1/8} x `TAPE`
{T_OWN = each panel on its own tape; **T_MATCHED** = every panel restricted to the SMALL panel's
own trading days — the LENGTH-MATCHED LARGE-CAP CONTROL this idea asks for} = **6 combinations,
ALL published**. PANEL (3) x STATISTIC (6) x RATIO DEFINITION (3) x PARTITION {ALIGNED, OFFSET} x
EPISODE {KEEP, DROP} are NOT dials — all 432 cells are dumped.

## 1. IT IS NOT THE ONE PLACE. EVERY PANEL CROSSES AS SOON AS THE LADDER GETS FINER.

MAXDD at R_MATCHED, ALIGNED / KEEP:

| ladder | U56 (T_OWN) | B136 (T_OWN) | SMALL (T_OWN) |
|---|---|---|---|
| F_1140 (1148's) | 1.172 | 1.307 | **0.794** |
| F_FINE | **0.691** | **0.740** | **0.551** |
| F_FINER | **0.652** | **0.694** | **0.468** |

The multiplier from F_1140 to F_FINER is **0.39x–0.59x on all six (tape, panel) cells** — the
ladder moves every panel by about the same factor. Per rung it is starker still: at F_1140 the
SMALL cell has 74% of its 27 books sub-1 against U56 15% and B136 22%, but at F_FINE it is
**27 of 27 on all three panels** (U56 26/27 on T_MATCHED). H_FINE SUPPORTED, but for the reason
that kills the premise: the finer ladder does not confirm SMALL, it drags the large caps down to
it.

## 2. IT IS NOT A SMALL-PANEL FACT — H_PANEL REFUTED ON THE LENGTH-MATCHED CONTROL.

T_MATCHED / F_FINE MAXDD: **SMALL 0.560x, U56 0.619x, B136 0.579x** — the three panels are
indistinguishable, and B136 is *below* SMALL. The tape dial moves the cell by **0.009**
(0.551 -> 0.560); the fraction-ladder dial moves it by **0.326** (0.794 -> 0.468). The carrier is
the LADDER, not the panel.

## 3. IT IS NOT A SINGLE-EPISODE ARTEFACT — H_EPISODE REFUTED.

The SMALL anchor book's full-tape MaxDD is **-35.81%, trough 2020-03-18**. Dropping all of **2020**
moves the headline cell **0.551 -> 0.620**: still far below 1. Only in 1148's own coarse corner
(F_1140 + OFFSET) does dropping 2020 lift it over the line (0.553 -> 1.288), so *1148's particular
reading* is part-episode; the sub-1 finding on any finer ladder is not. Note the drop removes a
whole calendar year, more than the drawdown itself — an over-removal that can only make
H_EPISODE EASIER to support, and it still fails.

## 4. THE MECHANISM, WHICH IS THE PART WORTH KEEPING: the BETWEEN term carries 1148's OWN defect.

1148 corrected the **within** term for count inflation (max-minus-min grows with k) and left the
**between** term as `|median at 1/1 - median at 1/f_max|` — a range over the ladder's ENDPOINTS,
which grows as the ladder is extended downward, while the length-matched within spread does not.
On SMALL the between term runs **10.53 -> 15.39 -> 17.49** across the three ladders while the
within term sits at **8.36 / 8.48 / 8.18**; on U56 between runs **4.43 -> 6.92 -> 7.06** against
within **5.19 / 4.78 / 4.60**. The ratio is therefore not a property of the statistic and the
tape. It is a property of how far down the fraction ladder a run happened to cut. That is the
exact defect 1148 diagnosed in the within term and did not check for in the between term.

Why SMALL crossed FIRST at 1/3 is then a level fact and nothing more: its MaxDD is **-35.81%**
against U56's **-19.13%**, so both terms are ~1.9x larger, and the between term is the one that
outgrows.

## 5. AND THE WHOLE READING IS MECHANICAL — H_NULL SUPPORTED ON EVERY PANEL.

A moving-block bootstrap (L=63, the record's own) of the anchor book has **no regime ordering by
construction, only length**. Its MAXDD R_MATCHED median: **U56 0.681, B136 0.678, SMALL 0.633**,
with **0.92–0.98 of 200 draws sub-1** on every panel; IID nulls 0.583–0.704, same picture. The
observed SMALL cell, **0.551x**, sits inside its own null's 90% band **[0.441, 0.881]**. "Tape
length beats regime for MaxDD" is not a finding about small caps, about this tape, or about
markets: a maximum taken over more points grows with the number of points, and that is all this
measures. H_CONTINUUM **SUPPORTED 18 of 18** — MAXDD is among the two lowest-ratio statistics in
every (ladder, tape, panel) cell — so the 1148 cell is a threshold crossing in a continuum, not a
distinct phenomenon. Across all 432 cells, R_MATCHED reads sub-1 **69 times, and 14 of the 18
headline sub-1 readings are MAXDD**.

## GATES 7 of 7, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17; G2 CROSS-RUN the committed U56 W/H126/N=20 triple
3.18e-07; G3 SPY OOS triple 1.70e-04; G4 live RULES v2 MaxDD == committed -12.05% at 4.95e-05;
G5 determinism of the SMALL pipeline 0.00e+00; G6 1148's committed `regime.csv` present and its
MAXDD row quoted verbatim from the file; **G7 CROSS-RUN 1148's SMALL/MAXDD R_MATCHED 0.794259x
reproduced by a verbatim replica at |diff| 0.00e+00** — the premise this run refutes is refuted
on a number it first reproduces exactly.

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED AS A BOOK

The FRACTION LADDER dial is a READ of already-computed returns and cannot change a book: the 81
T_OWN rung books are byte-identical across all three ladders. The TAPE dial only TRUNCATES the
tape a book is read over. Scored at all **162 rungs** because rule 4 requires it. Rung chosen on
IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE: **10 of 72 picks clear 4b full,
10 of 72 clear 4b OOS, 0 of 72 clear 4a**; the IS chooser takes the OOS-best rung 20 of 72 times.
Whole grid: **4b full 31, 4b OOS 32, 4a 0** — T_OWN U56 10/27, B136 6/27, **SMALL 0/27**;
T_MATCHED U56 12/27, B136 3/27, **SMALL 0/27**. Binding leg among the 131 failures: **L_DD sole at
51**, L_CAGR sole at 18, L_H2 sole at 1. Every passing pick is the standing anchor or a
neighbouring GROSS/N rung of it — **U56 / W / H=126 / N=20 / gross 0.75, full 15.58% / 1.1397 /
-19.13%, halves 1.2037 / 1.0971, OOS 16.97% / 1.1643 / -19.13%** against **SPY OOS 15.21% /
0.8711 / -33.72%** and **live RULES v2 OOS 1.2762 / -12.05%**. Length-matching the U56 tape to
SMALL's costs the anchor 1.48pp of CAGR and 0.078 of Sharpe (14.10% / 1.0616 / -19.21%, OOS
15.93% / 1.1087). **NO NEW BOOK.**

## WHAT THE RECORD SHOULD DO WITH IT, STATED NARROWLY (proposed, NOT enacted — rule 6)

1148's drafted clause should not ship with the between term as written. A regime-to-length ratio
must either FIX the fraction ladder in the clause itself, or count-match the between term the way
1148 count-matched the within term; otherwise the ratio is an author's choice of ladder and two
runs quoting it are not comparable. And no regime-to-length ratio for MAXDD (or any maximum)
should be read as evidence at all without its own resample null beside it, because the null is
sub-1 everywhere.

## SURVIVORSHIP (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool is the current constituents of a
sub-$2B screen (**663 names after dropping 52 with `max_1d_move >= 1.0` from `data/small_meta.csv`,
715 listed; tape 2010-01-04 -> 2026-09-11**), so every name that fell below the screen, delisted
or went to zero is absent and the drawdowns read here are the SHALLOWEST the period could have
produced. A within-length spread and a between-length move contrast the same books over stretches
of the same inflated tape, so the bias very largely cancels out of the RATIO — the whole quantity
this run measures — and the null arm is a resample of one book, where it cancels exactly. It does
NOT cancel out of the 4b legs, measured against SPY, a real index, so the 31 full-sample 4b passes
are an UPPER bound.

## THE DECLARED APPROXIMATION, AND ITS DIRECTION

Every null here resamples ONE tape, so it prices sampling error around THIS regime and not regime
uncertainty across regimes; a null ratio is therefore biased TOWARD the reading it tests. H_NULL is
scored in the direction that favours calling the cell MECHANICAL — the conclusion this run reaches
— so that conclusion rests on the evidence that makes it hardest to avoid, not easiest. The EPISODE
arm drops a whole CALENDAR YEAR, more than the drawdown itself; that over-removal can only make
H_EPISODE easier to support, and it is refuted anyway.

Script `research/backtests/2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-REGIME_B.py`,
7 CSVs, console log, 5 LEADERBOARD rows.
