# Idea 103 — correlation-as-the-sleeve-design-variable (cloud, 2026-09-07)

**VERDICT: SPLIT — the curve is monotone, and the design variable is FALSIFIED.**
Idea 100's convexity-per-pp does fall monotonically as sleeve-to-book correlation rises
(spearman −0.624 over 360 points, mean within-cell −0.713). But the ordering is not a fact
about diversification: adding equity ETFs raises the sleeve's *own standalone Sharpe*
(corr +0.746 with the correlation axis), and that term sits inside the linear blend the
statistic subtracts. **Control for it and the relationship collapses from spearman −0.624 to
−0.056 (R² 0.195 → 0.0029).** Correlation is not the sleeve design variable; the sleeve's own
Sharpe is the confound. KILL the variable, KEEP the ladder as a measurement.

Script: `2026-09-07_correlation-as-the-sleeve-design-variable_cloud.py` · console `.console.txt` ·
660-point grid `.grid.csv` · `.correlation.csv` · `.convexity.csv` · `.ladder.csv` ·
`.monotonicity.csv` · `.pathdep.csv` · `.vs_null.csv` · `.keeppaths.csv` · `.walkforward.csv`.

Tuned parameters: **2** (f ∈ {0, .25, .50, .75, 1.00} and the sleeve). Books, universes,
conventions, lookbacks, gross, cadence and costs are all held at the incumbents' values.

## Reproduction gates — all exact

| gate | result |
|---|---|
| matched cash sleeve is algebraically the book | Sharpe spread across f = **4.441e-16** PASS |
| idea 100 u56/top20 S4 f=0.25 natural | 10.2% / 1.14 / −14.2% / 1.11 / 1.18 — **published exactly** |
| idea 100 u56/top20 S4 f=0.25 matched | 10.8% / 1.14 / −14.6% / 1.13 / 1.16 — **exact** |
| idea 100 u56/top20 S4 f=0.50 natural | 7.7% / 1.19 / −10.0% / 1.10 / 1.27 — **exact** |
| S9 standalone (idea 26 / idea 100 control) | 5.0% / 0.87 / −10.1% / 0.76 / 0.98 — **exact** |

## (1) The ladder the queue asked for

Eleven sleeves: the cash null, S4 = TLT/GLD/DBC/UUP, and the five equity ETFs added back one
at a time along **two** paths (forward SPY→QQQ→IWM→EFA→EEM, reverse EEM→EFA→IWM→QQQ→SPY),
sharing both endpoints. Realised mean corr(sleeve, book):

| sleeve | SCASH | S4 | S5r | S5f | S6r | S7r | S6f | S8r | S7f | S8f | S9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mean corr | 0.000 | 0.099 | 0.309 | 0.467 | 0.469 | 0.586 | 0.658 | 0.693 | 0.718 | 0.743 | 0.744 |

Span **0.000 … 0.744**. The queue asked for ~−0.2 … +0.8; the negative end does not exist —
**no combination of these nine assets is negatively correlated with a long-equity trend book**,
S4 itself is only −0.011 (broad/ewall) to +0.212 (u56/v1). That is itself a finding: the record
has been calling S4 a "genuine diversifier" when its realised correlation is ~0.1, not negative.

## (2) The curve — monotone, as claimed

| sleeve | corr | dSharpe mean | dSharpe > 0 | dCAGR pp | **conv_per_pp (median)** |
|---|---|---|---|---|---|
| S4 | 0.099 | +0.265 | 36/36 | −3.19 | **0.0902** |
| S5r | 0.309 | +0.189 | 36/36 | −3.05 | 0.0672 |
| S5f | 0.467 | +0.109 | 36/36 | −2.66 | 0.0401 |
| S6r | 0.469 | +0.140 | 36/36 | −3.05 | 0.0505 |
| S7r | 0.586 | +0.107 | 36/36 | −2.90 | 0.0425 |
| S6f | 0.658 | +0.044 | 29/36 | −2.07 | 0.0195 |
| S8r | 0.693 | +0.066 | 36/36 | −2.38 | 0.0321 |
| S7f | 0.718 | +0.042 | 30/36 | −2.03 | 0.0187 |
| S8f | 0.743 | +0.048 | 35/36 | −2.15 | 0.0235 |
| S9 | 0.744 | +0.052 | 36/36 | −2.15 | **0.0309** |

Idea 100's two published points (0.090 vs 0.031) are the two ends of this ladder and reproduce
to the digit. **Regression of conv_per_pp on realised correlation: slope −0.0965, R² 0.195,
spearman −0.624** (n=360). Natural convention −0.725, matched −0.583; f=0.25/0.50/0.75 give
−0.595/−0.656/−0.691. Within each (universe, book, conv, f) cell the ladder is strictly
monotone-decreasing in **3 of 36** cells with a mean of 2.86 inversions out of 10 adjacent
pairs, but the mean within-cell spearman is **−0.713**. So: strongly decreasing, not strictly.

## (3) Path dependence — the curve is not a pure function of correlation

Forward vs reverse sleeve at matched asset count (144 paired points):

| pair | mean corr fwd | mean corr rev | Δcorr | Δconv_per_pp |
|---|---|---|---|---|
| S5f vs S5r | 0.467 | 0.309 | +0.158 | −0.0300 |
| S6f vs S6r | 0.658 | 0.469 | +0.189 | −0.0496 |
| S7f vs S7r | 0.718 | 0.586 | +0.132 | −0.0260 |
| S8f vs S8r | 0.743 | 0.693 | +0.050 | −0.0041 |

Sign agreement with the correlation story is **134/144 = 0.931**, but the paired regression of
Δconv on Δcorr has **R² 0.032** — the direction survives, the magnitude does not. Which ETF was
added matters beyond the correlation it produces.

## (4) THE MECHANISM — why the curve exists, and why it is not the queue's variable

`conv_per_pp` subtracts the linear blend `(1−f)·Sharpe(book) + f·Sharpe(sleeve)`. Its second
term is the sleeve's **own standalone Sharpe**, which rises as equity ETFs are added:

* corr(realised sleeve-book correlation, sleeve standalone Sharpe) = **+0.7459**
  (sleeve Sharpe range 0.488 … 1.098 across the ladder).
* conv_per_pp on corr — **raw: slope −0.0965, R² 0.1949, spearman −0.6244**;
  **after residualising on the sleeve's own standalone Sharpe: slope −0.0099, R² 0.0029,
  spearman −0.0557.** The relationship is 91% gone.
* `raw_per_pp` = (Sharpe(f) − Sharpe(0)) / pp of CAGR surrendered — the same economic
  quantity with no benchmark term — never had the ordering: **slope +0.2209, R² 0.0155,
  spearman −0.2400**.

**A sleeve looks less convex as it gets more equity-like mostly because the yardstick it is
measured against got longer, not because the blend delivers less Sharpe.** That is the answer
to "is the relationship monotone": yes in idea 100's statistic, and it is an artefact of that
statistic's normalisation.

## (5) Where does it stop paying? — against a properly defined null

`conv_per_pp` is **undefined** for the cash null (its f=1 endpoint is all cash: zero vol,
Sharpe NaN), stated here as a limit of the statistic, not a result. The null is therefore read
on `raw_per_pp`, and under the matched convention the cash null *is* the book (gate (a)), so
the null exists only on the natural side.

**The null itself: SCASH raw_per_pp mean −0.0001, range [−0.0005, +0.0004] over 18 cells** — an
independent confirmation of ideas 351/367's numeraire clause: a pure exposure cut has
essentially exactly zero Sharpe content. Every sleeve therefore clears a bar of ~0:

| corr bin | n | conv_per_pp | raw_per_pp | **beat rate vs null** | dSharpe |
|---|---|---|---|---|---|
| ≤ 0.10 | 6 | 0.0694 | 0.0270 | **1.000** | +0.297 |
| 0.10–0.25 | 15 | 0.0742 | 0.0409 | **1.000** | +0.219 |
| 0.25–0.40 | 18 | 0.0530 | 0.0366 | 0.889 | +0.162 |
| 0.40–0.55 | 36 | 0.0386 | 0.0449 | 0.889 | +0.113 |
| 0.55–0.70 | 51 | 0.0250 | 0.1207 | 0.824 | +0.064 |
| 0.70–1.00 | 54 | 0.0208 | 0.0445 | 0.722 | +0.056 |

So it never fully stops paying inside the range the ladder can reach: the beat rate declines
monotonically 1.00 → 0.72 but stays above ½ even at correlation 0.74. **There is no cutoff to
report.** The economically honest statement is that the sleeve beats pure de-grossing
everywhere on this ladder, by a margin that shrinks as it becomes more equity-like — and that
the *size* of that margin is not predicted by correlation once the sleeve's own Sharpe is out.

## KEEP paths (all 660 points reported; 510 distinct books after collapsing the shared f=0)

* **4a vs RULES v2 (live): 1 / 660** — one broad/matched point. The sleeve family does not beat
  the live book. (4a vs RULES v1, idea 100's comparand: 434/660 — the v1→v2 baseline change is
  what moved this, not the sleeve.)
* **4b vs SPY: 80/660 raw, 32/510 distinct.** All at f = 0.25 (plus the pure-book f = 0 rows).
  Best: u56 / S4 / top20 / matched / f=0.25 — CAGR 10.83%, Sharpe 1.1419, MaxDD −14.61%,
  halves 1.1274/1.1588, OOS Sharpe 1.2174, 9.24×/yr turnover. **This is idea 100's own standing
  point, unchanged**; nothing on the new ladder beats it, and the 4b pass count falls
  monotonically along the ladder, which is the one place the correlation ordering does survive.

## Rule 8 walk-forward — (sleeve, f) chosen on 2009-2016 IS Sharpe, 2017- read once

| universe | book | conv | IS pick | pick corr | OOS CAGR / Sharpe / MaxDD | no-sleeve control OOS Sharpe |
|---|---|---|---|---|---|---|
| u56 | top20 | natural | **S4@f=0.50** | 0.120 | 8.89% / **1.3081** / −9.97% | 1.1680 |
| u56 | ewall | natural | S4@f=0.50 | 0.107 | 7.40% / 1.2796 / −8.68% | 1.1133 |
| u56 | v1 | natural | S7f@f=1.00 | 0.722 | 6.01% / 1.1724 / −8.74% | 0.7471 |
| broad | ewall | natural | S4@f=0.50 | −0.011 | 7.05% / 1.2317 / −10.24% | 1.0191 |
| broad | top20 | natural | S4@f=0.50 | 0.035 | 8.05% / 1.0525 / −10.91% | 0.8919 |
| broad | v1 | natural | S6f@f=0.75 | 0.570 | 6.23% / 1.1301 / −7.86% | 0.5763 |

(the six matched-convention cells are in `.walkforward.csv`; same picks, 0.03–0.11 lower OOS Sharpe)

* **IS pick − no-sleeve control, OOS Sharpe: mean +0.2489, wins 12/12.** The sleeve is
  selectable, and the same margin holds against the cash null (12/12) — this replicates idea
  100's rule-8 finding on a ladder ten times wider.
* **vs SPY OOS Sharpe (0.8820): pick wins 12/12. vs RULES v2 OOS: 4/12.** Every pick gives up
  half of SPY's OOS CAGR (6–9% vs 15.45%) to do it.
* **The chooser does not prefer low correlation.** It picks S4 (corr ~0.1) in 8 of 12 cells and
  a high-correlation sleeve (S6f/S7f, corr 0.57–0.72) in 4 — on the v1 book it picks corr 0.72
  and still beats its control by +0.43 of OOS Sharpe. If correlation were the design variable
  this would not happen.

## Caveats

* Both panels are current constituents (survivorship; levels biased up). The nine sleeve ETFs
  are survivors by construction. No small-cap panel — the sleeve assets are not in it.
* Correlations are full-eval-window daily-return correlations, not conditional or rolling; a
  sleeve whose correlation *falls in crises* would be mismeasured by this axis, and the ladder
  cannot see that.
* The negative end of the queue's requested span (~−0.2) is unreachable with these assets, so
  the curve is fitted over 0.00–0.74 and says nothing about genuinely negative correlation.
