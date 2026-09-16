# Idea 972 (cloud lane, 2026-09-16) — does the OOS leg stay REDUNDANT under a PURELY IS 4b?

**ANSWERED = YES, AND MORE COMPLETELY THAN 970 COULD SHOW. Under a fully in-sample 4b the
Sharpe leg binds on `0 of 1,188` rows — R(L3) = **1.0000 exactly** — on all three panels and
all five cost rungs. Across the whole 13,500-row ladder and all three leg sets the Sharpe leg
changes **exactly one verdict** (1 of 332, under 970's hybrid set, on B136). The leg that
changes verdicts is `L4_DD` (5,006 of 6,194 under the fully-IS set), then `L5_CAGR` (1,105 of
2,293), then `L1_H1` (167 of 1,355) and `L2_H2` (4 of 1,192). **4b is a four-leg bar and the
bar is the drawdown cap.** KILL for "a fully-IS 4b is a usable stand-in for the real bar":
agreement 0.8741, 234 of 268 IS passes are false positives, and the rule-8 choosers' eight
IS-certified picks go **0 for 8** out of sample while four uncertified picks pass. KEEP as a
PROTOCOL rule 4 reporting clause, PROPOSED and not applied (rule 6). Nothing promoted.**

Script: `2026-09-16_does-the-OOS-LEG-stay-REDUNDANT-under-a-PURELY-IS-4b_cloud.py`
Artifacts: `.ladder.csv` (13,500 rows × 57 cols), `.redundancy.csv` (240), `.agreement.csv`
(20), `.binding_order.csv` (45), `.walkforward.csv` (36), `.cost_robustness.csv` (15),
`.gates.csv`, `.hypotheses.csv`, `.console.txt`.

## Gates — 8 of 8 PASS, printed before any hypothesis number

| gate | what | value | bar |
|---|---|---|---|
| G0 | `offset_mask(·, per, 0)` ≡ `engine.rebalance_mask` on D/W/M/Q | 0 rows | 0 |
| G1 | fast `Ctx` ≡ `engine.backtest` (returns **and** turnover) | 1.67e-16 | 1e-10 |
| G2 | `BAND03@0.75` ≡ `baseline.rules_v2_weights` | 0.00e+00 | 1e-12 |
| **G3** | **CROSS-RUN: idea 993's committed 13,500-row ladder, all rows × 14 cols** | **7.11e-15** | 1e-9 |
| **G4** | **LEG IDENTITY: this run's `LS_REC` verdict ≡ 993's committed `pass4b` column** | **0 disagreements / 13,500 rows** | 0 |
| G5 | determinism: U56/TOP20/CORE/M phase 0 rebuilt | 0.00e+00 | 0 |
| G6 | SMALL hygiene: `max_1d_move >= 1.0` tickers dropped | 52 | ≥1 |
| G7 | IS and OOS masks share 0 trading days on every panel | 0 | 0 |

G3+G4 together are the load-bearing pair: the ladder is idea 993's own object rebuilt from
scratch, **and** the leg set being varied reproduces the record's committed 4b verdict on every
one of 13,500 rows. What varies below is therefore the leg set and nothing else.

## (A) The redundancy ratio — R(L) = P(all five legs) / P(the other four)

Pooled over the whole 13,500-row ladder, `n_binding / n_other4`:

| leg | `LS_REC` (record) | `LS_970` (halves moved IS) | `LS_ISALL` (**fully IS**) |
|---|---|---|---|
| L1_H1 | 25 / 687 | 321 / 652 | 167 / 1,355 |
| L2_H2 | 4 / 666 | 8 / 339 | 4 / 1,192 |
| **L3_OOS (the Sharpe leg)** | **0 / 662** | **1 / 332** | **0 / 1,188** |
| **L4_DD** | **4,699 / 5,361** | 3,806 / 4,137 | **5,006 / 6,194** |
| L5_CAGR | 521 / 1,183 | 303 / 634 | 1,105 / 2,293 |

- `H_970` **PASSES at 1.0000**: 970's reading reproduces exactly — U56/M R 1.0000 (36 of 36),
  U56/Q R 1.0000 (17 of 17), zero binding rows in either.
- `H_ISRED` **PASSES at 1.0000** (bar 0.95): reading the leg **in sample** does not rescue it.
  R(L3) = 1.0000 on U56 (0 of 122 at 10 bps), B136 (0 of 145) and SMALL (0 of 1), and
  **1.0000 at every one of 0 / 5 / 10 / 25 / 50 bps** on U56 and B136. *SMALL's denominator at
  10 bps is a single row and is not evidence on its own; the pooled 0 of 1,188 is.*
- `H_BIND` **PASSES at 1,361** binding rows under `LS_ISALL` at 10 bps: the queue's question
  — *which leg, if any, ever changes a verdict* — has a sharp answer. `L4_DD` 1,084,
  `L5_CAGR` 240, `L1_H1` 36, `L2_H2` 1, **`L3_OOS` 0**.

**So L3's redundancy is not the window overlap 942 blamed (970 ruled that out), and it is not
an in-sample-versus-out-of-sample artefact either.** A book that clears the two half-Sharpe
legs, the drawdown cap and the CAGR floor has already cleared the Sharpe-versus-SPY bar, in
every window this ladder can be read in. The record's 4b is a four-leg bar whose binding
constraint is the drawdown cap.

## (B) But the fully-IS 4b is NOT a stand-in for the real bar

| panel | rows | agreement | IS passes | OOS passes | both | IS-only | OOS-only |
|---|---|---|---|---|---|---|---|
| U56 | 900 | 0.7856 | 122 | 115 | 22 | 100 | 93 |
| B136 | 900 | 0.8378 | 145 | 25 | 12 | 133 | 13 |
| SMALL | 900 | 0.9989 | 1 | 0 | 0 | 1 | 0 |
| **ALL** | **2,700** | **0.8741** | **268** | **140** | **34** | **234** | **106** |

`H_SAME` **FAILS at 0.8741** (bar 0.90). **87.3% of the fully-IS 4b's passes (234 of 268) do
not survive contact with the OOS window, and it misses 75.7% (106 of 140) of the real ones.**
The conditional lift is real but modest — P(OOS 4b | IS 4b) = 0.1269 against a base rate of
0.0519, a **2.45×** lift pooled (1.41× on U56, 2.98× on B136) — so the IS bar is *weak
evidence*, not a certification.

`H_ORDER` **FAILS at +0.1539** (bar +0.50): the *order* in which the legs bind is not stable
across windows either (Spearman over the five legs: U56 +0.30, B136 +0.15, SMALL +0.50). On
B136 `L2_H2` refuses 43.7% of rows out of sample against 0.67% in sample, and `L3_OOS` 33.1%
against 0.67%. Only `L4_DD` keeps its place at the top in every window and on every panel
(0.92 / 0.92 / 0.70 on B136, 0.80 / 0.80 / 0.67 on U56).

## (C) Rule 8 — (book, gross) chosen on 2009–2016 alone, OOS read once

36 picks (3 panels × 4 cadences × 3 IS-only choosers), canonical phase, 10 bps.
**OOS 4b 4 of 36; OOS 4a 0 of 36.**

| | OOS 4b FAIL | OOS 4b PASS |
|---|---|---|
| IS 4b FAIL | 24 | **4** |
| IS 4b PASS | **8** | **0** |

**Every pick the fully-IS 4b certified failed out of sample, and every pick that passed out of
sample had been refused in sample** (all four are 4-of-5-leg books). On the 36-pick selection
the IS bar is not weakly predictive — it is **anti-**predictive, which is the opposite sign to
the 2.45× lift it shows over the ladder as a whole. The ladder-wide lift is a statement about
*rows*; the 0-of-8 is a statement about *what an IS chooser actually ends up holding*, and only
the second one is rule 8.

`H_R8` **PASSES at 4 of 36** (C_IS4B 2, C_ISSHARPE 2, C_ISCAGR 0).
`H_4A` **PASSES at 38 of 13,500** ladder rows, but only **5 of 2,700** at the protocol's own
10 bps, and all five are `SMALL / BAND03 / CORE` at **off-canonical phases** (W phase 2,
Q phases 18–21) — a phase-search artefact, not an edge. At phase 0 there are none.

**The four OOS 4b picks** — `U56 / BAND03 / EXT (gross 1.00)` at D and W, reached by both
`C_IS4B` and `C_ISSHARPE`:

| | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | turns/yr |
|---|---|---|---|---|
| U56/BAND03/EXT/**D** | 11.20% / 1.1897 / −14.77% | 1.1992 / 1.1837 | **12.45% / 1.2871 / −14.77%** | 3.26 |
| U56/BAND03/EXT/**W** | 11.53% / 1.2007 / −15.91% | 1.2330 / 1.1755 | **12.67% / 1.2758 / −15.91%** | — |
| SPY | 15.10% / 0.8830 / −33.72% | 0.9591 / 0.8208 | 15.21% / 0.8713 / −33.72% | — |
| RULES v2 (live) | — / 1.2009 / −12.05% | 1.2325 / 1.1762 | — | — |

**This is not a new candidate.** It is the live band book at gross 1.00 on daily and weekly
cadence — the same object idea 997 published as a CONDITIONAL 4b KEEP-candidate on U56, whose
own single rule-8 pass in nine slots was `U56/BAND03@1.05` at OOS 13.31% / 1.2756 / −16.67%.
This run reaches it from a completely different direction (an IS-leg-count chooser over books
and gross rather than a gross ladder) and lands on the same D/W object, which is corroboration
of 997's window, not a second candidate.

## The clause this proposes — for Sunday review, NOT written into PROTOCOL.md (rule 6)

> *"4b's `L3_OOS` leg (OOS Sharpe > SPY's) is NON-BINDING and is reported as such: across a
> 13,500-row ladder and three leg sets — the record's, 970's half-shifted one, and a fully
> in-sample one — it changes exactly ONE verdict, and zero under the fully in-sample set. A 4b
> pass is a four-leg pass whose binding constraint is `L4_DD` (5,006 of 6,194 rows), and any
> claim that a book 'clears 4b' should name `L4_DD`'s margin. Separately, a fully in-sample 4b
> is NOT a certification and must not be quoted as one: it agrees with the real bar on 0.8741
> of rows, 87.3% of its passes are false positives, and on this run's rule-8 selection it went
> 0 for 8 while four books it refused passed."*

## Survivorship (rule 9)

U56 / B136 / SMALL are CURRENT-CONSTITUENT lists; SMALL additionally drops the **52** tickers
with `max_1d_move >= 1.0` per `data/small_meta.csv`. Every CAGR and drawdown LEVEL and every
4b / 4a count is optimistic, most severely on SMALL. The measured object is a RATIO of two pass
rates over the same rows on the same tape, so a bias that lifts numerator and denominator alike
largely cancels; what does NOT cancel is that an optimistic panel pushes more rows over every
level bar at once, which makes a leg look *more* redundant than it is. Every R(L) here is
therefore an **upper bound on redundancy** — a conservative reading of how often a leg binds —
and the LEVELS quoted for `U56/BAND03/EXT` do not cancel and are upper bounds.
