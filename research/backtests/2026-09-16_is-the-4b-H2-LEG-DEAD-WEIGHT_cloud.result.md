# Idea 1014 — is the 4b H2 LEG DEAD WEIGHT?

**cloud lane, 2026-09-16, idea 2 of 2.**
Script: `2026-09-16_is-the-4b-H2-LEG-DEAD-WEIGHT_cloud.py`

## ANSWERED = NO, NOT DEAD — it is a FREQUENT CO-BINDER that almost never DECIDES.
## KILL the "dead weight" framing, and KILL 1001's `leg2 rate 1.000` as a property of the leg.

`L2_H2` is in the binding set of **54.3%** of the record's committed 4b FAIL rows — *more
often than `L1_H1` (46.7%) or `L3_OOS` (49.6%)*. It is the **sole** binder in **2,622 of
896,542 (0.29%)**. Deleting it from 4b therefore removes **2,622 rows' worth of FAIL** — 0.29%
of the FAIL population, but **+2.29% of the record's 114,655 committed PASS rows**. The clause
removes something. It is small, and it is not nothing.

## THE ARITHMETIC THE QUESTION REDUCES TO

Deleting a leg from a conjunction is **monotone**: it can never break a PASS, and it flips a
FAIL to a PASS **exactly** when that leg is the sole binder. **G7 asserts this row by row on
the committed masks (0 disagreeing rows, both directions)** rather than assuming it. So
"does the clause remove anything" has a closed form, and it is computed for **all five legs**,
because dead weight is comparative.

## THE CENSUS — 454 committed CSVs, 1,011,363 rows, 896,542 parsed 4b FAIL rows

**IN-FAIL** (the leg is somewhere in the binding set):

| claim set / defn | n | L1_H1 | **L2_H2** | L3_OOS | L4_DD | L5_CAGR |
|---|---|---|---|---|---|---|
| ALLROWS / STRICT | 896,542 | 0.4672 | **0.5432** | 0.4960 | 0.5882 | 0.6921 |
| REALROWS / STRICT | 651,674 | 0.5158 | **0.5798** | 0.5349 | 0.5588 | 0.7126 |
| ALLROWS / RECOMP | 107,945 | 0.2575 | **0.3389** | 0.2818 | 0.6191 | 0.6639 |
| FILEWT / STRICT | 441 files | 0.4167 | **0.5108** | 0.4534 | 0.6132 | 0.6098 |
| FRESH / STRICT | 10,474 | 0.4105 | **0.5137** | 0.4517 | 0.6714 | 0.7577 |

**SOLE = the deletion-flip rate:**

| claim set / defn | L1_H1 | **L2_H2** | L3_OOS | L4_DD | L5_CAGR |
|---|---|---|---|---|---|
| ALLROWS / STRICT | 0.00742 | **0.00292** | 0.00013 | 0.17526 | 0.18667 |
| REALROWS / STRICT | 0.00821 | **0.00371** | 0.00016 | 0.14349 | 0.18001 |
| ALLROWS / RECOMP | 0.00561 | **0.00041** | 0.00003 | 0.30901 | 0.25114 |
| REALROWS / RECOMP | 0.01151 | **0.01117** | 0.00068 | 0.23832 | 0.27657 |
| FILEWT / STRICT | 0.01862 | **0.01234** | 0.00012 | 0.20991 | 0.20218 |
| FRESH / STRICT · RECOMP | 0.00897 | **0.00067** | 0.00000 | 0.20823 | 0.16775 |

## THE PRE-REGISTERED SCORECARD — 2 of 7, and every failure is the answer

- **H_DEAD FAIL (0.5432 vs a < 0.25 bar).** The leg binds constantly. "Dead weight" is the
  wrong word for a leg present in more than half of all failures.
- **H_NOFLIP PASS (0.00292 vs < 0.005).** It decides almost nothing.
- **H_LEAST FAIL, 0 of 7 cells.** The record's deadest leg is **`L3_OOS`**, not `L2_H2`, in
  *every* claim-set × definition cell: 0.00013 vs 0.00292 on ALLROWS/STRICT, and **0.00000 vs
  0.00067 on fresh prices**. 1001 named the wrong leg.
- **H_NEST FAIL (0.7153 vs ≥ 0.90).** `L2_H2` is not a restatement of `L1_H1`: when H2 fails,
  H1 survives **28.5%** of the time. The two half-sample legs carry different information.
- **H_1001 FAIL, decisively.** On a fresh 120-cell × 100-draw ladder `p_L2_H2` averages
  **0.5544** with a minimum of **0.0000** — not 1.000. Broken out: the null clears H2 **0.9042
  at 0 bps, 0.4570 at 10 bps, 0.3020 at 25 bps**; the **real books** clear it **0.825 / 0.750 /
  0.575** at the same rungs. **1001's "leg2 rate 1.000 on 45 books × 5 windows" is a property
  of its 45-book set — committed passers plus their controls, a population selected for
  passing — not of the leg.** A leg has no variance in a sample chosen for clearing it.
- **H_STABLE FAIL.** The deletion rate moves **0.00041 → 0.01234 → 0.02810** (30×) across the
  two tuned dials. The *magnitude* is dial-dependent and must be quoted with its arm; the
  *ordering* — H2 two orders below the level legs, one order above `L3_OOS` — holds in all 7.
- **H_RULE8 PASS. 18 of 18** rule-8 picks score identically under 4b and 4b-minus-H2.

## RULE 8 (PROTOCOL rule 8) — OOS 4b **0 of 18**, 4b-minus-H2 **0 of 18**, 4a **0 of 18**

(book, cadence) chosen on 2009–2016 alone by three IS-only choosers × 2 panels × 3 rungs,
2017–2026 read once, scored under both conjunctions. Best pick `U56 C_ISSHARPE → TOP10/M
@0 bps`: OOS **18.05% / 1.1410 / −23.17%**. Comparands: SPY OOS **15.21% / 0.8713 / −33.72%**
(U56), 15.33% / 0.8769 / −33.72% (B136); RULES v2 @10 bps OOS **9.45% / 1.2765 / −12.05%**
(U56), 7.88% / 1.1061 / −12.24% (B136). **Every pick binds `L4_DD`**, and 8 of 18 also carry
`L2_H2` — as a co-binder, never alone. No KEEP candidate on either path, so no memo.

## GATES — 7 of 9, and both failures are facts about the record

- **G1 FAIL: 83 of 326,548** rows carry a committed `pass4b` that its own `fail4b` contradicts
  — **the same 83 rows idea 1010 found**, reproduced independently. Not a new defect; a
  confirmed one.
- **G3 FAIL (max |d| 1.49e-02 over 20 shared cells) — and G3b diagnoses it exactly.**
  **G3b PASS at 9.54e-17**: restricted to the *exact 449-file list idea 1010 committed*, this
  run reproduces 1010's census bit-for-bit on all five legs, at its published 883,294 rows.
  The whole miss is **corpus growth**: 5 new FAIL-bearing files and 13,248 new rows landed in
  `research/backtests/` in the hours between the two runs. **The record's own census is not
  reproducible across time unless the file list is pinned, because the corpus is append-only
  and contains the censuses themselves.** This run watched it happen live: its first pass read
  896,479 FAIL rows and its second, after writing its own `.freshreal.csv`, read **896,542**.
- G0 PASS (235 unparsed values of 1,011,363, all **excluded**, none guessed at) · G2 PASS
  (0 of 126,715) · G4 PASS (2.08e-17 / 4.44e-16) · **G5 PASS: SPY OOS ≡ the record's committed
  15.21% / 0.8713 / −33.72%** · G6 PASS (0.0) · **G7 PASS (0 disagreeing rows)**.

## SURVIVORSHIP (PROTOCOL rule 9)

The RECORD arm is a census of committed text and inherits its sources' bias. The FRESH arm
runs on U56 / B136, **current-constituent lists**. Survivorship lifts a book's Sharpe in *both*
halves together, which makes the half-sample legs easier to clear and therefore makes `L2_H2`
look **deader** than it would on a real-time panel. Every "dead weight" reading here is an
**upper** bound on deadness and every deletion-flip count a **lower** bound — i.e. the bias
works in favour of 1001's claim and the claim still fails.

## WHAT 1001 MAY STILL SAY / MAY NO LONGER SAY

**May still say:** `r_leg2_spyH2` was undefined *in its own 45-book sample*, and `L2_H2`
decides a 4b verdict alone in well under 1% of the record.
**May no longer say:** that the H2 leg passes at every window, that it is dead weight, or that
it is the leg 4b could drop. The leg that comes closest to dropping cleanly is **`L3_OOS`**
(sole binder 0.013% of the record, **0.000% on fresh prices**), and even that one is not free:
deleting it would add rows to the PASS population of a bar the record already reads too
loosely at low cost rungs.

## PROPOSED (not applied — PROTOCOL rule 6 reserves rule changes to Sunday review)

> *"`L2_H2` stays in 4b. It is a CO-binder, not a decider: present in 54.3% of committed FAIL
> rows and sole in 0.29% of them. A run may therefore not cite the H2 leg as independent
> evidence for a pass — clearing it is close to free — and may not drop it to make a book
> pass, which would widen the PASS population by 2.3%. A census of the record's committed rows
> states the FILE LIST it read, because the corpus is append-only: the same census run six
> hours apart differs by 13,248 rows."*

**No RULES change, no book promoted, no KEEP claimed, no memo.** RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.
