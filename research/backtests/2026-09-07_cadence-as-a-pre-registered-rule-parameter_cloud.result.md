# Idea 107 — cadence as a pre-registered RULES parameter (cloud, 2026-09-07)

**VERDICT: KILL the pre-registration.** No cadence can be fixed in RULES: the modal OOS-Sharpe
winner is M at only **43%** of cells (bar 75%), the winner **changes with the cost rung** (D 9/28 at
0 bps → 0/28 at 50 bps), it **flips by panel** (M on U56/B136/B80held, W on SMALL439), and it
**flips by KEEP path** (M wins on Sharpe, W passes 4b most). Cadence stays a per-idea reported dial.
Two upstream claims are resolved against each other. Rules unchanged; no new KEEP.
`2026-09-07_cadence-as-a-pre-registered-rule-parameter_cloud.py`

Menu: 7 books (N10/N20/N40, B03R/B12R band-respread, V2DG = live shape, EWALL) at the live gross
0.75 × 4 cadences {D,W,M,Q} × 4 panels {U56, B136, B80held, SMALL439} = 112 cells × 7 cost rungs.
Gates before any result was read: cost identity vs `engine.backtest` at 10 bps **0.000e+00**;
numpy metrics vs `engine.metrics` **0.000e+00**.

## H_CLEAN — PASS. Idea 38's trading-day index has landed.

| panel | rows | weekend rows | all-zero-return days | max calendar gap |
|---|---|---|---|---|
| U56 / B136 / B80held | 4699 | **0** | **0** | 5 d |
| SMALL439 | 4194 | **0** | **0** | 5 d |

The D arm no longer rebalances on weekend zero-return rows, so the D-vs-W gap below is a pure
schedule effect and the queue's second question is answered: **the re-measurement is now valid.**

## The D-vs-W gap, cleanly measured (10 bps, 28 panel×book cells)

- D − W Sharpe: mean **−0.0660**, median −0.0375; **D wins 4/28**.
- D turnover **16.0x/yr** vs W **7.5x** (2.1x more) → the D schedule alone costs **0.84 pp of
  CAGR/yr** at 10 bps.
- Idea 101's "4b fails at daily" is **CONFIRMED and now attributable**: D takes 3/28 4b passes vs
  W's 5/28, and the gap is the cost of the schedule, not the calendar.

## H_MONTHLY — the two upstream claims resolve in idea 3's favour

| claim | as stated | measured here |
|---|---|---|
| idea 101: M dominates W on CAGR, Sharpe **and** MaxDD | 8/8 = 100% | **2/28 = 7%** (U56 1/7, B136 0/7, B80held 0/7, SMALL439 1/7) — **KILLED** |
| idea 3: monthly buys 3–6 pp of extra drawdown | 3–6 pp | **M is worse on DD in 22/28 cells, by 3.94 pp on average** (worst 12.76 pp) — **REPRODUCED, in band** |

M does win Sharpe 18/28 (+0.0473 mean) and CAGR 22/28 (+1.08% mean). The mechanism is now explicit:
**monthly buys Sharpe and CAGR by paying drawdown**, which is precisely why it cannot be a constant —
the 4b path caps drawdown at 60% of SPY's and therefore prefers W.

## H_DOMINANT — FAIL (43%, bar 75%)

OOS-Sharpe argmax cadence at 10 bps: **D 5/28 (18%), W 3/28 (11%), M 12/28 (43%), Q 8/28 (29%)**.
And the answer moves with the cost assumption, so a fixed value would be pricing-dependent:

| rung | D | W | M | Q |
|---|---|---|---|---|
| 0 bps | 9 | 4 | 8 | 7 |
| 10 bps | 5 | 3 | 12 | 8 |
| 25 bps | 1 | 3 | 15 | 9 |
| 50 bps | 0 | 1 | 17 | 10 |

## H_STABLE — PASS (but it does not rescue the proposal)

IS-argmax agrees with OOS-argmax **14/28 = 50%** at the anchor (chance 25%), 45% over all rungs, so
cadence *is* partly knowable in advance. Policy comparison, anchor rung, 28 cells:

| policy | OOS Sharpe | OOS CAGR | OOS MaxDD | regret | > SPY |
|---|---|---|---|---|---|
| fixed D | 0.8614 | 9.81% | −22.80% | 0.1243 | 16/28 |
| fixed W (live) | 0.9177 | 10.90% | −22.02% | 0.0679 | 17/28 |
| **fixed M** | **0.9600** | 12.01% | **−25.02%** | 0.0257 | 21/28 |
| fixed Q | 0.8357 | 10.63% | −28.34% | 0.1500 | 14/28 |
| rule 8 (per-cell IS pick) | 0.9431 | — | — | 0.0425 | 19/28 |
| ORACLE (OOS) | 0.9857 | — | — | 0.0000 | 21/28 |

A **fixed M beats rule 8's own per-cell choice** (0.9600 vs 0.9431) — selection destroys value here —
but it costs **3.0 pp of OOS drawdown** against the live W, and it is the wrong answer on the small
panel (best fixed: U56 M 1.218, B136 M 1.081, B80held M 0.989, **SMALL439 W 0.567**).

## Both KEEP paths, 112 cells at 10 bps

- **4a: 0/112.** No cadence beats the live RULES v2 book in both halves without a worse MaxDD.
- **4b: 12/112** — U56 8, B136 3, B80held 1, SMALL439 0.
- **4b by cadence: D 3/28, W 5/28, M 4/28, Q 0/28.** The live weekly cadence carries the most 4b
  passes even though monthly carries the higher Sharpe: the DD ceiling is what separates them.

## What PROTOCOL should say

Cadence is **not** a constant to pre-register. It is a dial whose best value depends on the cost
rung, the panel and the KEEP path being argued, and a run that quotes one cadence is quoting a
choice, not a fact. The reportable clause: **every claim states its cadence, and any Sharpe
comparison across cadences states the drawdown it bought** (mean +3.94 pp W→M here).

## Caveats

SURVIVORSHIP: all four panels are current-constituent lists; SMALL439 (483 sub-$2B names minus the
44 with `max_1d_move ≥ 1.0`) is most exposed, and its IS window is 2011–2016 rather than 2009–2016.
Only the four cadences `engine.rebalance_mask` implements (D/W/M/Q) are tested; intermediate
schedules (2W, 6W) are untested here — idea 348 holds that question.
