# Idea 863 (lane C, 2026-09-15) — is the CORR-HI gate worth anything once the 2022 EPISODE is the only evidence?

**ANSWERED — and the queue's premise is FALSE. 2022 is NOT where this gate's work is. Removing
2022 entirely leaves the clause INTACT and slightly stronger (WORKS 33/40 cells ex-2022 vs 33/40
full; the memo cell 15.44% / 1.2591 / −13.83% ex-2022 against its own matched-gross twin's
14.77% / 1.1437 / −21.55%, 4b PASS full AND inside its OOS). The episode the clause actually
depends on is 2020: strip 2020 as well and WORKS collapses to 12/40 with the median Sharpe excess
going NEGATIVE (−0.0103). Verdict PARK under the rule fixed in advance — the clause has abundant
non-2022 evidence but the IS-alone rule-8 pick fails 4b's H2 leg on the 2022-free corpus. No RULES
change; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-15_is-the-CORR-HI-gate-worth-anything-once-2022-is-the-only-evidence_C.py`.
Panel B136 (`universe_broad.json`, 136 columns), scored sample 2009-01-13 → 2026-09-11, 10 bps,
weekly book, daily gate, t+1. Level `q = 0.17` FIXED at the memo's value. Two tuned parameters only
(the queue's own: **window** and **depth**), **all 40 grid points reported at all five corpora**
(`.grid.csv`, 200 rows). Deterministic, no network, no RNG.

## 0. Gates (printed before any verdict)

| Gate | Result |
|---|---|
| G1 runner identity — a depth-0 multiplier reproduces `engine.backtest` | max\|d\| **0.000e+00** PASS |
| G2 causality — `min_periods = w`, decided at t applied at t+1; no-threshold days rise with w | 0 / 0 / 11 / 263 / 515 / 767 / 1271 / 1775 PASS |
| G3 reproduction of idea 814's FULL cell (w=252, d=0.50) | **bit-exact** 14.02% / 1.1538 / −15.11% PASS |
| G4 determinism — grid recomputed | \|dSharpe\| **0.000e+00** PASS |
| G5 splice integrity — \|EX2022\| + \|ONLY2022\| = \|FULL\| | 4192 + 251 = 4443 PASS |

## 1. Comparands, corpus by corpus (10 bps, weekly, t+1)

| corpus | days | SPY | RULES v2 | UNGATED g=1.00 |
|---|---|---|---|---|
| FULL | 4443 | 15.16% / 0.8861 / −33.72% | 7.98% / 1.0993 / −12.24% | 14.20% / 1.0211 / −23.09% |
| **EX2022** | 4192 | 17.55% / 1.0247 / −33.72% | 8.95% / 1.2063 / −12.24% | 15.94% / 1.1436 / −23.09% |
| **ONLY2022** | 251 | −18.24% / −0.7096 / −24.50% | −6.99% / −1.4085 / −7.82% | −11.36% / −0.6345 / −21.45% |
| EX2020 | 4381 | 16.03% / 0.9896 / −24.50% | 8.45% / 1.1898 / −9.28% | 15.57% / 1.1458 / −21.65% |
| EXBOTH | 4130 | 18.53% / 1.1564 / −22.06% | 9.47% / 1.3053 / −7.90% | 17.45% / 1.2863 / −16.66% |

`WORKS(cell, corpus) := Sharpe(gated) > Sharpe(twin) AND |MaxDD(gated)| < |MaxDD(twin)|`, twin =
the same book held statically at the arm's realised mean gross **on that corpus**, at the arm's own
cost rung. This measure is comparand-free: it never touches SPY, so the 4b denominator problem
idea 814/861 found cannot drive it.

## 2. The grid — 40 cells at every corpus (the deciding table)

| corpus | WORKS | Sharpe leg | MaxDD leg | 4b | 4a | median ΔSharpe | median ΔMaxDD | median ΔCAGR |
|---|---|---|---|---|---|---|---|---|
| FULL | **33/40** | 34/40 | 38/40 | 26/40 | 0/40 | +0.0488 | +3.38 pp | +0.21 pp |
| **EX2022** | **33/40** | 33/40 | 39/40 | 27/40 | 0/40 | +0.0272 | +4.07 pp | +0.02 pp |
| **ONLY2022** | **26/40** | 26/40 | 30/40 | 14/40 | 0/40 | +0.0306 | +1.46 pp | +0.42 pp |
| EX2020 | 25/40 | 25/40 | 36/40 | 2/40 | 0/40 | +0.0055 | +2.63 pp | −0.03 pp |
| **EXBOTH** | **12/40** | 13/40 | 30/40 | 2/40 | 0/40 | **−0.0103** | +0.63 pp | −0.37 pp |

**H_PREMISE FAIL (26/40 < 30/40): 2022 alone is the WEAKEST of the three primary corpora.**
**H_NON2022 PASS (33/40 ≥ 20/40): non-2022 evidence is not scarce — it is the majority of the
evidence.** The queue asked whether anything survives 2022's removal; the answer is that the
clause barely notices. `4a` is 0/40 everywhere: nothing here ever beats the live book on 4a terms.

## 3. The memo's own cell at every corpus

| corpus | days | gate on | mean gross | GATED | matched-gross TWIN | WORKS | 4b |
|---|---|---|---|---|---|---|---|
| FULL | 4443 | 16.6% | 0.9172 | 14.02% / 1.1538 / −15.11% | 13.03% / 1.0211 / −21.33% | yes | PASS |
| **EX2022** | 4192 | 14.5% | 0.9276 | **15.44% / 1.2591 / −13.83%** | 14.77% / 1.1437 / −21.55% | **yes** | **PASS** |
| ONLY2022 | 251 | 51.4% | 0.7430 | −7.27% / −0.5507 / −14.85% | −8.32% / −0.6341 / −16.25% | yes | FAIL (H1,DD) |
| EX2020 | 4381 | 15.8% | 0.9211 | 14.73% / 1.2171 / −15.11% | 14.33% / 1.1456 / −20.06% | yes | FAIL (DD) |
| EXBOTH | 4130 | 13.6% | 0.9320 | 16.22% / 1.3293 / −13.25% | 16.23% / 1.2861 / −15.59% | yes | FAIL (DD) |

Read inside the **EX2022 OOS window** (2185 days): **17.06% / 1.4250 / −13.83%** against SPY's
19.98% / 1.1392 / −33.72% — 4b PASS. H_CELL PASS, H_4B_EX PASS. Note the EX2020 and EXBOTH 4b
FAILs are the *DD cap* alone, i.e. exactly the comparand artefact idea 814 named: the book's own
drawdown barely moves (−13.25% to −15.11% across all five corpora) while SPY's collapses from
−33.72% to −22.06%. The WORKS column, which has no SPY in it, passes at the memo cell everywhere.

## 4. Rule 8 walk-forward — the pick is chosen on a window containing no 2022 at all

IS = 2009-01-13 → 2016-12-31 (contains **no 2022 by construction**, so the chooser is itself
non-2022 evidence); OOS = 2017-01-01 → 2026-09-11, read once. **Both choosers pick the same cell**
(w=252, depth=0.75; IS Sharpe 1.0949, IS MaxDD −12.41%; interior in both dials; C2's eligible set
was 2/40).

| OOS corpus | days | ARM | matched-gross TWIN | SPY | RULES v2 | WORKS | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| FULL | 2436 | **14.37% / 1.2792 / −12.12%** | 12.17% / 1.0100 / −20.33% | 15.33% / 0.8767 / −33.72% | 7.88% / 1.1059 / −12.24% | YES | **PASS** | **PASS** |
| **EX2022** | 2185 | 16.87% / 1.4770 / −10.69% | 15.54% / 1.2479 / −20.97% | 19.98% / 1.1392 / −33.72% | 9.74% / 1.3128 / −12.24% | YES | **FAIL (H2)** | FAIL |
| ONLY2022 | 251 | −5.30% / −0.4447 / −11.84% | −6.83% / −0.6339 / −13.56% | −18.24% / −0.7096 / −24.50% | −6.99% / −1.4085 / −7.82% | YES | FAIL (H1) | FAIL |

**H_WF FAIL, on one leg and one leg only.** The rule-8 pick beats its matched-gross twin on every
corpus, and on the FULL OOS window it passes 4b *and* 4a — the only 4a pass anywhere in this run.
It fails 4b on EX2022 purely on **H2**: deleting 2022 removes the drawdown from SPY's second OOS
half, so SPY's H2 bar rises and the arm, whose whole product is a tamer path, cannot clear a bar
that is itself the absence of the crash it was built to survive. That is the same structural
defect in 4b's comparand that ideas 814 and 861 documented, arriving this time through the Sharpe
halves instead of the DD cap.

## 5. Ladders (reported, never selected) — the twin is priced at the arm's own rung

EX2022, memo cell: WORKS at **0 / 5 / 10 / 25 / 50 bps** (arm 1.3583 / 1.3088 / 1.2591 / 1.1097 /
0.8598 vs twin 1.2189 / 1.1813 / 1.1437 / 1.0305 / 0.8414) and at **lag 1 / 2 / 3** (1.2591 /
1.2076 / 1.1839 vs 1.1437). **H_LADDER PASS.** (An earlier draft of this script priced the twin at
the head rung while the arm paid the ladder's rung and reported a 25 bps failure; that comparison
was unfair to the arm and was corrected before any verdict was read. The corrected ladder is the
one above.)

## 6. Where the excess actually lives (calendar years, memo cell vs its own twin)

The arm beats its matched-gross twin in **11 of 18 calendar years**; cumulative excess **+16.10 pp**,
of which **2022 contributes +3.09 pp and 2020 contributes +8.56 pp** — more than half the total,
from a 3-month episode. Ex-2022 excess is +13.01 pp. The seven losing years (2011, 2013, 2014,
2015, 2019, 2021, 2024) cost −13.23 pp between them.

This is the run's real finding, and it is not the one the queue expected: **the clause is not a
2022 object, it is a 2020 object.** Remove both episodes (EXBOTH) and the grid-level evidence
inverts — WORKS 12/40, median ΔSharpe −0.0103, median ΔCAGR −0.37 pp. A correlation-spike gate
that pays only in the two fastest crashes on the sample, and costs a little in every ordinary year,
is a crash-shape bet, not a market-state clause.

## 7. Verdict (pre-registered rule, fixed before any number was read)

> KEEP-candidate (4b) iff H_NON2022 **and** H_CELL **and** H_4B_EX **and** H_WF.
> PARK if H_NON2022 alone. Else KILL.

| hypothesis | result |
|---|---|
| H_REPRO — idea 814's FULL cell rebuilds inside tolerance | **PASS** (bit-exact) |
| H_PREMISE — ONLY2022 WORKS at ≥ 30/40 | **FAIL** (26/40 — the queue's premise is wrong) |
| H_NON2022 — EX2022 WORKS at ≥ 20/40 ***DECIDING*** | **PASS** (33/40) |
| H_CELL — the memo cell WORKS on EX2022 | **PASS** |
| H_4B_EX — the memo cell passes 4b on EX2022, full and inside its OOS | **PASS** |
| H_WF — both IS-alone picks WORK and pass 4b on the EX2022 OOS corpus | **FAIL** (H2 leg) |
| H_LADDER — EX2022 WORKS at 0/5/10/25 bps and lag 1/2/3 | **PASS** |

**→ PARK.** Idea 814's PARK stands and is now better understood, not overturned: the doubt that
this run was sent to test (2022 dependence) is **retired outright**, and a sharper one replaces it
(2020 dependence, and a 4b comparand that punishes the arm twice — once through the DD cap, once
through the Sharpe halves — for the removal of the very crashes the arm exists to survive).
**NOT proposed for promotion.**

## 8. What this run retires and what it leaves open

Retired: the 2022-dependence doubt. The clause's value is not concentrated in 2022; on the
comparand-free WORKS measure 2022 is the weakest of the three primary corpora, and the ex-2022
corpus carries 33 of 40 cells.
Left open, and sharper: (a) the clause's dependence on the **2020** episode is severe and
untested by anything on the record — EXBOTH inverts the median Sharpe excess; (b) 4b's H1/H2 legs
inherit the same single-episode comparand defect as its DD cap, and the record has priced only the
DD side (queued below).

## 9. Survivorship (PROTOCOL rule 9)

B136 is `universe_broad.json`'s **current** constituents. Every CAGR above is biased upward and the
4b CAGR floor is easier than on a point-in-time panel. The correlation STATE is optimistic for the
same reason — the names that died are exactly the ones that would have co-moved hardest in 2020 and
2022. That bias cuts **in favour** of the clause on this run's central corpus: a 2022-free panel of
survivors is a generous place to look for non-2022 evidence, so H_NON2022's PASS is the weaker of
this run's two findings and the EXBOTH inversion the stronger one.
