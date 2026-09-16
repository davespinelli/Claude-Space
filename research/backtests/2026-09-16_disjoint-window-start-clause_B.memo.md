# MEMO — the DISJOINT WINDOW START clause (idea 971, lane B, 2026-09-16)

**PROPOSED, NOT APPLIED.** PROTOCOL rule 6: rules change only via Sunday review, one per week.
This memo does **not** modify RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py.

1. **What it fixes.** Idea 942's clause (i) moves 4b's halves inside the in-sample window but
   never names where that window starts. Idea 971 priced the dial: the same 900 books yield
   **21 / 19 / 19 / 21 / 2 / 3** REC5 4b passes at 0 bps under REC / w2009 / w2010 / w2011 /
   w2012 / w2013 and **4 / 0 / 1 / 0 / 4** rule-8 OOS certifications over 27 picks each.
2. **Why.** 143 of 144 destroyed rows bind on `L_H1` alone, and the `L_H1` pass rate tracks the
   **benchmark's** own Sharpe in that window, not the book's: Pearson −0.957 (pass rate) and
   −0.994 (median margin) against SPY's `L_H1` bar over the five starts.
3. **Exact RULES wording (proposed as a PROTOCOL rule 4 reporting clause):**

   > *A 4b verdict whose Sharpe halves are taken inside the in-sample window is published with
   > (a) the first date of that window, (b) the benchmark's own Sharpe in each half, and (c) the
   > book's margin over the benchmark in each half. A disjoint-halves verdict quoted without its
   > window start is reported as a two-leg verdict (`L4_DD`, `L5_CAGR`) with the Sharpe legs
   > marked UNPRICED.*

4. **Blast radius.** It changes no book and promotes nothing. It adds three numbers to any future
   4b pass read on disjoint halves, and it makes the record's one existing such family (idea
   970's `DISJ` column) self-describing.
5. **Cost.** Three scalars per published verdict; all three are already computed by
   `legs_4b` and are in this run's `.spywindows.csv` and `.mechanism.csv`.
6. **What it does NOT do.** It does not adopt clause (i). This run **KILLS** clause (i) as a
   replacement for the record's convention: a bar whose verdict count moves 16× on an unnamed
   dial is not stricter than one that fixes its windows by rule, only differently arbitrary.
7. **Capital impact: none.** The best rule-8 pick under any window start is U56/`BAND03`@g1.00
   weekly (OOS 12.67% / 1.2755 / −15.91% vs SPY 15.21% / 0.8713 / −33.72%), the book ideas 972
   and 997 already published. 4a is 1 of 135 picks. **Nothing here is promoted.**
8. **Survivorship (rule 9).** The panels are current-constituent lists, so the LEVELS above are
   optimistic; the clause rests on a window-definition contrast, which is not.
9. **Reproduction.** `research/backtests/2026-09-16_is-the-2009-2012-HALF-the-leg-that-kills-every-DISJOINT-4b-pass_B.py`,
   deterministic, gates 7 of 9 printed before any result number.
10. **Recommendation: adopt (3) at a Sunday review as a reporting clause only; do NOT adopt
    clause (i) itself, and do not change the live book.**
