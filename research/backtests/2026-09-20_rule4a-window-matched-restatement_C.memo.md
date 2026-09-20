# Idea 1631 — should PROTOCOL rule 4a be restated as a window-matched test?  **No. ANSWERED / KILL.**
*(lane C, 2026-09-20. Corpus 33 books x 2 panels = 66 committed cells (52 real, 14 NULL), 10 bps, weekly,
U56 + B136. Script `2026-09-20_rule4a-window-matched-restatement_C.py`, cells in the sibling `.csv`.)*

1. **All three restatements are cosmetic.** Across 13 grid points, the most any one moves is **1 of 66
   cells**. R1 (own active window) moves **0**; R2(p) moves 1 at p<=0.60 and 1 at p>=0.80; R3(m) moves 1
   at m>=0.05. Rule 4a's adjudication of this record is not knife-edge and no rewording rescues it.
2. **(i) is a NO-OP BY CONSTRUCTION, not a null result.** Window-matching needs a device that is
   sometimes off. Every committed book is deployed on ~100% of days and its held weights differ from
   the baseline's on **44 of 52 cells at diff-share 1.000** (min 0.944). R1a (gross>0) and R1b (book
   differs from the baseline's) each reproduce R0 on **52/52 real and 14/14 null**. 1602's complaint is
   real, but the device's own active window is not where the fix lives.
3. **(ii) and (iii) only ever move the SAME two cells.** p<=0.60 admits B136 DEGROSS G=0.25, which misses
   R0 by **0.0017 of H1 Sharpe**; p>=0.80 and m>=0.05 eject B136 VOLTGT t=0.08, the record's sole R0
   passer (dSharpe +0.0370 / +0.1049, dMaxDD +1.38 pp). Both are boundary cells, not verdicts.
4. **NO restatement admits a NULL.** 0 of 14 no-signal books (seeded random-k, week-parity, per-row
   score shuffle, Bernoulli band at the live in-band rate; gross-matched) pass at **any** of the 13 grid
   points on either panel. Loosening 4a is safe here — it just buys nothing.
5. **The real binding leg is GROSS, wearing a drawdown clause.** Of 51 failing books, **41 trip MaxDD**
   and 42 trip a Sharpe leg; 28 fail BOTH halves. Mean min-half Sharpe margin **-0.0894** (10 of 52
   positive); mean dMaxDD **-5.42 pp** (11 of 52 shallower). The live book is a de-grossed 0.75-gross
   band, so anything carrying more equity draws deeper. All three proposals rewrite the SHARPE legs.
6. **Rule 8 (p, m fixed on 2009-2016 rows only; 2017-2026 read once).** No null passes at any rung on IS,
   so the pre-registered "tightest rung admitting no null" is unidentified and lands at p=0.50 / m=0.00
   on both panels. Every restatement with a non-empty IS pass set then picks the **same** book per
   panel: U56 MADIST q=0.50 **7.42% / 1.1757 / -10.67%**, B136 DEGROSS G=0.25 **4.55% / 1.0891 / -9.03%**,
   against RULES v2 OOS 9.46% / 1.2766 / -12.05% and 7.85% / 1.1017 / -12.24%, and SPY OOS 15.26% /
   0.8737 / -33.72%. **Both fail 4a and 4b OOS** (CAGR 48.6% and 29.8% of SPY's, under the 70% floor).
   No restatement selects a better book than the one the record already runs.
7. **VOLTGT t=0.08 on B136 is a FULL-SAMPLE-ONLY pass and is PARKED, not kept.** It clears 4a on the full
   sample on one panel, fails 4a on U56 (margin -0.025, DD -12.3 vs -12.05 pp), and does **not** pass on
   the 2009-2016 IS rows at all — rule 8 calls that PARK by name.
8. **PROPOSED RULES WORDING: none. Leave PROTOCOL rule 4a exactly as written.** The record should instead
   record the reason: *path 4a's drawdown clause is a GROSS test. Measured against a 0.75-gross de-grossed
   incumbent it fails 41 of 51 committed books, 28 of which also lose both Sharpe halves, so rewording the
   Sharpe legs — by window, by block share, or by margin — moves at most 1 of 66 verdicts. Judge a
   growth book on path 4b, which is what 4b was added on 2026-09-04 to do.*  **PROPOSED, NOT ENACTED**
   (rule 6: Sunday review only; RULES.md untouched).
9. **GATES 6/6.** G1 cost axis exact off the zero-cost rung, `r(c) = r_gross - turnover*c/1e4`, vs a fresh
   10 bps engine run: **0.000e+00** both panels. G2 the (band 0.03, G 0.75, W) cell replays
   `baseline.rules_v2_weights`: **0.000e+00** both panels — that cell IS the live book. G3 13 rolling 5y
   blocks, G4 3 inside IS. G5 exactly two tuned parameters (p, m); device rungs are the corpus, not knobs.
   G6 no chooser statistic reads a 2017+ row, **tested on a hard-truncated array: 0.000e+00** both panels.
   Deterministic, offline, 97s. Every grid point published.
10. **SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists, so every ABSOLUTE level here —
    the pass counts and the OOS levels included — is an **UPPER BOUND**. The result that carries this memo
    is a count of verdict MOVES: the same books, on the same days, adjudicated under different wording.
    That contrast is first-order immune. The pass counts are not.
