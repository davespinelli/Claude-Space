# Idea 150 — the DD cap is what cuts risk-adjusted argmaxes (cloud, 2026-09-08)

**VERDICT: ANSWERED — YES, decisively, with a structural qualification the queue did not
anticipate. A Calmar-style RATIO bar changes ~69% of the admitted set and admits a set that is
BETTER out of sample on all three metrics; a LINEAR joint bar cannot change the set at all.**
Script `2026-09-08_the-DD-cap-is-what-cuts-risk-adjusted-argmaxes_cloud.py`. Not a book — this is
a PROTOCOL question. No RULES change, no candidate, no memo.

## Corpus and the gate that makes a re-scoring census honest

Every `research/backtests/*.grid.csv` in the repository was scanned: **237 files, 125 ADMITTED,
2 REJECTED on the verdict gate, 110 excluded on schema or unmappable panel labels** — all listed
in `.harvest.csv`. A file enters only if this script, recomputing all five 4b margins from the
row's own CAGR/MaxDD/H1/H2/OOS columns and *this* repository's SPY bars, **reproduces the parent's
committed 4b verdict on every single row**. Numeric agreement is reported separately and graded
(idea 401's `data/prices.csv` restatement means exact numeric agreement is not expected on older
u56 files; the verdict gate is what is checked at full strength). The two rejected files —
`holding-period-as-the-hidden-variable_cloud` (20 of 468 mismatches) and
`quote-every-n-argmax-with-its-saturation-share_cloud` (7 of 56) — are excluded from every number
below.

**Corpus: 67,316 rows from 125 files over 4 panels** (u56 27,302 / broad 27,333 / small 12,552 /
bstk100 129). 9,032 clear PROTOCOL 4b as written; 32,352 clear the three Sharpe legs alone. The
three Sharpe legs are **held identical under every rule**, so every difference below is
attributable to the DD/CAGR pair and to nothing else.

## The premise audit — idea 141's claim is half right, and the other half is the finding

Of the 32,352 rows clearing the three Sharpe legs:

| excluded by | rows | share |
|---|---|---|
| the DD CAP alone | 10,518 | **32.5%** |
| the CAGR FLOOR alone | 12,680 | **39.2%** |
| **both** | **122** | **0.4%** |

The DD cap is *not* the dominant cutter — the CAGR floor cuts more. And the two bars are **almost
perfectly disjoint**: 0.4% of exclusions fail both. PROTOCOL 4b's DD/CAGR pair is therefore a
conjunction of two nearly-independent constraints, each rejecting a different third of the
population. *That* is why the joint question matters, and it is a stronger reason than idea 141's.
Per panel: u56 30.6/37.6, broad 34.8/41.6, bstk100 **93.0/7.0** (the DD cap closes that panel
essentially alone), small 100/0 on its single Sharpe-clearing row.

## The two joint forms, all 29 grid points reported (`.sweep.csv`)

* **JOINT-L(lambda)** — half-plane through PROTOCOL's own corner:
  `CAGR - lambda*|MaxDD| >= 0.70*SPY_CAGR - lambda*0.60*|SPY MaxDD|`. Nests both current bars
  (lambda=0 is the CAGR floor alone, lambda=inf the DD cap alone).
* **JOINT-C(kappa)** — Calmar ratio bar: `CAGR/|MaxDD| >= kappa * SPY_CAGR/|SPY MaxDD|`.

**Structural result: JOINT-L has `swap_out = 0` at every one of its 12 coefficients.** SEP is the
*intersection* of two half-planes, and any half-plane through their corner *contains* that
intersection — so a linear joint bar can only ever admit MORE, never differently. **A linear
CAGR/drawdown trade-off cannot change which books pass 4b; it can only loosen the bar.** Confirmed
numerically at every lambda from 0 to inf (admits 19,550 to 29,943 against SEP's 9,032, and the
extra rows are worse: OOS Sharpe 1.0995-1.1394 vs SEP's 1.1373).

**Only the RATIO form re-orders.** JOINT-C begins excluding SEP-admitted rows at kappa >= 1.2 and
at kappa = 1.5 admits 11,954 rows of which only 5,017 are SEP's — **Jaccard 0.314, i.e. 69% of the
admitted set is different** — with OOS Sharpe **1.1639** vs SEP's 1.1373, OOS CAGR **13.81%** vs
13.07% and OOS MaxDD **-17.38%** vs -17.71%: better on all three at a *larger* admitted count, so
it is not a shrink-to-the-winners artefact.

## Rule 8 — the coefficient is chosen on the IS window only, then never touched

29,222 rows (55 files) carry `IS_CAGR` and `IS_MaxDD` and can be calibrated on. PROTOCOL's
separate pair admits 5,689 of them in sample (19.5%) — the equal-admission target. Nearest IS
admission: **lambda\* = 0.1** (12,107) and **kappa\* = 1.5** (6,613). Applied untouched:

| rule | admitted | swap in | swap out | Jaccard | OOS Sharpe | OOS CAGR | OOS MaxDD | both-paths |
|---|---|---|---|---|---|---|---|---|
| **SEP (PROTOCOL as written)** | 3,897 | – | – | 1.000 | **1.1253** | **13.04%** | **-17.89%** | 513 |
| JOINT-L(0.1) | 9,197 | 5,300 | **0** | 0.424 | 1.0909 | 14.84% | -21.79% | 864 |
| **JOINT-C(1.5)** | 4,680 | 2,741 | 1,958 | **0.292** | **1.1492** | **13.98%** | **-17.78%** | 739 |

Head-to-head on the swapped rows, which is the test that cannot be a count artefact:
**rows JOINT-C admits and SEP rejects: OOS Sharpe 1.1384 / CAGR 14.08% / MaxDD -18.10%.
Rows SEP admits and JOINT-C rejects: 1.0865 / 12.24% / -18.44%.** The joint bar swaps in strictly
better books at the same drawdown.

Reference OOS: SPY 0.882 / 15.45% / -33.72%; live RULES v2 @10 bps 1.285 (u56) / 1.119 (broad) /
1.140 (bstk100) / 0.566 (small).

## It is not one file and not one panel

Per panel at kappa\* = 1.5: u56 OOS Sharpe 1.1934 (JOINT-C) vs 1.1754 (SEP), broad 1.0688 vs
1.0645, both with higher OOS CAGR and shallower OOS MaxDD. **On bstk100 and small, SEP admits
ZERO rows and JOINT-C admits 8 and 1** — the ratio bar opens panels the separate pair closes
entirely, which bears directly on the record's small-panel wall (idea 136). Per parent file
(115 files with >= 5 admitted rows under both rules): **JOINT-C's mean OOS Sharpe beats SEP's in
88 of 115 files, median +0.0241, mean +0.0232.**

## Books, not rows — the queue's literal question

Aggregating to the parent file's own row identity (13,212 distinct books): SEP admits 2,302,
JOINT-C(1.5) admits 2,329, of which **1,137 are new and 1,110 of SEP's are dropped — roughly half
the admitted book set turns over**. JOINT-L(0.1) admits 4,550, dropping none: loosening, not
re-ordering.

## Caveats

* **SURVIVORSHIP (idea 54).** Every panel is current constituents (the small panel is the sub-$2B
  screen's survivors since 2010 with `max_1d_move >= 1.0` dropped). CAGR is inflated on every row,
  so the CAGR side of any joint bar is flattered relative to the drawdown side, and a rule that
  lets return pay for drawdown is biased **toward admitting more here** than it would on a
  delisting-complete panel. No level in this file is an achievable return.
* This is a **re-scoring census**: it changes the bar, not the books. It cannot discover a book and
  does not try. It says only which of the record's existing rows move.
* Rows are heavily clustered — 125 files re-derive overlapping books and arms — so 67,316 is not
  67,316 independent observations. Per-panel and per-file breakdowns are printed for exactly that
  reason, and the per-file count (88 of 115) is the statistic to read, not the row count.
* The `both_paths` column carries each parent's own committed 4a verdict, and idea 398 showed the
  record's 4a comparand is not uniform (V1u at a fixed 10 bps vs cost-matched
  `baseline.rules_v1_weights` vs RULES v2). Those counts are indicative only.
* Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the IS calibration
  of any drawdown-side coefficient is measured on a window that cannot express a deep drawdown.
* The 110 schema-excluded files are mostly grids without a resolvable panel label or without an
  OOS Sharpe column; they are listed in `.harvest.csv` and are not a curated omission.

## What this recommends (a Sunday-review question, not a change made here)

PROTOCOL 4b's separate DD cap and CAGR floor should be considered for replacement by the single
bar **`CAGR/|MaxDD| >= 1.5 * SPY_CAGR/|SPY MaxDD|`**, keeping the three Sharpe legs unchanged.
On the record's own 67,316 committed rows, with the coefficient fixed in sample and never retuned,
that bar admits a set with higher OOS Sharpe, higher OOS CAGR and shallower OOS drawdown than the
pair it replaces, wins in 88 of 115 parent files, and reopens two panels the pair closes outright.
The linear alternative should be dropped from consideration: it is provably incapable of changing
the answer. **PROTOCOL.md was not modified** — rule changes go through Sunday review.
