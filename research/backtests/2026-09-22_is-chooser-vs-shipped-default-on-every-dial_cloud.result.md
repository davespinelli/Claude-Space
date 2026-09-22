# Idea 953 — is an IS-CHOSEN FREE PARAMETER worth LESS THAN ITS DEFAULT on every dial?

**ANSWERED = YES ON FOUR OF FIVE DIALS, and the fifth is a MIS-SET DEFAULT, not chooser skill.
KILL of the free parameter as a thing worth spending; PARK on the shipped `n`.** Script:
`research/backtests/2026-09-22_is-chooser-vs-shipped-default-on-every-dial_cloud.py`
(84 books x 3 cost rungs = 252 grid points in `.grid.csv`; 135 chooser-vs-default cells in
`.chooser.csv`; full console in `.console.txt`).

Design: 5 dials, each walked in ITS OWN family so the comparand is always the value the live
book actually ships — N (v1, default 5, w = 0.75/n so gross is held), MAXVOL (v1, 0.60),
GROSS (v2, 0.75), BAND (v2, 0.03), CADENCE (v2, W) — x 3 panels x 3 choosers (IS_SHARPE,
IS_CALMAR, IS_CAGR, all reading the FIRST HALF only) x 3 cost rungs. PROTOCOL rule 8 is the
whole design: IS = 2009-2017 (2011-2018 on SMALL), OOS read once.

1. **944's headline reproduces, pooled.** The chooser deviates from the shipped default in
   **118 of 135** cells (87.4%) and beats it out of sample in **49 of 135 (36.3%)** — **49 of
   118 (41.5%)** conditional on deviating. Both sit below a coin flip and within a whisker of
   944's own 34.1% on the phase dial. Median dOOS Sharpe **-0.0008**.
2. **The positive pooled MEAN (+0.0390) is one dial and nothing else.** By dial, mean dOOS
   Sharpe / OOS wins: **N +0.2674 (18 of 27)**, GROSS -0.0023 (**0 of 27**), BAND -0.0072
   (15 of 27), CADENCE -0.0070 (10 of 27), MAXVOL -0.0559 (6 of 27). **Excluding N, the pooled
   mean is -0.0181, the median -0.0028, and the chooser wins 31 of 108 (28.7%)** — worse than
   944's number, on four dials it never tested.
3. **GROSS: 0 of 27, and the mechanism is visible.** The chooser takes the END of the ladder
   (g = 1.50) in all 27 cells and buys **+5.74 pp of mean OOS CAGR with 11.20 pp more
   drawdown**. Sharpe cannot see a pure sizing move (it is gross-invariant to ~0.003), so the
   criterion is blind to the only thing the dial does. A chooser on this dial is not a bad
   chooser; it is a chooser scored on the wrong statistic.
4. **N is a mis-set default, not an edge.** On U56 the chooser picks n = 20 and gains +0.2759
   of OOS Sharpe — but **every** rung n >= 10 beats the shipped n = 5 out of sample (OOS Sharpe
   0.8144 / 0.7712 / 0.9395 at n = 10 / 15 / 20 against 0.6636 at n = 5), same on B136 (0.4903 /
   0.5866 / 0.6436 vs 0.4893). The honest reading is that **v1's n = 5 should be re-examined on
   its own**, not that an IS chooser is worth installing: a dial where the default is dominated
   by most of its ladder rewards any chooser that moves at all.
5. **Where the grid's only OOS 4b pass lives, the chooser MISSES it.** SMALL / N / **n = 3**
   clears 4b read on the OOS window (**16.43% / 1.2021 / -19.24%** against SPY OOS 15.51% /
   0.8407 / -33.72%), and all three choosers pick the DEFAULT n = 5 instead (IS Sharpe 1.2283
   against n=3's 0.8286), whose OOS is 6.13% / 0.5380 / -30.25% and fails every 4b leg. That
   book is **not a KEEP**: on the full sample it fails the H1 leg (0.8286 vs SPY 0.9026) and the
   DD cap (-24.44% against -20.23%), it is a THREE-NAME book, and it sits on the panel with the
   heaviest survivorship. It is recorded as the counter-example to "the chooser at least finds
   what is there", not as a candidate.
6. **KEEP paths across all 84 rungs: 4a is 0 of 84 at 10, 25 AND 50 bps.** 4b(full) is 4 of 84
   at 10 bps — U56 GROSS 1.00 and 1.25, B136 GROSS 1.00 and 1.25 — and 4b(OOS) is 4 of 84
   (those three plus SMALL N = 3). **Not one passer is a shipped default, and not one is an IS
   chooser's pick at 10 bps** (the two chooser picks that reach 4b OOS at all are U56 GROSS 1.25
   at the 25 and 50 bps rungs, where the higher cost pulls the argmax back off 1.50). The CAGR
   floor binds 75 of 80 fails at 10 bps, the DD cap 25.
7. **No rules change.** Nothing here earns a Sunday review. The one thing worth queueing is
   clause-level: the record's shipped `n = 5` is dominated by its own ladder out of sample on
   two of three panels.

**Survivorship:** U56 / B136 are 2026 constituent lists held from 2008; SMALL is the current
sub-$2B screen held from 2010 (719 cached names less the **54** with `max_1d_move >= 1.0`,
leaving **665 investable**; SPY joined as benchmark only, never held). The chooser-vs-default
contrast is a DIFFERENCE between two books on the same panel and cancels most of that bias; the
absolute 4a/4b verdicts do not, and are read against SPY, which is traded and unbiased.

**Costs/execution:** 10 bps per unit turnover headline (25 and 50 reported), weights decided at
close t and applied at t+1, weekly cadence except on the CADENCE dial, 260-row warm-up. Two
tuned parameters only (the dial, the chooser); all 252 grid points and 135 cells reported.
