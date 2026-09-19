# Memo — idea 1602 (lane B, 2026-09-19): the cash leg wants an ACCRUAL, not an ETF

**Script** `research/backtests/2026-09-19_zero-duration-cash-leg_B.py` · 450 grid cells + a 492-cell
break-even scan, all published · gates 10/10 · 123 s, offline, deterministic.

1. **The question.** Ideas 1358 / 1498 / 1555 / 1547 credit the band's idle NAV with SHY and publish the
   result as a property of the RULE. SHY is a duration-bearing ETF (own MaxDD -5.71%, -3.88% in 2022). This
   run replaces it with a synthetic ZERO-DURATION accrual — a constant daily rate, no mark to market — on
   the same names, days, frame and F ladder, and separates CARRY from DURATION.
2. **Duration contributes nothing.** SHY minus its carry-matched zero-duration twin (MATCH1, flat accrual at
   SHY's own realised 1.31%/yr) over 6 panel-frames at F = 1.00: **dCAGR -0.0024 pp, dSharpe +0.0009,
   dMaxDD +0.033 pp**. Against the era-matched twin (MATCH2): **dSharpe -0.0003**, and on the HIKE era
   **0 of 6**. The twins pass 4a on **3 of 6** panel-frames against SHY's **2 of 6** — SHY's duration costs
   the SMALL/LIVE pass outright (MaxDD -13.78% vs the twin's -11.46%). **The credit is pure carry.**
3. **So the clause SURVIVES the removal of duration.** Restated as an accrual it clears path **4a FULL and
   OOS on all three LIVE panels** at any flat rate ≥ 1.00%/yr (U56 a\* = 0.75%, B136 1.00%, SMALL 0.25%;
   0.25% on all three if the sweep is free of transaction cost). It does not touch 4b: the CAGR floor still
   binds (U56 LIVE 9.01% vs a 10.59% bar), 4b unchanged at 5 of 30.
4. **But the flat rate is a counterfactual.** A sweep paid ~0 through the ZIRP years; SHY's 0.91%/yr there
   was roll and duration return, not a cash rate. Under the ERA-HONEST shape (0 before the FOMC's first
   2022 hike, a after), 4a passes **0 of 492** — every rate to 10%/yr, both cost conventions.
5. **And the reason is structural, proved not scanned (G10).** 4a's first leg is a STRICT inequality against
   the live book's first-half Sharpe. This tape's halves split at ~2017, so the WHOLE first half is ZIRP; an
   honest sweep earns nothing there and the book is bit-identical to the live one (max |daily diff| 3.8e-17).
   **Equal is not greater. Path 4a has no window in which to see a cash-leg rule at all.**
6. **Rule 8 is blind for the same reason.** The IS window (warm-up..2016-12-31) is entirely ZIRP, so the
   IS-Sharpe chooser over F picks **F = 0.00 on 18 of 18 era-honest cells** — it declines the sleeve at every
   rate. Yet that same sleeve at a 5% post-2022 rate would have returned OOS **10.57% / 1.4167 / -12.07% on
   U56/LIVE against the live book's 9.46% / 1.2769**, +0.140 of Sharpe. The record's two licensing devices
   both look only where the answer cannot appear.
7. **F is not a free parameter.** OOS Sharpe is monotone non-decreasing in F on **78 of 78** (arm, panel,
   frame) cells, and a real book has no reason to leave idle cash uncredited. F = 1.00 is forced, so the
   restated clause ships with **zero tuned parameters**; the rate is observed, not chosen.
8. **EXACT RULES WORDING, if the Sunday review enacts it (PROTOCOL rule 6 gives it that call; nothing is
   enacted here).** Replace clause 6 with: *"CASH LEG. Weight gated out by clause 2 is held as CASH, in
   full, and is credited with the broker sweep rate actually paid on that balance, accrued daily. The cash
   leg buys no instrument: it bears no duration, no credit risk and no transaction cost. Every backtest
   states the accrual path it assumed; where the realised rate is not observable the pre-registered path is
   0.00%/yr before 2022-03-16 and the prevailing sweep rate thereafter."*
9. **And the companion PROTOCOL clause this run earns:** *"A rule whose effect is confined to one monetary
   regime may not be adjudicated by path 4a's half-sample legs or by rule 8's 2009-2016 IS window, both of
   which sit inside ZIRP. Certify it on the window in which it can act, and say so."*
10. **Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen
    carried back to 2010 — every absolute level is an UPPER BOUND. The SHY-vs-twin contrast is same names,
    same days, same frame, and both arms inherit the identical bias. **Verdict: KEEP-4a confirmation for the
    accrual restatement, KILL for the era-honest form on path 4a, and a documented defect in path 4a itself.**
