# Idea 110 — selection-vs-no-selection-as-the-real-question (lane B, 2026-09-07)

**Verdict: SPLIT.** The queue's question is answered **YES — idea 109's +0.055 survives
pre-registration** (positive in **100/100** random grids of the same shape, null mean **+0.0482**).
Two corrections follow, and the premium turns out to be **capital-irrelevant**: 4a **0/44**,
4b **+1/44**, and every selector arm sits **below the live book's OOS Sharpe**.

## Gates (run before any result was read)
| gate | value |
|---|---|
| G2 cost linearity vs `engine.backtest` @10 bps | **0.000e+00** |
| G3 metric identity `nm3` vs `engine.metrics` | **0.000e+00** |
| G1 reproduce idea 109's committed grid | S_sharpe **1.0483** (committed 1.048), S_null **0.9933** (0.993), premium **+0.0551** (+0.055), **44 cells** — max \|d\| **0.0003** |

## Design
Pool = every instrument's full range at fine step, spanning idea 109's committed values exactly
(sleeve 41, band 33, breadth 41, stop 32, crypto 41, gross 31 values) × 2 books × 2 panels
= **794 weight matrices × 2 cost rungs = 1,588 points, all reported** (`.pool.csv`, and every
point printed at 10 bps in `.console.txt`). 44 cells (u56 24, broad 20), identical to idea 109.
100 random grids, seed 20260907, each the null point plus (K−1) draws from the pool, K = the
committed grid size. **2 tuned params:** selector × overlay parameter. The randomisation is a
null-distribution device — no result is chosen by it.

New pre-registered control that idea 109 did not have: **S_rand**, the *exact* expected OOS
Sharpe of a uniform pick from the same grid. It splits the premium into
`premium_total = premium_skill (S_sharpe − S_rand) + premium_instr (S_rand − S_null)`.

## Results — the null distribution (100 random grids)
| statistic | null mean | sd | p05 | median | p95 | positive | COMMITTED | percentile |
|---|---|---|---|---|---|---|---|---|
| premium_total | **+0.0482** | 0.0049 | +0.0382 | +0.0495 | +0.0541 | **100/100** | **+0.0551** | **97** |
| premium_skill | **+0.0240** | 0.0077 | +0.0142 | +0.0221 | +0.0396 | **100/100** | +0.0378 | 92 |
| premium_instr | **+0.0242** | 0.0080 | +0.0091 | +0.0263 | +0.0338 | **100/100** | +0.0172 | 22 |
| premium_total, excl. crypto | +0.0360 | 0.0044 | +0.0280 | +0.0367 | +0.0406 | 100/100 | +0.0407 | 96 |

Selector levels: S_sharpe null mean **1.0415** (sd 0.0049), S_rand **1.0175**, S_null **0.9933**
(constant by construction).

## Hypotheses
- **H_SURVIVES PASS** — mean premium_total +0.0482 > 0, positive **100/100** (bar 75).
  Idea 109's headline is **not** an artefact of its hand-picked parameter values.
- **H_NOT_CHERRY FAIL** — committed grid at **percentile 97** (bar ≤ 95).
  **CORRECTION 1: idea 109's +0.055 is inflated ~13% by post-hoc value choice.** The
  pre-registered magnitude is **+0.048**, and excluding crypto **+0.036** (committed +0.041, p96).
- **H_SKILL PASS** — premium_skill positive **100/100**, null mean **+0.0240**.
  **CORRECTION 2: the attribution in idea 109's framing is wrong.** On its committed grid the
  argmax carries **68.7%** of the gap; pre-registered it is a **50/50 split** (skill +0.0240 vs
  instr +0.0242). The committed grid is simultaneously *high* on skill (p92) and *low* on
  instrument value (p22) — its values flatter the selector and understate the overlays.
  Half of "selection beats no-selection" is really "having an overlay at all beats not having one".
- **H_RANKIC PASS but instrument-signed** — within-cell spearman(IS Sharpe, OOS Sharpe) over the
  pool = **+0.3622** mean, positive in only **30/44** cells. By instrument: crypto +1.000 (monotone,
  short IS window), stop +0.744, sleeve +0.544, gross +0.270, breadth +0.022, **band −0.089**.
  Mechanism: the IC **rises with the cost rung** (10 bps u56 +0.172 / broad +0.286 → 25 bps +0.450 /
  +0.562) — what travels IS→OOS is turnover, not signal, so rule 8's argmax is largely a
  cost-persistence selector.

## Rule-8 walk-forward (OOS 2017-01-01→, IS-only choice) — mean over each panel's cells
| panel | bps | arm | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| u56 | 10 | S_sharpe | 14.94% | **1.2225** | −18.08% |
| u56 | 10 | S_rand | 13.94% | 1.1771 | −17.39% |
| u56 | 10 | S_null | 14.18% | 1.1504 | −18.08% |
| u56 | 10 | RULES v2 (live) | 10.49% | **1.3801** | −12.51% |
| u56 | 10 | RULES v1 | 7.19% | 0.6994 | −13.83% |
| u56 | 10 | SPY | 15.45% | 0.8820 | −33.72% |
| u56 | 25 | S_sharpe / S_null / v2 / SPY | 14.08 / 12.39 / 10.18 / 15.45% | 1.0936 / 1.0213 / **1.3428** / 0.8820 | −19.81 / −18.58 / −12.55 / −33.72% |
| broad | 10 | S_sharpe / S_null / v2 / SPY | 12.99 / 12.27 / 7.98 / 15.45% | 0.9858 / 0.9514 / **1.1185** / 0.8820 | −20.43 / −20.03 / −12.24 / −33.72% |
| broad | 25 | S_sharpe / S_null / v2 / SPY | 10.82 / 10.19 / 7.64 / 15.45% | 0.8475 / 0.8129 / **1.0740** / 0.8820 | −20.67 / −20.36 / −12.28 / −33.72% |

**RULES v2, the live book, has the highest OOS Sharpe in 4/4 (panel × rung) — above every
selector arm, S_sharpe included — while giving up 3.0–5.0 pp of OOS CAGR.** No selector arm beats
SPY's OOS CAGR anywhere.

## KEEP paths
- **4a vs RULES v2: 0/44 picks, and 0/1,588 pool points.** Nothing in this instrument set beats
  the live book on both halves' Sharpe with no worse MaxDD, at any parameter value.
- 4a vs RULES v1 (idea 109's baseline): 17/44 picks, 730/1,588 pool points.
- **4b: S_sharpe 20/44 full and 22/44 OOS-only, S_null 19/44 and 19/44 — the selector buys +1 of 44.**
  Across the 100 random grids S_sharpe's 4b count is 20.98/44 (min 15, max 26).
- No new KEEP; no memo; RULES unchanged.

## Committed-grid premium by instrument (mean over its cells)
| instrument | premium_total | premium_skill | premium_instr | regret | cells |
|---|---|---|---|---|---|
| crypto | +0.1982 | +0.1008 | +0.0974 | 0.0000 | 4 |
| sleeve | +0.1046 | +0.1238 | −0.0192 | −0.0188 | 8 |
| band | +0.0571 | +0.0039 | +0.0532 | −0.0276 | 8 |
| breadth | +0.0334 | +0.0004 | +0.0329 | −0.0258 | 8 |
| stop | +0.0077 | +0.0289 | −0.0212 | −0.0098 | 8 |
| gross | +0.0010 | +0.0008 | +0.0002 | −0.0005 | 8 |

Two of six instruments (crypto, sleeve) carry the whole premium; the gross lever contributes
**+0.0010**. Cell-by-cell, S_sharpe beats S_null in 30/44 on the committed grid (27.5/44 in the
null) and beats S_rand in 35/44 (33.0/44).

## Caveats
- **Crypto**: BTC-USD starts 2014-09-17, so that instrument's IS window holds ~2 years — it has
  rho = 1.000 and the largest premium. Every headline is reported with and without it.
- **Survivorship**: both panels are current constituents; the bias is identical across selectors,
  which is what this run compares.
- The null distribution's spread (sd 0.005 on premium_total) is small because S_null is a
  constant and the 44 cells are shared — this is a test of the *grid values*, not of the panels.

## What the evidence supports
1. Report the selection premium **against S_rand**, not only against the no-overlay null — half of
   idea 109's gap is instrument value, not selection.
2. Quote **+0.048 (excl. crypto +0.036)**, the pre-registered magnitude, not +0.055.
3. Rule 8's argmax is worth roughly **+0.024 of OOS Sharpe** and **+1 of 44** 4b passes; it does not
   move the 4a picture at all against the live book.

Files: `.py`, `.console.txt`, `.pool.csv` (1,588 points), `.picks.csv`, `.null.csv` (100 grids),
`.rankic.csv`, `.walkforward.csv`.
