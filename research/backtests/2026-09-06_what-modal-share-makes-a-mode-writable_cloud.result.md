# Idea 219 — what-modal-share-makes-a-mode-writable (cloud, 2026-09-06)

**KILL of the modal-share floor. There is no share at which the held-out mode stops beating the
fit, because the mode never stops beating the fit — and the record's one counter-example (idea
189's N cell at 22.6%, held-out mode −0.0229) is ONE DRAW of a distribution whose mean over 80
draws is +0.0050 with a 66% win rate. Worse, a share gate SUBTRACTS value: it withholds the
mode exactly where the mode has the most room. No RULES change, no new book, no KEEP candidate;
RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-06_what-modal-share-makes-a-mode-writable_cloud.py`; artefacts `.console.txt`,
`.ladder.csv.gz`, `.cells.csv`, `.sweep.csv`, `.walkforward.csv`, `.keep.csv`. 350 s.

## Reproduction, before any new number was read

Ideas 171/189/217 imported verbatim (`Book`, `build_corpus`, `build_corpus_B`, `fast_backtest`,
the metric helpers, the 4a/4b bars). Four controls, all asserted first:

* `fast_backtest` == `engine.backtest` at D/W/M/Q, max |dret| **1.7e-18 … 6.2e-17**.
* CAND-20 weights == idea 78's `weights_cand` on three books, **0.000e+00**.
* idea 217's cost identity `net(c) = gross − turnover·c/1e4` re-asserted direct-vs-derived over
  3 books × 3 configs × 5 rungs: **0.000e+00** (so the 5 rungs cost one simulation, not five).
* the rebuilt ladder vs **both** committed parents: idea 189's `ladder.csv` **6048/6048 rows**
  and idea 217's **30240/30240 rows**, max |d| over 12 metric columns **3.553e-15**, **0 4a/4b
  verdict mismatches**. Idea 189's published Q6 table re-derives to 4 decimals (corpus A
  MODE-LOO 1.0196 / SEL-SHARPE 1.0100 / CONST-INC 0.9638 / ORACLE 1.0438; corpus B 0.7375 /
  0.7251 / 0.6793 / 0.7716).

36 120 ladder rows: 168 books × 43 simulated points × 5 rungs, 10 bps carried as the anchor,
IS ≤ 2016-12-31 chooses, OOS ≥ 2017-01-01 read once.

## Q2 — why the record's 10 cells could not answer this

Idea 189's grid puts 9 of its 10 cells at share ≥ 0.67 and 2 at ~0.23; **the whole 0.25–0.65
range is empty**, so no threshold in it is identified. The cell corpus is widened along three
axes already in the record and costing nothing extra — idea 217's 5 cost rungs, sub-panel book
GROUPS (each family and family × k, a different pick distribution on the same simulator), and
idea 218's two extendable dials (BAND → 0.15, SLEEVE → 0.50; GROSS is NOT extended, it needs a
financing assumption and idea 218 called its extension a truncation artefact). **560 cells**,
16 groups, 7 dial views; coverage 18 / 49 / 91 / 55 / 43 / 27 / 48 / 90 / 119 cells per 0.10
share bin from 0.15 to 1.05.

Each cell runs the mode's own walk-forward **40 times** (seeded random half reads the mode and
its share, the other half is scored, both directions) = **44 800 observations**, against idea
189's single seeded split.

**The record's counter-example does not survive that.** Idea 189's Q5 cell, re-derived:

| corpus | dial | mode | share | mode stable across halves | mean d (80 draws) | win rate | idea 189's single draw |
|---|---|---|---|---|---|---|---|
| A | **N** | 20 | **22.6%** | **25.0%** | **+0.0050** | **66.2%** | **−0.0229** |
| B | N | 15 | 23.5% | 77.5% | +0.0167 | 91.2% | +0.0256 |
| A | CADENCE | M | 83.0% | 100.0% | +0.0261 | 100.0% | +0.0261 |
| B | CADENCE | M | 88.7% | 100.0% | +0.0255 | 100.0% | +0.0255 |
| A | BAND | 0.08 | 81.1% | 100.0% | +0.0005 | 56.2% | +0.0005 |
| B | BAND | 0.08 | 68.7% | 100.0% | +0.0078 | 97.5% | +0.0078 |
| A | GROSS | 1.00 | 94.3% | 100.0% | −0.0001 | 12.5% | −0.0001 |
| B | GROSS | 1.00 | 84.3% | 100.0% | −0.0000 | 33.8% | −0.0000 |
| A | SLEEVE | 0.30 | 100.0% | 100.0% | +0.0000 | 0.0% | +0.0000 |
| B | SLEEVE | 0.30 | 87.8% | 100.0% | +0.0030 | 98.8% | +0.0030 |

Nine cells are deterministic to 4 decimals under resampling — because their mode is stable in
100% of splits, so there is only one draw to take. **The tenth, the only one whose mode is
unstable (25%), is the only one whose single draw was informative about the split rather than
about the dial**, and its sign flips. This is idea 158's finding again, on a different statistic.

## Q3 — the curve (threshold-free, reported before any threshold was chosen)

Mean d = OOS Sharpe(held-out mode) − OOS Sharpe(each book's own IS fit), binned by the share
read on the fitting half, m_min = 12 (560 cells):

| share bin | cells | mean d | median d | t | cells d>0 | mean d(4b margin) |
|---|---|---|---|---|---|---|
| [0.00,0.25) | 18 | **+0.0073** | +0.0076 | +1.29 | 61.1% | +0.0234 |
| [0.25,0.35) | 49 | +0.0032 | +0.0036 | +1.12 | 59.2% | +0.0186 |
| [0.35,0.45) | 91 | **−0.0040** | −0.0005 | −2.04 | 49.5% | −0.0097 |
| [0.45,0.55) | 55 | +0.0111 | +0.0048 | +4.83 | 70.9% | +0.0064 |
| [0.55,0.65) | 43 | +0.0206 | +0.0050 | +4.50 | 79.1% | +0.0179 |
| [0.65,0.75) | 27 | +0.0223 | +0.0078 | +3.62 | 70.4% | +0.0175 |
| [0.75,0.85) | 68 | +0.0082 | +0.0003 | +3.24 | 58.8% | +0.0137 |
| [0.85,0.95) | 90 | +0.0056 | +0.0013 | +5.48 | 57.8% | +0.0051 |
| [0.95,1.01) | 119 | +0.0004 | +0.0000 | +2.65 | 7.6% | +0.0003 |

**Spearman(share, mean d) = −0.046** over 560 cells, **−0.131** on corpus A and **−0.015** on
corpus B — and it gets MORE negative as the group-size floor tightens (−0.106 at m_min = 20,
−0.234 at m_min = 40, negative on both corpora at every level). **P2 predicted a positive slope
and is a clean MISS: the relationship the queue assumed exists, runs the other way.**

The lowest share bin in the whole corpus is the second-best bin on the board. The highest bin is
the worst, for a reason that is arithmetic rather than empirical: at share ≥ 0.95 the mode IS
the fit in ≥ 95% of books, so d ≈ 0 by construction (7.6% of those cells are positive because
92.4% are exactly zero). **Modal share governs how much a mode can move, not whether moving
helps.**

Per dial view (m_min = 12, pooled over rungs and groups) says the same thing:

| dial view | share | mean d | cells d>0 | mode stable |
|---|---|---|---|---|
| GROSS | 88.3% | −0.0000 | 18.8% | 94.4% |
| BAND | 75.7% | +0.0013 | 37.5% | 89.0% |
| SLEEVE | 92.3% | +0.0013 | 41.2% | 95.2% |
| **CADENCE** | 85.6% | **+0.0254** | 76.2% | 97.9% |
| **N** | **38.4%** | **+0.0084** | 60.0% | 35.9% |
| **BAND+** | **42.3%** | **+0.0016** | 66.2% | 38.9% |
| **SLEEVE+** | **54.1%** | +0.0011 | 47.5% | 60.1% |

The three dials whose share falls below 0.6 — the ones a floor would gag — have mean d of
+0.0084, +0.0016, +0.0011, all positive.

## Q4 — the sweep: no threshold separates (every grid point in `.sweep.csv`)

33 τ from 0.200 to 1.000. What a floor would have to show is `above` positive and `below` not.

| τ | n ≥ τ | mean d above | n < τ | mean d below | separation |
|---|---|---|---|---|---|
| 0.200 | 560 | +0.0056 | 0 | — | — |
| 0.300 | 526 | +0.0058 | 34 | +0.0018 | +0.0040 |
| 0.400 | 439 | +0.0075 | 121 | −0.0015 | **+0.0091** (max) |
| 0.500 | 374 | +0.0076 | 186 | +0.0014 | +0.0062 |
| 0.600 | 331 | +0.0073 | 229 | +0.0031 | +0.0042 |
| 0.700 | 284 | +0.0043 | 276 | +0.0069 | **−0.0026** |
| 0.800 | 251 | +0.0032 | 309 | +0.0075 | −0.0043 |
| 0.900 | 169 | +0.0009 | 391 | +0.0076 | −0.0067 |
| 0.975 | 100 | +0.0000 | 460 | +0.0068 | −0.0068 |

**At NO τ is the below-group mean negative by more than −0.0015 (t −0.80), and above τ = 0.65 the
separation INVERTS** — the cells a floor would exclude are the better half. The best available
separation, +0.0091 at τ = 0.40, is one fifth of the CADENCE dial's own effect and rests on a
below-group mean that is statistically zero.

The local-window (±0.075) crossing reads **0.425**, with a **block bootstrap over 112
(corpus, dial, group) blocks giving a 90% CI of [0.200, 0.450]** — the lower limit is the grid's
left edge, i.e. in a large share of draws there is no negative window anywhere and the "crossing"
is an artefact of a −0.003 wobble at 0.30–0.42 whose local win rates never drop below 51.4%.
**P3 and P4 are HITS on a number that the sweep beside them shows is not a threshold.**

## Q5 — rule 8 on the threshold itself, and the gate priced

τ is a fitted parameter, so it gets rule 8. Chosen to maximise banked value on one half of the
evidence, applied to the other:

| chosen on | evaluated on | τ* | cells gated | mean d among gated | value/cell |
|---|---|---|---|---|---|
| corpus A | corpus B | 0.300 | 363 of 385 | +0.0053 | +0.0050 |
| corpus B | corpus A | 0.400 | 136 of 175 | +0.0071 | +0.0055 |
| 10 bps | 5/15/20/25 bps | 0.450 | 324 of 448 | +0.0081 | +0.0058 |
| published dials | extended dials | 0.400 | 95 of 160 | +0.0037 | +0.0022 |

τ* transfers (0.30–0.45 everywhere) — and transferring it does not make it worth having. Book
level, every pick on IS ≤ 2016-12-31, OOS ≥ 2017 read once, GATED using the τ chosen on the
OTHER corpus (A: 0.400, B: 0.300):

| corpus | arm | OOS Sharpe | OOS CAGR | OOS MaxDD | d vs fit |
|---|---|---|---|---|---|
| A | ORACLE (not implementable) | 1.0336 | 9.23% | −15.14% | +0.0294 |
| A | **MODE-LOO (ungated)** | **1.0109** | 9.96% | −16.92% | **+0.0067** |
| A | GATED (share floor) | 1.0082 | 10.08% | −17.12% | +0.0040 |
| A | SEL-SHARPE (the fit) | 1.0042 | 10.02% | −17.20% | 0 |
| A | SEL-4B | 0.9643 | 10.06% | −17.50% | −0.0399 |
| A | RANDOM | 0.9520 | 9.17% | −16.52% | −0.0522 |
| A | CONST-INC | 0.9275 | 9.52% | −17.31% | −0.0767 |
| B | ORACLE | 0.7744 | 5.45% | −15.42% | +0.0475 |
| B | **MODE-LOO (ungated)** | **0.7351** | 5.63% | −16.78% | **+0.0083** |
| B | GATED | 0.7324 | 5.61% | −17.12% | +0.0056 |
| B | SEL-SHARPE | 0.7268 | 5.45% | −17.06% | 0 |
| B | SEL-4B | 0.7440 | 6.04% | −16.88% | +0.0172 |
| B | RANDOM | 0.6820 | 4.98% | −16.69% | −0.0448 |
| B | CONST-INC | 0.6470 | 4.94% | −17.43% | −0.0799 |

**P5 is a HIT that argues against its own clause.** The gate does beat the fit (+0.0040 / +0.0056)
— but it beats it by LESS than doing nothing at all about share (+0.0067 / +0.0083). **The floor
costs 40% and 33% of the modal constant's value on corpora A and B respectively**, and it costs
it in the obvious place: the dials it switches OFF are exactly N, BAND+ and SLEEVE+ — the three
whose mean d is positive and whose ladders are the only genuinely non-degenerate ones in the set.
Restricted to idea 189's own published grid the ordering is identical (A: MODE-LOO 1.0196 >
GATED 1.0153 > SEL-SHARPE 1.0100; B: 0.7375 > 0.7324 > 0.7251).

Benchmarks, OOS: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 @10 bps 7.73% / 0.7471 / −13.83%
(U56), 5.94% / 0.5763 / −21.19% (B136), 7.88% / 0.6617 / −32.37% (small).

## Q6 — both KEEP paths

Over all 36 120 rows: 4a passes 1511/1857/1996/2056/2106 (corpus A) and 1250/1589/1906/2204/2532
(corpus B) at 5/10/15/20/25 bps; 4b passes 464/301/179/105/64 (A) and 410/307/248/178/137 (B).
By parent: **B136 1004 of 10750, U56 1389 of 14620, SMALL 0 of 10750 — the fourteenth
reproduction of idea 136's "no defensive class on the small panel" (P6 HIT).** Idea 218's
extended points contribute 425 of 5880 4b passes, 7 of them on a fixed panel; the best are U56
BAND = 0.12 (13.9% / 1.1487 / −18.17%, halves 1.138/1.162, OOS 1.2231) and BSTK100 SLEEVE = 0.35
(10.7% / 1.1733 / −15.89%, halves 1.394/1.000, OOS 1.0931). Per idea 144 a re-dialled book is
the same book, so **nothing here is proposed**; the best fixed-panel rows overall remain U56
SLEEVE = 0.25 (10.9% / 1.2212 / −13.57%, OOS 1.2856) and U56 CADENCE = M (14.8% / 1.2081 /
−19.58%, OOS 1.2866), both already in the record via ideas 101/134/175/189.

## What PROTOCOL should carry instead

Idea 189's sentence should not become a clause. The one-line replacement the evidence supports:

> A mode read on a corpus is worth writing down whenever the corpus is the unit you are willing
> to write for; its modal SHARE bounds how far the constant can move the answer, and does not
> predict the sign of the move. Report the share as a scale, never as a gate. Where a mode is
> unstable across corpus halves (idea 189's N), report the split-half distribution of the
> held-out difference, not one draw of it.

## Predictions

5 of 6 hit. **P1** (both parents reproduce) HIT at 3.553e-15, 0 mismatches. **P2 MISS, and it is
the run's headline**: the slope is negative (−0.046 overall, −0.131 / −0.015 by corpus, −0.234 at
m_min = 40), not positive. **P3** HIT (crossing 0.425 ∈ (0.226, 0.830)) and **P4** HIT (< 0.60) —
both on a "crossing" the bootstrap CI [0.200, 0.450] and the sweep's below-group means show is
not a real separation, so neither carries the information the prediction wanted. **P5** HIT
(GATED beats the fit on both corpora, +0.0040 / +0.0056) — and the arm table beside it shows the
gate loses to no gate at all, which is the KILL. **P6** HIT (0 SMALL 4b passes).

## Caveats carried

Current-constituent survivorship (idea 54) on B136, U56, ETF36 and the small panel: every arm
inherits it equally so the paired comparisons are unaffected, but every LEVEL above is biased
upward and none is a tradable estimate. Corpus A's `SMALL484` is idea 171's, built WITHOUT the
`max_1d_move >= 1.0` screen (corpus B's `SMALL439` applies it, 44 names dropped); corpus A is not
altered because it is the reproduction target, and that book is 1 of 53 and never a group of its
own. Cells are NOT independent: they share books (a k-group is a subset of ALL), share
simulations across rungs (one 0 bps run, derived by subtraction), and share parents (48 of corpus
A's 53 books are B136 sub-panels) — every t and CI here is over correlated units and optimistic
in size, which is why the crossing is bootstrapped over whole (corpus, dial, group) blocks and no
p-value is treated as one on a fresh sample. The modal share is itself estimated on half-corpora
of 8–57 books and its sampling error is largest exactly where the share is lowest; that is a
property of the statistic a floor would be written on, not a defect here. The m_min grid has
three effective levels, not four: every book group has ≥ 16 members, so m_min = 8 and 12 admit
the same 560 cells. Idea 144, idea 38's calendar-day index and idea 126's t+1-only execution
carry over. GROSS is not extended past 1.00 (financing).

## Follow-ups queued

221 (does share predict the VARIANCE of the held-out difference, which is what the curve's shape
actually says), 222 (back-fill the split-half DISTRIBUTION over every published single-draw
split-half claim in the record — idea 158's programme applied to this statistic), 223 (why the
0.35–0.45 window dips: is it a dial-composition artefact of BAND+/SLEEVE+ or a real hole).
