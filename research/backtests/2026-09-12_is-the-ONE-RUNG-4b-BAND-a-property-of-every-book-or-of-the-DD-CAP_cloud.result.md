# Idea 804 — is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP (cloud, 2026-09-12)

**ANSWERED = YES, AND IT IS A PROPERTY OF THE BARS, NOT OF THE BOOKS. Over 50 books × 17 gross
rungs the admissible 4b band's LOWER edge is the CAGR floor ALONE in 24 of 24 bands and its UPPER
edge is the DD cap ALONE in 19 of 19 bar-set upper edges (the other 5 bands run off the top of the
grid). No Sharpe leg appears at ANY edge of ANY band. The queue's reading — "the DD cap's upper edge
meeting the CAGR floor's lower edge with nothing else in play" — is confirmed at 24/24. Idea 574's
"median ONE rung" was a five-book artefact: over the wider set the median band is 2 rungs of 17
(0.10 of gross). No KEEP claimed — 4a 51 / 4b 57 / BOTH 0 of 850 cells, and the one book that
survives a rule-8 selection cleanly is PARKED, not promoted (see below).**

Script: `2026-09-12_is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP_cloud.py`
Artefacts: `.grid.csv .bands.csv .invariance.csv .walkforward.csv .keeppaths.csv .console.txt`

## The mechanism (G4, measured — this is why the answer is what it is)

A book at gross *g* is the same holdings mixed with cash, so mean and vol both scale by *g* and only
the cost drag differs. Measured over the 17 rungs, median spread across 50 books:

| metric | median spread over the whole gross grid | max over books |
|---|---|---|
| H1 Sharpe | **0.007** | 0.018 |
| H2 Sharpe | **0.003** | 0.018 |
| OOS Sharpe | **0.004** | 0.018 |
| CAGR | 10.39 pp | 21.42 pp |
| MaxDD | 22.4 pp | 38.0 pp |

The three Sharpe legs are **flat in gross to within 0.02**; the two level legs move by 10–22 points
across the same dial. So gross cannot decide a Sharpe leg — it decides only CAGR and DD. The Sharpe
legs decide **whether** a book has a band at all; the CAGR floor and DD cap decide **where** it is
and **how wide**. That is the whole of the "one-rung band".

## The edge census (all 24 bands, 10 bps)

| edge | binding legs | count |
|---|---|---|
| lower | **CAGR alone** | **24 / 24** |
| upper | **DD alone** | **19 / 19 bar-set** |
| upper | GRID-HI (band runs off g=1.00, so no bar binds) | 5 |

Over all 850 cells at 10 bps the per-leg failure rates are CAGR 69%, H2 41%, DD 35%, OOS 34%,
H1 28%: the CAGR floor is the single most binding bar in the protocol, and it binds hardest at low
gross where every other bar is easiest.

## The six pre-registered hypotheses: 6 of 7 PASS

| H | verdict | measured |
|---|---|---|
| H_DD | **PASS** | upper edge = DD alone in 19/19 bar-set upper edges (bar ≥ 2/3) |
| H_CAGR | **PASS** | lower edge = CAGR alone in 24/24 (bar ≥ 2/3) |
| H_ONLY | **PASS** | 24/24 bands have only DD/CAGR at both edges — no Sharpe leg anywhere |
| H_NARROW | **PASS** | median band width **2.0** rungs of 17 (bar ≤ 2); 574's "1" does not generalise |
| H_MONO | **PASS** | 24/24 bands contiguous — "band width" is a meaningful summary |
| H_RATE | **FAIL** | 24/50 books pass 4b somewhere (48%, bar ≥ 25) — 574's 5-of-10 rate is at the bar, not above it |
| H_WF | **PASS** | IS band contains the OOS band's midpoint in 16/20 books admissible in both windows |

Pass counts: **57 of 850 cells at 10 bps, 34 of 850 at 25 bps.** Whole panels are empty: ETF36 0/170
and SMALL 0/170 cells pass at any gross — on those panels the Sharpe legs fail everywhere, so no
gross exists that could rescue them. That is the cleanest form of the answer: the dial cannot buy a
Sharpe leg.

## Rule 8 walk-forward (required)

**WF-A** — bands refitted inside IS (..2016-12-31) and OOS (2017-01-01..) separately:
the **same legs bind the same edges in 20 of 20** books admissible in both windows (CAGR below, DD
or the grid above, every time). The band's *position* drifts (OOS bands sit 0.05–0.10 lower in
gross, because the OOS window's SPY CAGR floor is higher), its *anatomy* does not.

**WF-B** — gross chosen by IS Sharpe alone: because Sharpe is flat in gross, this rule lands at
g=1.00 for 48 of 50 books, i.e. **it is close to arbitrary** and lands outside the 4b band in
nearly every case. Best IS-Sharpe cell over the whole grid = U56/R620/M @ g=1.00 (IS Sharpe 1.30);
OOS read once: CAGR 22.30%, Sharpe 1.12, MaxDD −30.6% vs SPY 15.33% / 0.88 / −33.7% vs RULES v2
9.47% / 1.28 / −12.1%. Higher CAGR and Sharpe than SPY, but −30.6% is far outside 4b's DD cap.

**WF-C (POST-HOC — added after WF-A/WF-B were read and labelled as such, not pre-registered)** —
gross = midpoint of the IS-admissible band, OOS read once: **11 of 27 books pass all four in-window
4b legs out of sample.** The failures are almost all DD (the OOS window's drawdown is deeper than
the IS window's at the IS-chosen gross), never a Sharpe leg — the same anatomy again.

## The one candidate, and why it is PARKED and not a KEEP

`U56 / MA-DG / monthly / g=1.00` — hold every U56 instrument above its 200-day average, equal
weight at g/N of NAV over **all priced names** (gated-out weight to cash, never re-spread),
rebalanced monthly:

| window | CAGR | Sharpe | MaxDD | halves |
|---|---|---|---|---|
| full | 11.92% | 1.21 | −15.5% | 1.26 / 1.17 |
| OOS (2017–) | 12.65% | 1.27 | −15.5% | — |
| SPY full | 15.16% | 0.89 | −33.7% | 0.96 / 0.83 |
| SPY OOS | 15.33% | 0.88 | −33.7% | — |
| RULES v2 full | 8.63% | 1.20 | −12.1% | 1.23 / 1.18 |

Passes 4b at g = 0.90, 0.95, 1.00 (3 contiguous rungs, 2 of them at 25 bps); IS band 0.95–1.00,
OOS band 0.90–1.00, overlapping, same binding legs; the IS-chosen gross passes 4b out of sample.
Fails 4a (MaxDD −15.5% vs v2's −12.1%).

**It is PARK, not KEEP**, for one honest reason: it is the best of **50 books read off one grid**,
and 57 cells passed. Choosing it is a third selection on top of this run's two tuned parameters.
It deserves a dedicated pre-registered run (queued as idea 805), not a promotion.

Proposed RULES wording **for that run to test, not to adopt now** — 10 lines:

```
RULES v3 (CANDIDATE, not adopted — for a dedicated pre-registered run)
1. Universe: research/universe.json (U56), current constituents.
2. Eligibility: an instrument is IN on day t if close(t) > its 200-day simple moving average.
3. Weight: each IN instrument gets G / N of NAV, where N = ALL instruments priced that day,
   IN or OUT (so the book de-grosses; gated-out weight goes to CASH and is never re-spread).
4. Gross G = 1.00.
5. Rebalance monthly (last trading day), fills next day.
6. No ranking, no vol filter, no score, no leverage, no shorting.
7. Costs assumed 10 bps per unit turnover.
8. Daily hard exit is NOT part of this candidate — the monthly cadence is the whole timing rule.
9. Supersedes nothing until a pre-registered run reproduces 4b out of sample on its own.
10. Version bump and CHANGELOG entry only via the Sunday review (PROTOCOL rule 6).
```

## Caveats

**SURVIVORSHIP.** U56 / ETF36 / B136 / BSTK100 are current constituents of `universe.json` /
`universe_broad.json`; SMALL is the current constituent list of its screen with the 52 tickers whose
`max_1d_move ≥ 1.0` dropped first (663 tradable). Names that died are absent from all five panels,
so every CAGR above is biased upward and every CAGR-floor pass is **easier** than it would be on a
point-in-time panel. Since the CAGR floor is the leg that sets every band's lower edge, survivorship
bias moves every band's lower edge **down** — the true bands are narrower than the ones published
here, in the direction that makes 4b harder.

**Gates.** G1 fast_backtest vs engine.backtest max|Δ| = 1.7e-17 (bar 1e-9). G3 weights(g) =
g·weights(1.00) exactly (0.0) for all five forms, which is what licenses building each book once and
scaling. G2 comparands printed above so every bar can be checked by hand.

**PROTOCOL.** 10 bps per unit turnover (25 bps reported beside it, never selected on), next-day
fills, no shorting, no leverage. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
