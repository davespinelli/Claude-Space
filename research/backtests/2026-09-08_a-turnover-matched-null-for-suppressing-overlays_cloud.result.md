# Idea 203 — a turnover-matched null for suppressing overlays (cloud, 2026-09-08)

**Verdict: ANSWERED / the requested instrument KILLED / the premise CORRECTED.** The null idea 203
asks for **cannot exist**, and the run proves it constructively. The matched-count null it names
(**MC**) is a strict **downgrade** on the incumbent rotation null: worse turnover fidelity (10.3% vs
6.8% of base turnover) *and* it destroys the clustering the incumbent preserves exactly (switch-count
match 8.0% vs 100%). And the 1782.7% figure the idea is built on is an **artefact of the
denominator**, not of the null: on an overlay-independent denominator the same rotation null is off
by **6.8% mean / 13.6% max**. Nothing is nominated: the 9 incidental 4b passers belong to the base
book, which clears 4b un-overlaid, and the overlay adds less than a randomly-timed one.

## The obstruction, stated before any number was read
BUDGET's ON indicator is not an arbitrary state series. It is

    s_j = 1{ tt_j > tau },   tt_j = the turnover the base book would trade at rebalance j

— **a threshold on the very quantity the null is asked to match.** The ON set is therefore exactly
the top-K rebalance dates ranked by `tt`, so

> **the only matched-count draw whose skipped turnover equals the real overlay's is the real
> overlay.**

A matched-count null with exact turnover fidelity is **degenerate** for this family: one element,
zero entropy. Fidelity and independence-from-the-overlay are not two properties to optimise — they
are one dial read from two ends. `STRAT(f)` (draw K dates from the top-M by `tt`, M = ⌈K/f⌉) is that
dial, and the run reads it end to end:

| f | M/K | overlap with the real ON set | fidelity (÷ base turnover) | null sd(dSharpe) |
|---|---|---|---|---|
| 1.00 | 1.00 | **100.0%** | **0.0%** | **0.0000** |
| 0.75 | 1.33 | 80.9% | 7.5% | 0.0519 |
| 0.50 | 2.00 | 68.9% | 9.0% | 0.0583 |
| 0.25 | 4.00 | 58.9% | 9.8% | 0.0597 |

Monotone by construction. At f = 1.00 the "null" *is* the overlay: perfect fidelity, zero entropy,
tests nothing. There is no interior point that has both.

## Gates
| gate | measure | result |
|---|---|---|
| G1 | `fast_backtest` == `engine.backtest`, U56 base book, 0 bps | max abs diff **1.388e-17** — PASS |
| G2 | cost identity `r(c) = r(0) − turnover·c/1e4` | **0.000e+00** — PASS |
| G3 | null structure over 100 draws: on-count preserved | **100/100** — PASS |
| G3b | circular switch count preserved | ROT 25/25, RUN 25/25, **MC 6/25, STRAT 5/25** |
| G4 | reproduce idea 186's fidelity on its own tau grid {0.10,0.20,0.30} | **25.3% mean / 271.6% max** vs published **25.4% / 213.8%** |

**Determinism defect found and fixed in this run.** The first draft seeded each cell's RNG with
Python's built-in `hash()` of the cell key. `hash()` on strings is randomised per process, so two
runs of the same file disagreed in the third significant figure (ROT fid/base 6.9% vs 6.8%, chosen-
null counts 10/14/4 vs 14/10/2 — no conclusion moved, but PROTOCOL rule 5 requires deterministic).
Seeds now come from an md5 of the cell key: verified identical across processes (227645 and the same
draws), where the old path gave 1798 and 7727. Every number below is from the deterministic run.

## The correction: idea 191's 1782.7% is a denominator artefact
Idea 186 defines fidelity as `|TO_null − TO_real| / TO_real`. But a *suppressing* overlay drives its
own denominator toward zero as its on-share rises — at `tau=0.05` the overlay skips 91.8% of
rebalances, so `TO_real` is nearly zero and any relative error explodes:

| tau | on-share | fid ÷ real (published form) | fid ÷ real, max |
|---|---|---|---|
| 0.05 | 91.8% | **9368.3%** | 34159.8% |
| 0.10 | 83.8% | 97.6% | 271.6% |
| 0.20 | 61.6% | 27.4% | 54.3% |
| 0.30 | 26.3% | 10.5% | 22.2% |
| 0.50 | 7.7% | 3.0% | 9.8% |

Correlation of the published fidelity with on-share is **r +0.302** — idea 191's "degrades without
bound in on-share" is **confirmed**, and now explained: it is the *statistic* that degrades, not the
null. Divide by the **base** book's turnover instead — overlay-independent, bounded — and the
incumbent rotation null is within **6.8% mean, 13.6% max** across the whole widened grid.
**The rotation null was never as broken as the record says.**

## The four nulls, mode = skip (the suppressing overlay idea 203 is about; 30 cells each)
| null | fid ÷ real | max | fid ÷ base | max | overlap | switch match | clears q95 |
|---|---|---|---|---|---|---|---|
| ROT (incumbent) | 1901.4% | 34159.8% | **6.8%** | 13.6% | 54.5% | **100.0%** | 0.0% |
| **MC (what idea 203 asks for)** | 4722.6% | 75618.7% | **10.3%** | 18.1% | 54.2% | **8.0%** | 0.0% |
| RUN (matched count *and* clustering) | 2008.7% | 34930.6% | **6.8%** | 12.6% | 54.1% | **100.0%** | 0.0% |
| STRAT(0.75) | 4663.8% | 74375.1% | 7.5% | 17.8% | 80.9% | 13.0% | 0.0% |
| STRAT(0.50) | 4682.8% | 73323.1% | 9.0% | 17.5% | 68.9% | 11.3% | 0.0% |
| STRAT(0.25) | 4685.3% | 75880.3% | 9.8% | 18.1% | 58.9% | 8.7% | 0.0% |

(mode = half, where the overlay halves a trade instead of suppressing it, is well-conditioned under
both denominators: ROT 4.4% ÷ real and 3.3% ÷ base. The pathology is specific to *suppression*.)

**MC is a strict downgrade** and should not replace the rotation null. **RUN** — permute the
run-length decomposition of the state — is the one improvement available: the same exact
preservation of on-count and circular switch count as ROT, equal fidelity (6.8%), a tighter max
(12.6% vs 13.6%), and unlike ROT it is not limited to J correlated one-offset draws.

## Re-pricing idea 186's BUDGET family: the overlay loses to its own null
The real overlay's `dSharpe` sits **below the mean of its own null band** in the suppressing mode and
level with it in the halving mode:

* **skip**: real **−0.0539** vs null mean **+0.0275** — skipping the highest-turnover rebalances is
  *worse* than skipping the same number of randomly-chosen ones.
* **half**: real **+0.0288** vs null mean **+0.0335**.
* **clears the null's q95: 0 of 420 rows full sample; 1 of 420 out of sample** (BROAD136,
  tau=0.05 skip, STRAT(0.75) @25 bps, +0.2646 vs q95 +0.2604 — one row at a 93.6% on-share, i.e.
  inside the nominal 4.8% size of the test and not a finding).

## Rule 8 — the null chosen on 2010-2016 by turnover fidelity alone, 2017-2026 read once
Chosen null across 60 cells: STRAT(0.75) 20, RUN 16, ROT 12, STRAT(0.50) 6, STRAT(0.25) 4, MC 2.
The choice roughly halves IS fidelity error (U56/skip 3.9% chosen vs 6.4% ROT; U56/half 1.9% vs
3.4%) and **changes no verdict**: OOS clear rate **0.0% (0/60) under the chosen null and 0.0%
(0/60) under the incumbent; the two disagree on 0.0% of cells.** A better-matched null buys accuracy
in the fidelity column and nothing in the verdict column.

## KEEP paths — and a correction to my own first reading
Real BUDGET books, 3 panels x 5 tau x 2 modes x 2 rungs = 60: **4a 0/60, 4b 9/60**, every one on U56
in **half** mode. Benchmarks (u56 sample, 10 bps): SPY 15.23% / 0.8890 / -33.72%, halves
0.957/0.834, OOS 15.45% / 0.8820; RULES v2 (live) 8.66% / 1.2056 / -12.05%, halves 1.226/1.191, OOS
9.53% / 1.2851; RULES v1 Sharpe 0.6647.

**The 4b passes belong to the BASE BOOK, not to the overlay.** This run's own un-overlaid base
book — U56 top-20 by the composite among names above the 200d MA with vol20 < 0.60, equal weight at
gross 0.75, weekly, t+1 — already clears 4b on its own: **12.86% / 1.1075 / -18.21%, halves
1.110 / 1.112, OOS 14.49% / 1.1775** at 10 bps, and again at 25 bps (11.27% / 0.9844 / -18.33%).
The best overlaid cell (U56 tau=0.05 half @10 bps, 13.25% / 1.1207 / -18.17%, OOS 15.18% / 1.2057)
adds **+0.013 of Sharpe** to that, which is *below* what a randomly-timed half-rebalance of the same
count adds (ROT null mean +0.0170, MC +0.0209, RUN +0.0194) and clears the null's q95 under **none**
of the seven variants.

*(An earlier draft of this memo claimed the un-overlaid parent fails 4b on drawdown at -21.37% and
filed a PARK memo on that basis. That was wrong: -21.37% is idea 430's top-20 EW book, which has no
vol cap and is a different parent. Scored against this run's actual base book the overlay adds
nothing that clears a null, so there is no candidate here and the PARK memo has been withdrawn.
This is the same conclusion lane B reached independently on the same day.)*

For completeness, the arm-level rule-8 read (tau, mode chosen on 2010-2016 by IS Sharpe, 2017-2026
read once) clears 4b in **1 of 6** panel x rung picks: U56 @10 bps picks `tau=0.50 skip` (OOS 13.95%
/ 1.1026 / -20.90%, 4b FAIL), U56 @25 bps picks `tau=0.05 half` (OOS 14.12% / 1.1303 / -18.25%, 4b
PASS), and BROAD136 / SMALL439 fail at both rungs (OOS Sharpe 0.7507 / 0.6973 and 0.1881 / 0.1094,
all below SPY's 0.8820). The live question — is partial rebalancing the real turnover dial? — is
already open as idea 412 and belongs there, not to BUDGET.

**A degenerate arm was found and excluded.** On SMALL439 the `tt` distribution sits well above
tau=0.05, so that arm skips *every* rebalance and holds its day-0 weights — which are all zero,
because no score exists before 252 closes. The result is an all-cash book with undefined Sharpe. A
chooser must not be allowed to argmax over a NaN; non-finite IS Sharpes are now excluded and counted
(1 arm per SMALL439 rung).

## Caveats carried
Survivorship: all three panels are current-constituent lists and SMALL439 contains no delistings;
real and null draws inherit it identically so the null *comparison* is unaffected, the *level* of
every number is not. SMALL439 drops the 44 tickers with `max_1d_move ≥ 1.0`. 20 draws per cell gives
the clause a nominal one-sided size of 1/21 = 4.8%, approximate. 4a/4b are judged on the u56
benchmark bars for every panel, as the record does. Ideas 126 (t+1) and 38 (calendar-day index) carry.

Outputs: `.console.txt` `.grid.csv` (420 rows) `.fidelity.csv` `.frontier.csv` `.walkforward.csv`
`.armwalkforward.csv` `.keep.csv`.
