# Idea 1627 — is EVERY sleeve and hedge in the record a CARRY claim wearing an INSTRUMENT?

**2026-09-20, lane cloud (idea 1 of 2). ANSWERED: YES. KILL the sleeve family — retire all eight
instruments and keep one accrual line. NO NEW BOOK; RULES.md untouched (rule 6).**

Script `research/backtests/2026-09-20_every-sleeve-a-carry-claim_cloud.py` ·
grid `.grid.csv` (456 rows, every cell) · `.walkforward.csv` · `.instruments.csv` ·
`.gates.csv` · `.log.txt` / `.console.txt`. **Gates 19/19.**

## The construction

Live RULES v2 band book (200d ±3% hysteresis, equal weight inside, de-gross to cash, gross 0.75,
weekly, 10 bps, t+1). Fraction **F** of the gated-out (idle) NAV is routed to a sleeve. Two arms
on the same names, the same days, the same frame, the same F ladder, the same turnover charge:

* **ETF** — the instrument itself, marked to market (what the record actually priced).
* **MATCH** — a **zero-duration accrual** at a constant daily rate compounding to **that
  instrument's OWN realised CAGR** on that panel's scored tape. Same carry, zero vol, zero
  drawdown, zero mark-to-market.

`ETF − MATCH` is therefore **the instrument's own price path and nothing else**. A third arm,
**MATCH_IS**, sets the rate from 2009–2016 only and is the arm rule 8 uses, so no accrual rate a
chooser can pick has read an OOS row.

Dials (PROTOCOL rule 4, exactly two): **F** ∈ {0.00, 0.25, 0.50, 0.75, 1.00} and **the instrument**
∈ {SHY, IEF, TLT, GLD, TIP, HYG, LQD, UUP}. Panels (U56 / B136 / SMALL) and arms are reported
axes, not dials. Gross frozen at 0.75, band at 0.03. 3 × 8 × 5 × 3 = **360 priced cells, all
published**, plus 96 differenced cells.

## The answer: 0 of 8 instruments survive at full routing

"Survives" = the ETF arm is strictly better than its own matched accrual on Sharpe **and** no worse
on MaxDD.

| instrument | survives, all F (of 12) | survives at F = 1.00 (of 3) | mean dSharpe | mean dMaxDD |
|---|---|---|---|---|
| SHY | 7 | **0** | **+0.0012** | **+0.38 pp** |
| IEF | 3 | **0** | −0.0101 | −3.99 pp |
| UUP | 1 | **0** | −0.0430 | −0.11 pp |
| TIP | 0 | **0** | −0.0529 | −3.39 pp |
| LQD | 0 | **0** | −0.1278 | −7.81 pp |
| TLT | 0 | **0** | −0.1422 | −13.21 pp |
| HYG | 0 | **0** | −0.2482 | −8.75 pp |
| GLD | 1 | **0** | −0.2731 | −3.94 pp |

**12 of 96** differenced cells survive (U56 3/32, B136 4/32, SMALL 5/32), and **0 of 24 at
F = 1.00**. Every survivor sits at F ≤ 0.50 (one SHY/SMALL cell at 0.75), i.e. where the sleeve is
too small to matter. **SHY is the only instrument with a positive mean dSharpe and the only one
whose duration does not cost drawdown** — an independent replication of idea 1602's +0.0009 on a
wider instrument set (+0.0012 here). Every other instrument **loses** to a riskless accrual paying
its own realised carry, and loses **more the more of the book it is given**: the substitution
deficit is monotone in F for 7 of 8 instruments on all three panels.

The mechanism is not subtle and is the point of the idea: these instruments are held for what they
*pay*, and what they *are* is a second source of variance and drawdown bolted onto an equity book
that already has both. TLT at F = 1.00 costs **−20.3 pp of MaxDD on U56 and −28.3 pp on SMALL**
against an accrual paying TLT's own 1.08 %/yr.

## Both KEEP paths, 360 cells

| arm | 4a FULL | 4a OOS | 4b FULL | 4b OOS |
|---|---|---|---|---|
| ETF | 18/120 | 13/120 | 6/120 | 8/120 |
| MATCH | 96/120 | 96/120 | 8/120 | 12/120 |
| MATCH_IS | 84/120 | 84/120 | 8/120 | 16/120 |

**The MATCH arms' 4a passes are an artefact of the construction, not a result.** A zero-vol,
zero-drawdown accrual bolted to 25 % of NAV raises Sharpe and shrinks MaxDD mechanically; 96 of 120
is what that looks like. They are a measuring device, not a book, and nothing here is proposed on
their strength.

Bars — U56 RULES v2 FULL **8.62 % / 1.2011 / −12.05 %**, OOS **9.46 % / 1.2769 / −12.05 %**; B136
**7.96 % / 1.0973 / −12.24 %**, OOS **7.85 % / 1.1019 / −12.24 %**; SMALL **4.26 % / 0.6597 /
−14.16 %**, OOS **3.64 % / 0.5459 / −14.16 %**. SPY FULL **15.12 % / 0.8844 / −33.72 %** (SMALL's
shorter tape 14.01 % / 0.8562), OOS **15.26 % / 0.8738 / −33.72 %**.

## The one instrument that clears 4b — and why it is still not a book

**Every ETF-arm 4b pass in the run is GLD**: U56 F = 0.50/0.75/1.00 and B136 F = 0.50/0.75/1.00
clear 4b **FULL and OOS** (U56 F = 0.75: FULL 12.89 % / 1.2116 / −14.98 %, halves 1.099 / 1.318;
OOS 15.12 % / 1.4002 / −14.98 %, halves 1.561 / 1.265), and SMALL F = 0.75 clears 4b OOS alone.
That is a real, investable book, unlike the MATCH arms.

It is nonetheless **not a KEEP, and this idea is the reason why**: GLD **fails its own substitution
test worse than any other instrument** (mean dSharpe −0.2731). Its 4b pass is bought entirely by
gold's realised **9.51 %/yr CAGR over 2008–2026** — a zero-duration accrual at that same 9.51 %
beats the ETF arm by **+0.63 of Sharpe at F = 1.00 on U56** with 7.1 pp less drawdown. The pass is a
*carry* pass wearing a hedge's name, and the carry is one asset's realised return over one sample.

**Rule 8 settles it (params on 2009–2016 only, 2017–2026 read exactly once).** Two IS-only choosers
— C_SHARPE (argmax IS Sharpe) and C_4B (argmax IS Sharpe among IS-4b passers) — over both arms and
all three panels:

* **ETF arm: 0 of 6 picks clear 4a OOS or 4b OOS.** U56 and B136 both pick LQD F = 1.00 → OOS
  10.86 % / 1.0729 / **−24.31 %** and 9.28 % / 0.9309 / **−25.25 %**, against a live book at
  1.2769 / −12.05 % and 1.1019 / −12.24 %. SMALL picks IEF F = 1.00 (4.36 % / 0.5623 / −24.33 %) or
  TLT F = 0.75 (3.27 % / 0.3674 / −34.17 %). **Every pick roughly doubles the live book's drawdown
  and none of them earns it back.**
* **The chooser cannot reach GLD.** The GLD cells that clear 4b sit at IS-Sharpe ranks
  **#35 / #39 / #40 of 40** on U56, **#26 / #37 / #40** on B136 and **#38 / #39 / #40** on SMALL —
  dead last. Gold was the worst sleeve in the record's IS window and the best in its OOS window.
  Nothing an allocator could have known in 2016 selects it.
* **MATCH_IS picks pass 4a OOS on all three panels and 4b OOS on two — and are fiction.** The rate
  handed to them is HYG's 2009–2016 realised CAGR of **8.78 %/yr** (U56, B136) and TLT's
  **7.57 %/yr** (SMALL), applied as a **riskless** accrual through 2017–2026. No sweep pays that.
  Published in full because the number is informative about *how much* of the sleeve literature is
  carry; it is not a candidate and is not offered as one.

## Verdict

**KILL the sleeve family.** The record's eight non-equity routings are one accrual line wearing
eight tickers: at full routing not one instrument beats a zero-duration accrual paying its own
realised carry, seven of eight lose on both Sharpe and drawdown, and the only 4b-clearing
instrument (GLD) is both the *worst* substitution failure and unreachable by any in-sample chooser.
Hypothesis (a) as pre-registered; (c) as pre-registered. The constructive residue for a future
Sunday review — **not** a rules change, PROTOCOL and RULES.md untouched — is that a sleeve should be
written as an **accrual rate**, and any instrument proposed above that accrual must clear the
`ETF − MATCH` contrast on its own before its name is allowed into the clause.

## Caveats, stated

* **Survivorship (PROTOCOL rule 9).** B136 and SMALL are *current* constituents of their screens;
  both are biased upward and their absolute CAGRs are not investable. Every headline above is a
  **within-panel, same-names, same-days** contrast (ETF minus its own accrual twin), which the bias
  cannot manufacture, but the 4a/4b verdicts on those panels inherit it. SMALL additionally drops
  the **54** tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv` (665 names remain).
* **MATCH is handed the instrument's realised carry**, which is look-ahead by construction — the
  most generous possible version of the substitution, and therefore the right null for "does the
  instrument add anything *beyond* carry". Every walk-forward number uses MATCH_IS instead.
* One frame only (the live band book). The sleeve's contribution under the frozen 2026-09-04
  momentum incumbent was priced for SHY by idea 1602 and is not re-priced here.
* **Gates 19/19**: G0 sample 17.7 y / 17.7 y / 15.6 y; G1 F = 0 invariance 0.000e+00 for all 24
  (sleeve, arm) on all three panels; G2 engine replay of `baseline.compare`'s RULES v2 row
  1.7e-17 / …; G3 a = 0 at F = 1 with sleeve turnover un-charged reproduces the live book to
  3.5e-18 (charged sleeve cost published: 10.24 / 10.25 / 9.08 bps/yr); G4 max gross 1.0000;
  G5 two dials; G6 no chooser reads a row ≥ 2017-01-01; G7 456 rows published; G8 all eight
  instruments' standalone profiles published.
