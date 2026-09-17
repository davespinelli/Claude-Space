# MEMO — 4b KEEP-candidate, idea 1161 (2026-09-17, cloud). RECOMMENDATION: **PARK, do not enact.**

1. **WHAT PASSED.** A *selector*, not a new book: the live weekly CAND20 book at a
   **time-varying gross** re-chosen every 2 years by 1154's tent chooser. On U56 it clears
   4b full (11.89% / 1.1312 / -13.28%, halves 0.9507/1.2932) and 4b OOS (12.55% / 1.1801 /
   -13.28%) against SPY 13.74% / 0.8368 / -33.72% on the common span 2014-01..2026-09.
2. **EXACT RULES WORDING, if it were ever enacted.** *"Clause 3 (exposure). On the first
   rebalance of each even calendar year, for each gross level g in 0.200..1.000 step 0.025,
   compute over the trailing 1,260 trading days the three quantities M_S = (Sharpe_g -
   Sharpe_SPY)/|Sharpe_SPY|, M_DD = (0.60*|MaxDD_SPY| - |MaxDD_g|)/(0.60*|MaxDD_SPY|),
   M_CAGR = (CAGR_g - 0.70*CAGR_SPY)/|0.70*CAGR_SPY|, all on the book run at constant gross
   g with the live rules otherwise unchanged. Set the book's gross to the g maximising
   min(M_S, M_DD, M_CAGR), and hold it until the next even-year re-choice."*
3. **RULE 8 IS CLEAN AND IT IS THE STRONGEST THING HERE.** The (window, cadence) pair was
   chosen on the first half of the common span by three independent choosers; all three
   picked a rolling cell and all three cleared 4b on the untouched second half, where the
   frozen incumbent gross 0.750 **fails**.
4. **REASON NOT TO ENACT #1 — it is not a Sharpe discovery, and the walk-forward says so out
   loud.** On the second half the frozen incumbent posts a **higher** Sharpe (1.3332 vs
   1.2932) and a much higher CAGR (19.65% vs 14.73%). The rolling rule clears 4b only on the
   drawdown leg (-13.28% vs the -14.70% cap, which the incumbent misses at -15.77%).
5. **REASON NOT TO ENACT #2 — the dial is an exposure dial (1150's identity, re-measured).**
   Across the whole 33-rung U56 ladder Sharpe spans **0.0041** (1.1303..1.1344) while CAGR
   spans **16.97 pp**. Every rung is one book scaled; nothing on this dial can add Sharpe.
6. **REASON NOT TO ENACT #3 — it fails on the other panel.** B136: 0 of 12 cells clear 4b
   full, and all three rule-8 choosers fail OOS on the Sharpe leg (1.0329 vs SPY 1.0637).
   A rule that is a KEEP on one current-constituent panel and a KILL on the other is not a
   rule worth real capital.
7. **REASON NOT TO ENACT #4 — the chooser is unstable by construction.** Median move rate
   **0.833**; at the 2-year cadence *every* re-choice moves the pick, mean step 0.0685 of
   gross. A tent peaks where two noisy legs cross, the least resolvable point on a ladder
   whose Sharpe spread is 0.0041.
8. **THE ONE GENUINELY NEW FACT, worth keeping whatever happens to the rule.** The interior
   pick is a property of the **chooser**, not of 1154's single window: **361 of 368 rolling
   choices (98.1%) are interior**, and all 7 endpoint picks are gross 1.000 on B136 on
   2-3 year lookbacks ending 2021-07..2023-07, i.e. windows containing no drawdown deep
   enough for M_DD to bind. And the instability is **cheap**: median **1.18 bps/yr** of drag.
9. **HONEST DISCOUNT.** The chooser maximises trailing versions of the very legs 4b later
   tests, so the full-span pass is partly tautological; the rule-8 second-half pass is not.
   Survivorship (rule 9): current-constituent panels, so the drawdown cap and CAGR floor are
   both measured against an inflated book and the bias does not cancel out of the 4b legs.
10. **DISPOSITION.** PARK, consistent with 1154's own memo. No RULES change, no version bump,
    no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
    untouched. Re-read if and when a non-exposure leg replaces L_DD (queue idea 1163, open).
