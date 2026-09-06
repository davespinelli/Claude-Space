# Idea 54 — delisting-aware-small-panel (lane B, 2026-09-06)

**Verdict: ANSWERED / BOUND. The record's small-cap conclusion SURVIVES the survivorship
bias. No new KEEP (4a 0/6, 4b 0/6). The delisted-ticker panel itself stays PARKed —
needs local/Actions data.**

Script `2026-09-06_delisting-aware-small-panel_B.py`; outputs `.part1.csv`,
`.part1_years.csv`, `.grid.csv`, `.books.csv`, `.contrast.csv`, `.walkforward.csv`,
`.log.txt`. 10 bps, next-day execution, weekly, 75% gross, deterministic seeds.
Panel = SMALL439 (`prices_small.csv` minus SPY minus README's 42 unrepaired
level-step tickers). Tuned parameters: 2 (hazard `h`, terminal loss `L`). Every grid
point reported.

## Part 1 — the bias, bounded against IWM (matched windows)

| window | SMALL439 EW | IWM | gap |
|---|---|---|---|
| full 2010-2026 | 14.54% / 0.735 / -46.0% | 11.11% / 0.587 / -41.1% | **+3.43pp/yr** |
| IS 2010-2016 | 16.87% / 0.913 | 12.91% / 0.692 | **+3.96pp/yr** |
| OOS 2017-2026 | 12.88% / 0.635 | 9.83% / 0.520 | **+3.05pp/yr** |

Panel beats IWM in **11 of 17 calendar years**; rolling-3y gap mean +3.58pp, median
+2.57pp, p10 **-1.11pp**, p90 +9.69pp, positive on 79.8% of days. The gap is
concentrated in 2010 (+11.8), 2013 (+14.3), 2020 (+20.8) and 2021 (+11.4) — the
junk-rally years, exactly where a screen of names that were *still alive in 2026* should
look best.

**Equal-weight-tilt control:** the panel is equal-weighted, IWM is cap-weighted, so the
gap could be an EW artefact. It is not — over the identical window RSP − SPY =
**-1.66pp/yr**, i.e. equal weighting *cost* return in this sample. If the small-cap EW
tilt has the same sign, +3.43pp is a **lower** bound on the composition gap.

**Two-sided caveat:** the screen drops names that grew *past* $2B as well as names that
died, so the failure-side bias alone is larger than +3.43pp, while the missing-winner
side pushes the other way. This is a bound, not an estimate.

## Part 2 — synthetic delisting overlay (24 grid points, 6 seeds each)

Names die at annual hazard `h` with terminal loss `L` on the death day, then go unpriced
(the stub sits in cash until the next rebalance and pays the engine's turnover cost).
Two pre-registered forms: **TREND** (deaths only below the 200d MA, rescaled to keep the
unconditional rate at `h` — the treatment, a trend filter can see these coming) and
**UNCOND** (uniform deaths — the placebo, invisible to any filter).

Closing the IS gap with delistings **alone** requires **h = 8%/yr at L = 0.50**, which
kills **266 of 439 names (61%) by 2026**. Realised US small-cap delisting-for-cause
rates are nearer 2-4%/yr, so the calibrated point is an **upper bound on the hazard**,
and the IWM gap is demonstrably not all survivorship: this panel is a sub-$2B *value
screen*, not the Russell 2000. At a plausible h = 3%/yr, L = 0.90 the overlay closes
2.51pp of the 3.96pp IS gap.

## Part 3 — does it overturn ideas 49/51? No.

The record's claim: the RULES v1 eligibility gate (above 200d **and** vol20 < 0.60)
destroys CAGR on sub-$2B names. On the clean panel at this run's construction
(EW-all-eligible, de-gross to cash, 75% gross, weekly):

**CLEAN dGATE = -9.24pp CAGR, -0.336 Sharpe, +24.25pp MaxDD.**

| h | L | dGATE TREND | dGATE UNCOND | contrast (t) | share of claim |
|---|---|---|---|---|---|
| 0.02 | 0.50 | -8.37pp | -8.76pp | +0.38pp (t 3.7) | 4.1% |
| 0.02 | 0.90 | -7.80pp | -8.38pp | +0.59pp (t 5.1) | 6.3% |
| 0.04 | 0.50 | -7.45pp | -8.28pp | +0.82pp (t 5.5) | 8.9% |
| 0.04 | 0.90 | -6.27pp | -7.55pp | +1.27pp (t 6.9) | 13.8% |
| 0.08 | 0.50 | -5.59pp | -7.45pp | +1.86pp (t 9.4) | 20.1% |
| 0.08 | 0.90 | -3.34pp | -5.97pp | +2.63pp (t 11.4) | 28.5% |

Both forms shrink the gate's measured cost, because the gate holds less gross and
absorbs less of the death drag — that movement is **not** foresight, which is what the
UNCOND placebo is for. The identifying quantity is TREND − UNCOND: **positive in 6/6
matched cells, +0.38 to +2.63pp, and at most 28.5% of the claim — only at the
implausible corner (61% of the panel dead, 90% loss).** At plausible hazards it recovers
4-14%. The sign of dGATE never flips: **0 of 36 TREND points and 0 of 36 UNCOND points**
have the gate adding CAGR. The gate also still buys drawdown everywhere (dMaxDD +24.0 to
+28.1pp), consistent with idea 56's reading of vol20 as a drawdown instrument.

## Rule 8 walk-forward (parameters on 2010-2016, 2017-2026 read once)

IS chooser (minimise |adjusted EW CAGR − IWM| on 2010-2016) picks **h=0.08, L=0.50** for
both forms.

| arm | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| SPY | 14.19% | 0.863 | -33.7% | 0.893/0.852 | 15.45% / 0.882 / -33.7% |
| RULES v2 baseline (clean panel) | 4.11% | 0.626 | -14.7% | 0.658/0.601 | 3.85% / 0.568 / -14.7% |
| EWall (clean) | 11.22% | 0.736 | -36.2% | 0.902/0.626 | 10.09% / 0.637 / -36.2% |
| GATED (clean) | 1.97% | 0.400 | -11.9% | 0.558/0.229 | 1.05% / 0.234 / -11.9% |
| EWall (TREND h=.08 L=.50) | 7.13% | 0.505 | -39.1% | 0.699/0.372 | 5.23% / 0.378 / -39.1% |
| GATED (TREND h=.08 L=.50) | 1.55% | 0.319 | -13.0% | 0.512/0.103 | 0.52% / 0.129 / -13.0% |
| EWall (UNCOND h=.08 L=.50) | 8.05% | 0.554 | -39.0% | 0.717/0.447 | 6.54% / 0.445 / -39.0% |
| GATED (UNCOND h=.08 L=.50) | 0.60% | 0.142 | -15.0% | 0.303/-0.040 | **-0.30%** / -0.038 / -14.3% |

**4a 0/6, 4b 0/6** (4a judged against the RULES v2 baseline re-run on the *matching*
adjusted panel). First-failing 4b bar: H1 in 5 of 6, H2 in 1. No small-panel book here
is capital-worthy under either path, before or after the adjustment.

## What this changes in the record

1. **Absolute** small-panel returns carry a survivorship premium of **~3.4pp/yr**
   (bounded, and probably understated on the failure side). Every LEADERBOARD row from
   `prices_small.csv` should be read with that haircut on its CAGR.
2. **Relative** comparisons at matched gross move by **≤2.63pp and never change sign**.
   The README's existing "relative comparisons only" caveat is the right one, and ideas
   39/49/50/51's gate-cost finding is not an artefact of the missing cohort.
3. The overlay only kills survivors. It cannot reproduce the dead names' actual paths or
   correlations, and it does not model the acquired names' takeover premium (which cuts
   the other way). The real delisted-ticker panel remains worth building.

**PARK (needs local/Actions data):** a panel with actual delisted/acquired tickers and
CRSP-style delisting returns. No internet in this sandbox; yfinance is never called.
