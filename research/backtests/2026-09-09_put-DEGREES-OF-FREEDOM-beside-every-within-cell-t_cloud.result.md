# Idea 512 — put DEGREES OF FREEDOM beside every within-cell t in the record (cloud, 2026-09-09)

**ANSWERED. The correction is REAL and it changes NOTHING that is published. Every one of the
302 restatable published within-cell claims over the record's own |t|>2 bar survives the
corrected dof — 302/302, and 106/107 of the within-OLS ones survive even the worst-case charge
the estimator's own `>= 4 rows per cell` rule allows — because the record's within-cell t's sit
a long way from the bar (|t| median 16.4, min 2.22) while its actual p/N is small (median
0.076, max 0.250). The dof charge that WOULD kill the median claim is p/N = 0.98. So the queue's
proposal is adopted as a REPORTING clause, not as a re-reading of the record.**

**Two things the back-fill found that matter more than the charge itself.** (1) **The record
cannot restate most of its own t's: 1,192 of the 1,510 published t rows in its within-transform
scripts are not restatable at all** — 1,174 do not publish `p`, and for 1,172 the CSV header
does not even say which estimator the column is. (2) **A false-positive rate 2.5–5.7x nominal
is sitting in the record's cluster-robust arm, not in its dof** — `within_cell_fit` divides by
a Liang-Zeger meat and refers the result to a NORMAL, which at the small cluster counts the
record actually uses (G = 3–10) clears |t|>2 on 8.3–25.1% of INDEPENDENT draws, against 4.3–9.5%
for the naive dof the queue asked about. CR1 + t(G-1) restores 1.8–5.1%.

No RULES change, no KEEP-candidate, no memo. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched.

Script `2026-09-09_put-DEGREES-OF-FREEDOM-beside-every-within-cell-t_cloud.py`; console
`.console.txt`; CSVs `.census.csv` (113 t-carrying CSVs), `.backfill.csv` (1,510 rows),
`.montecarlo.csv` (9 rungs x 2 draw counts), `.withint.csv`, `.walkforward.csv`,
`.keeppaths.csv` (396 arms). Runtime 610 s, deterministic, no network.

---

## The clause this run proposes

> **PROTOCOL addendum (reporting, not a bar).** Any published t computed after a cell transform
> must carry four columns beside it: `estimator` (which t it is), `N` (rows entering the fit),
> `p` (parameters the transform absorbs — cells, dummies, per-name effects) and `dof` (the
> reference the p-value used). A t whose `estimator` is not stated cannot be restated by anyone,
> including its own author. Where the SE is cluster-robust, `G` is required too, and the
> reference is t(G-1), not the normal.

The three numbers are cheap to emit — every one of them is already a local variable inside the
estimator that produced the t — and without them a reader cannot tell a t(N-2) from a t(N-p-1)
from a t over `cells` cell-level statistics, which on this record differ by up to a factor of
1.15 in scale and by an unbounded amount in reference distribution.

## (1) CENSUS — what the record publishes beside a t

113 committed CSVs under `research/` carry a t-statistic column. 11 come from a script that
demeans both sides by a cell — the Frisch-Waugh family idea 483 named. Of those 11:

| published beside the t | files |
|---|---|
| N | 9 / 11 |
| p (cells) | 4 / 11 |
| G (clusters) | 2 / 11 |
| N **and** p — the pair needed to restate the dof | **3 / 11** |

At the row level, 1,510 published t values, split by what estimator the column actually is
(read off the producing source, line numbers committed in the script's `EST_MAP`):

| estimator | rows | restatable | N published | p published | G published |
|---|---|---|---|---|---|
| WITHIN_OLS (cell-demeaned slope) | 116 | **116** | 116 | 116 | 47 |
| CELL_AGG (t over per-cell statistics) | 202 | **202** | 202 | 202 | 136 |
| WITHIN_MEAN (one-sample t on demeaned values) | 18 | 0 | 0 | 18 | 0 |
| POOLED (ordinary multi-parameter OLS) | 2 | 0 | 2 | 0 | 0 |
| UNMAPPED (header does not identify the estimator) | 1 172 | 0 | 1 166 | 0 | 0 |

**1,192 of 1,510 are not restatable**: 1,174 do not publish p, and 1,172 do not say which
estimator they are. This is the finding the queue's proposal is for.

**A concrete instance of the ambiguity, found while back-filling.** In
`2026-09-08_why-does-the-DD-ranking-die-on-U56_C.py`, `transfer_row()` builds its row by
`r.update(within_cell_fit(...))` and then `r.update(per_cell_slopes(...))` — and both return a
key named `cells`. The second overwrites the first, so the `cells` published beside that file's
within-OLS `t` belongs to a *different* estimator in the same row (per-cell slopes keeps only
cells with >= 8 rows and non-zero variance; the within fit keeps every cell with >= 4). The 44
affected rows are flagged `p_ambiguous` in `.backfill.csv` and are restated at their worst case
instead. They survive it.

## (2) BACK-FILL — the restatement, and why it does not move

Over the 318 restatable rows: p/N median 0.0323, q90 0.1667, max 0.2500; the inflation
`sqrt((N-2)/(N-p-1))` median 1.0000, q90 1.0626, **max 1.1530** — reproducing idea 483's
median 1.0511 / max 1.1530 on the sites it measured.

| | claims over \|t\|>2 | still over the bar after the charge | significant at 5% under the corrected reference |
|---|---|---|---|
| WITHIN_OLS | 107 | **107** | 107 |
| CELL_AGG | 195 | **195** | 194 |
| all | **302** | **302 (100%)** | 301 |

The one 5% flip is a CELL_AGG row: `t_rho = 2.220` over 9 cells in
`does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud.transfer.csv`, published against a normal
(p 0.0264) and restated against t(8) (**p 0.0572**). It is the record's only published
within-family claim whose 5% verdict the correct reference changes.

**Why nothing else moves, stated as a number rather than a shrug.** The published within-OLS
|t| are median 16.44, q10 6.47, min 2.22. The dof charge that would push each to exactly 2 needs
p/N median **0.983** (q10 0.902, min 0.187), against an actual p/N of 0.076 (max 0.250). Even
setting p to its structural ceiling — `within_cell_fit` keeps only cells with >= 4 rows, so
p <= N/4 — leaves **106 of 107** over the bar. The record's within-cell claims are not marginal,
and a 5–15% scale charge does not reach them.

## (3) MONTE CARLO — the charge is real, and it is not the biggest one

x and y independent, balanced cells, at the record's own (N, p, G) rungs. A correct procedure
sits at 0.050. 1 000-draw rows (200-draw rows in `.montecarlo.csv`, both reported):

| N | p | G | p/N | naive dof | corrected dof | leave-one-out | cluster SE + NORMAL (the record's own) | CR1 + t(G-1) |
|---|---|---|---|---|---|---|---|---|
| 558 | 18 | 6 | 0.032 | 0.043 | 0.040 | 0.045 | **0.125** | 0.043 |
| 224 | 56 | 8 | 0.250 | **0.095** | 0.053 | 0.098 | 0.103 | 0.029 |
| 548 | 120 | 10 | 0.219 | 0.066 | 0.036 | 0.066 | 0.083 | 0.018 |
| 360 | 120 | 6 | 0.333 | 0.092 | 0.041 | 0.093 | **0.130** | 0.025 |
| 360 | 6 | 3 | 0.017 | 0.047 | 0.044 | 0.052 | **0.251** | 0.051 |
| 6822 | 833 | 34 | 0.122 | 0.053 | 0.046 | 0.054 | 0.066 | 0.037 |
| 4123 | 436 | 24 | 0.106 | 0.074 | 0.059 | 0.072 | 0.084 | 0.057 |

Idea 483's headline rung reproduces exactly: at N=224, p=56 the naive dof clears |t|>2 on
**0.095** of independent draws against **0.053** corrected — its 0.095 / 0.055, and its finding
that **leave-one-out does not fix it** (0.098). Over all 18 rungs the naive-dof rate is median
0.0655 against 0.0435 corrected.

**The new reading is the last two columns.** The record's `within_cell_fit` does not use the
naive dof at all — it uses a cluster-robust SE with a NORMAL reference, and that arm is worse
than the one the queue asked about wherever G is small: 0.125 at G=6, **0.251 at G=3**, i.e. a
five-fold false-positive rate from three clusters. At the cluster counts the record's real
within fits actually use (G = 34 and 24, from `provenance.csv`) it is 0.066 and 0.084 — mildly
anti-conservative, not pathological. CR1 with a t(G-1) reference lands at 0.037 / 0.057 there
and over-corrects at small G. **So the required column beside a cluster-robust t is G, and the
rule is: below about G = 20 the normal reference is not usable.**

## (4) FRESH BOOKS — the same question where (N, p) are known exactly

360 random equal-weight draw books (k in {5, 20}, 60 seeds, 3 panels) plus 36 ranked arms
(top-n, n in {5,10,15,20,30,40}, gross in {0.75, 1.00} — the only two tuned parameters), weekly,
10 bps, t+1. Within-cell fit of OOS Sharpe on IS Sharpe, cells = (panel, k) refined by q
quantile bins of the book's own in-sample vol, so p rises on the SAME rows:

| q | N | p | dof naive | dof correct | slope | t naive | t correct | inflation | cluster t (G=3) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 360 | 6 | 358 | 353 | 0.1361 | 3.808 | 3.782 | 1.007 | 0.875 |
| 2 | 360 | 12 | 358 | 347 | 0.1560 | 4.337 | 4.270 | 1.016 | 1.039 |
| 5 | 360 | 30 | 358 | 329 | 0.1687 | 4.791 | 4.593 | 1.043 | 1.087 |
| 10 | 360 | 60 | 358 | 299 | 0.1680 | 4.777 | 4.365 | 1.094 | 1.129 |
| 20 | 360 | 120 | 358 | 239 | 0.1635 | 4.634 | **3.787** | **1.224** | 1.365 |

The charge is monotone in p and reaches 22% of the t at p/N = 0.33 — the largest deflation
anywhere in this run — and still crosses nothing (0/5 grid points flip at |t|>2, 0/5 at 5%).
The cluster column is the same lesson from the other side: three panels is not enough clusters
to say anything, and the same data reads t = 4.63 or t = 1.36 depending on a choice the record
does not currently publish.

## (5) PROTOCOL — rule 8 and both KEEP paths

Arm chosen on the first half by IS Sharpe, second half read once:

| panel | pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|
| U56 | top5 g1.00 | 1.3045 | 32.13% / 1.0492 / −36.53% | 8.95% / 1.1828 / −12.05% | 14.88% / 0.8287 / −33.72% |
| B136 | top10 g1.00 | 1.2716 | 19.05% / 0.7737 / −33.52% | 7.14% / 0.9844 / −12.24% | 14.99% / 0.8340 / −33.72% |
| SMALL439 | top15 g1.00 | 0.9980 | 18.38% / 0.6594 / −39.85% | 4.08% / 0.5770 / −11.74% | 15.92% / 0.8577 / −33.72% |

The IS-chosen arm beats the live book's OOS Sharpe on **0 of 3** panels and SPY's on 2 of 3,
at 2.7–3.4x SPY's drawdown. **Both KEEP paths over all 396 arms: 4a 0/396, 4b 4/396** (U56
ranked top15_g0.75 and top40_g0.75, plus one 5-name draw book on U56 and one on B136 — single
draws out of 120, i.e. the base rate idea 486 already priced, not candidates). **No KEEP.**

## Caveats

* The census classification is a file-level regex on the producing script plus a hand-read
  estimator map; WITHIN is a lower bound and "publishes p" an upper bound (a file can publish
  `cells` for one t and not another). The map is committed in the script with its source line
  numbers so it can be checked.
* `p_ambiguous` rows are restated at their structural worst case, not at their true p, which is
  not recoverable from the committed CSV.
* The Monte Carlo uses balanced cells and independent x, y — the null the |t|>2 bar is a bar
  against. Unbalanced cells make the naive-dof charge larger, not smaller.
* SURVIVORSHIP: B136 and the sub-$2B panel are current constituents only; the small panel drops
  44 tickers with `max_1d_move >= 1.0` per `data/small_meta.csv`. No level comparison across
  panels in section (4) or (5) is a tradable statement.
