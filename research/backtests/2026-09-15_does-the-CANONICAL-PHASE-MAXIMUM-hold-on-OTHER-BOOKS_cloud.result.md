# Idea 942 (cloud, 2026-09-15) — does the CANONICAL PHASE MAXIMUM hold on the record's OTHER committed MONTHLY and QUARTERLY books?

**ANSWERED = NO, on every reading. KILL for "canonical = max" as a general fact.** It reproduces
exactly where 938 measured it (G3: **16 of 16**) and dies everywhere else: the pooled rate over
300 (book × panel × gross × cadence × rung) cells is **0.177**. It is **not universal** (H_UNIV
0.177 vs bar 0.90), **not a property of TOP20** (H_BOOK: TOP20 0.333, non-TOP20 0.138 — TOP20
fails its own bar), and **not a lookback alias** (H_ALIAS: the two books with *no* momentum
lookback score **higher**, 0.192, than the three that use one, 0.167). The one thing that does
generalise is a negative, and it is absolute: **on the quarterly grid the canonical phase is the
maximum in 0 of 150 cells.** "Canonical = max" is a *month-end* fact about a handful of
large-cap cells, not a period-end fact.

## Gates — 6 of 6 PASS, printed before any number of the hypothesis was read
`G0` `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on W/M/Q, 0 differing rows · `G1` fast runner
≡ `engine.backtest` @10 bps, worse of M and Q **2.082e-17** · `G2` BAND03 @0.75 ≡
`rules_v2_weights` (the LIVE rules), **0.0** · `G4` every phase trades 12/yr (M: 12.02–12.08) or
4/yr (Q: 3.97–4.03), 0 of 84 out of band · `G5` determinism, **0.0** · **`G3` 938's published 16
of 16 replays EXACTLY** (TOP20 / M / U56+B136 × CORE+EXT × 0/5/10/25 bps, every `canon_pctile`
1.000). 938's finding is real; this run is measuring its reach, not disputing it.

## The grid
5 books × 3 panels × 2 gross (CORE 0.75 / EXT 1.00) × (21 M + 63 Q) phases × 5 cost rungs
(0/5/10/25/50 bps) = **12,600 published grid rows**, 600 family cells. Two tuned dials only (book
set, cadence); panel, gross, cost and statistic are reported axes with nothing fitted on them.

## The answer — canonical-is-CAGR-max rate, pooled over panel × gross × rung (30 cells each)
| book | lookback? | M | Q |
|---|---|---|---|
| TOP20 (938's book) | yes | **0.667** | **0.000** |
| EWELIG | **no** | 0.433 | **0.000** |
| TOP05 | yes | 0.333 | **0.000** |
| BAND03 (= RULES v2) | **no** | 0.333 | **0.000** |
| TOP10 | yes | **0.000** | **0.000** |
| **pooled** | | **0.353** | **0.000** |

- **H_UNIV NOT SUPPORTED** — 0.177 pooled (53 of 300), bar 0.90.
- **H_BOOK NOT SUPPORTED** — TOP20 0.333 pooled, below its own 0.90 bar. On the M cadence alone
  TOP20 reaches 0.667, and at 10 bps/M it is 1.000 on U56 and B136 — **and 0.000 on SMALL.** So it
  is not even a property of TOP20; it is a property of *TOP20 on the two large-cap panels,
  monthly*.
- **H_ALIAS NOT SUPPORTED, and refuted in the right direction** — composite books 0.167,
  lookback-free books **0.192**. EWELIG ranks nothing and BAND03 is a pure 200d-band book; neither
  can alias a 21-day momentum leg, and both beat TOP10's 0.000. The signal is not the carrier.
- **H_Q NOT SUPPORTED, and this is the run's strongest number** — M 0.353 vs Q **0.000**, gap 0.353
  against a 0.20 bar. Across all 150 quarterly cells the canonical phase's mean percentile inside
  its own 63-phase family is **0.170** and its *best* is 0.540. Quarter-end is not month-end.

## The lookback probe (REPORTED, never selected on) — U56 / TOP20 / CORE / M / 10 bps
| composite short leg | canonical CAGR | family max | argmax phase | canonical is max |
|---|---|---|---|---|
| 0 d | 14.77% | 14.85% | 12 | no |
| 5 d | 14.61% | 14.65% | 1 | no |
| 10 d | 14.69% | 14.74% | 1 | no |
| **21 d (committed)** | 14.69% | 14.69% | **0** | **yes** |
| 42 d | 14.53% | 14.53% | 0 | yes |
| 63 d | 14.40% | 14.40% | 0 | yes |

The argmax **does** move with the lookback on TOP20 (canonical is the max at 3 of 6). So the
aliasing story has a real mechanism *on this one book* — but it cannot be the general carrier,
because the two books that have no lookback at all score higher than the ones that do. Both
readings are published; neither rescues H_ALIAS.

## The phase spread is the story the record should carry instead
The phase is a free parameter worth a great deal of CAGR and nothing is fitted on it in the live
rules. Median family spread **3.04 pp (M)** and **4.37 pp (Q)**, maxima **12.49 pp** and
**23.93 pp**. Examples at 10 bps / CORE: U56 TOP05/M spans 17.11%–21.56% (4.45 pp) with the
canonical at percentile **0.238**; SMALL TOP05/Q spans −0.72%–17.16% (**17.88 pp**) with the
canonical at percentile 0.095. Any single-phase CAGR quoted without its family spread is
unadjudicable.

## Rule 8 walk-forward — phase AND book chosen on 2009–2016 ALONE, 2017–2026 read ONCE (10 bps, CORE)
| panel | cad | chooser | picked | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 | M | IS CAGR / Sharpe max | TOP05/ph01 | 1.326 | 19.0% | 0.988 | −25.2% | n | n (`L4_DD`) |
| U56 | M | canonical ph00, best IS book | TOP05/ph00 | 1.280 | 15.6% | 0.824 | −27.2% | n | n (`L2_H2,L3_OOS,L4_DD`) |
| U56 | Q | IS CAGR / Sharpe max | TOP05/ph50 | 1.369 | 21.2% | 0.998 | −24.5% | n | n (`L4_DD`) |
| B136 | M | IS Sharpe max | TOP05/ph01 | 1.354 | 20.6% | 0.958 | −28.4% | n | n (`L4_DD`) |
| B136 | M | canonical ph00, best IS book | TOP20/ph00 | 1.234 | 15.5% | 1.000 | −26.1% | n | n (`L4_DD`) |
| SMALL | M | IS CAGR / Sharpe max | TOP10/ph05 | 1.019 | 4.7% | 0.327 | −35.5% | n | n (all five) |

SPY over the same OOS window: **15.1% / 0.874 / −33.7%** (U56 tape). Live RULES v2 baseline OOS
Sharpe 1.277 (U56), 1.106 (B136), 0.560 (SMALL).

**OOS 4b PASS 0 of 18. OOS 4a PASS 0 of 18.** And the decisive line for capital: **the in-sample
choosers land on the canonical phase in 0 of 12 cells.** Where the in-sample maximum *is* the
canonical phase (938's cells), choosing it out of sample buys nothing; where it is not, the
in-sample phase pick reliably fails OOS on **`L4_DD`** — it buys 3–6 pp of OOS CAGR with 2–5 pp of
extra drawdown and loses the 4b DD cap doing it. **This run adds no book and touches no rule.**

## Survivorship (PROTOCOL rule 9)
U56 / B136 / SMALL are current-constituent lists; SMALL additionally drops the **52 tickers with
`max_1d_move` ≥ 1.0** per `data/small_meta.csv` (**663 names + SPY benchmark**). Every CAGR,
Sharpe and drawdown **level** above is optimistic. The `canonical = max` tallies are **same-tape,
same-universe, same-weights** comparisons that differ only in *which day* the identical book
trades, so they are unaffected by panel composition. The 4b levels in the walk-forward are read
against SPY, which is not survivorship-inflated — a survivor panel makes books look **better** and
4b failures **rarer**, which cuts against this run's 0-of-18, not for it.

## What this changes
1. 938's `canon pctile 1.000` should be restated in the record as a fact about **TOP20 on U56 and
   B136, monthly** — not about month-end, and not about the book set.
2. **The quarterly result is publishable on its own: 0 of 150.** No committed quarterly claim
   anywhere in the record may assume the canonical phase is its family's best point.
3. Every published single-phase CAGR needs its family spread beside it (median 3.04 pp M /
   4.37 pp Q, max 23.93 pp).

## Follow-ups filed
961 (why is the canonical phase *systematically low* on the Q grid — mean percentile 0.170, and
the argmax never lands closer than **17 trading days** before quarter-end, median 29, range 17–51,
mode 23) · 962 (does the
phase-argmax chosen in sample ever survive out of sample on ANY book, or is `L4_DD` its universal
OOS failure) · 963 (price the phase family spread as a required companion statistic for every
committed cadence claim, the way idea 943 did for null gains).
