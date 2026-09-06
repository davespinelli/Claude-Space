# Idea 76 — holding-period-as-the-hidden-variable (cloud, 2026-09-06)

**Verdict: ANSWERED, and idea 76's thesis is a KILL as stated. "Holding period is the design
variable and turnover is only its shadow" is not testable the way the idea asks, because
(a) cost sensitivity is an ARITHMETIC IDENTITY in turnover and book vol — measured
`dSharpe/10bps` matches `-turnover×0.0010/σ` at Spearman −1.000, R² 1.0000, mean absolute
residual 0.00049 — and (b) `L` and turnover are the SAME DIAL, at Spearman(L, turnover)
= −0.989 and `turnover ≈ 2·gross/L` at R² 0.9812 over 52 book-cells. Adding `1/L` and
held-name vol on top of `turnover/vol` buys +0.0000 of R². The one channel where `L` could
have been independent — cadence — gives it +0.0179 of R² over turnover alone. Nothing new
is promoted.**

Script: `2026-09-06_holding-period-as-the-hidden-variable_cloud.py`
Primary cell 10 bps / weekly / next-day execution; common window 2011-01-13 → 2026-09-04
(15.64 yrs). 13 books × 4 panels (U56, ETF36, B136, SMALL) × 4 cost rungs × 3 cadences =
**624 backtests, all reported** in `.grid.csv`. Small panel drops the 44 tickers with
`max_1d_move >= 1.0` (439 tradable remain).

**Harness sanity — idea 9's three published anchors reproduce almost exactly:**

| book | this run (L / held-vol20) | idea 9 published |
|---|---|---|
| U56 / V1 | 15.7d / 0.146 | 16d / 0.144 |
| U56 / CAND20 | 39.6d / 0.226 | 39d / 0.228 |
| U56 / BAND3 | 168.8d / 0.193 | 170d / 0.189 |

## 1. P2 — `L` and turnover are one variable, not two

Over all 52 book-cells: **Spearman(L, annual turnover) = −0.989**; Spearman(1/L, turnover)
= +0.989; OLS `turnover ~ 2·gross/L` gives **R² = 0.9812** (mean absolute error 1.82×/yr,
concentrated in the NOGATE corner where L is the whole sample). Held-name vol20 is nearly
orthogonal to turnover (ρ +0.316). So the two candidate "design variables" are a
re-parameterisation of each other, and no test on this corpus can show one dominating.
`L` ranges 11.4d (SMALL/V1) to 3,855d (B136/NOGATE, one episode per name); turnover ranges
0.65×/yr to 33.3×/yr.

## 2. P1 — cost sensitivity is an identity, not a finding

`engine.backtest` charges `− turnover_t × bps/1e4` on a turnover path that does not depend
on the cost rung, so `dSharpe/10bps` is fixed by turnover and book vol before any book is
run. Measured against the prediction over 52 cells:

| test | result |
|---|---|
| Spearman(turnover/σ, dSharpe/10bps) | **−1.000** |
| \|measured − predicted\| Sharpe | mean **0.00049**, max 0.00103 |
| \|measured − predicted\| CAGR | mean 0.098pp, max 0.324pp (residual is compounding, CAGR is geometric) |
| R² dSharpe ~ turnover/σ | **1.0000** |
| R² dSharpe ~ 1/L + held-vol | 0.8626 |
| R² dSharpe ~ turnover/σ + 1/L + held-vol | 1.0000 (**incremental +0.0000**) |

Measured range **−0.281 .. −0.007 Sharpe per 10 bps**, wider on both sides than idea 68's
published −0.068 .. −0.099, because this corpus spans NOGATE (0.65×/yr) to SMALL/V1
(33.3×/yr). Held-name vol20 alone is uninformative about cost sensitivity (ρ +0.041):
it enters only through σ in the denominator, not as a separate channel.

## 3. Cadence — the one channel that is not turnover arithmetic

Cadence response is where `L` had a chance, and it very nearly does not take it:

| predictor | Spearman vs cadence Sharpe range | R² alone |
|---|---|---|
| turnover | +0.630 | 0.3578 |
| 1/L | +0.594 | 0.3297 |
| held-vol20 | −0.131 | — |
| turnover + 1/L | — | 0.3757 (**1/L incremental +0.0179**) |

Direction is right and monotone by `L` quartile — mean cadence Sharpe range 0.321 (Q1,
L≈17d) → 0.256 → 0.215 → **0.093** (Q4, L≈1215d) — so long-held books really are more
cadence-insensitive, which is idea 65's bar restated. But turnover explains it marginally
better than `L` does, so even here `L` is the shadow, not the substance.

The strongest practical form of the effect is the **cost × cadence interaction**: at 30 bps
there are **8 4b passes at monthly cadence, 0 at weekly and 0 at daily**. Lengthening the
holding period by slowing the cadence is what buys cost resilience — and it does so
entirely through turnover (U56/BAND3 4.68×/yr weekly → 3.06×/yr monthly).

## 4. Rule 8 walk-forward — IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once

Choosers pick one book per panel on IS only; pooled OOS, equal weight over 4 panels:

| rule | pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| **NOTHING** (U56/CAND20) | — | 14.5% | **1.131** | -18.3% |
| LONGEST (max IS episode length) | NOGATE 4/4 | 11.6% | 0.937 | -26.6% |
| LOWTURN (min IS turnover) | NOGATE 4/4 | 11.6% | 0.937 | -26.6% |
| ISSHARPE | MOM20/ABS/ABS/NOGATE | 10.6% | 0.882 | -23.1% |
| RANDOM (mean of 13) | — | 9.4% | 0.781 | -23.5% |
| LOWVOL (min IS held-name vol) | V1 4/4 | 6.3% | 0.584 | -21.7% |

SPY OOS 15.5% / 0.882 / -33.7%; RULES v1 OOS 7.7% / 0.747 / -13.8%.

**LONGEST and LOWTURN are byte-identical in 4/4 panels — both pick NOGATE everywhere.** The
two "rival" design variables cannot even be told apart by a chooser. Both beat a coin flip
(+0.156) and the incumbent IS-Sharpe selector (+0.055), but both lose to doing nothing by
−0.194. That is the **14th** instance in the record of a dial rule losing to the do-nothing
control. LOWVOL is the worst rule in the run, so held-name vol is not a selector either.

## 5. KEEP paths, all 624 points

**4a 89/624, 4b 91/624.** Primary cell (W/10bps): 4a **11/52**, 4b **14/52**.
SPY 14.1% / 0.862 / -33.7%, halves 0.891/0.858; 4b bars MaxDD ≤ 20.2%, CAGR ≥ 9.9%.

By cadence × cost (4a / 4b): D 12/13, 6/6, 2/1, 1/0 · W 16/17, 11/14, 9/6, 8/0 ·
M 10/10, 8/8, 4/8, **2/8**.

**Nothing new is promoted.** Every 4b pass is a book already in the record. The notable rows:

- **U56/BAND3 (idea 57's book) W/10bps: 10.9% / 1.120 / -15.1%, halves 1.015/1.217, OOS
  1.232, 4.68×/yr** — better than the standing candidate on Sharpe, MaxDD and OOS at less
  than half its turnover. It passes 4b at 0/10/20 bps weekly and at **all four rungs
  monthly**, but **fails 4b on ETF36 and SMALL at every rung**, so idea 58's open question
  (cross-universe cost wall) is confirmed, not closed: the wall is at 30 bps weekly,
  20 bps daily, and 2 of 4 panels at any rung.
- **B136/BAND3 W/10bps: 10.8% / 1.064 / -16.8%, OOS 1.071 — passes BOTH 4a and 4b**, as do
  B136/EWALL, B136/ABS, B136/CAND40 and B136/CAND60.
- Best 30-bps row anywhere: **U56/CAND20 monthly, 14.0% / 1.130 / -19.6%, halves
  1.082/1.179, OOS 1.233, 4.72×/yr** — the standing candidate surviving triple costs by
  being re-decided monthly. Consistent with idea 101/107; the extra 1.3pp of MaxDD versus
  weekly is inside the 20.2% cap but is idea 3's monthly drawdown tax showing up again.

## 6. What this means for the record

Report **turnover**, not holding period, as the cost-sensitivity variable — `dSharpe/10bps
= −turnover×0.0010/σ` is exact enough (max residual 0.001) to be published as a formula
rather than measured per book. Report **`L` only as a cadence-insensitivity proxy**, where it
is a slightly worse predictor than turnover itself. Do not use either as a book selector:
LONGEST and LOWTURN both lose to doing nothing by 0.194 of pooled OOS Sharpe.

**SURVIVORSHIP:** all panels are current constituents, one-directional, hardest on B136 and
SMALL. Holding-period statistics are especially exposed — a name that delisted has its
episode truncated in reality and does not appear here at all — so measured `L` is biased
**up**, most on the panels where the bias is worst. NOGATE's L is the sample length by
construction (censored share 1.000) and is included as the corpus's endpoint, not as a book.

Artefacts: `.grid.csv` (624), `.episodes.csv` (52), `.costsens.csv` (52), `.cadence.csv` (52),
`.walkforward.csv` (24), `.console.txt`.
