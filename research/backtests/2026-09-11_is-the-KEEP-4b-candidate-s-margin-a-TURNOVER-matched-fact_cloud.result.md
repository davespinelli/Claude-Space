# Idea 678 — is the KEEP-4b candidate's margin a TURNOVER-matched fact?

**Run:** 2026-09-11, cloud lane. Script `2026-09-11_is-the-KEEP-4b-candidate-s-margin-a-TURNOVER-matched-fact_cloud.py`.
Artefacts: `.grid.csv` (54 cells), `.draws.csv` (9,000 book-rows at 10 bps), `.walkforward.csv` (9), `.console.txt`.

## Verdict: ANSWERED — **NO, it is not. Idea 502's 0/1000 was a TURNOVER artefact, and the KEEP does need a base-rate clause after all.**

No book promoted, no RULES change, no PROTOCOL edit applied. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## Gates (9, pre-registered, printed before any new number was read) — ALL PASS

| gate | result |
|---|---|
| G1 `ctx.run` == `engine.backtest` @10 bps | **6.939e-18** |
| G2 `band_book(0.03,0.75)` == `rules_v2_weights` | **0.000e+00** |
| G3 the 2026-09-04 KEEP-4b incumbent re-derived on full U56 | 12.63% / 1.0903 / −18.31% vs published 12.66% / 1.0921 / −18.31%, max\|d\| **1.777e-03** |
| G4 every null book: ≤20 names, each at exactly 0.75/20, gross ≡ 0.75×held/20 | dev **0.000e+00** |
| G5 the three cost rungs are ONE gross stream minus turnover×c/1e4 | **2.060e-18** |
| G6 draws reproducible (seed 678 re-run) | **0.000e+00** |
| G7 SMALL439 drops all 44 `max_1d_move >= 1.0` tickers | 44 dropped |
| G8 **RANDGEO(p=1) == idea 502's committed RANDROT** | gross **0.7195** (published 0.7195), turnover **36.44x/yr** (published 36.48x) |
| G9 turnover(p) monotone (the bisection's precondition) | 3.55 → 4.93 → 6.80 → 12.15 → 22.15 → 36.50x |

## The null

`RANDGEO(p)`: up to 20 names at exactly 0.75/20, forced out when they leave the eligible set
(above the 200d MA, vol20 < 0.60), otherwise leaving with probability p per weekly rebalance, vacancies
refilled uniformly from the eligible names not held. p is solved by bisection on log p so the null's
**median** realised turnover equals the target, on **40 pilot seeds disjoint from the 1,000 evaluation
seeds**. p→0 is the turnover floor (forced exits only); p=1 is exactly idea 502's RANDROT (G8).
The candidate differs from RANDGEO(p\*) in ONE way only: which of the eligible names it holds.

## The answer, U56 (the candidate's own panel), 1,000 draws

candidate: turnover **9.64x/yr**, gross 0.7151, mean 37.5 eligible names.

| rung | null turnover | 4b share @0 bps | **@10 bps** | @25 bps | cand Sharpe pctile @10 | cand OOS-Sharpe pctile @10 |
|---|---|---|---|---|---|---|
| p=0 (forced only) | 3.53x | 87.8% | **53.5%** | 6.6% | **19.3%** | 38.3% |
| 0.5x | 4.83x | 78.3% | **38.3%** | 2.3% | 43.9% | 44.7% |
| **1.0x (matched)** | **9.62x** | 81.0% | **13.4%** | 0.0% | **82.3%** | **67.3%** |
| 2.0x | 19.28x | 80.6% | 0.2% | 0.0% | 99.6% | 96.7% |
| 4.0x = p=1 (502's RANDROT) | 36.48x | 73.7% | **0.0%** | 0.0% | 100.0% | 100.0% |

* **At the candidate's own turnover, 134 of 1,000 coin flips clear 4b at PROTOCOL's own 10 bps rung.**
  Idea 502's 0/1000 is reproduced here at 36.48x — its gross-matched null traded **3.8x** the
  candidate — so the entire separation it reported was the nulls' cost, not the composite's selection.
* At **0 bps the pass share is flat in turnover** (0.737–0.878 across a 10x turnover range): the 4b bar
  is cleared by three quarters of coin flips regardless, exactly as idea 502 found.
* The candidate's one-sided empirical p against the matched null is **0.177** (Sharpe) and **0.327**
  (OOS Sharpe) at 10 bps — inside its own null on both.
* **A slower coin flip beats it.** At 3.53x/yr the candidate sits at the **19.3rd** Sharpe percentile and
  53.5% of those nulls clear 4b: at 10 bps the best random book is not the matched one, it is the lazy one.
* What the candidate does own: **CAGR percentile 100.0%** at every rung and **MaxDD percentile 0.1%** —
  selection buys return and pays drawdown, never risk-adjusted return (ideas 504/672 replicate).
* Binding 4b bar inside the matched null at 10 bps: **CAGR** (74% of failures), i.e. the cost-eroded
  return floor, not the drawdown cap.

## Replication panels (labelled; no verdict taken from them)

* **B136** (250 draws, candidate turnover 13.77x): matched rung 13.84x → 4b **31/250 (12.4%)** @10 bps,
  candidate Sharpe percentile 63.6%. The candidate itself **fails 4b** on B136 (H2 leg) at 10 and 25 bps.
* **SMALL439** (250 draws, candidate turnover 20.20x, survivorship caveat below): **0/250 at every rung
  and every cost rung**, and the candidate fails 4b on all five bars. The candidate does dominate its null
  there (Sharpe percentile 90–95%), but nothing on that panel comes near the bar.

## Rule 8 (PROTOCOL 8) — turnover target chosen on 2009–2016 only, 2017–2026 read once

Pick rule pre-registered and outcome-blind (the rung whose median **IS** turnover is closest to the
candidate's own IS turnover, p re-calibrated on IS data alone). It picks **1.0x on all three panels**
(U56 gap 0.01x, B136 0.00x, SMALL439 0.07x).

| panel | cost | candidate OOS (CAGR/Sharpe/MaxDD) | null median OOS | null p95 Sharpe | RULES v2 OOS | SPY OOS | cand OOS pctile | null 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | 0 | 15.41% / 1.2437 / −18.22% | 12.23% / 1.2361 / −15.46% | 1.3533 | 9.64% / 1.2992 / −12.03% | 15.24% / 0.8721 / −33.72% | 54.4% | 823/1000 |
| **U56** | **10** | **14.31% / 1.1648 / −18.31%** | **11.13% / 1.1348 / −15.58%** | **1.2519** | **9.45% / 1.2747 / −12.05%** | **15.24% / 0.8721 / −33.72%** | **65.5%** | **119/1000** |
| U56 | 25 | 12.68% / 1.0461 / −18.44% | 9.49% / 0.9820 / −15.73% | 1.0991 | 9.15% / 1.2378 / −12.09% | 15.24% / 0.8721 / −33.72% | 78.9% | 1/1000 |
| B136 | 10 | 12.49% / 0.8919 / −20.05% | 9.49% / 0.8981 / −17.89% | 1.0308 | 7.98% / 1.1185 / −12.24% | 15.45% / 0.8820 / −33.72% | 47.2% | 25/250 |
| SMALL439 | 10 | 7.23% / 0.4873 / −27.43% | 2.86% / 0.2701 / −34.79% | 0.4824 | 3.85% / 0.5680 / −14.68% | 15.45% / 0.8820 / −33.72% | 95.2% | 0/250 |

Out of sample, at the binding rung, the candidate's Sharpe is **inside** its matched null (65.5th
percentile, below the null's own 95th percentile of 1.2519) and **below RULES v2** (1.1648 vs 1.2747);
its OOS CAGR beats the null's median by 3.2 pp and its OOS drawdown is 2.7 pp deeper. Neither KEEP path
passes for any null book on any panel: **4a 0 of 54 cells**, and 4b only via the shares tabled above.

## What this means for capital

The standing 2026-09-04 KEEP-4b candidate still *passes* 4b on U56 at 10 bps — that verdict is unchanged.
What changes is its **margin**: at its own turnover, one coin flip in seven clears the same bar, and the
rule sits at the 82nd percentile of that null, not outside it. Idea 502's conclusion ("no base-rate clause
needed at the protocol's cost rung") is **overturned by its own logic**: the 0/1000 it relied on came from a
null trading 3.8x faster. Nothing here promotes a book, and nothing here demotes the incumbent's verdict —
it prices the incumbent's evidence at p ≈ 0.18 rather than p < 0.001.

## PROTOCOL wording PROPOSED for Sunday review (not applied)

> **4c (base rate, proposed).** A 4b KEEP must publish, beside its verdict, the 4b pass share of a null
> matched to the book on BOTH gross and realised turnover at the same cost rung, and the rule's own
> percentile inside that null. A KEEP whose matched-null pass share exceeds 10% is PARK, not KEEP.

## Survivorship (PROTOCOL 9)

B136 is today's constituents; SMALL439 is the current sub-$2B screen only (`data/SMALL_PANEL_README.md`);
names delisted, acquired or grown out of the screen are absent, so every level on those panels is biased
upward. A random list drawn from a survivor panel is a **better** book than a real-time random list would
have been, so the null's pass share is an **upper** bound and the candidate's percentile inside it a
**lower** bound — the bias runs against the incumbent, not for it, and the headline (13.4%, 82.3rd
percentile) is on U56, which carries the mildest version of it.
