# Idea 922 (cloud, 2026-09-15) — why is the IS H1 Sharpe leg unpassable for CAND20 on U56?

**ANSWERED = THE ELIGIBILITY FILTER, AND THE LEG IS A U56 PANEL FACT, NOT A BOOK FACT.
KILL for both of the queue's other two candidates (cash-drag and concentration-alone). Nothing
promoted, no RULES / PROTOCOL change, no memo.**

Script `2026-09-15_why-is-the-IS-H1-SHARPE-leg-UNPASSABLE-for-CAND20-on-U56_cloud.py`.
3 panels × 6 arms × 30 gross rungs × 4 cost rungs = 2,160 scored books, plus a 150-rung fine
ladder (H_FLAT), a 480-row episode scan and its all-blocks calibration, and 18 rule-8 picks.
Two tuned parameters, the queue's own: **sub-window** (14 levels, all reported) and **panel**
(3 levels, all reported). **GATES 7 of 7 PASS**, including an exact cross-run reproduction of
idea 675's committed `.ladder.csv` (150 rungs, max |ΔIS_H1| 0.000e+00, leg verdict agrees
150/150, 0 passes in both runs).

## The correction that reframes the question (G7)

Idea 675's docstring calls CAND20 a book that holds "the rest in CASH (de-gross, never
re-spread)". Its committed `ranked_w1` divides by the **realised** k, so the book re-spreads to
**full gross g whenever at least one name is eligible**. On U56 the eligible count never reaches
zero (min 3, median 41, below 20 on 487 of 4,444 days), so **CAND20 is fully invested on every
day of the sample and has no cash channel at all** — target gross deviates from g by 0 on U56
across all four 2×2 arms. The single day in the whole record where the book would hold cash is
**SMALL, 2020-03-19**. RULES v2 (`BAND03`) is the arm that actually de-grosses (mean 0.685 of g
in the leg window). The 200d-MA / vol filter is therefore a **name filter**, not a cash position,
and the queue's "cash-drag" candidate has no mechanism in this book.

## The three candidates

| candidate | verdict | the number |
|---|---|---|
| **CASH (constant gross)** | **KILL, twice over** | Sharpe is scale-free: over the 150-rung 0.01 ladder the leg-window Sharpe moves ≤ **0.0154** (0 bps), ≤ **0.0173** (10 bps), ≤ **0.0258** (25 bps) on every arm and panel. And per G7 the book holds no cash to begin with. |
| **CONCENTRATION** | **FAIL — but on a 0.008 knife edge** | Removing it (`EWELIG`, equal-weight every eligible name) still fails the leg at **0 of 30** rungs: 0.8301 against SPY's 0.8378. It closes 93% of the gap and misses by **0.0077**. |
| **ELIGIBILITY FILTER** | **PASS — the carrier** | Removing it (`CAND20_NG`, same score, same top-20, no MA/vol filter) clears the leg at **30 of 30** rungs: 0.9123 vs 0.8378. |

**The 2×2 at g = 0.75, 10 bps, U56, leg window (ISH1_HALF, 2009-01-13 … 2013-01-07, 1,003 days):**
`EWALL` (neither feature) 1.0384 — the U56 equal-weight index beats SPY by **+0.2006** —
then the filter gives back **−0.1953**, concentration **−0.1130**, interaction **+0.0260**,
landing CAND20 at 0.7300, i.e. **−0.1077 under SPY**. The filter's main effect is negative in
**13 of 14** sub-windows on U56; concentration's in 8 of 14.

## The other pre-registered bars

- **H_MEANVOL FAIL, and the direction is the useful part.** The exact decomposition reads
  **MEAN −0.420, VOL +0.312** (bar: |mean| > 2×|vol|; actual 1.35×). The book earns **8.62%**
  annualised against SPY's **17.29%** in the leg window at **11.81%** vol against SPY's **20.63%**.
  It is not that the book is too volatile — it gives up more than half the return and buys back
  three-quarters of that with vol. The leg is a return shortfall only partly rescued by vol.
- **H_EPISODE PASS as pre-registered, REFUTED by its own calibration.** The best ≤ 60-day excision
  is **2009-03-10 … 2009-05-08 (43 days, the March-2009 rebound)**, which moves the gap
  −0.108 → **+0.229**, and a block as short as **L\* = 3** flips it. But that is an argmax over
  ~60,000 blocks. Over **all** contiguous blocks, only **3.1%** of 43-day and **5.8%** of 60-day
  excisions flip the leg, and the median excision leaves the gap at **−0.103** — unchanged. **The
  gap is a persistent level, not an episode.** The pre-registered bar was too weak; both readings
  are published.
- **H_PANEL FAIL — and this is the headline.** The same book, same leg, same days: **U56 0 of 30,
  B136 30 of 30, SMALL 30 of 30.** On B136 CAND20 reads 0.967 against SPY's 0.838 and essentially every
  contiguous excision leaves it passing (flip share **0.995–1.000** across L = 5…60). *"`L1_H1` is
  unpassable for CAND20" is a statement about U56, not about the book.*

## Rule 8 (required) — (arm, gross) chosen on 2009-2016 alone, 2017-2026 read once

18 picks = 3 panels × 6 selectors (three IS-only choosers, two no-leverage variants added because
the record's gross axis runs past 1.00 while PROTOCOL 2 forbids leverage, and the zero-parameter
`PICK_LIVE`). **OOS 4b 1 of 18, OOS 4a 2 of 18.**

On U56, every IS-only chooser abandons the filter and picks **`CAND20_NG`** — the arm that wins
the in-sample leg — and it **fails 4b out of sample on the DD cap alone**:
17.25% / **1.141** / **−23.29%** at g=0.80 (cap −20.23%), 21.61% / 1.141 / −28.49% at g=1.00,
32.42% / 1.141 / −40.44% at g=1.50. The zero-parameter `PICK_LIVE` (CAND20 at g=0.75) is the
**only 4b pass in the run**: **14.34% / 1.123 / −18.31%**, against SPY OOS 15.27% / 0.874 /
−33.72% and RULES v2 OOS 9.46% / 1.277 / −12.05%.

**So the filter is exactly what the record thinks it is: it costs Sharpe in the 2009-2013 rebound
and buys the drawdown that the 4b DD cap is made of.** Deleting it to win the in-sample leg is the
one change that would lose the book its only out-of-sample 4b pass. Nothing here is promotable.

## Survivorship

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown **level** above is
optimistic — the book's and the comparands' alike. The 2×2 decomposition and the flip shares are
same-days, same-names contrasts across books and are far less exposed; the leg verdicts and the
rule-8 triples are levels read against SPY, which is not survivorship-inflated, so those are upper
bounds. Stated, not hidden.

## Follow-ups filed

- 924 — is the U56 equal-weight index's **+0.2006** edge over SPY in 2009-2013 a panel-composition
  fact (U56 carries ETFs) or a size fact?
- 925 — `EWELIG` misses the leg by **0.0077**; is that margin inside the record's own
  rebalance-offset spread (idea 806's clause), i.e. is "concentration is not the carrier" a date?
- 926 — the filter costs Sharpe in 13 of 14 in-sample sub-windows and buys the 4b DD cap; price a
  filter that is **partially** on (a vol-cap-only arm, an MA-only arm) on the same 2×2.
