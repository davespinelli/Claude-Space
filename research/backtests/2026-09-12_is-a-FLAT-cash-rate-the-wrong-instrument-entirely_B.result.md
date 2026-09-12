# Idea 642 — is a FLAT cash rate the wrong instrument entirely? (lane B, 2026-09-12)

**VERDICT: KILL as a capital idea / ANSWERED as a convention question — and the queue's premise is
half confirmed, half REVERSED.** The backloading is real (SHY paid **0.81%/yr in sample and
1.74%/yr out of sample, 2.15x**), but it is the **LEVEL**, not the **PATH**, that moves the
verdicts: once a flat rate is matched to SHY's own compounded return on the window being scored,
the real path is worth **≤ 0.039 of OOS Sharpe** at every one of 25 grid points (mean −0.015).
The finding that does matter for capital is a different one, and it is a selector hazard:
**crediting the idle leg at ANY non-zero rate — the right instrument included — flips the rule-8
pick from gross 1.00 to gross 0.50 on 6 of 7 arms and turns a 4b OOS PASS into a 4b OOS FAIL.**

Script: `research/backtests/2026-09-12_is-a-FLAT-cash-rate-the-wrong-instrument-entirely_B.py`
Panel: U56 (`baseline.load_universe()`, committed cache). 10 bps, t+1, weekly.
Tuned parameters: exactly 2 — `band` ∈ {0.00, 0.01, 0.03, 0.05, 0.08}, `gross` ∈ {0.50, 0.65, 0.75,
0.90, 1.00}. All 25 points × 7 cash arms × 3 windows = 175 cells reported in `.grid.csv`.

## Unparking

The queue marked 642 "PARK/needs local data until the series is in data/" for a 3M T-bill path.
No download was needed: **`SHY` (iShares 1-3y UST, adjusted close = total return) is a committed
column of `data/prices.csv` back to 2008-01-02**, and idea 796 (2026-09-11, lane B) already swept
the idle leg into it. 796 did not separate level from path; that separation is this run's job.

## Gates (5 of 5 PASS, printed before any new number)

| gate | result |
|---|---|
| G1 LIVE RULES v2 @10bps U56 | 8.6282% / 1.2018 / −12.0549% vs committed, max\|d\| **4.063e-05** |
| G2 SPY buy-and-hold | 15.1631% / 0.8861 / −33.7172% vs committed, max\|d\| **4.561e-05** |
| G3 `backtest_cash(cash=0)` == `engine.backtest` | max\|d\| **0.000e+00** (bit-identical) |
| G4 fully-idle book credited at SHY == SHY itself | max\|d\| **0.000e+00** |
| G5 live-book idle share vs idea 796's 0.467/0.472/0.464 | 0.4672 / 0.4722 / 0.4631, max\|d\| **8.944e-04** |

## The seven cash arms

`ZERO` (0 bps, the live convention — `engine.py` credits the idle fraction at exactly zero) ·
`FLAT150` · `FLAT300` (the record's convention, idea 406) · `FLATMATCH_ORACLE` (flat rate matched
to SHY's compounded return **on the window being scored** — the level-only counterfactual, NOT
tradeable, labelled ORACLE everywhere) · `FLATMATCH_IS` (matched on 2009–2016 only, then held
fixed — what an honest 2016 analyst would have written down) · `BILLPATH` (SHY's trailing 252d
return, lagged one day, accrued daily: the rate cycle with the mark-to-market stripped out — the
closest bill-ladder proxy the cache can build) · `SHYPATH` (SHY's own daily total return).

## Pre-registered hypotheses

| H | reading | verdict |
|---|---|---|
| **H_BACKLOAD** SHY's OOS credit ≥ 2× its IS credit | IS **0.8108%**, OOS **1.7419%**, **2.15×** | **PASS** |
| **H_FLATWRONG** 150 bps errs in opposite directions IS vs OOS | IS **+0.6892%**, OOS **−0.2419%** | **PASS** |
| **H_PATH** \|OOS Sharpe(SHYPATH) − OOS Sharpe(FLATMATCH_ORACLE)\| > 0.05 somewhere on the grid | max **0.0392**, mean **−0.0149**; CAGR gap mean **−0.04 pp/yr** | **FAIL — it is the LEVEL** |
| **H_DURATION** \|SHYPATH − BILLPATH\| OOS Sharpe > 0.05 | max **0.0236** | **FAIL on Sharpe** |
| **H_VERDICT** level-matched flat and the real path give different KEEP counts | 4b **7 = 7**, 4a-vs-live **12 vs 14** | **PASS, but only via 4a/MaxDD** |

H_PATH is the queue's own hypothesis and it fails. The one place the real instrument does separate
from a level-matched flat is **drawdown, not Sharpe**: at the live cell SHYPATH returns **+0.587 pp**
of MaxDD relief over ZERO against BILLPATH's **+0.115 pp**, because SHY's duration rallies in equity
drawdowns. That is a *duration* effect, i.e. the one thing a real T-bill would NOT have given you —
the opposite of what the queue item asked for.

## Where the credit lands (live cell, band 0.03 / gross 0.75, idle share 0.4672)

| arm | credit IS pp/yr | credit OOS pp/yr | ΔSharpe IS | ΔSharpe OOS | ΔMaxDD pp |
|---|---|---|---|---|---|
| FLAT150 | +0.759 | +0.757 | +0.103 | +0.095 | +0.038 |
| FLAT300 | +1.512 | +1.508 | +0.204 | +0.188 | +0.075 |
| FLATMATCH_ORACLE | +0.411 | +0.878 | +0.056 | +0.110 | +0.033 |
| FLATMATCH_IS | +0.411 | +0.410 | +0.056 | +0.051 | +0.021 |
| BILLPATH | +0.666 | +0.640 | +0.090 | +0.079 | +0.115 |
| SHYPATH | +0.390 | +0.808 | +0.065 | +0.094 | **+0.587** |

The record's 150 bps **over-credits the IS window by 0.69 pp/yr and under-credits the OOS window by
0.24 pp/yr**; 300 bps over-credits both (+2.19 / +1.26). So the flat convention flatters exactly the
window rule 8 uses to *choose* and starves the one rule 8 *reads* — the queue's mechanism is
confirmed. It just does not change the answers, because 0.4 pp/yr of misplaced credit on a 47%
idle leg is worth ~0.05 of Sharpe.

## Both KEEP paths, all 175 cells (`.keeppaths.csv`)

| arm | 4a vs live book | 4a matched (same arm both sides) | 4b |
|---|---|---|---|
| ZERO | 0 | 0 | 5 |
| FLAT150 | 12 | 6 | 8 |
| FLAT300 | 12 | 8 | 10 |
| FLATMATCH_ORACLE | 12 | 6 | 7 |
| FLATMATCH_IS | 10 | 4 | 6 |
| BILLPATH | 12 | 7 | 7 |
| SHYPATH | 14 | 6 | 7 |
| **total** | **72 / 175** | **37 / 175** | **50 / 175** |

The 4a column is reported twice on purpose. Judged against the live book *as it is priced today*
(cash at zero) a credited arm wins 72 times; judged against the same book carrying the same credit
it wins 37 times. **Roughly half of every "4a win" a cash credit produces is the credit itself, not
the book** — which is the comparand error idea 796's headline (SHY-swept vs live-at-zero) contains.

## RULE 8 — (band, gross) chosen on 2009–2016 alone, 2017–2026 read once (`.walkforward.csv`)

| arm | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1/H2 | 4b |
|---|---|---|---|---|---|---|
| ZERO | band 0.08, gross 1.00 | **12.04%** | 1.1654 | −19.05% | 1.246 / 1.079 | **PASS** |
| FLAT150 | band 0.08, gross 0.50 | 7.03% | 1.3618 | −9.71% | 1.424 / 1.298 | FAIL (CAGR) |
| FLAT300 | band 0.08, gross 0.50 | 8.08% | **1.5535** | −9.66% | 1.595 / 1.515 | FAIL (CAGR) |
| FLATMATCH_ORACLE | band 0.08, gross 0.50 | 7.20% | 1.3929 | −9.70% | 1.452 / 1.333 | FAIL (CAGR) |
| FLATMATCH_IS | band 0.08, gross 0.50 | 6.55% | 1.2728 | −9.74% | 1.345 / 1.197 | FAIL (CAGR) |
| BILLPATH | band 0.08, gross 0.50 | 7.07% | 1.3665 | −9.61% | 1.452 / 1.276 | FAIL (CAGR) |
| SHYPATH | band 0.08, gross 0.50 | 7.20% | 1.3716 | −8.92% | 1.485 / 1.251 | FAIL (CAGR) |
| **RULES v2 baseline (live)** | — | 9.47% | 1.2782 | −12.05% | 1.410 / 1.134 | — |
| **RULES v1 (previous)** | — | 7.60% | 0.7361 | −13.83% | 1.029 / 0.423 | — |
| **SPY buy-and-hold** | — | 15.33% | 0.8767 | −33.72% | 0.980 / 0.765 | — |

OOS 4b bars read on the OOS window's own SPY: Sharpe 0.8767, halves 0.9802/0.7650, CAGR floor
10.7322%, MaxDD cap −20.2303%. Spearman(IS Sharpe, OOS Sharpe) over the 7 arms = **+0.5766** (n=7).

**Every credited arm clears the OOS Sharpe, half and drawdown legs comfortably and fails on the
CAGR floor alone, by 2.65 to 4.18 pp.** They are not bad books; they are half-invested books.

## Why the picks flip — and why the one PASS is not a KEEP (`.identifiability.csv`)

Sharpe is scale-invariant, so with cash at zero the `gross` dial reaches IS Sharpe only through
costs. Its mean spread across the five gross rungs is **0.0010** for ZERO — the selector is picking
on the fourth decimal — against **0.087 to 0.322** for every credited arm, i.e. **84× to 309× more
visible in sample**, and pointing at gross 0.50 every time. Meanwhile that same dial is worth
**5.1 to 6.2 pp of OOS CAGR**.

So the ZERO arm's rule-8 4b PASS is a **tie-break, not a selection**: at band 0.08 its five gross
rungs span IS Sharpe **1.121735 … 1.122612** while spanning OOS CAGR **5.98% … 12.04%**. A fourth-
decimal perturbation moves it from a 4b PASS to a 4b FAIL with 6 pp less return. **It is not
claimed as a KEEP and nothing is promoted.** (Its full-sample cell — 11.39% / 1.1461 / −19.05%,
halves 1.2437/1.0660 — does clear 4b on paper with +0.78 pp of CAGR and +1.18 pp of MaxDD room,
which is exactly how thin a knife-edge this is. The gross ladder is already the subject of ideas
677/679 and the 2026-09-12 ZERO-CASH-convention runs; this run adds no claim there.)

## What this says about the record's convention

Not a rules change and not a protocol change — rule 6, proposed only:

1. **The flat convention is defensible in aggregate and indefensible in the selector.** Its verdict
   error is ≤ 0.05 Sharpe, but a non-zero credit of any kind makes `gross` identifiable to an IS
   Sharpe chooser and points it at cash. A run that credits the idle leg and then tunes gross on IS
   Sharpe is measuring the cash rate, not the book.
2. **A credited arm must be scored against a comparand carrying the same credit.** 72 vs 37 4a
   passes is the size of that error on this grid.
3. If a credit is used at all, **`FLATMATCH_IS` is the only honest flat rate** (0.81%, calibrated on
   the IS window and carried forward). 150 bps and 300 bps are both wrong, and 300 bps is the
   direction that flatters.

## Caveats

`universe.json` is a **current-constituent list** — U56 carries survivorship bias and every CAGR
above is biased upward; the 4b CAGR floor is therefore, if anything, too easy. SHY is 1–3y
duration, not 3M bills: `BILLPATH` is this run's duration-stripped proxy and the two differ by
≤ 0.024 of OOS Sharpe, so the substitution does not carry the argument. Only 2020 and 2022 are real
stress tests in the OOS window. `ORACLE` arms read the answer on their own window by construction
and are controls, never candidates.

`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched. No KEEP, no memo, no
book promoted.
