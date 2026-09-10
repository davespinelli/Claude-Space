# KEEP-candidate (PROTOCOL path 4b) — VOLQ60 half-gross overlay on the top-20 book (U56)

1. **Source.** Idea 601 (cloud, 2026-09-10), script
   `research/backtests/2026-09-10_re-read-every-published-EXPANDING-QUANTILE-verdict-at-w-1008_cloud.py`,
   full rule-8 chooser cell U56/CAND20; 1,728 arm-rows committed, all reported.
2. **Exact RULES wording proposed.** *"Hold the top 20 names on the composite score (no vol
   scaler) at equal weight, gross 1.00, rebalanced weekly. On each rebalance day, if the panel's
   20-day realised volatility (equal-weight panel return, annualised) is at or above the 60th
   percentile of its own history to date (expanding, minimum 252 observations), hold half that
   weight and the rest in cash; otherwise hold full weight. Decisions at the close of t are
   executed at t+1."*
3. **4b evidence at PROTOCOL's own rung (10 bps, weekly, next-day fill, U56, eval from
   2009-01-13).** CAGR 15.45% / Sharpe 1.115 / MaxDD -18.78%; halves 1.149 / 1.081; OOS
   (2017+) CAGR 16.14% / Sharpe 1.164 / MaxDD -18.78%. SPY: 15.23% / 0.889 / -33.72%, halves
   0.957 / 0.834, OOS 0.882. All five 4b legs clear.
4. **It survives 25 bps**, which the record's 4b passers usually do not: 13.08% / 0.964 /
   -18.94%, halves 0.996 / 0.933, OOS 1.017 — still every leg. Only 4 of 570 gated arms in this
   run pass 4b at 25 bps and all four are this panel and this base book.
5. **Rule 8.** The whole configuration (state series, quantile level, instrument) was chosen on
   the first half by IS Sharpe alone; every number in 3 and 4 is the untouched second half plus
   the full sample. The chooser was run identically on all 6 panel x base cells; this is the
   only one that passes.
6. **It is not a gross dial.** Against its matched-mean-gross static twin (the same 0.861 mean
   exposure, constant, no timing) it wins OOS on Sharpe (1.164 vs 1.131) and on MaxDD (-18.78%
   vs -20.94%). Against its own ungated parent it wins only on drawdown; the parent fails 4b on
   the DD leg alone at every cost rung.
7. **The DD leg is earned, not substituted.** Over the parent's binding decline
   (2020-02-19 -> 2020-03-12) the gate cuts 29.4% of gross; there is no zero-cover arm in the
   family. The residual MaxDD floor is the 2022 episode at -18.78%, which no gating in this run
   improves.
8. **What fails.** PROTOCOL 4a fails everywhere: 0 of 570 gated arms beat live RULES v2's halves
   (1.226 / 1.191 on U56) at 10 or 25 bps. The same clause on B136 fails 4b (H2 and DD) and on
   SMALL439 fails all five legs, so this is a U56 result and nothing wider.
9. **Caveats.** U56 and B136 are current-constituent lists (survivorship: levels optimistic,
   contrasts durable). The instrument is the causal EXPANDING quantile that this very idea shows
   fires at 0.686 of its nominal rate on U56 — the arm is a 27.4%-of-days gate wearing a "top
   40%" label; its repaired twins (BREADTH q=0.17/0.20 at w=1008, q=0.30 at w=504) also pass 4b
   at 25 bps, so the pass does not depend on the mis-calibration.
10. **Recommendation.** Take to Sunday review as a 4b candidate, not a rules change today. The
    single-panel footprint is the open question; the pre-registered next test is the same clause
    on the 2026-09-04 KEEP 4b book across fresh draw panels, not another dial on U56.
