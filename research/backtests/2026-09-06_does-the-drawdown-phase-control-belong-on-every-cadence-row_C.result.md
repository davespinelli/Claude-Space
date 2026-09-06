# idea 273 — does-the-drawdown-phase-control-belong-on-every-cadence-row (lane C, 2026-09-06)

**VERDICT: ANSWERED — YES, the control belongs on every cadence row, and applying it KILLS 24 of
the record's 26 monthly KEEP claims. Two by-products: (i) the Sunday review's own 3-of-8 number
is a DIFFERENT BOOK's — idea 171's by-product as published slides to 5/8, not 3/8; (ii) idea
223's MEAN-21 is the only anchor-robust member of the corpus, and this run finds its own new
limit — it fails 4b at t+5 and t+7 execution lag.** No RULES change is proposed.

Script `research/backtests/2026-09-06_does-the-drawdown-phase-control-belong-on-every-cadence-row_C.py`.
Artefacts: `.console.txt`, `.census.csv` (69 memos classified), `.phases.csv` (1 024 rows),
`.claims.csv` (26 re-priced claims), `.walkforward.csv` (32 rule-8 cells), `.memo.md`.

## What was done

The Sunday review of 2026-09-06 disqualified the top-ranked KEEP-candidate (idea 171's
by-product, min-half Sharpe 1.206) by sliding its month-end schedule 0–7 trading bars with the
decision-to-fill gap held at one bar. That control was applied to two rows, by hand, in the
review. This run applies it to **every** monthly/quarterly row a memo has ever called a
KEEP-candidate, over the **full 21-bar wrap** (u56 and broad both carry 20.88 bars/month), and
adds the quarterly cadence the record has never claimed.

**Two tuned parameters** (PROTOCOL rule 4): PHASE (swept, all 21 points reported) × CADENCE
(M and Q, both reported). Book, panel, cost rung and execution lag are audit axes read off the
parent memos, not choices — every cell the memos asserted is re-priced, none is selected.

## The census (the corpus is read off the record, not chosen)

All **69** `*.memo.md` are classified in `.census.csv`, included and excluded alike, with the
reason. 10 mention a monthly/quarterly word; **6 name a monthly BOOK**; **0 name a quarterly
book — the record has never published a quarterly KEEP-candidate.**

| # | book | memos | construction (u56, gross 0.75, top-20 EW, gate = >200d MA & vol20 < 0.60) |
|---|---|---|---|
| B1 | COMP-M | ideas 171, 188 | scan.py composite, no vol scaler, **SPY untradable**, monthly |
| B2 | R6-M | ideas 173, 182, 182B | R6 / vol20^0.5, ranks every column (SPY included), monthly |
| B3 | MEAN21 | idea 223 | B2 held on all 21 anchors at once, 1/21 each — anchor-agnostic |

## Controls (asserted before any phase > 0 number was read)

* **[A]** `sim(lag=1, phase=0)` == `engine.backtest` to **1.4e-17** (returns) and **0.0**
  (turnover); **[A2]** same on broad, 1.4e-17.
* **[B]** cost identity `net(c) = gross − turnover·c/1e4` vs a direct 10 bps engine run: **1.4e-17**.
* **[C] decisive for B2.** Reproduces idea 182B's committed `.phase.csv` on **8 phases × 17
  columns to 2.220e-16**. This is 182B's instrument, unmodified.
* **[D2] decisive for B1.** Equals idea 171's **committed `.ladder.csv` U56/CADENCE/M row** on 7
  columns to **2.220e-16**.
* **[D]/[E]/[F]** all three books reproduce their memos' published digits (max |d| 5e-4, 4e-4,
  3.1e-4). No book was guessed at; a book that failed the gate would have been recorded
  unauditable.

## The answer

26 memo-asserted monthly 4b claims, each re-priced over the 21 anchors of its own cadence.
Pre-registered: **ROBUST ≥ 19/21, FRAGILE 11–18/21, ANCHOR-ARTEFACT ≤ 10/21.**

| verdict | claims | share |
|---|---|---|
| ROBUST | 2 | 7.7% |
| FRAGILE | 8 | 30.8% |
| **ANCHOR-ARTEFACT** | **16** | **61.5%** |
| **NOT ROBUST (headline)** | **24 / 26** | **92.3%** |

All 26 pass at phase 0 — that is what a published claim is. **The bar that breaks is the
drawdown cap in 24 of 24 cases; H1, H2, OOS and the CAGR floor never break.** The 4b drawdown
condition is the only bar in the protocol that the trade date can move.

The band on the identical rule, u56 @10 bps t+1 — nothing about the book changes across a row:

| book | cadence | MaxDD range | Sharpe range | CAGR range | OOS Sharpe range | 4b (0–20) | 4b (0–7) | 4a |
|---|---|---|---|---|---|---|---|---|
| B1 COMP-M | M | −14.38% .. −22.40% (**8.02pp**) | 1.0417–1.2088 | 13.01–14.98% | 1.0727–1.3286 | **9/21** | 5/8 | 0/21 |
| B2 R6-M | M | −14.67% .. −23.52% (**8.85pp**) | 1.0078–1.1628 | 12.07–13.80% | 0.9882–1.2298 | **12/21** | 7/8 | 0/21 |
| B1 COMP-M | Q | −17.66% .. −28.12% (**10.46pp**) | 0.9999–1.1884 | 12.93–15.25% | 0.9347–1.2842 | **1/21** | 0/8 | 0/21 |
| B2 R6-M | Q | −16.57% .. −26.90% (**10.32pp**) | 0.9705–1.1461 | 12.11–14.19% | 0.9160–1.2183 | **1/21** | 0/8 | 0/21 |

On broad both books are **1/21** at monthly and 0–1/21 at quarterly — the portability failure
the memos report at phase 0 is a 20-of-21 failure, not a one-anchor one.

**Execution lag multiplies the effect.** Idea 182's 9/9-cell claim holds at 12/21 at t+1 but
collapses to **4/21 at t+5 and 3/21 at t+7**: a one-week fill and an unlucky trade date are the
same instrument twice.

**Quarterly, as a pre-registered extension (not an audit — there is no quarterly claim to
audit): the anchor band WIDENS with the cadence**, 7.45pp pooled at monthly against 9.26pp at
quarterly, and neither book's quarterly form clears 4b at more than 1 of 21 anchors. Enumerated
on every 3rd bar of the ~62.65-bar wrap, 21 points; that coarseness is stated, not hidden.

## By-product 1 — the review's 3-of-8 is a neighbouring book (a CORRECTION)

The review reported idea 171's by-product at **3/8, MaxDD −18.41%..−21.33%, "k = 1..5 all breach
the cap"**. On the published book — control [D2], idea 171's own committed ladder row to 1e-16 —
the same slide gives **5/8, −17.74%..−20.74%, 3 of 5 breaching**. The construction that
reproduces the review's digits exactly is **B1x: the identical composite with SPY left IN the
ranking universe**, which idea 171's script forbids in as many words ("SPY: benchmark, never
tradable"):

| | phase-0 MaxDD | 0–7 band | DD-pass 0–7 | 4b 0–7 | 4b 0–20 | k = 1..5 breaches |
|---|---|---|---|---|---|---|
| B1 as published | −19.577% | −17.74% .. −20.74% | 5/8 | 5/8 | 9/21 | 3/5 |
| B1x (SPY in the ranking) | −19.507% | **−18.41% .. −21.33%** | **3/8** | 3/8 | 7/21 | **5/5** |

**The direction of the review's disqualification stands** — 9/21 is ANCHOR-ARTEFACT under this
run's own pre-registered rule, and the book does not robustly meet its path's drawdown
condition. **The number it was made on does not.** The highest min-half Sharpe on the board was
passed over on a statistic belonging to a book one column wide of it.

## By-product 2 — MEAN-21 is the only robust member, and it has a new limit

B3 removes the dial instead of picking a value on it and is the corpus's only ROBUST arm:
u56 **4b PASS at 0, 5, 10 AND 25 bps** (12.84% / 1.1058 / −19.61% at 10 bps, halves
1.1737/1.0581, OOS 13.95% / 1.1280 / −19.61%, turnover 4.85×/yr) — one rung wider than idea 223
published. But this run adds the axis idea 223 did not run:

**MEAN-21 FAILS 4b on DRAWDOWN at t+5 (−20.98%) and t+7 (−21.79%), and on broad at every rung.**
Averaging the anchors buys certainty, not margin: it converts a 12-of-21 lottery into a certain
−19.61%, which is **0.62pp** inside the −20.23% cap, and one week of fill delay spends it. That
is the number a sizing decision needs, and it was not on the record before this run.

## Rule 8 (walk-forward) — the anchor is not selectable

Phase chosen on 2009–2016 IS Sharpe alone, read once on 2017–2026, 32 cells (2 books × 2 panels
× lags × 4 rungs), all reported in `.walkforward.csv`:

| comparison | mean ΔOOS Sharpe | wins |
|---|---|---|
| IS-chosen anchor − PUBLISHED phase 0 | **−0.0450** | 4/32 |
| IS-chosen anchor − anchor MEAN (MEAN21) | +0.0245 | 24/32 |
| IS-chosen anchor − anchor MEDIAN | +0.0207 | 16/32 |
| regret vs the OOS oracle | −0.0946 (worst −0.1686) | — |

The IS chooser lands on the published phase 0 in 8/32 cells; **the OOS oracle is phase 0 in
0/32**. Choosing a trade date in-sample loses 0.045 of OOS Sharpe against simply keeping the
published one and never recovers the oracle's 0.095 — this is the eleventh instance in the
record of an IS chooser losing to doing nothing (ideas 110/151/155/229). The anchor is a
**source of variance, not a dial with skill**: the only two things worth doing with it are
averaging it away (MEAN-21) or reporting the band.

OOS levels, u56 @10 bps t+1 (the numbers a sizing decision needs):

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| B1 IS-pick (ph 5) | 15.20% | 1.1602 | −20.46% |
| B1 published (ph 0) | 16.71% | 1.2866 | −19.58% |
| B2 IS-pick = published (ph 0) | 14.56% | 1.1695 | −18.81% |
| B3 MEAN-21 (no choice) | 13.95% | 1.1280 | −19.61% |
| SPY | 15.45% | 0.8820 | −33.72% |
| RULES v2 (live baseline) | 9.53% | 1.2851 | −12.05% |

## What this means for PROTOCOL

The phase control is **not** a special objection to idea 171. It is the general one: on this
project's monthly books the trade date moves full-sample MaxDD by 8–9pp and quarterly by 10pp,
against 4b margins of 0.6–1.4pp. A published monthly or quarterly MaxDD without its anchor band
is a one-draw statistic. Proposed as a reporting clause (no RULES change, no coefficient
change): **any KEEP-candidate at a cadence slower than weekly must publish its 4b pass count over
the full anchor wrap of its own cadence, and a pass rate below 19/21 is reported as
anchor-dependent rather than as a pass.** Wording in `.memo.md`.

## Caveats

* SURVIVORSHIP. `universe.json` and `universe_broad.json` are current-constituent lists (idea
  54). No level here is an attainable return; the phase-to-phase differences are same-names,
  same-days and much less exposed.
* The corpus is **3 books / 26 claims** — every monthly KEEP claim the record contains, not a
  large sample. The 92.3% is a share of the claims that exist.
* Quarterly is enumerated every 3rd bar (21 of ~63 points), and is an extension, not an audit.
* B3's 4a column is 0/16: like every growth book here it carries a worse drawdown than the live
  low-return book. Nothing in this run is proposed for RULES.
