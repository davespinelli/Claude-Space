# Idea 317 — do the record's conditional clauses ever beat their own unconditional parents? (cloud, 2026-09-09)

**Verdict: ALMOST NEVER, and the bar earns its place in PROTOCOL rule 4.** Idea 48's 4/16 was
optimistic by an order of magnitude: over **720 conditional books on 3 panels the full-sample rate is
2/720 = 0.3%, and out of sample it is 0/720**. The decisive finding is the cross-tab: **every one of the
36 books in this menu that PASSES 4b fails the parents bar, and all 36 fail it on CAGR** — each is
strictly out-returned by one of the two rules it interpolates.

## Scope, honestly stated
The LEADERBOARD's conditional rows are prose, not runnable objects, so this run does **not** claim to
re-execute them. It rebuilds the record's recurring conditional FORM — *hold book A while a market
state is ON, hold book B while it is OFF* — as a pre-registered menu spanning the clause families the
record actually uses, and runs every member against its own two parents at matched gross. That is a
larger and fully reproducible sample than the prose rows, under idea 48's unchanged bar.

- **Forms (the parents, each a complete book at the same gross 0.75):** EWALL, TOP10, TOP20, MADG
  (the live RULES v2 form), LOWVOL20, CASH.
- **States (decided at close t; every quantile is an EXPANDING quantile, min_periods=252 — no
  look-ahead):** TREND (SPY > 200d MA), MOM12 (SPY 12m return > 0), BREADTH@q, CALM@q for
  q ∈ {0.30, 0.50, 0.70}.
- **30 ordered pairs × 8 states = 240 conditional books per panel**, on **U56 / B136 / SMALL439**, plus
  18 parents. 10 bps, weekly, next-day execution, no shorting, no leverage, gross 0.75 everywhere so
  no comparison here is a gross comparison.
- **SMALL439 survivorship caveat:** the small panel is current constituents of the sub-$2B screen only
  (the 44 tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` are dropped first), so its levels
  are optimistic. The parents test is a *within-panel* comparison — conditional vs its own two parents
  on the same names — which survivorship bias does not manufacture.
- **Gate G1:** `fast_backtest` reproduces `engine.backtest` on RULES v2 / U56 to **6.939e-18**.

## The bar (idea 48's, unchanged): C must beat BOTH parents

| window | CAGR | Sharpe | MaxDD | **ALL3** |
|---|---|---|---|---|
| FULL | 30/720 = 4.2% | 45/720 = 6.2% | 59/720 = 8.2% | **2/720 = 0.3%** |
| IS (2010–2016) | 51/720 = 7.1% | 82/720 = 11.4% | 59/720 = 8.2% | **2/720 = 0.3%** |
| OOS (2017–2026) | 57/720 = 7.9% | 80/720 = 11.1% | 63/720 = 8.8% | **0/720 = 0.0%** |
| halves | H1 71/720 = 9.9% | H2 78/720 = 10.8% | both halves 11/720 = 1.5% | — |

By panel (n=240 each), FULL ALL3: **U56 0/240, B136 0/240, SMALL439 2/240**. Transport: of the 2
full-sample ALL3 passers, **0 pass ALL3 out of sample**; of the 2 IS passers, **0 pass OOS**.

Idea 48's second claim — *0/16 on drawdown* — does **not** generalise. Drawdown is the leg conditional
books beat most often (8.2% full-sample), ahead of Sharpe (6.2%) and CAGR (4.2%). The clause family
buys drawdown; what it cannot do is buy drawdown **and** keep the return.

## Reporting axes (never selected on)

| state | n | ON | FULL CAGR | Sharpe | MaxDD | ALL3 | OOS ALL3 |
|---|---|---|---|---|---|---|---|
| BREADTH30 | 90 | 80.7% | 3.3% | 11.1% | 7.8% | 0.0% | 0.0% |
| BREADTH50 | 90 | 57.4% | 4.4% | 6.7% | 7.8% | 0.0% | 0.0% |
| BREADTH70 | 90 | 28.7% | 1.1% | 0.0% | 6.7% | 0.0% | 0.0% |
| CALM30 | 90 | 38.6% | 1.1% | 3.3% | 11.1% | 0.0% | 0.0% |
| CALM50 | 90 | 58.2% | 3.3% | 6.7% | 10.0% | 0.0% | 0.0% |
| CALM70 | 90 | 74.8% | 5.6% | 8.9% | 11.1%\* | 1.1% | 0.0% |
| MOM12 | 90 | 87.6% | 7.8% | 6.7% | 5.6% | 0.0% | 0.0% |
| TREND | 90 | 83.5% | 6.7% | 6.7% | 7.8% | 1.1% | 0.0% |

\*8.9% as printed in the console's MaxDD column; the ALL3 column is the binding one.

The one swept parameter q changes nothing: FULL ALL3 is **0.0% / 0.0% / 0.6%** at q = 0.30 / 0.50 / 0.70,
and OOS ALL3 is **0.0% at every q**. The best pair anywhere is TOP20|TOP10 at 8.3% FULL ALL3 and
**0.0% OOS** — a concentration switch, not a regime gate.

## The decisive cross-tab: 4b passes are blends, not edges

| panel | conditional books passing **4b** | of those, ALL3 | **CAGR-beats** | Sharpe-beats | MaxDD-beats | 4a |
|---|---|---|---|---|---|---|
| U56 | 25 / 240 | **0** | **0** | 14 | 6 | 0 |
| B136 | 11 / 240 | **0** | **0** | 3 | 4 | 1 |
| SMALL439 | 0 / 240 | 0 | 0 | 0 | 0 | 2 |

**All 36 conditional 4b passers fail the parents bar, and all 36 fail it on CAGR.** Among the 18
unconditional parents, exactly one passes 4b anywhere (U56 TOP20).

The mechanism is visible in the rule-8 pick itself, `EWALL|LOWVOL20@CALM70` on U56:

| book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| **C = EWALL\|LOWVOL20@CALM70** | **11.51%** | **1.210** | **-17.79%** | 1.294 | 1.126 | 11.20% | 1.224 | -17.79% |
| parent EWALL | 13.25% | 1.123 | -22.53% | 1.194 | 1.067 | 13.79% | 1.134 | -22.53% |
| parent LOWVOL20 | 6.81% | 1.000 | -14.79% | 1.201 | 0.827 | 6.37% | 0.918 | -14.79% |

C's CAGR and MaxDD sit **strictly between** its parents — it interpolates, as the form guarantees. Its
only win over both is Sharpe (+0.087), which is the generic mixing gain from combining two
imperfectly correlated books, available without any timing skill. **4b then passes it because 4b's DD
and CAGR legs are BRACKETING FLOORS**: EWALL fails 4b on drawdown (-22.53% against the -20.23%
floor) and LOWVOL20 fails on H2 (0.827 against SPY's 0.829, by 0.002), so a blend that lands between
them clears both floors while beating neither parent on either. That is 4b's blend loophole, and the
parents bar closes it exactly.

## Rule 8 — (pair, state) chosen on IS 2010–2016 only, OOS 2017–2026 read once

| panel | selector | IS pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | pick's OOS ALL3 | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 | IS Sharpe-bar passers (no IS ALL3 passer existed) | EWALL\|LOWVOL20@CALM70 | 1.197 | **11.20% / 1.224 / -17.79%** | **False** | False | **True** |
| B136 | IS Sharpe-bar passers (none ALL3) | EWALL\|MADG@CALM50 | 1.196 | 10.04% / 1.268 / -12.24% | False | False | False (CAGR 10.4% vs the 10.7% floor) |
| SMALL439 | IS ALL3 passers | TOP20\|LOWVOL20@CALM70 | 0.945 | **3.19% / 0.328 / -28.75%** | **False** | False | False (every leg) |

References on the same panels and windows: **RULES v2 (live)** U56 OOS 9.51% / 1.282 / -12.05%,
B136 8.0% / 1.119 / -12.24%, SMALL439 3.85% / 0.568 / -14.68%; **RULES v1** U56 7.66% / 0.741,
B136 5.94% / 0.576, SMALL439 6.35% / 0.492; **SPY** OOS 15.4% / 0.879 / -33.72%.

**SMALL439 is the cleanest rule-8 result in the run:** the only panel with an IS ALL3 passer picks it,
and its Sharpe collapses **0.945 → 0.328 (-65%)** while MaxDD deepens from -11.6% to -28.8%. The
parents bar does not survive being optimised against either.

KEEP paths over the whole menu (720 conditional + 18 parents): **U56 4a 0/246, 4b 26/246; B136 4a
1/246, 4b 11/246; SMALL439 4a 2/246, 4b 0/246; BOTH 0/246 on every panel.**

## The one KEEP-candidate, and why it is PARKed
`EWALL|LOWVOL20@CALM70` on U56 passes 4b on a genuine walk-forward selection (see memo for exact
RULES wording). It is PARKed, not proposed: it fails the parents bar on CAGR and MaxDD, it loses to
the live RULES v2 book out of sample on Sharpe (1.224 vs 1.282) and on drawdown (-17.8% vs -12.1%),
4a is False, and it is 1 of 26 U56 books in this menu that pass 4b — a discrimination rate consistent
with idea 311's finding that 4b barely discriminates on this panel.

## What this licenses
The queue's conditional is met. Offered for the Sunday review and **not applied here**: add to
PROTOCOL rule 4, ahead of the half-sample tests —

> **4c (parents precondition, for any conditional or regime-switching book):** a book of the form
> "A when S, else B" is only KEEP-eligible if it beats BOTH A and B, each run unconditionally at the
> same gross over the same window, on CAGR **and** Sharpe **and** MaxDD. Report the two parents'
> numbers alongside the candidate's.

Measured cost of adopting it in this menu: it removes **36 of 36** 4b passes and **2 of 2** full-sample
ALL3 passes that do not transport, and removes nothing that survives out of sample.

Script: `2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-unconditional-parents_cloud.py`
Outputs: `.books.csv` (all 774 book-panel rows), `.parents.csv` (all 720 bar cells), `.grid.csv`, `.walkforward.csv`, `.console.txt`
