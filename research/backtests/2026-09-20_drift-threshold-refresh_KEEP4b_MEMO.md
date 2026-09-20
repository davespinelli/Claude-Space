# KEEP-candidate memo (path 4b) — DRIFT-THRESHOLD SCALAR REFRESH (idea 1799, lane C, 2026-09-20)

1. **The book.** The standing VOLTGT construction — hold every priced name in the panel at equal
   weight at `g/N` of NAV, no ranking, no band, no vol filter — but the exposure scalar
   `g_t = clip(0.16 / sigma20_panel, 0, 1)` is **re-read only when the book has drifted from it by
   more than `h = 0.12`**, not on a calendar. Names re-spread monthly, 10 bps, next-day execution,
   never levered. TWO tuned dials: `t` and `h`.
2. **Path 4b, FULL, U56:** 15.62% / 1.2451 / −18.16%, halves 1.2944 / 1.2036, vs SPY 15.12% /
   0.8843 / −33.72%. All four 4b legs clear (margins: H1 +0.337, H2 +0.379, DD +2.07 pp, CAGR
   +5.03 pp).
3. **Path 4b, OOS (rule 8, 2017–2026 read once), U56:** **16.36% / 1.2810 / −18.16%** vs SPY
   15.26% / 0.8737 / −33.72% and live RULES v2 9.46% / 1.2766 / −12.05%. 4b OOS PASS, and the cell
   is one a legal IS-only chooser (`C_ISSHARPE` on 2009–2016) actually REACHES.
4. **It clears at 0 / 10 / 25 / 50 bps** — the standing VOLTGT memo's own cell fails at 50 — on
   **1.13 turns/yr** against that memo's 1.83 and live RULES v2's 1.77. B136's reached cell
   (`t=0.16, h=0.25`) also clears all four rungs: OOS 14.08% / 1.1888 / −17.93% at 1.19 turns/yr.
5. **Why it works, measured not asserted.** Through the 2020 crash the `h=0.12` book cuts gross
   1.00 → **0.254** on ~9 refreshes/yr; the calendar `R=M` book, at the *same* turnover, only
   reaches 0.687 and `R=Q` never moves. Against its own arm's turnover-matched point on the
   calendar ladder the drift trigger wins **263 of 263 cells** (mean +0.0596 OOS Sharpe,
   +4.07 pp OOS MaxDD), on all three panels, at every cost rung.
6. **It does NOT clear path 4a** (0 of every reached pick on U56): its drawdown is deeper than the
   live book's −12.05%. 4a is the wrong bar here, exactly as PROTOCOL 4b (added 2026-09-04) says.
7. **The rung is NOT certified and this is the memo's main weakness.** The IS chooser walks to the
   laziest rung of whatever `h` ladder it is given (18 of 24 picks on the top two rungs), so
   extending the ladder from 0.12 to 0.25 moves the pick and drops the U56 weekly-trade arm from
   PASS to FAIL. What this run certifies is the **TRIGGER**, not `h = 0.12`.
8. **Caveats, stated.** U56 / B136 are CURRENT constituents (survivorship); SMALL665 clears 4b
   **0 of 150** cells, for drift and calendar alike (fourth confirmation of the VOLTGT memo's A2).
   The sigma convention is fixed at `(L=20, d=0)`; idea 1771 showed the `t=0.16` rung loses 3 of 4
   defensible conventions and this run does not re-price that surface.
9. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, scan.py, bot.py and
   baseline.py are NOT modified by this run):

   > **2. Sizing.** Hold every instrument in the universe that has a price that day at `g/N` of
   > NAV, where `N` is the count of priced instruments. Let
   > `g_t = min(1, 0.16 / sigma_20)`, `sigma_20` being the annualised 20-day realised volatility of
   > the equal-weight, unlevered universe portfolio (`sqrt(252) *` the 20-day standard deviation of
   > its daily returns, computed through yesterday's close). **Re-read `g` and reset the book's
   > total exposure to it on any day on which the book's actual total exposure differs from `g_t`
   > by more than 0.12; on all other days leave the exposure alone.** The equal-weight re-spread of
   > the names runs monthly. Weight not deployed sits in CASH, is never re-spread across the held
   > names, and `g` never exceeds 1. No ranking, no momentum screen, no per-name volatility filter.

10. **Status: KEEP-candidate, path 4b, awaiting Sunday review** — and the review should weigh
    point 7: the trigger is the finding, the threshold value is not choosable in sample. Evidence:
    `research/backtests/2026-09-20_drift-threshold-refresh_C.py` (gates 8/8; `h=0` ≡ `R=D` at
    0.000e+00, calendar diagonal ≡ `engine.backtest` at 0.000e+00, standing memo reproduced at
    4.605e-05, idea 1793's oracle at 4.875e-05), `.result.md`, `.grid.csv` (420 cells published).
