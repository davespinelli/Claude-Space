# MEMO — idea 247: a 4b KEEP-candidate for a Sunday review (NOT adopted here)

1. **What it is.** Idea 246's PARKed arm survives the repair. Hold every priced U56 name at
   75%/N of NAV; on days when SPY's 20-day realised vol is at or above a FIXED threshold,
   de-gross into the RULES v2 200d ±3% band instead (gated weight goes to cash, never
   re-spread). Weekly, next-day execution. Threshold = the 80th percentile of SPY vol20 over
   2009-01-13..2016-12-31 only, frozen thereafter: **θ = 0.2125 annualised**.
2. **Why the repair mattered.** idea 246's expanding 80th percentile armed **3.3% of IS days
   (67) against 17.1% of OOS days (415)**, so rule 8 chose it on a regime it barely saw. The
   frozen IS threshold arms **15.5% IS / 16.4% OOS** — mean |IS−OOS coverage gap| falls from
   14.4% (EXP80) to 3.6% (ISFIX). The pass is not an estimator artefact.
3. **Full sample (2009-01-13..2026-09-08, 10 bps):** CAGR **11.05%**, Sharpe **1.2201**,
   MaxDD **−15.49%**, halves **1.3483 / 1.1100**, turnover 1.74× NAV/yr, mean realised gross
   0.6803. At 25 bps: 10.76% / 1.1906 / −16.05%, halves 1.3211 / 1.0784.
4. **vs SPY (the 4b bar):** SPY 15.19% / 0.8871 / −33.72%, halves 0.959 / 0.829. Sharpe beats
   SPY in both halves and OOS; MaxDD −15.49% is inside 0.60 × −33.72% = −20.23%; CAGR 11.05%
   clears 0.70 × 15.19% = 10.63%. **4b PASS at both cost rungs.**
5. **Rule 8 (params on IS ≤ 2016-12-31, 2017-2026 read once):** the IS chooser picks q = 0.80
   on U56 at both rungs and **never picks the defective EXP80 (0/6 cells)**. OOS: **11.19% /
   1.2077 / −15.49%** (25 bps: 10.88% / 1.1769) against SPY OOS 15.38% / 0.8786 / −33.72%.
   **OOS 4b PASS.**
6. **It beats its own matched-realised-gross control.** EW_ALL at nominal gross 0.6800 (same
   realised 0.6803, matched to 4.2e-13) earns Sharpe 1.1226 full and 1.1336 OOS: the arm adds
   **+0.0975 of Sharpe full and +0.0741 OOS**. This is not idea 244's gross channel.
7. **What it costs, stated plainly.** The matched control earns **+0.95 pp/yr MORE CAGR**
   (12.00% vs 11.05%). The arm buys **5.1 pp less drawdown** (−15.49% vs −20.59%) with that
   0.95 pp. Anyone who does not want that trade should hold the control.
8. **Margin (idea 408).** The binding bar is the CAGR floor, and the margin is thin:
   **+0.42 pp at 10 bps, +0.13 pp at 25 bps**, against a q-step worth ~0.6–0.8 pp of CAGR —
   i.e. **~0.6 and ~0.2 grid steps**. The 4b region in q is contiguous and 2 of 4 points wide
   ({0.80, 0.90}); q = 0.60 and 0.70 fail the CAGR floor, not the Sharpe or DD bars.
9. **Where it fails.** 4a: **0 of 66 points** — live RULES v2 has the higher OOS Sharpe
   (1.2817 vs 1.2077); this candidate buys CAGR (+2.4 pp/yr full) at slightly lower Sharpe.
   SMALL439: every arm LOSES to its matched control (dSharpe −0.003 to −0.19). B136's rule-8
   pick clears 4b in sample but misses the OOS CAGR floor by 0.21 pp. **U56 only.**
10. **Exact RULES wording if a Sunday review adopts it** (RULES.md is NOT edited by this run):
    > **Clause 2 (replaces the unconditional band).** Compute SPY's 20-day realised volatility
    > (annualised, √252). If it is **≥ 0.2125**, the book is ARMED: hold each instrument whose
    > close is inside the 200-day moving-average +3% / −3% band (hysteresis per RULES v2) at
    > `0.75 / N` of NAV, N = instruments priced that day; weight released by the band goes to
    > CASH and is never re-spread. If SPY vol20 is **< 0.2125**, the book is DISARMED: hold
    > every priced instrument at `0.75 / N` of NAV with no band test. Rebalance weekly on the
    > last trading day; weights decided at close t are applied at close t+1. The 0.2125
    > threshold is a FIXED constant, never re-estimated.

SURVIVORSHIP: U56 is a fixed ETF/mega-cap list (the least biased of the three panels); B136
and SMALL439 are current-constituent lists and their levels are biased upward. The
load-bearing number here is the arm-minus-matched-control contrast inside U56, not any level.

Script: `research/backtests/2026-09-08_fix-hivol80s-IS-OOS-coverage-and-re-read-the-parked-arm_cloud.py`
