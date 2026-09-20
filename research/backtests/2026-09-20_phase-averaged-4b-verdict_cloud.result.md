# Idea 956 — does a PHASE-AVERAGED 4b verdict change which books in the record PASS?

**2026-09-20, lane cloud (idea 2 of 2). ANSWERED: BARELY, AND ONLY IN ONE DIRECTION.
KILL the queue's proposal as a PROTOCOL change; PARK one reporting line (the phase pass-share),
which separates the record's one fragile 4b pass from its robust ones at zero cost.
NO NEW BOOK; RULES.md and PROTOCOL.md untouched (rule 6).**

Script `research/backtests/2026-09-20_phase-averaged-4b-verdict_cloud.py` ·
`.grid.csv` (1,872 scored books) · `.verdicts.csv` (864) · `.walkforward.csv` (108) ·
`.gates.csv` · `.log.txt` / `.console.txt`. **Gates 28/28.**

## The corpus — real books, not a prose census

Six books the record has certified as 4b passers or is currently standing on, re-built from
source: **TOP20** (the 2026-09-04 first KEEP-4b shape — top 20 on the composite, no vol scaler,
fixed g/N, g = 0.75), **BAND03_G075** (the live RULES v2 book), **BAND10_G100** (idea 1719/896's
U56 4b passer), **EWELIG**, **MAXVOL060** (idea 1617's PARK), and **VOLTGT016** (the standing
KEEP-4b candidate found by idea 1730 *this day*). 6 books × 3 panels × 26 phases × 4 cost rungs =
**1,872 scored books**, every one published.

Dial 1 = **phase grid**: DOM21 (monthly, rebalance *d* trading days before each month's last
trading day, d = 0…20 — the 21 DOM phases the idea names) and DOW5 (weekly, d = 0…4). Dial 2 =
**averaging rule**: CANON (d = 0, what PROTOCOL reads today), MEAN, **MEDIAN** (the rule the queue
names), MIN, SHARE50 (majority vote) and TRANCHE (1/P of NAV in each phase-book, re-levelled
daily). Both levels of both dials reported, neither chosen.

**The distinction this run refuses to blur** (inherited from idea 964, and it decides the verdict):
MEAN / MEDIAN / MIN / SHARE50 are **estimators**. No allocation of capital produces a
median-of-Sharpes, so none of them can ever *be* a KEEP — they can only certify or de-certify one.
**TRANCHE alone is tradable.**

## The answer

144 (panel × grid × book × cost) cells; CANON certifies **30** on 4b FULL and **31** on 4b OOS.

| rule | 4b FULL passes | CANON passes surviving | newly certified | disagreement with CANON |
|---|---|---|---|---|
| CANON | 30/144 | 30/30 | 0 | 0.000 |
| MEAN | 33/144 | 25/30 | **8** | 0.090 |
| **MEDIAN** | **25/144** | **25/30** | **0** | **0.035** |
| MIN | 16/144 | 16/30 | 0 | 0.097 |
| SHARE50 | 25/144 | 25/30 | 0 | 0.035 |
| TRANCHE *(tradable)* | 38/144 | 30/30 | 8 | 0.056 |

4b OOS is the same shape: MEDIAN 24/144, 24 of 31 surviving, 0 newly certified, disagreement 0.049.

Three things follow, and the first is the finding:

1. **The median is strictly one-directional.** It de-certifies **5 of 30** CANON passes and
   certifies **nothing** CANON misses. MEAN goes the other way (8 newly certified, 5 lost),
   because the mean MaxDD across phases is shallower than any single bad phase. **The averaging
   rule is not a neutral estimator choice — it picks which way the 4b bar leans**, which is
   precisely why it should not be adopted without saying so.
2. **At the 10 bps primary rung, MEDIAN and CANON disagree on 1 of 36 cells** — so the queue's
   proposal, taken as a re-publication rule, would move almost nothing.
3. **That one cell is the record's own first KEEP-4b book.** U56 / DOM21 / **TOP20** passes 4b at
   the canonical month-end and **fails at 16 of its 21 DOM phases** (phase pass-share **0.238**).
   It de-certifies at every cost rung, 0 / 10 / 25 / 50 bps. The other four losses are the same
   book on the other grid/rung (B136 / DOW5 / TOP20 at 0 bps). **Every de-certified cell in the
   run is TOP20.**

## The phase pass-share separates the record's fragile pass from its robust ones

Published for every cell; the headline column at 10 bps:

| book | U56 DOW5 | B136 DOW5 | U56 DOM21 | B136 DOM21 |
|---|---|---|---|---|
| **VOLTGT016** *(standing KEEP-4b candidate)* | **0.800** ✓ | **1.000** ✓ | 0.143 ✗ | 0.048 ✗ |
| BAND10_G100 | 1.000 ✓ | 0.800 ✓ | 0.476 ✗ | 0.000 ✗ |
| MAXVOL060 | 1.000 ✓ | 0.800 ✓ | 0.476 ✗ | 0.048 ✗ |
| **TOP20** | 1.000 ✓ | 0.000 ✗ | **0.238 ✓ ← the artefact** | 0.048 ✗ |
| BAND03_G075 (live) | 0.000 | 0.000 | 0.000 | 0.000 |
| EWELIG | 0.000 | 0.000 | 0.000 | 0.000 |

(✓ / ✗ = CANON's 4b FULL verdict.) Every certified cell in the corpus has a pass-share of
**0.800–1.000 except one, which has 0.238**. The statistic is free — it falls out of the same 21
runs a phase check already makes — and it is the one line that would have flagged the 2026-09-04
book's fragility at the time without changing what PROTOCOL certifies.

**The standing KEEP-4b candidate survives.** VOLTGT016 clears 4b FULL *and* OOS at **5 of 5**
weekly phases on B136 and **4 of 5** on U56, and holds its certification under CANON, MEAN,
MEDIAN, SHARE50 and TRANCHE alike (only MIN drops it to 1 of 6). Its DOM21 failure is not a phase
result: on a *monthly* cadence the book's OOS MaxDD blows out to −24.2 % (U56) and −26.1 % (B136)
against −19.9 % / −18.8 % weekly, so it simply is not a 4b book at that cadence. **The candidate's
4b pass is cadence-dependent and phase-robust**, and the memo now says so.

## Both KEEP paths, per-phase (1,872 books, 10 bps shown)

| grid | 4a FULL | 4a OOS | 4b FULL | 4b OOS |
|---|---|---|---|---|
| DOM21 | 0/378 | 7/378 | 31/378 | 31/378 |
| DOW5 | 1/90 | 11/90 | 32/90 | 32/90 |

Binding legs among the 405 4b FULL failures at 10 bps: **L4_DD 0.654**, L5_CAGR 0.637, L2_H2
0.462, L3_OOS 0.412, L1_H1 0.240 — the DD cap is the most frequently binding leg, reproducing
idea 944's ranking on an independent corpus.

## Rule 8 (phase chosen on 2009–2016 only, 2017–2026 read exactly once)

| grid | arm | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | 4a OOS | 4b OOS |
|---|---|---|---|---|---|---|
| DOM21 | IS_PICK | 0.8929 | 9.60 % | −23.16 % | 1/18 | 1/18 |
| DOM21 | CANON | **0.9144** | 9.70 % | −22.31 % | 2/18 | 1/18 |
| DOM21 | TRANCHE | 0.8745 | 9.23 % | −22.46 % | 0/18 | 3/18 |
| DOW5 | IS_PICK | 0.9070 | 9.10 % | −18.18 % | 1/18 | 6/18 |
| DOW5 | CANON | 0.9128 | 9.15 % | −17.95 % | 0/18 | 8/18 |
| DOW5 | TRANCHE | **0.9149** | 9.12 % | −17.52 % | 3/18 | 7/18 |

**Choosing the rebalance date in sample is worth −0.0215 of OOS Sharpe on DOM21 (3 of 18 wins) and
−0.0058 on DOW5 (7 of 18).** Idea 944's reading holds on this corpus: the phase is a **KILL as a
dial**. The tradable TRANCHE buys −0.0400 (DOM21) and +0.0021 (DOW5) against CANON — i.e. nothing
— so "trade the phase average" is not a book worth building either. Bars: SPY OOS
**15.26 % / 0.8737 / −33.72 %**; live RULES v2 OOS 9.46 % / 1.2766 / −12.05 % (U56),
7.85 % / 1.1017 / −12.24 % (B136), 3.64 % / 0.5458 / −14.16 % (SMALL).

## Verdict

**KILL the queue's proposal.** Replacing PROTOCOL's canonical-date 4b verdict with a phase median
would move **1 cell in 36** at the primary cost rung, can never itself certify a book (a
median-of-Sharpes is not a portfolio), and its tradable cousin earns nothing. Pre-registered
outcome **(c)**, with a named exception to it, plus **(d)** confirmed.

**PARK, for a future Sunday review only** (PROTOCOL.md is *not* modified by this run): publish the
**phase pass-share** beside every 4b verdict. It is free, it is a statement about the book rather
than about an estimator, and on this corpus it is the single number that separates the record's one
fragile 4b certification (TOP20 at 0.238) from every robust one (0.800–1.000).

## Caveats, stated

* **Survivorship (rule 9).** U56 / B136 / SMALL are *current* constituents; SMALL additionally
  drops the **54** tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv` (665 names remain).
  Every CAGR and drawdown *level* is optimistic and both 4b bars are easier here than on a
  point-in-time panel. The phase contrasts are same-tape, same-names, same-rule comparisons with
  only the rebalance date moved, and are far less exposed; the 4b levels are read against SPY,
  which is not survivorship-inflated.
* The corpus is six books, not the record's full committed list; it is the set the record is
  currently standing on plus its first KEEP-4b shape. A wider corpus could move the 5-of-30 count.
* **Published, not hidden:** `engine.backtest` does `.fillna(0).shift(1)` on the weights, so its
  row-0 target is NaN and its returns and turnover are NaN on day 0 and on the first rebalance day
  (2008-01-02 and 2008-01-07 on U56/B136; 2010-01-04 and 2010-01-08 on SMALL). Every script in the
  record skips those via the 260-day warm-up, and so does gate G1, which compares over the scored
  window only.
* **Gates 28/28**, including **G3 cross-run**: idea 1730's committed VOLTGT t = 0.16 memo cells
  reproduce to **max|Δ| 0.0000** on CAGR / Sharpe / MaxDD / OOS CAGR / OOS Sharpe on both U56 and
  B136 — this run nests the standing candidate's own numbers. Also G0 phase-0 masks identical to
  `engine.rebalance_mask` on M and W (0 diffs, all panels); G1 fast runner == `engine.backtest` to
  < 1e-12 on returns and turnover; G2 rebalance rate 12.04–12.11 /yr (DOM21) and 52.28–52.35 /yr
  (DOW5); G4 determinism bit-identical on a re-built cell; G6 two dials; G7 no chooser reads a row
  ≥ 2017-01-01; G8 all 1,872 + 864 + 108 rows published.
