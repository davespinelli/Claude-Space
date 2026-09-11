# Idea 794 — does a REALISED-VOL TARGET on the BAND BOOK spend the UNUSED DRAWDOWN BUDGET?

**lane B, 2026-09-11. VERDICT: KILL for the overlay** — the budget *is* spendable and spending
it *does* buy the missing CAGR, but a **constant** gross buys it more cheaply. The scaler is a
net cost on 27 of 30 cells, and every cell that clears 4b has pinned itself to the cap.
**No RULES change; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-11_realised-vol-target-on-band-book_B.py`. Artefacts: `.grid.csv` (30 U56 cells),
`.broad.csv` (30 B136 cells), `.matched.csv` (30 exposure-matched controls), `.reference.csv`,
`.walkforward.csv`, `.summary.json`, `.console.txt`.

## The book under test

Live band 0.03 **frozen** (not a dial). Base = that band book at gross 1.00. Risk proxy
`u_t = sum_i W_base_{t-1,i} ret_{t,i}` (no costs), `sigma_t = std(u_{t-L+1..t}) sqrt(252)`,
`s_t = min(1.00, TARGET/sigma_t)`, `W_t = W_base_t s_t`. Two tuned parameters and no more:
**TARGET** ∈ {0.05, 0.06, 0.08, 0.10, 0.12, 0.15} × **LOOKBACK** ∈ {21, 42, 63, 126, 252} = 30
cells, **all reported**. CAP 1.00 is the PROTOCOL no-leverage bound, not a dial. 10 bps, next-day
execution, weekly — every change the scaler makes is charged.

## Gates — four, all PASS

| gate | reading |
|---|---|
| G1 live cell == live book | Sharpe **1.1998** (= `baseline.rules_v2_weights`, record 1.1998), MaxDD **-12.05%**, OOS CAGR **9.45%** |
| G2 no lookahead | max \|s_t(full panel) − s_t(panel truncated at t)\| = **0.000e+00**, 5 dates × 5 lookbacks |
| G3 degenerate limit | TARGET 10.0 pins s to the cap; **0.000e+00** over the 4,433 days after the warm-up transition, **0** differing days |
| G4 comparands are the record's | SPY full **15.11% / 0.8835 / -33.72%**, OOS **15.24% / 0.8721**; 4b floors **10.58% / 10.67%**, DD caps **-20.23%** |

G3 was re-specified after its first reading (1.662e-04 → FAIL). All 67 differing days sit in the
0.75 warm-up window and the one-day transition out of it, which is the engine re-setting held
weights only on a rebalance day — a warm-up convention, not the scaler. Both segments are
printed beside the gate rather than dropped. Disclosed in the script header.

## (1) The budget is real and it is spendable — H_BUDGET HELD

The live book spends **59.6%** of the 4b drawdown budget (-12.05% against the -20.23% cap) and
misses the full-sample CAGR floor by **-1.96 pp** (8.61% vs 10.58%). **11 of 30** cells clear all
five 4b legs on the full sample; the best-CAGR cell (t=0.15, L=126) reads **11.53% / 1.2006 /
-15.91%**, +0.95 pp over the floor at **78.6%** of the budget. The CAGR floor is again the **only**
binding leg anywhere on the grid: b_cagr fails 19 of 30, b_h1 / b_h2 / b_oos / b_dd fail **0**.
**4a passes 0 of 30** — nothing beats the live book's -12.05% while raising return.

## (2) The scaler does not earn its keep — H_TIMING FALSIFIED, and this is the answer

Each cell is scored against a **constant** gross matched on its own mean realised exposure
(g* = Ebar_cell / Ebar_gross1.00; `.matched.csv`). The scaler **loses** on **27 of 30** cells:
median ΔSharpe **-0.0227** (mean -0.0289), median ΔCAGR **-0.47 pp**, for a median **+0.23x/yr**
of extra turnover. Its only compensation is drawdown — median ΔMaxDD **+0.82 pp** — which the
book does not need, since the unused budget is the premise of the idea. The three cells where it
wins (t=0.15, ΔSharpe +0.0074 / +0.0061 / +0.0010) are the cells where g* ≈ 0.993–0.999, i.e.
where there is nothing left to time.

## (3) The 4b passers are degenerate — the mechanism never fires where it pays

The base book's own realised vol at gross 1.00 is **9.29%/yr**. Every TARGET that clears the CAGR
floor is *above* the vol it is targeting, so the scaler sits at the cap: every 4b passer has
**sbar ≥ 0.9560** and is capped on **≥ 69.5%** of days (at t=0.15, 95–98%). Across the 30 cells
**rho(sbar, CAGR) = +0.9849** — the grid's return ordering is its exposure ordering and nothing
else. A vol target that clears the floor *is* constant gross 1.00 with a turnover bill attached.

## (4) Rule 8 — H_WF HELD, and it is the exposure that walks forward

Both pre-registered IS-only selectors (2009–2016), read on 2017–2026 **once**:

| selector | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS halves | 4b OOS |
|---|---|---|---|---|---|---|
| S1 highest IS Sharpe | t=0.10, L=126 | 11.20% | 1.2113 | -15.36% | 1.2988 / 1.1197 | **all 5 pass** |
| S2 highest IS Sharpe clearing the IS CAGR floor (feasible set **EMPTY**, 0/30 → pre-registered fallback to highest IS CAGR) | t=0.15, L=126 | **12.65%** | **1.2735** | -15.91% | 1.4008 / 1.1340 | **all 5 pass** |
| RULES v2 live | band 0.03, gross 0.75 | 9.45% | 1.2747 | -12.05% | — | CAGR leg fails |
| SPY | — | 15.24% | 0.8721 | -33.72% | 0.9762 / 0.7598 | — |

The two selectors **disagree** on TARGET (0.10 vs 0.15) and S2's pick is the one that is ~98%
capped — the walk-forward's answer is "use more exposure", not "time it".

## (5) What it all collapses to — and a correction to the record's standing candidate

| book | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | turnover | 4b full / OOS |
|---|---|---|---|---|---|
| **band 0.03 × gross 1.00** (nothing tuned) | **11.52% / 1.1996 / -15.91%** | 1.2354 / 1.1711 | **12.66% / 1.2740 / -15.91%** | 2.35x | **PASS / PASS** |
| idea 795's pick band 0.08 × gross 1.00 | 11.37% / 1.1439 / -19.05% | 1.2437 / 1.0619 | 12.00% / 1.1616 / -19.05% | 1.48x | PASS / PASS |
| RULES v2 live band 0.03 × gross 0.75 | 8.61% / 1.1998 / -12.05% | 1.2349 / 1.1718 | 9.45% / 1.2747 / -12.05% | 1.77x | FAIL / FAIL |

Holding the **live** band and moving only gross **dominates idea 795's two-parameter pick on every
OOS leg**: CAGR **+0.66 pp**, Sharpe **+0.1123**, MaxDD **+3.14 pp** shallower — and it spends 79%
of the drawdown budget where 795's pick spends 94%. This is an independent confirmation of idea
795's own caveat (b), "the band leg is noise the walk-forward paid for", reached from a different
direction: 795 needed the band move only because no gross at band 0.03 cleared its **IS** CAGR
floor, and this run's grid shows the same IS floor is empty (0 of 30) while the OOS floor is not.
Memo: `2026-09-11_u56-band003-gross100_4b_B_MEMO.md`.

## (6) B136 replication (reported, never selected)

Same 30 cells on the broad panel: **4b 2/30, 4a 0/30**; SPY full 15.23% / 0.8890 / -33.72%, live
band book 8.03% / 1.1058 / -12.24%. The ordering is the same (return tracks sbar, the scaler adds
turnover), the level is lower, and the two 4b passers are again the most-capped cells. Same-sign,
weaker — as in 795.

## Verdict and the disclosed correction to the verdict rule

**KILL for the vol-target overlay.** As first written the script's verdict rule was
`KEEP-candidate (4b) if H_BUDGET and H_WF`, which would have read **KEEP-candidate (4b)**. That
rule cannot tell "the overlay works" from "the overlay pinned itself to a constant", which is
exactly what section (3) shows it did, so the rule now also requires **H_TIMING**. The change is
disclosed in the script, both readings are printed, and no cell count moved.

## Limits

`universe.json` is current-constituent survivorship-biased (data/ has no delisted names and the
sandbox has no network, so this cannot be measured internally — see idea 786). The vol proxy is
the book's own return, not a forecast; a better volatility model is not tested here and this run
does not claim vol targeting is useless in general, only that **on this book, at this cadence and
cost, the scaler is dominated by the constant it collapses to**. Gross 1.00 remains a corner at
the PROTOCOL no-leverage bound with no cash buffer, and 2009–2026 is one QQQ-favourable regime.
