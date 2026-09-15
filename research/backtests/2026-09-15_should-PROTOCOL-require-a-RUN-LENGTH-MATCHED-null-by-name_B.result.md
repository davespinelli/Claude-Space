# Idea 871 — should PROTOCOL require a RUN-LENGTH-MATCHED null by name? (lane B, 2026-09-15)

**ANSWER = YES, PROTOCOL SHOULD NAME A MATCHED STATISTIC — AND THE STATISTIC IS THE SWITCH COUNT,
NOT THE RUN-LENGTH DISTRIBUTION. The queue's stated exposure, however, IS NOT THERE: 0 of 70
committed placebo-bearing files name RAND without also naming BLOCK. KILL for capital.**

No RULES change, no PROTOCOL edit, nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched (rule 6). One PROTOCOL line is PROPOSED, NOT APPLIED. A 4b
KEEP-candidate falls out as a by-product, is memo'd, and is explicitly NOT proposed.

## Design
3,456 real gate arms (3 panels × 8 gate families × level q × window w × depth × cadence × gross),
each priced against **four** firing-rate-matched, information-free nulls at **10 md5 seeds** and
**three cost rungs** — 414,720 placebo cells, every grid point published. The two tuned parameters
the queue names are **claim set** (gate family, both directions always reported) and **null**.

| null | rate | switch count | run-length multiset | run order | calendar |
|---|---|---|---|---|---|
| RAND (idea 602/606) | y | n | n | n | n |
| SWITCHMATCH (NEW) | y | y | n | n | n |
| RUNPERM (NEW) | y | y | y | n | n |
| BLOCK (idea 602/606) | y | y | y | y | n |

## Gates (printed before any new number was read)
G1 0.000e+00 · G2 0.000e+00 · G4 0.000e+00 · G6 0.000e+00 — all PASS.
**G3 PASS 8 of 8**: idea 815's committed RAND/BLOCK headline rebuilds here (RAND +0.1709..+0.2503,
share>0 0.993–1.000; BLOCK −0.0347..+0.0725).
**G5: three arithmetic legs PASS at 0 violations** (firing-day count, RUNPERM multiset, SWITCHMATCH
run count). **Its fourth leg FAILS as printed** — on short synthetic paths SWITCHMATCH reproduces
the real multiset 99 of 1,423 times (7.0% against a 5% bar). That leg is reported FAILED and then
settled where it matters: **on the 3,456 REAL arms SWITCHMATCH reproduces the real multiset in
0.00% of draws** (RUNPERM 100.00%, BLOCK 85.19% — its wrap point — RAND 0.00%), so the
H_SWITCH-vs-H_RUNMATCH contrast is real here and not a construction coincidence.

## The answer to Q2 (COST): the whole RAND–BLOCK gap is switch cost
Pooled median (RAND − BLOCK) excess: **−0.0015 at 0 bps, +0.1852 at 10 bps, +0.4782 at 25 bps.**
RAND's switch-count ratio is **13.34×** the real arm's; every matched null's is **1.00**.
Spearman(placebo switch-count ratio, excess) = **−0.001 / +0.567 / +0.634** at 0 / 10 / 25 bps.
H_COST PASS (ratio −0.008), H_ZERO PASS (|gap| 0.0015), H_MECH PASS.
**RAND is not a null. It is a turnover surcharge**, and it is exactly zero at zero cost.

## The answer to Q3 (WHICH statistic): the switch count already suffices
Per-arm medians, at every rung: **|RUNPERM − BLOCK| 0.0142–0.0144**, **|SWITCHMATCH − BLOCK|
0.0144–0.0146**, against a seed-noise floor of **|RAND − BLOCK| = 0.0145 at 0 bps**. Both
H_RUNMATCH and H_SWITCH PASS, at values indistinguishable from noise and from each other, on all
3,456 arms (0.00% are degenerate, median 38 runs of mean length 15.4 days). Preserving the
run-length *multiset* buys nothing beyond preserving the *count*.

**Honest limit on that conclusion.** SWITCHMATCH destroys the exact multiset (0.00% match) but its
mean run-length dispersion is still **0.919×** the real arm's, because a uniform random composition
of k days into m runs is not a wild distribution. So what is demonstrated is that the count
suffices *against a null of comparable dispersion* — not against an arbitrarily shaped one.

## Rule 8 on the statistic
Spearman(IS gap, OOS gap) = **+0.906 to +0.935 in 8 of 8 families** (H_WF PASS, bar +0.30 in ≥6).
The gap is a fully mechanical, reproducible property of the null — which is what makes it worth
writing into PROTOCOL once rather than re-measuring per idea.

## Rule 8 on the books, and both KEEP paths (10 bps, next-day, weekly)
Selector declared IS-only: highest 2009–2016 Sharpe over every arm of the panel.

| panel | IS-pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | BREADTH-HI q0.12 w2016 d1.00 W g1.00 | 14.18% | 1.123 | −19.91% | 1.144/1.107 | 14.81% | 1.150 | −19.91% | ✗ | **✓** |
| B136 | BREADTH-HI q0.12 w2016 d1.00 D g1.00 | 12.63% | 0.949 | −21.58% | 1.257/0.660 | 9.49% | 0.743 | −21.58% | ✗ | ✗ |
| SMALL | CORR-LO q0.17 w504 d1.00 D g1.00 | 8.06% | 0.585 | −45.59% | 0.805/0.460 | 6.33% | 0.451 | −45.59% | ✗ | ✗ |
| — | RULES v2 live (U56) | 8.64% | 1.208 | −11.90% | 1.237/1.186 | 9.49% | 1.286 | −11.90% | — | — |
| — | SPY (U56 window) | 15.13% | 0.885 | −33.72% | 0.959/0.824 | 15.27% | 0.874 | −33.72% | — | — |

Base rate over all 3,456 arms, unselected: 4a **1** (0.03%), 4b **378** (U56 239/1152 = 20.7%,
B136 139/1152 = 12.1%, SMALL 0/1152). The U56 pick's 4b pass is the base rate of this grid, its
DD-cap margin is 0.32 pp, and its family (BREADTH-HI) carries the *smallest* placebo excess of the
eight measured here (+0.0128, share>0 0.592). Memo'd, **not proposed**.

## Q1 (CENSUS) — the exposure the queue assumed is not in the record
70 committed files carry placebo prose. **RAND-only: 0 (0.0%).** BLOCK-only 7 (10.0%), both 16
(22.9%), **neither 47 (67.1%)**. So no committed claim is priced against RAND alone; the real
unadjudicable mass is the two-thirds of files that name no kind at all. A file naming both is safe
only if its *headline* number is the BLOCK one — the census bounds exposure, it does not clear it.

## PROTOCOL line PROPOSED, NOT APPLIED (rule 6)
> *Add to rule 4: "A placebo or permutation control must match the real arm's firing RATE and its
> SWITCH COUNT (number of state changes), and every placebo-differenced number must name the null
> that produced it. A rate-only null such as an i.i.d. day shuffle is not admissible at non-zero
> cost: it multiplies the real arm's switch count by ~13× and inflates the published excess by
> +0.19 of Sharpe at 10 bps and +0.48 at 25 bps, all of which is switch cost and none of which is
> signal."*

## Caveats
SURVIVORSHIP: all three panels are current-constituent lists (SMALL additionally drops every ticker
with max_1d_move ≥ 1.0), so CAGR and drawdown LEVELS are optimistic; the null-vs-null differences
this run is about are computed on one fixed real arm at a time and are the durable part. Binding
drawdown is 2020. Deterministic (md5-seeded); re-running reproduces every number bit-for-bit.

**Verdict: ANSWERED = YES (name the SWITCH COUNT) / PREMISE PARTLY REFUTED (no RAND-only exposure)
/ KILL for capital.**
