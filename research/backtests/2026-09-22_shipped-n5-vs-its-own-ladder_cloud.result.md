# Idea 2244 — is the SHIPPED n = 5 DOMINATED BY ITS OWN LADDER? (lane cloud, 2026-09-22)

**ANSWERED = YES, and NO single n is defensible across panels: the dial must be PANEL-CONDITIONAL.**

Script: `2026-09-22_shipped-n5-vs-its-own-ladder_cloud.py`. 168 cells published
(3 panels x 7 rungs n in {3,5,10,15,20,30,40} x 2 cadences {W,M} x 4 cost rungs {0,10,25,50} bps),
gross FIXED at 0.75 by solving `w = gross/n` so the ladder is a BREADTH ladder and not a sizing
ladder. Two tuned dials and no more: **n** and **PANEL**. Cost, cadence and gross are reported.
Book = the shipped v1 composite and eligibility (`max_vol=0.60`, `vol_scale=True`), next-day fill.

## Gates (9 of 9 exact)
| gate | max abs diff |
|---|---|
| G1 numpy engine == `engine.backtest`, 3 panels x {W,M} | **0.000000** (6 of 6; 2 NaN warm-up rows agree in both) |
| G2 shipped `rules_v1_weights(n=5, w=0.15)` == gross-solved `w=0.75/5`, 3 panels | **0.000000** (3 of 3) |

## 1. The shipped default is dominated by its own siblings
Of the 6 sibling rungs, the number that beat `n = 5` **out of sample**:

| panel / cadence | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| U56 W / M | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| B136 W / M | 4 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| SMALL W / M | 1 / 6 | 1 / 6 | 1 / 6 | 4 / 6 |

Pooled over all 24 (panel, cadence, cost) families the mean is **4.5 of 6** on full-sample Sharpe,
4.58 on CAGR and 4.17 on MaxDD. On U56 it is 5 of 6 on Sharpe and on CAGR at **every** family.
`n = 5` is not a default; it is a rung chosen by nobody.

## 2. But the ladder points in OPPOSITE directions on different panels
OOS-Sharpe argmax n:

| panel / cadence | 0 | 10 | 25 | 50 bps |
|---|---|---|---|---|
| U56 W / M | 40 / 40 | 40 / 40 | 40 / 40 | 40 / 40 |
| B136 W / M | 40 / 20 | 40 / 20 | 40 / 40 | 40 / 40 |
| SMALL W / M | **3 / 3** | **3 / 3** | **3 / 3** | **3 / 3** |

The argmax sits at the **widest** rung on the two large-cap panels at 16 of 16 cells and at the
**narrowest** rung on the small-cap panel at 8 of 8. There is no n that is even second-best on
both: on U56/W at 10 bps n = 3 reads OOS Sharpe 0.6392 against n = 40's 1.2430, and on SMALL/W
n = 40 reads 0.4404 against n = 3's 1.1956. **n must be panel-conditional or it is unpriced.**

Mechanism, from the same grid: the v1 book's realised annual turnover falls monotonically in n on
all three panels (U56/W 27.9x at n=3 -> 4.9x at n=40; SMALL/W 35.7x -> 21.8x), so on the large-cap
panels widening the book buys both breadth and a turnover rebate, while on SMALL the concentrated
rung carries a CAGR (13.05% at n=3 vs 5.80% at n=40, W/10bps) large enough to pay its own churn.

## 3. KEEP paths over all 168 cells
* **4a: 0 of 168.** The v1 ranked book never beats live RULES v2 in both halves with no worse
  drawdown, at any n, cadence or cost rung. RULES v2 reads 1.2010 (1.2276/1.1806) / -12.05% on U56;
  the best ladder rung at the live rung is n = 40/W at 1.1208 (1.0913/1.1498) / -13.80%.
* **4b full-sample: 17 of 168. 4b OOS leg: 21. 4b FULL+OOS: 15** (U56 13, B136 1, SMALL 1).
  Ten of the fifteen are at the **0 bps** rung. At the binding 10 bps rung there are **4**, all U56
  and all MONTHLY: n = 15, 20, 30, 40.
* **BOTH paths at once: 0 of 168.**
* `n = 5` itself clears 4b FULL+OOS at **1 of its own 24 cells** (U56/M at 0 bps only).

## 4. Rule 8 walk-forward (n chosen on 2009-2016 by IS Sharpe; 2017-2026 read ONCE)
The chooser beats the shipped `n = 5` OOS in **21 of 24** families: median dOOS Sharpe **+0.1694**,
median dOOS CAGR **+2.00 pp**, median dOOS MaxDD **+0.64 pp** (shallower — it gives up nothing).
4b-OOS pass counts: **CHOSEN 3 of 24, SHIPPED n=5 1 of 24, ORACLE(best OOS) 7 of 24.**

Its picks: U56 15/15/40/40 (W) and 20/20/40/40 (M); B136 30/30/40/40 both cadences;
SMALL 5/5/5/40 (W) and 10/10/10/10 (M). IS->OOS rank persistence of the ladder (spearman over the
7 rungs) is **+0.768 median** over the 24 families, but it is panel-split: B136 **+0.82 to +1.00**,
U56 **+0.29 to +1.00**, SMALL **-0.57 to +0.32** — and on SMALL/M it is NEGATIVE at every cost
rung, which is exactly why the chooser takes n = 10 there (OOS Sharpe 0.3385) while the oracle
rung n = 3 reads 0.6438. **The n dial is learnable on the large-cap panels and anti-learnable on
the small-cap one.**

## 5. One rule-8-reachable 4b candidate — RECORDED, NOT RECOMMENDED
U56, v1 ranked book, **n = 20, gross 0.75, MONTHLY, 10 bps**, next-day fill — the IS-Sharpe
chooser's own pick at that (panel, cadence, cost):

| | CAGR | Sharpe | MaxDD | H1 / H2 | turnover |
|---|---|---|---|---|---|
| candidate, full | 11.21% | 1.0672 | -18.19% | 1.1847 / 0.9719 | 4.82x/yr |
| candidate, OOS | 11.37% | 1.0413 | -18.19% | — | — |
| RULES v2 (live) | 8.62% | 1.2010 | -12.05% | 1.2276 / 1.1806 | — |
| SPY | 15.14% | 0.8851 | -33.72% | 0.9570 / 0.8264 | — |

4b legs: CAGR floor 10.60% (margin **+0.61 pp**), DD cap -20.23% (margin **+2.04 pp**),
H1/H2 and OOS Sharpe all over SPY. **It fails 4a** (Sharpe below RULES v2 in both halves, drawdown
6.1 pp deeper) and **it dies at 25 bps** — CAGR 10.41% against a 10.60% floor, OOS 10.54% against
10.70%. Its more robust neighbour n = 30/M (11.54% / 1.1638 / -15.52%, 4b at 0/10/**25** bps,
DD margin +4.71 pp) is **not** the chooser's pick at any cost rung, so it is post-hoc and is
reported, never adopted.

## Honest caveats
* SURVIVORSHIP: all three panels are CURRENT constituents. SMALL is the sub-$2B screen of
  `data/SMALL_PANEL_README.md` with the 54 names whose `max_1d_move >= 1.0` dropped (665 remain);
  every SMALL number above is survivorship-inflated and is reported, never adopted alone.
* The candidate's CAGR margin is 0.61 pp on a leg the record has repeatedly shown to be the
  largest binding leg and the most cost-fragile one; one cost rung kills it.
* MONTHLY beating WEEKLY on U56 is not new here — idea 2256's grid already established the
  committed book's monthly cadence as the turnover minimum — so the cadence half of this cell is
  a known record fact, not this run's finding.

## Verdict
**ANSWERED = YES (the shipped n = 5 is dominated by its own ladder on 23 of 24 families) +
PANEL-CONDITIONAL (argmax n = 40 on U56/B136, n = 3 on SMALL) + KILL of `n = 5` as a defensible
default + ONE recorded-not-recommended KEEP-4b candidate. 4a 0 of 168, BOTH 0 of 168.**
