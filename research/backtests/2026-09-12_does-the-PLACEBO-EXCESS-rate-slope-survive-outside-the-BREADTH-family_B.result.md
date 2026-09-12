# Idea 606 — does the PLACEBO-EXCESS rate slope survive outside the BREADTH family? (lane B, 2026-09-12)

**ANSWERED = PARTLY, AND THE SPLIT IS CLEAN: THE *LEVEL* GENERALISES TO EVERY RISK-OFF STATE, THE
*SLOPE* IS MOSTLY A BREADTH FACT, AND THE WHOLE STATISTIC FAILS RULE 8.** A non-breadth 4b
KEEP-CANDIDATE falls out of the grid as a by-product and is memo'd separately. No RULES change;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

Script `research/backtests/2026-09-12_does-the-PLACEBO-EXCESS-rate-slope-survive-outside-the-BREADTH-family_B.py`

## What was run

Idea 602's machinery, rebuilt verbatim, with only the gate's **state** changed. Book: EWALL (every
name above its 200d with `vol20 < 0.60`, equal weight at `gross/n`, weekly). Gate: de-gross to
`1-depth` when the state is in its bad tail, cash never re-spread, switch cost on `|dm|`. Comparand:
the arm's **matched-mean-gross static twin**. Null: **BLOCK** (circular shift — exact firing rate,
exact run-length distribution, zero information) and **RAND** (iid days, exact count), 10 seeds each,
both sharing the arm's twin exactly.

**Four states, all from the panel's own closes:** BREADTH (602's, share above 200d), VOL20
(cross-sectional mean 20d vol), DISP (20d mean of the daily cross-sectional return std), CORR (20d
average pairwise correlation from the index-vs-name variance identity). **Both directions of every
state are always reported** — the low-tail and high-tail arms fire at the same rate with the same
clustering and opposite information, which makes the reversed arm a second, sharper placebo.

Tuned parameters (2): **state** and **rate bucket** (K ∈ {3,4,5,6,8} × equal-count and equal-width).
Reported axes, never selected on: level q 0.07/0.12/0.17, w 252/504/1008/2016, depth 0.25/0.50/1.00,
cadence D/W, gross 0.75/1.00, cost 0/10/25 bps, panel U56 / B136 / SMALL663.

**10,368 gated cells; 69,120 placebo cells** (10 seeds × 2 kinds × 3,456 head-rung arms).

## Reproduction gates — all six PASS

| | gate | result |
|---|---|---|
| G1 | derived cost rung `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(cost_bps=10)` | **0.000e+00** on all three panels |
| G2 | idea 84's ungated EWALL U56 g=0.85 @10bps (target 11.8% / 1.05 / −17.9% / H 1.07 / 1.04) | 11.75% / 1.046 / −17.89% / H 1.076 / 1.022 |
| G3 | idea 602's **committed** `.excess.csv` QROLL K=5 curve re-derived | **+0.0259 / +0.0446 / +0.0705 / +0.0695 / +0.1017**, share>0 **0.925 / 0.966 / 0.992 / 1.000 / 1.000** — exact |
| G4 | twin interpolation vs a true backtest at the exact g, 18 off-grid values | max abs return diff **3.67e-07**, max abs dSharpe **1.20e-07** |
| G5 | placebo matching identity over 6,912 arm × kind checks | **0.000e+00** on both the de-grossed day count and the mean multiplier |
| G6 | the fast Sharpe used on the 69k placebo cells vs `engine.metrics()["Sharpe"]` | **0.000e+00** |

## Q3 — the LEVEL generalises

Median excess of the real arm's dSharpe over its own rate/depth/gross/panel-matched BLOCK placebo,
and the share of arms that beat their own placebo (n = 432 per family):

| family | | median excess vs BLOCK | share > 0 | median excess vs RAND |
|---|---|---|---|---|
| BREADTH-LO | prior (602's) | **+0.0737** | 0.981 | +0.2259 |
| CORR-HI | prior | **+0.0420** | 0.861 | +0.1867 |
| DISP-HI | prior | **+0.0280** | 0.796 | +0.1940 |
| VOL20-HI | prior | **+0.0210** | 0.722 | +0.1820 |
| CORR-LO | reversed | +0.0270 | 0.845 | +0.2110 |
| BREADTH-HI | reversed | +0.0114 | 0.632 | +0.1801 |
| VOL20-LO | reversed | **−0.0128** | 0.361 | +0.1374 |
| DISP-LO | reversed | **−0.0204** | 0.162 | +0.1123 |

Every prior-direction state carries a positive placebo excess, so **a firing gate on vol, dispersion
or correlation earns something over an information-free gate at the identical rate — this is not a
breadth-only fact.** Its size is 2.6–3.5× smaller than breadth's. The reversal test splits: VOL20 and
DISP flip sign when the direction is reversed (as a real signal should), **CORR and BREADTH do not** —
CORR-LO keeps +0.0270 at share 0.845 — so on two of four states some of the excess is a property of
de-grossing on *any* tail of the state, not of the direction.

## Q2 — the SLOPE is mostly a breadth fact (the headline)

Pre-registered bar, idea 602's own: every adjacent bucket step non-decreasing **and**
Spearman(bucket, median excess) ≥ +0.80, applied at **every** K and **both** bucket units — 10 readings.

| family | | readings passed | median rho | median span |
|---|---|---|---|---|
| BREADTH-LO | prior (602's) | **6 of 10** | +1.000 | +0.0617 |
| DISP-HI | prior | **5 of 10** | +0.950 | +0.0345 |
| VOL20-HI | prior | 2 of 10 | +0.800 | +0.0184 |
| CORR-HI | prior | 2 of 10 | +0.171 | +0.0044 |
| BREADTH-HI | reversed | 1 of 10 | +0.686 | +0.0247 |
| CORR-LO / DISP-LO / VOL20-LO | reversed | **0 of 10** each | +0.450 / −1.000 / −0.750 | +0.0165 / −0.0373 / −0.0443 |

**No non-breadth family passes all ten readings; 3 of 6 pass at least one.** K=5 equal-count medians
(602's own reading): BREADTH-LO +0.0472 → +0.0575 → +0.0837 → +0.0793 → **+0.1078**; DISP-HI −0.0029 →
+0.0331 → +0.0092 → +0.0332 → **+0.0518**; VOL20-HI +0.0050 → … → +0.0259; CORR-HI rises +0.0257 →
+0.0582 then **collapses to −0.0067** in the top bucket (n=6 there — the rolling-quantile arms simply
do not reach high realised rates on that state).

**A second result the run did not go looking for: idea 602's own headline survives only 6 of the 10
readings.** Its committed number is one cell (K=5, equal-count) of a 10-cell table, and at K=3 and
under equal-width bucketing the curve is not monotone. The record should quote the reading beside the
slope.

## Q6 — rule 8, on the claim and on the books

**On the claim (the decisive leg).** Excess re-measured on 2009–2016 alone and read once on 2017+:

| family | median excess IS | median excess OOS | Spearman(IS, OOS) | sign agreement |
|---|---|---|---|---|
| BREADTH-LO | +0.0177 | **+0.1078** | +0.291 | 0.743 |
| CORR-HI | +0.0163 | +0.0639 | +0.263 | 0.625 |
| DISP-HI | +0.0073 | +0.0495 | **−0.295** | 0.431 |
| VOL20-HI | −0.0081 | +0.0450 | **−0.311** | 0.361 |

The rate-slope itself is IS +0.075 / OOS +0.368 for breadth, i.e. **the phenomenon lives almost
entirely in the second window**: the IS K=5 curve for BREADTH-LO is +0.0103 → +0.0384 (flat) against
OOS +0.0691 → **+0.1701**. An in-sample observer in 2016 would not have found this effect in any
family, and an arm's IS excess does not forecast its own OOS excess (best Spearman +0.291, negative in
three of eight families). **The statistic is descriptive, not a screening rule.**

**On the books.** 4a passes **11 of 10,368** cells (1 at the protocol rung); 4b passes 1,706 of 10,368
(372 of 3,456 at 10 bps, 0 at 25 bps / g=0.75). The rule-8 chooser (level and w fitted on IS Sharpe
2009–2016, per panel × family × depth × cadence × gross × rung) gives 864 picks: **4b full 19.3%, 4b
OOS 18.6%, 4a full 0.8%**. At the protocol rung 16 of 288 picks beat RULES v2's OOS Sharpe (12 of the
16 are CORR-HI) and 178 of 288 beat SPY's. SMALL663 contributes **zero** 4b passes at any rung.

## The gross-matched control — and the one book that survives it

Idea 596's bar, applied verbatim: a 4b pass its own matched-gross twin also earns is a statement about
exposure. Of the **372** arms passing 4b at 10 bps, **178 have a twin that passes 4b too**; 177 beat
their twin *and* have a twin 4b rejects; **164** of those also pass 4b inside the OOS window; **13** of
those are the rule-8 IS pick of their group; and **2** are still clean at 25 bps — both **CORR-HI on
B136**. (The ungated book itself: U56 g=1.00 fails 4b on drawdown at every rung; B136 g=0.75 *passes*
4b at 0 and 10 bps, which is why the matched-gross twin, not the ungated book, is the right control.)

**KEEP-CANDIDATE (path 4b only), memo `2026-09-12_b136-corr-hi-q017-w252-d050-D-g100_4b_B_MEMO.md`:**
B136, CORR-HI q0.17 w252, depth 0.50, daily gate, gross 1.00, @10 bps — full **14.02% / 1.1538 /
−15.11%** (H 1.2097 / 1.0973), OOS **14.29% / 1.2080 / −15.11%**; SPY 15.16% / 0.8861 / −33.72% (OOS
0.8767); RULES v2 7.98% / 1.0993 / −12.24% (OOS 1.1059); the same book **ungated** at gross 1.00 is
14.20% / **1.0211** / **−23.09%** and fails 4b on the DD cap. 4b holds at 0 / 5 / 10 / 25 bps and at
execution lag 1 / 2 / 3 days; it dies at 50 bps. **4a FAILS** (H1 1.2097 < 1.2348; MaxDD −15.11% vs
−12.24%). It is **post-hoc** — read off a grid built for another question — so it is queued as idea
814 for a pre-registered confirmation run and is not proposed for promotion.

## Caveats

1. **Survivorship.** All three panels are current-constituent lists; CAGR and drawdown levels are
   optimistic, the SPY bars included. Correlation measured on a survivor panel is itself optimistic:
   the names that died are the ones that would have co-moved hardest in 2020 and 2022.
2. **One binding episode.** Every panel's binding drawdown is 2020, so "the gate cuts the drawdown"
   rests on one event, exactly as idea 596 recorded.
3. **SMALL663 ≠ idea 602's SMALL439.** That cache was rebuilt, so G3 is priced on 602's committed rows
   rather than on a re-run of its small panel; U56 and B136 are membership-identical.
4. **The rolling-quantile gates do not fire at their nominal rate** (the 2026-09-10 result); every
   bucket here is cut on the *realised* rate, which is why CORR-HI's top bucket holds only 6 arms.
5. The 2 surviving cells are 2 of 3,456. That is a small number, and the run's own claim leg says the
   mechanism they embody is not out-of-sample stable.

## Files

`.cells.csv` (10,368 gated cells) · `.excess.csv` (3,456 arm-level placebo excesses) ·
`.slope.csv` (80 readings) · `.claim.csv` (rule 8 on the claim) · `.walkforward.csv` (864 rule-8
picks) · `.control.csv` (1,706 4b passers vs their own twin) · `.clean.csv` · `.nogate.csv` ·
`.gates.csv` · `.placebo.csv.gz` (69,120 placebo cells) · `.console.txt`
