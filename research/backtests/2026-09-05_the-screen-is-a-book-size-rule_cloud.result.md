# Idea 199 — the-screen-is-a-book-size-rule (cloud, 2026-09-05)

**VERDICT: ANSWERED, YES, and more strongly than the queue asked. KILL of the IS-window 4b
screen as an instrument — it is DOMINATED by a bare pre-registered minimum book size on every
axis that matters. `n >= 25` returns +0.1297 paired OOS Sharpe against idea 178's control
(t +12.43, 11 wins / 0 losses / 0 ties) where the screen returns +0.0287 (t +1.92, 3/0/8):
453% of the screen's edge, from a rule with no null, no SPY bars, no coefficients and no
window split. It also fires in 11 of 11 cells including the five 25-bps cells and the two
small-panel cells where the screen is structurally empty, and its picks clear the OOS-window
4b in 6 of 11 against the screen's 2.** Rules unchanged; no new book proposed; the substitute
is offered as a PROTOCOL clause for Sunday review, with its price named.

Script: `2026-09-05_the-screen-is-a-book-size-rule_cloud.py` (480 s, 11 cells, 3 workers,
1003 backtests). Outputs: `.console.txt`, `.corpus.csv`, `.picks.csv`, `.walkforward.csv`.

---

## 0. Reproduction — total, asserted before any new number was read

Idea 178's script is **imported, never re-typed**, so its panels, book constructions, 4b bar
machinery and window splits all execute their own committed code.

| gate | what | result |
|---|---|---|
| [a] | idea 178's committed `corpus.csv`, **row by row, all 1003 rows**, 11 quantities each | max abs diff **2.220e-16**, 0 `n` mismatches |
| [b] | `W_STATIC` pick (the IS-Sharpe argmax control) | **11/11 cells identical** |
| [c] | `W_4bIS[STATIC][AS165]` and `[PUB]` picks, and screen-eligible counts | **11/11 and 11/11**, eligible counts match 11/11 |

**SCOPE LIMIT, stated up front:** only the STATIC gross convention (g = 0.75) is re-run. Idea
178's CF_IS ladder is not — it found `[STATIC]` and `[CFIS]` differ in exactly one arm-cell of
22, so the comparison is unaffected, and skipping it is why this run costs 1003 backtests
instead of ~10000.

## 1. THE ANSWER — the substitute does not "capture most of" the screen's edge, it laps it

All 11 cells, paired against `S0 = W_STATIC` (the IS-Sharpe argmax, idea 178's do-nothing).
Every grid point is reported.

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | dOOS Sharpe | t | W/L/T | picks changed | fired | mean n | d\|MaxDD\| | OOS-4b clears |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 do-nothing (IS-Sharpe argmax) | 0.7515 | 13.53% | −25.76% | — | — | — | 0 | 0 | 8.5 | — | 0/11 |
| SCREEN 4bIS [AS165] | 0.7802 | 13.45% | −25.01% | **+0.0287** | +1.92 | 3/0/8 | 3 | 4 | 9.7 | −0.75pp | 2/11 |
| SCREEN 4bIS [PUB] | 0.7687 | 11.75% | −24.59% | +0.0172 | +1.18 | 3/1/7 | 4 | 4 | 13.9 | −1.16pp | 3/11 |
| SIZE n ≥ 10 | 0.8058 | 11.86% | −23.65% | +0.0543 | +2.08 | 7/1/3 | 8 | 11 | 16.2 | −2.10pp | 3/11 |
| SIZE n ≥ 15 | 0.8275 | 11.02% | −22.54% | +0.0760 | +2.92 | 9/1/1 | 10 | 11 | 20.2 | −3.21pp | 6/11 |
| SIZE n ≥ 20 | 0.8224 | 10.55% | −22.55% | +0.0708 | +2.88 | 9/1/1 | 10 | 11 | 22.7 | −3.21pp | 6/11 |
| **SIZE n ≥ 25** | **0.8812** | 10.96% | **−22.23%** | **+0.1297** | **+12.43** | **11/0/0** | 11 | 11 | 27.8 | −3.53pp | **6/11** |
| BIGGEST BOOK (no fitting at all) | 0.8435 | 8.70% | −21.78% | +0.0919 | +3.25 | 9/2/0 | 11 | 0 | 69.9 | −3.98pp | 4/11 |
| ORACLE-OOS (ceiling, not implementable) | 1.0184 | 15.36% | −21.90% | +0.2669 | +14.83 | 11/0/0 | 11 | — | 27.6 | −3.86pp | 4/11 |

Every rung of the size ladder beats both screen conventions on OOS Sharpe, on OOS drawdown,
and on OOS-4b clears. The queue's threshold ("captures most of the +0.0287") is cleared at
**k = 10**, the cheapest rung.

## 2. Where the two instruments can fire — this is the real gap

| | 10 bps cells | 25 bps cells | u56 | broad | small |
|---|---|---|---|---|---|
| SCREEN 4bIS [AS165] fires | 4 of 6 | **0 of 5** | 2 of 5 | 2 of 4 | **0 of 2** |
| SIZE n ≥ 25 fires | 6 of 6 | **5 of 5** | 5 of 5 | 4 of 4 | 2 of 2 |

Idea 178's "the screen never fires at 25 bps and is empty on the whole small panel" is
reproduced exactly. A size floor has no such boundary: it is a property of the *pool*, not of
the book's realised statistics against SPY, so it is defined wherever the pool is. **Seven of
the size floor's eleven wins come from cells the screen cannot reach at all.**

## 3. MECHANISM — the same one idea 178 found, and it is not a selection effect

Within-cell Spearman of book size `n` against the outcomes, over all 1003 books:

| corpus / panel / cost | ρ(n, OOS Sharpe) | ρ(n, OOS \|MaxDD\|) | ρ(n, IS Sharpe) |
|---|---|---|---|
| C159 broad 10 / 25 | +0.790 / +0.818 | −0.674 / −0.762 | +0.131 / +0.351 |
| C159 u56 10 / 25 | +0.745 / +0.753 | −0.592 / −0.684 | +0.186 / +0.269 |
| C165 u56 10 | +0.714 | −0.514 | +0.180 |
| C168 broad 10 / 25 | +0.544 / +0.584 | −0.591 / −0.761 | −0.097 / +0.114 |
| C168 u56 10 / 25 | +0.605 / +0.591 | −0.414 / −0.631 | +0.349 / +0.374 |
| **C159 small 10 / 25** | **−0.482 / −0.283** | **+0.530 / +0.305** | +0.119 / +0.171 |
| **mean (n = 11)** | **+0.489 (t +3.67)** | **−0.435 (t −3.31)** | +0.213 |

On the large-cap panels a bigger book is simply better out of sample and shallower in
drawdown, and `n` is nearly uninformative in sample (ρ ≈ +0.2), which is exactly why the
IS-Sharpe argmax lands on n = 4 books and gets punished. **On the small panel the sign
reverses** (ρ −0.48 / −0.28): bigger is *worse* there, and the floor's two small-panel wins
(+0.0725, +0.0783) are won against a control that picked n = 21 and n = 7, not by the
mechanism that works on the large caps. The clause is panel-conditional and is stated as such.

That `BIGGEST BOOK` — take the largest book in the pool, fit nothing, read no statistic —
already returns +0.0919 says the effect is **de-concentration, not selection**. The screen,
the floor and the biggest book are three prices for one thing.

## 4. WHAT IT COSTS — the floor buys Sharpe and drawdown with CAGR

| selector | mean OOS CAGR | cells beating SPY's OOS CAGR (15.45%) | cells beating SPY's OOS Sharpe (0.882) | cells beating RULES v1 |
|---|---|---|---|---|
| S0 do-nothing | 13.53% | **6 of 11** | 3 of 11 | 9 of 11 |
| SCREEN [AS165] | 13.45% | 5 of 11 | 4 of 11 | 9 of 11 |
| SIZE n ≥ 15 | 11.02% | 1 of 11 | 7 of 11 | 9 of 11 |
| **SIZE n ≥ 25** | 10.96% | **0 of 11** | **7 of 11** | **10 of 11** |
| BIGGEST BOOK | 8.70% | 0 of 11 | 7 of 11 | 9 of 11 |

OOS window benchmarks: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 averages 0.4849 Sharpe /
5.04% CAGR across the eleven (panel, cost) cells. The size floor takes the control from 3 to 7
cells beating SPY's *Sharpe* and from 6 to **0** cells beating SPY's *CAGR*. On the 4b path
that is a direct move toward the CAGR floor: two of the floor's four full-sample 4b failures
name `CAGR` as a failing bar (u56 25 bps: `CAGR` alone; C168 u56 25 bps: `H1|CAGR`), where the
control failed those cells on `H1|OOS|DD` and `H1|H2|OOS|DD`. **This is a risk-for-return
trade, not free money, and anyone adopting `n >= k` is choosing the 4b drawdown cap over the
4b CAGR floor.**

## 5. BOTH KEEP PATHS, on the 11 picked books (full sample, g = 0.75)

| selector | 4a passes | 4b passes | OOS-window 4b clears |
|---|---|---|---|
| S0 do-nothing | 3 | **0** | 0 |
| SCREEN [AS165] | 3 | 2 | 2 |
| SCREEN [PUB] | 4 | 3 | 3 |
| SIZE n ≥ 15 / 20 / 25 | 3 | **4** | **6** |
| BIGGEST BOOK | 4 | 3 | 4 |

Pool-wide: 302/1003 books pass 4a, 162/1003 pass 4b, 229/1003 clear the OOS window. **No new
book is proposed** — every book here belongs to ideas 159/165/168 and is already priced; what
is on trial is the selection rule.

## 6. Rule 8

Every number above **is** the walk-forward read: each pick is chosen on ≤ 2016-12-31 only and
2017-01-01 → is read once. Two tuned parameters, both reported at every grid point: the size
floor k ∈ {10, 15, 20, 25} and the screen's coefficient convention (AS165 φ=0.60 δ=0.70, PUB
φ=0.70 δ=0.60).

## 7. Predictions — 4 of 5 hit

| | prediction | outcome |
|---|---|---|
| P1 | idea 178's corpus and picks reproduce | **HIT** — 2.2e-16, 11/11, 11/11, 11/11 |
| P2 | best floor captures ≥ half the screen's edge | **HIT** — +0.1297 vs +0.0287 |
| P3 | a floor changes more picks than the screen | **HIT** — 11 vs 3 of 11 |
| P4 | the floor's changed picks reduce OOS \|MaxDD\| | **HIT** — −3.53pp mean |
| P5 | neither instrument reaches \|t\| ≥ 2 | **MISS** — the floor reaches **t +12.43** |

P5 is the run's one surprise and the reason this is not simply an eleventh "no selector beats
do-nothing". It is also the number to distrust most: see the caveats.

## 8. Caveats, carried not buried

* **k = 25 sits at the queue's grid edge** (idea 183's anchor-position caveat applies to this
  run's own headline). The ladder is not monotone — 15 (+0.0760) beats 20 (+0.0708) — and the
  unbounded extreme, `BIGGEST BOOK`, is *worse* than 25 (+0.0919 < +0.1297), so the optimum is
  bracketed between k = 25 and the pool maximum rather than running off the end. The honest
  pre-registerable read is **"k in the twenties", not "25"**.
* **t +12.43 is a paired statistic over 11 cells that share three panels, two corpora and one
  OOS window.** C159/u56/10 and C165/u56/10 are the *same book pool at the same cost* and give
  identical rows; C168 broad/u56 repeat the same two panels. The effective sample is far below
  11 and the t is not a p-value. What survives that discount is the win count (11/0/0) and the
  fact that the mechanism is visible directly in ρ(n, OOS Sharpe).
* **SURVIVORSHIP (idea 54):** all three panels are current constituents; the small panel has no
  delistings. Every selector reads the same biased panel so the *comparison* is unaffected, but
  no level here is a tradable estimate.
* `n` is derived from the share m × mean eligible names, so a floor on n is a floor on m up to
  the panel's breadth. Both are published in `.picks.csv`.
* Idea 38: calendar-day index after 2014-09-17 on u56/broad. Idea 126: t+1 only.

## 9. Proposed PROTOCOL clause, report-only, for Sunday review (evidence, not a rule change)

> **Book size is a pre-registered parameter, not a fitted one.** Any walk-forward that selects
> a book by an in-sample statistic must publish the selected book's name count `n`, and must
> report the same selector under a pre-registered floor `n >= k` for k in the twenties. On
> idea 178's eleven cells the bare floor returns +0.1297 OOS Sharpe against the unconstrained
> IS-Sharpe argmax (11/0/0) where the IS-window 4b screen returns +0.0287 (3/0/8), fires in 11
> of 11 cells against 4, and clears the OOS-window 4b in 6 against 2 — so the screen is
> redundant and should be dropped. The floor is not free: it costs 2.6pp of OOS CAGR and moves
> every cell below SPY's OOS CAGR, trading the 4b CAGR floor for the 4b drawdown cap. On the
> sub-$2B panel the size/OOS-Sharpe correlation reverses sign (−0.48, −0.28) and the clause
> does not apply.
