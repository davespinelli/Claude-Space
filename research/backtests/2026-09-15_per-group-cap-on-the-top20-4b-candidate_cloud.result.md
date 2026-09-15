# RESULT — idea 897, does-a-PER-GROUP-CAP-keep-the-TOP20-4b-pass (cloud, 2026-09-15)

**ANSWERED: NO — KILL the per-group cap as a 4b-preserving constraint.** Every cap that actually
binds this book fails 4b on the CAGR floor alone, and the damage is not the diversification most
of it is de-grossing, but what is left over is a **−0.102 Sharpe** median hit against a
gross-matched uncapped parent — 20× the 0.005 that idea 879's pure gross dial moves Sharpe over
its whole 0.50→1.00 ladder. One non-binding cell (SLEEVE2 m=10) clears 4b by the letter and is the
rule-8 IS-PICK, but it loses to the do-nothing parent on **all four** OOS metrics, so it is not a
new candidate and no book is promoted. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched (rule 6).

## Gates, printed before any hypothesis was read
| Gate | Result |
|---|---|
| G1 m=20 (cannot bind) reproduces the uncapped SORTPAR | **PASS**, max&#124;dw&#124; = max&#124;dr&#124; = **0.000e+00**, both schemes |
| G2 admitted-count monotone in m, all 225 rebalance dates | **PASS** |
| G3 RANKPAR reproduces idea 879's memo triple (12.69% / 1.201 / −17.11%) | **PASS**, exact to the printed digits |

**Disclosed convention, and it is not free.** The composite is a mean of three percentile ranks,
so boundary ties are common: on **20 of 225** rebalance dates the record's published cut
(`rank(ascending=False) <= 20`, average ties) holds only **19** names. A cap must walk names in a
strict order, so this run's book uses sort-tie top-20. That choice alone is worth
**−0.050 pp CAGR and −0.0093 Sharpe** (SORTPAR 12.63% / 1.192 / −17.11% vs RANKPAR 12.69% /
1.201 / −17.11%). Any future run that re-prices this book should state which cut it used.

## H_BINDS — PASS. The cap is a real constraint
10 of 16 (scheme, m) cells with m ≤ 6 cut the book on ≥ 20% of rebalances. JSON4 m=2 holds a
median of **8** names, SLEEVE2 m=2 holds **4**. Even the uncapped parent is short of 20 names on
15.1% of dates (its own eligibility gate), which is the baseline this is measured against.

## H_KEEP — FAIL. No binding cap clears 4b
At the PROTOCOL cell (g = 0.65, 10 bps, monthly, next-day fills), full sample 2009-01-13 →
2026-09-14, against SPY 15.13% / 0.885 / −33.72% (halves 0.959 / 0.824; 4b bars: CAGR floor
10.59%, DD cap −20.23%) and RULES v2 live 8.62% / 1.201 / −12.05%:

| scheme | m | CAGR | Sharpe | MaxDD | H1 / H2 | dd | cagr | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|
| JSON4 | 2 | 5.1% | 1.127 | −6.1% | 1.067 / 1.185 | ✔ | ✗ | **FAIL** | FAIL |
| JSON4 | 5 | 9.5% | 1.081 | −14.4% | 1.146 / 1.028 | ✔ | ✗ | **FAIL** | FAIL |
| JSON4 | 6 | 10.5% | 1.092 | −15.1% | 1.161 / 1.037 | ✔ | ✗ | **FAIL** | FAIL |
| JSON4 | 8 | 12.0% | 1.173 | −16.9% | 1.214 / 1.145 | ✔ | ✔ | PASS | FAIL |
| JSON4 | 20 (parent) | 12.6% | 1.192 | −17.1% | 1.211 / 1.183 | ✔ | ✔ | PASS | FAIL |
| SLEEVE2 | 6 | 7.9% | 1.098 | −12.1% | 1.226 / 1.004 | ✔ | ✗ | **FAIL** | FAIL |
| SLEEVE2 | 10 | 12.9% | 1.227 | −17.2% | 1.293 / 1.177 | ✔ | ✔ | PASS | FAIL |

The failure is **one-legged and always the same leg**: both half-Sharpe legs and the DD cap are
**True in all 64 cells** of the grid (2 schemes × 8 caps × 2 gross × 2 cost); only the CAGR floor
ever flips. A cap cannot fail this book on risk, because capping *lowers* risk — it fails it on
return. Full grid in `.grid.csv`, binding census in `.binding.csv`.

## H_FREE — FAIL, and H_DEGROSS says why
Median CAGR give-up of a binding cap vs the uncapped parent at matched target gross: **−6.19
pp/yr** (range −2.17 to −10.81). But the binding cells hold 4–12 names at the parent's own g/20
weight, so their **realised** gross is 0.13–0.62, not 0.63. Re-running the uncapped parent at each
cell's own realised mean gross:

- CAGR: the cap gives up **+0.42 pp median** against its gross-matched twin — i.e. essentially
  **all** of the −6.19 pp is de-grossing, not selection.
- Sharpe: the cap costs **−0.102 median** (worst −0.177 at SLEEVE2 m=2), against idea 879's
  measured **0.005** span for the pure gross dial on this same book. **The cap destroys ~20× more
  Sharpe than the exposure change it is confounded with.**

So the honest statement is not "diversification is expensive" — at matched exposure it is roughly
CAGR-neutral. It is: **a per-group cap on this book is a de-grossing device that additionally
throws away a tenth of a Sharpe.** `.degross_control.csv`.

## PROTOCOL rule 8 — walk-forward, selector declared before the run, OOS read once
IS-PICK = the (scheme, m) with the highest 2009→2016 Sharpe at the PROTOCOL cell, ties to smaller
m → **SLEEVE2 m=10** (IS Sharpe 1.2173, ahead of the parent's 1.0932). OOS 2017-01-01 → 2026-09-14
read once:

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1 / H2 |
|---|---|---|---|---|
| **IS-PICK SLEEVE2 m=10** | **13.67%** | **1.2368** | **−17.17%** | 1.4133 / 1.0462 |
| SORTPAR m=20 (do-nothing) | 14.24% | 1.2675 | −17.11% | 1.4426 / 1.0800 |
| RANKPAR (record's parent) | 14.38% | 1.2814 | −17.11% | 1.4469 / 1.1039 |
| RULES v2 (live) | 9.46% | 1.2772 | −12.05% | 1.4098 / 1.1318 |
| SPY | 15.27% | 0.8740 | −33.72% | 0.9802 / 0.7593 |

The IS-PICK's OOS 4b is a **PASS** on all four legs (h1 ✔, h2 ✔, DD −17.17% vs cap −20.23%, CAGR
13.67% vs floor 10.69%). OOS 4a **FAIL**. **But the pick is dominated by doing nothing**: it is
worse than the uncapped parent on OOS CAGR (−0.57 pp), OOS Sharpe (−0.031), OOS MaxDD (−0.06 pp)
and both OOS half-Sharpes. The cap that looked best in sample is the one the OOS window charges
for. That is the whole rule-8 content of this run.

## Verdict
**KILL** the per-group cap as a way to keep the TOP20 4b pass. No new KEEP candidate, no memo
proposing adoption, no rules change. SLEEVE2 m=10 is recorded as a by-the-letter 4b pass that is
dominated by its own parent out of sample and is **not** promoted — a 4b pass that loses to doing
nothing is not a book.

## Caveats
- **SURVIVORSHIP**: `research/universe.json` is the CURRENT constituent list (idea 54). Every
  level here is optimistic and both 4b level bars are easier on this panel than on a
  point-in-time one. The cap-vs-parent comparison is same-names, same-days and is much less exposed.
- Group labels are a static present-day classification: fixed for the whole sample, so not future
  data, but not point-in-time either.
- 2020 and 2022 are the only real stress episodes in the window.
- Gross is **imported** at 0.65 (idea 879's published rung) and 0.75 (the 2026-09-04 shelf's), not
  tuned; only cap m and group scheme are tuned, and every value of both is published above.
- Rule 6: a rules change is a Sunday-review decision. This is not a proposal.
