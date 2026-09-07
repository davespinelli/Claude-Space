# Idea 375 — is the LOSS-SHARE statistic a usable PRE-SCREEN for gate ideas?

**Verdict: KILL as a pre-screen. It has ordering information out of corpus and NO sign skill and
almost no magnitude skill, and the zero-parameter mechanical bound out-ranks the fitted
regression that idea 350's headline implies. It survives only as a REPORT-ONLY ranking column.
No RULES change, no book promoted, no KEEP claimed; RULES.md, scan.py, bot.py and baseline.py
untouched. One 4b PARK by-product is filed below.**

Script: `2026-09-07_is-the-LOSS-SHARE-statistic-a-usable-PRE-SCREEN-for-gate-ideas_cloud.py`
Artefacts: `.grid.csv` (1134 overlay points), `.windows.csv` (126 controls), `.walkforward.csv`
(42 rule-8a cells), `.score.csv`, `.screen_wf.csv`, `.console.txt`. Every point is written; nothing
is filtered out of the CSVs.

## 0. Reproduction gates (all PASS, printed before any new number was read)

| gate | result |
|---|---|
| derived rung `r(c) = r(0) - turnover*c/1e4` vs `engine.backtest(cost_bps=25)` | max\|diff\| **0.000e+00** |
| idea 40/41 U56 TOP3 @10bps | 21.9%/1.04/-25.8% (H 1.01/1.06) vs published same — **PASS** |
| idea 40/41 U56 TOP5 @10bps | 16.5%/0.95/-21.6% vs published same — **PASS** |
| LIVE RULES v2 U56 @10bps | 8.66%/1.2056/-12.05% (1.2259/1.1908) vs published same — **PASS** |
| idea 350's committed grid, **rebuilt from source** | **486/486** rows matched; max\|d dDD_pp\| **1.78e-15**, dCAGR_pp 4.4e-16, CAGR 9.7e-17, Sharpe 2.2e-16, MaxDD 9.7e-17 |
| idea 350's committed windows | **54/54** peak dates and **54/54** trough dates identical; max\|d neg_share\| **5.6e-17 / 6.1e-17 / 8.3e-17** at B = 0.30/0.40/0.50 |

**Correction to the record.** Idea 350 publishes Spearman(neg_share, dMaxDD) = **-0.53 / -0.55 /
-0.40**. Re-derived from this rebuild — and, independently, from idea 350's OWN committed
`grid.csv` joined to its OWN `windows.csv` — the three numbers are **-0.528 / -0.682 / -0.293**
over 162 points each. Only the B=0.30 figure reproduces. The parent's `new_neg_share` column
(the statistic recomputed on the *gated* book's window) gives -0.100 / -0.195 / -0.386, and its
`loss_share` variant gives -0.747 / -0.736 / -0.343, so no column in its committed data yields
-0.55/-0.40. The headline's DIRECTION is reproducible; two of its three magnitudes are not.

## 1. Design

Fit on idea 350's books, score on books it never gated. **IN** = its 6 forms (EWALL, TOP3, TOP10,
TOP20, MAEW, RULESV2). **OUT** = 8 forms it never gated: TOP5, TOP40, IVOL (inverse-vol over all
names), LOWVOL20 (20 lowest-vol admitted names), MOM20 (raw 12-1 only), MAEW_RS (the MA gate
RESPREAD instead of de-grossed), V2B12 (RULES v2 at a 12% band), EWALL_M (EWALL monthly). Both
sets: 3 panels (U56 / B136 / SMALL439) x 3 rungs (0/10/25 bps) x the gate dial.
**IN 486 overlay points + 54 controls; OUT 648 + 72.**

**Exactly two tuned parameters, idea 350's own and not re-picked here:** breadth threshold
B ∈ {0.30, 0.40, 0.50}, gate depth d ∈ {0.25, 0.50, 1.00}. Reported, not tuned: form (14),
panel (3), rung (3), predictor (4).

**The four predictors were written down before any OUT number was read.** Target is
`dDD_pp = (|ctrl MaxDD| - |gated MaxDD|) * 100`, positive = the gate helped.

* **A NAIVE** — the IN-corpus mean (`+1.7791 pp`). The do-nothing control.
* **B SHARE** — OLS on IN: `dDD = +3.8865 - 3.5559 * neg_share`. The literal reading of the headline.
* **C SHARExD** — OLS on IN with depth and its interaction: `+6.8534 -7.5883*share -5.0861*d +6.9128*share*d`.
* **D BOUND** — `d * (1 - neg_share) * |ctrl MaxDD| * 100`, **zero fitted parameters**: the
  mechanical ceiling implied by idea 350's own argument.

## 2. The answer: the ordering transfers, the decision does not

Out of corpus (648 points), rank correlation of prediction with actual, sign accuracy, MAE, and
the skill score `1 - MAE/MAE_naive`:

| subset | n | A NAIVE | B SHARE | C SHARExD | D BOUND |
|---|---|---|---|---|---|
| OUT all — rho | 648 | — | **+0.276** | +0.292 | **+0.361** |
| OUT all — sign acc | 648 | **0.881** | 0.881 | 0.881 | 0.881 |
| OUT all — skill | 648 | 0.000 | **+0.048** | +0.029 | **-1.007** |
| OUT minus TOP5/TOP40 — rho | 486 | — | +0.362 | +0.228 | **+0.534** |
| OUT minus TOP5/TOP40 — skill | 486 | 0.000 | +0.085 | +0.060 | -0.624 |
| IN (reference) — rho / skill | 486 | — | +0.441 / +0.132 | +0.448 / +0.136 | +0.416 / -0.911 |

Three findings, and they decide the idea.

1. **The sign column is worthless.** `dDD_pp > 0` in **88.1%** of OUT points (80.9% of IN), so the
   constant "a breadth gate cuts a bit of drawdown" is right 0.881 of the time — and **every**
   fitted predictor scores *exactly* 0.881 too, because none of them ever predicts a negative
   dDD on this grid. The queue asked the statistic to "predict the sign and size of dDD". On
   sign it adds **nothing over a constant**.
2. **The size column adds ~5%.** MAE skill of the fitted regression is **+0.048** out of corpus
   (+0.085 dropping the two count-dial forms nearest idea 350's own set), against +0.132 in
   corpus — a two-thirds haircut. On **B136 it is negative (-0.007)**: worse than predicting the
   corpus mean. Per form it is negative on TOP5 (-0.337) and ranges +0.071..+0.126 elsewhere.
3. **The best RANKER is the one with no fitted parameters.** D BOUND beats both regressions on
   rank correlation (+0.361 all, +0.534 excluding TOP5/TOP40, +0.605 on U56) while being the
   *worst* magnitude estimate by a factor of two (skill -1.007) — it overstates because a gate
   never removes the whole addressable share. So the transferable content is the ORDERING
   `d * (1 - share) * |MaxDD|`, not idea 350's fitted slope.

Panel spread out of corpus: U56 rho +0.477 / skill +0.143, B136 +0.344 / **-0.007**, SMALL439
+0.056 / +0.040. Threshold spread: B=0.40 is the informative rung (rho +0.529), B=0.30 is not
(+0.172, skill +0.001).

## 3. Rule 8b — the screen walked forward (fit on 2008-2016 episodes, scored on 2017-2026)

Each control's binding episode is recomputed *inside* each window, with its own neg_share and its
own dDD; predictors are re-fitted on the 486 IN IS-window points and read once on the OOS window.
IS fit: `A +0.1337; B +2.3058 - 3.3351*share; C +3.8338 -3.5998*share -2.6194*d +0.4539*share*d`.

| subset | n | A NAIVE | B SHARE | C SHARExD | D BOUND |
|---|---|---|---|---|---|
| OUT OOS-window — rho | 648 | — | +0.288 | +0.075 | **+0.430** |
| OUT OOS-window — sign acc | 648 | **0.915** | 0.787 | 0.682 | 0.915 |
| OUT OOS-window — skill | 648 | 0.000 | +0.103 | +0.123 | -0.353 |
| OUT minus TOP5/TOP40 — rho / sign / skill | 486 | — / **0.940** / 0.000 | +0.320 / 0.860 / +0.110 | +0.002 / 0.681 / +0.123 | **+0.569** / 0.940 / -0.078 |

Walked forward the picture does not improve, it sharpens: the fitted predictors' **sign accuracy
falls BELOW the naive constant** (0.787 and 0.682 against 0.915) because the IS fit has a low
enough intercept to emit negative predictions that the OOS window does not deliver. Magnitude
skill is a real but small +0.10..+0.12. The zero-parameter bound is again the only thing whose
rank correlation *rises* out of sample (+0.430; +0.569 excluding the count dial).

## 4. Rule 8a — the book walked forward (menu incl. gate-OFF, chosen on IS Sharpe @10 bps)

| set | gate picked | mean OOS Sharpe (pick / control) | mean regret vs do-nothing | beats control | > RULES v2 OOS | > SPY OOS |
|---|---|---|---|---|---|---|
| IN | 11/18 | 0.8288 / 0.8639 | **+0.0351** | 5/18 | 2/18 | 10/18 |
| OUT | 18/24 | 0.8360 / 0.8745 | **+0.0385** | 8/24 | 2/24 | 14/24 |

The IS chooser arms the gate in 29 of 42 cells and **loses** 0.035-0.039 of OOS Sharpe on average
for doing so — another instance of the record's standing result that an IS chooser loses to doing
nothing. The loss is panel-concentrated: on SMALL439 the rule-8 pick's regret runs **+0.012 to
+0.426** (MOM20 0.2504 vs 0.6768 control) in 12/12 cells, while on U56 8 of 8 picks have negative
regret (the gate helps). The gate family is a large-cap instrument.

## 5. KEEP paths (evaluated at all 1134 overlay points and 126 controls)

| set | 4a overlays | 4b overlays | 4a controls | 4b controls | beats own numeraire |
|---|---|---|---|---|---|
| IN | 24/486 | 52/486 | 8/54 | 4/54 | 223/486 |
| OUT | 13/648 | **76/648** | 0/72 | 6/72 | 350/648 |

OUT 4b passes by rung **45 / 27 / 4** at 0 / 10 / 25 bps and by panel **U56 43, B136 33,
SMALL439 0** — the usual cost cliff and the usual panel ordering. Most passes sit on controls that
already clear 4b (MAEW_RS, TOP40), i.e. the gate is not the source.

**PARK by-product (not a KEEP).** `U56 / EWALL monthly / breadth gate B=0.40, depth 0.50` is the
one gate-CREATED 4b pass that holds at all three rungs, and its (B, d) cell is exactly what rule
8a's IS chooser picks:

| rung | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | control Sharpe / MaxDD | dDD | dCAGR |
|---|---|---|---|---|---|---|---|---|
| 0 bps | 12.11% | 1.2238 | -18.67% | 1.256 / 1.199 | 1.277 | 1.1375 / -22.27% | +3.61 pp | -1.22 pp |
| 10 bps | 11.87% | 1.2009 | -18.76% | 1.236 / 1.173 | **1.252** | 1.1340 / -22.28% | +3.52 pp | -1.42 pp |
| 25 bps | 11.50% | 1.1664 | -18.91% | 1.206 / 1.134 | 1.215 | 1.1288 / -22.28% | +3.38 pp | -1.72 pp |

against SPY 15.23% / 0.8890 / -33.72% (H1 0.957, H2 0.834, OOS 0.882) and the live RULES v2 book
8.66% / 1.2056 / -12.05% (1.2259 / 1.1908, OOS 1.285). It clears every 4b bar at 25 bps, which is
rare in the record — but it is **PARK, not KEEP**, for two stated reasons: the monthly-EWALL form
was selected from 8 OUT forms, which is a third dial this run did not pre-register; and it fails
4a on drawdown against the live book at every rung and does not beat it OOS. Its B136 sibling
fails 4b on the drawdown cap at all three rungs (-21.80% / -21.94% / -22.17% against a 20.23% cap),
so it is one-panel.

## 6. Caveats

(1) **Survivorship**: all three panels are current-constituent lists, so drawdown levels and CAGRs
are optimistic and 4b's DD cap and CAGR floor read against an inflated book; the screen scores are
rank/error statistics over books that all share the bias, which makes the screen half of this run
more robust than the KEEP half. SMALL439 drops the 44 tickers with `max_1d_move >= 1.0` and starts
2010-01-04, so its halves are not U56/B136's calendar halves. (2) "Out of corpus" means outside
*idea 350's* six forms; the record at large has gated top-n books at other n, so TOP5/TOP40 are the
weakest two OUT rows and every score above is reported with and without them. (3) The sample starts
2008 with a 260-bar warm-up, so the binding episode is 2020 or 2022 for nearly every control and the
OOS-window scores rest largely on ONE episode per book. (4) The overlay convention is idea 350's
verbatim (`rg = mult*rc - |d mult|*GROSS*c/1e4`), which re-scales the control's already-costed path;
it is kept unchanged so the two corpora are comparable, and the overstatement is bounded by
`mult*turnover*c/1e4`.

## 7. What should change

Nothing in RULES. The loss share should be published **beside** a gate result as a report-only
ranking column, in its zero-parameter form `d * (1 - share) * |MaxDD|` (the better ranker), never as
a gate on which ideas get run: on this evidence it would have mis-ordered the two count-dial forms,
added nothing to the sign, and saved roughly 5% of the error of guessing the corpus mean.
