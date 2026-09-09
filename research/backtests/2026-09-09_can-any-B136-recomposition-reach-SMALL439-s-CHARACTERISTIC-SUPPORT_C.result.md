# Idea 568 — can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT (lane C, 2026-09-09)

**VERDICT: KILL of the characteristic read — and NO to the title for B136.** No capital candidate,
no memo, no RULES change. Script:
`research/backtests/2026-09-09_can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT_C.py`

## Gates (run before any new number was read)
- **G1 PASS** — idea 312's committed `.grid.csv` REAL rows (3 panels × 2 arms × 3 gross × 2 cadence
  = 36 rows × 13 columns) rebuilt from source: **max |diff| 4.44e-16**, 4a 36/36 and 4b 36/36 flags
  reproduce. Published premium re-read U56 −0.0045 > B136 −0.0465 > SMALL439 −0.1023, GAP **+0.0978**
  exactly as pre-registered.
- **G2 PASS** — vectorised runner vs `engine.backtest`, max |dreturn| **1.39e-17**.

## The answer to the title: NO for B136, YES only by importing SMALL names
k = 36 draws, kernel-weighted (bandwidth = 0.5 × cross-name sd, pre-registered) on the pooled
134 B136 + 439 SMALL439 names, common index 2010-01-04 … 2026-09-04 (15.7 yr after warm-up).

| pool | cvol reach | breadth reach |
|---|---|---|
| BONLY (B136 only) | **[0.165, 0.401]** | **[0.575, 0.770]** |
| SONLY (SMALL only) | [0.314, 0.995] | [0.234, 0.627] |
| POOL | [0.165, 0.995] | [0.232, 0.770] |
| **SMALL439 anchor** | **0.5618** | **0.4830** |

**No re-composition of B136 reaches SMALL439's cvol (0.562) or its breadth (0.483) at k = 36** — the
extreme 36-name tilts of the large-cap panel stop at 0.401 and 0.575. Idea 312's premise is confirmed
and sharpened: the published ladder was never bracketed and cannot be, from inside B136.
`H_SUPPORT` **PASS** only for the POOL (draw-level support cvol [0.278, 0.588], breadth
[0.448, 0.684]), i.e. the anchor is reachable *only* by importing small-cap names — which is the very
confound the matching was supposed to remove.

## Is the premium a function of the characteristic once support overlaps? No.
Premium = `Sharpe(MA-RS) − Sharpe(EWall)`, mean over 6 seeds × 3 gross × 2 cadence.

| char | flavour | slope | R² | span | slope×span | \|eff\|/GAP | seed sd | monotone |
|---|---|---|---|---|---|---|---|---|
| cvol | POOL | **+0.1522** | 0.020 | 0.311 | **+0.0473** | 0.48 | 0.1000 | no |
| breadth | POOL | +0.4847 | 0.264 | 0.236 | +0.1143 | 1.17 | 0.0581 | no |
| cvol | BONLY | +1.1886 | 0.223 | 0.088 | +0.1046 | 1.07 | 0.0562 | up |
| cvol | SONLY | +0.6769 | 0.226 | 0.201 | +0.1358 | 1.39 | 0.0739 | no |
| breadth | BONLY | −0.7864 | 0.203 | 0.086 | −0.0676 | 0.69 | 0.0459 | down |
| breadth | SONLY | +0.9318 | 0.208 | 0.094 | +0.0876 | 0.90 | 0.0527 | up |

- **H_CHAR FAIL.** On POOL the cvol slope has the **wrong sign** (the published ordering needs the
  premium to *fall* as constituent vol rises; it rises, R² 0.020) and neither ladder is monotone.
- **H_NOISE FAIL.** Recomputed noise floor = mean within-rung seed sd **0.0690** (0.71× GAP; idea 312
  got 0.0745). The POOL cvol effect (+0.0473) is **inside its own rung sd (0.1000)**.
- **H_PRED FAIL.** The POOL fit evaluated at the real panels' own characteristics predicts
  cvol: U56 −0.145, B136 −0.143, SMALL439 −0.099 — the ordering **backwards**, max |resid| 0.153;
  breadth: −0.088 / −0.088 / −0.185, ordering right-ish but max |resid| 0.096, both far above the
  0.03 tolerance carried over from idea 312.

## The finding: ORIGIN survives the match, and it is 2× the published gap
At a **matched** characteristic level, B-sourced and S-sourced draws are not the same book.

| char | L | achieved B / S | premium B | premium S | B − S | seed sd | t | (B−S)/GAP |
|---|---|---|---|---|---|---|---|---|
| cvol | 0.320 | 0.2732 / 0.4022 | −0.0473 | −0.3010 | **+0.2537** | 0.0773 | +8.04 | **+2.59** |
| cvol | 0.390 | 0.3103 / 0.4373 | −0.0067 | −0.2064 | **+0.1997** | 0.0688 | +7.11 | +2.04 |
| breadth | 0.580 | 0.6322 / 0.5354 | +0.0068 | −0.1280 | **+0.1348** | 0.0595 | +5.55 | +1.38 |

**H_ORIGIN FAIL, 0/3 matched rungs inside the seed sd, mean B−S = +0.1961 = +2.00× the whole
published GAP.** Note the kernel cannot even match exactly at k = 36 (the two pools' achieved levels
differ by 0.10–0.13 in the direction that would *shrink* the gap if the characteristic carried it) —
so this is a lower bound on the origin effect. The characteristic is not the carrier; the panel is.
That kills the cvol/breadth read without rescuing the cap read: idea 312 already showed the
three-panel margin is 0.76× its own draw-level noise floor, so "origin" here names an unexplained
composition effect, not a validated cap boundary.

## Rule 8 walk-forward (IS ≤ 2016-12-31, OOS ≥ 2017-01-01, read once)
- **WF-A**: the POOL cvol slope's **sign flips**, IS −0.0493 (R² 0.000) → OOS +0.2530 (R² 0.039). The
  POOL breadth slope holds sign but collapses, IS +1.2321 (R² 0.256) → OOS +0.1179 (R² 0.015). Only
  the *origin-restricted* slopes hold both sign and R² (BONLY cvol +0.664→+1.499, R² 0.047→0.190;
  SONLY cvol +0.406→+0.788, R² 0.025→0.210) — the same message as H_ORIGIN.
- **WF-B** (pick (char, level) by IS Sharpe of the seed-pooled MA-RS book at g=0.75/W → breadth
  L=0.700):

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| WF-B pick (seed-pooled) | 10.53% | 0.968 | −23.84% | 1.142 / 0.846 | 10.52% | 0.921 | −23.84% |
| RULES v2 (B136) | 7.62% | 1.082 | −12.24% | 1.126 / 1.040 | 7.98% | 1.119 | −12.24% |
| SPY | 14.13% | 0.862 | −33.72% | 0.891 / 0.858 | 15.45% | 0.882 | −33.72% |

  4a **False** (loses H2 and MaxDD to RULES v2); 4b fails on **H2, DD**.

## KEEP paths over every book (1,836 books = 36 REAL + 1,800 DRAW)
**4a 3/1836 (0.16%), 4b 35/1836 (1.9%), BOTH 0/1836.** Binding 4b legs: DD 1561, H2 1346, OOS 1312,
CAGR 1032, H1 1025. All three 4a passers are `EWall` (the ungated control) at g=0.50/M — i.e. the
de-grossed control, not the gate. **31 of the 35 4b passers are BONLY draws** (large-cap-only
recompositions) — the by-product agrees with H_ORIGIN — and the best of them
(`cvol~BONLY~L0.390~1` MA-RS g=0.75/W, CAGR 15.84%, Sharpe 1.245, MaxDD −17.61%, OOS 1.314) is a
seeded kernel draw of current constituents, **not a rule anyone can trade**. No capital candidate,
no memo filed.

## Restatements
- **SURVIVORSHIP**: both `universe_broad.json` and the small panel are CURRENT constituents; the
  small end carries more of that bias. The premium is an arm-minus-arm difference on the same panel,
  so the level bias largely cancels, but the B−S origin gap above is not immune to it.
- **SAMPLE**: the pooled index starts 2010-01-04 (the small cache's first bar), so every draw is read
  on 2011-01 … 2026-09, and the three real panels are restated on that same window beside their
  published full-sample numbers (U56 +0.0080 / B136 −0.0250 / SMALL439 −0.1023; gap +0.1102 vs the
  full-sample +0.0978).
- **Tuned parameters: exactly two** — the characteristic {cvol, breadth} and the target level L.
  Gross {0.50, 0.75, 1.00}, cadence {W, M}, seed and flavour are reported axes; all 1,800 draw books
  and all 25 feasible rungs (8 infeasible rungs named) are in the committed CSVs.
