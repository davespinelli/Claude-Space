# idea 1678 (lane C, 2026-09-19) — VOLTGT ladder of its two inherited dials

**PRIMARY VERDICT: PARK for idea 1656's specific cell.** Idea 1678 pre-stated "if the IS-chooser's
pick is not 0.15/20d, the 1656 candidate is a PARK and says so." It is not. Over 48 rule-8 chooser
rows (3 panels x 4 cost rungs x 4 IS-only choosers) the inherited (target 0.15, window 20) cell is
picked **6 times**, and only **2 of those 6 also clear 4b OOS** (U56 `C_SHARPE` at 0 and 10 bps; it
moves to 0.20/40 and fails at 25 and 50 bps). `C_CALMAR` — one of the two choosers 1656 named —
reaches 0.15/20 in **0 of 12** rows. 4 of the 6 hits are on SMALL, where the cell fails 4b at every
rung. The 1656 numbers replicate exactly (G3, max |dev| 3.26e-05): the candidate is real but its
dials were not recoverable, so it is a PARK, not a KEEP.

**BUT THE FAMILY SURVIVES, AND THE IS SCREEN IS A PERFECT OOS PREDICTOR.** 4b FULL *and* OOS passes
**87 of 240** published cells (U56 12/20, B136 11/20, SMALL 0/20 at 10 bps); the passing region is a
connected LOW-TARGET block, so 0.15/20 sits on a plateau, not an argmax. The record's own pre-stated
4b-feasibility screen read on IS rows only (MaxDD >= 0.6 x SPY_IS, CAGR >= 0.7 x SPY_IS) admits
**9 of 20 cells on U56 and 5 of 20 on B136, and 9 of 9 and 5 of 5 of them clear 4b FULL and OOS.**
The tie-break inside that set is therefore immaterial to the verdict. On SMALL the screen admits
**0 of 20** — there is no legitimate pick there at all, and the family is dead on small caps.

**SECONDARY VERDICT: KEEP-4b CANDIDATE (rule-8 legitimate, 2 tuned parameters), NOT ENACTED.**
`C_MEMO` picks **target 0.10 / window 10** on BOTH U56 and B136 from IS rows alone. U56 @10 bps:
FULL 12.06% / 1.1787 / -14.22% (halves 1.2102/1.1499 vs SPY 0.9570/0.8249), **OOS 13.11% / 1.2678 /
-14.22%** vs SPY OOS 15.26% / 0.8737 / -33.72% and the live book's 9.46% / 1.2766 / -12.05%.
B136 @10 bps: FULL 11.85% / 1.1470 / -14.89%, **OOS 12.22% / 1.1831 / -14.89%**. 4b FULL and OOS
clear at 0/10/25 bps on both panels; at 50 bps U56 keeps 4b OOS and loses 4b FULL, B136 loses both.
Turnover is the bill: **4.85x / 5.04x per year** against the incumbent's 1.92x / 2.05x. It buys
**5.1 pp (U56) and 3.4 pp (B136) of OOS drawdown** for **2.6 pp and 2.8 pp of OOS CAGR**.

**AND THE DIAL IS NOT A DE-GROSS IN COSTUME — the first family this month to clear that bar.** Every
cell was priced against its OWN realised-gross-matched constant-gross EW twin (G6, match 5.8e-06).
The twins clear 4b FULL&OOS in **0 of 60 cells at every one of the four cost rungs**, while the cells
clear 23 / 23 / 22 / 19 of 60. MaxDD is shallower than the matched twin in **59 of 60** at 10 bps,
mean **+7.56 pp** (U56 +6.88, B136 +9.77, SMALL +6.03) — about 2.6x idea 1511's measured 2.93 pp
paired SE. The Sharpe credit is inside noise and dies with cost (40 of 60, mean +0.0026 at 10 bps;
**-0.0133 at 25 and -0.0398 at 50**), and CAGR is paid every time (mean -1.85 pp/yr). So the honest
statement is narrow: **vol targeting buys drawdown at matched exposure; it does not buy Sharpe.**

**PATH 4a FAILS 0 OF 240.** Live RULES v2 draws only -12.05%; path 4a cannot adjudicate a growth
book, as eleven runs this month have now found.

**PROPOSED RULES WORDING (NOT ENACTED — Sunday review, rule 6).** *Clause: hold every priced name at
an equal share of a VOL-TARGETED sleeve. Each rebalance (weekly, last trading day), compute the
trailing 10-day realised volatility v of the equal-weight sleeve, annualised as std x sqrt(252).
Set the sleeve scale k = min(1.00, 0.10 / v); if v is unavailable set k = 0. Hold each of the N
priced names at k / N of NAV; the residual 1 - k is CASH, never re-spread. No ranking, no vol
filter, no band. Gross is capped at 1.00 and leverage is never used.*

**CAVEATS, IN FULL.** (1) Two tuned parameters (target, window), the protocol maximum; gross was
pinned at 1.00 and not re-swept here. (2) Survivorship (rule 9): U56/B136 are current-constituent
lists, so the absolute 4b levels are UPPER BOUNDS; the cell-vs-twin contrast is first-order immune.
(3) The candidate's CAGR is **2.15 pp below SPY** on U56 FULL — it clears 4b because the bar asks
70% of SPY's return at 60% of its drawdown, which a de-risked book delivers in a 17.7y bull sample:
**this is de-risking, not alpha.** (4) 4.85x/yr turnover at 10 bps is the live rung; at 50 bps the
book is gone. (5) **It is dead on SMALL** (OOS 2.28% / 0.2571 / -23.22%, 4b 0 of 20 at every rung).
(6) 8 of 8 gates PASS, including the exact cost axis (G4, 0.000e+00) and no leverage (G5, max
realised gross 1.000000).
