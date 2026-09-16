# Memo — the U56 `n = 12, H = 21` 4b candidate, re-priced on the cost ladder (idea 1094, lane C, 2026-09-16)

1. **Status.** This memo UPDATES `2026-09-16_is-the-EDGE-HUMP-a-MIN-HOLD-artefact_cloud.memo.md`; it
   does not replace the candidate or propose a new one. The cell still clears PROTOCOL **4b**
   full-sample and out of sample on U56, and now does so at **25 and 50 bps as well as 10**.
   **This lane does NOT recommend promotion.** Rule 6 permits one rules change per week via Sunday
   review; the wording below is on file so the decision is made on the wording, not a description.
2. **Exact RULES wording, if it were ever promoted (unchanged from 1086's memo except the cost
   clause, which is the only thing this run touches):**
   *"On the last trading day of each week, score every instrument priced that day by the mean of its
   percentile ranks on three momentum legs — return from 252 to 21 trading days ago, return over the
   last 126 days, return over the last 63 days — multiplied by 1.0 if its close is above its 200-day
   moving average and by 0.5 otherwise. An instrument is ELIGIBLE if its close is above its 200-day
   moving average and its 20-day realised volatility is below 60% annualised. RETAIN, regardless of
   eligibility, every currently-held name entered fewer than 21 trading days ago that is still
   priced. Then fill the remaining slots, up to 12 held names in total, with the highest-scoring
   ELIGIBLE instruments that are not among those retained — a name held 21 trading days or longer
   competes for its own slot on equal terms with every other eligible instrument, and its holding
   clock restarts if it is re-selected. Weight every held name equally at 0.75 of NAV divided by the
   number held, whatever that number is; the remaining 0.25 of NAV is cash. Weights are decided at
   that close and applied the next trading day. The rule is priced at 10 bps per unit turnover and
   is warranted only while realised round-trip cost stays below 60 bps; above that it no longer
   clears 4b."*
3. **What it delivers on the cost ladder, all 11 rungs published.** CAGR / Sharpe / MaxDD, full
   sample: **17.64% / 1.2131 / −19.45%** at 0 bps, **16.80% / 1.1625 / −19.48%** at 10, **15.54% /
   1.0865 / −19.51%** at 25, **13.48% / 0.9595 / −19.61%** at 50, **11.46% / 0.8322 / −19.75%** at
   75. OOS (2017-2026, read once): **17.57% / 1.1426** at 10 bps, **16.26% / 1.0685** at 25,
   **14.11% / 0.9448** at 50. Turnover **7.19x/yr** (1.80 pp of drag at 25 bps, 3.59 pp at 50).
4. **Breakeven.** All five 4b legs and all three OOS legs hold to **c\* = 63 bps** (OOS 64); the
   first failure at 64 bps is **L_H1** — the first-half Sharpe falling under SPY's 0.9588 — with the
   CAGR floor still clear by +0.9 pp at 75 bps. The pass set is contiguous from 0 bps.
5. **The queue's objection is answered and is smaller than it looked.** Its 2.4x turnover ratio
   against `H = 126` at the same n buys a **1 bp** difference in breakeven (63 vs 64), because the
   H = 126 cell binds on drawdown, a leg cost barely moves: over 0→50 bps a cell loses 1.7-4.7 pp of
   CAGR and gains only 0.07-0.51 pp of |MaxDD|.
6. **Reason 5 of the earlier memo is therefore WITHDRAWN, and a better one replaces it.** What an
   IS-only procedure can REACH is far more cost-fragile than what the cell delivers: at **15 bps and
   above U56's IS-Sharpe chooser stops picking this cell** and switches to (n = 5, H = 63), which
   fails 4b at every rung. Reachable 4b passes survive only to 30 bps (C_ISDD's n = 40, H = 21) and
   none at 40. **Above 10 bps this candidate is a cell no honest procedure selects.**
7. **Reasons 1-4 stand untouched.** The binding leg at 10 bps is drawdown with a **+0.753 pp**
   margin against a quantity idea 1083 measured at 4.1-7.2 pp of 90% width; the identical
   construction on B136 fails 4b outright; the hold is not stably choosable (choosers split 21/21/63);
   and **0 of 594 (cell, rung) pairs clear 4a anywhere on this grid.**
8. **It is not a coin flip, and that is the one thing in its favour.** 40 gross-matched random-rank
   draws at the same cell clear 4b at 0.050 / 0.025 / 0.000 at 0 / 10 / ≥15 bps, with median c\* of
   **9 bps** against the book's 63; the book sits at percentile 1.000 of that distribution.
9. **Evidence.** Gates **12 of 12**, printed before any result number: the exact cost ladder equals
   `engine.backtest` at 10, 25 and 50 bps to 1.39e-17, and **1086's committed candidate reproduces
   bit-identically (0.00e+00)** on both triples. Script
   `2026-09-16_does-the-U56-n12-H21-CANDIDATE-survive-25-and-50-bps_C.py`; grid, breakeven, rule-8,
   null and benchmark CSVs committed.
10. **Survivorship (rule 9).** U56 is a CURRENT-CONSTITUENT list, so every level above is optimistic,
    the 4b pass is an UPPER bound, and **c\* = 63 bps is an upper bound on the cost a real book of
    this shape could have paid.** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py`
    are untouched by this run.
