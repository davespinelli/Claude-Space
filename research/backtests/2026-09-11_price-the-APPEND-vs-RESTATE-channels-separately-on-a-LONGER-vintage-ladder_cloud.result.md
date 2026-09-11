# Idea 519 — price the APPEND vs RESTATE channels separately

**2026-09-11, cloud lane. Verdict: ANSWERED / RESTATEMENT KILLED as a source of verdict risk at the
observed envelope.** The restatement channel flips **0 of 768** 4b verdicts and **0 of 768** 4a
verdicts at idea 514's observed 3.000e-04 bound, under both a gentle and an adversarial noise
shape, against the append channel's **3 of 192 (1.56%)**. No RULES change, no book promoted, no
PROTOCOL edit. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

Script `2026-09-11_price-the-APPEND-vs-RESTATE-channels-separately-on-a-LONGER-vintage-ladder_cloud.py`.
Artefacts: `.draws.csv` (3,840 rows), `.picks.csv` (240), `.fliprates.csv`, `.pickstability.csv`,
`.console.txt`.

## Gates (all printed before any result was read)
| gate | got | bar | |
|---|---|---|---|
| G1 `fast_backtest` == `engine.backtest` (U56 BAND03 @10bps) | 6.94e-18 | 1e-12 | PASS |
| G1b engine NaN rows all inside the discarded 260-row warm-up | row 3 | < 260 | PASS |
| G2 ε=0 reproduces the panel EXACTLY, NaN mask preserved | 0 | 0 exact | PASS |
| G3 realised IID envelope == requested 3.000e-04 | 2.99999e-4 | ≤ 3e-4 | PASS |
| G4 same (envelope, draw) seed is bit-for-bit reproducible | 0 | 0 exact | PASS |
| G4b `seed_of` is crc32-based, stable **across interpreters** | 1026344283 | pinned | PASS |
| G4c draw 1 differs from draw 0 (seeds are not constant) | 3.65 | > 0 | PASS |
| G5 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | 0 | 0 exact | PASS |
| G6 BLOCK leaves within-month returns untouched | 2.22e-16 | 1e-15 | PASS |

Two gates failed on first execution and were corrected before any number was read. G2/G4 used
`np.abs(...).max()` on panels that carry NaN cells, so both returned NaN. Fixing them surfaced a
**real reproducibility bug**: the draw seed was `hash((shape, eps, draw))`, and Python's `str`
hash is salted per interpreter (`PYTHONHASHSEED`), so every re-run of this script on a fresh
process would have drawn a *different* set of panels while claiming to be seeded. The seed is now
`crc32` of a canonical string, and **G4b pins the actual value** so the bug cannot return silently.

## Design
2 panels (U56, B136) × 8 committed book families × gross {0.75, 1.00} = **32 books**, each run on
**5 envelopes × 24 draws** = 3,840 book-runs at 10 bps. Two tuned parameters and no more:
**ENVELOPE** (shape, width) and **DRAWS** (nested 6/12/24, so it is a convergence report, not a
second grid). Every one of the 15 (envelope, draws) points is reported.

The restatement model multiplies every cell — the SPY benchmark column included, since SPY is
restated by the same vendor in the same file — by (1+u):
- **IID ε**: u ~ U(−ε, ε) independent per (day, ticker). The **adversarial** shape: independent
  cell moves inject noise into *every* daily return, the worst case for a Sharpe/CAGR verdict.
- **BLOCK ε**: one u per (ticker, calendar month), flat across the month. The **gentle** shape:
  moves price levels, leaves within-month returns untouched (G6), and is closer to how a real
  restatement — a corrected split or dividend factor — actually lands.

**This test is strictly harsher than the restatement it models.** Idea 514 measured
max |d| = 3.000e-04 over 23,055 cells; this run applies a draw of that magnitude to **every**
cell of the panel, where the real vintage had most cells unchanged. The perturbation mass here
exceeds the observed restatement by orders of magnitude, which is what makes a zero-flip result
meaningful rather than under-powered.

## Result 1 — flip rates, all 15 points
| envelope | draws | n | 4a flips | 4b flips | max abs ΔSharpe | max abs ΔCAGR | max abs ΔMaxDD |
|---|---|---|---|---|---|---|---|
| IID 1e-04 | 24 | 768 | 0 (0.00%) | **0 (0.00%)** | 0.0110 | 0.364% | 0.488% |
| **IID 3e-04 (observed)** | 24 | 768 | 0 (0.00%) | **0 (0.00%)** | 0.0260 | 0.813% | 1.611% |
| IID 1e-03 | 24 | 768 | 0 (0.00%) | 3 (0.39%) | 0.0292 | 0.978% | 2.838% |
| IID 3e-03 | 24 | 768 | 0 (0.00%) | 15 (1.95%) | 0.0833 | 2.594% | 4.062% |
| **BLOCK 3e-04 (observed)** | 24 | 768 | 0 (0.00%) | **0 (0.00%)** | 0.0173 | 0.492% | 1.276% |

(6- and 12-draw rows are in `.fliprates.csv`; every zero above is zero at all three draw counts.)

## Result 2 — APPEND vs RESTATE, side by side
| channel | flips | rate |
|---|---|---|
| **APPEND** (idea 514's truncation ladder) | 3 / 192 | **1.56%** |
| **RESTATE**, IID @3.000e-04, 24 draws (4b) | 0 / 768 | **0.00%** |
| **RESTATE**, BLOCK @3.000e-04, 24 draws (4b) | 0 / 768 | **0.00%** |

**The two channels are not comparable in size: appending days moves verdicts, restating cells does
not.** The restatement envelope would have to be **~3× the observed bound before a single 4b
verdict moves** (first flip at ε=1e-3) and **~10×** before it matches the append channel's rate
(1.95% at ε=3e-3). Idea 514's worry about the unpriced restatement channel is retired; its
truncation ladder was measuring the channel that actually matters.

## Result 3 — which books flip, and in which direction
Every 4b flip in the entire 3,840-row grid is listed here:
- ε=1e-3: B136 EWELIG@0.75 × 3 draws (a 4b **passer** → fail).
- ε=3e-3: B136 EWELIG@0.75 × 11 (pass→fail); B136 BAND03_M@1.00 × 1, B136 CAND20@0.75 × 2,
  U56 CAND10@0.75 × 1 (all fail→**pass**).

The instability is **concentrated in one book**: B136 EWELIG@0.75 accounts for 14 of the 15 flips
at ε≥1e-3 and is a knife-edge 4b passer. This is a property of that book's margin, not of the
panel — which is the same lesson idea 691 records for the CAGR floor on the same day.

## Result 4 — PROTOCOL 8 walk-forward, run on every restated panel
The rule-8 pick is chosen on 2008–2016 **only**, on each restated panel, and evaluated on
2017–2026 untouched. **The pick never moves: 0/24 flips at every envelope on both panels.**

| panel | pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| U56 | BAND08 @ g1.00 | 12.00% | 1.162 | −19.05% |
| U56 — RULES v2 baseline | | 9.45% | 1.275 | −12.05% |
| U56 — SPY | | 15.24% | 0.872 | −33.72% |
| B136 | BAND08 @ g1.00 | 11.17% | 1.108 | −19.50% |
| B136 — RULES v2 baseline | | 7.98% | 1.119 | −12.24% |
| B136 — SPY | | 15.45% | 0.882 | −33.72% |

Across all 240 restated panels the pick's OOS CAGR stays inside [11.86%, 12.17%] (U56) and
[11.03%, 11.24%] (B136) even at ε=3e-3, ten times the observed envelope. Nothing is promoted on
this: the pick is idea 691's BAND08@g1.00, whose 4b pass is bought with exposure (it fails on the
CAGR floor alone at the live gross 0.75).

## Caveats that limit what this proves
1. **The 4a zero is low-power.** 0 of 32 books pass 4a unperturbed on either panel, so "4a never
   flips" mostly says a fail→pass flip never happened; it is not evidence that 4a passes are
   stable, because there are none to destabilise. The 4b zero **is** powered: 7 of 32 books pass
   unperturbed, so flips could and at larger ε did go both ways.
2. **Dense-small, not sparse-large.** The model applies a small move to every cell. A restatement
   that rewrites *few* cells by a *large* amount (a botched split factor on one ticker) is a
   different corner and is not tested here. Idea 514 reported the envelope but not the sparsity.
3. **Survivorship (PROTOCOL 9).** U56 and B136 are current constituents; every level above is
   biased upward. The claim made is a within-panel flip rate, which survivorship biases far less
   than a level, but no level here is a tradeable estimate.

## What this changes
Stop treating the restatement channel as an unpriced risk to published verdicts — at the observed
envelope it is measurably zero under both a gentle and an adversarial noise shape, and the append
channel is 1.56%. Vintage-stability effort belongs on **append** (idea 517's common-last-date
truncation), not on restatement.
