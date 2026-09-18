# Memo — idea 1268 (lane B, 2026-09-18): the idle sleeve, and why the DURATION part of it is not capital

1. **Question.** Six dials say the committed 2026-09-04 4b pass is decided by the DRAWDOWN leg alone, and
   the three mechanisms priced for buying that leg (1262 brake, 1263 vol target, 1264 inverse-vol sizing)
   all cut EQUITY EXPOSURE and so all confound "the risk clause worked" with "less equity was held".
   The committed book parks a constant 25% of NAV in cash; this run asks what that idle sleeve should hold,
   with the equity book **bit-identical at all 180 cells** (gate G2: the 30 FILL-0 rows are one book, 0.000e+00).
2. **It works — and it is the FIRST mechanism in this line that buys the DD leg without paying return.**
   Pooled over the 24 non-SPY cells at FILL 1.00 against each cell's own CASH anchor: d_CAGR **+0.70pp**,
   d_Sharpe **+0.0400 (positive 30 of 30)**, d_OOS_Sharpe **+0.0116**; SHY and IEF improve MaxDD at **6 of 6
   arms at every FILL** (IEF +0.73pp at FILL 1.00). 12 cells convert a committed 4b FAIL into a PASS.
3. **Best cell.** U56/COMPOSITE3 IEF@FILL 1.00 = **16.41% / 1.2077 / -18.53%**, halves 1.3285/1.1264,
   OOS 1.2022, turnover 3.02/yr — **strictly dominating** the committed anchor (15.78% / 1.1522 / -19.13%,
   halves 1.2127/1.1128, OOS 1.1832, 2.75/yr) on CAGR, Sharpe, MaxDD, both halves and OOS. 4b PASS.
4. **And the SHY control kills the duration story.** The engine pays 0% on cash, so SHY@FILL 1.00 is
   approximately the bill rate the book should already have been earning (1193's point, here with a HELD
   asset instead of an rf assumption) — not a strategy. Measured against SHY at the same FILL on the same
   equity book, the duration excess is **IS-only and reverses out of sample at 0 of 24 for every duration
   rung**: d_OOS_Sharpe IEF **-0.0044 (0/24)**, TLT **-0.0192 (0/24)**, LQD **-0.0145 (0/24)**, monotone in
   duration and growing with FILL (IEF -0.0012 -> -0.0082 across FILL 0.25 -> 1.00).
5. **Rule 8 as declared refuses the idea.** Choosing (SLEEVE, FILL) on warm-up..2016-12-31 IS Sharpe and
   reading 2017-2026 once picks **TLT @ FILL 1.00 at 6 of 6 arms** and **loses OOS Sharpe at 6 of 6**
   (mean **-0.0110**, IS/OOS rank corr +0.01..+0.31). The chooser buys the 2009-2016 duration bull.
6. **Post-hoc (declared as such, not pre-registered).** With the sleeve FROZEN, FILL is the only dial and
   rule 8 picks FILL 1.00 everywhere, beating do-nothing at 6 of 6 for SHY (+0.0257), IEF (+0.0175) and
   TIP (+0.0253) and 0 of 6 for TLT. But IEF's FILL-only pick still sits **-0.0082 of OOS Sharpe BELOW the
   SHY control at 0 of 6**, so what the chooser can reach is the bill rate, not duration.
7. **Stress.** In 2022 every sleeve is WORSE than cash on U56/COMPOSITE3 at FILL 1.00: cash -7.12%,
   SHY -8.08%, TIP -10.17%, IEF -10.86%, LQD -11.67%, TLT -15.19%. The full-sample gain is a falling-rate fact.
8. **Duration is nonetheless not merely "being invested":** H_DUR held 24 of 24 — the best duration sleeve
   beats the SPY equity fill on MaxDD at every matched FILL, and the SPY fill costs full Sharpe (-0.0030
   vs SHY) while adding 2.08pp of CAGR and 4.54pp of drawdown. 4a is 0 of 180 (live v2's -12.05% again).
9. **VERDICT: KILL (capital). Nothing enacted, no RULES change (rule 6), no PROTOCOL edit.** One cell is
   PARKED for the record — U56/COMPOSITE3 **SHY@FILL 1.00** (16.15% / 1.1774 / -18.87%, halves 1.2325/1.1432,
   OOS **1.2126**, 3.00/yr), the only strictly-dominating 4b pass a one-dial honest chooser reaches — and this
   memo **recommends AGAINST enacting it as a rule**, because it is a MEASUREMENT convention (pay the idle
   sleeve the bill rate) and not a signal. Its home is a Sunday-review PROTOCOL argument, alongside 1193's
   finding that the record's implicit 0% cash is its strictest convention, not a v3 of RULES.md.
10. **SURVIVORSHIP (rule 9).** U56/B135 are current-constituent lists and SMALL663 a current sub-$2B screen
   (52 of 715 dropped for max_1d_move >= 1.0), so every LEVEL here is optimistic and the 4b passes are upper
   bounds — they clear on the drawdown leg, the leg a survivorship-free panel would hurt most. The headline
   is a CONTRAST between sleeves on an identical equity book and identical dates, and is first-order immune;
   the 4a/4b legs are not. Costs 10 bps, next-day execution, 21 of 21 gates, 28s, offline, deterministic.
