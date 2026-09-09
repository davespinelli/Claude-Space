# Idea 315 — does de-lagging the breadth gate turn it into a real bear defence?

**cloud, 2026-09-09** · script `2026-09-09_does-de-lagging-the-breadth-gate-turn-it-into-a-real-bear-defence_cloud.py`

## VERDICT — **KILL. The gate is a volatility discount, exactly as the queue's second branch says.**

The queue set the decision rule in advance: *"If the 2022 column moves, the gate is a timing
signal; if it does not, it is a volatility discount."* The column moves — **but not on the
de-lagging dial**. It moves on `q`, and the queue's own first instrument (rate of change)
moves it the **wrong way**.

492 books: 41 gates × 3 panels (U56 / B136 / SMALL439) × 2 cadences (W/M) × 2 underlyings
(EWALL, MA-DG) + 12 ungated controls. Gross 0.75, DEGROSS, 10 bps, t+1. Gates all PASS before
any hypothesis was read: **G1 2.8e-17**, **G2 causality 180/180 truncated-history rebuilds
agree**, **G3 identity 0.0e+00**.

## 1. The 2022 column moves on `q`, not on de-lagging

Mean calendar-2022 return over the 12 arms, by (variant, q) — every second dial averaged in,
all 40 grid points in `.grid.csv`:

| variant | q=0.10 | q=0.20 | q=0.30 | q=0.40 |
|---|---|---|---|---|
| LEVEL (idea 48's, no de-lagging) | −11.78% | −8.06% | −3.76% | −2.66% |
| ROCQ (rate of change, rate-matched) | −8.94% | −8.10% | −7.34% | −5.42% |
| ASYM (hysteresis re-entry) | −6.93% | −2.90% | −2.92% | −2.59% |
| BOTH | −9.35% | −7.46% | −3.17% | −2.15% |

The **level dial alone** carries **+9.12 pp** (LEVEL −11.78% → −2.66%). At *matched* q the
de-lagging instruments carry: ASYM **+5.16 pp** at q=0.20, **+0.84** at q=0.30, **+0.07** at
q=0.40; **ROCQ −0.04 / −3.58 / −2.76** — i.e. **the queue's literal instrument makes 2022
worse than the un-de-lagged gate at three of the four q values.** ROCQ's mean edge in the
three worst SPY years is **−1.04 pp**: gating on the rate of change removes the defence
instead of sharpening it.

## 2. What ASYM actually buys 2022 with (U56, weekly, EWALL — every year printed)

| | 2018 | 2019 | 2020 | 2021 | **2022** | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| ungated control | +0.05% | +21.63% | +21.47% | +19.57% | **−11.99%** | +23.45% | +19.99% | +16.73% |
| LEVEL@0.20 (idea 48's) | +1.99% | +15.90% | +13.36% | +19.57% | **−9.85%** | +16.97% | +19.99% | +8.16% |
| ASYM@q=0.40/qup=0.50 (best 2022) | +0.71% | +5.01% | +7.74% | +19.57% | **−1.54%** | +5.92% | +20.25% | +6.63% |

The best-2022 cell buys **+10.45 pp in 2022** and pays **−16.6 pp in 2019, −13.7 in 2020,
−17.5 in 2023**. On SMALL439 the same cell posts **+0.00% in 2022** (fully in cash) and
**−17.38% in 2024**. That is not a defence being sharpened; it is a larger cash position.

## 3. H_TIMING passes its relative bar and fails the arithmetic

Three worst SPY calendar years: **2022 (−18.2%), 2018 (−4.6%), 2015 (+1.2%)**. In 425 of 480
gated cells (**88.5%**) the drawdown-year edge over the control exceeds the other-year edge,
so H_TIMING "passes" at its pre-registered 80% bar. But the levels say what the ratio hides:

| variant | edge in the 3 worst years | edge in the other 15 |
|---|---|---|
| ASYM | **+1.72 pp** | **−3.39 pp** |
| LEVEL | +0.57 pp | −2.40 pp |
| ROCQ | −1.04 pp | −4.01 pp |
| ROC (raw, unmatched rate) | −0.62 pp | −7.11 pp |
| BOTH | +0.12 pp | −5.72 pp |

Blended over the 18-year sample the best variant is **3/18 × 1.72 − 15/18 × 3.39 = −2.54
pp/yr**. Across all 480 gated books: **98.5% have a LOWER CAGR than their own ungated control,
87.9% a lower Sharpe, and 86.2% a shallower drawdown** (mean ΔCAGR −2.5 to −6.0 pp, mean
ΔMaxDD +4.4 to +7.0 pp by variant). The clause is a one-way trade of return for depth in
every form tested — the queue's "volatility discount", not its "bear defence".

## 4. KEEP paths and rule 8

**4a 9/492, 4b 36/492**, all on U56 and B136, none on SMALL439. 11 de-lagged books clear a
path that LEVEL@0.20 does not on the same arm (H_KEEP PASS on the letter). Binding 4b legs
over all books: **CAGR 434**, H2 303, H1 278, OOS 261, DD 106 — the clause fails the CAGR
floor far more than any other bar, which is the same sentence as finding 3.

Rule 8 — (variant, q, dial) chosen on IS ≤ 2016-12-31 by IS Sharpe inside each panel ×
underlying, **2017+ read once, so 2018 / 2020 / 2022 were untouched by the selector**:

| panel | under | pick | OOS CAGR / Sharpe / MaxDD | own control OOS | RULES v2 OOS | SPY OOS | 2022 (gate / control) | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 | EWALL | ASYM q=0.30 qup=0.35 / M | 8.8% / **1.166** / −8.6% | 13.9% / 1.151 / −22.3% | 9.5% / 1.282 | 15.4% / 0.879 | −3.4% / −11.8% | no | no (**CAGR**) |
| U56 | MADG | ASYM q=0.30 qup=0.35 / M | 7.1% / 1.090 / −7.5% | 9.6% / 1.229 / −14.4% | 9.5% / 1.282 | 15.4% / 0.879 | −2.9% / −4.5% | no | no (CAGR) |
| B136 | EWALL | ASYM q=0.30 qup=0.35 / M | 6.8% / 0.955 / −11.8% | 13.8% / 1.109 / −25.0% | 8.0% / 1.119 | 15.5% / 0.882 | −6.4% / −7.1% | no | no (H2\|CAGR) |
| B136 | MADG | ASYM q=0.30 qup=0.35 / M | 5.3% / 0.894 / −9.3% | 8.3% / 1.096 / −15.7% | 8.0% / 1.119 | 15.5% / 0.882 | −4.5% / −6.2% | no | no (H2\|CAGR) |
| SMALL439 | EWALL | ASYM q=0.20 qup=0.65 / M | 5.3% / 0.524 / −21.6% | 9.7% / 0.623 / −34.7% | 3.8% / 0.568 | 15.5% / 0.882 | −0.1% / −14.6% | no | no (all five) |
| SMALL439 | MADG | ASYM q=0.20 qup=0.65 / M | 3.5% / 0.570 / −10.4% | 4.4% / 0.619 / −16.8% | 3.8% / 0.568 | 15.5% / 0.882 | −0.0% / −5.2% | no | no (H1\|H2\|OOS\|CAGR) |

**All six rule-8 picks fail both KEEP paths, and all six fail 4b on the CAGR floor.** Every
pick loses OOS CAGR to its own ungated control by 2.5–7.0 pp; five of six also lose OOS
Sharpe. The selector picks ASYM on every panel and every underlying, and ASYM is precisely the
variant that de-lags by staying in cash *longer*. **No KEEP-candidate; no memo; no RULES
proposal.**

## 5. H_REPRO — idea 48's published cell

Idea 48's book (U56, 12.2% / 1.131 / −12.7%, OOS 1.240, 2022 −9.0%) was a *ranked* grid book,
not a plain EWALL or MA-DG, so it is not reproduced here and no claim of reproduction is made.
The closest cells this script builds, printed for comparison:

| U56 arm | CAGR / Sharpe / MaxDD | 2022 |
|---|---|---|
| EWALL / W | 11.42% / 1.128 / −18.71% | −9.85% |
| EWALL / M | 12.15% / 1.202 / −18.31% | −14.63% |
| MADG / W | 8.03% / 1.150 / −13.20% | −4.84% |
| MADG / M | 8.75% / 1.216 / −8.89% | −6.01% |

The EWALL/W cell lands within **0.8 pp of CAGR and 0.003 of Sharpe** of the published pair and
**within 0.9 pp of the published 2022 return**, on a drawdown 6 pp deeper. The published 2022
figure of −9.0% is therefore a real feature of this gate family, not a one-book artefact.

## Answer to the queue, in its own words

The gate is a **volatility discount**, not a timing signal. Rate-of-change de-lagging (the
first instrument) is strictly worse than the gate it replaces; hysteresis re-entry (the second)
improves 2022 only by holding more cash in the fifteen years that are not 2022, and most of
even that improvement is the `q` dial rather than the de-lagging. If the breadth flag ever
enters RULES it belongs there as an **exposure clause**, priced against the CAGR floor, never
as a bear defence.

## Survivorship

SMALL439 is the current constituents of a sub-$2B screen (`data/SMALL_PANEL_README.md`); its
levels are optimistic and its CAGRs are not investable numbers. Every SMALL439 statement here
is a within-panel contrast (gated vs ungated, same names, same days), which survivorship bias
does not manufacture.
