# Idea 508 — price the 4a MaxDD leg against a VOL-MATCHED cap (lane B, 2026-09-11)

**VERDICT: the queue's DIAGNOSIS is CONFIRMED and its FIX is KILLED.** Restating
PROTOCOL 4a's MaxDD leg as a volatility-matched cap flips **2 of 244 arm-rows (0.8%)** —
one arm at two rungs — leaves 4a still decided by its drawdown leg, and destroys **all 14**
of the corpus's committed 4b passes. No KEEP on either path under any statistic, no book
promoted, no RULES or PROTOCOL change applied; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

Script `2026-09-11_price-the-4a-MaxDD-leg-against-a-VOL-MATCHED-cap_B.py`, runtime 44.0 s,
10 bps headline + 25 bps rung, weekly cadence (except the cadence dial), weights at t
applied at t+1, no network. Two tuned parameters exactly as the queue allows — matching
statistic (5 points) × panel (3) — **all 15 cells reported**; the cost rung is a second
reading of the same books through the exact decomposition `r(c) = r(0) − turnover·c/1e4`.

## Gates (all PASS)
| gate | result |
|---|---|
| G1 `fast_run` vs `engine.backtest` @10 bps (U56, RULES v2) | max\|dr\| **6.939e-18**, max\|dturnover\| **2.880e-16** |
| G2 cost-rung identity vs a live 25 bps run (SMALL439, band 0.05) | max\|dr\| **6.939e-18** |
| G3 RULES v2 on U56 @10 bps | 8.61% / 1.1998 / −12.05% / 1.2349 / 1.1718 (idea 500 published 8.66% / 1.2056 / −12.05% / 1.2259 / 1.1908 — **two extra tape days**, 2026-09-08 → 2026-09-10) |
| G4 idea 270R SMALL439 band 0.05 @10 bps | 4.18% / 0.6183 / −14.59% / 0.6385 / 0.6031 — **every published digit**, tape unchanged |
| G5 CAP identity | `CAP(NONE)` = base.MaxDD exactly; `CAP(VOL)` at a 2×-vol arm = 2 × base.MaxDD exactly |
| corpus | **244 arm-rows** (174 published + 70 extension), 15 Sharpe-clears (6.1%), MaxDD leg cuts 13 (86.7%) — **idea 500's three headline numbers reproduced exactly** |

## 1. The premise is right: the DD leg is mostly an exposure fact
|MaxDD| regressed on realised vol across the corpus (10 bps rung):

| panel | n | slope | R²(VOL) | R²(GROSS) | \|DD\|/VOL min · med · max |
|---|---|---|---|---|---|
| U56 | 39 | 1.505 | **0.715** | 0.646 | 1.280 · 1.745 · 2.962 |
| B136 | 41 | 1.811 | **0.893** | 0.740 | 1.581 · 1.830 · 2.611 |
| SMALL439 | 42 | 2.816 | **0.955** | 0.912 | 2.045 · 2.403 · 3.062 |

71–95% of the cross-sectional variance in an arm's drawdown is its realised volatility.
The queue's complaint about the cap is factually correct.

## 2. The fix changes almost nothing on 4a
| s | 4a passes | flip ↑ | flip ↓ | DD-leg survival among the 15 Sharpe-clears | 4b passes | 4b flip ↓ |
|---|---|---|---|---|---|---|
| NONE (incumbent) | 2 | – | – | 13.3% | 14 | – |
| VOL | 4 | 2 | 0 | 26.7% | **0** | 14 |
| SEMIVOL | 4 | 2 | 0 | 26.7% | **0** | 14 |
| SQRTVOL | 3 | 1 | 0 | 20.0% | **0** | 14 |
| GROSS | 4 | 2 | 0 | 26.7% | **0** | 14 |

Both flips are the **same arm**: SMALL439 band = 0.08, at 10 and 25 bps. Nothing flips on
U56 or B136 at all (U56 has 0 Sharpe-clears, B136 has 1 and it stays cut). The matched cap
leaves 4a a drawdown test: it still cuts **11 of 15** Sharpe-clears instead of 13 of 15.

**The fix rescues exactly one of the two arms the queue named.** Band 0.08 breaches the live
book by 0.23 pp (−14.91% vs −14.68%) on 2.6% more vol → rescued. Band 0.12 breaches by
1.32 pp (−16.00%) on only 5.2% more vol → still cut. The queue's own example splits 1–1.

## 3. Matching is not neutral — its direction is the comparand's own vol
4a's comparand (RULES v2) is a **low-vol** book (0.070–0.072), so matching **loosens** the cap
for the higher-vol arms: +2 passes. 4b's comparand (SPY) is a **high-vol** book (0.170–0.177),
so matching **tightens** it for the low-vol books that pass 4b — and kills every one of them.
All 14 corpus 4b passers (9 U56, 5 B136) run vol 0.095–0.110 against SPY's 0.177: the cap
moves from a flat −20.23% to −10.8%…−12.6% and none of them clears it. A "neutral
restatement" that zeroes one KEEP path is a different bar, not a restatement.

## 4. Rule 8 (PROTOCOL 8) — statistic and arm chosen on 2009-2016 only, 2017-2026 read once
30 cells (3 panels × 2 rungs × 5 statistics); 19 produce a pick. Full table in
`.walkforward.csv`. The decisive cell:

| panel / rung | s | pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| SMALL439 @10 | NONE | cadence = M | 4.38% | **0.6207** | −16.75% |
| SMALL439 @10 | VOL / SEMIVOL / SQRTVOL / GROSS | n = 20 | 4.08% | **0.3612** | **−32.04%** |
| — RULES v2 (live) OOS | | | 3.85% | 0.5680 | −14.68% |
| — SPY OOS | | | 15.45% | 0.8820 | −33.72% |

Matching **replaces the one rule-8 pick in the corpus that beats the live book with one that
loses 0.26 of OOS Sharpe and doubles OOS drawdown to SPY's own −32%** — it admits precisely
the high-vol arm the incumbent cap was keeping out. Elsewhere the matched picks are new but
not better: U56 @10 SEMIVOL picks cadence = M (OOS 1.2226 vs live 1.2747); B136 @10
VOL/SEMIVOL/GROSS pick gross = 1.00 (OOS 1.1174 vs live 1.1185). 6 of 19 picks beat the live
book OOS and **all 6 are the same SMALL439 cadence = M book that the incumbent cap already
finds** (NONE @10 and @25, plus all five statistics @25) — not a matched-cap discovery. Unconditional IS-Sharpe chooser (no 4a filter), 10 bps: U56 1.1627
(band 0.08), B136 1.1095 (band 0.08), SMALL439 0.3612 (n = 20).

## 5. Both KEEP paths, 10 bps headline (122 arm-rows)
| s | 4a | 4b | BOTH |
|---|---|---|---|
| NONE | 1 | 13 | **0** |
| VOL | 2 | 0 | **0** |
| SEMIVOL | 2 | 0 | **0** |
| SQRTVOL | 1 | 0 | **0** |
| GROSS | 2 | 0 | **0** |

**No KEEP-candidate on any path under any statistic. No memo filed.**

## 6. What this does and does not license (PROPOSED only — Sunday review decides)
- **Do not** adopt a vol-matched 4a MaxDD leg. It buys 0.8% of verdicts, keeps 4a a drawdown
  test (73.3% cut rate), and its only out-of-sample consequence in this corpus is negative.
- The queue's diagnosis stands and is better stated as a **scale-free reading**: a vol-matched
  cap is exactly `arm.MaxDD/arm.VOL ≥ base.MaxDD/base.VOL`, i.e. a path-**shape** test that by
  construction gives no protection against the size of a real drawdown. PROTOCOL 4b's 60%-of-
  SPY cap exists because capital cares about the level, not the shape; matching it away is the
  wrong direction for the path that matters for capital.
- A defensible one-line PROTOCOL wording, if Sunday wants one, is to say so explicitly:
  *"4a's MaxDD leg is an absolute cap, not a risk-adjusted one; an arm that needs more vol to
  beat the book on Sharpe must be judged on path 4b."* **Not applied here.**

Artefacts: `.arms.csv` (244 arm-rows + 24 comparands, every statistic's cap and verdict),
`.flips.csv`, `.bypanel.csv`, `.bydial.csv`, `.flippers.csv`, `.exposure.csv`,
`.walkforward.csv`, `.console.txt`.
SURVIVORSHIP: B136 is current constituents of `universe_broad.json`; SMALL439 is the sub-$2B
screen with the 44 tickers whose `max_1d_move ≥ 1.0` dropped first (idea 500's panel).
