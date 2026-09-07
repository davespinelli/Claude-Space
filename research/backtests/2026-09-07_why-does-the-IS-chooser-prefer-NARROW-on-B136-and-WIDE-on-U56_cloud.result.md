# Idea 385 — why does the IS chooser prefer NARROW on B136 and WIDE on U56? (cloud, 2026-09-07)

**ANSWERED, and both halves of the queue's framing are FALSIFIED. The B136-narrow / U56-wide
ordering is not a panel fact — on 13 rolling 5-year blocks B136 picks *wider* than U56 on 11 —
and the 2009-2013 momentum run is not the cause; that block pushes both panels toward WIDE. The
real mechanism is that on B136 the IS width curve is ANTI-CORRELATED with the OOS one
(rank corr −0.700), and the IS margin the chooser acts on is smaller than block-to-block noise.
No RULES change, no book promoted, no KEEP claimed; RULES.md, scan.py, bot.py and baseline.py
untouched.**

Script: `2026-09-07_why-does-the-IS-chooser-prefer-NARROW-on-B136-and-WIDE-on-U56_cloud.py`
(console `.console.txt`; 60-row `.grid.csv`; 37-row `.blocks.csv`; `.widthcurve.csv`;
`.walkforward.csv`).

## Reproduction gates (all PASS before any new number was read)

| Gate | Result |
|---|---|
| `fast_backtest` vs `engine.backtest`, returns / turnover | **0.000e+00 / 0.000e+00** |
| derived rung `r(25) = r(0) − turnover·25/1e4` vs `engine.backtest(25)` | **0.000e+00** |
| idea 333 committed WF: B136 n=10 g=0.75 | IS **1.055860** (pub 1.055860), OOS **0.780593** (pub 0.780593) |
| idea 333 committed WF: U56 n=20 g=0.75 | IS **0.975940**, OOS **1.130697** — both exact |
| idea 333 committed WF: SMALL439 n=20 g=0.75 | IS **0.423147**, OOS **0.465731** — both exact |
| idea 333 committed grid B136 n=20 g=0.75 @10 bps (= idea 329's W m=0) | 12.9930% / 0.943185 / −20.0520%, H1/H2 1.1048/0.8025 — **exact to 1e-6** |

Family unchanged from idea 333: top-n of the v1 composite (vol scaler OFF), v1 eligibility,
NORM weights `g/k_t`, m=0, weekly, next-day execution. Two tuned parameters, **n ∈
{10,20,40,80,ALL} × g ∈ {0.375,0.50,0.625,0.75}** = 20 points/panel, all reported at 0/10/25 bps.

## [A] The ordering the queue asserts does not survive rolling blocks

13 blocks on U56/B136, 11 on SMALL439 (it starts 2011). Pick = argmax IS Sharpe @10 bps.

| Panel | pick_n distribution (10 / 20 / 40 / 80 / ALL) | Flip rate |
|---|---|---|
| B136 | 1 / 1 / 3 / 6 / 2 | **6/12 = 50.0%** |
| U56 | 0 / 7 / 4 / 2 / 0 | 4/12 = 33.3% |
| SMALL439 | 2 / 7 / 1 / 0 / 1 | **6/10 = 60.0%** |

**Block by block, B136 is narrower than U56 on only 2 of 13 blocks, EQUAL on 0, and WIDER on 11.**
The two exceptions are 2009-2013 (B136 n=20 vs U56 n=80) and **2012-2016 (B136 n=10 vs U56 n=20)**
— the second is idea 333's own reading, and it is the *only* block in the whole study where B136
picks n=10. From 2016-2020 onward B136 locks onto n=80 for six consecutive blocks while U56 sits
at 20–40. The "B136 prefers narrow" contrast is a property of one IS window, not of the panel.

## [B] The proposed mechanism is falsified — and points the other way

Blocks split by ≥3 years of overlap with 2009-2013:

| Panel | momentum-run blocks | non-momentum blocks |
|---|---|---|
| B136 | n = 20, 40, ALL | n = **10**, 40×2, 80×6, ALL |
| U56 | n = **80, 80**, 20 | n = 20×6, 40×4 |
| SMALL439 | n = 20 | n = 10×2, 20×6, 40, ALL |

The 2009-2013 run pushes U56 to its **widest** picks of the whole study (n=80 twice) and B136 to
n=20 with a margin of exactly 0.0000 over the anchor. B136's single narrow pick lives in
2012-2016, which overlaps the run by 2 years. So the momentum run cannot be what makes B136 pick
narrow; if anything it is a WIDE-book window on both panels.

## [C0] What actually explains it: the IS width curve is inverted on B136

At g=0.75, 10 bps, over the single 2008-2016 / 2017-2026 split:

| Panel | IS by n (10/20/40/80/ALL) | OOS by n | rank corr IS↔OOS | IS spread | OOS spread |
|---|---|---|---|---|---|
| **B136** | 1.056 / 1.023 / 1.010 / 1.000 / 1.032 | 0.781 / 0.884 / 0.971 / **1.044** / 1.019 | **−0.700** | 0.056 | **0.264** |
| U56 | 0.854 / 0.976 / 0.942 / 0.968 / 0.968 | 0.989 / 1.131 / **1.136** / 1.113 / 1.113 | +0.368 | 0.122 | 0.147 |
| SMALL439 | 0.344 / 0.423 / 0.328 / 0.386 / 0.421 | **0.551** / 0.466 / 0.456 / 0.436 / 0.288 | −0.200 | 0.095 | 0.262 |

On B136 the IS ordering is very nearly the reverse of the OOS ordering, and the IS spread the
chooser reads (0.056) is a fifth of the OOS spread it is choosing across (0.264). That is the
whole of idea 333's +0.266 regret: the chooser is not merely uninformative on this panel for this
dial, it is anti-informative. U56 is the only panel where it is weakly right, which is why its
regret was +0.005.

## [C1] The chooser acts on a margin smaller than its own noise

IS Sharpe of the pick minus the n=20 cell at the same gross, and the block-to-block movement of
the same statistic:

| Panel | mean margin | median | max | median \|ΔIS\| between consecutive blocks |
|---|---|---|---|---|
| B136 | 0.1389 | 0.1402 | 0.2714 | **0.1691** |
| U56 | 0.0266 | 0.0000 | 0.0856 | **0.1877** |
| SMALL439 | 0.0293 | 0.0000 | 0.2084 | **0.1656** |

On every panel the evidence the chooser acts on is at or below the amount the same number moves
when the window slides by one year. On U56 and SMALL439 the median margin is exactly 0.0000 — the
chooser usually picks n=20 and has no preference at all.

## [C2] Does the width preference pay out of block?

Each block's pick scored on the following 3 years (never seen by the chooser), against the fixed
n=20 g=0.75 anchor; 31 of 37 blocks have ≥2 years of follow-on.

| Panel | beats anchor | mean ΔSharpe | mean regret vs forward-best |
|---|---|---|---|
| B136 | **9/11** | **+0.1010** | +0.0926 |
| U56 | 1/11 | −0.0271 | +0.0917 |
| SMALL439 | 2/9 | −0.0571 | +0.1780 |
| **Pooled** | **12/31 = 38.7%** | **+0.0096** | +0.1171 |

Pooled, the chooser is worth nothing. B136's 9/11 is real but must not be read as 9 independent
successes: the blocks overlap 4 of 5 years and the forward windows overlap 2 of 3, and six of
those nine are the same n=80 g=0.375 decision repeated as the window slides. What it does say is
consistent with [C0] — **wide genuinely wins on B136**, and every rolling window from 2014 on
finds it. Only idea 333's 2008-2016 window did not.

## [D] Rule 8 (PROTOCOL's own split; reproduces idea 333 exactly)

| Panel | Pick | OOS CAGR | OOS Sharpe | OOS MaxDD | anchor n=20 OOS | OOS-best | Regret | RULES v2 OOS | SPY OOS | Full 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | n=20, g=0.75 | 14.45% | **1.131** | −18.31% | 1.131 | 1.136 (n=40, g=0.375) | +0.005 | 1.285 | 0.882 | **PASS** |
| B136 | n=10, g=0.75 | 12.77% | **0.781** | −21.44% | 0.884 | 1.046 (n=80, g=0.375) | **+0.266** | 1.119 | 0.882 | FAIL (H2, OOS, DD) |
| SMALL439 | n=20, g=0.75 | 6.95% | **0.466** | −33.48% | 0.466 | 0.551 (n=10, g=0.75) | +0.085 | 0.568 | 0.882 | FAIL (all five) |

SPY OOS 15.45% / 0.882 / −33.72%. **KEEP paths over all 60 points: 4a 0/60 at every rung; 4b
13/60 @0 bps, 5/60 @10 bps, 0/60 @25 bps** — U56 n=20 and n=40 at g=0.75, B136 n=40/80/ALL at
g=0.75. These are the record's existing U56 object plus B136 cells idea 333 already filed; no new
candidate and no memo.

## Verdict

**SPLIT: the queue's question is answered, its premise-as-an-ordering is KILLED, and its proposed
mechanism is KILLED.** What survives is a sharper and more useful statement: on B136 the rule-8
width chooser is *anti-informative* (IS↔OOS rank corr −0.700, IS spread 0.056 vs OOS spread
0.264), and on all three panels it acts on a margin at or below the noise of its own window. Idea
333's B136 pick was not a narrow-panel preference — it was the one window in thirteen that reads
that way. **Practical consequence for PROTOCOL rule 8:** on this family the width dial should be
pre-registered rather than IS-chosen; a chooser whose IS margin (≤0.27) is below the window-slide
noise of the same statistic (≈0.17) has no business selecting n, and quoting its regret as if it
were a tuning cost understates the problem — on B136 it is worse than a coin.

## Caveats

(1) All three panels are current-constituent lists — **SURVIVORSHIP** — which flatters every
momentum book; the 2009-2013 block is where it bites hardest, so the wide-book preference found
there is the most suspect number here. The 44 tickers with `max_1d_move ≥ 1.0` in
`data/small_meta.csv` are dropped from the small panel first (439 names). (2) SMALL439 starts
2010-01-04, so it has 11 blocks and none covering 2009. (3) The first U56/B136 block starts at the
panel's evaluation start (2009-01-13), ~8 trading days into 2009. (4) Rolling blocks overlap by
4 of 5 years and their forward windows by 2 of 3, so block counts are not independent trials;
this is why [C2] is reported per panel with the overlap stated rather than as a win rate with a
p-value. (5) The last blocks' forward windows are truncated by the data (last close 2026-09-04);
blocks with under ~2 years of follow-on are excluded from [C2].
