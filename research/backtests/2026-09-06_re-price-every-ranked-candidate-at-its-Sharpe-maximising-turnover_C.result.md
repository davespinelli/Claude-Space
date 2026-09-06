# Idea 281 — re-price-every-ranked-candidate-at-its-Sharpe-maximising-turnover (lane C, 2026-09-06)

**ANSWERED. The queued premise HOLDS as a description and FAILS as an edge: 4 of 12 published
4b verdicts move, but every mover is a turnover extreme, and at the protocol's own 10 bps
rung the selector that picks the buffer is no better than picking blind. Verdict: KEEP-candidate
4b for one by-product (`u56 top20-200d DAILY + m=50`), no RULES change proposed.**

Script `2026-09-06_re-price-every-ranked-candidate-at-its-Sharpe-maximising-turnover_C.py`;
outputs `.console.txt`, `.census.csv`, `.grid.csv` (all 108 cells x 2 rungs), `.verdicts.csv`,
`.rungs.csv`, `.walkforward.csv`.

## What was run
The census is the 12 distinct ranked books the record published leaderboard rows for — the
same object throughout (composite = mean pct-rank of 12-1/6m/3m, NO vol scaler; eligible =
vol20 < 0.60 AND gate; top 20 equal-weight at 0.75/20, cash otherwise) across the record's two
dials: gate in {none, 200d, band3} at weekly, and cadence in {D, W, M, Q} at gate=200d, on u56
and broad. Idea 273's no-trade band is attached verbatim (j fixed at uncapped), **one** tuned
dial, m in {0,2,5,10,15,20,30,50,999}, all 108 points reported at 10 and 25 bps.

Two gates were asserted before any new number was read:
1. **12/12 census parents reproduce** their published rows (worst miss 0.037pp CAGR, 0.004
   Sharpe, 0.05pp MaxDD).
2. **m=0 nests every parent exactly**: max|weight diff| on every rebalance row and max|return
   diff| are both 0.0e+00, on all 12 books.

## The four findings
1. **The turnover curve is general, not idea 273's book.** corr(turnover, Sharpe) over a book's
   9 m-cells is negative in **10/12 books @10bps (median -0.764)** and **11/12 @25bps (median
   -0.942)**, across a per-book realised-gross span of at most **0.0071** — so it is not idea
   274's gross comparison. The two exceptions are the two MONTHLY books (u56 +0.770, broad
   +0.120): exactly the cadence at which idea 279 found the buffer's increment collapsing.
2. **4 of 12 published 4b verdicts move @10bps** (5 of 12 @25bps): three KILL -> KEEP (u56
   200d/D, u56 200d/Q, broad 200d/D) and one KEEP -> KILL (u56 none/W, whose Sharpe rises
   +0.141 — the biggest gain on the board — while turnover falls 9.53x -> 0.87x/yr and the book
   drops through the 4b CAGR floor at 8.8% vs the 10.68% bar). **4a is 0/12 before and after,
   and 0/216 over every cell**: no ranked book, buffered or not, beats the live RULES v2 book.
3. **The moves survive the rule-8 selector at the verdict level and not at the OOS-Sharpe
   level.** m picked on 2009-2016 alone gives the IDENTICAL 4b verdict to the oracle
   full-sample m in **12/12 books at both rungs** — the m-curve is a plateau, not idea 171's
   island. But @10bps the rule-8 arm beats its own parent OOS in only **7/12** and beats the
   grid MEAN in **4/12**, i.e. worse than picking any m blind (median Spearman(IS,OOS) over the
   9 cells +0.213). At 25 bps the same selector is informative (10/12, 9/12, +0.558). The gain
   is a cost effect that the 10 bps rung is too small to make selectable.
4. **Every mover sits at a turnover extreme.** The two KILL->KEEP Sharpe movers are the DAILY
   parents (23.0x and 32.2x/yr); the third is the quarterly book whose binding axis is drawdown
   (-27.12% -> -19.06%, bar -20.23%), not Sharpe. The three broad WEEKLY near-misses that miss
   4b on H2 alone do **not** move: broad 200d/W goes 0.958 -> 1.061 full Sharpe and still fails
   H2. This is idea 279's reading confirmed on 12 books: a turnover statement, not a buffer one.

## The by-product worth a memo
`u56 top20-200d DAILY + buffer m=50` (the rule-8 pick): **11.71% / 1.1454 / -12.37%, halves
1.1239 / 1.1688, OOS 13.49% / 1.2567 / -12.37%, turnover 5.80x/yr, realised gross 0.7228**,
against SPY 15.26% / 0.8904 / -33.72% (0.957/0.837, OOS 0.884) and the live RULES v2 8.68% /
1.2075 / -12.05% (1.226/1.194). It clears 4b on all five bars with m chosen in-sample only,
on a plateau of 8/9 cells, at 5/10/25 bps (it fails at 50 bps on H1 and CAGR). It **fails 4a**
on both halves. Memo: `.KEEP_MEMO.md`. Ranked by the review's own rule (min-half Sharpe subject
to the drawdown condition) it sits at 1.124, **below** the live book's 1.191 — so it is a
candidate to record, not a replacement to argue for.

## Caveats
* 2017-2026 is essentially H2 on this sample, so the rule-8 OOS bar and the 4b H2 bar overlap
  almost completely (idea 111's window problem). Every OOS number here inherits that weakness.
* SURVIVORSHIP: both panels are current constituents, so absolute CAGR/Sharpe are optimistic;
  all comparisons are between arms on the same panel over the same days.
* Multiplicity: 6 of 12 books produce a rule-8 4b KEEP, and the memoed cell is the best of them
  by min-half Sharpe. The census was pre-registered from published rows, and the only tuned dial
  is m, but the candidate is still the best of 12 and should be read that way.
* A daily book at 5.8x/yr turnover contradicts RULES v2's "no intra-week trading" clause and
  costs ~3.3x the live book's turnover; the 50 bps failure is the honest boundary.
