# Idea 357 — is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable (cloud, 2026-09-07)

**SPLIT.** The regression question is **ANSWERED** — on a sleeve population that actually
decouples the two axes, **the sleeve's own Sharpe survives the correlation control and
correlation does not** (except among low-Sharpe sleeves). But own-Sharpe is **KILLED as a
design variable** out of sample: pre-registered, it is the *worst* of the three choosers.
Two corrections to the record fall out. No KEEP, one PARK by-product.

Script: `2026-09-07_is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable_cloud.py`
(+ `.console.txt`, `.grid.csv` 1260 rows, `.axes.csv`, `.bivariate.csv`, `.withincell.csv`,
`.strata.csv`, `.convexity.csv`, `.correlation.csv`, `.sleeves.csv`, `.keeppaths.csv`,
`.walkforward.csv`)

---

## 0. Why idea 103 could not answer its own question

Idea 103's ladder is one-dimensional: adding equity ETFs to S4 raises the sleeve's
correlation to the book **and** its own standalone Sharpe together. On such a ladder
"corr survives own-Sharpe" and "own-Sharpe survives corr" are the same regression run
twice, and whichever is residualised second wins. This run keeps `sleeve` as one tuned
parameter (with `f`, two in total) but widens its **population** from idea 103's 11 rungs to
21, adding ten single-asset sleeves fixed a priori by *where they sit in the plane*, not by
any result: GDX/USO/SLV/UNG (low corr, poor own Sharpe), TLT/GLD/SHY/DBC (low corr, varied
own Sharpe), HYG (mid), QQQ (high/high).

It worked as strata, which is what the test needs: mean own-Sharpe **span inside**
correlation quartiles is 1.19 / 0.51 / 0.30 / 0.26, and mean correlation span inside
own-Sharpe quartiles is 0.42 / 0.43 / 0.38 / 0.82. (The two axes are still correlated
overall — sleeve-level pearson +0.673 on the plane vs +0.696 on the ladder; it is the
non-degenerate strata, not a lower global correlation, that make the control possible.)

## 1. Reproduction gates — all pass

| gate | result |
|---|---|
| MATCHED cash sleeve is algebraically the book | max Sharpe spread across f = **4.441e-16** |
| idea 100/103 S4 f=0.25 natural | 10.2% / 1.14 / -14.2% / 1.11 / 1.18 — **published exactly** |
| idea 100/103 S4 f=0.25 matched | 10.8% / 1.14 / -14.6% / 1.13 / 1.16 — **published exactly** |
| idea 100/103 S4 f=0.50 natural | 7.7% / 1.19 / -10.0% / 1.10 / 1.27 — **published exactly** |
| idea 26/100 S9 f=1.00 natural | 5.0% / 0.87 / -10.1% / 0.76 / 0.98 — **published exactly** |
| idea 103 corr(corr, sleeve standalone Sharpe) | **+0.7459** (published +0.746) |
| idea 103 conv_per_pp chain | spearman **-0.6244 → -0.0557** (published -0.624 → -0.056) |

## 2. CORRECTION 1 — idea 103's collapse is a semi-partial, and it overstates by ~6x

Idea 103 residualised the *statistic only*, linearly, on the sleeve's standalone Sharpe and
then took a rank correlation against `corr`. That is a semi-partial. The proper partial
spearman (residualising **both** variables, on ranks) on its own 11-rung ladder is:

| statistic | raw spearman vs corr | idea 103's semi-partial | proper partial |
|---|---|---|---|
| conv_per_pp | -0.6244 | **-0.0557** | **-0.3390** |
| raw_per_pp | -0.2400 | -0.5046 | -0.4617 |

The record should read idea 103's "-0.056" as **-0.339**. Its *direction* (correlation is
substantially a proxy for the sleeve's own Sharpe) stands; its *magnitude* ("91% a proxy")
does not.

## 3. CORRECTION 2 — conv_per_pp is undefined well beyond the cash null

Idea 103 flagged that `conv_per_pp` is undefined for the cash sleeve. On this wider
population it also **explodes for any sleeve whose CAGR matches the book's**, because its
denominator (CAGR surrendered) passes through zero: **23 of 756** interior points surrender
< 0.05 pp, worst |conv_per_pp| = **5.4e7** (X_QQQ 2, S6f 1, S7f 1, X_SLV 1, SCASH 18). Every
pooled OLS on it returns slopes in the millions and R² ≈ 0.002, with or without the guard.
Within cells its orderings reverse sign across strata (own-Sharpe: +0.15/+0.46/**-0.39/-0.41**
across correlation quartiles; corr: -0.27/-0.67/**+0.11/+0.03** across own-Sharpe quartiles).
**On this population idea 100's statistic is not a usable yardstick at all** — direct support
for open idea 359's proposal to retire it record-wide in favour of `raw_per_pp`.

## 4. THE ANSWER — which variable survives the other

On the benchmark-free `raw_per_pp`, within each (universe, book, conv, f) cell — 36 cells,
SCASH dropped, so `f` and the book cannot confound either axis:

| population | rho_corr | rho_own | partial corr\|own | partial own\|corr | own>0 | partial own>0 |
|---|---|---|---|---|---|---|
| idea 103's 11 rungs | -0.018 | +0.561 | -0.345 | +0.807 | 36/36 | 36/36 |
| **this run's 21-sleeve plane** | **+0.440** | **+0.734** | **-0.022** | **+0.715** | **36/36** | **36/36** |
| plane, conv-defined subset | +0.439 | +0.731 | -0.022 | +0.712 | 36/36 | 36/36 |

Matched strata, no functional form (rho computed within cell, then averaged over bins):

* **own-Sharpe orders `raw_per_pp` inside every correlation quartile**: +0.667 / +0.775 /
  +0.651 / +0.901, positive in **137 of 138** cells.
* **correlation orders it inside only the bottom two own-Sharpe quartiles**: -0.858 / -0.322,
  then dies and reverses in the top two: **+0.069 / +0.075**. 47 of 144 positive.

Pooled on `dSharpe_raw` the same ordering holds with the plane's full n: joint OLS gives
own-Sharpe **t +27.4** against corr **t -5.89**, joint R² 0.585.

> **The sleeve's own Sharpe survives the correlation control everywhere. Correlation
> survives the own-Sharpe control only among sleeves that are individually poor** — where
> "low correlation" and "low Sharpe" are still hard to tell apart. Note the sign: on the
> plane, raw correlation runs the *wrong* way (+0.44, 3/36 cells negative) — the queue's
> "low correlation is good" ordering is not even present until own-Sharpe is controlled.

## 5. RULE 8 — and this is where own-Sharpe dies

Three pre-registered sleeve choosers, IS 2009-2016, OOS 2017-2026 read once, 12 cells
(2 universes x 3 books x 2 conventions). `f` = IS-Sharpe argmax given the chosen sleeve.

| chooser | OOS Sharpe | OOS CAGR | OOS MaxDD | beats no-sleeve ctrl | Δ vs ctrl | beats RULES v2 | beats SPY | 4b |
|---|---|---|---|---|---|---|---|---|
| S_OWN (highest IS own Sharpe) | **0.9006** | 6.97% | -14.61% | 4/12 | **-0.0186** | **0/12** | 7/12 | **0/12** |
| S_CORR (lowest IS correlation) | **1.0305** | 6.28% | -11.64% | 4/12 | +0.1113 | 2/12 | 9/12 | 0/12 |
| FREE (joint IS-Sharpe argmax) | 0.9202 | 8.73% | -17.12% | 4/12 | +0.0009 | 0/12 | 7/12 | 0/12 |

S_OWN beats S_CORR in **6/12** cells, mean gap **-0.1299**. The in-sample regression winner
is the out-of-sample loser.

**And S_CORR's apparent win is not diversification.** It picks a Treasury sleeve in 12/12 —
`X_SHY` (1-3y) in the four v1 cells, `X_TLT` in the other eight — and its **only two beats of
RULES v2 are the two `X_SHY@f=1.00` cells, whose OOS CAGR is 1.43% and 1.44%** at Sharpe
1.372/1.383. Holding a book almost entirely in short Treasuries is a constant exposure cut —
ideas 351/367's numeraire clause — wearing a correlation label. Its mean OOS CAGR (6.28%) is
the lowest of the three. (S_OWN, symmetrically, picks `X_HYG` in 12/12: the chooser collapses
to one asset either way.)

**Both candidate design variables therefore fail the only test that pays: neither clears 4b in
a single one of 12 walk-forward cells, and neither beats the free argmax by enough to justify
pre-registering it.**

## 6. KEEP paths (all 1260 points reported, none selected on)

**4a vs RULES v2: 1/1260. 4b: 137/1260 raw, 49/990 distinct** (f=0 collapsed across sleeves;
matched≡natural for the cash null). Every distinct 4b pass is at f=0.25 or f=0.50.

**PARK by-product, and it bears on open idea 105.** The best distinct 4b pass is a
**gold-only** sleeve, not the 4-asset macro sleeve:

| book | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe | turn/yr |
|---|---|---|---|---|---|---|
| **u56 top20 + 25% X_GLD, natural, 10 bps** | 11.56% | **1.1539** | -14.58% | 1.0733 / 1.2296 | **1.2844** | 8.23 |
| u56 top20 + 25% S4, matched (idea 103's standing best) | 10.83% | 1.1419 | -14.61% | 1.1274 / 1.1588 | 1.2174 | 9.24 |

PARK, not KEEP: it fails 4a, rule 8 never selects it (0/12), and it is one cell of a 990-point
scan. It is a *pre-registerable hypothesis for idea 105*, which asks exactly this question.

## Caveats

* **Survivorship**: both panels are current constituents (equity levels biased up); the sleeve
  ETFs are survivors by construction. No small-cap panel — the sleeve assets are not in it.
* The 21-sleeve population is wider than idea 103's but still a *choice*; it was fixed before
  the grid ran and no sleeve was dropped afterwards, but a different decoupling set could move
  the strata.
* Sections 4-5 disagree by construction: section 4 is an in-sample description of a statistic,
  section 5 is an out-of-sample selection test. The disagreement **is** the finding.
