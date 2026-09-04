# Memo — idea 55 KEEP-candidate (PROTOCOL 4b): drop the 200d gate from idea 2's book

1. **The book.** Identical to idea 2's KEEP-candidate except that the 200d-MA half of the
   eligibility filter is removed; the `vol20 < 0.60` half is unchanged.
2. **Exact RULES wording proposed.** *"Each Friday close, rank every universe name whose
   20-day annualised volatility is below 60% by the composite score (mean of the
   percentile ranks of 12-1 momentum, 6-month return and 3-month return; no volatility
   scaling). Hold the top 20 at 3.75% each, executed at the next close. If fewer than 20
   names qualify, hold all of them at 3.75% and leave the remainder in cash."*
3. **Full sample (universe.json, 2009-01-13 → 2026-09-03, weekly, 10 bps, t+1):**
   13.7% CAGR / 1.123 Sharpe / -18.5% MaxDD, halves 1.154 / 1.101, turnover 9.5x/yr.
4. **Versus the incumbent candidate** (idea 2's K=200d n=20, 12.7%/1.093/-18.3%): +1.0pp
   CAGR, +0.030 Sharpe, -0.2pp drawdown, same turnover — one fewer filter.
5. **Versus the benchmarks:** SPY 15.3%/0.890/-33.7% (halves 0.957/0.837); RULES v1 live
   6.5%/0.666/-13.8%. Passes all five 4b tests; fails 4a on drawdown, like every growth
   book the project has produced.
6. **Rule-8 walk-forward** (chosen on 2009-2016 only): **both** pre-registered selection
   rules — plain in-sample Sharpe and the 4b-aware rule — pick this exact point, and its
   untouched OOS is **14.9% / 1.164 / -18.5%** against SPY 15.5%/0.884/-33.7% and RULES v1
   7.8%/0.751/-13.8%. OOS Sharpe exceeds in-sample (1.164 vs 1.071): not an overfit signature.
7. **Why it is only a candidate, not a recommendation.** It inherits idea 2's universe
   fragility exactly: on `universe_broad.json` (136 names) **0 of 16 grid points pass 4b**,
   and this point fails on H2, OOS and MaxDD. Two heavily-overlapping current-constituent
   large-cap lists are one replication, not two (ideas 39/49).
8. **Survivorship.** Both lists are current constituents; a 20-name book holds over a third
   of the 56-name list. Absolute CAGR and Sharpe are optimistic. The gate comparison in (4)
   is far less exposed — both arms draw from the same names on the same days.
9. **The gate's own contribution is not distinguishable from zero, which is the real
   finding.** Dropping the 200d gate is worth +0.35 to +1.47%/yr across n on universe.json
   (t +1.42 to +1.76 — positive at every n, significant at none) and -0.22 to +0.19%/yr on
   the broad list (t -0.50 to +0.68). It is not an edge; it is a filter we have been paying
   turnover for.
10. **For the Sunday review:** adopt this only as a *replacement* for idea 2's wording if
    idea 2 is adopted at all, since it strictly dominates it on the primary universe at
    equal cost. Do not treat the removal of the 200d gate as an improvement in its own
    right — the evidence says the gate does nothing, not that removing it adds something.
