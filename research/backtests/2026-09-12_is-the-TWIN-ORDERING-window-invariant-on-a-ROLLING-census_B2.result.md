# Idea 609 — is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census (lane B **_B2**, 2026-09-12)

> **FILED AS AN INDEPENDENT REPLICATION, NOT A CLAIM ON THE IDEA.** Idea 609 was answered and
> committed twice while this run was executing — **aa87884** (lane B, headline WINDOW-matched twin,
> 0.0847) and **2c96cad** (cloud, headline FULL-matched twin, 0.322). This script was written from
> idea 605's committed outputs alone, without sight of either, and is committed under the `_B2`
> suffix so it overwrites neither. The queue entry for 609 is left as the prior runs set it.
>
> **What it adds, and it is only two things:**
>
> 1. **It reproduces the cloud run's FULL-matched headline exactly, on an independent
>    implementation.** At the shared headline cell (756-day window, 63-day step, 10 bps, pooled over
>    all three panels) this run gets **0.322034 = 19/59**, QROLL on top **0.644068**, and the cost
>    ladder **0.271186 / 0.322034 / 0.305085** at 0 / 10 / 25 bps. The cloud run published **0.322**,
>    **0.644**, and **0.271 / 0.322 / 0.305**. Two independently written census implementations, same
>    numbers to the digits published.
> 2. **It shows the verdict is not an artefact of the step-63 sampling both prior runs used.** Both
>    headlined 59 windows at step 63; this run reports **176 windows at step 21** as its headline and
>    **1,125 cells** (5 scopes × 5 window lengths × 3 steps × 15 cost rungs) in full. **Zero of the
>    1,125 reach 0.50.** Agreement moves only 0.0757 across window length and 0.0220 across step.
>
> **It does not adjudicate aa87884's 0.0847**, which is the WINDOW-matched convention; that
> difference was separately diagnosed in **7df829b** (lane C: 714 of 717 flips are arms whose gate
> never fires in the window, where WINMATCH makes the twin the arm itself and `dSharpe = 0` scores
> as a loss). This run uses idea 605's FULL-matched twin throughout and reports no WINMATCH leg.
> The three runs therefore agree on the verdict and differ only on a convention already named.
>
> Everything below is this run's own output, unedited.

**ANSWERED = NO. THE PUBLISHED ORDERING IS A FULL-SAMPLE OBJECT, NOT ONE A READER EVER SEES.**
Over 176 rolling 3-year windows the order idea 605 published, `QROLL > QEXP > ABS`, is what a reader
standing in the window would have measured **31.25% of the time** (55/176) — and **0 of the 1,125
(scope × window × step × rung) cells this run reports reaches even 0.50**, best anywhere 0.4314.
**KILL for capital.** No RULES change, no KEEP, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

Script: `2026-09-12_is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census_B2.py`
Outputs: `.console.txt` `.census.csv` `.windows.csv.gz` `.grid.csv.gz` `.walkforward.csv` `.g3.csv.gz`

## 0. Reproduction gates, read before any new number

| gate | result |
|---|---|
| G1 derived cost ladder `r_gate(c) = m·r0 − (c/1e4)(m·t0 + g·|dm|)` vs live `engine.backtest` through idea 399's apply_gate, all 15 rungs | max \|diff\| **3.469e-18** → PASS |
| G2 fast CAGR/Sharpe/MaxDD vs `engine.metrics`, 200 real series | **0.000e+00** → PASS |
| G4 idea 84 EWALL U56 g=0.85 @10bps | **11.75% / 1.046 / −17.89% / H 1.076/1.022** vs committed 11.8/1.05/−17.9/1.07/1.04 → PASS |
| G5 O(1) cumsum window-Sharpe vs direct `fsharpe` on the same slice, 648 (arm, rung, window) triples — the whole census rests on this | max \|diff\| **2.265e-14** → PASS |
| G3 idea 605's committed `.cells.csv.gz`, all 9,720 rows joined field-for-field | **2 of 3 panels PASS** (see below) |

### G3 found something the census had to be built around: the record's SMALL439 panel no longer exists

`data/prices_small.csv.gz` is rewritten by the daily Actions job. Commit **56e08b1 "Daily close
2026-09-11 [actions]" (2026-09-11 23:27 UTC) took it from 483 columns to 715** — from idea 605's
439 names + SPY to **663 names + SPY**. `baseline.load_universe(small=True)` and idea 399/602/605's
drop rule are unchanged; the cache under them is not. Every statistic the record files under the
label "SMALL439" from that commit onward is a different panel wearing an old name.

G3 per panel, bar declared on the statistic this run actually uses (a **sign** test):

| panel | n | win flips | rate | max \|dSharpe\| | max \|g_eff\| | verdict |
|---|---|---|---|---|---|---|
| U56 | 3,240 | 2 | **0.0006** | 7.73e-03 | 1.37e-04 | PASS |
| B136 | 3,240 | 13 | **0.0040** | 2.47e-02 | 1.02e-03 | PASS |
| SMALL439→SMALL663 | 3,240 | **724** | **0.2235** | 3.65e-01 | 1.35e-01 | **FAIL** |

**G3b, the data-drift calibrator** — five *ungated* reference books (SPY, RULES v1, RULES v2, EWALL
g=0.75, EWALL g=1.00: no gate, no twin, so any move is the caches moving under the record, not this
run's code):

| panel | max \|dSharpe\| ungated | max \|dCAGR\| ungated |
|---|---|---|
| U56 | 1.87e-03 | 1.92e-04 |
| B136 | 6.54e-03 | 8.21e-04 |
| **SMALL663** | **3.18e-01** | **2.54e-02** |

U56 and B136 drift at the daily-cache scale idea 406 documents; the small panel's *ungated* SPY-free
books move by a third of a Sharpe, because `g_eff` itself moves — the breadth series is a different
panel. So the failure is the cache, not the code. This run therefore calls the panel **SMALL663** by
its measured width and publishes every census number **twice**: on the three-panel population as
pre-declared, and on **POOLED_REPRO** = the two panels that reproduce idea 605. The verdict is the
same under both, so no headline rests on the swap.

## 1. The census — what a reader standing in a window actually sees

Population: **9,720 grid points** = 648 twin pairs (3 panels × 18 arms × 3 depths × 2 cadences ×
2 gross) × 15 cost rungs. Tuned, exactly two, both named by the queue: **window** ∈ {378, 504, **756**,
1008, 1260} trading days, **step** ∈ {**21**, 63, 126}. Headline 756/21 declared before the run
because the queue says "3-year". Cost is a *reported* axis here, not a tuned one — idea 605 already
showed the ordering is cost-invariant full-sample, so cost cannot be a selector for this question.

**Headline cell (756d window, 21d step, 10 bps, POOLED, n = 176):**

| | POOLED (3 panels) | POOLED_REPRO (U56+B136) | U56 | B136 | SMALL663 |
|---|---|---|---|---|---|
| **published order `QROLL > QEXP > ABS` seen** | **0.3125** | **0.2159** | 0.2386 | 0.2727 | 0.2645 |
| QROLL on top | 0.6534 | 0.6705 | 0.4432 | 0.7273 | 0.3613 |
| ABS on bottom | 0.6136 | 0.4602 | 0.4659 | 0.4148 | 0.5097 |
| pair QROLL > ABS | **0.9545** | 0.9375 | 0.7500 | 0.8977 | 0.6839 |
| pair QROLL > QEXP | 0.6989 | 0.7102 | 0.7330 | 0.8068 | 0.6839 |
| pair QEXP > ABS | 0.6136 | 0.5057 | 0.5057 | 0.4205 | 0.5742 |
| mean ρ vs published order | +0.6193 | +0.5595 | +0.4496 | +0.5364 | +0.4122 |

**The order a reader sees, ranked (POOLED, headline cell):**

| order (top → bottom) | windows | share |
|---|---|---|
| **QROLL > ABS > QEXP** | 60 | **0.3409** |
| QROLL > QEXP > ABS *(the published one)* | 55 | 0.3125 |
| QEXP > QROLL > ABS | 53 | 0.3011 |
| ABS > QROLL > QEXP | 5 | 0.0284 |
| strict tie | 3 | 0.0170 |

The published order is not even the **modal** one. Random ordering of three families is 1/6 = 0.1667,
so 0.3125 is above chance — but the honest reading is that three of the six orderings are live and the
record published one of them as the ordering.

**Which leg breaks.** `QROLL > ABS` holds in **95.45%** of windows and is the durable part of idea
605's claim. `QROLL > QEXP` (0.6989) and `QEXP > ABS` (0.6136) are both near coin-flips. **QEXP's
position is the whole instability** — which is exactly what idea 605's two-draw IS/OOS split hinted at
(IS `ABS < QROLL < QEXP`, OOS `QEXP < ABS < QROLL`) and what this census resolves at 176 draws.

**Both tuned dials, every grid point, none selected on** (POOLED, 10 bps):

| window \ step | 21 | 63 | 126 |
|---|---|---|---|
| 378 | 0.3041 | 0.2615 | 0.1818 |
| 504 | 0.2394 | 0.2381 | 0.1875 |
| **756** | **0.3125** | 0.3220 | 0.3000 |
| 1008 | 0.2805 | 0.2727 | 0.2857 |
| 1260 | 0.2368 | 0.2353 | 0.2308 |

Across the whole reported surface — **1,125 cells** = 5 scopes × 5 windows × 3 steps × 15 rungs:

| scope | min | max | mean | cells ≥ 0.50 | cells ≥ 0.80 |
|---|---|---|---|---|---|
| POOLED | 0.1000 | 0.3667 | 0.2594 | **0** | 0 |
| POOLED_REPRO | 0.0385 | 0.3846 | 0.2052 | **0** | 0 |
| U56 | 0.0000 | 0.4000 | 0.1624 | **0** | 0 |
| B136 | 0.0909 | **0.4314** | 0.2293 | **0** | 0 |
| SMALL663 | 0.0376 | 0.4091 | 0.2068 | **0** | 0 |

There is no window length, no step, no cost rung and no panel at which a majority of windows show the
published order. The result is not a knife-edge and is not tuned to the queue's 3 years.

**And idea 605's cost-invariance is itself a full-sample artefact.** Full sample the family order is
identical at all 15 rungs (ρ +1.000, reproduced here). *Within* a rolling window the order at 0 bps
equals the order at 100 bps in only **0.5398** of the 176 windows.

## 2. Rule 8 — the census as a selector, chosen on IS only, read once on OOS

60 windows end on or before 2016-12-31 (IS), 80 start on or after 2017-01-01 (OOS), 36 straddle and
are used by neither.

* IS top-family counts: **QEXP 50, QROLL 10**. OOS: **QROLL 72, ABS 5, tie 3**.
* **H7 FAILS: the IS-top family (QEXP) is not the OOS-top family (QROLL).** The census is not a
  usable selector — picking the "best" family on history picks the wrong one.
* IS match rate with the published order 0.1667; OOS 0.2875.

Capital leg, one book, chosen on IS Sharpe alone inside the IS-chosen family, read **once** on OOS
(B136, `QEXP L0.12 d1.00 D g1.00`, 10 bps, IS Sharpe 1.035):

| book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| **609 rule-8 pick** | **14.34%** | **1.0700** | **−15.87%** | 1.1513 | 0.9866 | **14.21%** | **1.1034** | **−15.87%** |
| RULES v2 baseline (live) | 7.98% | 1.0993 | −12.24% | 1.2348 | 0.9658 | 7.88% | 1.1059 | −12.24% |
| RULES v1 (previous) | 6.41% | 0.6375 | −21.19% | 0.7933 | 0.5038 | 5.87% | 0.5702 | −21.19% |
| SPY | 15.16% | 0.8861 | −33.72% | 0.9596 | 0.8259 | 15.33% | 0.8767 | −33.72% |

Its matched-mean-gross static twin at the same rung: Sharpe 1.0211, **dSharpe +0.0488, dOOS +0.0939**.

**Both KEEP paths on every one of the 9,720 grid points:** 4a **14**, 4b **1,952**, both **4**. At
10 bps alone, 4b passes **141 of 648**. **A 4b pass is not informative here** — on these panels 4b is
carried by the gross dial, as the record has found repeatedly, and one in five grid points clears it.
4a is essentially empty (14/9,720, all at ≤ 5 bps on B136). The pick's own 4b pass is therefore
**not** a reason to put capital behind it, and H7's failure is the reason not to.

## 3. Pre-registered hypotheses (bars declared in the docstring before the run)

| | bar | result | |
|---|---|---|---|
| H1 AGREEMENT | published order seen in ≥ 0.80 of headline windows | 0.3125 (repro-panels 0.2159) | **FAIL** |
| H2 TOP | QROLL tops ≥ 0.90 of windows | 0.6534 (0.6705) | **FAIL** |
| H3 BOTTOM | ABS is bottom in ≥ 0.80 of windows | 0.6136 (0.4602) | **FAIL** |
| H4 WINDOW-LEN | agreement moves < 0.15 across the 5 window lengths | span 0.0757 | PASS |
| H5 STEP | agreement moves < 0.05 across the 3 steps | span 0.0220 | PASS |
| H6 COST | order at 0 bps == order at 100 bps in ≥ 0.90 of windows | 0.5398 | **FAIL** |
| H7 RULE-8 FAM | IS-top family == OOS-top family | IS QEXP / OOS QROLL | **FAIL** |
| H8 CAPITAL | the rule-8 book passes 4b | 4b True, 4a False | PASS |

**3 of 8 pass.** H4/H5 passing is what makes the three failures load-bearing: the agreement rate is
stable across both tuned dials, so ~0.26 is the answer, not an artefact of the window choice.

## 4. What the record should do with this

1. **Idea 605's ordering claim should be restated as a single pairwise claim.** `QROLL > ABS` survives
   at 0.9545 of windows and is publishable. `QROLL > QEXP > ABS` is a full-sample object seen in about
   one window in three and should not be quoted as an ordering a reader would measure.
2. **Cost-invariance of an ordering needs a window, not a full sample.** ρ = +1.000 at all 15 rungs
   full-sample coexists with only 54% within-window agreement between 0 and 100 bps.
3. **Any committed statistic labelled `SMALL439` produced after 2026-09-11 23:27 UTC is a different
   panel.** This is queue idea 565's shape (artefacts reading a nightly-rewritten file) landing on a
   *price* cache, not a metadata file. A census of the record's SMALL439 rows against the commit date
   is filed as a follow-up; nothing in this memo asks for a PROTOCOL edit (rule 6 — Sunday review).
4. **Do not put capital behind the rule-8 pick.** It passes 4b, but so do 1,952 of 9,720 grid points,
   and the selector that produced it failed its own out-of-sample test.

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic; the gate-minus-twin contrast and its window census are the durable part. SMALL663 starts
2010-01-04 and joins only windows its own calendar covers ≥ 90% of (155 of 176 at the headline cell).
The master census calendar is U56's eval index, 2009-01-13 → 2026-09-11, 4,443 days._

Follow-up filed: **826** (adjudicate the three 2026-09-12 runs of idea 609 against each other — this
run and the cloud run agree to the published digit under FULLMATCH, aa87884's 0.0847 is WINMATCH, and
the record currently carries all three numbers under one idea number). Ideas 823/824/825 drafted by
this run were dropped: the prior runs' own follow-ups already cover the SMALL439 cache rewrite and the
matching-convention question.
