# KEEP-4b CONFIRMATION memo for the Sunday review — the incumbent U56 book is TAPE-VINTAGE CERTIFIED
(idea 1350, lane B, 2026-09-19. Rule 6 reserves enactment for the Sunday review; nothing is enacted here.
This CERTIFIES the standing 2026-09-04 candidate against a defect idea 1335 raised; it proposes no new book.)

1. **What was tested.** Every vintage of `data/prices.csv` recoverable from this repo's history — 14
   commits, 14 distinct blobs, 2026-09-03..2026-09-18, read offline with `git show` — with
   `prices_broad.csv` / `prices_small.csv.gz` taken as of the same commit. The frozen 2026-09-04 book
   (N=20, H=126, gross 0.75, weekly, 10 bps, t+1) was rebuilt on each, on all three panels. 912 books.
2. **The verdict is vintage-robust.** U56 clears 4b on **12 of 12** post-fix vintages, on both readings.
   Head vintage (4e19a80d): **15.80% / 1.1537 / −19.13%**, halves 1.2067 / 1.1203, OOS **17.32% /
   1.1857 / −19.13%**; SPY 15.12% / 0.8844 / −33.72%, OOS Sharpe 0.8738.
3. **The margins barely move.** Restatement-only (V_TRUNC, common end date): every 4b margin spreads by
   **≤ 1.05e-4** across the 12 vintages; full Sharpe by **5.2e-6**. Adding each vintage's own extra rows
   (V_RAW, up to 11 more sessions): full Sharpe spread **6.4e-3**, H2 margin 1.2e-2, OOS margin 1.2e-2,
   CAGR margin 0.09 pp.
4. **The leg the record calls the binder is the safest one.** The 4b drawdown-cap margin is **+1.1028 pp**
   and its vintage spread is **1.05e-4 pp** — a margin-to-spread ratio of **10,521**. MaxDD is −19.13% on
   all 12 post-fix vintages: the 2020/2022 drawdown sits deep inside every tape.
5. **Idea 1335's 6.98e-3 residual is the tape's NEW ROWS, not its rewrites.** It is the size of the V_RAW
   spread (6.4e-3 full, 1.2e-2 on halves) and ~1,000x the V_TRUNC one. Cross-run replay in this repo is
   resolution-limited to ~6e-3 of Sharpe unless both runs name the same tape blob.
6. **The verdict DOES flip on 2 of 14 vintages — both pre-c006b439**, the commit that fixed the
   calendar-day index. Those tapes carry ~6,060 calendar rows against ~4,700 trading rows and give
   1.00 Sharpe / −20.89% MaxDD / DD margin −0.66 pp → 4b FAIL. That is a fixed data bug, not tape noise.
7. **Why the book cannot feel the rewrite.** 9.2% of overlapping U56 price cells restate per daily step,
   but the median |Δ daily return| is **1.1e-6** (CSV formatting), only **0..699** return cells per step
   move by more than 1 bp, and the largest move (5.1 pp) is in the two crypto columns the universe excludes.
8. **Rule 8 (dials chosen on warm-up..2016-12-31, 2017–2026 read once).** The IS-Sharpe chooser over
   N {10,16,20,25} x H {63,126,252} picks (16, 63) on **12 of 12** post-fix U56 vintages — stable — and
   **LOSES to doing nothing** by **−0.0400** of mean OOS Sharpe (pick 1.1388..1.1462, anchor
   1.1759..1.1870); the pick clears 4b **0 of 12**, the anchor **12 of 12**. H_HINDSIGHT again.
   4a is **0 of 912**: live RULES v2 (full Sharpe 1.2011, MaxDD −12.05%) is out of reach for a growth book.
   On SMALL the pick DOES move ((20,63) → (10,252), worth 0.43 of OOS Sharpe) — but at the same commit the
   cached panel went from 445 to 665 names, so that is a universe rebuild, not a restatement.
9. **Survivorship (rule 9).** U56 / BROAD are current-constituent lists and SMALL a current sub-$2B screen,
   so every absolute level is an upper bound. The headline is a SPREAD of the same book over the same names,
   which is first-order immune; the 4b pass count is not.
10. **Exact RULES wording, if a Sunday review enacted the certified book.** *"Each week at the close of the
    last trading session, rank every instrument in the mega-cap/ETF universe that is above its own 200-day
    moving average and has 20-day annualised volatility below 0.60, by the equal-weighted average of its
    percentile ranks on (t−21 / t−252), (t / t−126) and (t / t−63) total return. Hold the top 20, equally
    weighted, at 0.75 of NAV with the remainder in cash; a holding is retained for at least 126 trading days
    from the session it was bought, and a retained holding keeps its slot. Trade at the next session's
    close. Every number published for this rule states the git blob of the price tape it was computed on;
    two numbers computed on different tapes are comparable only to 6e-3 of Sharpe."*
