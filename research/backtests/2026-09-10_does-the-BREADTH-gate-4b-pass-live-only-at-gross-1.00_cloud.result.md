# Idea 585 — does the BREADTH gate's 4b pass live only at gross 1.00?

**ANSWER: NO. The premise is KILLED. The 4b pass is a CONTIGUOUS BAND in gross, 7 rungs wide on
U56 and 6 on B136, not the single point idea 581 happened to publish — and the band is created by
the GATE, not by the exposure dial.** The U56 book `BREADTH-DG q=0.20` accordingly upgrades from
PARK to **KEEP-candidate on PROTOCOL path 4b**; the B136 book stays PARK (its rule-8 pick is
selection-convention dependent). No RULES change; RULES.md, scan.py, bot.py, baseline.py untouched.

Grid: 2 panels x 4 dials q x 17 gross rungs (0.20..1.00 step 0.05) = **136 clause books** plus
**34 gate-less EWall controls**, all 170 committed to `.grid.csv`. 10 bps, weekly, t+1.
Two tuned parameters only: `q` and `g`.

## Gates (pre-registered, printed before any hypothesis number) — ALL PASS
- **G1** `fast_bt` vs `engine.backtest` on 4 books: **1.388e-17** (U56 EWall and BREADTH-DG),
  **2.776e-17 / 2.082e-17** (B136). `engine.backtest` emits NaN on 2 warm-up rows where panel
  columns are not yet priced; both are before the scored window and are reported, not hidden.
- **G2** the gate's firing path is gross-invariant: `max|W(g=.5)/.5 − W(g=1)/1| = **0.000e+00**`,
  i.e. `g` is a pure exposure dial and cannot change *when* the gate fires.

## Part A — the admissible 4b band (all 136 books, nothing dropped)

| panel | q | fire rate | 4b band in g | rungs | shape |
|---|---|---|---|---|---|
| U56 | 0.10 | 8.2% | [0.70, 0.80] | 3/17 | contiguous |
| U56 | **0.20** | 14.3% | **[0.70, 1.00]** | **7/17** | contiguous |
| U56 | 0.35 | 24.6% | [0.90, 1.00] | 3/17 | contiguous |
| U56 | 0.50 | 40.0% | none | 0/17 | — (H1 fails at every rung) |
| U56 | **EWall control (no gate)** | 0% | [0.65, 0.65] | **1/17** | — |
| B136 | 0.10 | 8.2% | [0.70, 0.70] | 1/17 | contiguous |
| B136 | **0.20** | 14.6% | **[0.75, 1.00]** | **6/17** | contiguous |
| B136 | 0.35 | 27.5% | none | 0/17 | — (H2 fails at every rung) |
| B136 | 0.50 | 43.9% | none | 0/17 | — (H1 fails at every rung) |
| B136 | **EWall control (no gate)** | 0% | none | **0/17** | — |

U56 4b passes at **13/68** (q,g) cells and 4a at **0/68**; B136 4b at **7/68**, 4a at **8/68**
(the 4a passes are all at g ≤ 0.55, where the book is too small to clear 4b's CAGR floor).

**The band is bracketed by the two return-side bars, and which one binds is fully determined by g:**
below the band every rung fails on the **4b CAGR floor** (70% of SPY); above it — at q = 0.10 —
every rung fails on the **DD cap** (60% of SPY's MaxDD). At q = 0.20 the DD cap never binds up to
g = 1.00, which is why that dial has the widest band.

**The gate is what creates the band.** The gate-less equal-weight control at matched gross clears
4b at **1 of 17** rungs on U56 (only g = 0.65) and **0 of 17** on B136 — its whole ladder fails on
CAGR below and on drawdown above. Turning the gate on widens the U56 window from 1 rung to 7.

## Part A2 — idea 581's own cell, every rung (U56, q = 0.20)

| g | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|---|---|---|---|
| 0.20 | 3.13% | 1.255 | −3.48% | 1.181 | 1.358 | 3.18% | 1.457 | −2.95% | fail (CAGR) |
| 0.50 | 7.90% | 1.256 | −8.52% | 1.184 | 1.357 | 8.04% | 1.456 | −7.26% | fail (CAGR) |
| 0.65 | 10.31% | 1.256 | −10.97% | 1.185 | 1.356 | 10.50% | 1.455 | −9.37% | fail (CAGR) |
| **0.70** | 11.12% | 1.256 | −11.77% | 1.185 | 1.356 | 11.33% | 1.455 | −10.07% | **PASS** |
| **0.75** | 11.92% | 1.256 | −12.57% | 1.186 | 1.356 | 12.16% | 1.455 | −10.76% | **PASS** |
| **0.85** | 13.55% | 1.256 | −14.15% | 1.186 | 1.355 | 13.83% | 1.454 | −12.13% | **PASS** |
| **1.00** | 15.99% | 1.257 | −16.48% | 1.187 | 1.354 | 16.35% | 1.453 | −14.16% | **PASS** |

(SPY on U56: 15.15% / 0.886 / −33.72%, halves 0.959 / 0.826, OOS 15.32% / 0.876 / −33.72%.
RULES v2: 8.63% / 1.202 / −12.05%, halves 1.231 / 1.180, OOS 9.48% / 1.279 / −12.05%.
Gate-less EWall at g = 1.00: 17.69% / 1.122 / −29.18%, 4b FAILS on DD.)

**Note on the reconciliation idea 585 asked for:** the 2026-09-09 KILL run's "same family at
g = 0.75" does *not* reproduce here — at (q = 0.20, g = 0.75) 4b **passes on both panels**. The
disagreement between the two prior runs is therefore not the gross dial alone; it is the (q, g)
pair, and only q ∈ {0.10, 0.35, 0.50} is fragile in g.

## Part B — rule 8 (PROTOCOL 8). (q, g) chosen on 2009–2016 ONLY; 2017–2026 read once

| panel | convention | pool | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | SPY OOS | RULES v2 OOS | full 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 | S1 max IS Sharpe | 68 | q .20, **g 1.00** | **16.35%** | **1.453** | **−14.16%** | 15.32% / 0.876 / −33.72% | 9.48% / 1.279 / −12.05% | **PASS** |
| U56 | S2 IS-4b screen | 4 | q .20, **g 0.75** | 12.16% | **1.455** | −10.76% | same | same | **PASS** |
| B136 | S1 max IS Sharpe | 68 | q .20, **g 1.00** | 12.58% | **1.155** | −15.32% | 15.45% / 0.882 / −33.72% | 7.98% / 1.119 / −12.24% | **PASS** |
| B136 | S2 IS-4b screen | 1 | q .20, **g 0.60** | 7.53% | 1.159 | −9.40% | same | same | **FAIL (CAGR)** |

Both conventions pick **q = 0.20** on both panels, and the U56 pick clears 4b under either. The
B136 S2 pick lands one rung below its own band and fails the CAGR floor — the one genuine weakness.

## Part C — is the verdict a gross artefact? (margins vs g, ρ = ±1.000 by construction)

Sharpe is flat in g (U56 1.255 → 1.257; B136 1.134 → 1.136, ρ +1.000 on a 0.002 range): with
de-grossed cash held at 0%, `g` scales CAGR and MaxDD together and leaves the risk-adjusted number
alone. So all three **Sharpe** legs of 4b (H1 +0.222→+0.229, H2 +0.532→+0.529, OOS +0.581→+0.578
on U56) are effectively **g-invariant and clear by wide margins at every rung**. Only the two
level legs move: the CAGR margin goes −0.075 → +0.054 and the DD margin +0.168 → +0.038 across the
ladder. **The 4b verdict is a level question, not a risk-adjusted one, and the band is where the
two level bars overlap.**

## Verdict

**PREMISE KILLED (it is not idea 311's g-band loophole) + KEEP-candidate on path 4b (U56 only).**
The window is 7 contiguous rungs wide, both rule-8 conventions pick inside it, and the gate-less
control clears at 1 rung. **PARK stands for B136.** 4a fails on U56 at every rung.

## Caveats
- **Survivorship:** `universe.json` and `universe_broad.json` are current-constituent lists, so
  every LEVEL here is biased up — including the CAGR floor's margin, which is the binding leg.
  The band's SHAPE is a within-panel comparison and is not affected.
- The dial `q = 0.20` is the best of four; that is one of the two tuned parameters, and the other
  (g) is now shown to be non-critical over a 7-rung range. No third parameter was spent.
- 2020 and 2022 are the only real stress tests in the sample; the gate fires 14.3% of days.
- Cash is credited at 0% throughout (idea 642's open question); at g < 1.00 that understates CAGR
  and therefore understates the band's lower edge.
