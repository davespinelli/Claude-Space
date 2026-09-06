# Idea 297 — is-the-negative-exposure-timing-residual-a-general-property-of-gates (lane B, 2026-09-06)

**Verdict: SPLIT. The SIGN is general; the DIAL-DEPENDENCE is not, and idea 290's cadence claim
does not survive re-reading on its own panel. No RULES change, no KEEP (4a 1/216, 4b 29/216).**

Script `2026-09-06_is-the-negative-exposure-timing-residual-a-general-property-of-gates_B.py`,
216 cells (3 panels × 2 gates × 3 cadences × 6 bands × 2 constructions) at 10 bps and 0 bps,
plus 9 no-filter controls and the live book. 8m32s, deterministic.

## Gates asserted before any new number was read
- **B0 reproduction** of idea 290's committed `identity.csv` on the 36 SMALL439 cells:
  worst |diff| **8.9e-16** on c_bar / gap0 / pred0 / resid0 (bar 1e-6). HOLDS.
- **P1** the leverage identity `r_dg,t ≡ c_t·r_rs,t` on all 108 pairs across all three panels:
  worst error **0.0e+00** (bar 1e-12). HOLDS — the decomposition is exact off the small panel too.

## The four pre-registered hypotheses
| | bar | SMALL439 (anchor) | U56 | B136 | verdict |
|---|---|---|---|---|---|
| **H1** sign | resid0<0 in ≥33/36 on each large panel | 35/36 | **31/36** | **36/36** | **FAILS as written** |
| **H2** band widens it | mean(b=0.12) < mean(b=0.00) AND \|t(ρ)\| ≥ 2 | −0.322→−0.574, ρ −0.330 t −2.04 | −0.242→−0.451, ρ −0.268 **t −1.62** | −0.512→−0.659, ρ −0.042 **t −0.25** | **FAILS** |
| **H3** slower cadence widens it | W > M > Q | W −0.273, **M −0.184**, Q −0.745 | W −0.310, **M −0.072**, Q −0.517 | W −0.489, **M −0.302**, Q −0.666 | **FAILS on all three, anchor included** |
| **H4** live book | RULES v2 resid0 < 0 | — | **−0.155 pp/yr** (share 0.9601, c_bar 0.7101) | — | **HOLDS** |

## What the numbers actually say
1. **The negative sign is general — H1 fails only on a window.** U56's 5 positive cells are all
   in its pre-2011 head, which SMALL439 does not have: all 5 flip negative once that head is
   dropped. On the **COMMON window** (2011-01-13 → 2026-09-04, identical days for all three
   panels) the count is **35/36 SMALL439, 36/36 U56, 36/36 B136**, mean residual −0.400 / −0.480
   / −0.695 pp/yr, exact sign-test p 1.1e-9 / 2.9e-11 / 2.9e-11. It is also
   general **across time**: OOS (2017-) is 36/36, 31/36, 36/36, mean −0.591 / −0.362 / −0.671.
   The pre-registered bar was set on the FULL window and is reported as failed there; the honest
   reading is that de-grossing times its own exposure badly on large caps too, and *more* so than
   on the sub-$2B panel (B136 −0.486 vs SMALL439 −0.401 pp/yr on FULL).
2. **The dial-dependence does not generalise.** The band gradient shrinks to insignificance off
   SMALL439 (t −2.04 → −1.62 → −0.25) even though the sign of every panel's endpoint difference
   is right; the effect is a level shift, not a slope.
3. **Idea 290's cadence claim was mis-stated and this run corrects it.** "Widens with slower
   cadence" is not monotone on *any* panel including idea 290's own: **monthly is the least
   negative rung everywhere** (−0.184 / −0.072 / −0.302) and quarterly the most (−0.745 / −0.517
   / −0.666). All 6 non-negative FULL-window cells across the whole grid are monthly. The right
   statement is "Q is worst, M is best", not "it widens as the dial slows".
4. **The live book carries the property but is nearly free of it.** RULES v2 reconstructs exactly
   (max |w − `baseline.rules_v2_weights`| = 0.0e+00) as the DEGROSS construction; its de-gross
   cost is −3.88 pp/yr of CAGR of which **96.0% is pure cash drag** at c_bar 0.71 and only
   **−0.155 pp/yr** is timing (IS −0.158, OOS −0.166 — stable). The live book's de-gross choice
   costs 3.6 pp of CAGR (8.66% vs the respread twin's 12.25%) and buys 5.7 pp of drawdown
   (−12.05% vs −17.71%) and +0.045 Sharpe. That trade is an exposure trade, not a timing one.
5. **Consistent with idea 298's "it's the gate's FORM":** MA cells are roughly twice as negative
   as MAVOL cells on every panel (−0.519/−0.402/−0.627 vs −0.282/−0.197/−0.344).

## Rule 8 walk-forward (band, cadence picked on ≤2016-12-31 inside each of 12 arms; 2017– read once)
Best OOS: U56/DEGROSS/MA (pick b=0.00, M) **9.53% / 1.2815 / −11.87%**; B136/RESPREAD/MA
(b=0.12, W) **13.77% / 1.1646 / −21.72%**. Comparands OOS: **LIVE RULES v2 9.53% / 1.2851 /
−12.05%**, **SPY 15.45% / 0.8820 / −33.72%**, control EWall-W 10.10%/13.86%/13.95% by panel.
Picks beating SPY OOS on Sharpe **8/12**, the matched no-filter control **7/12**, the live book
**0/12**. Walk-forward on the residual itself: IS→OOS sign agreement 58/64/75%, and an IS panel
mean beats the naive zero on OOS MAE (0.488 vs 0.591, 0.267 vs 0.385, 0.420 vs 0.671) — i.e. the
level is weakly predictable, the per-cell pattern is not.

## KEEP paths (all 216 cells)
- **4a: 1/216** — U56/DEGROSS/MA/W/0.03, i.e. the live book's own construction on U56 without SPY
  as a holding (8.68%/1.2128/−11.90%). It is a re-labelling of the live rules, not a new book,
  and it fails 4b on CAGR. Not a candidate.
- **4b: 29/216**, all on the large panels and all RESPREAD (U56 19, B136 10), none on SMALL439.
  Binding bars: CAGR 140, DD 103, H2 82, OOS 77, H1 72. These are levels on a survivorship-
  screened panel and none is a pre-registered dial of this idea — reported, not claimed.

**SURVIVORSHIP:** all three panels are current constituents; the headline residual is an
arm-minus-arm contrast on identical names and days, so the bias largely cancels there. It does
not cancel out of the 4a/4b columns.

## Follow-ups proposed
- Why is MONTHLY the least-negative rung on every panel and every gate? A cadence that is neither
  the fastest nor the slowest being the best-timed is either a phase artefact (cf. idea's
  phase-averaged cadence work) or a real rebalance-timing effect worth naming.
- The residual's level is weakly predictable per panel (IS mean beats zero on OOS MAE by 17-31%)
  but its per-cell sign is not (58-75% agreement). Idea 301 should use a per-panel constant, not
  a per-cell one.
