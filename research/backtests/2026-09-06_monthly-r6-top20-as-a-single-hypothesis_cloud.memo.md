# KEEP-candidate memo — idea 182, R6 top-20 monthly (4b path, scoped to universe.json)

1. **Path:** PROTOCOL 4b. Clears on u56 in **9/9 cells** (5/10/25 bps × t+1/t+5/t+7 execution
   lag), full-sample **and** on the OOS window alone, and in **400/400 composition draws @10 bps**
   (96.5% at drop-10 @25 bps). Fails 4a everywhere — its drawdown is worse than the live book's.
2. **Numbers @10 bps, t+1, u56:** 13.61% CAGR / 1.1557 Sharpe / −18.81% MaxDD, halves
   1.228/1.102, **OOS 14.56% / 1.1695 / −18.81%**, turnover 4.82x/yr.
   SPY 15.23%/0.8890/−33.72% (OOS 15.45%/0.8820); RULES v1 6.45%/0.6642/−13.83% (OOS 0.7471).
3. **Rule 8:** on u56 the IS-only chooser lands on monthly by itself at all three cost rungs —
   IS-PICK = FIXED-M = ORACLE. The cadence is not a hindsight pick.
4. **Binding bar:** the 4b drawdown cap in all 27 cells. Margin +0.070 at t+1/10 bps (−18.81%
   against the −20.23% cap) but only **+0.011 at t+7** (−20.01%). A one-calendar-week fill nearly
   exhausts the cap; that is the number to watch before any sizing decision.
5. **SCOPE — the limitation, not a footnote:** 0/9 cells on universe_broad.json (MaxDD −24.5%,
   margin −0.211) and 0/9 on the small panel (fails H1, H2, OOS, DD and CAGR). This is a
   universe.json rule, and it must be written as one.
6. **Survivorship:** universe.json is a current-constituent list (idea 54). No level above is an
   attainable return; the composition draws bound composition sensitivity, not survivorship.
7. **Not affected by ideas 187/221:** MONTHLY is a k=1 calendar block, so it has exactly one
   phase and carries no block-phase alignment draw.
8. **Recommendation to the Sunday review:** adopt as **RULES v2** for the paper book (4b may
   replace the live rules wholesale, PROTOCOL rule 6), or hold one more week for a delisting-aware
   check (idea 54) — but do NOT widen it to a broader universe, which it fails outright.
9. **Do not tune it.** Every dial is at idea 173's published value; n, gross and cadence were
   fixed before this run and must stay fixed if it is adopted.
10. **Script:** `research/backtests/2026-09-06_monthly-r6-top20-as-a-single-hypothesis_cloud.py`
    (controls [b] 1.735e-17, [e] 0.000e+00, [c] 4.441e-16 vs idea 173's committed grid).

---

## Exact RULES wording, if adopted

> # Paper Book Rules — v2 (effective YYYY-MM-DD)
> Applied mechanically by the daily routine using the newest reports/<date>.csv (output of
> research/scan.py).
>
> 1. **Universe:** all instruments in research/universe.json except BTC-USD and ETH-USD. This
>    rule set is scoped to that list; it is **not** validated on a broader or small-cap universe
>    (idea 182: 0 of 9 cells pass on either).
> 2. **Eligibility:** `above_200 == True` and `vol20 < 0.60`.
> 3. **Ranking key:** `r6_vol = (close / close_126_bars_ago − 1) / max(vol20, 0.08) ** 0.5`,
>    computed across the eligible set only. This replaces v1's 3-term momentum composite.
> 4. **Selection:** top 20 eligible by `r6_vol`.
> 5. **Sizing:** 3.75% of current NAV per position (max 20 positions → 75% invested, ≥25% cash).
>    Round shares down to whole units. If fewer than 20 names are eligible, hold the shortfall in
>    cash — do **not** re-spread the gross over fewer names.
> 6. **Rebalance:** on the last trading day of each calendar month only. On that day, sell every
>    holding not in the new top 20 and buy every new entrant, then reset all positions to 3.75%
>    of NAV. There is no weekly rebalance and no top-up band.
> 7. **Hard exit any day:** sell a position the day it closes below its 200-day average
>    (`above_200 == False`).
> 8. **Trade price:** last close in the report (paper fill, no slippage modeled; note this as a
>    known bias). Backtested at 10 bps per unit turnover with next-day execution; the rule also
>    clears its acceptance bars at 25 bps and at a one-week fill.
> 9. **Reason string:** always "RULES v2: <selection|exit|rebalance> rank=<n> r6_vol=<x>".
>
> Changes require a dated entry in research/CHANGELOG.md and a version bump here.

**Note on wording of clause 5**, which is not cosmetic: idea 81 found that dividing gross by a
fixed `n` silently de-grosses whenever fewer than `n` names are eligible. The backtest above is
the *literal* `gross/n` book, so the rule must say "hold the shortfall in cash" to match what was
tested. Any implementation that re-spreads the gross is a different book and is unpriced.
