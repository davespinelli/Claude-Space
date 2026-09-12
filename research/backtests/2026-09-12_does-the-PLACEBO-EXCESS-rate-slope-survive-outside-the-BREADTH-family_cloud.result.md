# Idea 606 — does the PLACEBO-EXCESS rate slope survive outside the BREADTH family?

**ANSWERED = YES AT THIS RUN'S BAR, NO AT THE PARENT'S — see the reconciliation section: a
concurrent lane-B run applied idea 602's own stricter bar and this run's own K-ladder fails it outside
breadth, so lane B's reading stands and the headline below is a weak-bar pass.**

**At this run's bar,** idea 602's one surviving positive result (QROLL's excess over its own rate- and
run-length-matched BLOCK placebo rising +0.026 → +0.102 across five firing-rate buckets) reproduces on
breadth AND on all three non-breadth market states (vol, dispersion, correlation), with
Spearman(bucket, excess) = +0.90 / +1.00 / +0.90 / +1.00 at K = 5 and positive at every one of the
five bucket counts. **But the decomposition shows it is not a gate-quality fact either: 21–59% of the
gap is the PLACEBO DECAYING, the RAND placebo's own slope is −1.000 on all four states, and the
statistic's in-sample gap is 2–15× smaller than its out-of-sample gap (and changes sign on DISP).
The excess-over-placebo statistic is partly a mechanical function of the firing rate under a null in
which the gate does nothing, so it cannot be read as evidence that a gate that fires more is a better
gate. KILL for capital: 4a is 0 of 1,728 arms.**

Script `2026-09-12_does-the-PLACEBO-EXCESS-rate-slope-survive-outside-the-BREADTH-family_cloud.py`
(493.9 s, deterministic via md5 seeds, no network). **Tuned: state (4) × bucket count K (5) = 20
points, all reported.** Reported-never-selected and inherited verbatim from idea 602: family, level,
window w, depth (0.25/0.50/1.00), cadence (D/W), gross (0.75/1.00), cost rung (0/10/25 real, 10
placebo), placebo kind (RAND/BLOCK), seed (10), panel (U56 headline, B136 reported), window. 1,728
real arms at 10 bps, 34,560 placebo runs.

## The four states (all causal, all oriented LOW = risk-off, so one gate form serves)
| state | definition |
|---|---|
| BREADTH | share of panel names above their own 200d MA — idea 602's, verbatim (the anchor) |
| VOL | −1 × SPY 20d realised vol, annualised |
| DISP | −1 × the 20d mean of the daily cross-sectional dispersion (std across names) of returns |
| CORR | −1 × the 60d σ-weighted mean pairwise correlation, in closed form from the equal-weight index variance and the constituent variances — exact, and O(TN) rather than O(TN²) |

**ABSZ is not idea 602's ABS.** Idea 602's ABS is a fixed level in breadth's own units (0.30/0.40/
0.50) and has no meaning on vol, dispersion or correlation; ABSZ is the cross-state-comparable
analogue (a fixed threshold in the state's own causally standardised units). Idea 602's literal ABS
is carried as **ABSLIT on breadth only**, purely so gate G3 can test reproduction.

## The statistic: median excess over the BLOCK placebo, by firing-rate bucket (K=5)

| state | QROLL b0 → b4 | ρ(bucket, excess) | top−bottom |
|---|---|---|---|
| **BREADTH** | +0.0478 +0.0851 +0.0828 +0.0866 **+0.1221** | **+0.900** | +0.0743 |
| **VOL** | +0.0214 +0.0428 +0.0617 +0.0747 **+0.1049** | **+1.000** | +0.0835 |
| **DISP** | +0.0136 +0.0289 +0.0268 +0.0359 **+0.0653** | **+0.900** | +0.0517 |
| **CORR** | +0.0261 +0.0302 +0.0344 +0.0376 **+0.0680** | **+1.000** | +0.0419 |

Robustness across the second tuned dial (all reported, nothing selected on it) — ρ at K = 3/4/5/6/8:
BREADTH +1.000/+1.000/+0.900/+0.943/+0.857 · VOL +1.000/+1.000/+1.000/+0.943/+0.976 ·
DISP +1.000/+1.000/+0.900/+0.886/+0.786 · CORR +1.000/+1.000/+1.000/+0.886/+0.738. **Positive at all
20 tuned points.**

## The decomposition — excess = REAL − BLOCK, and both legs move

| state | ρ(bk, REAL) | REAL top−bot | ρ(bk, BLOCK) | BLOCK top−bot | ρ(bk, RAND) | share of the gap from the placebo leg |
|---|---|---|---|---|---|---|
| BREADTH | +0.900 | +0.0283 | **−1.000** | −0.0389 | **−1.000** | **52.3%** |
| VOL | +1.000 | +0.0545 | −0.700 | −0.0175 | **−1.000** | 21.0% |
| DISP | +0.500 | +0.0243 | −0.600 | −0.0182 | **−1.000** | 35.2% |
| CORR | +0.300 | +0.0096 | −0.900 | −0.0249 | **−1.000** | 59.4% |

This is the finding the parent could not see with one state. The real gate's own advantage over its
matched-gross twin **does** rise with the firing rate (ρ +0.90/+1.00/+0.50/+0.30), so the effect is
not purely artefactual. But the placebo leg falls monotonically on every state — and the RAND
placebo, which destroys run-length structure as well as timing, falls at **ρ = −1.000 on all four** —
so between a fifth and three-fifths of the published gap is the null arm decaying, not the real arm
improving. A shuffled gate that de-grosses on more days pays more switch cost and mistimes more of
those days; the excess therefore widens with the rate *even when the gate has no skill*. Any future
"excess over a rate-matched placebo" claim needs its placebo leg published beside it.

## The seven pre-registered hypotheses

| test | bar | measured | verdict |
|---|---|---|---|
| **H_REPRO / G3** breadth reproduces idea 602 | QROLL top−bottom ≥ +0.05, ρ > 0 | **+0.0743**, ρ **+0.900**; ABSLIT +0.0091→+0.0718, QEXP +0.0000→+0.0526 | **PASS** |
| **H_SLOPE** *(the deciding test)* QROLL's slope survives on every non-breadth state | ρ > 0 on all 3 | **+1.000 / +0.900 / +1.000** | **PASS — the slope is not a breadth fact** |
| **H_FLAT** the parent's ABS-is-flat contrast reproduces | \|ρ(ABSZ)\| < 0.5 on all 4 | +0.400 / +0.500 / **+0.800** / −0.100 — fails on DISP | **FAIL** |
| **H_SIGN** top bucket's median excess > 0 | all 4 | +0.1221 / +0.1049 / +0.0653 / +0.0680 | **PASS** |
| **H_ZERO** the slope lives in the real arm, not the placebo | \|ρ(BLOCK)\| < 0.5 on all 4 | **−1.000 / −0.700 / −0.600 / −0.900** — fails on all four | **FAIL, decisively** |
| **H_WF** rule 8 — IS and OOS top−bottom gap agree in sign | all 4 | BREADTH +0.042/+0.126, VOL +0.042/+0.151, **DISP −0.007/+0.109**, CORR +0.007/+0.092 | **FAIL (DISP)** |
| **H_KEEP** no arm earns 4a | 0 | **0 of 1,728** | **PASS** |

**4 of 7 pass.** Note the size asymmetry H_WF exposes even where it passes: the OOS gap is 3.0× the
IS gap on breadth, 3.6× on vol and 12.7× on correlation. The statistic is far larger in the window
containing 2020 and 2022 than in the one that does not — it is an episode-weighted quantity, and the
parent's single full-sample number hides that.

## Gates
G1 a never-firing multiplier ≡ `engine.backtest` **0.000e+00** (bar 1e-12) · G2a every placebo's
de-grossed-day share ≡ the real arm's **0.000e+00** and G2b BLOCK's mean multiplier ≡ the real arm's
**0.000e+00** (bar 1e-12 — so placebo and real share the same matched-gross twin exactly) · G3 as
H_REPRO above · G4 determinism, 18 placebos recomputed from the same md5 seeds **0.000e+00**.

## Rule 8 book leg, and capital
Per (panel, state) the arm is chosen on IS Sharpe alone and the OOS window is read once (U56 shown;
B136 in `.walkforward.csv`):

| state | rule-8 pick | FULL CAGR/Sharpe/MaxDD | OOS CAGR/Sharpe/MaxDD | 4a | 4b |
|---|---|---|---|---|---|
| BREADTH | QROLL q0.17 w504 d1.0 D g1.00 | 12.69% / 1.154 / −17.86% | 13.46% / 1.232 / −17.86% | ✗ | ✓ |
| VOL | ABSZ 0.0 d1.0 W g1.00 | 10.61% / 1.010 / −15.00% | 9.13% / 0.968 / −15.00% | ✗ | ✗ |
| DISP | QROLL q0.12 w504 d1.0 W g1.00 | 13.45% / 1.117 / −19.01% | 14.18% / 1.169 / −19.01% | ✗ | ✓ |
| CORR | ABSZ −1.0 d1.0 D g1.00 | 12.58% / 1.069 / −17.59% | 12.93% / 1.138 / −17.59% | ✗ | ✓ |

Comparands, OOS: **RULES v2 (live) 9.47% / 1.278 / −12.05%**; **SPY 15.33% / 0.877 / −33.72%**.
Full sample: RULES v2 8.63% / 1.202 / −12.05%, SPY 15.16% / 0.886 / −33.72%.

**KEEP paths over all 1,728 arms at 10 bps: 4a 0, 4b 480, BOTH 0.** Of the 480 4b passes, 256 have a
matched-gross *static* twin that fails 4b — those are the only ones where 4b sees the gate rather
than the exposure, and none of them clears 4a. Every rule-8 pick is beaten on OOS Sharpe by the live
book it would replace. **KILL for capital. No RULES change, no book promoted, no PROTOCOL edit
(rule 6).** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## What this says about the record (proposal only — rule 6, Sunday review)
Idea 602's excess-over-placebo slope should be quoted with **three** numbers, not one: the excess, the
**placebo leg's own slope**, and the IS/OOS split. On this corpus the placebo leg alone moves
−0.018 to −0.039 across the rate range and the RAND placebo is monotone at ρ = −1.000 on every state,
so a "the gate beats its shuffle by more when it fires more" claim is partly a statement about what
shuffling costs, not about what the gate knows.

## Reconciliation with lane B's concurrent run of the same idea (added after the fact)

Lane B ran idea 606 the same day (`..._B.py`, 3 panels, 8 families = 4 states × both directions,
10,368 gated cells) and published the opposite headline: *the LEVEL generalises to every risk-off
state, the SLOPE is mostly a breadth fact.* **Lane B is right and this run's H_SLOPE PASS is a
weak-bar pass.** The two runs do not disagree about the data; they disagree about the bar:

* this run pre-registered **ρ > 0 at K = 5** and got +0.900 / +1.000 / +0.900 / +1.000;
* lane B used **idea 602's own bar — monotone AND ρ ≥ +0.80 at every K × unit** — under which no
  non-breadth family passes all ten readings;
* and **this run's own K-ladder fails that bar outside breadth**: DISP +0.786 and CORR +0.738 at
  K = 8 (see the ladder above). The parent's bar was the right one to pre-register and this run did
  not.

What the two independent runs **agree** on, which is the durable part: rule 8 on the claim fails (the
IS and OOS gaps differ by 3–13× here, with a sign flip on DISP; lane B finds the IS curve flat against
a steep OOS one), the phenomenon lives in the post-2016 window, and no book earns 4a. What this run
adds that lane B does not carry: **the REAL − BLOCK decomposition** above — the placebo leg's own
slope, which turns out to be 21–59% of the published gap.

## Caveats
- **SURVIVORSHIP.** U56 and B136 are current-constituent lists; every level is optimistic. The
  headline is a within-panel real-vs-shuffled-self difference on the same book, which the bias moves
  far less than it moves levels; the walk-forward levels carry it in full.
- **Two panels, not three.** The small panel is not run here (runtime); nothing above speaks to it.
- The medians pool U56 and B136, as idea 602 pooled its panels; per-panel cells are in `.excess.csv`.
- ABSZ is a *new* family, not idea 602's ABS (see above); every ABS claim here is an ABSZ claim, and
  the H_FLAT failure on DISP is a failure of ABSZ, not a refutation of the parent's ABS reading.
- A bug caught and fixed before any verdict was read: the bucket assignment was index-aligned rather
  than positional, which silently NaN'd most groups. The numbers above are from the fixed run; the
  first run's partial table is not published.
