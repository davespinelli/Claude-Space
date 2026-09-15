# Idea 875 — does a deliberately mis-dispersed run-length null still land inside the noise floor?

**Cloud lane, 2026-09-15, idea 2 of 2. ANSWERED: YES UNDER IDEA 871's OWN STATISTIC — AND THAT IS
THE FINDING, BECAUSE THAT STATISTIC IS 95% SEED NOISE. The signed statistic, which 871's |·| form
cannot see, shows the maximally dispersed null IS systematically biased against BLOCK by −0.0046 of
Sharpe (sign-test z +3.8 over 1,152 arms), while the two comparable-dispersion nulls are not
(z +0.7). KILL for capital — nothing here is a book. A PROTOCOL amendment is PROPOSED, NOT APPLIED
(rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Script: `2026-09-15_does-a-MIS-DISPERSED-run-length-null-stay-inside-the-NOISE-FLOOR_cloud.py`
Outputs: `.arms.csv` (1,152) `.excess.csv` (5,760) `.gap.csv` `.walkforward.csv` `.books.csv`
`.console.txt`

## What was run

1,152 real gate arms (8 families × q{0.07,0.12,0.17} × w{252,1008} × depth{0.50,1.00} ×
cadence{D,W} × gross{0.75,1.00} × panels U56 / B136 / SMALL-664) × **5 nulls** × 10 md5 seeds ×
3 cost rungs. Two nulls are new here and hold the real arm's firing-day count *k* and run count *m*
**exactly** — so the switch count, and therefore the entire switch-cost term, is identical to BLOCK's
— while changing only the dispersion of the fire-run lengths:

* **SM-DOM** — one dominant run of *k−(m−1)* days, the other *m−1* runs of length 1. Measured
  fire-run sd ratio **5.87×** the real arm's.
* **SM-UNIF** — every run *k//m* or *k//m+1* days. Measured sd ratio **0.030×**.
* (871's SWITCHMATCH measures **0.936×** here, reproducing its published 0.919×.)

Two tuned parameters as the queue names them: dispersion target and cost rung. Declared axis
reduction vs 871: w drops {504, 2016}, depth drops {0.25} — stated before any number was read.

## Gates

G1 never-firing multiplier = ungated book **0.000e+00** · G6 fast Sharpe = `metrics()` **0.000e+00** ·
G2 rate match **0.000e+00** · G4 determinism **0.000e+00** · G5 *k* and *m* preserved by all three
switch-matched nulls in **0 of 34,560** real cells and 0 of 900 synthetic ones, with sd ratios
bracketing as designed (0.030 < 0.936 < 5.87). All PASS.

**G3 reproduction of 871 — the level DIFFERS, the ratio reproduces, and the difference is the point.**
On this declared axis subset the pooled median |SWITCHMATCH − BLOCK| is **0.0215** (871: 0.0144–0.0146)
and the seed-noise floor |RAND − BLOCK| at 0 bps is **0.0213** (871: 0.0145). **Both moved by the same
factor**, so the scale-free form of 871's claim — |SWITCHMATCH − BLOCK| ÷ floor = **1.010** against
871's 1.007 — reproduces exactly. A statistic whose level tracks its own noise floor 1:1 across a
change of grid is a statistic that is measuring the noise floor.

## 1. The literal question: H_SUFF CONFIRMED, H_SUFF2 REFUTED — and the ordering is backwards

Pooled median |null − BLOCK|, against a floor of **0.0213**:

| null | dispersion | 0 bps | 10 bps | 25 bps | vs floor |
|---|---|---|---|---|---|
| SWITCHMATCH | 0.94× | 0.0218 | 0.0215 | 0.0221 | outside at all three |
| SM-UNIF | 0.03× | 0.0232 | 0.0229 | 0.0227 | outside at all three |
| **SM-DOM** | **5.87×** | **0.0205** | **0.0209** | **0.0208** | **inside at all three (0.98×)** |
| RAND | 0.03× (unmatched switches, 13.23×) | 0.0213 | 0.2720 | 0.6830 | outside at 10/25 bps |

So the queue's question answers **YES**: the deliberately mis-dispersed null lands inside the floor.
But the most-dispersed null has the *smallest* gap and the near-uniform one the *largest*, i.e. the
statistic is **not monotone in the thing being manipulated** across a 195-fold dispersion range. That
is the signature of noise, not of sufficiency.

## 2. Noise accounting — the |·| statistic is measuring the seed budget

Under pure independent seed noise the per-arm median gap should be
`0.6745 × 1.2533 / √NSEED × √(sd_null² + sd_BLOCK²)`:

| null | observed | predicted by noise alone | obs/pred | seeds to resolve 0.010 | to resolve 0.005 |
|---|---|---|---|---|---|
| SWITCHMATCH | 0.0215 | 0.0247 | **0.87** | 61 | 244 |
| SM-UNIF | 0.0229 | 0.0246 | **0.93** | 61 | 242 |
| SM-DOM | 0.0209 | 0.0221 | **0.95** | 49 | 195 |
| RAND (10 bps) | 0.2720 | 0.0239 | **11.37** | — | — |

**Every matched null's gap is 87–95% of what seed noise alone predicts; RAND's is 11×.** At 10 seeds
the record cannot resolve a true difference below ≈0.02 of Sharpe at all, which is *larger than* 871's
own 0.02 pre-registered bar. This is open idea 877's question, answered in passing for these three
nulls: the budget needed is **≈50 seeds for 0.010 and ≈200 for 0.005**, against the 10 in use.

## 3. The signed statistic — dispersion does bite, one-sidedly

|·| is a per-arm quantity, so seed noise survives pooling. The **signed** gap pooled over 1,152 arms
does not (SE ≈ 0.0006):

| null | signed @0 | @10 | @25 | share of arms below BLOCK | sign-test z |
|---|---|---|---|---|---|
| SWITCHMATCH | −0.0008 | −0.0008 | −0.0009 | 51.0% | +0.7 |
| SM-UNIF | −0.0003 | −0.0006 | −0.0005 | 51.0% | +0.7 |
| **SM-DOM** | **−0.0044** | **−0.0046** | **−0.0042** | **55.6%** | **+3.8** |
| RAND | −0.0040 | +0.2720 | +0.6830 | 0.0% | −33.9 |

**SM-DOM is systematically different from BLOCK and the other two are not.** The effect is
cost-invariant (range 0.0004 across 0/10/25 bps, H_COSTINV CONFIRMED), so unlike RAND's it is a
return-path effect and not a turnover surcharge: a single giant de-grossed run is a long cash holiday
that lowers the placebo's vol, raising its Sharpe and *shrinking* the measured excess.

**The asymmetry is the usable result.** Dispersion far *below* the real arm's (SM-UNIF at 0.03×)
costs nothing measurable; dispersion far *above* it (SM-DOM at 5.87×) biases the excess by −0.005 of
Sharpe. A clause naming the switch count alone admits the biased case.

## 4. Two hypotheses that came back NO, printed as they came

**H_VAR REFUTED, and inverted:** SM-DOM's across-seed sd is **0.73×** BLOCK's (0.0465 vs 0.0642), not
≥2×. The pre-registered guess — that a giant run either hits the crash or misses it, so extreme
dispersion buys variance — is wrong: a run covering a large fraction of the sample self-averages,
while BLOCK's circular shift moves a structured path around and is the *more* seed-variable null.

**H_WF REFUTED:** Spearman(IS gap, OOS gap) ≥ +0.30 in **0 of 8 families** for every matched null
(all rhos between −0.17 and +0.11). Consistent with §2 — a noise quantity has nothing to walk
forward. The *level* does persist in sign for the one null with a real effect: SM-DOM's signed gap is
**−0.0096 in sample and −0.0163 out of sample**, against SWITCHMATCH's +0.0016 / +0.0027 and
SM-UNIF's +0.0002 / −0.0019.

## 5. Rule 8 on the books, and both KEEP paths (10 bps, next-day, weekly)

Declared IS-only selector: highest 2009–2016 Sharpe over every arm of the panel; OOS read once.

| panel | IS pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% | 1.034 | −22.93% | 1.160/0.915 | 12.41% | 1.016 | −22.93% | ✗ | ✗ (DD) |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% | 1.166 | −16.63% | 1.289/1.037 | 12.97% | 1.154 | −16.63% | ✗ | **✓** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% | 0.404 | −48.52% | 0.736/0.201 | 2.00% | 0.203 | −48.52% | ✗ | ✗ |
| — | RULES v2 live (U56) | 8.64% | 1.208 | −11.90% | — | 9.49% | 1.286 | −11.90% | — | — |
| — | SPY (U56 window) | 15.13% | 0.885 | −33.72% | 0.959/0.824 | 15.27% | 0.874 | −33.72% | — | — |

Unselected base rates over all 1,152 arms: **4a 0 (0.0%)**, 4b 105 (U56 61/384 = 15.9%,
B136 44/384 = 11.5%, SMALL **0**/384). The B136 pass is a by-product of a methodology run, is not
proposed, and sits inside a family (CORR) that idea 815 already flagged as the one whose placebo
excess walks forward while buying no capital (idea 870, still open). **Nothing here is promoted.**

## Verdict

**ANSWERED: YES, it stays inside the floor — because at 10 seeds the floor is wider than the effect.**
871's sufficiency finding is not wrong, but it is weaker than it reads: the statistic it used is
87–95% seed noise, its level tracks its own floor 1:1 across a change of grid, and it is not monotone
in dispersion across a 195× range. Under the signed statistic the switch count is **not** sufficient:
a null with 5.87× the real arm's run-length dispersion is biased by −0.0046 of Sharpe at z +3.8,
cost-invariantly, and the bias is one-sided — under-dispersed nulls are harmless.

**PROPOSED PROTOCOL amendment (rule 6: proposed, NOT applied; PROTOCOL.md untouched).** Amend idea
871's proposed clause to: *a placebo or permutation control must match the real arm's firing RATE and
its SWITCH COUNT, and its longest run must not exceed the real arm's longest run (equivalently, its
run-length dispersion must not exceed the real arm's); a null may be less dispersed than the real arm
but never more. Every placebo-differenced number must name the null that produced it AND its seed
budget, and no placebo difference smaller than 0.02 of Sharpe may be published at 10 seeds — that is
this record's measured resolution limit; ≈50 seeds are needed for 0.010 and ≈200 for 0.005.*

**Honest limits.** (1) The −0.0046 bias is small: 2.6% of RAND's cost artefact and well under a
typical published excess, so this refines 871's clause rather than overturning its practical
conclusion. (2) The seed-budget numbers are computed from the measured per-arm seed sd under a
normal-noise model, not simulated at 200 seeds. (3) SMALL is a current-constituent sub-$2B panel
(664 of 716 columns kept after dropping every ticker with `max_1d_move` ≥ 1.0 in
`data/small_meta.csv`); dead small caps are absent, so its levels are the most optimistic in the run —
its 0 of 384 4b rate is an upper bound that still reads zero. The headline quantity is a *difference
between two nulls on the same arm* and is far less exposed to survivorship than any level.
