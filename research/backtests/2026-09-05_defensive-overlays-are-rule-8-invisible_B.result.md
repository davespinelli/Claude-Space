# Idea 99 — defensive-overlays-are-rule-8-invisible — **KILL** (lane B, 2026-09-05)

Script: `2026-09-05_defensive-overlays-are-rule-8-invisible_B.py`
Outputs: `.console.txt`, `.grid.csv` (208 points), `.deltas.csv` (164 non-null points), `.years.csv`, `.walkforward.csv`

## The claim under test
Idea 26: "IS (2009-2016) Sharpe monotone DECREASING in the sleeve fraction while OOS (2017-2026)
Sharpe is monotone INCREASING, so rule 8's selector rejects every defensive overlay by
construction." Statistic pre-registered before any number: `d(W,p) = Sharpe_W(p) − Sharpe_W(no-overlay)`
and the invisibility gap `G = d(IS) − d(OOS)`; G < 0 means rule 8 under-selects the overlay.
Grid: 6 leaderboard overlays (sleeve, band, breadth, stop, crypto, gross) × 2 books (top20, ewall)
× 2 universes (u56, broad) × 2 cost rungs (10, 25 bps), weekly, 44 cells.

## 1. The premise does not reproduce — 0/4 books
| book | IS Sharpe by sleeve fraction f ∈ {0,.25,.50,.75,1} | monotone ↓ | OOS Sharpe | monotone ↑ |
|---|---|---|---|---|
| u56/top20 | 1.012 1.060 **1.077** 0.938 0.271 | **no** | 1.156 1.208 **1.261** 1.243 0.728 | **no** |
| u56/ewall | 0.988 1.053 **1.077** 0.912 0.271 | **no** | 1.145 1.214 **1.278** 1.229 0.728 | **no** |
| broad/top20 | 1.025 1.079 **1.120** 1.023 0.274 | **no** | 0.885 0.937 1.006 **1.068** 0.729 | **no** |
| broad/ewall | 1.034 1.115 **1.167** 1.003 0.274 | **no** | 1.018 1.103 1.200 **1.207** 0.729 | **no** |

Both curves are hump-shaped with an **interior IS maximum at f = 0.50 in 4/4 books**. Rule 8 is not
blind to the sleeve: it picks f = 0.50 in **8/8 sleeve cells**, never the no-overlay point, and that
pick is the standing idea-101 candidate (u56/top20/10bps 12.3%/1.180/-14.3%, halves 1.161/1.200,
OOS 13.6%/1.261/-14.3% vs SPY 15.5%/0.882/-33.7% and RULES v1 7.2%/0.699/-13.8%; **4b pass**, and
4a on 3/4 books). Across all six grids rule 8 takes a **non-null** overlay in **32/44 cells**.

## 2. G < 0 is real, general, and has nothing to do with being defensive
Mean G = **−0.058**, negative in **82%** of 164 points. But the split by direction kills the label:

| class | n | mean d(IS) | mean d(OOS) | mean G | % G<0 |
|---|---|---|---|---|---|
| a-priori DEFENSIVE (sleeve/band/breadth/stop) | 128 | −0.052 | +0.014 | −0.067 | 88% |
| a-priori OFFENSIVE (crypto) | 12 | +0.052 | +0.130 | **−0.078** | **100%** |
| MEASURED offensive (higher mean gross) | 16 | +0.002 | +0.001 | +0.001 | 25% |

The crypto carve-out — the one unambiguously *offensive* overlay — has the **most negative G of any
grid**, 12/12 points. Per grid: sleeve −0.169, crypto −0.078, breadth −0.057, band −0.036,
stop −0.004, gross ±0.000. The gap is a property of the two windows, not of the instrument.

## 3. It is crisis density (T2), not in-sample-ness (T1)
T1 is mechanical (`G_rev ≡ −G`), so it carries no sign of its own; the content is *which window*.
T2, the pre-registered discriminator, regresses each of 17 calendar years' pooled mean d on that
year's SPY MaxDD (34 year-universes): **slope −0.73, r −0.41** (all overlays); **−1.03, r −0.44**
(defensive only). MaxDD is negative, so overlays pay *more* the deeper the year's drawdown. The
2×2 is decisive because the sign flips on year-badness *inside each window*, not across them:

| window | SPY MaxDD < −15% year | n year-universes | mean d (defensive) |
|---|---|---|---|
| IS 2009-2016 | yes (2010, 2011) | 4 | **+0.135** |
| IS 2009-2016 | no | 10 | −0.147 |
| OOS 2017-2026 | yes (2018, 2020, 2022, 2025) | 8 | **+0.047** |
| OOS 2017-2026 | no | 12 | −0.056 |

IS holds 2/7 bad years, OOS 4/10, and IS contains 2013 (SPY +32%, MaxDD −5.6%), the single worst
year for overlays in the sample (d = −0.36 u56, −0.42 broad). That composition *is* the gap. The
supporting split sweep agrees: G stays in [−0.080, −0.051] at all six pre-registered split dates,
because every split leaves 2013 before it and 2020/2022 after it.

## 4. The blindness costs ~nothing (PROTOCOL rule 8 walk-forward, params from 2009-2016 only)
| pick | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | mean regret | 4a | 4b | 4b(OOS-only) |
|---|---|---|---|---|---|---|---|
| rule 8 (argmax IS Sharpe) | 1.048 | 13.3% | −19.7% | −0.015 | 17/44 | **20/44** | 22/44 |
| no-overlay control | 0.993 | 12.4% | −19.2% | −0.070 | 18/44 | 19/44 | 19/44 |
| OOS-best ceiling (unattainable) | 1.063 | 13.0% | −18.7% | 0.000 | 21/44 | 15/44 | 21/44 |

Paired, rule 8 beats not-selecting in **30/44** cells and loses in 2 (+0.055 mean OOS Sharpe). The
ceiling is only **+0.015** OOS Sharpe above it, and the OOS-Sharpe-maximising point produces
**fewer** full-sample 4b passes (15) than rule 8 (20) — maximising OOS Sharpe breaks 4b's CAGR
floor. Reference: SPY 15.2%/0.889/-33.7% (OOS 0.882); RULES v1 u56 6.3%/0.649/-13.8% (OOS 0.699),
broad 6.4%/0.635/-21.2% (OOS 0.576).

## Verdict: KILL
No RULES change. The premise is false (0/4 monotonicity, rule 8 takes the defensive overlay in
32/44 cells), the measured gap is shared by the offensive overlay and explained by how many
drawdown years a window contains, and closing it perfectly would buy +0.015 OOS Sharpe while
*losing* five 4b passes. Rule 8 needs no defensive-overlay correction.

**Caveats.** Survivorship: both panels are current constituents. Crypto's IS window holds ~2 years
of BTC/ETH (reported in and out of every pooled statistic). Calendar-day index after 2014-09-17
(idea 38) hits every point identically. 2009 excluded from the year regression as a partial year.

Follow-ups filed: 111 (year-composition as a stated PROTOCOL caveat), 112 (2013 as a leave-one-year-out
target for the IS window), 113 (whether an overlay's crisis-beta is itself the pre-registrable selector).
