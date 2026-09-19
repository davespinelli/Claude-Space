# Idea 1523 (lane cloud, 2026-09-19) — is ID's ONLY channel the DRAWDOWN LEG, and is it RESOLVABLE?

**VERDICT: PARK.** Both questions are answered. **Yes, the drawdown leg is ID's only channel**
(z > +2 at 4 of 27 control cells on MaxDD and 2 of 27 on Calmar, against **0 of 27 on Sharpe**).
**Yes, it is now resolvable** — at 15x 1519's seed budget. But it is **panel-split, single-episode
and not convertible**, so it is not a KEEP. All 18 gates pass; G1 replays the committed
2026-09-04 U56 anchor to < 5e-3 and G2 shows the w = 0 frame bit-identical across all three L.

**WHAT WAS RUN.** 63 real books (L {63,126,252} x w {0,0.10,0.20,0.35,0.50,0.75,1.00}, every one
published) on U56 / B136 / SMALL, plus the rank-permuted-ID twin null at **S = 300 seeds** on
1519's own 9 pre-registered control cells per panel — **8,100 permuted books**. S is not a third
dial: it changes no book, nothing is selected on it, and it is reported at every rung of the
ladder {20, 50, 100, 200, 300}.

**(1) THE CHANNEL IS THE DD LEG, AND ONLY THE DD LEG.** Real beats the twin mean at 14 of 27 on
MaxDD, 13 of 27 on Calmar, **9 of 27 on Sharpe**; median z **+0.049 (MaxDD), -0.079 (Calmar),
-0.184 (Sharpe)**; **z > +2 at 4 / 2 / 0**. 1519's Sharpe KILL therefore stands and is now
resolved rather than merely unresolved. The positive cells are B136 L=126 w=1.00 (MaxDD -16.71%
vs twin mean -20.87%, z +2.52, p 0.0100; Calmar z +3.28, p 0.0033), U56 L=126 w=0.50 (z +2.47,
p 0.0033), U56 L=252 w=1.00 (z +2.16) and U56 L=63 w=0.20 (z +2.09) — all at LOWER turnover than
the frozen book (2.42-2.99 x/yr against 2.87). **This exactly replicates 1519's two incidental
readings: U56 -16.46% (L=252, w=1.00) and B136 -16.71% (L=126, w=1.00).**

**(2) AND IT IS PANEL-SPLIT, WHICH IS THE REASON THIS IS NOT A KEEP.** On SMALL the sign
REVERSES and does so significantly: L=252 w=0.50 gives z **-2.53** on MaxDD and **-2.45** on
Calmar, L=252 w=1.00 gives Calmar z **-2.99**. A device whose DD channel is +2.5 on large caps
and -2.5 on small caps has no mechanism the record can name yet. With 27 cells per statistic and
no multiplicity correction, 4 positives against ~1.4 expected by chance is above the noise floor
but not far above it.

**(3) THE CAVEAT THAT OUTWEIGHS THE FINDING.** **62 of 63 real books — and 26 of 27 control cells
— have MaxDD exactly equal to oMaxDD**: every one of these books takes its worst drawdown inside
the 2017-2026 OOS window (the 2020 episode). So the "OOS" DD test is **the same number as the
full-sample DD test**, carries no independent out-of-sample content, and the entire channel rests
on ONE episode. Any future run must say this before quoting an OOS DD.

**(4) RESOLVABILITY, ANSWERED WITH A NUMBER.** Read off the realised twin spread, not assumed:
median **S = 1,536 seeds** to pin the MaxDD permutation p to +/-0.01, and median **S = 6 seeds**
for the |z| > 2 decision itself to stop depending on the draw. The p-side number binds: a 20-seed
null **cannot produce a p below 1/(20+1) = 0.0476 at all**, and its Monte-Carlo SE at p = 0.05 is
+/-0.0487 — the same size as the quantity measured. **1519's "UNRESOLVED" was a statement about
its seed budget, not about ID.** Along the nested S ladder, 6 of 54 cell-statistics change their
|z| > 2 decision, all of them between S = 20 and S = 100.

**(5) BOTH KEEP PATHS AND RULE 8.** 4a **0 of 63** FULL and OOS (thirteenth consecutive zero).
4b 29 of 63 FULL, 29 OOS, 29 both (U56 19, B136 10, SMALL 0) — every one inherited from the
frozen incumbent. Rule 8 with **two** IS-only choosers (argmax IS Calmar, the statistic this run
is about, and argmax IS Sharpe): mean OOS Sharpe **0.7966 (Calmar chooser) / 0.8214 (Sharpe
chooser) vs frozen anchor 0.8812 vs SPY 0.8738 vs RULES v2 1.0087** — both lose to doing nothing.
The Sharpe chooser does improve mean OOS MaxDD (**-23.70% vs the anchor's -25.46%**, better on 2
of 3 panels), which is the DD channel showing through, but it buys that with CAGR (13.26% vs
16.19% on B136) and clears no KEEP path it did not inherit.

**SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010 (54 tickers with max_1d_move >= 1.0 dropped; 665 investable). Every
MaxDD LEVEL here is an upper bound. The headline is a real-minus-twin contrast on the same names
and days, where a bias common to both cancels.

Script: `research/backtests/2026-09-19_id-drawdown-leg-resolvability_cloud.py`
