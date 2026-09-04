# Memo — idea 8, `12-1 n=30`: a cross-universe 4b pass that rule 8 will not select (PARK)

1. **What it is.** Idea 2's KEEP construction with the ranking signal replaced by pure 12-1
   momentum and the book widened to 30 names; gate, gross, cadence and costs unchanged.
2. **Numbers.** universe.json 10.9% / Sharpe 1.097 / MaxDD -15.8%, halves 1.105/1.094, OOS 1.193,
   turnover 6.7x. universe_broad.json 13.0% / 1.004 / -20.2%, halves 1.159/0.875, OOS 0.971,
   turnover 10.9x. SPY: 15.3% / 0.890 / -33.7%, halves 0.957/0.837, OOS 0.884.
3. **Why it is notable.** It is the only one of 20 grid points to clear KEEP path 4b on *both*
   universes, and on broad it clears 4a as well — the incumbent blend-v1 n=20 fails broad H2.
4. **Why it is PARK, not KEEP.** Rule 8 never picks it: it is not in the IS (2009-2016) top 6 on
   either list, and IS→OOS Sharpe rank correlation is +0.000 on universe.json, so the selection
   procedure that would have to find it demonstrably cannot.
5. **Second reason to wait.** Its broad MaxDD is -20.2% against a -20.2% cap: zero margin. Idea 45's
   cost/lag protocol has not been run on it (queued as idea 68).
6. **Third reason.** On universe.json n=30 holds ~74% of the eligible set, so most of this arm is
   the unranked EW-all-eligible book; the ranking contributes +0.40%/yr (t +0.49) there.
7. **Exact RULES wording, if a future Sunday review promotes it** (replacing v1's §Selection and
   §Sizing wholesale, per protocol rule 6):
   > **Selection.** Each Friday at the close, rank every universe name that is (a) above its
   > 200-day simple moving average and (b) has 20-day annualized volatility below 0.60, by
   > 12-1 momentum: `close[t-21] / close[t-252] - 1`. Hold the top 30 (or all eligible names if
   > fewer than 30 qualify).
   > **Sizing.** Equal weight, 2.5% of book per name (75% gross when 30 names qualify; the
   > shortfall is held in cash when fewer qualify). No volatility scaling.
   > **Execution.** Orders placed at the next session's close; the 200-day exit remains a daily
   > hard rule.
8. **Do not adopt this week.** Protocol rule 6 allows one rules change per week and the standing
   4b candidates (idea 2's blend-v1 n=20, idea 57's ew-band3) are ahead of it in the review queue.
9. **What would promote it.** A rule-8 selection rule that picks it prospectively (none found
   here), plus a 5-50 bps and 1-week-lag pass with the broad drawdown staying inside the cap.
10. **What would kill it.** Any cost above 10 bps that pushes broad CAGR under 10.7%, or a
    universe-composition test (idea 53's protocol) in which the broad pass does not survive
    dropping 5-10 names.
