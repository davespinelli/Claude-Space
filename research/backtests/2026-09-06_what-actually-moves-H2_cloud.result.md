# Idea 70 — what-actually-moves-H2 (cloud, 2026-09-06)

**Verdict: ANSWERED / KILL of both mechanisms the queue named. The broad ranked book's H2
shortfall is **not** a handful of names — **0 of 128** single-name deletions lift H2 above SPY's,
the whole leave-one-out distribution is sd 0.0101 around a mean of +0.0002 — and it is **not**
mega-cap weight: the uncapped book holds only 14.5% in the PIT top-10 during H2, and capping
that weight moves H2 the **wrong way, monotonically** (0.8025 → 0.7372 as the cap goes 1.00 → 0),
clearing the bar at 0 of 5 cap levels. It is a **regime**, and a specific one: the book is a
defensive trend-follower that gives up return in melt-ups. Inside H2 it beats SPY by **+6.05
pp/yr while SPY is below its own 200d MA** (401 days) and loses **−7.31 pp/yr while SPY is in a
shallower-than-5% drawdown** (1,474 days). H2 happens to contain 2019, 2021 and 2023 — three
SPY melt-ups — and the book loses 13–15 pp in each. No KEEP-candidate, no RULES change; the
usable consequence is that **H2 Sharpe is a window statistic, not a book defect**, which is
idea 111's open question with a number attached.**

Script: `research/backtests/2026-09-06_what-actually-moves-H2_cloud.py`
Outputs: `.repro.csv`, `.names.csv` (128 leave-one-out runs), `.years.csv`, `.regimes.csv`,
`.sectors.csv`, `.grid.csv` (40 points), `.walkforward.csv`, `.console.txt`.
Book fixed, not tuned: `top20-200d`, gross 0.75, weekly, next-day, 10 bps (0 bps diagnostic).

---

## Leg A — reproduction

| convention | CAGR | Sharpe | MaxDD | H1 | **H2** | SPY H1 | SPY H2 | H2 gap |
|---|---|---|---|---|---|---|---|---|
| B136, all 136 tradable | 13.0% | 0.943 | −20.1% | 1.105 | **0.8025** | 0.957 | 0.834 | **−0.0315** |
| B136, stocks-only tradable | 13.7% | 0.937 | −27.6% | 1.101 | 0.7849 | 0.957 | 0.834 | −0.0492 |

Idea 66 published 0.814 / 0.837 (gap −0.023). The all-136 convention lands within **0.012** of
its book row and **0.003** of its SPY row; the *shortfall* reproduces under both conventions, the
*level* does not match to the third decimal (different tradable set / warm-up). Every number
below is measured on this run's book, not on the quoted one.

## Leg B — is it a handful of names? **No.**

H2 = 2017-11-03 … 2026-09-04 (2,220 days). 128 of 136 names carry H2 exposure: 84 net
contributors, 44 net detractors. **18** names produce 50% of the positive H2 P&L, **52** produce
90%. Biggest contributors NVDA +0.085, MU +0.059, SMH +0.050, LRCX +0.049, AVGO +0.049;
biggest detractors ZTS −0.025, ABBV −0.020, LOW −0.015, UNP −0.012, WFC −0.012.

The decisive test is not attribution but counterfactual: ban each name from eligibility over the
**whole** sample so the book reconstitutes, and re-measure H2.

| leave-one-out over 128 names | value |
|---|---|
| mean dH2 | **+0.0002** |
| sd dH2 | 0.0101 |
| best deletion | USO **+0.0291** → H2 0.8316 (still below SPY's 0.8340) |
| worst deletion | NVDA −0.0241 → H2 0.7784 |
| **deletions that clear the SPY H2 bar** | **0 of 128** |
| corr(H2 contribution, dH2) | −0.531 |

The best single deletion misses the bar by **0.0024**, and it is USO — an oil futures ETF whose
own H2 contribution is only −0.0096, i.e. the benefit is reconstitution (freeing a slot), not
the name's P&L. The correlation of −0.531 is moderate, not the near−1 a "few bad names" story
needs. **KILL of the handful-of-names mechanism.**

## Leg C — is it a regime? **Yes, and a legible one.**

Per calendar year inside H2 (book vs SPY total return):

| year | book | SPY | excess | | year | book | SPY | excess |
|---|---|---|---|---|---|---|---|---|
| 2017 (39d) | +1.4% | +4.1% | −2.7% | | 2022 | −9.8% | −18.2% | **+8.4%** |
| 2018 | +1.8% | −4.6% | **+6.4%** | | 2023 | +12.1% | +26.2% | **−14.1%** |
| 2019 | +16.5% | +31.2% | **−14.7%** | | 2024 | +20.6% | +24.9% | −4.3% |
| 2020 | +10.5% | +18.3% | −7.8% | | 2025 | +20.1% | +17.7% | +2.4% |
| 2021 | +15.6% | +28.7% | **−13.1%** | | 2026 (170d) | +14.6% | +13.5% | +1.1% |

The book beats SPY in **4 of 10** H2 years, and every win is a stress year (2018, 2022) or a
flat-to-choppy one (2025, 2026). Trailing-computable splits:

| state (inside H2) | days | book Sharpe | SPY Sharpe | book ann. | SPY ann. | **excess ann.** |
|---|---|---|---|---|---|---|
| SPY below its own 200d MA | 401 | −1.428 | −0.920 | −24.7% | −30.7% | **+6.05%** |
| SPY drawdown ≤ −5% | 746 | −0.676 | −0.519 | −11.6% | −14.5% | **+2.87%** |
| SPY 60d vol ≥ H2 median (0.140) | 1,110 | 0.597 | 0.783 | +9.3% | +18.7% | −9.32% |
| SPY 60d vol < H2 median | 1,110 | 1.035 | 1.062 | +14.4% | +12.9% | **+1.54%** |
| SPY above its own 200d MA | 1,819 | 1.410 | 1.896 | +19.9% | +26.0% | −6.08% |
| SPY drawdown > −5% | 1,474 | 1.776 | 2.603 | +23.8% | +31.1% | **−7.31%** |

Read together: the book earns its keep in *falling* markets and pays for it in *rising* ones,
and 1,819 of H2's 2,220 days are rising. Note the vol split runs the other way from the trend
split — the book is not simply short volatility; it is short *melt-up participation*. Dropping
the single worst year (2019) moves mean annual excess from −3.84% to −2.63%, so no one year
carries it either.

## Leg D — sector concentration of the H2 P&L (proxy)

No GICS map is cached, so each name is assigned point-in-time to the sector ETF it correlates
with most over a trailing 252d window, re-stamped every 63 days (37 stamps, 16 ETFs).

| assigned sector | H2 contribution | share of gross |
|---|---|---|
| SMH (semis) | +0.4575 | **36.3%** |
| XLK | +0.2872 | 22.8% |
| XLF | +0.1027 | 8.2% |
| XLY / XLC / XLI | +0.100 / +0.082 / +0.072 | 8.0 / 6.5 / 5.7% |
| KRE, XLU | −0.0162, −0.0223 | negative |

The three largest assigned blocks are **67.3%** of the gross H2 attribution and semis alone is
36.3%. So the book's H2 P&L *is* extremely concentrated — but concentrated in what **worked**.
That is the mirror image of the shortfall, not its cause: the book's problem in H2 is what it
failed to hold in melt-ups, not what it did hold. **CAVEAT: correlation proxy, not GICS.**

## Leg E — mega-cap weight, the actionable arm (40 points, all reported)

No shares-outstanding series is cached and the sandbox has no internet (ideas 195/265), so
MEGA10(t) = the 10 names with the highest cumulative return to date (idea 71's `PITGROW`
convention) — a **growth proxy for size, not market cap**.

Uncapped book's MEGA10 weight, H1 → H2: U56 0.328 → 0.274, **B136 0.237 → 0.145**,
BSTK100 0.250 → 0.161, SMALL 0.114 → 0.051. The broad book's mega weight *falls* by a third
into H2, so an over-weight story cannot even be posed there.

Capping it (B136, 10 bps) — the excess is re-allocated pro-rata to held non-MEGA10 names:

| cap | H2 | SPY H2 | Sharpe | CAGR | MaxDD | realised mega w. H2 |
|---|---|---|---|---|---|---|
| 0.00 | 0.7372 | 0.8340 | 0.866 | 11.6% | −19.9% | 0.003 |
| 0.10 | 0.7904 | 0.8340 | 0.900 | 12.2% | −20.1% | 0.084 |
| 0.25 | 0.8020 | 0.8340 | 0.918 | 12.6% | −20.1% | 0.142 |
| 0.50 | 0.8025 | 0.8340 | 0.932 | 12.8% | −20.1% | 0.145 |
| 1.00 (do nothing) | 0.8025 | 0.8340 | 0.943 | 13.0% | −20.1% | 0.145 |

**Monotone in the wrong direction, and 0 of 5 cap levels clear the H2 bar.** The lever the queue
proposed makes the thing it was meant to fix worse.

**Rule 8** (IS 2009-01-01..2016-12-31 chooses the cap, OOS 2017-01-01+ read once, 10 bps):
IS_ARGMAX picks the do-nothing cap in **3 of 4** panels and beats CAP_NONE out of sample by
**+0.0031 Sharpe / +0.06 pp CAGR** (better in 1 of 4 panels). OOS Sharpe by panel —
B136 0.884, BSTK100 0.891, U56 1.131, SMALL 0.466 — against RULES v1 (0.576 / 0.544 / 0.747 /
0.492) and SPY (0.882). The dial is inert; only SMALL picks a non-trivial cap and it is the
panel that loses to SPY and to RULES v1 everywhere anyway.

## KEEP paths

4a passes **0/20**, 4b passes **2/20** at 10 bps. Both 4b passes are U56 (caps 0.50 and 1.00,
12.7–12.8% / 1.049–1.064 / −18.3%, OOS 1.131) — the standing 2026-09-04 candidate's own
construction, unchanged by the cap. B136, BSTK100 and SMALL pass nothing at any cap.
**No KEEP-candidate, no memo, no RULES change.**

## Caveats

**SURVIVORSHIP.** `universe_broad.json`, the BSTK100 cut and the sub-$2B panel are CURRENT
constituents; names that died are absent. Every H2 attribution here is measured on known
survivors, and the PIT-growth mega proxy is biased hardest — it selects names that kept
compounding to today. 44 small-panel names with `max_1d_move >= 1.0` were dropped first.

**Window.** H1/H2 are PROTOCOL's own halves of the common sample, so H2 begins 2017-11-03 and
its first "year" is 39 days. That is a *different* split from rule 8's 2017-01-01 IS/OOS
boundary; the two are reported separately above and never mixed.

## What this leaves for the queue

The finding is a window property, not a book property, so the honest follow-ups are about the
window and about melt-up participation, not about more dials on this book:
* Does the H2 bar bind on *any* panel whose second half excludes 2019/2021/2023? (idea 111's
  year-composition question, now with the mechanism named.)
* Is the melt-up shortfall a property of the 200d gate specifically — i.e. does a book with no
  trend gate keep up in 2019/2021/2023 and still hold 2022?
* Should 4b's H2 clause be stated against a *regime-matched* benchmark rather than SPY's raw
  half, given that a trend book's H2 Sharpe is mechanically a function of how many melt-up
  years the half contains?
