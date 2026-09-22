# Idea 1062 (lane C, 2026-09-22) — is the D-vs-W margin at 10 bps resolvable at all?

**Slug disambiguation.** Two `## Open` lines carry the label 1062 (standing defect 932). This
answers the one at the smaller file offset, `is-the-D-vs-W-MARGIN-at-10-bps-RESOLVABLE-at-ALL`.
The other (`is-the-QUARTER-END-REBALANCE-PENALTY-minus-1.53pp-a-STANDING-RULE`) is untouched.

**Verdict: ANSWERED — YES on the cell 968/1059 published it on; KILL of the general claim.
No memo, no promotion, no RULES change.**

## The two tuned dials (rule 4)
1. **Cost-rung ladder** `{0, 2, 5, 7.5, 10, 15, 25, 50}` bps — the queue's fine ladder plus
   PROTOCOL's own rungs, so 1059's cells are reproduced *in place*, not interpolated (G10).
2. **Denominator** `{DEN_FULL = 6 x (P+1), 1059's own; DEN_CANON = canonical period-end alone,
   n = 6 MATCHED across cadences; DEN_PHASE = phase members alone}`.

Panel `{U56, B136}`, gross `{0.50, 0.75, 1.00}` and the 6 mechanism arms are **reported, never
selected on**. 1,320 distinct books x 8 rungs = 10,560 published rows.

## Gates: 9 of 10
`G5` reproduces 1059's committed 4b pass-rate profile to **4.55e-04** (U56@10bps
0.333/0.833/0.205/0.044; B136@10bps 0.000/0.028/0.000/0.000). **`G4` FAILS** (SPY OOS 0.1529 vs
committed 0.1521). `G4b` attributes it only partly: truncating to 1059's last date shrinks the
residual 3.78e-03 -> 2.89e-03 but does not close it — vintage plus a cache revision. Not waived.

## (A) The margin is real and decisive where it was published
On **U56 / gross 0.75**, `M(c) = pass4b(W) − pass4b(D)`:

| bps | 0 | 2 | 5 | 7.5 | 10 | 15 | 25 | 50 |
|---|---|---|---|---|---|---|---|---|
| M | 0.0000 | 0.0000 | 0.0000 | +0.1667 | **+0.5000** | +0.8333 | +0.2222 | 0.0000 |

- **Exactly zero at three consecutive rungs** → the pre-declared *pure cost object* signature
  holds; the pre-registered alternative (non-zero at zero cost) is rejected on this cell.
- `c* = 5.0 bps`, bracket **(5.0, 7.5]**, **identical on all three denominators**.
- At 10 bps: **+0.5000 = 6.00 of DAILY's 12 books**, mechanism-clustered 95% CI
  **[+0.1667, +0.8333]** (2,000 draws, seed 106200, resampling the 6 mechanism ARMS and carrying
  each arm's whole phase family at both cadences). Decisive under both rulers.
- **The queue's own falsifier reads FALSE**: the width does not span 0–25 bps here, so 968's
  weekly headline is **not** a one-book-margin claim.
- Mechanism: realised turnover D **22.43** vs W **9.04** turns/yr (2.48x) → **134 bp/yr**
  differential drag at 10 bps. The first binding leg on every dying D book is **`L_H1`**, not
  `L_CAGR` — the rung eats the first half before the CAGR floor.

## (B) But it is one cell, and GROSS is what decides it
Decisive at **14 of 144** (panel x gross x denominator x rung) cells; **8 of the 14 are the same
U56/gross-0.75 cell** read at 10/15/25 bps under three denominators.

- U56 **gross 0.50**: pass rate 0.000 / 0.000 at *every* rung — no margin to resolve.
- U56 **gross 1.00**: pinned at 0.167 / 0.167 from 0 through 25 bps — cost-insensitive.
- **B136**: `M(0)` = **+0.1667 / +0.1389 / −0.0278** at gross 0.50 / 0.75 / 1.00 — non-zero at
  *zero* cost at every gross, and **negative** at 1.00. Not a cost object on that panel at all.
  Decisive at 0 of 8 rungs at 10 bps.
- **Denominator moves the crossing nowhere.** DEN_CANON's matched `n = 6` removes the 12-vs-36
  asymmetry the queue suspected and returns the identical bracket and identical `M` at every
  rung. It moves only persistence past 15 bps (25 bps: DEN_CANON 0.0000 vs DEN_FULL +0.2222).

## Both KEEP paths at every grid point
**4a 17, 4b 688, BOTH 0 of 10,560** book-rungs (D/W pair only: 4a 17, 4b 345, **BOTH 0 of
2,304**). All 17 4a passes are one object — `BAND03` (the live RULES v2 mechanism) on B136 at
weekly phase 1, gross 0.50 and 0.75, all 8 rungs, plus phase 3 at 50 bps: a rebalance-**phase**
offset of the live book, prior art under idea 914, **not promoted**. Binding 4b legs over the
9,872 failures: `L_DD` 0.812, `L_H2` 0.275, `L_CAGR` 0.256, `L_OOS` 0.175, `L_H1` 0.055.

## Rule 8 — cadence chosen on ≤ 2016-12-31 only, 2017–2026 read once (144 grid points)
| chooser | picks W | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b-OOS | beats live |
|---|---|---|---|---|---|---|
| C_ISSHARPE | 144/144 | 12.26% | 1.0005 | −18.63% | 0.181 | **0.000** |
| C_ISLEGS | 131/144 | 12.06% | 0.9855 | −18.88% | 0.180 | **0.000** |
| **C_FROZEN = W** (0 params) | — | 12.26% | 1.0005 | −18.63% | 0.181 | **0.000** |
| live RULES v2 | — | 8.56% | **1.1775** | −12.16% | — | — |
| SPY | — | **15.27%** | 0.8744 | −33.72% | — | — |

`C_ISSHARPE` is **bit-identical to the zero-parameter frozen rule** — the fitted chooser buys
nothing. Both name the OOS-better cadence at 132 of 144 (0.917). **KILL for capital.**

## What this changes
"Weekly beats daily, and 10 bps is the rung that decides it" survives as a statement about
**U56 at gross 0.75**, decisively measured. It does **not** survive as a cadence law. Any future
claim of the form "cadence X beats cadence Y at rung c" must state its **gross**, because gross
is the dial that decides whether the rung bites at all.

## Survivorship (rule 9)
U56 and B136 are current-constituent panels. The bias is common to both cadences and cancels in
the *margin*, but flatters both the CAGR floor and the DD cap against SPY in every absolute
figure above.
