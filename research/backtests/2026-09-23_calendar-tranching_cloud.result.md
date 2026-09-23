# RESULT — idea 2408, does calendar tranching cut the candidate's turnover without the damper's stub?

**2026-09-23, lane cloud, run 44. ANSWERED = NO. KILL of the rota as a turnover device.**
No new KEEP-candidate; no rule change. `RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

1. **What was priced.** A ROTA: assign every investable name to one of k fixed tranches by a
   price-blind hash `md5(ticker|salt) mod k`, rebalance tranche `week mod k` IN FULL each week,
   leave the rest to drift. k {1, 2, 4, 8} x 4 salts x 2 books (CAP2, CAND) x 2 panels x 2 gross
   x 4 rungs, with idea 2391's partial-adjustment damper at lam {1, 0.5, 0.25, 0.125} priced
   alongside as a reference. 544 rows, 14 of 15 gates.
2. **The idea's structural claim is TRUE.** The traded-name stub is **exactly 0.000e+00 at every
   one of 104 rota books** (G6), against the damper's 1.30% / 3.15% / 5.57% of NAV at
   lam = 0.50 / 0.25 / 0.125. Every name the rota trades does go exactly to target, including
   exactly to zero.
3. **And it buys nothing, because the stub that costs money is a different quantity.** A name
   gated OUT in a tranche whose turn has not come keeps its FULL stale weight for up to k-1
   weeks: book-level stale-OUT NAV is **0.76% / 2.00% / 3.90%** at k = 2 / 4 / 8 on U56 CAP2.
   The rota moves the residue from "a little in every name, forever" to "all of it in 1/k of the
   names, for up to k weeks". Reporting only the traded-name number would be the flattering half.
4. **The scale-free comparison, which is the result.** The lam = 1/k pairing is not a turnover
   match (the rota runs heavier in 100 of 128 cells), so each device is measured against its own
   undamped anchor. Turnover saved per pp of MaxDD given up: **ROTA median 0.282 x/yr per pp,
   DAMP median 0.769** — the damper is ~2.7x more efficient at the same job. Mean dSharpe against
   the anchor: ROTA **-0.0074**, DAMP **+0.0050**.
5. **G5 failed and the failure is reported, not patched.** Turnover is monotone decreasing in k in
   only 6 of 8 ladders. On the uncapped book on U56, k=2 costs MORE than k=1 (4.44x vs 4.39x at
   gross 0.75; 5.74x vs 5.68x at gross 1.00): freezing half the names lets the other half's
   targets drift further before they are re-set. A rota is not a turnover cut per se.
6. **A second rota artifact, published (G4b).** The stale equity sleeve already summed to > 1 of
   NAV at **5,391 rebalances across 49 of 136 books** and had to be de-grossed pro rata — never a
   source of leverage (G4: max gross 1.000000000), but it means the rota does not always reach
   target even inside the tranche it is trading.
7. **4b counts.** Joint both-panel 4b: incumbent (k=1) 6 of 16; ROTA k=2 24 of 64 (the same 37.5%
   rate — no gain); k=4 7 of 64; k=8 **0 of 64**. Damper: 6 of 16 at lam=1.00 and 0.50, 0 of 16
   below. `L_DD` is the binding failure on 49 of 60 / 84 of 89 / 101 of 101 of the k = 2 / 4 / 8
   FAILs. **0 of 544 rows pass 4a.**
8. **Rule 8 is the independent kill.** (k, salt) fitted on <= 2016-12-31 only, 2017-2026 read
   once: 64 picks, 64 of 64 beat SPY's OOS Sharpe (they are still the candidate book), but 27 of
   64 land on **k = 8, the single worst setting for 4b (joint 0 of 64)**, of which only 3 carry a
   full-sample 4b pass. Only 13 of 64 land on the incumbent, and only 11 of 64 both beat the
   incumbent's OOS Sharpe and hold a 4b pass.
9. **Noise band, and one definition that does not reproduce run 39's.** Four independent tranche
   assignments give a salt sd of turnover of 0.011-0.088 x/yr and of Sharpe 0.007-0.024 at k=8, so
   the k effects are well outside assignment noise. This run's `fidelity` (share of WANTED names
   actually held) reads 100% for the damper at every lam and does NOT reproduce run 39's 76.1%;
   run 39 measured a different quantity under the same word and nothing here rests on matching it.
   Run 39's other findings are reproduced in kind (positive stub at every lam < 1; mean names held
   rising 37.6 -> 49.5-51.8).
10. **Survivorship (rule 9).** U56 and B136 are current constituents of their screens held from
    2008, so absolute levels are biased upward and `L_CAGR` is the contaminated leg. The
    rota-vs-damper contrast is same-tape, same-day and same-target, so it is first-order immune;
    the absolute 4b verdicts are not.
