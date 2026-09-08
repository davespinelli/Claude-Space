# Idea 226 — why-the-035-045-share-window-dips (cloud, 2026-09-08)

**ANSWERED. The dip is NEITHER of the two things the queue offered: not a dial-composition
artefact (controlling for the mix makes it DEEPER and significant) and not a hole worth a clause
(the raw dip is inside its own CI, flips sign at 6 of 12 tuned-parameter points, and is worth
+0.0005 of OOS Sharpe when written in). It is a NOISY-MODE band carried by the 16-book k-groups.**

Script: `2026-09-08_why-the-035-045-share-window-dips_cloud.py`. Substrate: idea 219's committed
`cells.csv` (560 cells) and `ladder.csv.gz` (36 120 rows), READ not re-simulated — which makes Q1
an exact reproduction test against the 33 numbers in 219's console. Outputs: `.console.txt
.curve.csv .composition.csv .bydial.csv .holdout.csv .adjusted.csv .boot.csv .params.csv
.groupsize.csv .book.csv .walkforward.csv`.

## The chain

**Q1 reproduction.** All 33 published rows rebuilt: 0 cell-count errors, max |Δ mean_d| 5.0e-05,
max |Δ frac_pos| 5.0e-04 (printed precision). The dip under test is **−0.0030 at share 0.325**;
28 of 33 grid points are positive.

**Q2 composition — the queue's premise is TRUE about the mix.** In the window [0.225, 0.500]
(184 cells) BAND+ and SLEEVE+ hold **0.538** of the cells vs **0.286** corpus-wide (lift +0.252).
But the biggest single over-representation is **N** (0.348 vs 0.143, +0.205), which the queue does
not name. CADENCE has **zero** cells there. The window's modal shares are also the corpus's
noisiest: mean share_sd **0.0726** vs 0.0617 corpus-wide.

**Q3 dial-by-dial — the dip is not one view.** 5 of 7 views go negative somewhere in the window
(BAND −0.0031, BAND+ −0.0038, N −0.0049, SLEEVE −0.0052, SLEEVE+ −0.0112); only GROSS is
uniformly positive and CADENCE has no cells. **P3 MISS** (≤2 predicted).

**Q4 leave-one-dial-out — no single view removes it.**

| held out | dip depth | vs all-dials |
|---|---|---|
| (none) | −0.0030 | — |
| BAND | −0.0030 | +0.0000 |
| **BAND+** | **−0.0062** | **−0.0031** (deeper) |
| CADENCE | −0.0030 | +0.0000 |
| GROSS | −0.0032 | −0.0001 |
| N | −0.0027 | +0.0003 |
| SLEEVE | −0.0030 | +0.0000 |
| SLEEVE+ | −0.0013 | +0.0018 |

Holding out the queue's prime suspect, BAND+, **doubles** the dip. Only SLEEVE+ shrinks it
materially, and not to zero.

**Q5 composition-adjusted curve — the mix was MASKING the dip, not creating it.**
raw −0.0030 → dial FE **−0.0067** → dial×corpus×rung FE −0.0064 → equal-weight-by-dial −0.0031.
**P4 MISS**: the adjustment adds 122% to the depth instead of removing half of it.

**Q6 sampling — the two readings disagree, and that is the whole result.**
112 blocks, 2000 resamples, seed 226700:
* raw depth −0.0030, 90% CI **[−0.0095, +0.0019]**, P(depth ≥ 0) = 0.155 → **0 INSIDE** (P5 HIT).
* dial-FE depth −0.0067, 90% CI **[−0.0115, −0.0033]**, P(depth ≥ 0) = 0.000 → 0 outside.

A cell-level sign test over the whole window is *positive*: 103/184 cells, mean +0.0017, t +1.16.
So the negative local means come from the ±0.075 smoothing, not from a majority of negative cells.

**Q7 the two tuned parameters (m_min × half-width, all 12 points reported).** The raw depth is
negative at 6 of 12 and **positive at every point with m_min ≥ 20** (+0.0029 to +0.0052); the
dial-FE depth is negative at 12/12.

**The mechanism.** m_min ≥ 20 drops exactly the 16-book k-groups. Split on group size:

| stratum | cells | raw dip depth | dial-FE depth | in-window share_sd |
|---|---|---|---|---|
| 16-book k-groups | 350 | **−0.0126** | −0.0152 | 0.0884 |
| groups with ≥ 20 books | 210 | **+0.0029** | −0.0034 | 0.0542 |

The dip lives entirely in the 16-book sub-panel groups, where the mode is read on 8 books per
split half. Note it is *not* simply "small groups": in the window the mean group is slightly
larger (33.3 vs 30.5 books) — the noise is intrinsic to a low-concentration mode, which is
precisely what idea 224 (still open) proposes measuring as sd rather than mean.

## Consequence (PROTOCOL 2/3/4/8) — writing the hole in buys nothing

The gate 219 proposed (mode where share ≥ tau, else the per-book IS-Sharpe fit) and its HOLED
variant, built over all 15 book groups on 219's committed ladder: 49 200 arm-rows over 12 300
(corpus, rung, dial, group, book) units, tau inherited from 219's cross-corpus rule 8
(A 0.400, B 0.300). 107 of 560 cells sit in the window; 74 also clear tau (all on corpus B —
corpus A's tau of 0.400 sits above the window, so the hole cannot bite there at all).

* The hole bites in **694 of 12 300** rows and actually changes **484**. On the biting rows only:
  HOLED − GATE = **+0.0001, t +0.02**, wins 244/694.
* Arm means (10 bps rung inside the 5-rung set; full table in `.book.csv`): corpus B GATE
  5.28%/0.682/−18.4% (OOS 5.59%/0.707/−18.3%) vs GATE-HOLED 5.32%/0.684/−18.4%
  (OOS 5.60%/0.707/−18.3%) vs SEL-SHARPE 5.28%/0.696/−18.0% (OOS 5.51%/0.715/−17.9%).
* **4b passes go DOWN with the hole**: 1098 vs 1116 for the plain gate. **SMALL-parent 4b passes:
  0 of 7350** under either gate.
* References @10 bps: U56 window SPY 15.23%/0.889/−33.7% (OOS 15.45%/0.882/−33.7%),
  RULES v2 8.66%/1.206/−12.1% (OOS 9.53%/1.285/−12.1%); SMALL window SPY 14.13%/0.862/−33.7%,
  RULES v2 3.80%/0.571/−14.7% (OOS 3.84%/0.566/−14.7%).

**Rule 8** (picks on IS ≤ 2016-12-31, 2017→ read once, 400 cells): every gate arm LOSES to just
fitting per book. Corpus A GATE OOS 0.998 vs SEL-SHARPE 1.003 (d −0.0049, 38/125 wins);
corpus B GATE 0.726 vs 0.732 (d −0.0067, 117/275). HOLED minus plain, cell level: **+0.0005,
t +1.02, 16/400 wins, 37 cells differ at all** — indistinguishable from zero. **P6 MISS on the
letter** (mean is +0.0005, not ≤ 0); the effect is null and on 4b counts it is negative.

## Pre-registered predictions

| | prediction | result |
|---|---|---|
| P1 | 33 published rows reproduce exactly | **HIT** |
| P2 | BAND+/SLEEVE+ over-represented in the window | **HIT** (0.538 vs 0.286) |
| P3 | ≤2 of 7 dial views negative in the window | **MISS** (5 of 7) |
| P4 | dial FE shrinks the depth by >half | **MISS** (it deepens it 122%) |
| P5 | 90% CI on the raw depth contains 0 | **HIT** ([−0.0095, +0.0019]) |
| P6 | HOLED ≤ plain AND 0 SMALL-parent 4b passes | **MISS on the letter** (+0.0005, t +1.02; 0 SMALL 4b passes) |

Three of six predictions missed, all in the same direction: the dip is more robust to composition
than expected and less robust to sampling and to group size.

## Recommendation

**Stop quoting the −0.003 wobble as a feature of the share curve.** A modal-share clause needs a
FLOOR, not a hole, and the floor should carry a minimum-books condition: m_min ≥ 20 removes the
dip from the raw curve altogether. Written in as an actual hole the clause changes 37 of 400
cells and buys +0.0005 of OOS Sharpe while costing 18 4b passes.

**Verdict: ANSWERED / report-only. No book, no PROTOCOL edit made here.**

## Caveats carried

* **SURVIVORSHIP** (idea 54): U56, B136 and the small panel are current-constituent lists with no
  delistings. Every arm inherits it equally so the PAIRED contrasts are unaffected; every LEVEL
  is biased upward and none is a tradable estimate. No book is proposed.
* Cells are **not independent**: they share books, share one 0-bps simulation across the five
  cost rungs (219's exact cost-additivity identity), and 48 of corpus A's 53 books are B136
  sub-panels. Every t and CI here is over correlated units and its nominal size is optimistic;
  the bootstrap resamples whole (corpus, dial, group) blocks to blunt the worst of it, and no
  p-value here is a p-value on a fresh sample.
* m_min = 12 (219's headline) admits **all 560 cells** — it was never a binding setting in the
  parent, which is why the m_min sweep is the informative axis here rather than a robustness
  check.
* The gate uses each cell's FULL-corpus modal share and mode (219's "read it once and write it
  down" arm), while the curve is built on split-half shares. That is 219's own convention, kept
  so the two are comparable; it means the Q8 coverage count (107/560, 74 clearing tau) is a
  statement about full-corpus shares, not about the split-half shares plotted in the curve.
* Idea 144: a re-dialled book is the same book. Nothing here is a new signal.
