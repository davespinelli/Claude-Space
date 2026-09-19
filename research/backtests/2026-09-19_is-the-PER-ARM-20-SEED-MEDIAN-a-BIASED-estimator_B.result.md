# Idea 903 (lane B, 2026-09-19) — is the PER-ARM 20-SEED MEDIAN a BIASED estimator of every null-minus-BLOCK headline?

**ANSWERED: YES, THE MEDIAN IS BIASED — 885's DIAGNOSIS IS CONFIRMED — AND NO, IT DOES NOT
EXPLAIN A SINGLE COMMITTED NUMBER. The bias is 0.0018 of Sharpe at S=20, which is 6.4% of the
0.0278 SD a single 20-seed read carries. CAPITAL ARM: KILL, NO NEW BOOK. SCHEMA FIX: use the
MEAN, which removes the bias AND cuts the read noise 20-24%, at zero cost.**

Script: `2026-09-19_is-the-PER-ARM-20-SEED-MEDIAN-a-BIASED-estimator_B.py` · GATES **10/10** ·
598 s · offline, committed caches only.

---

## What was built

7,200 null books + 18 real arms. The DECLARED ARM SUBSAMPLE 903 asks for is the record's own
N ladder at the frozen H: **N {5,10,15,20,25,30} x H=126**, min-hold on the RULES-v1 composite
rank key, eligibility `above 200d MA & vol20 < 0.60`, **gross 0.75, weekly, 10 bps, t+1**
(PROTOCOL rule 2), on **U56 / B136 / SMALL**. N=20 is the frozen anchor (idea 1323); G8 replays
it at **15.8028% / 1.1537 / -19.1276%** on U56, bit-consistent with idea 1350's committed head
anchor (15.80% / 1.1537 / -19.13%).

Two gross-matched nulls, both part of the OBJECT (903's headline form *is* a null-minus-BLOCK
contrast, so both sides must exist), neither a tuned dial:

* **RAND** — the record's standard: the arm's ordering replaced by a fresh uniform draw at
  every rebalance row. Same N, H, eligibility, gross, days, costs.
* **BLOCK** — a circular block bootstrap of the **real** key: rebalance row *i* gets the real
  rank key of a donor row, donors drawn in contiguous blocks of **LB = 13** rebalance rows
  (~63 trading days, the record's block length).

**S_MAX = 200** md5-deterministic seeds per (panel, arm, kind). All 7,200 per-seed null Sharpes
are **stored** (`.null_seeds.csv.gz`) — the thing 885 could not do, and the reason 903 exists.

**The two dials and no more (PROTOCOL rule 4):** `S {5,10,20,50,100,200}` x
`ESTIMATOR {median, mean, trimmed10}`. 18 cells per panel, **all published**.

---

## The gate this script failed first, and why it is in the record

Gate **G3** originally asserted that the MEAN arm's measured bias would be 0 to machine
precision — it is 0 *in expectation*, because the mean of a subsample mean is the population
mean. **G3 FAILED at 1.824e-03.** The mathematics was not wrong; the instrument was. `Ehat` is
itself a Monte-Carlo average over R subsets with SE = sd/sqrt(R), which at S=5, R=400 is ~3e-03
— the gate was measuring its own noise. Fixed by publishing the MC SE beside every bias,
raising R 400 -> 2000, and reading the three estimators on **common random numbers** so the
median's bias can be read net of the mean arm's residual (`bias_net`). The original failure and
its value are kept here rather than deleted. No dial, no book and no verdict changed.

---

## LEG 1 — the bias, measured directly

Bias(S, E) = mean over 2,000 random size-S subsets of E(subset), minus E(all 200 seeds),
averaged over the 6 arms. Sharpe units.

**RAND null (the record's standard):**

| panel | estimator | S=5 | S=10 | **S=20** | S=50 | S=100 | 1-read SD @20 |
|---|---|---|---|---|---|---|---|
| U56 | median | +0.003495 | +0.003040 | **+0.002693** | +0.001797 | +0.001259 | 0.019836 |
| U56 | mean | -0.000322 | -0.000273 | **+0.000019** | +0.000110 | -0.000031 | 0.015808 |
| U56 | trimmed10 | -0.000251 | -0.000351 | **+0.000057** | +0.000100 | +0.000022 | 0.015990 |
| B136 | median | -0.003259 | -0.002815 | **-0.002938** | -0.001996 | -0.001685 | 0.022367 |
| B136 | mean | -0.000346 | +0.000197 | **-0.000184** | +0.000008 | -0.000138 | 0.016974 |
| B136 | trimmed10 | -0.000462 | +0.000125 | **-0.000294** | -0.000034 | -0.000153 | 0.017668 |
| SMALL | median | -0.003978 | -0.003322 | **-0.003307** | -0.002018 | -0.001985 | 0.029062 |
| SMALL | mean | -0.000051 | +0.000277 | **-0.000267** | +0.000176 | +0.000114 | 0.022840 |
| SMALL | trimmed10 | -0.001345 | -0.000020 | **-0.000427** | +0.000126 | +0.000065 | 0.023613 |

**BLOCK null** (median): U56 +0.000748 / B136 +0.000590 / SMALL -0.000398 at S=20 — **3.6x to
8.3x smaller than RAND's**. Full table in `.bias_agg.csv`.

### 1. THE DECLARED TEST — 885's diagnosis is RIGHT

Declared before the numbers were read: *the sample mean is unbiased at every S by construction,
so if the drift disappears under the MEAN, the drift IS the median's small-sample bias.* It
disappears. Scored per (panel, kind) row against that row's own MC floor (3 x mean per-arm
MC SE / sqrt(6 arms)):

* **median: 4 of 6 rows RESOLVED** (all three RAND rows, plus U56 BLOCK) — G3b.
* **mean: 0 of 6 rows resolved** — G3c. Every read is inside its own noise, as the mathematics
  requires.
* mean |bias| at S=20: **median 0.001779 · trimmed10 0.000315 · mean 0.000168** (MC floor
  0.000622). Net of the mean arm's MC residual under common random numbers, the median's is
  **0.001648**.

### 2. BUT 885's TWO SUPPORTING CLAIMS BOTH FAIL

* **"9 of 9 shift the same way" does not generalise.** Over this run's 36 (panel, kind, arm)
  cells the median's S=20 bias is **15 positive / 21 negative**. The sign is consistent *within*
  a panel on RAND (U56 **+**, B136 **-**, SMALL **-**) and differs *across* them. 885's
  unanimity is a property of its single corpus, not of the median.
* **The cancellation claim is right only in the trivial direction.** 885 reasoned that the bias
  cancels between same-construction nulls, citing BLOCK2 (BLOCK vs BLOCK) not moving. True, but
  the form the record actually publishes is **null-minus-BLOCK**, and there it does **not**
  cancel: the contrast's median bias at S=20 is **+0.002049 (U56) / -0.002728 (B136) /
  -0.002471 (SMALL)**, i.e. **76%-102% of the RAND arm's own bias survives**, because BLOCK's
  median bias is several-fold smaller. A cross-construction contrast inherits the biased side
  nearly in full.

### 3. THE NUMBER THAT DECIDES IT — the bias is real and irrelevant

The per-arm SD of **one** 20-seed median read is **0.027829** of Sharpe. The bias is
**0.001779**. **bias / noise = 0.0639** — the systematic error is **6.4%** of the random error
on the very number it biases, i.e. **15.7x smaller**. Measured per-arm null-Sharpe dispersion
sigma = 0.0707 (U56) / 0.0759 (B136) / 0.1021 (SMALL), between 885's assumed 0.067 and idea
904's 0.1307 (904's grid included H=21, which disperses more).

### 4. THE FIX IS FREE, AND THE MEDIAN BUYS NOTHING

Switching estimator median -> mean removes the bias **and** cuts the per-arm read SD by
**-20.3% (U56) / -24.1% (B136) / -21.4% (SMALL)**. The mean **dominates the median on both
axes at zero cost**: the null-Sharpe distribution is near-symmetric, so the median's robustness
buys nothing while it pays the usual efficiency penalty. trimmed10 sits between (bias
0.000315, SD -19% to -21%). **The record's habit of reporting a per-arm median is a strictly
worse estimator than the arithmetic mean, in both bias and variance, on every panel tested.**

---

## LEG 2 — the capital arm: KILL

At every (S, E) cell, on every panel: among the 6 arms pick argmax of
`Sharpe_IS(a) - E_{s<=S}[Sharpe_null(a,s)]`, computed on **IS rows only** (warm-up..2016-12-31);
2017-2026 is untouched by construction (G4). **108 chooser cells (54 RAND + 54 BLOCK), every one
published** in `.grid.csv`.

**KEEP paths: 4a 0 of 108. 4b full 0 of 108. 4b full AND OOS 0 of 108.** Binding legs:
**L_DD fails at 108 of 108**, L_H2 at 72, L_H1 and L_CAGR at 36 each.

**THE DIAL IS ALL BUT INERT.** Distinct picks over the 18 RAND cells per panel: **U56 1,
B136 1, SMALL 2**. On U56 and B136 every one of S in {5..200} x E in {median, mean, trimmed10}
picks **N=5** — neither the seed budget nor the estimator moves the book on two of three panels.
(BLOCK-keyed: U56 2, B136 1, SMALL 2.)

**AND THE BOOK IT PICKS IS THE WORST ONE.** U56 N=5 is OOS Sharpe **0.9118** against the frozen
anchor's **1.1857** and N=15's **1.1971**. This independently reproduces idea 904's mechanism —
*placebo-differencing is a concentration bias*: a random 5-name portfolio is a terrible null, so
subtracting it rewards exactly the arms that lose out of sample. 904 found it on a 24-book
(N,H) grid at 50 seeds; it is the same at H=126 with a 200-seed budget.

**RULE 8 (strict) — (S, E) chosen on IS by argmax IS Sharpe of the selected book, 2017-2026 read
ONCE:**

| panel | IS pick | -> N | OOS CAGR / Sharpe / MaxDD | vs anchor | vs raw chooser | SPY OOS | LIVE v2 OOS |
|---|---|---|---|---|---|---|---|
| U56 | S=5, median | 5 | 17.32% / **0.9118** / -25.85% | 1.1857 (**-0.2738**) | 1.1971 (-0.2853) | 0.8738 | 1.2769 |
| B136 | S=5, median | 5 | 14.67% / **0.7513** / -28.12% | 1.0180 (**-0.2667**) | 0.7513 (+0.0000) | 0.8739 | 1.1019 |
| SMALL | S=20, median | 25 | 8.84% / **0.5236** / -36.87% | 0.4440 (**+0.0796**) | 0.5236 (+0.0000) | 0.8738 | 0.6473 |

**Mean d(OOS Sharpe) vs doing nothing: -0.1536, beats it 1 of 3. Vs the raw IS-Sharpe chooser:
-0.0951, beats it 0 of 3.** The IS pick is the ex-post best cell on all three panels only
because the dial barely moves — there is nothing to choose.

**H_HINDSIGHT fires again.** Six comparand books clear 4b full **and** OOS and **none of them is
reachable by any chooser in this run**: U56 ARM-N15 (17.14% / 1.1722 / -20.14% full; OOS 19.01%
/ **1.1971** / -20.14%), U56 ANCHOR-N20 (15.80% / 1.1537 / -19.13%; OOS 17.32% / 1.1857), B136
ARM-N15 (OOS 1.0405) and ARM-N10 (OOS 0.9212). Consistent with 1321 / 1323 / 1331 / 904: every
chooser the record builds loses to the cell nobody had to choose.

---

## LEG 3 — re-pricing the record's committed 20-seed placebo numbers (903's second clause)

Mechanical harvest over `research/backtests/*.md` + `CHANGELOG.md` (LEADERBOARD.md and QUEUE.md
excluded by declaration, idea 904's rule, so the two runs are comparable).

**FUNNEL: 1,262 files -> 410 placebo-cued sentences -> 24 carrying a >=4-dp decimal -> 18
DIFFERENCES (|x| < 0.1) -> 4 stamped with a seed count -> 1 stamped with S=20 exactly.**

* inside the measured S=20 median bias (0.000435): **3 of 18**
* inside the per-arm 1-read 20-seed SD (0.027829): **12 of 18**
* the single S=20-stamped number (0.0002, `2026-09-15_is-the-ONE-SIDED-DISPERSION-defect...B`)
  is inside both.

**THE RE-PRICING VERDICT: two-thirds of the record's committed placebo differences are inside
the noise of a single 20-seed read, and only one-sixth are inside the bias.** The record's
placebo numbers are not wrong because the median is biased. They are unresolved because twenty
seeds is not enough seeds. Same shape as 904's funnel finding, from the opposite direction.

---

## What this licenses, and what it does not

**RECOMMENDED SCHEMA CHANGE (free, and strictly dominant):** a committed placebo statistic
should aggregate seeds with the **arithmetic MEAN, not the median** — lower bias *and* 20-24%
lower variance on every panel tested — and should quote its **seed count** and its **per-arm
1-read SD** beside the number. Not enacted here: PROTOCOL rule 6 confines rules changes to the
Sunday review, and this run modifies no rule file.

**NOT licensed:** any claim that the record's placebo headlines are wrong *because of* the
median. They are not; they are unresolved for a different reason, and the fix for that is seeds,
not estimators.

**SURVIVORSHIP (rule 9).** U56, B136 and SMALL are current-constituent lists, so every absolute
level is an upper bound. The bias headline is a difference between estimators computed on the
SAME books and the SAME seeds, so it is first-order immune; the 0-of-108 pass count is not.

**RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.**

Artefacts: `.py` `.console.txt` `.gates.csv` `.bias.csv` `.bias_agg.csv` `.contrast.csv`
`.contrast_agg.csv` `.null_seeds.csv.gz` `.grid.csv` `.walkforward.csv` `.census.csv`
`.census_funnel.csv`
