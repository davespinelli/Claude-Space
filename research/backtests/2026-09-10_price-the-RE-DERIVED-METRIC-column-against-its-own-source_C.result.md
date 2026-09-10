# Idea 664 (lane C, 2026-09-10) — price the RE-DERIVED METRIC column against its own source

**Verdict: ANSWERED for the record, KILL for capital. The queue's premise is FALSIFIED for the
bulk and CONFIRMED for a small, named tail. No RULES change, no book promoted, no KEEP claimed,
no PROTOCOL edit; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script: `2026-09-10_price-the-RE-DERIVED-METRIC-column-against-its-own-source_C.py`
(deterministic, standalone, no network, 111s).

---

## GATES (all pre-registered, run before any new number was read)

| | |
|---|---|
| G1 | `band_book(0.03, 0.75)` == `baseline.rules_v2_weights` at **0.000e+00**; the vectorised harness == `engine.backtest` at **6.94e-18** |
| G2 | cost-rung identity `r(25) = r(0) − turn·25/1e4` at **0.000e+00** |
| G3 | idea 661's committed `.misspairs.csv` reproduces at **3,940 pairs / 146,008 misses**, exact; today's pointer scan **260 instances / 1,099,298 rows** is a superset of 661's 250 / 1,089,229 |
| G3b | PROVENANCE — live RULES v2 U56 **8.63% / 1.2021 / −12.05% (1.2309 / 1.1798)** reproduces idea 661's same-day committed row to published precision |
| G4 | census partition exact at all 18 grid points; COPY count non-decreasing in tolerance in every family |
| G5 | all three live channels agree at their level-0 point on every (panel, gross) |

**G3b is itself a datum.** The CHANGELOG's 2026-09-08 row for the *same book under the same
rules* reads 8.66% / 1.2056 / −12.05% (1.2259 / 1.1909). Two extra trading days of price cache
move it by **dSharpe 0.0035, dCAGR 0.03 pp, dH1 0.0050, dH2 0.0111**. The record already contains
window-difference recomputation; the gate was re-anchored on the same-day artefact and the gap is
reported, not hidden.

---

## THE POPULATION

260 pointer instances over 249 files, 1,099,298 pointer rows. Restricted to (child, metric
column, source) pairs: **1,399,337 metric VALUE reads over 2,515 pairs, 14 child files, 248
sources, 18 distinct metric columns.**

`d = min_s |child − s|` — the nearest-neighbour gap of the child's printed number against the
source's own column. **Deliberately permissive: it ignores row alignment**, so it is an UPPER
bound on how much of the record copies rather than recomputes.

## PART A — the answer: it is a PRINTING difference, not a window and not a book

| family @ rung | N | COPY | ROUND | UNIT | WINDOW | BOOK |
|---|---|---|---|---|---|---|
| M3_ALL @ EXACT | 1,399,337 | 0.4375 | **0.5415** | 0.0000 | 0.0197 | 0.0012 |
| M3_ALL @ 1e-06 | 1,399,337 | **0.9773** | 0.0021 | 0.0000 | 0.0193 | 0.0012 |
| M3_ALL @ 5e-02 | 1,399,337 | **0.9989** | 0.0000 | 0.0000 | 0.0000 | 0.0010 |
| M1_CORE @ EXACT | 292,278 | 0.4948 | 0.5042 | 0.0000 | 0.0010 | 0.0000 |
| M1_CORE @ 1e-02 | 292,278 | **1.0000** | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

Only **43.75%** of metric reads are bitwise copies, so the queue is right that the record
*re-derives*. But **97.73% are COPY at a 1e-6 rung** and the entire remaining ROUND block sits
under half of the child's own last printed digit: the record prints fewer decimals than its
source. **M1_CORE {CAGR, Sharpe, MaxDD} is 100% COPY at 1e-2 with zero BOOK-class reads at any
rung.**

This does **not** contradict idea 661's "97.63% of misses survive the widest tolerance". 661
measured *key-join* misses, whose dominant mechanism is label vocabulary (`family`, `dial`,
`panel` = 58.8%). 664 measures the *values*. **The record's join failure is a row-addressing
failure, not a numeric one** — the numbers are there, the rows cannot be found.

## PART B — the tolerance-proof residual is real, small, and has one address

**1,508 reads (0.11%) are still not a COPY at 5e-2** — 49 WINDOW + 1,459 BOOK. Per column:

| col | N | COPY | ROUND | WINDOW | BOOK | d_max | survives 5e-2 |
|---|---|---|---|---|---|---|---|
| **regret** | 9,948 | 0.2956 | 0.2159 | **0.3178** | **0.1707** | **0.7451** | **1,442** |
| m_H1 | 118,300 | 0.3863 | 0.5456 | 0.0680 | 0.0001 | 0.3514 | 41 |
| m_H2 | 118,300 | 0.3968 | 0.5351 | 0.0680 | 0.0001 | 0.3314 | 25 |
| m_CAGR | 118,300 | 0.0626 | 0.8693 | 0.0679 | 0.0001 | 0.0227 | 0 |
| OOS_Sharpe | 124,634 | 0.7958 | 0.2042 | 0.0000 | 0.0000 | 0.0000 | 0 |
| the other 12 columns (OOS_CAGR, OOS_MaxDD, IS_CAGR, IS_MaxDD, IS_Sharpe, CAGR, MaxDD, H1, H2, Calmar, sharpe, Sharpe) | 909,854 | — | — | ≤0.0017 | 0.0000 | ≤0.0050 | 0 |
| d_OOS_Sharpe | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0001 | 0 |

**95.6% of the tolerance-proof residual is the single column `regret`**, 1,675 of whose reads
exceed the live between-book bar. One published file
(`2026-09-08_make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN_cloud.cells.csv`, which
*proposed the metric*) carries 1,675 of the record's 1,727 BOOK-class reads.

A fourth mechanism the queue does not name, and which no tolerance rung can ever recover:
**23 UNIT reads** — the child prints `12.66` where the source printed `0.1266`.

## PART C — the yardsticks, re-derived live (so the bars are measured, not asserted)

Pooled median |Δmetric| on U56 + B136, RULES v2 book:

| metric | WINDOW bar (same book, different window) | BOOK bar (different band book, same window) |
|---|---|---|
| Sharpe | **0.0355** (p90 0.098–0.137) | 0.0235 |
| CAGR | 0.0044 | 0.0047 |
| MaxDD | 0.0095 | 0.0163 |
| H1 / H2 | 0.1267 / 0.0898 | 0.0257 / 0.0422 |
| Calmar | 0.0737 | 0.0302 |

**Moving the measurement window moves Sharpe, H1, H2, Calmar and Sortino MORE than changing the
band book does.** In this record a window difference is a bigger perturbation than a different
book — which is why WINDOW is the class that matters and why the live leg below prices it the
same way.

## PART D — exposure

**13 of 13** child files with a non-COPY metric read ship a committed `.result.md` **and** are
cited by LEADERBOARD / CHANGELOG / QUEUE. **787,101 non-COPY reads rest under published claims**
— but 785,593 of those are the harmless printing block. **5 files carry a BOOK-class read
(1,727 reads)**, and the exposure that matters is the `regret` column above.

## PART E — priced live: a chooser that MISREADS its own metric

90 grid points, all reported. Candidates = band books b ∈ {0, .01, .02, .03, .05, .08, .12, .20};
the chooser picks argmax IS Sharpe and the pick is deployed. Three channels, meeting exactly at
their level-0 point (G5): **ROUND** (read to dp decimals), **WINDOW** (read on a different
window), **BOOK** (read off a neighbour band). Ties broken by smallest band — stated, outcome-blind.

| channel | picks flipped | worst Δ OOS Sharpe | worst Δ OOS MaxDD | worst Δ OOS CAGR |
|---|---|---|---|---|
| ROUND | 12/30 | **+0.0000** | +0.00 pp | −0.66 pp |
| BOOK | 12/30 | −0.0187 | −0.00 pp | −0.55 pp |
| **WINDOW** | **18/24** | **−0.0981** | **−1.26 pp** | −0.18 pp |
| POOLED | 42/84 (0.500) | −0.0981 | | |

**Half of all picks flip and rounding costs nothing.** Reading a metric to zero decimals flips
12 of 30 picks and never costs OOS Sharpe. Reading it on the wrong window flips 18 of 24 and
costs up to **−0.0981 Sharpe and −1.26 pp of drawdown**. The live ordering
(WINDOW ≫ BOOK ≫ ROUND ≈ 0) reproduces the census ordering of the bars — and the record's
dominant class (ROUND, 54%) is the free one.

### Rule 8 (fitted on 2009–2016, scored 2017–2026 untouched)

28 honest points (look-ahead `FULL` windows flagged and excluded):
**beat SPY OOS Sharpe 28/28, beat the LIVE BOOK 2/28, 4a 0/28, 4b 25/28.**
U56 OOS: picks 1.1267–1.2560 Sharpe vs SPY 0.8758 vs live RULES v2 **1.2788**.
B136 OOS: picks 1.0112–1.1244 vs SPY 0.8820 vs live RULES v2 **1.1185**.

### NOT PROMOTED

Full sample: **4a 0/90, 4b 27/90, BOTH 0/90.** All 27 4b passes sit at **g = 1.00**, with
**0 at g = 0.75 and 0 at g = 0.50**, while Sharpe is flat in gross to three decimals
(1.0377…1.2022 / 1.0378…1.2021 / 1.0378…1.2020). The entire 4b footprint is the CAGR floor
moving with gross — **idea 311's loophole and open idea 657's question, for the fourth time.**

---

## LIMITATIONS, STATED

- The nearest-neighbour match ignores row alignment: it is an **upper bound** on copying.
- The record does not carry the weights function behind most rows, so "re-derive from the
  source's own book" means (a) the source's own column for the census and (b) live books this
  script rebuilds for the three mechanism bars. Two committed rows are rebuilt exactly (G3b).
- B136 is **survivorship-biased** (current constituents only, PROTOCOL 9).
- `regret` is not a PROTOCOL metric; it is included only under M3_ALL, and M1_CORE/M2_SHAPE are
  reported separately precisely so the headline does not rest on it.

## FOLLOW-UPS FILED

666, 667, 668 (see QUEUE.md).
