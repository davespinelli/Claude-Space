# Idea 1745 (lane C, 2026-09-20) — is the BAND's RETURN COST predicted by its names' own WHIPSAW RATE?

**VERDICT: ANSWERED / KILL the whipsaw reading. No new book.** The crossing rate alone carries
**R² = +0.0056** of dCAGR pooled over 291 draws, its pooled rank-association with the OOS cost has
the **WRONG SIGN** (−0.4022 pooled vs +0.4679 within U56), the joint fit that looks strong is a
**near-collinear pair** (corr +0.9571, VIF 12.3 / 13.4) reducible to ONE difference column, and the
constructive claim — predict which universe a band is affordable on — **fails on every panel**
(leave-one-panel-out R² negative 3 of 3). Under rule 8 the price-only whipsaw chooser clears
**4a OOS 0 of 3 and 4b OOS 0 of 3**, and on U56 it lands BELOW the draw base rate.

Script: `research/backtests/2026-09-20_band-cagr-cost-vs-whipsaw-rate_C.py` (11/11 gates, 208s).
Grid: 291 draws × 4 bands × 4 cost rungs = 4,656 rows; 1,164 band books, each with its own
realised-gross-matched no-gate twin. **G12: reproduces idea 1632's committed grid cell for cell,
max |dev| 9.975e-17 on dCAGR and dSharpe over all 4,656 matched cells.**

## The object

Idea 1632 localised the band's whole panel dependence in the CAGR leg: at c = 0.03 the gate costs
U56 **−0.704 pp/yr**, SMALL **−1.393**, B136 **−1.972** (means over 49 / 145 / 97 draws), flat in
N inside each panel. Idea 1745 asked whether three PRICE-ONLY regressors — computable without any
backtest — replace the panel label:

| | U56 | B136 | SMALL |
|---|---|---|---|
| dCAGR (pp/yr) | −0.704 | −1.972 | −1.393 |
| GATEOUT (share of priced name-days out of band) | 0.2897 | 0.2905 | 0.4599 |
| XRATE (200d-MA crossings per name-year) | 1.814 | 2.097 | 2.935 |
| RECOV_21 (excess fwd return at a gate-out event) | −0.00142 | +0.00088 | +0.00413 |

Note the panel ordering already breaks: B136 is the MOST expensive panel but has nearly U56's
gate-out share and the LOWEST recovery-adjusted whipsaw of the two big panels.

## (1) The crossing rate on its own explains nothing

Pooled univariate R² at W = 21: **GATEOUT 0.0225, XRATE 0.0056, RECOV 0.0018** — all three
indistinguishable from zero against a 2,000× rung-block bootstrap (t = +0.85, −0.39, −0.30; the
bootstrap resamples whole (panel, N) rungs, because draws inside a rung share names by
construction). The panel LABEL alone carries **R² 0.3908**. The idea's headline regressor is the
weakest of the three.

## (2) The joint fit is one difference column, not a three-regressor law

GATEOUT + XRATE jointly give **R² 0.5900** with standardized betas **+1.820 / −1.794** that almost
exactly cancel — the textbook suppressor signature. Pooled **corr(GATEOUT, XRATE) = +0.9571**,
VIF **12.3 / 13.4**, and a SINGLE column `zGATEOUT − zXRATE` recovers **R² 0.5885 of the 0.5900**.
So pooled, the model has one degree of freedom, not two, and it is not "the whipsaw rate": it is
*time spent out of the band net of how often the gate changed its mind*.

Within panels the correlation collapses to +0.33 / +0.34 / +0.35 and the pair becomes genuinely
two-dimensional — but then the CARRIER ITSELF CHANGES PANEL BY PANEL, which is fatal to a law:

| single-regressor R² | U56 | B136 | SMALL |
|---|---|---|---|
| GATEOUT | **0.6150** | 0.1748 | 0.0202 |
| XRATE | 0.0232 | **0.2501** | **0.1879** |
| RECOV_21 | 0.0191 | 0.0865 | 0.0127 |

On U56 the cost is a GATE-OUT fact and the crossing rate is noise; on B136 and SMALL it is the
reverse. There is no single price-only statistic that plays the same role on all three.

## (3) In sample the regressors DO subsume the panel label — and it does not help

PANEL alone 0.3908 | GXR 0.6081 | GXR+PANEL 0.6365 — the label adds only **+0.0284** on top of the
regressors. That is the one result favourable to the idea, and it is in-sample only. The
constructive claim needs the fit to TRANSFER, and it does not:

**Leave-one-panel-out (fit on two panels, predict the third's draws), GXR at W = 21:**

| held out | predicted mean | true mean | bias | R² on held-out panel | corr |
|---|---|---|---|---|---|
| U56 | −1.114 | −0.704 | −0.410 | **−0.3157** | +0.5640 |
| B136 | −1.550 | −1.972 | +0.423 | **−0.3320** | +0.7560 |
| SMALL | −0.773 | −1.393 | +0.621 | **−1.2755** | +0.3922 |

Every held-out R² is NEGATIVE: the fit is worse than predicting the held-out panel's own mean.
With XRATE alone it is catastrophic (−6.40 / −6.07 / **−35.96**, level bias up to −3.57 pp). The
RANKING partially transfers (corr +0.39 to +0.76); the LEVEL does not. **The record cannot predict
a new universe's band affordability from these statistics — it still has to price it.**

## (4) Simpson's paradox on the crossing rate

IS crossing rate vs realised OOS dCAGR, Spearman: **U56 +0.4679, SMALL +0.1048, B136 −0.1550,
POOLED −0.4022.** The pooled association has the opposite sign to the majority of the within-panel
ones, because XRATE is itself a panel proxy. Any future memo quoting a pooled whipsaw coefficient
is quoting a panel label in disguise.

## (5) Capital arm — both KEEP paths at every cell, and rule 8

Over all **1,164** band books at 10 bps: **4a FULL 19, 4b FULL 5, 4a OOS 21, 4b OOS 13**; clearing
4b FULL *and* OOS: **3**, all on U56 at N = 20 (draws 3 and 18), replicating 1632 exactly.

**Rule 8** — dials (W, regressor set) chosen on 2009–2016 rows ONLY by IS adjusted R² (W = 21,
GXR, IS adjR² 0.5692; G6 re-verified on a tape truncated at 2016-12-31, max |dev| 0.000e+00), then
2017–2026 read ONCE:

| panel | chooser | OOS CAGR / Sharpe / MaxDD | 4a | 4b | draw base rate (mean OOS Sharpe, 4b OOS share) |
|---|---|---|---|---|---|
| U56 | **C_WHIP** | 6.63% / 0.9590 / −11.51% | ✗ | ✗ | 1.2102, 12.2% |
| U56 | C_XRATE | 8.73% / 1.2519 / −11.23% | ✗ | ✗ | " |
| U56 | C_SHARPE | 10.85% / 1.1995 / −14.75% | ✗ | **✓** | " |
| U56 | C_LIVE | 9.46% / 1.2769 / −12.05% | ✗ | ✗ | " |
| B136 | **C_WHIP** | 6.27% / 0.9067 / −10.17% | ✗ | ✗ | 1.0516, 0.0% |
| B136 | C_SHARPE | 6.23% / 0.9109 / −11.36% | ✗ | ✗ | " |
| SMALL | **C_WHIP** | 6.87% / 0.7252 / −17.78% | ✗ | ✗ | 0.4995, 0.0% |
| SMALL | C_SHARPE | 2.02% / 0.2709 / −21.74% | ✗ | ✗ | " |

Benchmarks OOS: live RULES v2 **9.46% / 1.2769 / −12.05%** (U56), 7.85% / 1.1019 / −12.24% (B136),
4.41% / 0.6473 / −12.48% (SMALL); SPY **15.26% / 0.8738 / −33.72%** on every panel.

**The whipsaw chooser has no capital value.** C_WHIP clears 4a OOS 0 of 3 and 4b OOS 0 of 3, and
on U56 its pick (OOS Sharpe 0.9590) sits BELOW the panel's own draw base rate of 1.2102 — picking
by predicted band cost is worse than picking a draw at random. C_XRATE is 0 of 3 as well. Every
non-passer fails on the same leg the record keeps hitting: the 4b CAGR floor.

**Incidental, and NOT a KEEP.** With the band fixed at the live rung c = 0.03, the ordinary
IS-Sharpe chooser reaches U56's draw-18 passer (OOS 10.85% / 1.1995 / −14.75%, 4b OOS ✓, 4b FULL ✓
at 11.07% / 1.2355 / −14.75%). This does not contradict idea 1632's 0-of-9: 1632's chooser ranged
over all four band rungs and landed elsewhere. One pick out of three panels, against a U56 4b-OOS
base rate of **12.2%**, is indistinguishable from the lottery — which is exactly what idea **1749**
is filed to settle. PARK it there; it is not evidence for a rules change.

## Residue (not a rules change; rule 6 — RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched)

1. The band's return cost is **not** a whipsaw-rate fact. Retire "crossing rate" as a candidate
   explanation of the −0.72 / −1.46 / −1.99 panel spread; it explains 0.6% of it and flips sign
   between the pooled and within-panel views.
2. Any pooled regression over these panels must publish **corr(GATEOUT, XRATE)** and the VIFs: at
   +0.9571 the two-regressor fit is one difference column, and its ±1.8 betas are not coefficients
   anyone may quote.
3. A regression that subsumes the panel label IN SAMPLE (label adds +0.0284) can still fail to
   transfer OUT of panel (held-out R² negative 3 of 3). In-sample dummy absorption is not evidence
   of a predictive law, and the record should stop treating it as one.

**Survivorship (rule 9):** U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
screen carried back to 2010, so every absolute level and every 4b pass count above is an upper
bound. The regression's LHS is a band-minus-twin contrast inside one draw — same names, same days,
same realised exposure — so the R² findings are first-order immune; the chooser levels are not.
