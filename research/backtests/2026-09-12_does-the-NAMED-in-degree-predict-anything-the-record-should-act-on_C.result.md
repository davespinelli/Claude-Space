# Idea 793 (lane C, 2026-09-12) — does-the-NAMED-in-degree-predict-anything-the-record-should-act-on

**ANSWERED = NO. NAMED in-degree predicts exactly one thing — being OVERTURNED — and that is
the citation-exposure artefact, not a quality signal. KILL for capital; no RULES change, no
book promoted, no KEEP claimed, no memo. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched (rule 6).**

Script `2026-09-12_does-the-NAMED-in-degree-predict-anything-the-record-should-act-on_C.py`,
162 s, deterministic, no network. Corpus 1,564 committed text files, **710 rankable dated
runs**, 759 MB of committed data artefacts read. Self excluded from both sides of the graph.

## The parameter grid had to be re-scaled, and that is a result

Pre-registered at LAG ∈ {7, 14, 30, ALL}. **The whole committed record spans 9 calendar days
(2026-09-03 … 2026-09-12) and holds 710 runs**, so at L = 7 every citation the record contains
is already inside the predictor window and NAMED@7 = NAMED@14 = NAMED@30 = 903 identically.
The full ladder is printed as an appendix; `citations_beyond_window` — the material the
SURVIVE outcome is made of — reads 742 / 432 / 166 / 47 / **0 / 0 / 0** at L = 1 / 2 / 3 / 5 /
7 / 14 / 30. The grid is therefore **{1, 2, 3, FWD} × {REPRO, SURVIVE, KEEP4B} = 12 points,
all reported**. No day-lag of a week or more can separate predictor from outcome on a record
this young; that ceiling, not a tuning choice, set the rungs.

Also reported, never tuned: idea 790's own **NAMED@ALL is undirected in time** (it counts
earlier and same-day citers), which is why its in-degree is 1,878 against the strictly-forward
903.

## Gates

| gate | reading | verdict |
|---|---|---|
| G1 identity | `fast_backtest` vs `engine.backtest`, worst \|dr\| over 3 parents **1.388e-17** | PASS (1e-12) |
| G2 comparands | tape **pinned at 2026-09-10**: RULES v2 U56 8.61% / **1.1998** / **-12.05%**, OOS CAGR **9.45%**; SPY **15.11% / 0.8835 / -33.72%**; worst \|d\| **4.944e-05** | PASS (5e-04) |
| G2b tape drift | un-pinned (last bar 2026-09-11): 8.63% / 1.2018 / -12.05%, SPY 15.16% / 0.8861; drift **2.554e-03 on one extra bar** — reported, not absorbed; every price number below is on the FULL tape | reported |
| G3 graph | idea 790's NAMED rebuilt from the tree it saw (`git archive 35b031d` minus its own `.md`): **exact on 685 of 686**, total \|d\| = **1** of its 1,828 edges (0.055%) | **MISSED BY 1 EDGE, REPORTED NOT RELAXED** |
| G3b monotone | today's un-pinned NAMED@ALL decreases on **0 of 686** shared runs | PASS |
| G4 verifier | idea 790's `DATA_share` on 457 shared runs, max \|d\| **1.110e-16** | PASS (1e-09) |
| G5 monotone | NAMED@1 ≤ NAMED@2 ≤ NAMED@3 ≤ NAMED@FWD, **0** violations | PASS |
| G6 calibration | PLANT-TRUE **100.0%** of 579; PLANT-FALSE **46.0%** of 580 (idea 790 measured 46.0%) | PASS |

**G3 is a miss and is stated as one.** The residual is +1 on
`2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-in-record-units_C`.
Mechanism: the tree idea 790 globbed was a working directory mid-lane and is not exactly any
commit. Every headline is re-read with that run dropped (SENSITIVITY below) and moves in the
fourth decimal.

**G6 sets the floor that governs the REPRO column: 46.0%.** Any reproduction share near it
means nothing. The record's runs sit far above it (DATA_share mean 0.9052, median 0.9754), so
REPRO has real spread to be predicted — and none of it is predicted.

## The 12 tuned points

`rho` = Spearman(NAMED@L, outcome); `recency` = rank-partialled on exposure days; `topic` =
both ranks demeaned within the run's 6-way slug topic; `p` = two-sided permutation p over
2,000 seeded shuffles; `floor95` = 95th pct \|rho\| under that null. COUNTS = \|rho\| ≥ 0.20
**and** p < 0.05 **and** recency and topic each retain ≥ 50% of \|rho\|.

| lag | outcome | n | rho | t | p | floor95 | recency | topic | COUNTS |
|---|---|---|---|---|---|---|---|---|---|
| 1 | REPRO | 662 | +0.0150 | +0.39 | 0.6830 | 0.0749 | +0.0024 | +0.0114 | False |
| 1 | SURVIVE | 710 | **-0.2890** | -8.03 | 0.0000 | 0.0736 | -0.2572 | -0.2836 | **True** |
| 1 | KEEP4B | 710 | -0.0062 | -0.17 | 0.8565 | 0.0735 | +0.0319 | -0.0049 | False |
| 2 | REPRO | 662 | +0.0297 | +0.76 | 0.4455 | 0.0758 | +0.0166 | +0.0244 | False |
| 2 | SURVIVE | 710 | **-0.3059** | -8.55 | 0.0000 | 0.0753 | -0.2729 | -0.2963 | **True** |
| 2 | KEEP4B | 710 | +0.0378 | +1.01 | 0.3185 | 0.0733 | +0.0798 | +0.0396 | False |
| 3 | REPRO | 662 | +0.0101 | +0.26 | 0.8025 | 0.0766 | -0.0091 | +0.0028 | False |
| 3 | SURVIVE | 710 | -0.1976 | -5.36 | 0.0000 | 0.0708 | -0.1487 | -0.1877 | False (|rho| < 0.20) |
| 3 | KEEP4B | 710 | +0.0112 | +0.30 | 0.7720 | 0.0738 | +0.0675 | +0.0105 | False |
| FWD | REPRO | 662 | -0.0041 | -0.11 | 0.9175 | 0.0760 | -0.0268 | -0.0117 | False |
| FWD | SURVIVE | 710 | **-0.6081** | -20.38 | 0.0000 | 0.0746 | -0.5897 | -0.6002 | **True** |
| FWD | KEEP4B | 710 | +0.0272 | +0.72 | 0.4760 | 0.0749 | +0.0941 | +0.0283 | False |

**H_PRED technically HOLDS at 3 of 12 — and all 3 are SURVIVE cells. 0 of the 8 REPRO and
KEEP4B cells clear the bar, and every one of them sits inside its own permutation floor.**

- **REPRO: nothing.** \|rho\| ≤ 0.030 at every lag, p 0.45–0.92, all inside floor95 ≈ 0.076.
  Being leaned on does not predict that a run's own arithmetic reproduces from its own data.
- **KEEP4B: nothing, and what there is runs the wrong way.** \|rho\| ≤ 0.038, p 0.32–0.86. On
  the **79 runs carrying an actual committed `keep4b` column** — the leg that needs no
  narrative parsing — the sign is **NEGATIVE at every lag: -0.2573 / -0.2186 / -0.1886 /
  -0.1604**. The record leans, if anything, on the runs that produced *fewer* capital-relevant
  positives.

## What "survival" actually measures (H_SURV)

| lag | challenged | never named beyond L | rho(NAMED, overturned) all | **conditional on being challenged** | overturn rate |
|---|---|---|---|---|---|
| 1 | 142 | 568 (80.0%) | +0.2890 | **+0.2696** | 0.3944 |
| 2 | 96 | 614 (86.5%) | +0.3059 | **+0.3190** | 0.3854 |
| 3 | 45 | 665 (93.7%) | +0.1976 | **+0.2719** | 0.4222 |
| FWD | 178 | 532 (74.9%) | +0.6081 | **+0.4364** | 0.3764 |

**H_SURV HOLDS.** The negative rho(NAMED, SURVIVE) is an exposure artefact: 74.9–93.7% of runs
are never named beyond the window at all and score SURVIVE by default. Condition on the runs
that were actually challenged and **the sign flips positive** — more naming means *more*
overturning, at a 37.6–42.2% overturn rate. The one thing NAMED predicts is being argued with,
and among runs that are argued with it predicts losing. That is not a signal the record should
act on; it is the mechanical consequence of being cited at all.

**H_RECENCY FALSIFIED at the stated 0.50 bar but material:** rho(NAMED@FWD, exposure days)
**+0.3503** (t +9.95), rising monotonically 0.2168 → 0.2274 → 0.3061 → 0.3503 across the lag
ladder. Idea 790's time-undirected NAMED@ALL reads +0.1228. Exposure is the strongest single
confound the run measures; it is not a majority of the variance.

**H_TOPIC FALSIFIED:** within-topic demeaning retains **95.0%** of the headline \|rho\|
(recency-partialling retains 75.3%). The queue's "topic artefact" reading is refuted — the
association is not a topic effect. It is simply not an association with anything useful.

**SENSITIVITY (G3 residual):** dropping the one G3-offending run moves SURVIVE rho from
-0.2890 → -0.2889 (L=1), -0.3059 → -0.3072 (L=2), -0.1976 → -0.1983 (L=3), -0.6081 → -0.6096
(FWD). Nothing turns on it.

## Rule 8 walk-forward

**WF-A (corpus split at 2026-09-08, EARLY 347 runs / LATE 363).** Sign agreement IS → OOS on
the 9 comparable (lagged) cells **6/9**, median \|OOS rho\| 0.0578 against median \|IS rho\|
0.0238 — i.e. both halves are noise on REPRO and KEEP4B. Restricted to the **3** cells whose
IS \|rho\| clears its own permutation floor, sign agreement is **2/3 and they are SURVIVE
cells only**. SURVIVE@3 reads NaN out of sample because **not one late-vintage run has a citer
beyond 3 days** — the outcome has no variance on the OOS half. That is the corpus-age ceiling
again, reported rather than patched.

**WF-B (price, OOS read once).** NAMED@L priced as a decision rule: act on the IS-best parent
only if one of the record's backing claim-runs for it (idea 779's committed 607-claim census:
U56 120, B136 119, SMALL663 82) is in the top share by NAMED@L on EARLY citers only **and**
verifies at DATA ≥ 90%; else stand down to RULES v2 on U56. 4 lags × 5 shares = **20 decision
books, all reported**.

**THE GATE IS DEGENERATE: the 20 books take exactly 2 distinct values.** Either the gate fires
in all 6 (gross, cadence) cells — reproducing ALWAYS-ACT at OOS 13.04% / **1.1601** / -18.40% —
or in none, reproducing RULES v2 U56 at 9.47% / **1.2782** / -12.05%. The backing-claim sets
are so large that at any share ≥ 0.05 some backing run is always in the core. Beating RULES v2
**0/20**, beating ALWAYS-ACT **0/20**, beating BOTH **0/20** (a book equal to a control to
1e-09 is not counted as beating it). Beating SPY (0.8767) 20/20, which is what the always-act
arm does on its own. **H_ACT FALSIFIED: the statistic never changes a decision, so it cannot
improve one.**

**KEEP paths.** Price grid 3 parents × 2 arms × 3 gross × 2 cadence = **36 books: 4a 0/36, 4b
3/36, BOTH 0/36** (U56/MA-RS/g0.75/W, U56/MA-RS/g0.75/M, B136/MA-RS/g0.75/W) — **identical to
idea 790's grid one day and one tape bar ago, same three names.** Nothing here is a new
candidate: these are the record's standing MA-gate respread arms re-priced, and idea 787
already killed that whole shelf against an equal-weight bar. Decision books: **4a 0/20, 4b
17/20, BOTH 0/20**, and the 17 are the ALWAYS-ACT twin — declared before the run as a
diagnostic, never a capital candidate.

## Verdict

| hypothesis | outcome |
|---|---|
| H_PRED | HOLDS 3/12 — **all 3 SURVIVE, 0 of 8 REPRO/KEEP4B** |
| H_RECENCY | FALSIFIED at 0.50 (+0.3503, material not majority) |
| H_TOPIC | FALSIFIED (retains 95.0%) |
| H_SURV | **HOLDS** (+0.2719 conditional at L=3, +0.4364 at FWD) |
| H_ACT | **FALSIFIED** (0/20, 2 distinct books) |

**KILL for capital. NAMED in-degree does not predict reproduction, does not predict
capital-relevant output (and inversely tracks it on the runs that publish a `keep4b` column),
and the one thing it does predict — being overturned — is the exposure artefact H_SURV was
written to catch. Priced as a decision rule it is not a selector at any of its 20 points.**
Idea 790's concentration finding stands as a description of the graph; this run says the graph
carries no information the record should act on. No KEEP claimed.

**Caveats.** (1) The record is 9 days old; every forward statement here is bounded by that and
SURVIVE@3 has no OOS variance. (2) The overturn detector is a 300-character keyword window
around a naming mention — it will over-call a citer that discusses a KILL near an unrelated
reference and under-call a polite refutation; the conditional column in Part 3 is what the
verdict rests on, and it is robust to the level of that rate. (3) KEEP4B's narrative leg
agrees with its committed-data leg on only 54.4% of the 79 runs where both are readable, which
is why the data-only subset is reported separately and carries the opposite sign. (4)
Survivorship: universe.json / universe_broad.json / the small panel are current constituents.
