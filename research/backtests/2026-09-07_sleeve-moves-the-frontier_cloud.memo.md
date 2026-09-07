# MEMO — 4b KEEP-candidate: equal-weight book + a 25% macro sleeve (idea 139 by-product, 2026-09-07 cloud)

1. **The book.** Equal-weight every priced name at 0.75 gross (idea 94's `EWall`), blend 25% of a
   three-asset macro sleeve (TLT/GLD/UUP, ideas 100/104's momentum-vote x risk-parity), rescale to
   0.75 gross, rebalance weekly, execute t+1. No ranking, no trend gate, no vol filter, no leverage.
2. **The numbers, 10 bps, 2009-01-13 → 2026-09-04.** u56 **11.22% / Sharpe 1.2331 / MaxDD −16.67%**,
   halves **1.327 / 1.160**, OOS Sharpe **1.221**; broad **11.93% / 1.2370 / −18.50%**, halves
   **1.372 / 1.118**, OOS **1.196**. At 25 bps: u56 10.84% / 1.1943 / −16.72%; broad 11.54% /
   1.1997 / −18.57%. Turnover 2.29x (u56) / 2.33x (broad) per year.
3. **KEEP path 4b, all five bars, both panels, both cost rungs.** SPY 15.23%, halves 0.957/0.834,
   MaxDD −33.72% ⇒ bars CAGR ≥ 10.66%, MaxDD ≥ −20.23%. Every bar clears with margin; the binding
   one is the CAGR floor (+0.56 pp on u56, +1.27 pp on broad at 10 bps). **4a fails** — it does not
   beat RULES v2 in both halves — so this is a 4b candidate only, which is the path PROTOCOL says
   matters for capital.
4. **Rule 8.** Choosing f on 2009–2016 alone (argmax IS Sharpe among arms clearing 4b's four
   IS-evaluable bars) picks **f = 0.25 in 7 of 8** admitting cells and f = 0.20 in the eighth; the
   pick clears all three OOS 4b bars in **7 of 8** (fails only broad/TOP20 @25 bps). The dial was
   not fitted on the second half.
5. **It is not a de-grossing point.** At its own drawdown, simply holding less of the same book
   returns **1.66 pp/yr less** (u56) and **1.93 pp/yr less** (broad); the arm's mean gross is
   0.7502 against the control's 0.7502 — it buys drawdown with mix, not exposure.
6. **It is not knife-edged in f.** On this book the 4b-passing window is **f = 0.10–0.25 on u56
   and f = 0.20–0.25 on broad, at BOTH cost rungs** — f = 0.05 (and 0.10–0.15 on broad) fails the
   DD cap, f = 0.50 fails the CAGR floor. The window is an interior plateau, not a grid edge, and
   f = 0.20–0.25 is the intersection that holds on all four panel x rung cells.
7. **Exact RULES wording, if Sunday review adopts it.**
   > **Universe.** Every instrument priced that day in `research/universe.json`.
   > **Sleeve.** S = {TLT, GLD, UUP}. For each s in S on day t: `vote(s)` = the fraction of
   > {12-1m, 6m, 3m} total returns that are > 0; `rp(s)` = (1/60d stdev of daily returns)
   > normalised to sum to 1 over S. Sleeve weight `sl(s) = vote(s) * rp(s)`.
   > **Equity leg.** `eq(i) = 0.75 / N` for each of the N priced names.
   > **Book.** `raw = 0.75 * eq + 0.25 * sl`, then scale every weight by `0.75 / sum(raw)`.
   > **Cadence.** Rebalance weekly to those weights; orders decided at Friday's close execute at
   > the next session's close. No shorting, no leverage, no daily override.
8. **What is NOT claimed.** No 4a. No small-cap panel (TLT/GLD/UUP are not in it). No claim that
   the sleeve is a uniquely off-ladder instrument — this run's main result KILLS that; the 200d
   gate and the 3% band beat their own matched-drawdown ladder points at nearly the same rate.
9. **Risks, stated first not last.** (a) The sleeve's contribution is partly an asset-class fact
   about 2009–2026: TLT is IS 3.77% / OOS −0.97%, GLD IS 3.91% / OOS 14.55% — the momentum vote is
   what carries it across that reversal, and a sample with all three legs dead at once is not in
   this record. (b) Turnover nearly triples against the plain equal-weight book; the 25 bps rung is
   reported and still clears, but nothing here prices market impact. (c) Survivorship (idea 54)
   inflates the equity leg. (d) MaxDD is one number off one path.
10. **Blocked on.** Ideas 105/106 (how a sleeve is written into RULES at all) and idea 395 (does
    the sleeve earn anything over its own de-grossed control). On 395's question this run is
    evidence, not a verdict — 395 owns it — and the evidence says **yes**: over the eight EWall
    f = 0.20/0.25 cells the sleeve returns **+1.26 to +1.93 pp/yr more** than its own book
    de-grossed to the same drawdown, and over every EWall sleeve arm the range is +0.29 to +2.79.
    Not proposed for RULES this week; filed for Sunday review.
