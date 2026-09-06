# Idea 52 — small-cap-slower-trend (lane B, 2026-09-06)

**ANSWERED / mechanism CONFIRMED / KILL as a capital rule.** Whipsaw *is* the mechanism behind
idea 49's 5.4pp filter cost, and slowing the filter recovers essentially all of it — but only the
200d half, only when exposure is held constant, and the recovered book still beats the no-filter
control by nothing worth trading (+0.053 Sharpe at best) and fails both KEEP paths 0/72.

Script: `research/backtests/2026-09-06_small-cap-slower-trend_B.py`
(console `…_B.console.txt`; CSVs `…grid.csv`, `…decomp.csv`, `…flips.csv`, `…walkforward.csv`)

## Setup
439-name sub-$2B panel (`data/prices_small.csv.gz`, 483 in file, 44 dropped for
`max_1d_move >= 1.0`), 2011-01-13 → 2026-09-04, 10 bps, next-day execution, 75% gross.
Tuned parameters (exactly two): **band** b ∈ {0.00, 0.02, 0.03, 0.05, 0.08, 0.12} (the RULES v2
clause-2 hysteresis, `baseline.band_state`; b=0 is the hard gate) and **cadence** ∈ {W, M, Q}.
Reported, not tuned: gate form (MA = 200d band only; MAVOL = + vol20 < 0.60) and construction
(RESPREAD = gross/E_t over the gated-in names, always 75% invested — idea 49's f=1.00 form, so
the filter is pure selection; DEGROSS = gross/N per live name, gated-out weight to cash — the
RULES v2 form). All 72 points reported, each also at 0 bps.

**Reproduction of idea 49 is exact.** No-filter control EWall/W: 10.2% / 0.679 / −36.2% (idea 49:
10.2% / 0.677 / −36.2%). Its f=1.00 cell (RESPREAD/MAVOL/W/b=0.00) decomposes to **total 6.56pp,
timing 5.35pp, turnover 1.20pp** vs idea 49's 6.6 / 5.4 / 1.2.

## 1. The band is a near-pure churn dial, and the cost tracks the churn
| b | flips/name/yr (daily) | flips/name/yr (weekly-sampled) | mean % of panel IN | timing cost, pp of CAGR (MA/W/RESPREAD) |
|---|---|---|---|---|
| 0.00 | 8.91 | 4.17 | 49.6 | 2.82 |
| 0.02 | 4.11 | 3.36 | 49.5 | 2.25 |
| 0.03 | 3.27 | 2.91 | 49.5 | 2.25 |
| 0.05 | 2.34 | 2.24 | 49.6 | 1.41 |
| 0.08 | 1.67 | 1.65 | 50.2 | 1.42 |
| 0.12 | 1.20 | 1.20 | 51.3 | 0.69 |

A 7.4× cut in crossings moves average exposure by 1.8pp and removes 76% of the 200d gate's
timing cost. That is the whipsaw hypothesis, confirmed on its own terms.

Adding slower cadence takes it past zero: the MA-gate timing cost at 0 bps is
**+0.73/+0.93pp at b=0.00 (M/Q) and −0.43/−0.52pp at b=0.12/M and b=0.08/Q** — the slow filter
stops losing and marginally *earns*.

## 2. Two things the band does NOT fix
- **The vol20 half.** MAVOL timing cost stays **2.02–5.35pp** at every one of the 18 band×cadence
  cells, never within 2pp of zero. Slowing cannot rescue it; it is a selection cost, not churn.
  (Consistent with ideas 38 and 56: vol20 is the destroyer.)
- **De-grossing.** Under DEGROSS the cost is **4.78–8.33pp** and barely moves with the band
  (6.45 → 5.61pp across b at W). There the loss is *exposure* — ~50% cash in a panel that
  compounds at 10.4% — not churn, so a churn dial cannot buy it back.

The whipsaw recovery therefore exists in exactly one corner: 200d-only, exposure held constant.

## 3. The pre-registered test — does it BEAT the control?
Barely, and not usefully. **4 of 72 points** beat the matched-cadence no-filter control on *both*
CAGR and Sharpe, all RESPREAD/MA at slow cadence (M b=0.12; Q b=0.05/0.08/0.12).
13 of 72 beat it on Sharpe alone, 4 of 72 on CAGR alone.
Best margins: **dSharpe +0.053** (MA/M/b=0.12), **dCAGR +0.33pp** (MA/Q/b=0.08).
Range over the whole grid: RESPREAD/MA −0.176…+0.053 Sharpe, MAVOL −0.344…−0.076,
DEGROSS/MA −0.144…+0.031, DEGROSS/MAVOL −0.344…−0.106.
So the filter *merely stops losing*, exactly the weaker of the two outcomes the QUEUE named.

## 4. Verdicts — 0 of 72 on both paths
| | |
|---|---|
| 4a (vs RULES v2 on universe.json: 8.2% / 1.169 / −12.1%, halves 1.056/1.272) | **0 / 72** |
| 4b (vs SPY: 14.1% / 0.862 / −33.7%, bars H1>0.891, H2>0.858, OOS>0.882, MaxDD ≥ −20.2%, CAGR ≥ 9.89%) | **0 / 72** |

Failure modes: 41 fail all five, 26 fail H1/H2/OOS/CAGR, 5 fail H1/H2/OOS/DD. The **no-filter
control fails 4b too** (H1,H2,OOS,DD) — nothing on this panel is capital-worthy against SPY at
these bars, filtered or not.

Best cell in the grid (RESPREAD/MA/b=0.08/Q): **10.5% / 0.735 / −36.6%**, halves 0.725/0.760,
OOS 12.2% / 0.789 / −36.6%, 2.25× annual turnover.

## 5. Rule-8 walk-forward — (b, cadence) chosen on 2010–2016, 2017–2026 read once
| arm | S1 (IS Sharpe) | OOS CAGR / Sharpe / MaxDD | best OOS cell | regret | S2 (4b-aware) |
|---|---|---|---|---|---|
| RESPREAD MA | b=0.12/M | 10.7% / **0.716** / −37.6% | b=0.08/Q 0.789 | −0.072 | none (no IS point met the DD cap) |
| RESPREAD MAVOL | b=0.12/M | 6.5% / 0.508 / −38.4% | same | 0.000 | none |
| DEGROSS MA | b=0.05/M | 4.7% / 0.654 / −16.7% | same | 0.000 | b=0.05/M (same) |
| DEGROSS MAVOL | b=0.05/M | 2.0% / 0.410 / −14.7% | b=0.12/M 0.463 | −0.053 | b=0.05/M (same) |

OOS comparands: **SPY 15.45% / 0.882 / −33.7%**; **live book (RULES v2 on U56) 9.53% / 1.285 /
−12.1%**; no-filter controls 10.10%/0.637 (W), 9.71%/0.623 (M), 10.16%/0.647 (Q).
The walk-forward *does* select a band — the IS chooser lands on a large band and a slow cadence in
all four arms, and **3 of 6 picks beat the weekly no-filter control out of sample** — but every pick
loses to SPY OOS and every pick loses to the live book OOS. The dial walks forward; the book does not.

## 6. By-product worth keeping: slowing is what makes the filter survivable at small-cap costs
| point | CAGR@0 / @10 / @25 / @50 bps | Sharpe@0 / @10 / @25 / @50 |
|---|---|---|
| CONTROL EWall/W | 10.4 / 10.2 / 9.9 / 9.4% | 0.690 / 0.679 / 0.663 / 0.636 |
| RESPREAD/MAVOL/b=0.00/W (idea 49's cell) | 5.0 / 3.6 / 1.6 / **−1.8%** | 0.435 / 0.335 / 0.185 / **−0.064** |
| RESPREAD/MA/b=0.08/Q | 10.7 / 10.5 / 10.1 / 9.5% | 0.750 / 0.735 / 0.712 / **0.675** |
| DEGROSS/MA/b=0.05/M | 5.0 / 4.9 / 4.6 / 4.2% | 0.712 / 0.690 / 0.658 / 0.604 |

Annual turnover falls 13.4× → 2.2× from idea 49's cell to the slow one. The hard weekly filter goes
negative at 50 bps; the slow one still returns 9.5%. If any small-cap trend book is ever built here,
it should be banded and quarterly on cost grounds alone — independently of whether it beats anything.

## Caveats
SURVIVORSHIP: all 483 names trade through 2026-09-03 — a screen of *current* sub-$2B constituents,
no delistings. The bias inflates the **no-filter control** most (it holds the beaten-down names the
gate excludes), so it runs *against* the filter and softens this KILL. Idea 54 (2026-09-06, lane B)
bounded that correction: the gate's measured cost shrinks but never flips sign (0/36 and 0/36) at
plausible hazards. There is no IWM/IJR column offline, so SPY is the only 4b comparand and it
understates the passive small-cap alternative by ~3.4pp/yr (idea 54).

## Verdict
**ANSWERED — mechanism CONFIRMED, KILL as a rule.** Whipsaw explains idea 49's 5.4pp: an
exposure-neutral churn dial removes 76% of it at weekly cadence and all of it at monthly/quarterly.
But the recovery is confined to the 200d half under constant exposure, the best recovered book beats
the no-filter control by +0.053 Sharpe / +0.33pp CAGR, and **0 of 72 points pass 4a or 4b**. Not a
PARK: there is no candidate here to park, only a mechanism finding and a cost-side by-product.
