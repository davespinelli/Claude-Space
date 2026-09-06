# Idea 304 — does-the-EXPOSURE-vs-TIMING-split-price-the-live-de-gross-clause-correctly

**Lane C, 2026-09-06.** Script `2026-09-06_does-the-EXPOSURE-vs-TIMING-split-price-the-live-de-gross-clause-correctly_C.py`
· grid `.grid.csv` (442 rows) · matched `.matched.csv` (18 rows) · walk-forward `.walkforward.csv` · console `.console.txt`

## Verdict: **ANSWERED / KILL of the mispricing hypothesis. The live de-gross clause is priced correctly. No RULES change.**

Idea 297 priced RULES v2's de-gross clause at 3.6 pp of CAGR for 5.7 pp of drawdown and found
**96% of the CAGR gap is pure cash drag**, only -0.155 pp/yr timing. The natural inference — that
a *constant* cash allocation would buy the same risk more cheaply — is **wrong**. At the live
book's own drawdown the static-gross twin is worse on every clause the queue named.

## B0 reproduction gate (asserted before any new number)

| clause | result | bar |
|---|---|---|
| (i) `DEGROSS(0.03,0.75)` vs `baseline.rules_v2_weights`, max abs weight diff | **0.000e+00** | < 1e-12 |
| (ii) live row vs idea 297's published 8.66% / 1.2056 / -12.05% | 4.942e-05 | < 5e-4 |
| (iii) RESPREAD twin vs published 12.25% / -17.71% | 4.790e-05 | < 5e-4 |
| (iv) `c_bar = mean(held_DG/held_RS)` vs published 0.7101 | 5.002e-06 | < 1e-3 |

**Pre-registration deviation, logged.** The script first used idea 297's stricter live mask
`px.notna() & px.shift(1).notna()`; under it clause (i) is **2.941e-04 and FAILS** the 1e-12 bar
(early days only; metrics still reproduced to 1.3e-04). The fix adopted is the LIVE book's own
denominator, `N = instruments priced that day` — which makes the identity exact. Also noted:
`universe.json` lists **SPY as an instrument** and the live book holds it, so all three arms keep
it as a constituent; dropping it moves the live book to 8.68% / 1.2128 / -11.90% and would not
reproduce 297.

## H1 EXISTENCE — **PASS**

MaxDD is weakly monotone in gross on **26/26 arms, 0 violations**, so the bisection is well posed.
On U56 at the live band the RESPREAD twin matches the live **-12.0549%** drawdown at
**g\* = 0.5002** (err -2.2e-08, no leverage).

## H2 THE CAPITAL CLAIM — **FAIL on all three clauses**

| U56, b=0.03, matched MaxDD | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| **live DEGROSS (g=0.75)** | **8.66%** | **1.2056** | -12.05% | **1.2259 / 1.1908** |
| RESPREAD, static g\*=0.5002 | 8.14% | 1.1608 | -12.05% | 1.2097 / 1.1288 |
| EWALL (no gate), static g\*=0.3849 | 6.77% | 1.1229 | -12.05% | 1.1875 / 1.0719 |

dCAGR **-0.52 pp/yr**, dSharpe **-0.0448**, and the live book wins **both** halves. Buying the live
book's drawdown with constant cash instead of the dynamic clause costs return *and* Sharpe.

**Robustness — the sign is not a band or panel artefact.** Across all 12 matched (panel × band)
RESPREAD cells, dCAGR is negative **12/12** (U56 -0.26 .. -1.39 pp/yr, B136 -0.46 .. -1.17) and
dSharpe negative 9/12. Under the second matching target (annualised vol, not drawdown) the sign
is unchanged: U56 dCAGR -0.35 / dSharpe -0.0448, B136 -0.29 / -0.0373.

## H3 DOES THE GATE EARN ANYTHING — yes, and more than the de-grossing does

At matched -12.05% the three-way ordering decomposes the live book's return **at constant risk**:

    EWALL @ g*=0.385    6.77%   <- pure static exposure, no gate
    + the 200d band     +1.37 pp/yr   (RESPREAD @ g*=0.500 = 8.14%)
    + dynamic de-gross  +0.52 pp/yr   (live DEGROSS @ 0.75  = 8.66%)

So idea 297's "96% of the gap is drag" is an **accounting share, not a verdict**: the drag is not
free, because removing it and re-matching risk statically gives back less than it saves. The
ungated control is 4a=False and 1.89 pp/yr behind the live book at identical drawdown.

## H4 WALK-FORWARD (rule 8) — the live book is not beaten out of sample either

Both dials re-chosen on 2009-2016 only (band by IS Sharpe, gross by matching the live book's IS
MaxDD of -7.89%); 2017-2026 read once.

| panel | arm | band / g\* picked IS | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| U56 | **live-form ref (b=0.03, g=0.75)** | — | **9.53%** | **1.2851** | **-12.05%** |
| U56 | RESPREAD | 0.12 / 0.5023 | 10.07% | 1.2665 | -13.31% |
| U56 | DEGROSS | 0.08 / 0.6977 | 8.42% | 1.1728 | -13.49% |
| U56 | EWALL | — / 0.4617 | 8.47% | 1.1359 | -14.33% |
| B136 | live-form ref | — | 7.98% | 1.1185 | -12.24% |
| B136 | RESPREAD | 0.12 / 0.4867 | 8.88% | **1.1632** | -14.50% |
| B136 | EWALL | — / 0.3746 | 6.93% | 1.1039 | -13.32% |
| SPY | — | — | 15.45% | 0.8820 | -33.72% |

On U56 the live book beats **all three** re-selected matched-risk alternatives on OOS Sharpe. On
B136 the RESPREAD pick edges the transplanted live form on Sharpe (1.1632 vs 1.1185) but only by
carrying 2.3 pp more drawdown than the IS match promised — i.e. the static match does not hold
its risk out of sample, which is the one thing it was supposed to buy. Every arm beats SPY on OOS
Sharpe; **none clears 4b**, all failing the CAGR floor (0.70 × SPY's 15.23% = 10.66%).

## KEEP paths

**4a 11/442, 4b 54/442 — no KEEP.** All 11 4a passers are the same arm: U56/B136 RESPREAD at
b=0.12 and gross 0.20-0.45, CAGR **3.6-8.3%**. They pass 4a only because its drawdown clause
rewards holding less, and every one fails 4b on CAGR — the exact failure mode 4b was added to
catch. The 4b binding-bar census over all 442 points is **CAGR 317, DD 71, pass 54**; the live
book itself fails 4b on CAGR. (The 54 4b passers are the already-published high-gross corner of
the DEGROSS/RESPREAD families, e.g. live-form at g=0.95: 11.00% / 1.2055 / -15.15%, OOS 1.2845 —
a gross dial on the incumbent, not a new rule.)

## What this means for the record

Idea 297's exposure/timing split **describes** the live clause correctly but does **not** price it.
The 96% drag share invited the reading "the clause is 96% dead weight"; at matched risk that
reading is false by -0.52 pp/yr of CAGR and -0.0448 of Sharpe on the live panel, 12/12 in sign
across bands and panels, under two independent matching targets, and it does not reverse out of
sample. Any future claim of the form "X% of a de-gross book's cost is cash drag" should be
re-quoted with its matched-risk head-to-head before it is read as a verdict.

**SURVIVORSHIP:** both panels are today's constituents; no delistings. The H2/H3 headline is an
arm-minus-arm contrast on the same names and days at matched realised risk, so the bias very
largely cancels out of it; it does not cancel out of the 4a/4b columns, which are levels.
