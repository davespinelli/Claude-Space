# Idea 971 (lane B, 2026-09-16) — is the 2009-2012 HALF the leg that kills every DISJOINT 4b pass?

**ANSWERED = THE LEG IS `L_H1`, BUT THE TAPE IS NOT 2009-2012 — IT IS WHICHEVER TAPE THE WINDOW
START HAPPENS TO PUT THERE, AND 2009-2012 IS ONE OF THE KINDEST CHOICES.**

`H_H1` **PASS at 1.000**: of the 144 DISJ-destroyed rows on 970's own 900-row grid, **143 bind on
`L_H1` alone and 1 on `L_H1`+`L_H2`; none binds on `L_H2` alone**. 970's single STRICT committed
casualty was not a coincidence — the first half is the whole clause.

`H_TAPE` **FAILS, and in the opposite direction**: sliding the in-sample window start forward does
not release the destruction, it **quadruples** it. Pooled over the 5 cost rungs, destroyed goes
**13 (w=2009) → 20 (2010) → 5 (2011) → 55 (2012) → 51 (2013)** of 60 reproduced REC passes, a
destroyed share of **0.217 → 0.333 → 0.083 → 0.917 → 0.850**. `H_SPY` **FAILS 0 of 3 panels**:
SPY's own `L_H1` bar is *minimal*, not maximal, at w=2009.

## The mechanism, named and measured

`L_DD`, `L_CAGR` and `L_OOS` are read full-sample under every split rule (**G8: 0 disagreements on
900 rows × 5 window starts**), so every created and destroyed row is a Sharpe-leg event by
construction. What moves is the **benchmark's** first half, not the books':

| window start | SPY's `L_H1` bar | median book `L_H1` | margin | `L_H1` pass rate (900 rows) | destroyed |
|---|---|---|---|---|---|
| 2009-01-01 | 0.838 | 0.924 | **+0.087** | 0.599 | 13 |
| 2010-01-01 | 0.805 | 0.885 | +0.079 | 0.572 | 20 |
| 2011-01-01 | 0.969 | 1.042 | +0.073 | 0.656 | 5 |
| 2012-01-01 | **1.807** | 1.619 | **−0.188** | 0.134 | 55 |
| 2013-01-01 | **1.877** | 1.694 | −0.183 | 0.220 | 51 |
| *(REC, for reference)* | 0.959 | 1.100 | +0.141 | 0.623 | — |

The books' own first-half Sharpe **rises** as the window slides into the QE melt-up (0.92 → 1.69).
SPY's rises faster (0.84 → 1.88), and the margin flips sign. Across the five window starts,
Pearson(`L_H1` pass rate, SPY's own `L_H1` bar) = **−0.957** and Pearson(median margin, SPY's bar)
= **−0.994** (Spearman −0.50 on 5 points; the rank statistic is weak because 2010/2011 swap).
2009-2012 is a window that contains the 2011 drawdown, so SPY's Sharpe there is *below* its
full-sample H1 bar. **Clause (i) is a dial on the benchmark's luck in whichever four years land
in `L_H1`, not a test of leg independence.** Derived rows are in `.mechanism.csv`; the pass-rate
column is `grid[f"DISJ{w}_L_H1"].mean()` over the committed `.grid.csv`.

## KILL 1 — clause (i) as written is not adoptable

The window start is a free, unpriced parameter and it swings everything it touches. Over the whole
900-row grid the REC5 4b pass count runs **21/19/19/21/2/3** at 0 bps and **12/12/12/16/1/3** at
10 bps for REC / w2009 / w2010 / w2011 / w2012 / w2013. A clause whose verdict count moves by
**16×** on a dial it does not name cannot replace one that at least fixes its windows by rule.

## KILL 2 — and it is not verdict-neutral out of sample either (`H_RULE8` PASS)

Rule 8, 135 picks = 5 window starts × 3 panels × 3 cadences × 3 IS-only choosers (each chooser
sees `[w, 2016-12-31]` and nothing else; **G6 0 mismatches** under permuted OOS rows). OOS 4b
passes by window start: **4 / 0 / 1 / 0 / 4**. OOS 4a: **0 / 0 / 0 / 0 / 1** — one pass in 135.
**8 of 27 (panel, cadence, chooser) slots take a different BOOK depending on the window start.**

Best OOS pick (U56 / W / w2009 / `CH_SHARPE` → `BAND03` @ g1.00, 2.35 turns/yr):
**OOS 12.67% / 1.2755 / −15.91%** vs **SPY OOS 15.21% / 0.8713 / −33.72%** and **RULES v2 OOS
9.45% / 1.2762 / −12.05%**; full sample 11.53% / 1.2006 / −15.91%, halves 1.2327 / 1.1752.
This is **not a new candidate** — it is the same U56/`BAND03` book ideas 972 and 997 already
published, reached from a third direction. It fails 4a (the live book's −12.05% drawdown).

## KILL 3 — the null does NOT share the books' binding leg (`H_NULLH1` FAILS at 0.356)

On 1,800 gross-matched rotating coin flips (`RANDROT`, **G4** gross 2.22e-16 / count 0 / turnover
9.28×), the median over the 9 (panel, cadence) cells of the share of destroyed draws binding on
`L_H1` is **0.356** at w=2009 against **1.000** on the real books, and `L_H2` binds on 0.707 of
them. The null's own 4b base rate is 0.000 at the median cell under every split rule. So the
clause's `L_H1` monopoly is a property of **books that passed REC 4b**, not of the window
arithmetic in general: a REC pass is, by selection, a book with a strong *second* half.

## THE REPRODUCTION DEFECT (G5 FAIL, and it is bigger than drift)

G3a (this run's REC statistics vs 970's committed `grid.csv`, 900 matched rows) fails at
CAGR 8.22e-04 / Sharpe 2.91e-03 / MaxDD 1.28e-06 / OOS_Sharpe 4.99e-03 against a 1e-09 bar.
**G3b, the verdict cross-run, PASSES: 0 disagreements on `p4b_REC` and 0 on `p4b_DISJ2009` vs
970's `p4b_DISJ`, over all 900 rows.** G5b (the null stream, same seeds, same construction) fails
at max |ΔSharpe| **2.541e-01** — and the failure is panel-structured:

| panel | max \|ΔSharpe\| | median | exactly reproduced |
|---|---|---|---|
| B136 (`prices_broad.csv`, cached **Fridays**) | **0.000e+00** | 0.000e+00 | **600 of 600** |
| SMALL663 (`prices_small.csv`, frozen) | 1.63e-07 | 2.0e-08 | 3 of 600 |
| U56 (`prices.csv`, **restated nightly**) | 2.54e-01 | 5.3e-02 | 0 of 600 |

A restated panel does not *perturb* a rotating null, it **resamples** it: one changed eligibility
flag changes which names `rng.choice` draws on that row and every row after it. **7.4% of the
null's REC 4b verdicts and 5.3% of its DISJ verdicts flip between 970's run and this one on the
same seeds.** Idea 974 reported that no committed grid is byte-reproducible on a later day; this
run localises it — the frozen caches reproduce *exactly*, and only the nightly one does not.
Reported, not tuned away.

## PROPOSED, NOT APPLIED (PROTOCOL rule 6)

`2026-09-16_disjoint-window-start-clause_B.memo.md` — a rule 4 reporting clause requiring any
disjoint-halves 4b to publish its window start and the benchmark's own per-half Sharpe.

## Gates: 7 of 9

G1 1.11e-16 · G2 0.000e+00 · **G3a FAIL** (nightly restatement, above) · **G3b PASS** 0/900 ·
G4 PASS · **G5 FAIL** (G5a determinism 0.000e+00 PASS; G5b cross-run, above) · G6 0 mismatches ·
G7 disjointness 0/0/0 at all 5 window starts on all 3 panels, REC H2∩OOS 2,223 / 2,222 / 1,969
days · G8 0 disagreements.

## Caveats

**SURVIVORSHIP (rule 9):** U56 / B136 / SMALL663 are current-constituent lists, so every CAGR and
drawdown LEVEL and every walk-forward number above is optimistic. The created/destroyed contrast
and the binding-leg census are the SAME books on the SAME tape under different window
definitions, so they are untouched by it.
**DEGENERATE DIAL:** SMALL663's tape starts 2010-01-04 and its warm-up ends 2011-01-13, so
w=2009, 2010 and 2011 are the SAME window on that panel — a third of the panel-level dial has
three levels, not five. Stated, not hidden; the U56 and B136 columns carry all five.
**5 POINTS:** the window-start dial has five levels, so every correlation above rests on five
observations and is quoted as a level relationship, not as a significance claim.
