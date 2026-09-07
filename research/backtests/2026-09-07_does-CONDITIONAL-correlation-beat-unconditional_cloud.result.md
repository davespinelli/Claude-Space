# Idea 358 — does-CONDITIONAL-correlation-beat-unconditional (cloud, 2026-09-07)

**VERDICT: KILL — and the premise is falsified in the opposite direction.**
Crisis-day correlation is not a better design axis than full-window correlation. It is
*largely the same variable* (spearman +0.86 against it), it collapses under the *same*
own-Sharpe control by the *same* amount (26.2% of |rho| retained vs 26.0%), and out of
sample it **changes zero of 12 picks** — the crisis chooser and the unconditional chooser
select the identical (sleeve, f) in 12/12 cells for a mean OOS Sharpe identical to four
decimals. Separately, the queue's motivating premise — "a sleeve whose correlation FALLS in
crises" — describes **no sleeve on this ladder**: S4's correlation to the book *more than
triples* into the tail (0.099 → 0.334 at q=0.10, → 0.440 at q=0.05).

Script: `2026-09-07_does-CONDITIONAL-correlation-beat-unconditional_cloud.py` ·
console `.console.txt` · 660-point grid `.grid.csv` · `.axes.csv` · `.ladder.csv` ·
`.convexity.csv` · `.regression.csv` · `.monotonicity.csv` · `.walkforward.csv` ·
`.keeppaths.csv` · `.costladder.csv`.

**Tuned parameters: 2** — crisis-day quantile q ∈ {0.05, **0.10** (the queue's pre-registered
worst decile), 0.20} × f ∈ {0, .25, .50, .75, 1.00}. The 11-sleeve ladder is the regression's
x-axis, reported in full and never selected on outside rule 8, where selection is IS-only.
Books {v1, top20, ewall}, universes {u56, broad}, conventions {natural, matched} and the
0/5/10/15/20/25 bps ladder are reported controls. Cadence W, gross 0.75, 60d vol, (252,126,63)
lags, next-day execution, 10 bps headline — all at incumbent values.

**Survivorship:** both panels are current constituents, so equity levels are biased up. Every
sleeve asset is an ETF and is not exposed to it; the bias hits all arms identically.

## Reproduction gates — all exact

| gate | result |
|---|---|
| cost linearity vs a direct 10 bps run | max abs err **0.000e+00** PASS |
| matched cash sleeve is algebraically the book | Sharpe spread across f = **4.441e-16** PASS |
| idea 100 u56/top20 S4 f=0.25 natural | 10.2% / 1.14 / −14.2% / 1.11 / 1.18 — **as published** |
| idea 100 u56/top20 S4 f=0.25 matched | 10.8% / 1.14 / −14.6% / 1.13 / 1.16 — **exact** |
| idea 100 u56/top20 S4 f=0.50 natural | 7.7% / 1.19 / −10.0% / 1.10 / 1.27 — **exact** |
| S9 standalone (idea 26 control) | 5.0% / 0.87 / −10.1% / 0.76 / 0.98 — **exact** |
| idea 103's unconditional ladder | 0.0000 / 0.0988 / … / 0.7441 — **reproduced to 4 dp** |

Crisis days are taken over **non-zero** SPY rows only (12 u56 / 18 broad calendar-index zero
rows excluded — queue idea 38's weekend artefact is not a crash). q=0.10 → SPY ≤ −1.124%,
443 days, mean −2.043%.

## (1) Q1 — the crisis axis has LESS negative reach, not more

Mean corr(sleeve, book) over books × universes:

| sleeve | SCASH | S4 | S5r | S5f | S6r | S7r | S6f | S8r | S7f | S8f | S9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| unconditional | 0.000 | **0.099** | 0.310 | 0.467 | 0.469 | 0.586 | 0.658 | 0.693 | 0.718 | 0.743 | **0.744** |
| crisis q=0.10 | 0.000 | **0.334** | 0.423 | 0.515 | 0.494 | 0.548 | 0.609 | 0.611 | 0.639 | 0.654 | **0.647** |
| crisis q=0.05 | 0.000 | **0.440** | 0.526 | 0.604 | 0.587 | 0.626 | 0.679 | 0.674 | 0.697 | 0.706 | 0.697 |

The tail conditioning **compresses the ladder from both ends**: it pulls the diversifier end
*up* (S4 +0.235 at q=0.10) and the equity end *down* (S9 −0.097). Span falls from **0.744 to
0.654**. The single negative point in the entire record — S4 on broad/ewall, unconditional
**−0.0113** — becomes **+0.200** on the worst-decile days; the minimum crisis correlation over
all 60 non-cash points is **+0.200**, against **−0.011** unconditional. The axis the queue
wanted, one that can see a sleeve decorrelating in crises, does not exist because **no sleeve
here decorrelates in crises**. The two axes rank the ladder near-identically: spearman
**+0.816 / +0.861 / +0.937** at q = 0.05 / 0.10 / 0.20.

## (2) Q2 — the same regression, the same collapse

Idea 103's test, x-axis swapped, on the same 480 non-cash points:

| statistic / axis | raw slope | raw R² | raw rho | after own-Sharpe control: slope | R² | rho | \|rho\| retained |
|---|---|---|---|---|---|---|---|
| conv_per_pp / **unconditional** | −0.0724 | 0.1174 | **−0.3608** | −0.0074 | 0.0015 | **−0.0939** | 26.0% |
| conv_per_pp / **crisis q=0.10** | −0.1041 | 0.0875 | **−0.3246** | −0.0088 | 0.0008 | **−0.0849** | **26.2%** |
| conv_per_pp / crisis q=0.05 | −0.1201 | 0.0859 | −0.3221 | −0.0132 | 0.0013 | −0.0952 | 29.6% |
| conv_per_pp / crisis q=0.20 | −0.0983 | 0.0954 | −0.3398 | −0.0060 | 0.0004 | −0.0678 | 20.0% |

The crisis axis is **weaker raw** (rho −0.325 vs −0.361, R² 0.088 vs 0.117) and survives the
control by the same fraction. The confound is barely reduced: corr(sleeve's own standalone
Sharpe, axis) is **+0.746** unconditional and **+0.657** at q=0.10 — adding equity ETFs still
raises both the sleeve's own Sharpe and its crisis correlation together. Within-cell rho
(mean over 24 cells) is −0.713 unconditional vs −0.746 crisis, negative in 11/16 cells either
way: indistinguishable. Natural-only is the strongest scope for both (−0.420 → −0.208 vs
−0.403 → −0.227); matched-only kills both (−0.336 → −0.049 vs −0.267 → −0.010).

On idea 359's benchmark-free `raw_per_pp` neither axis has a stable sign: the crisis axis is
**+0.211 raw and −0.112 controlled**, the unconditional axis −0.104 raw and −0.483 controlled.
(The "retained" ratios >1 in the CSV for `raw_per_pp`/unconditional are an artefact of dividing
by a near-zero raw rho and carry no meaning; the sign instability is the reportable fact.)

## (3) Q3 — the capital test: the axis changes no decision

Three IS-only choosers over the same ladder, 2009-2016 → 2017-2026 untouched, 12 cells:

| chooser | mean OOS Sharpe | OOS CAGR | OOS MaxDD | vs no-sleeve ctrl | vs SPY | mean regret | 4b |
|---|---|---|---|---|---|---|---|
| CORR_UNCOND (lowest IS full-window corr, f=0.50) | 1.0766 | 7.24% | −10.6% | +0.157 (12/12) | +0.195 (10/12) | −0.191 | 0 |
| **CORR_CRISIS** (lowest IS worst-decile corr, f=0.50) | **1.0766** | 7.24% | −10.6% | +0.157 (12/12) | +0.195 (10/12) | −0.191 | 0 |
| IS_SHARPE (joint argmax over sleeve × f) | **1.1681** | 7.50% | −9.8% | +0.249 (12/12) | +0.286 (12/12) | **−0.099** | 0 |

**CRISIS minus UNCONDITIONAL, OOS Sharpe: mean +0.0000, wins 0/12, ties 12/12. The two
choosers picked different sleeves in 0 of 12 cells** — both land on S4 at f=0.50 everywhere,
because the compression in §1 preserves S4's rank at the bottom of both axes. A design
variable that reproduces the incumbent's every pick is not a new design variable. Both
correlation choosers are beaten by plain IS Sharpe (+0.091 mean OOS Sharpe, regret halved),
which is idea 103's conclusion restated: correlation, conditional or not, is not what should
be choosing the sleeve.

Reference rows (same days, 10 bps): SPY 15.23%/0.889/−33.7% (H 0.957/0.834, OOS 0.882);
RULES v2 live u56 8.66%/1.206/−12.1% (1.226/1.191, OOS 1.285), broad 8.03%/1.106/−12.2%
(1.229/0.984, OOS 1.119).

## (4) KEEP paths — reported, nothing selected on them

80 of 660 points clear **4b** (u56 24 matched / 15 natural; broad 23 matched / 18 natural);
**1 of 660 clears 4a** vs RULES v2. The 4b passes are concentrated at **f = 0.00 (the bare
book, 4 per sleeve) and f = 0.25**; no sleeve clears 4b at f ≥ 0.50 — the CAGR floor
(≥10.66%) binds, exactly as ideas 101/106 found. The cash null SCASH clears 4b at f = 0.25,
0.50 and 0.75, i.e. **de-grossing alone reproduces the pass**, so none of these 4b points
prices the sleeve. Best 4b point: u56/top20/matched S4 f=0.25, 10.83%/1.142/−14.6%
(1.127/1.159), OOS 12.08%/1.217/−14.6%, 9.24×/yr.

**No rule-8 pick clears 4b at any cost rung, 0 bps included.** 4a passes among the picks run
7/4/1/0/0/0 at 0/5/10/15/20/25 bps — dead by 15 bps.

## What this settles

1. **Idea 358 is answered NO.** Conditional correlation does not beat unconditional
   correlation as the sleeve design variable, on any of the three tests: it is not a distinct
   variable (rho +0.86), it does not survive the control that killed the incumbent axis
   (26.2% vs 26.0%), and it changes no out-of-sample pick (0/12).
2. **The premise behind it is false.** The record's "genuine diversifier" S4 is *more*
   correlated to the book in crises (0.099 → 0.334 → 0.440 as q tightens), not less. Any
   future wording that justifies a sleeve by crisis decorrelation must cite this table.
3. **Idea 103's conclusion is reinforced, not replaced.** The own-standalone-Sharpe confound
   is a property of the ladder's construction, not of how correlation is measured; swapping
   the axis does not escape it.
4. Idea 359's `raw_per_pp` proposal gains a datum: on this ladder it has **no stable sign**
   against either axis, which is a further argument against reporting either correlation
   statistic as a design number.
