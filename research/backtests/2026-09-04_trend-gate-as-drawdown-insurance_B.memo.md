# Memo — idea 57 KEEP-candidate (PROTOCOL 4b): equal-weight all eligible, 3% re-entry band

1. **The book.** Idea 28's equal-weight-every-eligible-name construction at 75% gross, with
   the 200d-MA gate replaced by a **3% hysteresis band** so a name only changes state on a
   decisive cross, not on every touch of the average. No ranking, no vol scaling, no count cap.
2. **Exact RULES wording proposed.** *"A name is IN the book while its 20-day annualised
   volatility is below 60% and its trend state is 'up'. Trend state starts 'down' and flips
   to 'up' only when the close exceeds 1.03 × its 200-day moving average, and back to 'down'
   only when the close falls below 0.97 × that average; between those thresholds the previous
   state carries forward. Each Friday close, hold every IN name at equal weight totalling 75%
   of the book, remainder in cash, executed at the next close."*
3. **Full sample (universe.json, 2009-01-13 → 2026-09-03, weekly, 10 bps, t+1):**
   11.3% CAGR / 1.136 Sharpe / -15.1% MaxDD, halves 1.113 / 1.160, turnover **4.9x/yr**.
4. **The reason it exists.** It is the **first arm this project has produced that clears all
   five 4b tests on both large-cap universes** — `universe_broad.json` reads 11.1% / 1.064 /
   -16.8%, halves 1.163 / 0.971. Idea 2's n=20 fails broad H2 by 0.02; idea 55's K=none fails
   broad on H2, OOS and MaxDD. Two neighbours (monthly gate, 5% band) pass with it, so this is
   a region, not a point.
5. **Versus the benchmarks:** SPY 15.3%/0.890/-33.7% (halves 0.957/0.837); RULES v1 live
   6.5%/0.666/-13.8%. Passes all five 4b tests on both lists; fails 4a on drawdown, like every
   growth book the project has produced.
6. **Rule-8 walk-forward** (10 arms, chosen on 2009-2016 only): on `universe_broad.json` the
   4b-aware rule **picks this exact arm**, OOS 11.2% / 1.074 / -16.8% vs SPY 15.5%/0.884/-33.7%.
   On `universe.json` neither pre-registered rule picks it — both pick top20/`none`
   (OOS 14.9%/1.164/-18.5%). Its own untouched OOS there is 12.6% / 1.234 / -15.1%.
7. **Why the band and not the plain gate.** The continuously re-evaluated 200d gate flips
   7.55x per ticker per year; the band flips 1.77x. At 10 bps the band buys **more** drawdown
   (+3.25pp vs +2.51pp against the ungated book) for **less** forgone CAGR (-0.96pp vs -1.81pp)
   at 4.9x turnover instead of 8.2x, and is the only instrument in the grid with a non-negative
   Sharpe delta (+0.009). The plain gate's Sharpe delta is negative at every cost tested.
8. **Cost ceiling — the binding caveat.** At 25 bps no arm passes 4b on both universes (5/10
   and 0/10); at 50 bps, 1/10 and 0/10. This is a 10 bps rule. Idea 45's execution-lag test has
   not been run on it.
9. **Survivorship.** Both lists are current constituents and this book holds the entire
   eligible list, so absolute CAGR and Sharpe are optimistic — more so than for a ranked book.
   The band-vs-gate comparison in (7) is far less exposed; both arms draw from the same names.
10. **For the Sunday review.** Two decisions, separable. (i) The live daily 200d hard-exit is
    the most expensive version of this instrument and buys the least protection — replace it
    with the band regardless of what else changes. (ii) Adopt this book as the 4b candidate in
    preference to ideas 2 and 55, whose only advantage is a higher fitted CAGR on the one list
    they were fitted to. Do **not** read the band as alpha: it is cheaper insurance, and the
    insurance itself still costs ~1pp of CAGR.
