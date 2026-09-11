# Idea 540 — is `disp` the SECOND vol channel?

**Run:** 2026-09-11 UTC, cloud. **Script:** `2026-09-11_is-disp-the-SECOND-vol-channel_cloud.py`

**Verdict: ANSWERED — but the answer KILLS THE STATISTIC THE QUESTION ASKS FOR.** "Which of the
published disp direction claims survive log(book vol) held?" has a nominal answer — **52 of 91**
under `logx`, **0 of 28** under the elasticity form — and that answer is **not distinguishable
from a zero-signal control**: a disp column permuted within stratum still produces **64.74 of 180
cells "significant"** per draw (median 65, p95 81) against the real 91, and its survival shares
are **76.9% (partial) / 70.5% (logx) / 0.0% (loglog)** against the real **61.5% / 57.1% / 0.0%**.
The real shares sit **at or below** the null band on every control. The only leg that separates
anything is the **book leg**, and it says disp-residualised-on-vol picks **worse than doing
nothing** in two of three arms. No RULES change, no book promoted, no KEEP, no memo; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 idea 533's 2,880-row residualisation grid re-derived from its own `.arms.csv` | max \|d\| **b 4.65e-16, t 1.91e-14, r2 9.99e-16** (bar 1e-9) **PASS** |
| G2 idea 533's 144-row log-log table re-derived the same way | max \|d\| **3.55e-14** **PASS** |
| G3 the 504 arm-rows' own KEEP counts | **4a 0/504, 4b 41/504** — exactly as published **PASS** |
| G3 disp's published collinearity median | **+0.4195** vs published **+0.42** **PASS** (the *range* is corrected below) |
| G4 zero-signal control — disp permuted within stratum, 200 draws, seed 540 | ran; it is the finding |

No new backtests were run: the 504 committed arm-rows of idea 295's MIX ladder (k=40, 21 q rungs ×
8 draws, EWall/top10/top20 at gross 0.75, weekly, 10 bps, t+1) are re-read under this run's own
fitters, and G1/G2 require the parent's entire published grid back out of them first.

## RECORD CORRECTION — the queue's own premise

The queue quotes disp's within-stratum collinearity with the book's own vol as **+0.32..+0.64,
median +0.42**. That band is the **EWall+top10 slice** (+0.3215..+0.6420). Over the **12 cells
idea 533 actually measured** it is **+0.0612..+0.6420**:

| arm | range | median |
|---|---|---|
| EWall | +0.3215..+0.5849 | +0.4071 |
| top10 | +0.6044..+0.6420 | +0.6262 |
| **top20** | **+0.0612..+0.3946** | **+0.2334** |

`top20` — the arm where a top-n book is least an exposure proxy for its own eligible set — reads
+0.0612 at strata = 3, an order of magnitude below the quoted floor. The published **median**
reproduces exactly.

## The re-pricing (91 claims among 180 published disp cells; 1,080 cells published in full)

| control | defined | survive | share | permuted null (median [p5, p95]) | reading |
|---|---|---|---|---|---|
| partial (linear, idea 533's) | 91 | 56 | 61.5% | 76.9% [65.6, 88.1] | **BELOW the band** |
| residx | 91 | 55 | 60.4% | — | — |
| ratio | 91 | 39 | 42.9% | — | — |
| **logx** (y ~ log disp + **log bookvol**) | 91 | **52** | **57.1%** | 70.5% [56.8, 82.3] | **INSIDE** (bottom edge) |
| **loglog** (log\|y\| ~ log disp + **log bookvol**) | **28** | **0** | **0.0%** | 0.0% [0.0, 1.9] | **INSIDE** |

`loglog` is defined only where the outcome is strictly one-signed inside the cell, which on this
corpus is exactly the two drawdown outcomes. Its 0/28 therefore **cannot** be read as "disp's
drawdown content is the vol channel": the permutation shows the elasticity form has essentially no
power here (a no-information disp survives it 0.0% of the time too). That is the run's first
correction to its own expected story.

**The bar itself is mis-calibrated on this corpus.** A within-stratum permutation destroys the
disp↔outcome link but leaves **35.97%** of the 180 cells reading \|t\| ≥ 1.96 — seven times the
nominal 5% — because the 168 panels are not independent draws (8 draws per q rung share names, and
within-stratum demeaning does not remove the cross-sectional dependence). The real claim count, 91,
is only **1.41×** the null's median of 65. Every "N of M claims survive" statement built on this
corpus, idea 533's and this run's alike, inherits that.

## Where the control still does something specific

Splitting the 91 claims by outcome family (the per-family null was **not** separately measured —
the pooled `logx` band [56.8, 82.3] is the only reference this run has, so read this as
directional):

| outcome family | claims | survive logx | share | sign REVERSALS under logx |
|---|---|---|---|---|
| drawdown (MaxDD, DDnorm) | 28 | 5 | **17.9%** — far below the pooled band | **14 of 28** |
| return (CAGR, Sharpe, CAGRnorm) | 63 | 47 | **74.6%** — inside the pooled band | 7 of 63 |

By arm on MaxDD alone: EWall **0 of 11** survive, top10 **0 of 4**, top20 **2 of 4** — the gradient
the corrected collinearity band predicts. On EWall the published MaxDD slope does not merely die,
it **reverses**: t goes **−4.65 → +1.94 (partial) / +2.05 (logx) / +6.00 (ratio)** at strata = 3.

**Resolution is load-bearing** (the queue's dial 2): of the claims made at strata = 3, **9 of 28**
survive logx; at strata = 21, **26 of 30**. The published direction is not even one sign — 51 of the
91 claims positive, 40 negative — because `none`'s own sign flips with resolution (EWall CAGR t
**−2.37 → +4.18** from strata 3 to 21, idea 284/295's flip).

## Rule 8 — claim leg (established on 2010–2016 only, read once on 2017–2026)

| control | IS claims | hold OOS | share |
|---|---|---|---|
| none | 24 | 15 | 62.5% |
| partial | 30 | 19 | 63.3% |
| residx | 27 | 16 | 59.3% |
| ratio | 38 | 20 | 52.6% |
| logx | 30 | 18 | 60.0% |
| loglog | 6 | **0** | **0.0%** |

Holding log(book vol) costs nothing in out-of-sample reliability (60.0% vs the uncontrolled 62.5%)
— which, read against the mis-calibrated bar above, mostly says both numbers are measuring the
same dependence structure rather than the same information.

## Rule 8 — book leg (IS-only selectors over the 168 panels, read once on OOS)

This leg does **not** depend on the t-bar, and it is where the run's evidence actually lives.
Comparands on the same calendar: RULES v2 OOS **+8.50% / 1.0734 / −12.53%**, SPY OOS
**+15.45% / 0.8820 / −33.72%**. Arm anchors (the do-nothing choice-set mean) OOS Sharpe
EWall 0.6572 / top10 0.6451 / top20 0.6860.

| arm | selector | pick | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|
| EWall | SEL-S argmax IS Sharpe | q=0.15 | 12.13% / **0.9844** / −19.33% |
| EWall | SEL-DISP+ | q=0.90 | 10.28% / 0.6788 / −33.29% |
| EWall | SEL-DISP− | q=0.00 | 11.29% / 0.9719 / −21.22% |
| EWall | **SEL-DISP\|v** | q=0.90 | 10.28% / **0.6788** / −33.29% |
| top10 | SEL-S | q=0.05 | 12.83% / 0.8262 / −28.77% |
| top10 | SEL-DISP+ | q=0.90 | 12.12% / 0.8092 / −23.82% |
| top10 | SEL-DISP− | q=0.00 | 9.04% / 0.6863 / −24.68% |
| top10 | **SEL-DISP\|v** | q=0.80 | 4.03% / **0.3494** / −23.36% |
| top20 | SEL-S | q=0.10 | 9.09% / 0.8714 / −15.82% |
| top20 | SEL-DISP+ | q=0.90 | 6.27% / 0.5970 / −17.99% |
| top20 | SEL-DISP− | q=0.00 | 11.38% / **1.0120** / −18.15% |
| top20 | **SEL-DISP\|v** | q=0.90 | 2.49% / **0.2852** / −20.32% |

Over the 12 picks: beat the anchor 9, **beat RULES v2 0**, beat SPY 3, **4a 0, 4b 2**. The queue's
own control used as a **selector** — take the panel with the highest IS disp once log(book vol) is
residualised out — is the **worst of the four in two of three arms** and **below its own do-nothing
anchor** in both (0.3494 and 0.2852 against 0.6451 and 0.6860). Whatever disp knows about a book,
removing the book's own vol leaves nothing that picks.

Corpus for reference: EWall 8.31% / 0.6984 / −28.96% (OOS 7.97% / 0.6572 / −28.59%), top10 8.67% /
0.6690 / −25.53% (OOS 8.61% / 0.6451 / −25.03%), top20 7.39% / 0.7172 / −19.29% (OOS 7.25% /
0.6860 / −19.10%); **4a 0/504, 4b 41/504**.

## Prose census

**141** sentences across **20** files (LEADERBOARD 50, QUEUE 36, CHANGELOG 21, plus 17 `.result.md`)
name disp with a direction word; only **20 (14.2%)** also name an arm or a stratum resolution, i.e.
are re-priceable at all. Idea 533's finding (5) — "any published characteristic direction claim
that does not name its book is not re-readable" — holds on 85.8% of the record's own disp prose.

## Survivorship & scope

Both ends of the q ladder are current constituents of their screens (idea 54), so every level
inherited here is optimistic. The object adjudicated is a within-stratum slope under a control and
a selector's OOS ranking — neither is a level claim, and no arm here is a capital candidate.
