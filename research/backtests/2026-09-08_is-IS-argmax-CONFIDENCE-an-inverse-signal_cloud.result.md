# Idea 417 — is IS-argmax CONFIDENCE an inverse signal?  (cloud, 2026-09-08)

**KILL of the inversion as a general property of the record, and a METHOD correction the
record needs. Idea 151's rho = −0.383 is a property of idea 94's own arm menu, not of
committed grids at large: the sign REVERSES out of that corpus, and the one configuration
that looks strongest in sample does not transfer under rule 8. No book promoted. RULES.md,
scan.py, bot.py, baseline.py untouched.**

Census: every `research/backtests/*.csv` carrying, per arm, a matched (IS_M, OOS_M) pair.
**1,531 files scanned → 74 ADMITTED** (1,111 no arm column, 270 no matched IS/OOS pair, 76
no usable cell), **3,825 distinct cells over 69 files, 9,141 (file, cell, metric) rows.**
Cells are discovered mechanically (a column is a cell label only if it is not a metric/mask
column, has 2–40 values, and is *not* functionally determined by the arm); every exclusion
is in `.ledger.csv`. Two tuned parameters — metric M ∈ {Sharpe, CAGR, MaxDD, Calmar} and
margin normalisation ∈ {raw, z, rng} — **all 12 grid points reported, in `.rhogrid.csv`.**

## 1. The sign reverses the moment you leave idea 94's corpus

Idea 151's own configuration (Sharpe, raw margin, d over the labelled control):

| scope | n cells | rho | t | p |
|---|---|---|---|---|
| LINEAGE (files 132/142/151/416) | 210 | **−0.211** | −3.08 | 0.0020 |
| OUT-OF-LINEAGE (65 other files) | 1,163 | **+0.098** | +3.34 | 0.0008 |
| ALL | 1,373 | +0.055 | +2.04 | 0.041 |

Same split on d over the menu mean (`d_rand`, defined on every cell): lineage −0.096
(p 0.16), out-of-lineage **+0.221 (t +13.2)**. Of the 9 available out-of-lineage grid
points, the most negative is −0.125 (MaxDD/rng) and three are ≥ +0.22. `OOS_Calmar` exists
nowhere in the record, so 3 of the 12 grid points are empty — a reportable coverage gap.

## 2. The degeneracy the estimand carries

`d_ctl` is **identically 0 whenever the IS-argmax IS the control** — true in 961 of 4,075
control-carrying rows (23.6%). Re-run on MOVED cells only (argmax ≠ control), Sharpe/z:
ALL +0.133 (t +4.20); lineage/raw **−0.150 (p 0.052)**, out-of-lineage/raw **+0.191
(t +5.52)**. The reversal survives the fix; idea 151's own number weakens under it.

## 3. …but there IS a real effect, and pooling hides it (the method correction)

Per file (Sharpe/z/`d_rand`, 56 files with ≥ 8 cells): **rho < 0 in 39 of 56 files,
median −0.111, mean −0.086** — while the *pooled* rho over the same rows is **+0.202**.
The pooled statistic is dominated by between-file scale differences, so it reverses the
within-file sign. Idea 151's four lineage files are −0.411 / −0.348 / −0.224 / −0.020.
**Any rho the record quotes over a pooled corpus should be quoted per file as well**; the
two disagree in sign here, on 9,141 rows.

## 4. RULE 8 — the inversion does not transfer

Choose the (metric, normalisation) on the first half of the record by parent-file date
(32 files / 4,122 rows, dated < 2026-09-06), read the second half untouched (37 files /
5,019 rows). Chosen: **Sharpe/z, IS rho −0.207 (t −8.09) → OOS rho −0.023 (t −1.07,
p 0.29)**. Every point is in `.walkforward.csv`; the three other negative IS points
(Sharpe/rng −0.175, CAGR/z −0.133, CAGR/rng −0.139) go to −0.022, **+0.286** and **+0.245** out of sample.
As a decision rule ("skip the argmax when the IS margin is wide", τ = IS-half median
margin_z), the OOS halves are indistinguishable: narrow +0.0480 vs wide +0.0448 on Sharpe,
and on CAGR wide is **better** (+0.0390 vs +0.0211) — the opposite of the queue's mechanism.

## 5. Fresh out-of-corpus replication on real prices (186 arm-rows, 6 cells)

31 arms (band × gross × cadence, plus an ungated control) on **u56 / broad136 / SMALL439**
× 10 and 25 bps, IS-chosen through 2016-12-31 and read once on 2017-01-01.. Per metric
(6 cells each, under-powered and labelled so): `d_rand` rho(z) **Sharpe −0.657, CAGR −0.371,
MaxDD +0.371, Calmar +0.429** — mixed, and the pooled-across-metric version (+0.38 / −0.75)
is the units artefact idea 400 flags, not evidence.

Levels, freshly computed (OOS 2017-01-01..2026-09-04): SPY **15.45% / 0.8820 / −33.72%**
(4b OOS bars: CAGR ≥ 10.82%, MaxDD ≥ −20.23%); RULES v2 @10 bps **9.53% / 1.2851 / −12.05%**
on u56, 7.98% / 1.1185 / −12.24% on broad136, 3.85% / 0.5680 / −14.68% on SMALL439.
The rule-8 IS-Sharpe argmax picks the ungated control in 4 of 6 cells; on u56 it picks
`band 0 / gross 1.00 / monthly` → **OOS 12.72% / 1.2750 / −15.49% @10 bps** (12.37% /
1.2434 / −15.54% @25), which clears **4b on the full sample and on the OOS window at both
rungs** but fails 4a against RULES v2. KEEP paths over the whole fresh grid: @10 bps 4a 8/93,
4b 13/93, 4b(OOS) 11/93, **BOTH 0/93**; @25 bps 3 / 9 / 9 / **0**. SMALL439 admits **0 of 62**
on 4b at every rung. **Nothing is promoted from this menu**: it has three dials, over
PROTOCOL's two-parameter cap, and exists here to supply arms for the rho, not as a book.
SURVIVORSHIP: `universe_broad.json` and the small panel are current constituents only
(data/SMALL_PANEL_README.md) — read the contrasts, not the levels.

## What this changes

Idea 151's inversion should be recorded as **corpus-local**: within a single arm menu the
IS-argmax margin is weakly, negatively related to the OOS premium (39 of 56 files), but the
effect is too small to survive rule 8 (−0.207 → −0.023) and reverses under pooling. The
usable output is the method note in §3 and the coverage gap in §1, not a selector rule.
Corroborates idea 416 (which measured −0.012 / −0.166 on its own two scopes) and closes the
queue's question against the queue's own hypothesis.
