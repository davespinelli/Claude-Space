# Idea 8 — lookback-blend (lane C, 2026-09-04)

**Verdict: KILL for changing the ranking horizon.** No lookback component beats the incumbent
three-horizon blend at the KEEP-candidate's own position count on either universe, and the
walk-forward cannot tell the horizons apart at all on the primary list. Two by-products are
worth keeping: the **3-1 leg is the harmful leg** of the blend, and **12-1 n=30 is the only grid
point that passes 4b on BOTH universes** — but rule 8 never selects it, so it is PARK, not KEEP.

Script: `research/backtests/2026-09-04_lookback-blend_C.py` ·
console: `2026-09-04_lookback-blend_C.console.txt` · memo: `2026-09-04_lookback-blend_C.memo.md`

## Design

Everything in idea 2's KEEP construction is held fixed — eligibility `(px > 200d MA) & (vol20 <
0.60)`, top-n equal weight at 75% gross, weekly, 10 bps, next-day execution — and only the
**ranking signal** is swapped. Grid = signal × n, exactly 2 tuned parameters, all 20 points
reported on each of two universes:

| signal | definition |
|---|---|
| `12-1` | `px.shift(21)/px.shift(252) - 1` |
| `6-1` | `px.shift(21)/px.shift(126) - 1` |
| `3-1` | `px.shift(21)/px.shift(63) - 1` |
| `blend-v1` | mean pct-rank(12-1, 6m no-skip, 3m no-skip) — **the incumbent** |
| `blend-skip` | mean pct-rank(12-1, 6-1, 3-1) — skip-consistent variant |

n ∈ {5, 10, 20, 30}. Controls at the same gate and gross: EW-all-eligible (no ranking),
REVERSED (bottom-n) arms, 1-month reversal. Harness check: `blend-v1 n=20` reproduces idea 2's
published KEEP row to the decimal (12.7% / 1.093 / -18.3%, halves 1.088/1.103). Index is
trading-day (idea 38 fix confirmed: 251 rows in 2018, 252 in 2024).

## Headline numbers (universe.json, 2009-01-13 → 2026-09-03)

Bars: SPY 15.3% / 0.890 / -33.7%, halves 0.957/0.837, OOS 0.884 → 4b needs H1>0.957, H2>0.837,
OOS>0.884, MaxDD ≥ -20.2%, CAGR ≥ 10.7%. RULES v1 live: 6.5% / 0.666 / -13.8%.

| signal | n=5 | n=10 | n=20 | n=30 |
|---|---|---|---|---|
| 12-1 | 19.9/1.061/-24.1 | 15.2/1.038/-20.6 | 12.1/1.047/-18.8 **KEEP 4b** | 10.9/**1.097**/-15.8 **KEEP 4b** |
| 6-1 | 19.9/1.077/-22.8 | 13.9/0.964/-20.6 | 11.8/1.015/-19.2 **KEEP 4b** | 10.5/1.060/-16.9 |
| 3-1 | 14.5/0.854/-21.0 | 12.2/0.889/-18.9 | 10.4/0.935/-18.3 | 9.8/1.023/-16.4 |
| blend-v1 | 16.5/0.952/-21.6 | 12.9/0.929/-17.5 | 12.7/1.093/-18.3 **KEEP 4b** | 11.0/**1.099**/-16.6 **KEEP 4b** |
| blend-skip | 16.9/0.965/-22.5 | 12.2/0.876/-20.0 | 11.7/1.012/-19.5 **KEEP 4b** | 10.8/1.083/-16.5 **KEEP 4b** |

(CAGR / Sharpe / MaxDD; every point fails 4a on drawdown against the live book, as every growth
book in this project does.) On `universe_broad.json` the same grid loses H2 almost everywhere —
only **12-1 n=30 (13.0% / 1.004 / -20.2%)** passes 4b, and it also passes 4a there.

## What the run actually establishes

1. **The horizon does not matter at the candidate's position count.** Paired daily t-tests
   against `blend-v1` at matched n: on universe.json every alternative is *negative* at n=20/30
   (12-1 -0.52%/yr t -0.79; 6-1 -0.80%/yr t -1.40; blend-skip -0.82%/yr t -1.80); on broad the
   best alternative is 12-1 at +0.80%/yr **t +0.74**. Nothing clears t = 2 in either direction at
   n=20 or n=30. The horizon arms only separate in concentrated books (12-1 vs blend at n=10 on
   broad: +4.12%/yr t +2.36) — i.e. exactly where 4b's drawdown cap already kills them.
2. **The walk-forward cannot select a horizon on the primary universe.** Spearman(IS Sharpe,
   OOS Sharpe) across the 20 grid points is **+0.000** on universe.json (+0.463 on broad). The
   IS-best point (6-1 n=5, IS Sharpe 1.227) goes OOS 18.5%/0.971/-22.8% and misses OOS 4b on
   drawdown; the 4b-aware IS pick (6-1 n=20) does clear OOS 4b (12.3%/1.020/-19.2%) but the same
   procedure on broad picks 6-1 n=30, which misses OOS 4b (-20.6% vs the -20.2% cap). Picking a
   lookback in-sample is a coin flip on the list the live book trades.
3. **3-1 is the leg to drop, not to promote.** Raw weekly rank IC within eligible names:
   12-1 +0.0497 (t +4.29), blend-v1 +0.0499 (t +4.74), blend-skip +0.0434 (t +3.93),
   6-1 +0.0362 (t +3.33), **3-1 +0.0224 (t +2.07)** on universe.json — and on broad 3-1 collapses
   to +0.0110 (t +1.40) with H2 IC +0.0057 (t +0.49). In portfolio terms 3-1 costs -2.11%/yr
   (t -3.17) vs the blend at n=20 on universe.json and -2.04%/yr (t -1.77) on broad, and its
   books fail 4b on H1 (universe.json) or H2+OOS (broad) at every n.
4. **The blend is not redundant, it is the most stable leg.** blend-v1 has the highest full-sample
   IC t-stat on both lists and is the only signal whose IC does not decay from H1 to H2 on
   universe.json (+0.0460 → +0.0537; 12-1 decays +0.0603 → +0.0392). That is the honest defence of
   the incumbent: it is not the best in any half, it is the least variable across halves.
5. **Ranking earns its keep only in concentrated books.** Against the unranked EW-all-eligible
   control at the same gate and gross: n=5 +6.5 to +9.5%/yr (t +2.4 to +3.3), n=20 +1.4 to
   +2.2%/yr (t +1.4 to +2.3), n=30 **+0.1 to +0.6%/yr (t +0.1 to +0.7)** on universe.json. Caveat
   that matters for reading point (6): on universe.json a mean 37.5 names are eligible and n=30
   holds a mean 27.6 of them, so the primary n=30 arms are ~three-quarters of the eligible set —
   nearly the unranked control. On broad (91.5 eligible, 29.5 held) n=30 is a genuine top-third
   selection.
6. **One cross-universe 4b pass, unselectable by rule 8.** `12-1 n=30` is the only (signal, n)
   point passing 4b on universe.json (10.9% / 1.097 / -15.8%, halves 1.105/1.094, OOS 1.193,
   turnover 6.7x) **and** universe_broad.json (13.0% / 1.004 / -20.2%, halves 1.159/0.875, OOS
   0.971, turnover 10.9x, also KEEP 4a). It is not in the IS top 6 on either list, so no
   walk-forward rule selects it: **PARK**, per protocol rule 8, not KEEP. Its broad drawdown
   (-20.2%) sits exactly on the cap, so it has zero margin there.
7. **Sign checks pass.** Reversed books collapse (bottom-5 blend-v1: 2.7% / 0.348 on
   universe.json, 1.6% / 0.200 on broad) and 1-month reversal is flat-to-negative
   (IC -0.0074, t -0.72). The momentum sign is real; only the horizon choice is noise.

## Caveats

- **Survivorship**: both lists are current constituents, so all absolute CAGRs are optimistic.
  Signal-vs-signal comparisons hold names, days, gate and gross fixed and are much less exposed;
  the level of the 12-1 n=30 arm is not.
- Costs were held at the protocol's 10 bps. The 12-1 n=30 arm turns over 6.7x/yr on universe.json
  vs the incumbent blend-v1 n=20's 9.6x, so it should be *less* cost-sensitive, but that was not
  measured here (queued as idea 68).
- H1/H2 splits are the protocol's equal-row halves (break ≈ 2017-11), which is not the same cut
  as the rule-8 IS/OOS split (2016-12-31); both are reported for every point.
