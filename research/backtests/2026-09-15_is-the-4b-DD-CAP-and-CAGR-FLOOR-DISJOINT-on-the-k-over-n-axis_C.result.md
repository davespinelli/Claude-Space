# Idea 887 — is the 4b DD CAP and CAGR FLOOR disjoint on the k/n axis, generally?

**ANSWERED: NO — they are NOT disjoint in general; 769's zero-overlap is a CONSTRUCTION-and-GROSS
artefact, not a k/n fact. But the overlap is worth nothing as capital: it lives at the far END of
the k/n axis, where the dial is effectively off, and the zero-signal RAND family reaches it as
often as the ranking families. KILL for capital; one 4b KEEP-candidate memo'd and DECLINED.**

No RULES change, no PROTOCOL change, nothing promoted. `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched (rule 6).

**SELECTION.** Claimed as the second `## Open` idea **carrying a price leg**: 888 and 884 sit above
it with standing lane-C / cloud SKIP notes (both re-score committed prose and have no book to
price), and 886 is annotated in QUEUE.md this run for the same reason.

---

## Design

**2 tuned parameters, the queue's own: FAMILY x k/n (q).** Everything else is a reported axis.

| axis | values |
|---|---|
| panel | U56 (55 names) / B136 (135) / SMALL (663, current constituents, `max_1d_move` >= 1.0 dropped) |
| family (tuned) | MOM (12-1 + 6m + 3m rank composite, no vol scaler) / MADIST (px/ma200 - 1) / VOLLO (-vol20) / VOLHI (+vol20) / **RAND (md5-free fixed-seed uniform — the zero-signal control)** |
| k/n = q (tuned) | 0.05 0.10 0.15 0.20 0.30 0.40 0.50 0.70 0.90 1.00 |
| construction | **RESPREAD** (each of k gets gross/k -> book always at full gross) / **DEGROSS** (each of k gets gross/n_elig -> exposure = gross·k/n_elig, rest to CASH) |
| gross | 0.75 / 0.95 / 1.00 |
| cadence | W / M |
| cost rung | 0 / 10 / 25 bps (headline 10, PROTOCOL rule 2) |

Eligibility is the record's standing admission — priced, above its 200d MA — intersected with
"carries a finite ranking statistic that day", so `k/n` is a fraction of the **rankable** set and
`q = 1.00` makes the two constructions identical by construction (G3).

**1,710 books** (q=1.00 DEGROSS is dropped as identical to RESPREAD) **x 3 cost rungs = 5,130
book-rows**, every one published in `.books.csv`. Next-day execution, drift between rebalances.

## Gates — 7 of 7 PASS, printed before any hypothesis was read

| gate | value | bar |
|---|---|---|
| G0 `fast_run` vs `engine.backtest` returns (MOM q0.30 RESPREAD g0.75 W) | 5.109e-16 | < 1e-12 |
| G1 `fast_run` vs `engine.backtest` turnover | 6.106e-16 | < 1e-12 |
| G2 `fast_run` vs `engine.backtest` on the LIVE book (RULES v2) | 4.267e-16 | < 1e-12 |
| G3 q=1.00 RESPREAD == DEGROSS elementwise | 0.000e+00 | < 1e-12 |
| G4 RESPREAD exposure is exactly `gross` on rankable-eligible days | 8.882e-16 | < 1e-12 |
| G5 DEGROSS exposure == gross·k/n_elig | 8.327e-17 | < 1e-12 |
| G6 the 10/25 bps rungs are derivable from the 0 bps path | 0.000e+00 | < 1e-12 |

G0 excludes the **2 warm-up days on which `engine.backtest` itself returns NaN** (its `w_target` is
`shift(1)`ed, so row 0 and the first rebalance's turnover are NaN); both sit ~250 trading days
before the evaluation start and are inside every published book's warm-up.

## Comparands (10 bps, weekly, each panel's own window)

| panel | SPY full | SPY halves | SPY OOS | RULES v2 (live) full | RULES v2 OOS |
|---|---|---|---|---|---|
| U56 | 15.13% / 0.885 / −33.72% | 0.959 / 0.824 | 15.27% / 0.874 / −33.72% | 8.62% / 1.201 / −12.05% | 9.46% / 1.277 / −12.05% |
| B136 | 15.16% / 0.886 / −33.72% | 0.960 / 0.826 | 15.33% / 0.877 / −33.72% | 7.98% / 1.099 / −12.24% | 7.88% / 1.106 / −12.24% |
| SMALL | 14.06% / 0.858 / −33.72% | 0.914 / 0.834 | 15.33% / 0.877 / −33.72% | 4.30% / 0.664 / −13.89% | 3.75% / 0.560 / −13.89% |

4b bars on U56: CAGR floor **10.59%**, DD cap **−20.23%**. (`prices.csv` is re-downloaded daily with
auto-adjusted closes, so the U56 comparands reproduce the record's 8.64% / 1.208 / −11.90% to
~1e-3, not bit-exactly — the known limit named in idea 406's entry.)

---

## 1. THE ANSWER — NO, NOT DISJOINT; BUT THE OVERLAP IS AT THE END OF THE AXIS

At 10 bps, over 1,710 books: DD leg **762**, CAGR leg **686**, **BOTH LEVEL LEGS 57**, full 4b
**57**, 4a **24**. 769's own decomposition restated on this grid: fails on DD alone **629**, on
CAGR alone **705**, on both **319**.

Of the **180 slices** (panel x family x constr x gross x cadence), **43 contain a q at which both
level legs hold**. So the answer to the idea as asked is **NO: the two legs are not generally
disjoint on the k/n axis** — 769's `BOTH 0/720` is a property of its own grid (gross pinned at
0.75, one ranking statistic, the FIXK arm pair), not of the bar.

**But 53 of the 57 both-level books sit at q >= 0.7 and 2 at q <= 0.3, median q 0.90, on an axis
that runs 0.05..1.00.** The counts by construction x q are monotone in exactly the way that says
the overlap is an axis-endpoint object, not an interior window:

| q | DEGROSS BOTH | RESPREAD BOTH |
|---|---|---|
| 0.05–0.40 | 0, 0, 0, 0, 0, 0 | 0, 0, 1, 0, 1, 0 |
| 0.50 | 2 | 0 |
| 0.70 | 12 | 3 |
| 0.90 | 13 | 10 |
| 1.00 | (== RESPREAD) | 15 |

## 2. WHY — THE TWO LEGS ARE ONE DIAL READ FROM OPPOSITE ENDS, AND THE CONSTRUCTION SETS THE SIGN

Spearman of each leg's statistic on q, median over slices (MaxDD is negative, so rho_MaxDD > 0
means the drawdown SHRINKS as the book widens):

| constr | gross | rho(q, CAGR) | rho(q, MaxDD) | rho(q, Sharpe) |
|---|---|---|---|---|
| DEGROSS | 0.75 / 0.95 / 1.00 | **+1.000** | **−1.000** | +0.583 |
| RESPREAD | 0.75 | −0.970 | +0.921 | +0.558 |
| RESPREAD | 0.95 / 1.00 | −0.964 | +0.921 | +0.503 |

**DEGROSS: 0 of 90 slices have the two legs agreeing in sign — the anti-monotonicity is exact.**
That is forced, and G5 proves it: under DEGROSS the book's exposure *is* `gross·k/n`, so k/n is
the exposure dial and widening buys CAGR while paying drawdown, one for one. RESPREAD runs the
same conflict with the sign flipped (k/n is pure concentration at fixed gross, so *narrowing*
buys CAGR and pays drawdown); it agrees in sign in 29 of 90 slices, which is where the overlap
comes from.

So the honest restatement of 769's finding is not "the legs are disjoint on k/n" but **"k/n is a
one-dimensional dial and 4b's two level legs are read from its two ends"** — the same shape lane B
found on the gross dial in idea 879, arriving here on a completely different axis. The two legs can
only be satisfied together where the dial is near a stop, i.e. where k/n has stopped doing
anything. Median q-gap where both legs are reachable but disjoint: **0.300 (RESPREAD), 0.200
(DEGROSS)**.

## 3. THE ZERO-SIGNAL CONTROL — the overlap belongs to the BASE BOOK, not to any family

Every family against **RAND at the same (panel, q, constr, gross, cadence)**, 342 matched pairs
each, 10 bps:

| family | win Sharpe | win CAGR | win MaxDD | median dSharpe | median dCAGR | 4b passes | RAND's 4b at the same cells |
|---|---|---|---|---|---|---|---|
| MOM | 0.9211 | 0.9825 | 0.3187 | +0.1731 | +0.0266 | 11 | 12 |
| MADIST | 0.8918 | 0.9474 | 0.4737 | +0.2253 | +0.0265 | **15** | 12 |
| VOLLO | 0.5877 | 0.1550 | 0.9123 | +0.0763 | −0.0095 | 8 | 12 |
| VOLHI | 0.7807 | 0.9474 | 0.2018 | +0.1147 | +0.0275 | 11 | 12 |

The ranking families beat the coin flip on Sharpe (win rates 0.59–0.92, median +0.08 to +0.23) —
**and it buys them no 4b passes at all**: RAND clears 4b **12 of 342**, more often than MOM, VOLHI
and VOLLO and only three fewer than MADIST. The reason is visible in one cell: at **U56 RESPREAD
g0.75 M q=1.00 all five families read the identical 12.53% / 1.1536 / −18.23%**, because at q=1.00
every family holds every eligible name. That cell passes 4b, and the zero-signal selector picked
it. What clears the bar is the base book — equal-weight every name above its 200d MA at gross
0.75 — which is the RECOMMENDATION memo's Finding 2 and the family of the record's own
2026-09-04 KEEP 4b. The k/n dial and the ranking statistic are both decoration on it.

SMALL contributes **0 both-level books and 0 4b passes** out of 570; its 18 4a passes are all
de-grossed MADIST/MOM books. B136 15 and U56 42 of the 57.

## 4. RULE 8 — parameters chosen on 2009–2016 only, OOS 2017–2026 read once

Four selectors, all pre-registered, all IS-only, run over the (FAMILY x q) plane inside each
(panel, constr, gross, cadence) slice; 36 slices each:

| selector | OOS 4b | OOS legs DD / CAGR / Sharpe | beats SPY OOS Sharpe | beats LIVE | median OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| SEL-SHARPE (argmax IS Sharpe) | **0 / 36** | 18 / 12 / 6 | 6 | **0** | **3.36%** / 0.772 / −18.22% |
| SEL-DDCAP (769's: argmax IS CAGR s.t. IS MaxDD <= 0.60x SPY IS) | 5 / 36 | 5 / 21 / 22 | 22 | 2 | 12.09% / 0.980 / −23.86% |
| SEL-NULL (seeded uniform pick — control) | 2 / 36 | 16 / 13 / 17 | 17 | **7** | 8.84% / 0.779 / −23.72% |
| SEL-4bIS (oracle: argmax IS Sharpe among IS-4b cells; idea 712) | 4 / 26 (10 empty) | 5 / 18 / 18 | 18 | 0 | 13.70% / 1.051 / −23.58% |

Three readings, none of them flattering:

1. **The honest selector never reaches the bar.** SEL-SHARPE clears 4b **0 of 36** out of sample
   and its median OOS CAGR is **3.36%** — 769's "all three IS-only DD-capped selectors landed on
   2–4% CAGR books" reproduces here on the *Sharpe* selector across five families and three panels.
2. **The DD-capped selector's 5 passes do not belong to it.** All 5 sit at q >= 0.7, and RAND
   passes 4b at **3 of those same 5 cells**. SEL-NULL's own 4b pass is the family-invariant
   U56 RESPREAD g0.75 M q=1.00 cell, where the five families are numerically identical.
3. **The null selector beats the live book out of sample more often than any signal selector
   does** (7 of 36, against SEL-DDCAP's 2 and SEL-SHARPE's and the oracle's 0). Not one of the 144
   picks beats RULES v2's OOS Sharpe by more than noise; the live book's 1.277 is above every
   selector's median.

## 5. COST RUNGS (whole grid)

| rung | DD leg | CAGR leg | BOTH LEVEL | 4b | 4a | BOTH-LEVEL RESPREAD / DEGROSS |
|---|---|---|---|---|---|---|
| 0 bps | 782 | 820 | 92 | 89 | 82 | 46 / 46 |
| 10 bps | 762 | 686 | **57** | **57** | 24 | 30 / 27 |
| 25 bps | 704 | 563 | 24 | 24 | 9 | 12 / 12 |

At 10 and 25 bps `BOTH LEVEL == 4b` exactly: **once both level legs hold, the three Sharpe legs
never bind.** The whole 4b verdict on this grid is the two level legs, i.e. one dial read twice.

## 6. THE 4b KEEP-CANDIDATE — memo'd and DECLINED

One book is both a full 4b pass and rule-8 reachable (SEL-DDCAP picks it on 2009–2016 alone, at
two cadences and two grosses). **U56, MOM q=0.90, DEGROSS, gross 0.75, monthly**, 10 bps:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS | turnover |
|---|---|---|---|---|---|---|
| candidate | 12.14% | 1.1820 | −17.77% | 1.2650 / 1.1219 | 12.92% / 1.1931 / −17.77% | 3.28x/yr |
| **its RAND twin, same cell** | 11.44% | 1.1696 | −16.47% | 1.2528 / 1.1069 | 12.05% / 1.1777 / −16.47% | 4.27x/yr |
| SPY | 15.13% | 0.885 | −33.72% | 0.959 / 0.824 | 15.27% / 0.874 / −33.72% | — |
| RULES v2 (live) | 8.62% | 1.201 | −12.05% | 1.232 / 1.177 | 9.46% / 1.277 / −12.05% | — |

It clears 4b on every leg (CAGR 12.14% >= 10.59%; MaxDD −17.77% >= −20.23%; Sharpe above SPY in
both halves and OOS) and it holds at 0 and 25 bps (1.2142 / 1.1333).
**It is DECLINED, on three grounds stated before any of this was read as a recommendation:**

- **The gate earns +0.0124 of Sharpe over a coin flip at the same cell**, and pays 1.30 pp of extra
  drawdown for +0.70 pp of CAGR. The zero-signal twin passes 4b too. The pass belongs to the base
  book (equal-weight eligible, gross 0.75) and to the 0.75 rung, which the record already holds.
- **It loses to the live book on Sharpe everywhere** — 1.182 vs 1.201 full, 1.1931 vs 1.277 OOS,
  and −17.77% against −12.05% of drawdown. 4a is **0 of 1,710** on U56.
- Rule 6 forbids applying a rules change outside the Sunday review in any case.

### Exact RULES wording, if a Sunday review ever wanted it (NOT proposed)

> **RULES v3 clause 2 (k/n book).** Each month, on the last trading day, rank every instrument that
> is priced, above its 200-day moving average, and carries a full 12-month return history, by the
> equal-weight average of its percentile ranks of (12-1 month, 6-month, 3-month) return. Hold the
> top `k = round(0.90 x n_eligible)` of them, each at `0.75 / n_eligible` of NAV; the remainder of
> NAV is CASH and is never re-spread. Orders are placed at the next day's close. The daily hard
> exit below the 200-day average stays.

## Survivorship and other caveats

U56 / B136 / SMALL are **current-constituent** lists (SMALL additionally drops the 52 tickers with
`max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown **level** above is
optimistic — the candidate's, the base book's and the comparands' alike. The run's headline is a
**within-cell** comparison (family vs its own RAND twin on the same panel, same q, same tape) and a
**sign** statement about the k/n axis, both of which are protected against the bias; the 4b/4a
counts and the rule-8 levels are NOT. Only 2020 and 2022 are real stress tests in this window.
`RAND` is `np.random.default_rng(887)` over a fixed panel shape — deterministic, but it is ONE
draw, so its 12 4b passes carry a per-cell sampling error this run did not bound.

## Files

`.py` (the run) · `.books.csv` (5,130 rows, every grid point) · `.legs.csv` (180 slices, the q-sets)
· `.walkforward.csv` (144 rule-8 picks) · `.gates.csv` · `.console.txt`

## Follow-ups filed

906 (is `BOTH LEVEL == 4b` at 10/25 bps a record-wide fact — are the Sharpe legs ever binding?),
907 (bound RAND's 4b pass rate with a real draw budget, not one seed), 908 (does a k/n dial exist
on ANY axis where the two 4b level legs co-move?).
