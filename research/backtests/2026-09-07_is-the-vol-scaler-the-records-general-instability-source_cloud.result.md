# Idea 381 — is the vol scaler the record's general instability source? (cloud, 2026-09-07)

**Verdict: SCALER (pre-registered reading), with one qualification that must travel with it.**
The `1/sqrt(vol20)` ranking scaler — not the name count — is what breaks the sign of a quoted
price's denominator. On the axis idea 122's claim was actually made about (the **panel axis**,
D3) the effect is **positive on both panels** (+0.2318 u56, +0.2133 broad). On the joint
D1+D2+D3 screen the effect is **+0.4043 on u56 (5/5 rungs) and −0.0561 on broad (2/5)**, i.e.
the joint-screen gap is a u56 fact. Concentration **fails** as an explanation on both panels
and in both scaler states. **No KEEP, no book promoted, no RULES/PROTOCOL change proposed**;
RULES.md, scan.py, bot.py and baseline.py untouched.

Script `…_cloud.py`; console `…_cloud.console.txt`; data
`…_cloud.{grid,draws,d3,signtest,cellstats,matched,tau,w1,walkforward}.csv`.
704 arm-points (11 books × 16 treated arms × 2 published rungs × 2 panels) on D1/D2, plus
**14,960 sub-panel backtests** on D3 (2 panels × 40 draws × 11 books × 17 arms). Total 2,076 s.

## 0. What was actually varied

Idea 124 could not answer this question: its ladder was scaler-OFF at every rung and carried
exactly **one** scaler-ON book (V1u, n=5). A one-rung contrast cannot separate "the scaler is
bad" from "the scaler is bad at five names". This run puts the scaler on the whole ladder:

| scaler | books |
|---|---|
| OFF | TOP3 TOP5 TOP10 TOP20 TOP40 (idea 124's ladder, replicated) |
| ON | VS3 VS5 VS10 VS20 VS40 (**new**: `comp / clip(vol20,0.08)**0.5`) |
| n/a | TOPall (unranked; the scaler is provably a no-op) |

Inside a matched pair everything else is identical — same composite, same top-n rule, same
equal weight `GROSS/n`, same weekly cadence, same next-day execution, same 17 arms, same cost
rungs. Two tuned parameters: the scaler and the panel. `n` is the subject axis, every rung
reported. `q = 0.10`, `tau = 0.90` inherited unchanged from ideas 119/122/124.

Two structural facts, stated before the run and then gated:
1. `GROSS/5 = 0.75/5 = 0.15 = WV1`, so **VS5 *is* idea 94's V1u exactly** — the record's own
   unstable book is a rung of this ladder, not a separate object (G2 = 0.000e+00).
2. The scaler is a *ranking* instrument; at `n = all` nothing is ranked, so a scaler-ON TOPall
   is byte-identical to TOPall (G6 = 0.000e+00). The ladder must converge as n → all whatever
   the scaler does.

## 1. Reproduction gates — all PASS before any new number was read

| gate | result |
|---|---|
| G1 shared books == idea 124's `targets_n`, all 11 gate/conv combos | **0.000e+00** |
| G2 **VS5 == idea 94's V1u** | **0.000e+00** |
| G3 control `run()` == `engine.backtest` | **0.000e+00** |
| G6 scaler is a no-op at n=all | **0.000e+00** |
| G4 448 shared grid rows vs idea 124's **committed** `grid.csv` | max\|d\| **1.776e-15** |
| G5 224 shared D3 rows at q=0.10 vs idea 124's **committed** `d3.csv` | max\|d\| **1.776e-15** |
| LIVE RULES v2 on u56 @10 bps | 8.66% / 1.2056 / −12.05%, halves 1.2259/1.1908 — exact |

G5 is the strongest of these: the bootstrap consumes idea 124's `default_rng(20260907)` stream
in the identical q-order and only *backtests* the q=0.10 block, so these are literally the same
40 sub-panels idea 124 drew. This run is a strict superset of idea 124's screen, not a
re-derivation of it.

## 2. The headline — the matched contrast (q=0.10, tau=0.90)

`adm_pub` = share of a cell's **published** rows (|dMaxDD| ≥ 0.10 pp) surviving D1+D2+D3.

| panel | n | adm_pub OFF | adm_pub ON | Δ | d3_pub OFF | d3_pub ON | Δ (panel axis) |
|---|---|---|---|---|---|---|---|
| u56 | 3 | 0.5556 | 0.5000 | +0.056 | 0.6667 | 0.5000 | +0.167 |
| u56 | **5** | **1.0000** | **0.3333** | **+0.667** | **1.0000** | **0.4167** | **+0.583** |
| u56 | 10 | 0.8636 | 0.1250 | +0.739 | 1.0000 | 0.5000 | +0.500 |
| u56 | 20 | 0.7273 | 0.2500 | +0.477 | 0.9091 | 1.0000 | −0.091 |
| u56 | 40 | 1.0000 | 0.9167 | +0.083 | 1.0000 | 1.0000 | 0.000 |
| broad | 3 | 0.4211 | 0.7273 | −0.306 | 0.7895 | 0.7273 | +0.062 |
| broad | **5** | 0.7143 | 0.4706 | +0.244 | **1.0000** | **0.4706** | **+0.529** |
| broad | 10 | 0.3889 | 0.2917 | +0.097 | 0.8889 | 0.5833 | +0.306 |
| broad | 20 | 0.3333 | 0.5882 | −0.255 | 1.0000 | 0.7647 | +0.235 |
| broad | 40 | 0.7857 | 0.8462 | −0.060 | 0.8571 | 0.9231 | −0.066 |

- **mean Δ adm_pub = +0.1741** over the 10 (panel × n) pairs; OFF ≥ ON on **7/10** — exactly
  the pre-registered bar. **SCALER holds.**
- **mean Δ d3_pub (panel axis alone) = +0.2226**, and it is positive on **both** panels
  (+0.2318 u56, +0.2133 broad).
- By cost rung: mean **+0.1722** over the 20 (panel × n × cost) pairs, sign 14/20 — not a
  single-rung artefact.
- By tau: +0.182 / +0.174 / +0.172 / +0.222 at tau = 0.80 / 0.90 / 0.95 / 1.00 — flat.

**The n=5 row is the direct answer to idea 122.** At the same five names, the same 15% weights,
the same gross and the same arms, the scaler-OFF book TOP5 keeps its denominator's sign on
**100%** of panel draws on both panels; the scaler-ON book at n=5 — which *is* V1u — keeps it
on **41.7%** (u56) and **47.1%** (broad). Idea 122's failure address was the scaler, and it is
not a five-name effect: the same gap appears at n=10 on both panels.

## 3. Concentration fails as the explanation

| panel | scaler | spearman(n, adm_pub) | spearman(n, d3_pub) | adm_pub range |
|---|---|---|---|---|
| u56 | OFF | +0.4617 | +0.4472 | 0.556 – 1.000 |
| u56 | ON | +0.1000 | +0.7906 | 0.125 – 0.917 |
| broad | OFF | +0.1000 | +0.2052 | 0.333 – 0.786 |
| broad | ON | +0.3000 | +0.7000 | 0.292 – 0.846 |

`spearman(n, adm_pub) ≥ +0.50` in **0 of 4** (panel × state) cells, so the pre-registered
CONCENTRATION reading fails. This is idea 124's non-monotonicity finding, replicated and now
shown to hold *inside each scaler state separately*. TOPall — where the scaler provably cannot
act — sits at adm_pub 0.9583 (u56) and 1.0000 (broad), the top of both ladders.

## 4. The qualification that must travel with the headline

Two things cut against a clean "corpus-wide" reading and are reported rather than buried:

1. **The joint screen is a u56 fact.** Mean Δ adm_pub is **+0.4043 on u56 (5/5 rungs positive)**
   and **−0.0561 on broad (2/5)**. Only the **panel axis (D3)**, which is what idea 122's claim
   was actually about, is positive on both panels. The corpus-wide claim is safe on D3 and is
   **not** established on the joint D1+D2+D3 screen.
2. **Rule 8 / W1 — the contrast has the wrong sign in-sample.** Recomputing the whole screen on
   2009-2016 only and then reading 2017-2026 untouched:

   | window | mean Δ adm_pub | sign pairs | mean Δ d3_pub |
   |---|---|---|---|
   | IS (2009-2016) | **−0.0524** | 5/10 | −0.0211 |
   | OOS (2017-2026) | **+0.2073** | 7/10 | +0.2073 |
   | full | +0.1741 | 7/10 | +0.2226 |

   The scaler's instability is an **out-of-sample-window** phenomenon: in the first half the
   two states are indistinguishable. That is the good direction for a walk-forward claim (the
   effect is *not* an in-sample artefact) but it also means the effect is a 2017-2026 fact, not
   a stationary one, and a single window is one observation.

Also: 40 draws at one q is a 40-point binomial per cell, so a share near 0.90 carries a ±~0.09
sampling band; idea 216's warning about few-block estimators applies to every share above.

## 5. Rule 8 / W2 — the price lists the two states produce

Per (panel, book, cost) cell, S1 = idea 94's selector (among arms buying ≥ 1.0 pp of IS MaxDD,
the lowest IS rate), evaluated untouched on 2017-2026:

| scaler | cells with a pick | above SPY OOS | above RULES v2 OOS | above own control | mean OOS Sharpe | mean OOS CAGR | mean spearman(IS,OOS) |
|---|---|---|---|---|---|---|---|
| OFF | 20 | **11/20** | 0/20 | 10/20 | **0.9145** | 15.75% | −0.0340 |
| ON | 18 | **3/18** | 0/18 | 4/18 | **0.5654** | 5.05% | **+0.3877** |
| n/a (TOPall) | 4 | 4/4 | 0/4 | 3/4 | 1.1356 | — | +0.5967 |

SPY OOS Sharpe 0.8820 (15.45% CAGR, −33.72% MaxDD); RULES v2 OOS 1.2851 (u56) / 1.1185 (broad).
Two scaler-ON cells (u56 VS20) had **no** eligible arm at all.

The scaler damages the **level**, not the **ordering**: scaler-ON cells produce far worse books
(mean OOS Sharpe 0.5654 vs 0.9145, mean OOS CAGR 5.05% vs 15.75%) while their price lists
actually re-order *more* consistently out of sample (+0.39 vs −0.03). Neither state ever beats
the live RULES v2 baseline out of sample (0/42).

## 6. KEEP paths

**4a: 0 of 704 arm-points** at any rung, either scaler state. 4b: **36/320 scaler-OFF**,
**11/320 scaler-ON**, 14/64 TOPall — a 3.3× ratio in the same direction as the sign test. Every
scaler-ON 4b passer is u56 VS20 (5) or VS40 (6), i.e. the wide end where the scaler barely
binds. Failing 4b bars: H2 397, OOS 387, CAGR 379, DD 322, H1 286.

## 7. Caveats

1. **SURVIVORSHIP** — `universe.json` and `universe_broad.json` are current-constituent lists,
   so every absolute CAGR here is optimistic. The subject of this run is the **sign of a
   difference** between two arms sharing a panel and the same days, which is far less exposed
   than a level.
2. u56 and broad share names — two panels is not two independent samples.
3. One q (0.10) and 40 draws per cell; see the binomial band noted in §4.
4. This run tests the scaler as a **ranking** dial only. It says nothing about a vol scaler
   used for **sizing**, which is a different instrument.
