# KEEP-candidate memo — idea 2 position-count (4b) — for the Sunday review

1. **Candidate:** hold the top **20** eligible names, equal-weight at **75% gross (3.75% each)**,
   ranked by the v1 composite **without** the `/sqrt(vol20)` term. Weekly, 10 bps, next-day.
2. **Full sample (2009-01-13 → 2026-09-03):** CAGR 12.7%, Sharpe 1.093, MaxDD -18.3%, vol 11.5%,
   turnover 9.6x/yr — the lowest-turnover point in the whole grid.
3. **Halves:** H1 1.088 / H2 1.103, both above SPY's 0.957 / 0.837. RULES v1: 0.641 / 0.692.
4. **Walk-forward (rule 8), n chosen on 2009–2016 only:** the 4b-aware rule picks n=20; untouched
   OOS 2017–2026 is **14.4% / 1.170 / -18.3%** vs SPY 15.5% / 0.884 / -33.7% and v1 7.8% / 0.751 / -13.8%.
5. **Passes 4b on all five tests** (H1, H2, OOS Sharpe, MaxDD -18.3% ≤ -20.2% cap, CAGR 12.7% ≥
   10.7% floor). Fails 4a on MaxDD (-18.3% vs v1's -13.8%), as every growth book does.
6. **Mechanism:** n is a de-risking dial at constant gross (vol 24.3% → 11.5% as n goes 2 → 20).
   Position count is what resolves the H1-Sharpe constraint that ideas 24, 25, 28 and 40 all
   failed on — n = 6–10 fail H1 alone, n ≥ 12 clear it.
7. **Caveat A — margin does not replicate.** On the 136-name broad universe the direction holds
   (Sharpe 0.698 → 0.958 from n=2 → 20) but n=20's H2 is 0.814 vs SPY 0.837, i.e. it would fail
   4b's H2 there by 0.02. Only n=40 passes on that list; selecting it would be tuning.
8. **Caveat B — survivorship.** `universe.json` is a current-constituent list of 56 names, ~37.5
   eligible per day, so an n=20 book holds over half a hand-picked winner list. Levels optimistic;
   the ranking across n is the durable part.
9. **Caveat C — small gain at matched risk.** Scaled to a common 12% vol, n=20 earns 13.2%/yr vs
   n=5's 11.3% and n=4's 12.7%; the curve is U-shaped, not monotone. Most of the 4b clearance is
   vol reduction fitting under the drawdown cap, with a 1.9pp margin.
10. **Do NOT read `OFF/FIXEDW n=3` and `n=4` (also 4b passes) as support for concentration** —
    they are the n=3/n=4 books at 45%/60% gross, identical Sharpe, drawdown merely scaled under
    the cap. That is a leverage lever (idea 20), not an edge.

## Exact RULES wording, if adopted

> **Selection.** Each Friday at the close, rank every universe name that is (a) above its own
> 200-day moving average and (b) has 20-day realised volatility below 60% annualised, by the
> composite score `mean(pct-rank of 12-1 momentum, pct-rank of 6-month return, pct-rank of
> 3-month return) × (1.0 if above the 200-day MA else 0.5)`. **No `/sqrt(vol20)` term.**
>
> **Sizing.** Hold the top **20** ranked names at **3.75% each** (75% gross, 25% cash). If fewer
> than 20 names are eligible, hold all eligible names at 3.75% each and leave the remainder in
> cash — do not concentrate into a shorter list.
>
> **Execution.** Orders are decided at Friday's close and executed at the next session's close.
>
> **Daily hard exit.** Any held name that closes below its own 200-day moving average is sold at
> the next session's close and its weight goes to cash until the following Friday rebalance.

Adoption note: this replaces RULES v1 wholesale (PROTOCOL rule 6 permits a 4b KEEP to do so). It
raises the book from 5 names to 20 and removes the vol scaler, so it is a large operational
change; the drawdown budget goes from -13.8% to roughly -18%. Recommend the review either adopt
it or run it as a paper sleeve alongside v1 for a quarter before switching capital.
