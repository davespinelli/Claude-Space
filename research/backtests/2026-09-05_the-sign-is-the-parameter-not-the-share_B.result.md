# Idea 168 — the-sign-is-the-parameter-not-the-share (lane B, 2026-09-05)

**Verdict: KILL of the idea's own hypothesis.** The tilt exponent k has **no interior optimum**
on either large-cap panel: CAGR is monotone increasing in k across the whole ladder, the
beneficial band runs off the top of the grid in **12 of 12** large-cap (constr, share, cost)
cells at 10 bps, and the argmax sits at k ≥ +0.50 in 12 of 12 — at the grid EDGE (+0.75 or
+1.00) in **10 of 12**. So "the argmax k is at or near 0" is false, and the five prior
delete-the-scaler findings (ideas 72 / 82 / 141 / 160 / 159) are **three points read off a
monotone slope**, not a measured optimum. No new book, no RULES change, no new KEEP-candidate.

Script: `2026-09-05_the-sign-is-the-parameter-not-the-share_B.py`.
Outputs: `.grid.csv` (486 books), `.curve.csv`, `.band.csv`, `.argmax.csv`, `.walkforward.csv`,
`.console.txt`.

## Reproduction gate — 10 of 10, asserted before any new number was read
| anchor | got | ref |
|---|---|---|
| [a] mean weekly eligible, u56 / broad / small | 37.50 / 91.46 / 141.23 | 37.5 / 91.5 / 141.2 (idea 153) |
| [b] share→n map: u56 m=0.53→n, m=0.20→n; broad m=0.53→n | 20 / 7 / 48 | 20 / 7 / 48 |
| [c] dCAGR(k=+0.5) at m=0.20, lit, 10 bps: u56 / broad | +2.828% / +2.749% | +2.83% / +2.75% (idea 153/159) |
| [d] dCAGR(k=−0.5) at m=0.53, lit, 0 bps, u56 | −0.026806 | −0.0268 (idea 159) |
| [e] cost identity `r_0 − turnover·c/1e4` vs a fresh 10 bps engine run | max abs diff **0.00e+00** | ≤ 1e−12 |

Because [e] holds exactly, every gross/net pair below is the **same book**, not two runs.

## The measurement
`score_k = composite · (0.5 + 0.5·above200) · clip(vol20, 0.08)^k`, so **k = −0.5 IS RULES v1's
live score exactly**, k = 0 is the unscaled composite (idea 159's NONE), k = +0.5 its POS arm.
Two tuned parameters, both swept exhaustively, every grid point reported: **k** over 9 points
{−1.00 … +1.00 step 0.25} (the idea's five, extended two rungs each side so the argmax can be
shown interior or not), and **book share m** ∈ {0.20, 0.53, 0.85} realised as
n = max(2, round(m × mean weekly eligible)) — idea 153/159's own map. Panels (u56/broad/small),
cost rungs (0/10/25 bps), both gross constructions (lit/norm), halves and IS/OOS are reported
axes, never selected on. 3 panels × 2 constructions × 3 shares × 9 k = **162 books**, each run
once at 0 bps with the 10 and 25 bps rungs derived exactly = 486 (book, cost) rows.

## Result 1 — the curve is monotone, so zero is not an optimum (u56, lit, 10 bps)
| k | −1.00 | −0.75 | **−0.50 (live)** | −0.25 | **0.00** | +0.25 | +0.50 | +0.75 | +1.00 |
|---|---|---|---|---|---|---|---|---|---|
| CAGR, m=0.20 | 4.46% | 6.10% | **7.56%** | 12.80% | **14.68%** | 17.26% | 17.51% | 17.61% | **18.78%** |
| CAGR, m=0.53 | 7.67% | 8.17% | **9.90%** | 11.34% | **12.66%** | 13.21% | 13.15% | 13.19% | **13.51%** |
| Sharpe, m=0.53 | 0.909 | 0.913 | **0.996** | 1.046 | **1.092** | 1.102 | 1.082 | 1.079 | 1.095 |

Spearman(k, dCAGR) = **+0.93 … +1.00 in 12 of 12** large-cap cells at 10 bps (P2 confirmed on
the negative half at +1.00 everywhere). The **beneficial band's upper endpoint is open at the
grid edge in 12 of 12** of those cells: CAGR is still rising at k = +1. Its lower endpoint is
pinned at 0 by construction (k = 0 is the control, so dCAGR(0) ≡ 0) — reported, and **not**
quoted as a crossing. The **Sharpe** curve is a different animal: flat to within ±0.02 over
k ∈ [−0.25, +1.00] on u56 m=0.53, with an argmax that jitters from −0.25 to +1.00 across cells
(**span 2.00 of the 2.00-wide grid**, P4 confirmed). Buying CAGR with higher k buys vol at
almost exactly the same rate.

## Result 2 — the non-trivial crossing is the 4b boundary, and the live k is on the wrong side
The one crossing in k that is not definitional is where PROTOCOL 4b flips. At 10 bps:

| | lowest k passing 4b (full **and** OOS) | live k = −0.5 passes? |
|---|---|---|
| u56 lit m=0.53 / m=0.85 / m=0.20 | **−0.25** / 0.00 / −0.25 | no / no / no |
| broad lit m=0.53 / m=0.85 / m=0.20 | **−0.25** / +0.25 / none | no / no / no |
| all 12 large-cap cells at 10 bps | −0.25 in 8 of 12 | **passes in 1 of 12** (u56 norm m=0.85) |

`u56, lit, m=0.53 (n=20), 10 bps`: at k = −0.5 (the live tilt) CAGR 9.90%, Sharpe 0.996, halves
1.054/0.950, **fails 4b on the CAGR floor**. One rung up at k = −0.25 it passes 4b on the full
sample and on the OOS window alone; at k = 0, CAGR 12.66%, Sharpe 1.092, halves 1.088/1.102,
MaxDD −18.3%, OOS 14.36%/1.168/−18.3%. RULES v1 on the same panel at 10 bps: CAGR 6.45%,
Sharpe 0.664, halves 0.641/0.688, OOS 7.73%/0.747. SPY: 15.23%/0.889/−33.7%, halves 0.957/0.834,
OOS 15.45%/0.882/−33.7%. **At 25 bps nothing passes 4b full-sample at any k on any panel**
(the H1 Sharpe bar binds). Both KEEP paths were evaluated at every book: **4a passes 0 of 54**
u56 books at 10 bps (v1's own MaxDD of −13.8% is shallower than every k-book's) and 44 of 54 on
broad, where v1 is weaker — the asymmetry PROTOCOL 4b was added on Sep 4 to correct.

## Result 3 — sign flips on the small panel
On the sub-$2B panel every sign reverses: Spearman(k, dCAGR) = **−0.80 … −0.98** in all 18 cells,
argmax at k = −0.50 … −1.00, and the arm that is best on large caps is the worst here
(S_POS mean OOS Sharpe **0.233** vs S_ZERO 0.323, S_IS 0.321, S_INV 0.320 — the live tilt and
the do-nothing constant are indistinguishable on small). Idea 49/39's inverted gate carries:
reported, not traded. Whatever k prices, it is not the same object on the two panel types.

## Rule 8 walk-forward — k chosen on 2009–2016 only, read once on 2017–2026
Mean OOS Sharpe, large-cap cells (24 pairs): **S_POS (k=+0.5) 1.0195 > S_ZERO (k=0) 1.0002 >
S_IS 0.9979 > S_INV (k=−0.5, live) 0.8378**. Paired, **S_IS beats S_ZERO in 18 of 36 cells** —
a coin flip — and the IS argmax equals the OOS argmax in **30.6%** of large-cap cells with
Spearman(IS argmax, OOS argmax) = **+0.179**. This is the **fifth** independent instance of
ideas 110/151/132/166's finding that an IS-fitted chooser does not beat the do-nothing constant
(P5 confirmed). What does transfer is the *sign*: the live k = −0.5 is last of four selectors by
0.16 of Sharpe and 4.0 pp/yr of OOS CAGR, in every large-cap cell.

## Prediction scorecard (written before any number was read)
P1 reproduction **CONFIRMED** · P2 monotone on k ≤ 0 **CONFIRMED** · P3 Sharpe argmax ≥ 0 at
m = 0.53 **FALSIFIED** (broad's Sharpe argmax is −0.25; the Sharpe curve is flat and its argmax
is noise) · P4 argmax not sharply identified **CONFIRMED** · P5 IS chooser does not beat k = 0
**CONFIRMED** · P6 no large-cap 4b passer **FALSIFIED** — 26 of 54 u56 and 22 of 54 broad books
pass 4b full-sample at 10 bps. Every one of them is a **re-exponenting of a book already in the
record** (idea 153's n ≈ 0.53 × E, tilt-free): reported, **NOT PROPOSED** as a new candidate
(idea 144 convention, ideas 164/166 precedent).

## Caveats carried, not buried
Survivorship: all three panels are current-constituent lists (idea 54). vol20 is clipped at 0.08
before exponentiation and the gate already removes vol20 ≥ 0.60, so the ladder prices the slope
**inside the gate**, not a vol factor at large. At m = 0.85 all k hold most of the eligible set,
so dCAGR → 0 mechanically. Idea 38 (calendar-day index) and idea 126 (t+1 only) carry. One
realised path: a monotone slope measured once is not a factor study.
