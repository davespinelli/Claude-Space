# Memo — idea 263, exact wording for the Sunday review (PROTOCOL only; RULES v1 unchanged)

1. This is a **reporting** clause. It proposes no book, no position, no RULES.md edit.
2. Evidence: 34 of 138 within-family dial pairs (25%) flip sign inside 0–25 bps; 23 flip
   between 0 and 10 bps; the chooser's rung changes the walk-forward pick on 2 of 3 panels.
3. The queue's `2x turnover ratio` trigger scores precision 0.394 / recall 0.824 — it flags
   43 pairs that cannot flip (6 of them gross dials, where T and vol scale together) and
   misses 6 that do, two of them straddling PROTOCOL's own 10 bps rung.
4. The same four numbers, combined through idea 262's law, score 34/34 with 0 false flags.
5. Proposed PROTOCOL clause 12, verbatim:

> **12. Cost-rung sensitivity (report-only).** Any published comparison of two arms must
> state, beside the quoted rung, both arms' annualised turnover, both arms' annualised
> volatility, and the metric difference at 0 bps. Where those five numbers give a breakeven
> `c* = dSharpe(0)·1e4/(T_x/vol_x − T_y/vol_y)` inside 0–25 bps, the verdict must be quoted
> as rung-conditional. The turnover *ratio* is not the trigger: gross dials reach 4x ratio
> and never flip, while 1.2x pairs flip at 10 bps.

6. Back-fill cost: none in re-runs where a parent committed turnover and vol — the column is
   arithmetic (R² 0.9996, median error 0.015 bps on this run's non-null pairs). Idea 269
   censuses which committed rows carry the four numbers.
7. No leaderboard verdict is retracted by this run; the clause makes rung-conditionality
   visible, it does not reverse anything already published.
8. The clause fires on ~25% of within-family pairs, so it is not dead weight, and it is one
   line of arithmetic, so it is not a burden.
9. Scope limit: measured on real dials (cadence, n, gross, scaler, gate, band, selection) on
   U56/B136/SMALL439 only. SMALL439 is survivorship-screened current constituents.
10. Recommended action at Sunday review: adopt clause 12 as written; leave RULES v1 alone.
