# MEMO — 4b KEEP-candidate: SOFT MIN HOLD, monthly, H=126 (idea 1065, lane C, 2026-09-16)

1. **CANDIDATE.** U56, CAND20 top-20 score, monthly rebalance, min hold 126 trading days released
   early when a name leaves the free top-40. Full 14.36% / 1.1667 / −19.59%; halves 1.2631 /
   1.0943; OOS (2017-01-01..2026-09-15, read once) 15.50% / 1.1863 / −19.59%; turnover 3.38/yr.
2. **PATH.** 4b only. SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588 / 0.8207), OOS 15.21% /
   0.8711 / −33.72%. Legs: H1 ✓, H2 ✓, OOS ✓, DD −19.59% ≤ 0.60 × 33.72% = −20.23% ✓,
   CAGR 14.36% ≥ 0.70 × 15.10% = 10.57% ✓. **4a FAILS** (live RULES v2 1.2007, MaxDD −12.05%).
3. **RULE 8.** The arm was chosen on 2009–2016 IS Sharpe ALONE (1.1455) from the 68 arms of its
   (panel, mech) cell; OOS was read once. It is 1 of 6 rule-8 cells that passes 4b; 0 of 6 beat
   RULES v2 on OOS Sharpe; 6 of 6 beat SPY.
4. **EXACT RULES WORDING, if ever promoted.** *"Rank every priced instrument by the CAND20
   composite (21/252 momentum, 0/126 and 0/63 returns, each cross-sectionally percentile-ranked
   and averaged, times 0.5 + 0.5·[close > 200d MA]; no vol scaler). Eligible = close above its
   200d MA and 20d annualised vol below 0.60. On the last trading day of each month, hold the top
   20 eligible names at gross 0.75/20 of NAV each, applied at the next open. A name bought fewer
   than 126 trading days ago is RETAINED and may not be sold — unless it has fallen outside the
   top 40 of that day's ranking, in which case it is released and its slot refilled from the
   ranking. Gated-out weight goes to CASH."*
5. **WHY IT IS NOT PROPOSED.** The DD leg clears by 0.64 pp. On this record's own SE work
   (ideas 1012 / 1042) a 4b leg margin that size is not decidable on one tape half, so the pass is
   a coin flip on its binding leg.
6. **WHAT IT IS NOT.** It is not the mechanism this run was testing. The run's finding is that the
   min-hold drawdown tax is an EXPOSURE fact, so the soft release works by shrinking the frozen
   bucket, not by dropping bad names.
7. **UNSELECTED BASE RATE.** SOFT arms pass 4b 107 of 288 (0.372) against the gross-matched null's
   14 of 256 (0.055) — above chance, but the arm was still picked from 68 candidates.
8. **COSTS.** 10 bps per unit turnover, next-day execution, gross 0.75, no shorting, no leverage.
   At 3.38 turns/yr the drag is ~34 bp/yr; the book is not cost-fragile.
9. **SURVIVORSHIP.** U56 is a current-constituent list. The CAGR and Sharpe levels are optimistic;
   the SPY comparison is against a real index, so the 4b margins are upper bounds.
10. **STATUS.** REPORTED, NOT PROPOSED. No RULES change (rule 6 — Sunday review only);
    RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched by this run.
