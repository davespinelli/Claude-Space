# Idea 310 — is-EVOL-the-real-survivor-not-DISP (lane B, 2026-09-09)

**ANSWERED / KILL OF BOTH SURVIVOR CLAIMS. `evol` is the more stable of the two — but "more
stable" here means 8 sign flips instead of 18, not a usable ordering: every headline partial's
bootstrap CI crosses zero and the per-point partial does not replicate across a fresh seed block
for either characteristic.**

## Gates (graded before any new number was read)

| gate | what | result |
|---|---|---|
| G  | (q=0.500,k=40) stratum rebuilt from prices, seeds 0..59, vs idea 293's committed `.panels.csv`, 17 columns x 60 panels | **PASS, max abs diff 1.110e-16** (14 of 17 columns exact at 0.000e+00) |
| G2 | idea 284's published within-stratum `corr` rho (CAND10 −0.3648 / CAND20 −0.4815 / EWall −0.4708) | **PASS, |d| 0.0000 on all three** |
| G3 | idea 284's published joint-fit t on disp/evol at that cell | **PASS, max |dt| 0.0047** |
| G4 | idea 293's published 27-point mean partials (disp +0.0046, evol +0.1551) | **PASS, |d| 0.0000 on both** |

Both prior runs' arithmetic is confirmed. The disagreement is real, not a bug in either.

## What the disagreement actually is

1. **Different statistics, both computed correctly.** Idea 284's "disp survives / evol collapses"
   is its **joint-fit t** (disp +1.43/+1.31/+1.65, evol −0.97/+0.23/−0.49); its **marginal** rho
   is positive and significant for BOTH characteristics at that cell (disp +0.39/+0.53/+0.47,
   evol +0.23/+0.42/+0.32). Idea 293's "+0.1551 vs +0.0046" is the **rank-partial**, averaged
   over 27 points.
2. **At idea 284's own stratum, idea 284 is right.** Rank-partials at (q=0.500,k=40): disp
   **+0.2605 / +0.2641 / +0.2470**, evol **−0.0734 / −0.1259 / +0.0307**. k=40 (q=0.25 and 0.50)
   is where nearly all of disp's positive partial lives.
3. **It is NOT that cell alone.** Leave-one-stratum-out on the 27-point mean: evol > disp in
   **9/9** leave-outs, gap +0.1040..+0.2085 (full sample +0.1505). Dropping idea 284's own
   stratum *widens* the gap to +0.2085. So idea 293's ordering is not carried by any one stratum;
   idea 284 generalised one cell of nine.

## Stability, out of seed (the test with teeth)

540 **fresh** panels, seeds 100..159, same 9 strata, built and backtested from prices.

| char | partial A | partial B | sign agree | rank corr(A,B) | marginal A | marginal B | marginal sign agree |
|---|---|---|---|---|---|---|---|
| disp | +0.0046 | −0.0148 | **9/27** | −0.2503 | +0.2514 | +0.1131 | 21/27 |
| evol | +0.1551 | +0.1064 | **19/27** | −0.3004 | +0.2732 | +0.1490 | 22/27 |
| corr | −0.2180 | −0.0978 | 20/27 | −0.0440 | −0.2680 | −0.1211 | **26/27** |
| breadth | +0.0628 | −0.1332 | 5/27 | −0.2790 | +0.0132 | −0.1425 | 10/27 |

- Bootstrap (2,000 resamples inside each stratum): the partial's 95% CI **crosses zero in 53 of
  54 disp points and 44 of 54 evol points** across the two blocks.
- The per-point partial's cross-block rank correlation is **negative for both** (−0.25, −0.30):
  which stratum looks strongest does not replicate at all.
- The **marginal** rho is the object that does replicate in sign (21/27, 22/27) and is positive
  for both characteristics in both blocks — i.e. the two ideas never disagreed about the thing
  that is stable; they disagreed about a partial that neither block supports.

## Mechanism

Within-stratum rank corr(`disp_IS`, `evol_IS`) is **+0.55..+0.81, median +0.6909**; the other
three characteristics explain a median **0.59** of disp's rank variance and **0.49** of evol's.
The two partials are splitting one shared source of variance at n=60, which is exactly the
regime where a partial's sign is noise. `evol` wins the split more often (it is the less
explained of the two), which is all "evol > disp" ever meant.

## Pre-registered predictions, graded

| | prediction | result |
|---|---|---|
| P1 | \|mean partial\| < 0.20 for both chars in both blocks | **PASS** (+0.0046 / +0.1551 / −0.0148 / +0.1064) |
| P2 | partial sign disagrees across blocks in >= 9/27 for at least one char | **PASS** (disp 18/27, evol 8/27) |
| P3 | evol > disp ordering survives >= 8/9 leave-one-stratum-out | **PASS** (9/9) |
| P4 | median within-stratum rank corr(disp, evol) > 0.50 | **PASS** (+0.6909) |

## Rule 8 walk-forward (fresh block; IS 2009–2016 picks, OOS 2017– read once)

Each selector picks ONE panel per stratum on its IS characteristic; 27 (stratum x book) cells.

| selector | OOS Sharpe | regret vs anchor | beats anchor | beats SPY | beats RULES v2 | OOS CAGR | OOS MaxDD | PICK − REVERSE |
|---|---|---|---|---|---|---|---|---|
| S_DISP (highest IS disp) | +0.7585 | +0.0957 | 17/27 | 12/27 | 8/27 | 10.85% | −31.07% | +0.1568 |
| S_EVOL (highest IS evol) | +0.7198 | +0.0571 | 20/27 | 10/27 | 6/27 | 10.08% | −28.64% | +0.1332 |
| S_CORR (lowest IS corr) | +0.7303 | +0.0675 | 18/27 | 9/27 | **0/27** | 9.85% | −29.58% | +0.0792 |
| anchor (stratum mean) | +0.6628 (mean seed sd 0.1542) | — | — | — | — | — | — | — |
| SPY | **+0.8820** | — | — | — | — | **15.45%** | −33.72% | — |
| RULES v2 (live) | +0.8997 | — | — | — | — | 7.45% | −13.51% | — |

Every selector beats doing nothing by less than half a seed sd, and **none beats SPY out of
sample on average** (best is S_DISP at 12/27 cells). The sign checks are positive but small.

## Both KEEP paths (540 fresh panels x 3 books = 1,620 cells, all reported)

**4a 0/1620. 4b 46/1620. BOTH 0/1620.** The 4b footprint is the cap-mix gradient the record has
seen before, not a characteristic: **41 of 46 passers sit at q=0.25**, 5 at q=0.50, none at
q=0.75; 0 of the 46 also clear 4a. No selector's pick is among them by construction of the
selector — they are found by scanning every cell.

## Verdict

**KILL** of both "survivor" readings. On the queue's literal question, `evol` is the more stable
of the two (8 vs 18 cross-block sign flips, 19/27 vs 9/27 agreement, 44 vs 53 of 54 CIs crossing
zero), so if one had to be named it is evol — but the honest statement is that **neither partial
is an estimable object at n=60 given rank corr(disp,evol) ≈ +0.69**, and the characteristic
vocabulary's stable content is the **marginal** rho, which was never in dispute. No KEEP, no
memo. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script: `2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.py`
Outputs: `.gate.csv .blockA.csv .blockB.csv .panelsB.csv .stability.csv .walkforward.csv .keeppaths.csv .console.txt`

SURVIVORSHIP: SMALL439 and BSTK100 are current constituents of their screens; every constructed
panel inherits the bias whole and every return level is inflated. The bias is common within a
stratum and inflates between-panel spread, so it runs against a "nothing separates" verdict and
does not protect one — which is why the KILL is stated on sign stability and CIs, not on levels.

## Cross-lane note (added at merge)

A cloud-lane run answered idea 310 the same day, independently, by re-analysing idea 293's 540
committed panels with a seed split-half (direction fit on seeds 0–29, applied to 30–59). **The
two runs agree on the answer**: evol is the more stable of the two, disp is not, leave-one-
stratum-out never flips the ordering, and idea 284's cell is right for its stratum and
unrepresentative of the other eight. They differ on one number: on the split-half design both
selectors LOSE to the do-nothing anchor, while on this run's **fresh disjoint seed block** all
three BEAT it by +0.057..+0.096 — less than half the mean seed sd of 0.1542. The sign of the
anchor comparison is itself inside the noise, which is the same verdict either way. This run's
independent contribution is the 540-panel fresh block: the cross-block rank correlation of the
per-point partial is negative for both characteristics, which the single-artefact designs cannot
see.
