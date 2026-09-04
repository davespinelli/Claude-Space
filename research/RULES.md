# Paper Book Rules — v1 (effective 2026-09-04)
Applied mechanically by the daily routine using the newest reports/<date>.csv (output of research/scan.py).

1. **Universe:** all instruments in research/universe.json except BTC-USD and ETH-USD.
2. **Eligibility:** `above_200 == True` and `vol20 < 0.60`.
3. **Selection:** top 5 eligible by `score` (risk-adjusted momentum composite).
4. **Sizing:** 15% of current NAV per position (max 5 positions → 75% invested, ≥25% cash). Round shares down to whole units.
5. **Rebalance:** only on Fridays (or the last trading day of the week). Sell positions no longer in the top 8 or no longer eligible; buy new top-5 entrants; do not top-up/trim existing positions unless weight > 22% or < 8% of NAV.
6. **Hard exit any day:** sell a position the day it closes below its 200-day average (`above_200 == False`).
7. **Trade price:** last close in the report (paper fill, no slippage modeled; note this as a known bias).
8. **Reason string:** always "RULES v1: <selection|exit|rebalance> rank=<n> score=<x>".
Changes require a dated entry in research/CHANGELOG.md and a version bump here.
