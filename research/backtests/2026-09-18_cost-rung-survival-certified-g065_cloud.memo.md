# KEEP-4b confirmation memo for the Sunday review — THE CERTIFIED BOOK AT 25 AND 50 bps
(idea 1293, lane cloud, 2026-09-18. Rule 6 reserves enactment for the Sunday review; nothing is enacted
here. This CONFIRMS the standing U56 / N=20 / H=126 / g=0.65 candidate on a cost axis PROTOCOL rule 2
had frozen. It proposes NO change to the book and no new cell.)

1. **What was asked.** 4b's CAGR floor is one-sided — the book pays turnover, SPY does not — and the book
   turns 2.41x/yr, so a 25 or 50 bps account gives up ~0.60 / 1.20 pp/yr of CAGR the bar never gives up.
   If the committed pass died between 10 and 25 bps it would be an artefact of rule 2's rung.
2. **Outcome (A) SURVIVES.** The certified cell clears full-sample 4b at **0, 10, 25 and 50 bps**:
   CAGR 13.94 / 13.66 / 13.25 / 12.57%, Sharpe 1.1732 / 1.1526 / 1.1216 / 1.0699, MaxDD −16.68 / −16.73 /
   −16.80 / −16.93%, OOS 15.24 / 14.95 / 14.53 / **13.82%** and OOS Sharpe 1.2033 / 1.1833 / 1.1533 /
   **1.1031** against SPY's 15.28% / 0.8745 / −33.72%. The 10 bps quote is not doing the work.
3. **The anchor reproduces** to 4.8e-05 (13.66% / 1.1526 / −16.73%, OOS 14.95% / 1.1833; idea 1290).
4. **Breakeven.** A cost rung is an exact affine shift of the return series, so J = min(DD-cap margin,
   CAGR-floor margin) was read on a 1-bp sweep 0..100. At the certified gross J stays **> 0 past 100 bps**
   on FULL and OOS (it is the DD margin that binds there, and drawdown barely moves with cost: 3.55 → 3.30
   pp from 0 to 50). On the **IS half alone c\* = 73 bps** — the honest floor of this result.
5. **Cost does not move the sizing dial.** The declared rule-8 chooser (argmax J on warm-up..2016 only,
   ties to the lower gross) picks **g = 0.65 at every one of the four rungs** on U56. 2017-2026 read once.
6. **What cost does move is BREADTH OF THE PASS, not the pass.** U56 clears 4b at 5 of 7 gross rungs at
   every rung (0.55–0.75); B136 at 4 of 7 up to 25 bps and **0 of 7 at 50 bps**; SMALL **0 of 28**.
7. **B136 g = 0.60 stays PARK and gets a cost bound.** It clears 4b at 0/10/25 bps (OOS 12.59% / 0.9915 at
   25) and FAILS at 50; c\*(FULL) = 92 bps at g = 0.60 and >100 at g = 0.65. Still not stress-run.
8. **4a is 0 of 84 even cost-matched.** RULES v2 was re-run at every rung and still wins OOS Sharpe
   (1.2778 at 10 bps, 1.1795 at 50) at 9.47% / 8.69% OOS CAGR against 14.95% / 13.82%. That trade is the
   reviewer's decision, not this run's.
9. **Which leg binds.** Over the 52 failing cells the MaxDD cap fails 48 times and is the SOLE binder 17
   times; restricted to the 25/50 bps rungs it is 24 of 28 fails and sole binder 7 times. **Cost did not
   change the binding leg** — the CAGR floor never becomes the sole binder at any rung on any panel.
10. **Exact RULES wording, if a Sunday review enacted it** (UNCHANGED from idea 1290/1292 — this run adds
    only the cost bound): *"Each week at the close of the last trading session, rank every instrument in
    the mega-cap/ETF universe that is above its own 200-day moving average and has 20-day annualised
    volatility below 0.60, by the equal-weighted average of its percentile ranks on (t−21 / t−252),
    (t / t−126) and (t / t−63) total return. Hold the top 20, equally weighted, at 0.65 of NAV with the
    remainder in cash; a holding is retained for at least 126 trading days from the session it was bought,
    and a retained holding keeps its slot. Trade at the next session's close."*

**Caveats.** (i) The IS half's c\* of 73 bps, not the FULL sample's >100, is the number to quote to a
reviewer. (ii) SPY is left cost-free at every rung deliberately: repairing that asymmetry would make the
book look better, and this run tests the book, not the bar. (iii) **Survivorship (rule 9)** — U56 / B136
are current-constituent hand-kept lists, SMALL a current sub-$2B screen (tickers with max_1d_move ≥ 1.0
dropped). Delisted, acquired and bankrupt names are absent, which flatters momentum books and the drawdown
leg specifically, so every margin here is an upper bound.

Script: `research/backtests/2026-09-18_does-the-CERTIFIED-U56-g0.65-BOOK-survive-25-and-50-bps-COSTS_cloud.py`
