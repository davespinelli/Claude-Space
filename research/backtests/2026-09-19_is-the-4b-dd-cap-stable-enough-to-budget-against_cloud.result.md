# Idea 1450 (lane cloud, 2026-09-19) — ANSWERED / NO: the 4b bars are not stable enough to budget against

**Pre-registered reading, stated in the script before any number was read.** The cap is
"budgetable" only if (i) the margins the record quotes are LARGE against the cap's own rolling SD
and (ii) the licensed gross is the SAME at all four trailing windows. **Both legs fail.**

## 1. The bar moves more than the margins quoted against it

U56 tape, 0.60 × SPY MaxDD:

| window family | n | cap range | SD |
|---|---|---|---|
| rolling 3y | 176 | −4.41% … −20.23% | 4.69 pp |
| rolling 5y | 152 | −7.81% … −20.23% | 4.94 pp |
| rolling 8y | 116 | −11.16% … −20.23% | **4.17 pp** |
| rolling 10y | 92 | −11.61% … −20.23% | 3.08 pp |
| calendar years | 17 | −1.57% … −20.23% | 4.99 pp |

IS → OOS step: cap **−13.24% → −20.23% (−6.99 pp)**; on SMALL's tape **−11.16% → −20.23%
(−9.07 pp)**. Against that, the record's committed DD margins are small: the 2026-09-04
incumbent's +1.1028 pp and this ladder's live G = 0.75 (+8.18 pp) and G = 1.00 (+4.32 pp) are
**+1.96 and +1.04 SD_cap** respectively. A margin of one SD of its own bar is not a budget.

**The other bar moves too, and for this book it is the binding one.** The 4b CAGR floor
(0.70 × SPY CAGR) has SD **1.10 pp** over the same 116 windows (range 6.78% … 12.66%), and moved
10.47% → 10.68% IS → OOS. 1454's recommended G = 1.00 clears it by +0.95 pp full-sample =
**+0.86 SD_floor** — below one standard deviation of the bar it passes.

## 2. The license moves with the window, not with the book

The 2026-09-03 RECOMMENDATION's own rule ("smallest G whose MaxDD ≤ 60% of SPY's and CAGR ≥ 70%
of SPY's; if none, keep 75%"), run with rule and bar always reading the same trailing window
ending 2016-12-30, on the live RULES v2 shape at the live weekly cadence:

| trailing window | cap | floor | rungs clearing | licensed G | OOS CAGR / Sharpe / MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| 3y | −7.81% | 6.23% | 2/7 | **0.875** | 11.06% / 1.2766 / −13.99% | pass |
| 5y | −7.81% | 10.13% | 1/7 | **1.000** | 12.67% / 1.2762 / −15.91% | pass |
| 8y | −13.24% | 10.47% | 0/7 | **0.750** (fallback) | 9.46% / 1.2769 / −12.05% | fail |
| ALL-IS | −13.24% | 10.47% | 0/7 | **0.750** (fallback) | 9.46% / 1.2769 / −12.05% | fail |

Three distinct G from four windows on U56, two on B136, one on SMALL (fallback at 4 of 4).
**The decision swing is ±3.21 pp of OOS CAGR** between the 5y license (G = 1.00) and the
rule-8 license (G = 0.75) — on the same book, the same tape and the same rule, changed only by how
far back the bar was measured. Re-running the rule against **every** rolling 8y cap: U56 licenses
G = 0.875 at 55% of windows, G = 1.00 at **29%**, the 0.75 fallback at 16%; B136 licenses G = 1.00
at 60%; SMALL fires the fallback at **100%**.

## 3. What did NOT go wrong, stated as plainly as what did

The cap's movement in this window was **lenient, not punitive**: SPY drew down deeper out of
sample, so the cap widened and every licensed book held it (OOS DD margins +1.71 … +16.13 pp, cap
held at 12 of 12 panel×window licenses). Nothing breached. The damage is entirely in the
**license**, not in the realised risk — which is the failure mode that would not show up in any
backtest that reports only the book's own numbers.

## 4. Comparands and KEEP paths (rule 3, rule 4)

21 books published (3 panels × 7 G, weekly, 10 bps, t+1). **4a: 0 of 21 full and 0 OOS** — raising
gross deepens MaxDD against the live rules at an unchanged Sharpe (U56 Sharpe is 1.201 at all
seven rungs, to 3 dp). **4b: 2 of 21 full, 2 OOS, 1 both** — U56 G = 1.00 (full + OOS, replicating
1454 to 1.4e-05) and U56 G = 0.875 (OOS only). Nothing new is licensed here; this run re-prices
1454's own candidate, it does not propose another. SPY OOS 15.26% / 0.8738 / −33.72%; live RULES v2
OOS 9.46% / 1.2769 / −12.05% (U56 tape).

## 5. Caveats

**Survivorship (rule 9):** U56/B136 are current-constituent lists, SMALL a current sub-$2B screen
carried back to 2011 (665 names after dropping the 54 with max_1d_move ≥ 1.0 per
data/small_meta.csv), so every CAGR above is an upper bound. **The cap side is the one part of
this run the bias cannot touch — SPY is SPY — which is exactly why a bar that moves 4.17 pp is a
problem the survivorship caveat does not cover.** Two inherited conventions are flagged rather than
silently carried: (a) `rules_v2_weights` holds every column of the panel it is handed, so on SMALL
the baseline trades the benchmark SPY column too; (b) applying the protocol-mandated max_1d_move
filter to the panel the baseline itself trades moves the SMALL comparand from 4.66% / 0.7185 /
−12.48% (unfiltered) to 4.26% / 0.6597 / −14.16% (filtered, used here).

**Recommendation for the Sunday review (advisory, nothing enacted; PROTOCOL rule 6).** Do not read
1454's G = 1.00 pass as a 4b pass simpliciter. Quote it as: clears the DD cap by +1.04 SD_cap and
the CAGR floor by +0.86 SD_floor, on a rule whose licensed G is 1.00 at only 29% of rolling 8y
windows and 0.75 at the rule-8 window itself. If the review wants a G that survives the bar's own
movement, **G = 0.875 is the modal license (55% of windows)** and clears 4b OOS, missing the
full-sample CAGR floor by 0.51 pp.

Script `2026-09-19_is-the-4b-dd-cap-stable-enough-to-budget-against_cloud.py`; 21 books in
`.books.csv`, 1,582 cap windows in `.capwindows.csv`, 12 licenses in `.licenses.csv`, the 324-window
flip census in `.flipcensus.csv`, 8 gates all passing in `.gates.csv`.
