# Memo — idea 2266 (lane B, 2026-09-22): the DD-budget chooser does NOT generalise off gross

1. **Verdict: KILL of the device as a method; no RULES change, no adoption.** It survives only on
   GROSS, the one dial where PROTOCOL rule 2's no-leverage cap leaves it zero free content.
2. **Premise confirmed.** IS MaxDD is monotone in gross on both panels and non-monotone on every
   band and top-n ladder (gate G6). The budget binds — moves the pick off its own budget-free
   argmax — at 51.4% of gross cells, 21.4% of band cells, 78.3% of top-n cells.
3. **Replication.** On the gross dial the device reproduces idea 2264 exactly: gate G4 shows
   `C_DDB_CAGR` == 2264's largest-gross rule at 70 of 70 cells, and at kappa = 0.60 it reaches
   4b-OOS at 9 of 10 panel × cost cells while the no-information incumbent reaches 0.
4. **Off gross the rule is not one rule.** Its two equally defensible tie-breaks (argmax IS CAGR
   vs argmax IS Sharpe inside the budget) agree on 100% of gross picks at kappa <= 0.70 but on
   only 5–40% of band picks and 40–95% of top-n picks, and they reverse the verdict (BAND 4b-OOS
   reach 54 of 140 vs 20 of 140, against the incumbent's 42).
5. **It loses to doing nothing.** Versus `C_LIVE`, median OOS Sharpe is −0.0399 (BAND, win rate
   12.1%) and −0.2141 (TOPN, win rate 0.4%); on the top-n dial it destroys 34 of the incumbent's
   70 4b-OOS passes. Median regret vs the OOS oracle: `C_LIVE` 0.0000 on TOPN, the device −0.1890.
6. **kappa does not transfer.** Best kappa by 4b-OOS reach is 0.60 on gross, 0.60–1.00 on band and
   0.50 on top-n; the shipped 0.60 delivers 8 of 40 there. Off gross the device carries two free
   parameters (kappa, tie-break) where on gross it carried none.
7. **Mechanism, in one line.** The device is a risk-DEPLOYMENT rule, not a selection rule: it pays
   only where more IS drawdown is mechanically more CAGR (gross: +6.84 pp OOS CAGR for 9.70 pp of
   OOS drawdown, clearing the CAGR floor idea 2270 named as the binding leg). On a selection dial
   the same trade buys 4.90 pp of CAGR for 8.80 pp of drawdown and −0.21 of Sharpe.
8. **By-product, recorded and NOT recommended (KEEP-4b):** gross-matched top-n, u56, mean deployed
   gross 0.7042, N = 40, weekly, @10 bps FULL 12.16% / 1.1997 / −16.90% (halves 1.2413 / 1.1722),
   OOS 13.58% / 1.2650 / −16.90%, turnover 3.83x/yr, vs the standing candidate's 11.53% / 1.2009 /
   −15.91%, OOS 12.67% / 1.2760 / −15.91% at 2.35x/yr. It is **not rule-8 reachable** (no legal
   chooser picks N = 40 at 10 bps) and pays 1.63x the turnover for +0.91 pp of OOS CAGR.
9. **Exact RULES wording, if a Sunday review ever adopted the by-product** (it should not, on 8):
   *"Clause 2a: of the names inside the 200d ±3% band, hold the 40 with the highest composite rank
   (12-1 momentum + 6m + 3m, percentile-ranked and averaged, no vol scaling), equal weight, sized
   so that mean deployed gross matches clause 2's; idle NAV to cash. Weekly."*
10. **Standing recommendation unchanged: no rules change this week.** The live RULES v2 book
    remains the incumbent and remains the best rung of both non-gross dials out of sample.
