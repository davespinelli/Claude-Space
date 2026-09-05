# Idea 118 — why-the-DD-control-is-cheap-on-small-caps (cloud, 2026-09-05)

**Verdict: ANSWERED — the cheapness is a property of the PANEL's exchange rate and of the
control degenerating into de-grossing, not a property of the instrument. Idea 22's headline is
NOT reversed on small caps: the static-gross ladder beats the DD control at matched drawdown in
107 of 108 arms (36/36 on the small panel). KILL for reading idea 97's small-panel row as
"the cheapest instrument there".**

Script: `2026-09-05_why-ddctl-is-cheap-on-small_cloud.py` (imports idea 94's simulator
unchanged; idea 97's panel construction verbatim). 126 arm-points, 18 cells (3 panels x 3 books
x 2 costs), 25 depth-matched re-pricings, 6 vol-split re-pricings, all reported.
Two tuned parameters: D in {0.05,0.08,0.12}, k in {0.50,0.25}.

## 0. Reproduction is exact
All 36 committed `ddctl` rows of idea 97's `pricelist.csv` reproduce from the imported
simulator: max|d rate| 1.1e-16, max|d dCAGR| 8.9e-16, max|d dMaxDD| 1.8e-15, max|d lever| 9.0e-17.
Nothing below is a re-implementation.

## 1. H0 (units) — most of the gap is the panel's own exchange rate
`lever` (the static-gross ladder slope, pp of CAGR per pp of MaxDD from simply holding less) is
numerically the control's Calmar ratio in every cell (e.g. small/V1u/10bp: Calmar 0.207, lever
0.207). Panel means over the 108 sweep arms:

| panel | rate | lever | rate/lever | ctl Calmar | ctl MaxDD |
|---|---|---|---|---|---|
| u56 | 0.824 | 0.509 | 1.718 | 0.505 | -15.7%..-22.5% |
| broad | 0.547 | 0.416 | 1.360 | 0.412 | -23.5%..-28.9% |
| small | **0.324** | **0.278** | **1.153** | 0.277 | -30.8%..-44.1% |

Spearman(rate, lever) = **0.831** across 108 arms; Spearman(rate, control Calmar) = 0.831.
The panel spread in the raw price is 2.54x; in the normalised price 1.49x. The pre-registered
form of P0 ("normalisation removes >= half the gap", i.e. spread <= 1.27x) is **REFUTED**;
measured as excess over parity the normalisation removes 68% of it (1.54 -> 0.49). Either way
the ordering is unchanged and the direction is confirmed: a panel that pays little CAGR per pp
of drawdown from the de-grossing dial pays little for every instrument.

## 2. H1 (depth) — matching the control's drawdown INVERTS the ordering
Re-pricing each panel/book at a matched control MaxDD (static-gross bisection; targets
-15/-20/-25/-30%), the small panel stops being cheap and becomes the **dearest**:
u56 0.669, broad 0.431, **small 0.608** (unmatched: u56 0.824, broad 0.547, small 0.324).
The pre-registered P1 ("spread falls by more than half") is **REFUTED** (1.55x vs 2.54x), but
the cheapest panel moves from `small` to `broad`, which is the substantive claim: idea 97's
small-panel row is a reading of a -34% control, not of small caps. One depth-matched cell
(small/TOP20 at -20%) prices at 2.766 on a 1.4 pp denominator and should be ignored.

## 3. H2 (single-name vol) — refuted as posed, confirmed after normalisation
Small panel split at the median full-sample name vol20 (0.467; low half mean 0.379, high half
0.618; u56 0.247, broad 0.262 for reference). Raw price: low-vol half 0.228 vs high-vol 0.290,
so the **pre-registered P2 is REFUTED** — the high-vol half prices dearer. Normalised, the sign
flips (r/lev 1.752 low vs 0.966 high), because the low-vol half's own lever collapses (0.046 on
V1u). Name vol is not an independent channel; it moves the price through the lever again.

## 4. H3 (firing / absorbing state) — this is the mechanism, and it is a warning
The control is armed **74.2% of days on the small panel** vs 50.6% (u56) and 54.6% (broad),
with mean episode length 465 days, max 2003 days, and it **ends the sample still armed in 24 of
36 small-panel arms** (u56 11/36). Pooled Spearman(rate, armed fraction) = **-0.429** (P3
**CONFIRMED**), but within-panel it is ~0 (u56 +0.011, broad -0.247, small -0.183) — the pooled
number is the same between-panel depth/lever confound. The reading that survives: on the small
panel the DD control is armed three quarters of the time and mostly never resets, i.e. it *is*
a de-grossing, which is exactly why its price converges on the de-grossing lever (r/lev 1.15 on
small vs 1.72 on u56). This is idea 93's absorbing state, measured.

## 5. The decisive control — cheap is not the same as worth buying
At **matched drawdown**, the static-gross ladder delivers more CAGR than the DD arm in
**107 of 108** sweep arms, **36 of 36** on the small panel. Idea 97's `dominated` flag (rate >=
lever, a slope comparison) reports the opposite for 8 of 12 small cells; the slope test is the
wrong comparison because the ladder is not linear. Recommendation to idea 74's menu: quote the
matched-drawdown comparison, not the pp/pp ratio, and never quote a price without its panel's
lever beside it.

## 6. PROTOCOL 3/4/8
4a passes 40/126, 4b passes 3/126, **0 on the small panel** (P4 CONFIRMED). The three 4b passes
are u56/TOP20/10bp (D=0.08 and D=0.12, k=0.50) and broad/EWall/10bp (D=0.12, k=0.50) — all on
the large-cap panels and all at 10 bps only. Rule-8 walk-forward (D,k chosen on IS Sharpe only,
OOS read once): the pick's OOS Sharpe is **below SPY's 0.882 in 14 of 18 cells** (the four
exceptions are u56/TOP20/10bp 0.947, u56/EWall/10bp 1.207, broad/EWall 10bp 1.087 and 25bp
1.073), and **below the no-instrument control's own OOS Sharpe in 14 of 18** — the DD control
subtracts out-of-sample far more often than it adds. Small-panel picks: V1u 3.75%/0.444/-20.4%, TOP20 5.20%/0.550/-18.8%,
EWall 4.62%/0.644/-15.3%, against SPY OOS 15.45%/0.882/-33.7%.

## Survivorship
All three panels are current-constituent lists. The small panel's bias is the largest and
one-directional: the delisted, bankrupted and acquired names are missing and they are the
beaten-down cohort, so its drawdowns are shallower than the truth and its prices therefore
flattered. This run compares ratios inside each panel, which is the comparison the bias
distorts least; no level here is an achievable return.
