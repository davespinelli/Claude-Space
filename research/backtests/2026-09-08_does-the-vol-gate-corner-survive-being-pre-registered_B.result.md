# Idea 232 — does-the-vol-gate-corner-survive-being-pre-registered (lane B, 2026-09-08)

**Script:** `2026-09-08_does-the-vol-gate-corner-survive-being-pre-registered_B.py`
**Grid:** 3 panels x 2 ranking keys x 2 gross x 2 gate arms x 5 n x 7 rungs = **840 points, all reported**
(`.grid.csv`, `.headline.csv`, `.walkforward.csv`, `.bootstrap.csv`, `.keep.csv`, `.console.txt`)

## The question

Idea 228's rule-8 walk-forward found a positive selector premium (+0.0177 mean OOS Sharpe,
59.5% wins) and **all of it was the vol-cap dial choosing `max_vol` = off** (+0.1049 mean,
85.7% wins). That is a *corner* of a monotone ladder — idea 173's signature of a selector
artefact. The queue's own conditional: *if the corner is real it should not need a selector.*
So this run pre-registers the two arms and never chooses between them:

    GATE_ON   eligible = (px > 200d MA) AND (vol20 < 0.60)
    GATE_OFF  eligible = (px > 200d MA)

200d gate held fixed at g = 0.00. Tuned parameters: n and the cost rung, nothing else.

## Pre-checks

- **[a]** live RULES v1 on U56 6.5% / 0.665 / -13.8% (published 0.666); idea 2's CAND20 shape 12.7% / 1.092 / -18.3%.
- **[b1] the premise reproduces.** Idea 228's committed `.grid.csv`, **the whole V dial, 168 rows**
  (3 panels x 8 thresholds x 7 rungs): max |published − reproduced| **1.42e-4 Sharpe**, 3.42e-5 CAGR,
  3.01e-7 MaxDD. By panel: B136 3.3e-16, SMALL484 2.5e-8, U56 1.4e-4 (worst cell U56 V=0.3, turnover
  14.3049 vs 14.2992 — idea 228 hand-rolled its rebalance loop, this run uses `engine.backtest`;
  the two differ only in first-bar handling).
- **[b2] a record discrepancy, priced.** Idea 228's `U56 n=20 max_vol=off` and idea 256's
  `u56 n=20 max_vol=off g=0.75` are quoted as the same corner. They are **three construction changes
  apart** and are **not the same book**:

  | build | CAGR | Sharpe | MaxDD | H1/H2 | OOS | turn/yr |
  |---|---|---|---|---|---|---|
  | idea 256 verbatim (V1KEY, NORM, g=0.75) | 10.76% | 0.9947 | -19.49% | 1.039/0.968 | 1.0356 | 11.58 |
  | ... same but RAW gross/n | 10.54% | 1.0270 | -17.89% | 1.051/1.014 | 1.0855 | 10.65 |
  | ... same but COMP key, NORM | 14.36% | 1.1084 | -21.37% | 1.195/1.055 | 1.1199 | 10.33 |
  | idea 228 shape (COMP, RAW, g=0.75) | 14.27% | **1.1469** | -19.39% | 1.216/1.104 | 1.1707 | 9.17 |

  Idea 256's row reproduces on its own construction (|dSharpe| 1.3e-3, |dOOS| 2.3e-3; MaxDD and H1
  agree to 4 dp). **The construction spread is +0.1522 of Sharpe — 1.5x idea 228's entire +0.1049
  premium** — so the ranking key was carried into the grid as a second pre-registered axis
  (COMP = idea 228's un-tilted composite; V1KEY = `score(vol_scale=True)`, the LIVE RULES v1 key),
  as was gross at both published levels. Neither is chosen; every level is reported.
- **[c]** cost identity 0.000e+00; GATE_OFF is byte-identical to idea 228's V=5.00 arm (max|d| 0.0).
- **[d]** the gate binds, and how hard is the whole story of Result 2. Mean names removed from the
  trend-eligible set, and the share of rebalance weeks in which the top-20 book differs:

  | panel | trend-eligible | after gate | share cut | weeks top-20 differs | names swapped |
  |---|---|---|---|---|---|
  | U56 | 38.41 | 37.45 | **3.21%** | 52.8% | 0.78 |
  | B136 | 93.18 | 91.44 | **2.63%** | 53.1% | 0.99 |
  | SMALL484 | 186.31 | 148.34 | **20.65%** | 99.4% | 7.95 |
- **[d2]** the one deviation from idea 228, priced: idea 228 ranks every column, so on SMALL484 **SPY
  itself is holdable**. This run excludes it. **The correction costs nothing** — GATE_OFF n=20 g=1.00
  at 10 bps is 19.26% / 0.7623 / -43.90%, halves 1.0603/0.5930, either way (SPY never enters the
  top 20 of that panel).

## Result 1 — the corner does NOT need a selector (the queue's conditional: **HIT**)

Pre-registered pair, n = 20, g = 1.00, COMP key, every panel x every rung:

| panel | ON | OFF | dSharpe | ON OOS | OFF OOS | dOOS | dCAGR | dMaxDD |
|---|---|---|---|---|---|---|---|---|
| U56 @10 | 1.0922 | 1.1470 | **+0.0547** | 1.1683 | 1.1710 | +0.0027 | +2.18 pp | **-1.39 pp** |
| B136 @10 | 0.9588 | 0.9930 | **+0.0342** | 0.8937 | 0.9184 | +0.0247 | +2.12 pp | **-4.83 pp** |
| SMALL484 @10 | 0.4967 | 0.7623 | **+0.2657** | 0.5116 | 0.7408 | +0.2292 | +10.21 pp | **-8.68 pp** |

**dSharpe > 0 in 21 of 21 (panel x rung) cells, mean +0.1294; dOOS > 0 in 19 of 21, mean +0.0988** —
which lands on idea 228's published chooser premium of +0.1049 with no chooser in the loop.

Rule 8 (params on 2009-2016, 2017-2026 read once, 84 cells, every selector fixed in advance):

| arm | OOS mean vs do-nothing | wins |
|---|---|---|
| **A1 pre-registered GATE_OFF (no selector)** | **+0.0621** | **74/84 (88.1%)** |
| S1 IS-argmax over (arm, n) — idea 228's chooser rebuilt | +0.0978 | 56/84 (66.7%) |
| S2 IS-argmax over n, arm pinned ON (chooser denied the corner) | +0.0659 | 50/84 |
| S3 random (arm, n), seed fixed in advance | +0.0272 | 47/84 |

S1's mean regret vs the OOS oracle is +0.0897 and it picks GATE_OFF in 73 of 84 cells. **The
pre-registered arm wins more consistently (88.1%) than the chooser that finds it (66.7%)** — the
premium is the corner, not the selection. This is a rare non-negative selector result in the
record, and it is non-negative because the thing selected was pre-registrable all along.

## Result 2 — but the corner is NOT a vol result (the mechanism)

The gate is redundant with the rank tilt. Over all 420 (gross x panel x n x rung) cells per key:

| key | mean dSharpe | sd | min | max | share > 0 | mean dOOS | share > 0 |
|---|---|---|---|---|---|---|---|
| COMP (idea 228's un-tilted composite) | **+0.1345** | 0.0916 | +0.0225 | +0.3638 | **100%** | +0.1117 | 90.5% |
| V1KEY (the LIVE RULES v1 key, `/sqrt(vol20)`) | **+0.0171** | 0.0162 | -0.0063 | +0.0647 | 90.5% | +0.0185 | 82.9% |

**7.9x smaller on the live key.** By panel at 10 bps (COMP -> V1KEY): SMALL484 +0.2158 -> **+0.0118**
(18x), U56 +0.0911 -> +0.0270, B136 +0.0595 -> +0.0089. Stationary block bootstrap on the paired
daily difference (2,000 draws, mean block 21d, seed 232001), P(dSharpe <= 0):

| key | U56 | B136 | SMALL484 |
|---|---|---|---|
| COMP | 0.005 (OOS 0.095) | 0.034 (OOS 0.093) | 0.006 (OOS 0.033) |
| V1KEY | 0.072 (OOS 0.067) | **0.334** (OOS 0.335) | **0.361** (OOS 0.440) |

On the key the live book actually uses, the corner is **indistinguishable from zero on 2 of 3
panels**. A vol *gate* and a 1/sqrt(vol) rank *tilt* spend the same information; idea 228 measured
the corner on the one book that had thrown the tilt away.

And it is bought with drawdown: **dMaxDD < 0 in 372 of 420 cells, mean -2.95 pp** (at the headline
n=20/g=1.00: 21 of 21 worse, mean -4.74 pp).

## Result 3 — both KEEP paths, all 840 points

- **4a: 0 / 840** against the live RULES v2 (118/840 against the retired RULES v1).
- **4b: 82 / 840** — GATE_OFF 45/420, GATE_ON **37/420**. At PROTOCOL's own 10 bps, 12 of 120 pass
  (GATE_OFF 7, GATE_ON 5; COMP 9, V1KEY 3). Binding bars at 10 bps: DD 84, H2 78, OOS 68, H1 51, CAGR 50.
- The **highest-OOS 4b passer at 10 bps is a GATE_ON point** (COMP g=1.00 U56 n=40: 12.95% / 1.1236 /
  -18.38%, OOS 1.2656). The corner does not own the 4b frontier; it shifts a book already on it.
- A1 beats SPY OOS in 35/84 and **RULES v2 OOS in 10/84**; A0 beats SPY OOS in 32/84 and RULES v2 in 0/84.

## Verdict

**HIT on the queue's conditional, KILL as a rules change.**

The corner survives pre-registration cleanly — it needs no selector, and the pre-registered arm is
*more* reliable out of sample than idea 228's chooser (88.1% vs 66.7% of cells). But it is not the
vol gate doing the work: on the live vol-scaled ranking key the effect shrinks 7.9x and the bootstrap
cannot separate it from zero on B136 and SMALL484. It also deepens drawdown in 372 of 420 cells, it
clears 4a in 0 of 840, and its 4b passers are shared with GATE_ON and are known record objects
(ideas 2/38/49/256). No memo, no RULES wording.

**Follow-ups for the queue:** (i) the three-way construction discrepancy behind one quoted corner
(+0.1522 of Sharpe, 1.5x the premium it was used to explain) is a record-wide auditing question;
(ii) gate-vs-tilt redundancy should be back-filled over every published `max_vol` argmax, since each
one was quoted on a single ranking key.

**Survivorship:** all three panels are current constituents, one-directional. A vol gate is exactly
the clause such a panel flatters — the names that blew up on high vol are not in the list — so
GATE_OFF's edge here is an **upper bound**.
