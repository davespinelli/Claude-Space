# Memo — idea 96, execution lag is missing from every drawdown price (PROTOCOL, no RULES change)

1. **Finding.** Idea 94's per-name trailing stop KILL is confirmed on a harness that reproduces
   it at **max|diff| 0.0**: under the protocol's own execution convention the stop destroys
   drawdown in 12/12 cells at 15% and 8/12 at 25%, and is priceable in 0/12 under either the
   absolute or idea 119's relative floor.
2. **The queue's axis is the wrong one.** Check frequency (daily vs weekly grid) moves median
   dMaxDD by 0.1-1.3 pp and never flips a sign. Idea 94 was already checking daily; the weekly
   grid governs re-entry, not exit.
3. **The axis that matters is a single day of execution lag.** Median dMaxDD:
   **-0.69 pp** (exit decided at close t, applied t+1 = PROTOCOL rule 2) -> **+2.44 pp**
   (applied t+2) -> **-0.25 pp** (applied at the next weekly rebalance). Non-monotone, and the
   sign flips on one day.
4. **Mechanism, measured:** the day after a stop fires the triggering name earns **+0.57% to
   +2.21%** against an unconditional **+0.06%/day** (t **+2.70 to +10.37**, 9/12 cells,
   persisting +1.2 to +2.6% over five days). The stop sells into a short-term reversal; a
   one-day-slower exit harvests the bounce. That is not insurance, and it is not the stop.
5. **Nine arms appear to pass 4b — do not quote them.** All on `lag=t+2` (non-conformant), all
   `u56` only, all clearing 4b's drawdown cap by **0.15-1.6 pp** on a single-path extremum,
   and rule 8 picks the **no-stop control** in all four cells where they live (IS differences
   <= 0.001, mean OOS regret +0.002). Every control fails 4b on the drawdown cap alone.
6. **Generalisable exposure:** the project's entire drawdown-price list (ideas 9, 22, 40, 74,
   94, 96, 97, 117) is quoted without an execution lag, and for a fast instrument the lag moves
   the price by **more than the instrument does**. Prices for slow instruments (200d gate, 3%
   band, de-grossing) are not affected at the same order, but that is an assertion this run did
   not test and should not be assumed.
7. **Exact PROTOCOL wording proposed to the Sunday review** (extend rule 2; nothing else edited):

> **2 (extended, Sep 5).** Any rule that can act BETWEEN scheduled rebalances — a per-name stop,
> an intra-period exit, a same-day gate — must state its trigger frequency and its execution lag
> separately, and its execution lag must be the same as the scheduled book's: a trigger observed
> at close t is executed so that the position's first changed return is day t+1. A drawdown
> price (pp of CAGR per pp of MaxDD) may not be quoted without the execution lag it was computed
> at, and where an instrument's price changes sign under a one-bar change of lag, that fact must
> be reported beside the price.

8. **Retro-action if adopted:** annotate idea 94's and idea 97's stop rows with "conformant lag,
   sign stable at t+1 only", and re-check idea 40's book-level DD control and idea 75's
   conditionally-armed stop for the same one-bar sensitivity before either is priced again.
9. **No RULES change, no new candidate.** Idea 97's surviving clause ("the per-name trailing
   stop is the dearest instrument") is untouched and now has a mechanism behind it.
10. **New queue idea, deliberately not pursued here:** the +0.6-0.9%/day post-trigger reversal
    is a short-term-reversal signal on both large-cap panels in its own right. It is a statement
    about the panels, not about stops, and needs its own pre-registration, cost ladder and
    walk-forward — not a by-product row on a stop result.
