# Idea 232 — does-the-vol-gate-corner-survive-being-pre-registered (cloud lane, 2026-09-08)

> **RACE NOTICE.** Lane B published this queue item as commit `47c569b` while this run was
> executing; the two scripts were written independently against the same queue text. This lane's
> value is therefore (i) an **independent replication** — every overlapping cell agrees, see
> *Reconciliation* below — and (ii) **one axis lane B did not run**: the exposure-matched gross
> convention that decides whether the corner is idea 157's cash channel. Lane B's own distinctive
> axis, the **ranking key** (`V1KEY`, the live vol-scaled key), is the more important finding of
> the two and materially qualifies this one; it is carried into the verdict below rather than
> reported separately.

**Verdict: SPLIT.** The question is answered and the answer is YES — **the vol-gate corner does
not need a selector.** Removing the `vol20 < 0.60` clause beats keeping it in **63 of 63**
full-sample cells (3 panels × 3 n × 7 rungs), mean **+0.129** Sharpe, and it is **not** idea
157's cash channel: with exposure matched (gross rebuilt to 1.00) the gap is **+0.132**, i.e.
**103% of the de-grossed gap**, so pre-registered prediction R2 is falsified. But the corner
buys **no book**: 4a **0 of 756**, and the 36 4b passes are a property of the n = 40 de-grossed
U56 book — they occur at **every cap including 0.30**, and U56 under matched exposure is
**0 of 126**. No RULES change, no KEEP.

Script: `research/backtests/2026-09-08_does-the-vol-gate-corner-survive-being-pre-registered_cloud.py`
Artefacts: `.console.txt`, `.grid.csv` (756 rows), `.pair.csv`, `.walkforward.csv`, `.keep.csv`

---

## Reproduction gates (passed BEFORE any new number was read)

| gate | requirement | result |
|---|---|---|
| [a] harness | the fast backtester must replicate `engine.backtest` on 6 books | max \|d returns\| **2.8e-17**, \|d turnover\| **5.6e-16** |
| [b] cost identity | `net(c) = gross − turnover·c/1e4` vs a direct 10 bps backtest | max \|d\| = **4.2e-17** |
| [c] premise | idea 228's published OOS Sharpe for the do-nothing book (n=20, g=0, max_vol=0.60, k=1, dg) at 10 bps: U56 **1.1683**, B136 **0.8937** | **1.1683** and **0.8937**, \|d\| = **0.0000** both |

Idea 228's own numbers reproduce exactly, so this tests that result, not a different one.
(SMALL439 reads 0.4881 against idea 228's 0.5116 — a different panel, 439 names vs 484, not a
discrepancy; it is reported, never used as a gate.)

## Design

Idea 228's book verbatim: eligible = `px > 200d MA` (band g = 0, **held fixed**) AND
`vol20 < max_vol`; rank by the scan.py composite with no vol tilt; hold the top n; weekly, t+1.

**Tuned parameters (2):** P1 `max_vol ∈ {0.30, 0.45, 0.60, 0.80, 1.00, OFF}`, P2 cost rung
`∈ {0, 5, 10, 15, 20, 25, 30}` bps. Panel, `n ∈ {10, 20, 40}` and the gross convention are
pre-registered reporting axes, printed at every point and never chosen on.

**The exposure control.** Dropping the cap enlarges the eligible set, so under idea 228's
`dg` convention (w = 1/n, exposure floats) the OFF arm is mechanically more invested. Every
cell is therefore also run under `rw` (w = 1/count_held, gross rebuilt to 1.00), which matches
the two caps on exposure so that only **selection** differs. Mean invested is reported for every
cell.

## The pre-registered pair: OFF − 0.60

| conv | cells | gap > 0 | mean gap | median | min | max | mean OOS gap | OOS gap > 0 |
|---|---|---|---|---|---|---|---|---|
| dg (exposure floats) | 63 | **63/63** | +0.1292 | +0.0855 | +0.0230 | +0.3667 | +0.0991 | 56/63 |
| rw (exposure matched) | 63 | **63/63** | **+0.1318** | +0.0882 | +0.0313 | +0.3777 | **+0.1063** | 56/63 |

The gap is positive at **every rung on every panel at every n**, and it **grows with the cost
rung** (U56 n=10: +0.105 at 0 bps → +0.146 at 30 bps), because the vol cap churns the book.

**It is not the cash channel.** Mean invested at 10 bps is 0.963 (OFF) vs 0.955 (0.60) on U56
n=20 — an 0.8 pp exposure difference that cannot carry a +0.055 Sharpe gap. Removing the
exposure difference entirely leaves the gap intact:

| panel | n | gap dg | gap rw | rw as share of dg |
|---|---|---|---|---|
| U56 | 10 / 20 / 40 | +0.1186 / +0.0547 / +0.0438 | +0.1178 / +0.0447 / +0.0409 | 99% / 82% / 93% |
| B136 | 10 / 20 / 40 | +0.0755 / +0.0342 / +0.0522 | +0.0778 / +0.0477 / +0.0596 | 103% / 139% / 114% |
| SMALL439 | 10 / 20 / 40 | +0.2213 / +0.2846 / +0.1837 | +0.2218 / +0.2966 / +0.1787 | 100% / 104% / 97% |

R1 confirmed, **R2 falsified** (the prediction was that matching exposure would halve the gap),
R3 half-confirmed: the small panel does carry the largest gap (+0.250 mean) but **none** of it is
exposure.

## What the corner costs: drawdown

The gap is a return effect bought with risk. Mean `MaxDD(OFF) − MaxDD(0.60)`:
**−3.45 pp** (U56 dg), **−3.90 pp** (B136 dg), **−3.49 pp** (SMALL439 dg) — i.e. the uncapped
book draws down **3–5 pp deeper** on every panel. At n = 20, 10 bps, OOS:

| panel | conv | OFF | 0.60 | SPY | RULES v2 | RULES v1 |
|---|---|---|---|---|---|---|
| U56 | dg | 21.07% / **1.171** / −25.37% | 19.22% / 1.168 / −23.98% | 15.45% / 0.882 / −33.72% | 1.285 | 0.747 |
| B136 | dg | 18.91% / **0.918** / −31.02% | 16.51% / 0.894 / −26.20% | 15.45% / 0.882 / −33.72% | 1.119 | 0.576 |
| SMALL439 | dg | 21.13% / **0.786** / −39.37% | 9.04% / 0.488 / −36.39% | 15.45% / 0.882 / −33.72% | 0.568 | 0.492 |

On U56 at idea 228's own default the whole OOS Sharpe gain is **+0.003** for 1.4 pp more
drawdown. The large gaps live on B136 n=40 (+0.068) and on the survivorship-biased small panel.

## The "corner" is a boundary of a mostly monotone ladder, not a peak

Full ladder at 10 bps, Sharpe (`.grid.csv` carries all 756 points):

| panel | n | 0.30 | 0.45 | 0.60 | 0.80 | 1.00 | OFF |
|---|---|---|---|---|---|---|---|
| U56 | 20 | 1.0242 | 1.0988 | 1.0922 | 1.1095 | 1.1289 | **1.1470** |
| B136 | 20 | 0.8541 | 0.8731 | 0.9588 | **1.0245** | 1.0010 | 0.9930 |
| SMALL439 | 20 | 0.3565 | 0.3306 | 0.4639 | 0.5708 | 0.5624 | **0.7486** |

OFF is the ladder argmax in **7 of 9** panel × n cells under each convention — B136 at n = 10
and n = 20 peaks at **0.80**, i.e. a *loose* cap beats no cap there. Out of sample OFF is the
argmax in **10 of 18** cells: U56 n = 20/40 prefers **0.45** OOS. So "switch the gate off" is the
right direction everywhere and the exact right level on two panels of three.

## Rule 8 (PROTOCOL 8): the corner does not need a selector

Parameters read on 2009–2016 only; 2017–2026 read once.

* **Pre-registered OFF arm:** OOS margin over the 0.60 arm is positive in **56 of 63** cells per
  convention, mean **+0.0991** (dg) / **+0.1063** (rw).
* **Selected arm (idea 228's procedure):** the IS chooser picks OFF in **62 of 63** (dg) and
  **61 of 63** (rw) cells, and its mean OOS margin is **+0.0931 / +0.1033** — *smaller* than the
  pre-registered arm's, with mean REGRET 0.0236 / 0.0142.

That is the queue's own test, answered: **the selected premium and the pre-registered premium
are the same number to within the selector's regret**, so idea 228's +0.1049 was not a selection
artefact. It was ideas 38/49 restated by a chooser that happened to be right.

## KEEP paths (both, all 756 points)

* **4a vs the live RULES v2: 0 of 756.** Every point fails on drawdown; the live book's −12%
  MaxDD is out of reach for a fully invested equity book.
* **4b vs SPY: 36 of 756**, and they are not the cap:

| panel | conv | 4b |
|---|---|---|
| U56 | dg | **34/126** |
| U56 | rw | **0/126** |
| B136 | dg / rw | 1/126 each (both at 0 bps only) |
| SMALL439 | dg / rw | **0/126** — idea 136's 17th reproduction |

At the protocol rung there are **6** passes and every cap contributes exactly **1 of its 6**
cells (0.30 through OFF alike), because all 6 are the same book: **U56, n = 40, dg**. Its
MaxDD is **−20.22%** against a 4b bar of −20.23% — it clears by **0.012 pp**, on a mean invested
of **0.876**. Matching exposure (rw) removes every U56 pass. So the 4b passes here are
idea 157's cash carve-out at a razor-thin drawdown margin, not a vol-gate result, and none is
proposable.

## Reconciliation with lane B (same queue item, independent script)

Every overlapping cell agrees, to the digits both runs published:

| cell (n = 20, 10 bps, full gross) | lane B | this lane |
|---|---|---|
| U56 dSharpe (OFF − 0.60) | +0.0547 | **+0.0547** |
| B136 dSharpe | +0.0342 | **+0.0342** |
| U56 dOOS | +0.0027 | **+0.0027** |
| B136 dOOS | +0.0247 | **+0.0247** |
| mean dSharpe over its cells | +0.1294 (21 cells) | **+0.1292** (63 cells, dg) |
| pre-registered OOS win rate | 88.1% (74/84) | **88.9%** (56/63) |
| highest-OOS 4b passer at 10 bps | U56 COMP n=40 cap ON: 12.95% / 1.1236 / −18.38%, OOS 1.2656 | **12.95% / 1.124 / −18.38%, OOS 1.266** |
| 4a | 0 / 840 | **0 / 756** |

The two runs are measuring the same object. Two things are carried across:

* **From this lane to lane B's reading:** the gap is not the cash channel. Lane B varied gross
  between the two *published levels* (0.75 and 1.00) but both arms de-gross alike; this lane
  matches exposure exactly (`rw`) and finds the gap is **103% of its de-grossed size**. The
  corner is selection, not exposure.
* **From lane B to this one, and it is the binding qualification:** the corner is measured here on
  idea 228's **un-tilted composite**. On `V1KEY`, the live RULES v1 key with its `1/sqrt(vol20)`
  tilt, lane B finds the same gap shrinks **7.9x** (+0.1345 → +0.0171) and a stationary block
  bootstrap cannot separate it from zero on B136 (P ≤ 0 = 0.334) or SMALL484 (0.361). **A vol
  gate and a vol rank-tilt spend the same information.** Everything below about "the vol clause
  costs +0.13" is therefore a statement about a book that has already thrown the tilt away.

## What the record should now say

Idea 228's line — *"all of the rule-8 premium is the vol-cap dial choosing OFF, i.e. the chooser
rediscovering ideas 38/49"* — should be upgraded from a **selection artefact** to a
**pre-registered fact**: on the un-tilted composite the `vol20 < 0.60` clause costs about
**+0.13 Sharpe**, at **+3–5 pp of drawdown**, on all three panels, at all seven rungs, and — this
lane's addition — **with the cash channel removed**. It is a real property of *that* book. On the
key the live rules actually use it is not separable from zero on two panels of three (lane B), and
it clears neither KEEP path here. RULES v2 (the live book) has no vol clause at all, so nothing
here proposes a change; between the two lanes this retires the clause's remaining defence rather
than proposing a replacement.

## Limits

* Survivorship: `universe_broad.json` and the small panel are current constituents,
  one-directional; the SMALL439 gap (+0.25) inherits it in full and is the largest number here.
* One book shape only (composite ranking, top-n, weekly, 200d gate at g = 0). The result is
  about the vol clause *inside that book*, not about volatility screening in general.
* Sharpe differences on overlapping samples; the OOS read is a single window, not a distribution.
* The cap ladder is not a random treatment — vol20 correlates with the composite's own ranking,
  so removing the cap changes which names rank as well as how many are eligible. The dg/rw pair
  separates exposure from selection, not selection from ranking.
