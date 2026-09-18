# MEMO — idea 1298: the standing KEEP-4b book is STALENESS-ROBUST on U56, and B136 is not

1. **What was asked.** PROTOCOL rule 2 fixes execution at t+1, so every committed number in this
   family assumes Friday's decision is traded at Monday's close. This run walks EXECUTION LAG
   d in {1,2,3,5,10,21} trading days x panel {U56, B136, SMALL} at idea 1215's own rule-8 anchors
   (U56 N=15/g=0.60, B136 N=25/g=0.60, SMALL N=25/g=0.40), every other axis frozen. 18 books, all
   published. GATES 7 of 7, incl. fast runner == `engine.backtest` to **1.39e-17** (ndarray, no
   skipna) and a causality gate that poisons every signal row after t-d at all six lags.
2. **U56: 4b PASSES at ALL SIX LAGS.** Sharpe 1.1399–1.1967 against SPY 0.8849; CAGR 13.42–14.25%
   against SPY 15.13%; MaxDD -16.38% to -18.49% against the 0.60 x SPY cap of -20.23%. Joint 4b
   margin stays positive at every rung (+1.74 to +3.08 pp). This is a stress certification the
   record did not previously have for this book.
3. **And the book is genuinely different at the far rungs.** Slot overlap with d=1 falls to 0.760
   at d=21 — roughly a quarter of the holdings are different names — and it still clears 4b.
4. **B136 does NOT survive.** It passes at d=1,2,3,5 and FAILS at d=10 (margin -0.20 pp) and d=21
   (-0.55 pp), on the **DD leg alone**: MaxDD -20.43% / -20.78% against the -20.23% cap. Idea
   1215's second-panel corroboration is therefore a d<=5 result, and should be quoted as one.
5. **The failure is not signal decay.** B136's Sharpe RISES with d (1.0965 at d=1, 1.1854 at
   d=21); only drawdown worsens. Nothing here says the stale signal stops working.
6. **H_MONO fails 0 of 3 panels.** Sharpe is not monotone decreasing in d on any panel; the d=21
   rung has the HIGHER full-sample Sharpe on both large-cap panels. A 12/6/3-month composite with
   a 126-day minimum hold carries no information in the last few days, so freshness is not where
   this book's edge lives. Read the rung-to-rung spread (+/-0.09 Sharpe) as noise about a common
   level, not as a decay curve.
7. **RULE 8, 2017-2026 read ONCE. H_OOS FAILS: 1 of 3 panels, mean reach -0.0100.** U56's IS
   chooser picks d=3 and it COSTS **-0.0944** of OOS Sharpe against simply obeying the protocol
   (OOS 13.97% / 1.1002 vs d=1's 15.12% / 1.1947). B136 picks d=2, +0.0644. SMALL's IS 4b-shaped
   set is empty; the declared fallback is d=1, OOS 3.60% / 0.4089, FAIL at every lag.
8. **VERDICT: no RULES change, no new book.** 4a passes 0 of 18. The deliverable is a robustness
   certification of the STANDING 2026-09-04 / 1294 / 1215 incumbent, not a replacement for it, and
   a documented limit on its B136 corroboration. Selecting d in sample is value-destroying, so
   rule 2's d=1 stays exactly as written.
9. **EXACT RULES WORDING** if the Sunday review wants the robustness recorded (this is an ADDITIVE
   note to the existing v2 candidate text, changing no live behaviour — rule 6 still applies, one
   change per week, and this memo does not itself change RULES.md):
   > *Execution robustness.* The top-N momentum candidate (U56, N=15, gross 0.60, H=126, weekly,
   > above-200d and vol20 < 0.60, equal weight, 10 bps, t+1) clears PROTOCOL 4b at every execution
   > lag from 1 to 21 trading days on U56. A missed or delayed fill up to one month is therefore
   > not a reason to skip a rebalance or to trade at a worse price to stay on schedule. On the
   > broad 136-name panel the same book clears 4b only up to a 5-day lag; beyond that it breaches
   > the 4b drawdown cap, so the broad-panel corroboration is quoted as a d <= 5 result.
10. **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are current-constituent lists; delisted and
   acquired names are absent, which flatters every momentum book here. Every absolute level is
   optimistic and every 4b pass is an UPPER bound. The headline is a DIFFERENCE between lags on
   the SAME names in the SAME book, so a level bias common to a panel moves all six rungs
   together and the robustness finding is first-order immune; the pass COUNTS are not.
