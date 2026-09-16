# Idea 1098 (cloud lane, 2026-09-16) — is an ARGMAX over a 9-RUNG LADDER a PUBLISHABLE OBJECT AT ALL on this tape?

**ANSWERED = NO ON THE ONLY BAR THAT MATTERS, AND THE SPLIT BETWEEN THE TWO PANELS IS THE
FINDING.** The measured **90% sign-resolution floor is 3.25 pp of CAGR on U56 and 4.02 pp on
B136** (95%: 4.66 / 4.02). The published EDGE peak beats its runner-up by **0.61 pp** (U56) and
**1.49 pp** (B136) — **5.3x and 2.7x below the floor of the ladder it is read off**. On U56 the
argmax is not even reproducible: **P(bootstrap argmax == full-sample argmax) = 0.378**, and the
bootstrap's own MODE is **n=5**, not the published n=12. On B136 the point IS reproducible
(**0.728**) while the ladder around it is not — 18 of 36 rung pairs are not sign-resolved at 90%.
**KILL of "the EDGE argmax" as a publishable point on U56; CONFIRM that 1085/1082's four answers
(12 / 5 / 12 / 12 across seed counts) are ONE measurement seen four times; CONFIRM of 1082's whole
committed EDGE ladder at the rounding limit; and a resolution-floor clause proposed but NOT
enacted (rule 6).** No RULES change, no book promoted, no PROTOCOL edit; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

SELECTION: this lane takes the LAST open line for idea 2. QUEUE carries TWO lines numbered 1098
(idea 932's defect again); this is the argmax-resolution one.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**SEEDS S {5, 10, 20, 40}** (nested — the first S of the same 40 draws, so the seed dial moves the
precision of the null median and nothing else) **x LADDER SPACING {FULL9 = 1082's nine rungs,
ALT5 = {5,10,15,25,40}, COARSE3 = {5,15,40}}** — every spacing a SUBSET of FULL9, so all three
read the same paths and differ only in which rungs the argmax may land on. **12 cells per panel,
24 in total, ALL published.** Frozen at 1082/1086's construction: CAND20 legs, cap INF, max_vol
0.60, gross 0.75, W, min hold 126, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31. **BLOCK LENGTH
is not a dial** — headline L=63, L in {21,126} reported beside it and never selected on.

EDGE(n) = 100 x (CAGR_book(n) − median_seeds CAGR_null(n)) in pp under 1082's REBUILT convention
(each null re-run at the gross lam*0.75 that equalises its realised |MaxDD| with the book's, 34-step
bisection). The bootstrap draws circular blocks of trading days and applies **ONE index jointly**
to the book, all 40 nulls and every rung, because EDGE is a paired quantity over one tape. CAGR
under block resampling is exact from block sums of log1p. **LIMITATION DECLARED IN ADVANCE: lam is
matched once on the real tape and held fixed inside the bootstrap, so every width here is a LOWER
bound** — the conservative direction for a "not resolved" conclusion.

## THE ARGMAX'S OWN SAMPLING DISTRIBUTION (L=63, 1,000 draws)

| panel | spacing | S=5 | S=10 | S=20 | S=40 | 90% set at S=40 |
|---|---|---|---|---|---|---|
| U56 | FULL9 | 12 (P 0.546) | 5 (0.517) | 12 (0.286) | **12 (0.378)**, mode 5 (0.390) | {5,8,10,12} = 4 rungs |
| U56 | ALT5 | 5 (0.635) | 5 (0.625) | 10 (0.248) | 10 (0.300), mode 5 (0.497) | {5,10,15} = 3 |
| U56 | COARSE3 | 5 (0.731) | 5 (0.705) | 5 (0.619) | 5 (0.638) | {5,15} = 2 |
| B136 | FULL9 | 10 (0.738) | 10 (0.798) | 10 (0.764) | **10 (0.728)** | {5,8,10,12,15} = 5 |
| B136 | ALT5 | 10 (0.767) | 10 (0.804) | 10 (0.768) | 10 (0.731) | {5,10,15} = 3 |
| B136 | COARSE3 | 15 (0.561) | 15 (0.643) | 15 (0.669) | 15 (0.598) | {5,15} = 2 |

U56 FULL9 mass at S=40: **5: 0.390, 8: 0.055, 10: 0.095, 12: 0.378, 15: 0.014, 20: 0.068, and
exactly 0.000 on 25 / 30 / 40.** B136: **10: 0.728, 5: 0.146, 15: 0.116**, everything else ≤0.004.
Block length barely moves any of it (U56 P = 0.410 / 0.378 / 0.393 and B136 0.738 / 0.728 / 0.769
at L = 21 / 63 / 126), so the width is not an artefact of the resampling scale.

**H_STABLE FAILS on U56 (0.378 against the declared 0.50) and PASSES on B136 (0.728).** **H_WIDTH
PASSES on both** (4 and 5 rungs). The far side of the ladder is the one thing that IS resolved:
n = 25/30/40 carry zero argmax mass on U56, which is 1082's "EDGE collapses above ~n=15" — the
part 1085 also kept — and not its peak.

## THE RESOLUTION FLOOR (measured, not assumed)

Over all 36 rung pairs, the smallest |dEDGE| above which the bootstrap agrees with the full-sample
sign at least 90% of the time:

| panel | floor @90% | floor @95% | peak − runner-up | verdict | pairs unresolved @90% | largest unresolved gap |
|---|---|---|---|---|---|---|
| U56 | **3.25 pp** | 4.66 pp | +0.61 pp (12 vs 10) | **BELOW** | 15 of 36 | 3.00 pp |
| B136 | **4.02 pp** | 4.02 pp | +1.49 pp (10 vs 15) | **BELOW** | 18 of 36 | 3.86 pp |

**H_FLOOR PASSES on both panels.** The record has been publishing argmaxes off a ladder that
cannot sign-resolve gaps of 3-4 pp of CAGR, from peaks that lead by 0.6-1.5 pp. Note what this
does NOT say: 1082's collapse is much larger than the floor (EDGE(peak) − EDGE(40) is 6.41 pp on
U56 and 6.47 pp on B136) and stays resolved. The floor kills the **peak's location**, not the
**shape's far side**.

## THE PROPOSED CLAUSE (proposed, NOT enacted — PROTOCOL rule 6 reserves this for Sunday review)

> Any published argmax over a ladder must state (i) the gap between the winning rung and the
> runner-up in the units of the quantity being maximised, and (ii) the ladder's own resolution
> floor at 90%, measured by block bootstrap on the same paths. Where the gap is below the floor,
> the result is reported as a TIE SET — the rungs carrying 90% of the bootstrap argmax mass — and
> never as a single rung.

Applied to the record as it stands, that clause re-expresses 1082's "EDGE peaks at n=12 / n=10"
as **U56 tie set {5, 8, 10, 12}** and **B136 tie set {5, 8, 10, 12, 15}**, and leaves 1082's
far-side collapse verdict untouched.

## TWO SUPPORTING FACTS, BOTH OF WHICH CUT AGAINST BUYING A FIX

**H_SEED PASSES on both panels: the width is a TAPE fact, not a seed-count fact.** The 90% set is
4 rungs at S=5 and 4 at S=40 on U56, 5 and 5 on B136. Buying seeds does sharpen the null median —
the per-rung EDGE SE falls by 2.1x to 3.5x from S=5 to S=40 (U56 n=12: 1.597 -> 0.332 pp; n=20:
0.714 -> 0.284) — and it does not narrow the argmax at all, because what the argmax is uncertain
about is the TAPE, not the draws. On 17.6 years there is nothing to buy.

**The SPACING dial changes the ANSWER while raising apparent confidence, which is the warning that
generalises.** **H_SPACE PASSES on U56** — COARSE3 reports n=5 with P = 0.638 against FULL9's
0.378, i.e. a coarser ladder gives a DIFFERENT argmax with 1.7x the apparent stability — and
**FAILS on B136** (0.598 vs 0.728), where the mechanism is even blunter: **the published peak
n=10 is not a rung of COARSE3 at all, and the coarse ladder confidently reports 15 instead.** Any
argmax in the record read off a 3- or 4-rung ladder is suspect for this reason alone.

**H_1085 PASSES.** 1085/1082 reported the U56 argmax as 12 / 5 / 12 / 12 at S = 5 / 10 / 20 / 40;
this run's bootstrap puts **0.546 / 0.517 / 0.286 / 0.378** of the argmax mass on exactly the rung
each of them named. The four answers are one measurement seen four times, and 1085's framing of
"four ways of asking give three answers" is better read as one unresolved answer.

## GATES 8 of 8, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17. G1b `gross_rescaler(1.0)` == `nrun` 1.39e-17 (the
bisection kernel is the same book, not an approximation). G2 CROSS-RUN 936/1071/1082's committed
U56 W/H126 N=20 triple 3.18e-07. G3 SPY OOS triple 1.70e-04. G5 live RULES v2 MaxDD == committed
−12.05% at 4.95e-05. G7 determinism of 1082's seed recipe 0.00e+00. **G_XRUN: all 18 of 1082's
committed EDGE figures reproduce, max |d| 4.80e-03 pp (U56) and 4.53e-03 (B136) — inside the
0.005 pp that 1082's own two-decimal rounding allows**, so the two runs are pricing the same
object and the bootstrap is layered on 1082's numbers rather than on a re-derivation of them.

## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS

n chosen on IS 2009-2016 ALONE inside each spacing, at each seed count, by four choosers
(C_ISSHARPE, C_ISDD, C_ISCAGR and C_ISEDGE — the last on the IS-window EDGE, IS-matched nulls),
OOS 2017-2026 read ONCE. **0 of 48 picks clear 4b on U56 and 0 of 48 on B136; 4a 0 of 96.**
C_ISSHARPE picks n=40 (U56) and n=5/8 (B136); C_ISDD n=40 and n=30/40; C_ISCAGR and C_ISEDGE pick
**n=5 on both panels** — reproducing 1082's finding that its own EDGE selector is the worst pick
available. Whole ladder: **4b full 2 of 9 on U56 (n=12: 17.71% / 1.1692 / −20.17%, halves
1.275/1.088, OOS 18.89% / 1.1758; n=20: 15.58% / 1.1397 / −19.13%, OOS 16.97% / 1.1643) and 1 of 9
on B136 (n=15: 16.78% / 1.0682 / −19.66%, OOS 17.49% / 1.0458)** — 1082's committed 3 of 18,
reproduced exactly — **and 4a 0 of 18.** Benchmarks: U56 SPY full 15.10% / 0.8829 / −33.72%
(halves 0.9588/0.8207), OOS 15.21% / 0.8711 / −33.72%; RULES v2 live full 8.62% / 1.2007 /
−12.05%, OOS 9.45% / 1.2762 / −12.05%. B136 SPY OOS 15.33% / 0.8767 / −33.72%; RULES v2 OOS 7.88%
/ 1.1059 / −12.24%.

**NOTHING IS PROPOSED AS CAPITAL AND NO MEMO IS WRITTEN.** The two 4b-passing U56 rungs are
1082's already-PARKed cells and no honest IS-only chooser reaches either; EDGE was never a KEEP
path and this run does not turn it into one.

## SURVIVORSHIP (rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels. Book and null are drawn from the same pool over the
same tape, so the bias very largely cancels out of EDGE and out of the argmax's width; it does NOT
cancel out of the 4b legs, measured against SPY, a real index, so the three 4b passes above are
flattered by it.

Script `research/backtests/2026-09-16_is-an-ARGMAX-over-a-9-RUNG-LADDER-a-PUBLISHABLE-OBJECT-AT-ALL-on-this-tape_cloud.py`,
9 CSVs, console log, 4 LEADERBOARD rows.
