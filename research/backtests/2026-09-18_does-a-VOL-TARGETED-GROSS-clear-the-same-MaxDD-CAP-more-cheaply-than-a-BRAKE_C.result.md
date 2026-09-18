# Idea 1297 (lane C, 2026-09-18) — does a VOL-TARGETED GROSS clear the same MaxDD CAP more cheaply than a BRAKE?

**VERDICT: KILL (capital) for the overlay — no RULES change. KEEP-4b RE-CONFIRMATION of the
flat incumbent on U56 (full sample AND rule-8 OOS, every leg).** 101 of 101 gates pass;
offline, deterministic, 18.0s. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

**THE INSTRUMENT.** k_t = min(0.60, TARGET / v_t), v_t = annualised sd of the book's own gross
returns over the WINDOW rows ending at t-1 (rule 2), applied weekly to the certified incumbent
(N=15 / H=126 / GROSS=0.60 / W, 10 bps). Two dials, TARGET {6,8,10,12,14}% x WINDOW {21,63,126},
15 cells x 3 panels, **all 45 published** (`.grid.csv`), plus the B_SELF robustness basis
(`.robust.csv`, 45 more) and a 10-cell frozen reference brake per panel (`.brake.csv`).

**1. THE OVERLAY IS A PURE CAGR COST: 44 of 45 cells give up CAGR, 0 of 45 gain more than
+0.002 pp.** dCAGR runs -2.94 .. +0.00 pp; dMaxDD runs -0.05 .. +9.90 pp. Only 11 of 45 cells
beat the incumbent's Sharpe at all, all at WINDOW=21 or at TARGET >= 10% (i.e. where the scaler
is capped 87-99% of the time and the book is the incumbent).

**2. IT WORKS WHERE IT IS NOT NEEDED AND FAILS WHERE IT IS.** Idea 1215 named the DD cap the
modal 4b binder. On U56 and B136 the FLAT incumbent already clears it with room (-16.38% and
-15.97% against a -20.23% cap) — 4b passes 15 of 15 (U56) and 13 of 15 (B136), but the
incumbent passes there too, so the overlay adds nothing. On SMALL, where the cap really binds,
**0 of 15 cells pass on either basis**: the deepest cell (6%/21d) buys 9.90 pp of drawdown to
reach -22.43%, still **2.20 pp short of the cap**, while CAGR falls to 4.40% against a 9.84%
floor. The binder is not clearable by this instrument on the panel that binds.

**3. RULE 8 (2017-2026 READ ONCE), (TARGET, WINDOW) by argmax IS Sharpe on warm-up..2016-12-31.**
B_CONST picks: U56 8%/21d, B136 6%/21d, SMALL 6%/63d. **Mean OOS Sharpe against the incumbent
-0.0563; all three B_SELF picks are negative (-0.073 / -0.038 / -0.085).** Only U56/B_CONST
clears every 4b leg out of sample (OOS 13.58% / 1.2113 / -14.41% vs SPY OOS 15.28% / 0.8747 /
-33.72%, floor 10.69%, cap -20.23%) — and it does so by paying **1.54 pp of OOS CAGR for
+0.0166 of OOS Sharpe** over an incumbent that already clears the same legs (15.12% / 1.1947 /
-16.38%). B136's pick FAILS the OOS CAGR floor (9.91% vs 10.73%); SMALL's fails every leg.

**4. THE QUEUE'S QUESTION HAS NO BASIS-FREE ANSWER.** At matched MaxDD the vol-target is
CHEAPER than a SPY-200d brake on U56 at all four depths (+0.32 .. +1.63 pp of CAGR) and on
B136 at 2 of 4, but DEARER than the book's-own-equity brake on U56 at 3 of 4 (-0.04 .. -1.63 pp)
and DEARER than SPY-200d on SMALL at all four (-0.68 .. -1.38 pp). **The sign flips with the
brake's basis on the same panel**, so "vol-target vs brake" is not decidable without first
fixing the brake basis — which is idea 1296's dial, not this run's.

**5. 4a IS 0 of 45 ON BOTH BASES**, as for every book in this family: the live RULES v2 book's
-12.05% MaxDD is not matched by any gross overlay that keeps the incumbent's CAGR.

**COST.** Annual one-way turnover 2.26-2.94 (U56, incumbent 2.46), 2.37-3.12 (B136, 2.65),
2.63-3.72 (SMALL, 3.41): the de-grossing trade is real but small relative to selection churn.

**RULES WORDING IF THE SUNDAY REVIEW EVER ADOPTS THE RE-CONFIRMED BOOK (unchanged from the
incumbent — this run proposes NO overlay clause):** *"Hold the top 15 names by the 3-leg
composite among instruments above their 200-day average with 20-day annualised vol below 0.60,
equal weight at 60% gross, minimum hold 126 trading days, rebalanced weekly, decided at the
close and traded at the next close."* No vol-target clause is proposed; adding one costs CAGR
on 44 of 45 cells and loses OOS Sharpe on 5 of 6 panel-basis pairs.

**GATES 101 of 101.** G0 min sample 16.7y (rule 1). G1 the U56 incumbent replays idea 1215's
committed 13.66% / 1.1706 / -16.38% to 3e-05. G2 a degenerate TARGET=1000% reproduces the
incumbent BIT-EXACTLY on all three panels (max|d| 0.0), so the overlay is a strict
generalisation. G3 live RULES v2 U56 MaxDD == the committed -12.05%. G4 k_t is unmoved by
perturbing the tape at/after the probe row (causality, max|d| 0.0). G5 OOS starts 2017-01-03.
G7 max k <= 0.60 in all 90 cells — no rung levers up.

**SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are current-constituent lists; every absolute
level is optimistic and every 4b pass an UPPER bound. The headline is a DIFFERENCE between an
overlay and the flat book on the SAME names, so a panel-common level bias moves both together
and the sign of the cost is first-order immune; the pass COUNTS are not.
