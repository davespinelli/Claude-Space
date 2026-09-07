# Idea 336 — re-price the fixed ABSOLUTE breadth threshold as a QUANTILE

**Lane C, 2026-09-07. Verdict: SPLIT — the queue's DIAGNOSIS is CONFIRMED and its REMEDY is KILLED.** Idea 42's SMALL484 collapse is a firing-RATE artefact, not a property of the panel or of the gate: 85.7% of the cross-form OOS-Sharpe movement on SMALL484 is carried by the rate term, and in the exact cell the queue names it is +0.448 of a +0.517 recovery. But the causal expanding quantile is not a usable instrument. It under-fires its own nominal q by 3–4× (realised/q = 0.00–0.31), the q = 0.07 arm is INERT on all three panels, PROTOCOL rule 8's chooser picks that inert arm in 5 of 6 headline cells, and the family earns **4a 0/486** and **4b 50/162 @10 bps → 1/162 @25 bps**, with 42 of the 50 passes inherited from an ungated parent that already passes. No RULES change, no book promoted, no KEEP claimed; RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

Script: `research/backtests/2026-09-07_re-price-the-fixed-ABSOLUTE-breadth-threshold-as-a-quantile_C.py`
Data: `.grid.csv` (1 998 rows), `.decomposition.csv` (486), `.matched.csv` (162), `.walkforward.csv` (36), `.console.txt`.

## Design

Base book, fixed, idea 28/42's, never tuned: **EWALL(G)** = equal-weight every name above its own 200d MA with `vol20 < 0.60`, at `G/E_t`, weekly, next-day execution. Overlay: carry the book at `(1 − depth)` of its exposure whenever panel breadth is low; the switch executes at t+1 and pays the rung on `|Δmult| · G` of notional (idea 40/42's convention verbatim).

Four threshold forms on the same base book:

| family | rule | fires at | role |
|---|---|---|---|
| **ABS(B)** | `breadth_t < B`, B ∈ {0.30, 0.40, 0.50} | `f_panel(B)` | idea 42 verbatim — the comparand |
| **QUANT(q)** | `breadth_t <` causal expanding q-quantile of the panel's own breadth | measured | **the tuned family** |
| **ABSMATCH(q)** | absolute `B'` set at the panel quantile matching QUANT(q)'s *realised* rate | = QUANT(q) | rate-matched control (look-ahead in the RATE) |
| **DIAG** | quantile form at the panel's own nominal rate `f_panel(B)` | ≈ `f_panel(B)` | secondary read (look-ahead in the RATE) |

**Tuned parameters — exactly two.** (1) `q ∈ {0.07, 0.12, 0.17}` = U56's own realised firing rates under idea 42's own `B = {0.30, 0.40, 0.50}`, read off idea 42's committed console before any number here was computed; (2) `depth ∈ {0.25, 0.50, 1.00}`. 9 points, **all reported** at every panel / gross / cadence / rung. Reported and never selected on: panel {U56, B136, SMALL484}, gross {0.75, 0.85, 1.00}, cadence {D, W}, cost {0, 10, 25} bps. ABSMATCH and DIAG are controls: never tuned, never in the chooser, and no verdict is taken from them.

**Reproduction gates, all PASS, printed before any new number was read.** G1 derived rung `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`: **0.000e+00**. G2 idea 84's ungated EWALL U56 g=0.85 @10 bps 11.8% / 1.05 / −17.9% / H 1.07 / 1.03 vs published 11.8% / 1.05 / −17.9% / 1.07 / 1.04 — MATCH. G3 idea 42's committed gate grid re-run here, **486 of 486 rows joined, max abs diff over 6 columns 2.220e-16**. G4 decomposition identity `dTOTAL = dFORM + dRATE`: **1.110e-16** over 486 cells.

## Q1 — mechanics: the quantile equalises the RATE across panels, and misses its own LEVEL

Realised daily firing share, 10 bps, g = 0.75, cadence D:

| panel | ABS B=0.30/0.40/0.50 | QUANT q=0.07/0.12/0.17 |
|---|---|---|
| U56 | 0.070 / 0.123 / 0.167 | 0.002 / 0.032 / 0.052 |
| B136 | 0.065 / 0.109 / 0.152 | 0.000 / 0.025 / 0.047 |
| SMALL484 | 0.258 / 0.522 / 0.838 | 0.000 / 0.018 / 0.045 |

Cross-panel spread (max − min) collapses from **0.193 / 0.413 / 0.686** (ABS) to **0.002 / 0.015 / 0.007** (QUANT) — G5 PASS, and the sharpest single number in the run. But that is only the cross-panel claim. **Level fidelity is a separate question and it FAILS:** realised/nominal = 0.032 / 0.270 / 0.306 (U56), 0.000 / 0.207 / 0.277 (B136), 0.004 / 0.148 / 0.266 (SMALL484). A causal *expanding* quantile only fires at rate q if breadth is exchangeable over the sample; it is not. The estimator is anchored by the 2008–2011 lows and later breadth almost never revisits them, so the gate decays toward inertness the longer it runs. **q = 0.07 is an inert arm on all three panels** (0.000–0.002 of days); at cadence W on SMALL484 it never fires at all (`dSharpe` vs its matched twin is exactly 0.000000).

## Q2 — the queue's diagnosis: CONFIRMED, it is the RATE

`dTOTAL = QUANT(q) − ABS(B)` split into `dFORM = QUANT(q) − ABSMATCH(q)` (same realised rate, quantile vs absolute day-selection) and `dRATE = ABSMATCH(q) − ABS(B)` (both absolute, different rate). Rate-match quality `|quant_on − absmatch_on|`: max 0.0086, median 0.0018.

Share of total absolute movement carried by the RATE term:

| panel | Sharpe | OOS Sharpe | CAGR |
|---|---|---|---|
| U56 | 60.4% | 57.4% | 74.5% |
| B136 | 69.8% | 46.4% | 89.4% |
| **SMALL484** | **83.5%** | **85.7%** | **85.2%** |

The exact cell the queue names — SMALL484, B = 0.50 → q = 0.17, depth = 1.00, D, g = 0.75, 10 bps — fires 0.838 of days as ABS and 0.045 as QUANT, and recovers **dTOTAL OOS Sharpe +0.517 = dRATE +0.448 + dFORM +0.069**. Idea 42's `-0.403 vs inaction` was the panel being held 84% in cash, not the gate disagreeing with the panel. The instrument is the same instrument; only the frequency differed.

## Q3 — the remedy: KILLED, what remains is not an edge

Against the **ungated parent (do nothing)**, mean over all 486 QUANT points by panel: U56 dCAGR −0.001 / dSharpe +0.020 / dOOS +0.048; B136 −0.002 / +0.008 / +0.019; **SMALL484 −0.001 / −0.001 / −0.001**. On the panel the whole idea was raised for, the quantile gate is worth nothing at all — it stops the destruction and adds none of its own.

Against the **matched-mean-gross static twin** (a plain gross dial at the gate's own realised exposure, 10 bps, all three gross levels, 162 cells): mean dSharpe U56 +0.021, B136 +0.009, **SMALL484 +0.0001**; dOOS +0.049 / +0.020 / **+0.0000**. Eleven of 162 cells pass 4b where the twin fails — all cadence D, all q ∈ {0.12, 0.17}, all on U56/B136, none on SMALL484.

**KEEP paths over the whole grid:** 4a **0/486** at every rung, every panel, both cadences, all three gross. 4b (162 QUANT points per rung): 77 @0 bps → **50 @10 bps → 1 @25 bps**, and **42 of the 50 are inherited** — their own ungated parent passes 4b too (U56 g=0.85, B136 g=0.75/0.85). The 8 "earned" passes are all at g = 1.00, where the parent misses the DD cap and the gate's de-grossing to a mean 0.975 exposure closes it: idea 311's dial-placement shape.

The single 25-bps survivor, B136 QUANT q=0.12 d=1.00 D g=1.00 (12.5% / 0.949 / −18.1% / H 1.035/0.861 / OOS 0.975), is **not filed as a candidate**: it ranks **6th of 9 in-sample** at both 10 and 25 bps, so rule 8's chooser never selects it, and what the chooser does select at that gross fails 4b outright.

## Rule 8 walk-forward (10 bps, g = 0.75; the chooser sees IS Sharpe 2009–2016 only)

| panel | family | cad | pick | OOS Sharpe | do-nothing OOS | **vs_nogate** | regret | SPY OOS |
|---|---|---|---|---|---|---|---|---|
| U56 | QUANT | D | q0.07 d0.25 | 1.093 | 1.112 | **−0.019** | −0.226 | 0.882 |
| U56 | ABS | D | B0.40 d0.25 | 1.156 | 1.112 | +0.044 | −0.092 | 0.882 |
| B136 | QUANT | D | q0.07 d0.25 | 1.019 | 1.019 | **0.000** | −0.094 | 0.882 |
| B136 | ABS | D | B0.40 d0.25 | 1.039 | 1.019 | +0.021 | −0.066 | 0.882 |
| SMALL484 | QUANT | D | q0.17 d0.50 | 0.451 | 0.416 | **+0.036** | −0.014 | 0.882 |
| SMALL484 | ABS | D | B0.40 d1.00 | 0.013 | 0.416 | **−0.403** | −0.386 | 0.882 |

Over all 18 QUANT walk-forward cells the chooser beats do-nothing **3/18**, against ABS's 12/18; mean vs_nogate by panel is U56 −0.006, B136 0.000, SMALL484 +0.016. The quantile form is *worse* than the absolute form under the identical chooser on both large panels. **Its entire SMALL484 advantage (0.451 vs 0.013) is achieved by not firing** — the chooser picks the inert q = 0.07 arm in 5 of the 6 headline cells, and where it does not (SMALL484, cadence D) the gate is on 4.5% of days. No arm on any panel clears SPY's 0.882 OOS on SMALL484; the two large panels clear it with or without the gate.

## What the record should take from this

1. **Idea 42's cross-panel ordering is retired as an instrument claim.** Any published contrast between panels that rests on a *fixed absolute* threshold applied to a panel-dependent distribution is measuring the firing rate, not the signal. On SMALL484 that is 84–86% of the movement.
2. **A causal expanding quantile is not the drop-in fix.** It equalises the rate across panels (spread 0.686 → 0.007) but does not deliver its nominal level, and it decays toward inertness as history accumulates. A rolling or blocked-bootstrap quantile would be the honest next form; this run does not test one and makes no claim about it.
3. **The breadth gate remains a de-grossing dial.** 4a 0/486; 4b passes are inherited or gross-dial placements and survive 25 bps once in 486.

## Caveats

All three panels are current-constituent lists — **survivorship** — so CAGR and drawdown *levels* are optimistic and 4b's DD cap is a level test; the gated-vs-parent and gated-vs-twin *contrasts* are the durable part. SMALL484 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136's. ABSMATCH and DIAG carry look-ahead in the firing rate by construction and are controls only. The matched-gross twin was run at 10 bps only. The `q = 0.07` column is reported throughout even though it is inert, because dropping it after seeing that would be exactly the tuning PROTOCOL rule 7 forbids.
