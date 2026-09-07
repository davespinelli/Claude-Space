# Idea 380 — the SCORED vs PRICED denominator. **DEFECT LOCALISED. Proposal: standardise on PRICED.**

The queue's "5-point sign-stability gap" is real and reproduces exactly — but it is **not a
broad shift**. It is **4 of 32 arm-points, all of them the entry-budget (`ebud`) arms**, where
the PRICED book scores frac_pos 0.000 and the SCORED book 0.225–0.550. Everywhere else the two
conventions are indistinguishable. The convention still needs fixing, because it is the *sign
statistic* the record publishes, not the returns, that the choice moves.

## Gates (all before any new number, all EXACT)
| gate | result |
|---|---|
| PRICED arm == idea 94's `EWall` construction | max\|d\| **0.000e+00** |
| SCORED arm == idea 124 `_B2`'s `ALL` rung construction | max\|d\| **0.000e+00** |
| published max \|Δw\| 0.0150 on u56 | **0.0150**, \|d\| 0.0000 |
| published disagreement days 1530 of 4439 | **1530 of 4439** (34.5%) |
| published D3 frac_pos pair 0.8133 / 0.7609 (q = 0.10, identical draws) | **0.8133 / 0.7609**, \|d\| 0.0000 / 0.0000 |

## [A] The audit — the record has no convention
**16 committed scripts build an all-names denominator: PRICED 9, SCORED 5, BOTH 2** (one script
uses both idioms in the same file). Attributable committed LEADERBOARD rows: **PRICED 73,
SCORED 42, BOTH 7**. Every classification is backed by the matched construction line, committed
to `.audit.csv`. And decisively: **the live book already has a convention** —
`baseline.rules_v2_weights` is documented as *"gross/N of NAV, N = instruments priced that
day"*, i.e. **PRICED**.

## [B] What the choice is worth (36 cells: 6 M × 2 warm-ups × 3 panels, 3 cost rungs each)
Both conventions are endpoints of one ladder: require M prior closes to count. M = 1 **is**
PRICED; M = 253 and the exact composite mask are indistinguishable to 3 d.p. on every panel.

| panel | Δ CAGR | Δ Sharpe | Δ MaxDD (PRICED − SCORED) | Δ OOS | 4b flip |
|---|---|---|---|---|---|
| U56 | −0.07 pp | −0.0042 | +0.00 pp | −0.0095 | no |
| B136 | −0.04 pp | −0.0026 | +0.07 pp | −0.0025 | no |
| SMALL439 | +0.02 pp | −0.0032 | **−1.10 pp** | +0.0033 | no |

(SCORED − PRICED, 10 bps, WARM 260; the WARM 504 column is the same to ±0.002 Sharpe.)
**Max \|ΔSharpe\| across all 6 panel × warm-up cells is 0.0050 and max \|ΔCAGR\| is 0.08 pp; 0
of 6 4b verdicts flip.** The longer warm-up does not remove the disagreement (U56 34.5% → 33.0%
of days), so this is not a warm-up artefact — it is a panel-entry phenomenon, and it is nearly
total on the panel that has real entries (**SMALL439: the counts disagree on 3889 of 3934 days,
98.9%**, mean 348.9 PRICED names against 336.4 SCORED).

## [C] Sign stability of the difference (40 seeded draws, q = 0.10, both books rebuilt)
| panel | ΔSharpe mean | frac_pos | ΔMaxDD mean (PRICED − SCORED) | frac_pos |
|---|---|---|---|---|
| U56 | −0.0042 | 0.100 | −0.00 pp | 0.325 |
| B136 | −0.0026 | 0.075 | +0.07 pp | 0.925 |
| SMALL439 | −0.0037 | 0.050 | **−1.03 pp** | **0.000** |

The difference is tiny but **systematic, not noise**: SCORED is the worse book in 36–38 of 40
draws on every panel, and on the small panel PRICED is the shallower drawdown in **40 of 40**.

## [C2] Where the 5 points actually live — **the entry-budget arms, and nothing else**
On the 32 identical arm-points of the ALL rung, **only 4 differ at all**:

| universe | arm | SCORED | PRICED | Δ |
|---|---|---|---|---|
| u56 | `ebud-0.10` | 0.225 | 0.000 | +0.225 |
| u56 | `ebud-0.20` | 0.425 | 0.000 | +0.425 |
| broad | `ebud-0.10` | 0.550 | 0.000 | +0.550 |
| broad | `ebud-0.20` | 0.475 | 0.000 | +0.475 |

The other 28 arm-points are **identical to the digit**. The mechanism is clear: the entry-only
turnover budget binds on the weight vector itself, so a 0.0150 change in a ~0.014 weight
changes *which entries fit the budget*, and the sign of the arm's dMaxDD flips on up to 22 of
40 draws. **A 1.5 pp weight difference moves a published sign statistic by up to 0.550.** No
other instrument in idea 94's menu is exposed.

## [D] Rule 8 walk-forward ((M, WARM) on 2009–2016 IS Sharpe @10 bps, 2017–2026 read once)
| panel | pick | OOS Sharpe | OOS CAGR | regret | PRICED anchor | SPY | RULES v2 |
|---|---|---|---|---|---|---|---|
| U56 | M=63, WARM 260 | 1.125 | 13.67% | −0.010 | **1.136** | 0.882 | 1.285 |
| B136 | **M=1**, WARM 260 | 1.102 | 13.93% | +0.000 | 1.102 | 0.882 | 1.119 |
| SMALL439 | **M=1**, WARM 504 | 0.637 | 10.09% | −0.003 | 0.637 | 0.882 | 0.568 |

The IS chooser picks the PRICED endpoint on 2 of 3 panels with zero regret, and its one
non-PRICED pick (U56 M=63) *loses* to the PRICED anchor out of sample. **No cell beats live
RULES v2 on any panel.**

## [E] KEEP paths
**4b 0/36 and 4a 0/36 at 0, 10 and 25 bps** — the ungated all-names book at 75% gross clears
neither path on any panel at any warm-up. That is worth recording in its own right: the object
this whole convention argument is about is not capital-worthy either way.

## The proposal
**Standardise on PRICED — the denominator is every instrument with a close that day — and
state it in PROTOCOL rule 1.** Four reasons, in order of force:
1. **The live book already uses it** (`rules_v2_weights`: "N = instruments priced that day"), so
   PRICED is the only choice that keeps the record's all-names books comparable to the book the
   project actually runs.
2. It is the record's majority (9 scripts / 73 LEADERBOARD rows against 5 / 42).
3. It wins the one axis where the difference is material: **−1.10 pp of MaxDD on SMALL439, in
   40 of 40 bootstrap draws**.
4. SCORED silently embeds a **253-day price history requirement into a book that has no
   ranking** — a hidden dependency on a signal the book does not use, and the reason the two
   diverge on 98.9% of small-panel days.

**Second clause, narrower and more urgent:** any run quoting a sign-stability statistic for a
**turnover-budget arm** must state its denominator convention, because that is the only arm
family where the choice moves the statistic — by up to 0.550, i.e. more than the entire
published 5-point headline.

## Caveats
Survivorship: all three panels are current-constituent lists, so CAGR levels are optimistic; a
survivorship-free panel would have *more* entry dates and would make the gap larger, not
smaller. SMALL439 starts 2010-01-04 so its halves are not the same calendar halves. The audit's
classifier is a regex over committed source with every matched line committed as evidence in
`.audit.csv`; it reports what it found and cannot prove it found everything.
