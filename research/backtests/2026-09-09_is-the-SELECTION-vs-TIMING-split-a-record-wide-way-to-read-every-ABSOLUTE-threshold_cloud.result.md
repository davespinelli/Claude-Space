# Idea 578 — is the SELECTION-vs-TIMING split a record-wide way to read every ABSOLUTE threshold?

**cloud, 2026-09-09** · script `2026-09-09_is-the-SELECTION-vs-TIMING-split-a-record-wide-way-to-read-every-ABSOLUTE-threshold_cloud.py`

## VERDICT — **KILL of the reading, not of the arithmetic.** The split is not a discriminating instrument.

Idea 314's pivot (TOTAL = ABS − control; SELECTION = QTL@matched-rate − control; TIMING = the
residual) was applied unchanged to the record's other three absolute thresholds: the **200d
gate** (5 levels), the **breadth gate** (5 levels), the **ADV/dollar-volume floor** (5 levels,
SMALL439 only — `data/volume_small.csv` is the only cached share-volume series, so U56/B136
cannot carry that leg and were not faked). 146 books: 3 panels × 2 cadences × (3 families ×
5 levels × 2 arms) + 6 unclaused controls. EWALL, gross 0.75, DEGROSS, weekly/monthly,
10 bps, t+1 execution. Gates: **G1 1.4e-17**, **G2 max rate mismatch 0.0015 (bar 0.02)**,
**G3 identity 0.0e+00** — all PASS before any hypothesis was read.

## The three findings

**1. TIMING is a rounding error, everywhere.** Over the 69 material cells (|TOTAL| ≥ 0.50
pp/yr, 0 bps) the median |TOTAL| is **4.80 pp/yr** and the median |TIMING| is **0.72 pp/yr** —
**13.2%** of the total at the median. Every absolute threshold in the record costs, to first
order, exactly what a **frozen-rate** cross-sectional quantile of the same tightness costs.
The time-variation of the admission rate — the entire content of the word "absolute" — buys
and costs almost nothing.

**2. H_NAME FAILS, and it fails in the direction that kills the reading.** The queue's
question was which thresholds are selection and which are timing. The answer is *all three are
selection*, including the market-level one: median `sel_share` **MA200 +0.821 / ADV +1.000 /
BREADTH +0.807**. A gate with no cross-section at all still scores as SELECTION-dominated,
which means the statistic is not measuring cross-sectional name-picking; it is measuring
"whatever a matched-rate control also gets", i.e. the admission *rate*. `sel_share` is a
tightness statistic wearing a selection label.

**3. H_WIDE FAILS at 73.9% (bar 80%), and H_SIGN is CONFIRMED.** 18 of 69 material cells sit
outside [0,1] — **all 18 above 1** (max 1.308, min 1.007), i.e. TIMING is a small *positive*
offset there: the absolute level is mildly *better* than its frozen-rate twin. And the TIMING
leg's sign flips across panels in **5 of the 10** multi-panel cells, reproducing idea 314's
sign instability on three new families. A leg that is 13% of the total and whose sign is
panel-dependent is not a reportable decomposition.

## KEEP paths over all 146 books — and the one thing that is real

**4a 2/146. 4b 17/146.** All six unclaused controls fail 4b on **DD alone**
(B136/W control: 14.1% / 1.121 / −25.4%; SPY 15.2% / 0.889 / −33.7%, so the 0.60× cap is
−20.2%). Every 4b passer is a de-grossing clause buying that one leg. Binding-leg census over
all books: CAGR 112, H2 64, OOS 64, DD 62, H1 61.

**But the ABS arm is not what buys it.** On B136 the breadth gate passes 4b in 3 of its 10
(level × cadence) ABS cells and **6 of its 10 QTL cells**; on U56, 1 ABS vs 4 QTL, and the
U56 MA200 gate passes 4b in 0 ABS vs 3 QTL cells. The frozen-rate relative gate clears 4b
**twice as often** as the absolute one (13 QTL passes vs 4 ABS). Consistent with
finding 1: the operative object is the de-grossing rate, not the absolute level.

## Rule 8 (PROTOCOL 8) — (family, level) picked on IS ≤ 2016-12-31 by IS Sharpe among ABS books, 2017+ read once

| panel | pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | own control OOS | RULES v2 OOS | SPY OOS | full | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 | BREADTH@0.20 / M | 1.199 | **13.3% / 1.133 / −22.3%** | 13.9% / 1.151 / −22.3% | 9.5% / 1.282 / −12.1% | 15.2% / 0.88 / −33.7% | 13.0% / 1.159 / −22.3% (1.288/1.062) | no | no (DD) |
| B136 | BREADTH@0.20 / W | 1.212 | **12.1% / 1.081 / −19.5%** | 13.9% / 1.102 / −25.4% | 8.0% / 1.119 / −12.2% | 15.2% / 0.88 / −33.7% | 12.9% / 1.140 / −19.5% (1.308/0.987) | no | **yes** |
| SMALL439 | BREADTH@0.40 / W | 0.906 | **5.7% / 0.526 / −26.7%** | 10.1% / 0.637 / −36.2% | 3.8% / 0.568 / −14.7% | 15.2% / 0.88 / −33.7% | 6.9% / 0.655 / −26.7% (0.835/0.515) | no | no (H1\|H2\|OOS\|DD\|CAGR) |

**On every panel the rule-8 pick loses to its own unclaused control out of sample** on both
CAGR and Sharpe. The threshold's only OOS contribution is a shallower drawdown.

## PARK, not KEEP — the one 4b passer

`B136 / BREADTH ≥ 0.20 / weekly` clears 4b's letter (H1 1.308, H2 0.987, OOS 1.081, all >
SPY's 0.957/0.834/0.882; MaxDD −19.5% vs the −20.2% cap; CAGR 12.9% vs the 10.66% floor). It
is **PARKed, not proposed**, for three reasons stated plainly: its DD margin is **0.7 pp** on a
cap idea 321 has already flagged as one-episode; its own frozen-rate QTL twin passes 4b at the
same level (1.118 full / H2 0.999 against the ABS arm's 1.140 / 0.987); and it is
**beaten OOS by the control it is supposed to improve**. Exact RULES wording, if a Sunday
review ever wants it:

> **Clause B (breadth de-gross).** Let `E_t` be the fraction of priced universe names trading
> above their own 200-day simple moving average at close `t`. If `E_t < 0.20`, hold **no**
> equity for the following rebalance period; otherwise hold the book at its stated gross.
> `E_t` is evaluated at close `t` and applied at the next open. No other clause is conditioned
> on `E_t`.

## Survivorship

SMALL439 is the current constituents of a sub-$2B screen (`data/SMALL_PANEL_README.md`); its
levels are optimistic and its CAGRs are not investable numbers. Every SMALL439 statement here
is a within-panel contrast (clause vs its own unclaused control, same names, same days), which
survivorship bias does not manufacture. No cross-panel level claim is drawn from it.

## What the record should do with `sel_share`

Stop reading it as "cross-sectional name-picking vs market-state timing". On these three
families it is a monotone function of the clause's admission rate and nothing else. Any future
citation of idea 314's 65–74% should carry the counterpart measured here: on the *market-level*
breadth gate, which has no cross-section whatsoever, the same statistic reads **+0.807**.
