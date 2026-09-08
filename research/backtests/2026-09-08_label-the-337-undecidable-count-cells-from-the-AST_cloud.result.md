# Idea 469 — label-the-337-undecidable-count-cells-from-the-AST (cloud lane, 2026-09-08)

Script `2026-09-08_label-the-337-undecidable-count-cells-from-the-AST_cloud.py`,
console `…_cloud.console.txt`, artefacts `…census.csv` / `…census_today.csv` /
`…sidebyside.csv` / `…ladder.csv` / `…grid.csv` / `…walkforward.csv` / `…reference.csv`.
10 bps headline (+25 bps rung), weekly cadence, next-day execution.

**VERDICT: METHOD — the bound narrows *and the point estimate falls 15 pp*. No KEEP, no
RULES change.**

---

## CHECK(a) — idea 244 reproduces exactly, before the AST is used at all

The record has grown by 1,596 CSVs since idea 244 ran this morning, so the comparison is
made on a **frozen corpus**: the 396 files idea 244's own `.census.csv` + `.census_rejects.csv`
name (a file in neither contributed nothing), symlinked into a scratch directory and read
by idea 244's own committed `census()` through its own `label_convention()`. On that
corpus it returns **694 cells, FIXEDTOT 222 / NORM 135 / MIXED 260 / UNKNOWN 77 — every
number identical to the published census.** Corpus drift is reported, not folded in: the
same AST census over the corpus as it stands today is 1,992 files / 850 cells.

## Q1 — what the AST changes

Same files, same admission tests (count column with ≥3 distinct ints in [2,500], a Sharpe
column beside it, a parent script that ranks), same panel map, same `target_gross` measure,
same pre-registered ladder threshold. **Only `label_convention` is replaced.** The AST does
four things a regex cannot, and each one is load-bearing here:

| | | |
|---|---|---|
| **shape** | a weight is a *frame* | `p2 = float((dev >= …).sum()) / n` is wholly scalar arithmetic and is dropped; the regex counted it as `GROSS/n` |
| **local dataflow** | which name is the denominator | `k = sel.sum(axis=1)` binds `k` to a *realised count*, so `.div(k, axis=0)` is NORM even though `k` is also a common name for the dial |
| **guards** | convention is a *function of a variable* | `if conv == "NORM": return … ; return sel * (g/nn)` is not "a script that does both", it is `conv` ↦ {NORM, FIXEDTOT}, trailing return included (the ELSE arm) |
| **the resolving column** | the script's *own* name for the dial | idea 244 looked for a fixed list (`conv`, `convention`, …); the AST discovers `constr`, `arm`, `dg`, … and finds the column carrying those literals |

On the 572 cell keys the two censuses share:

- decided by **REGEX 281/572 = 49.1%**; decided by **AST 421/572 = 73.6%**
  (of which **46 are cells the AST resolves into two or more arms** — one published "cell"
  that is really two books; single-label AST coverage is 375/572 = 65.6%).
- where both decide, they **agree on 87.6%**; **all 24 disagreements are printed with the
  deciding expression at file:line** in the console, so each is checkable against the
  committed source. Four adjudicated examples, all of which the AST gets right and the
  regex gets wrong:
  - `trend-filter-by-market-cap_cloud.py:193,195,203` — `.div(k, axis=0)` / `.div(n, axis=0)`
    where `n = live.sum(axis=1).clip(lower=1)`. **All NORM.** The regex read the `/ n` and
    said FIXEDTOT.
  - `position-count-broad-confirm_B.py:76,78` — `conv=="NORM"` → NORM, else `sel*(g/nn)`.
    **Per-row via the `conv` column**, not one label.
  - `does-book-share-price-a-tilt_C.py:200,202` — `constr=="lit"` → FIXEDTOT, else NORM;
    the file has a `constr` column. The regex called the whole file FIXEDTOT.
  - `does-the-vol-gate-corner…_cloud.py:177,179` — `dg` guard → FIXEDTOT / else NORM.

**Known false negative, documented:** a guard that is not an equality against a string
literal (`if fixedw is not None: return m * fixedw`, same file, line 197) is invisible to
the arm resolver, so that script's FIXEDW branch is not labelled. The FIXEDW and MATCHED
label classes fired **zero** times in this corpus — the extended ladder rate equals the
core one exactly (94/468).

## Q2 — THE RE-QUOTED BOUND (the answer to the queue item)

Pre-registered, unchanged: a cell is a GROSS-LADDER point iff mean target gross moves
≥ 0.05 NAV across the cell's **own** quoted grid.

| | idea 244 (regex) | idea 469 (AST) |
|---|---|---|
| decidable coverage | 271/694 = 39.0% | **468/790 = 59.2%** |
| **lower bound** (undecidables all NORM) | 95/546 = 17.4% | **94/645 = 14.6%** |
| **point estimate** | 95/271 = **35.1%** | 94/468 = **20.1%** |
| **upper bound** (undecidables all FIXEDTOT) | 238/546 = 43.6% | **206/645 = 31.9%** |
| bound width | 26.2 pp | **17.4 pp** |

**The premise is right that the bound was loose, but the interesting result is that
narrowing it moves the point estimate DOWN by 15 pp.** The regex was not merely
*undecided* on 337 cells — where it did decide, it was biased toward FIXEDTOT, because
every `/ n` in a script (including realised-count denominators and scalar arithmetic) fired
the FIXEDTOT pattern. Under the AST the record holds **353 NORM cells against 238 FIXEDTOT**
(regex: 135 vs 222), and the ladder partition is clean by construction:
**NORM 300 FLAT / 0 LADDER, FIXEDTOT 94 LADDER / 74 FLAT.** Ladder cells live in 19 of 39
files; the largest span is 0.390 NAV; median span over decidable cells is 0.000; no cell's
grid top implies leverage (max implied gross 0.75).

**The bound does not collapse.** 177 cells on a mappable panel are still undecidable, and
they are counted, not hidden: **138 multi-arm-with-no-resolving-column** (the script's
convention genuinely varies row to row and the CSV never published which arm each row is),
**35 no-weight-expression**, **26 multi-arm-unguarded**. The 138 are a *publication*
defect, not an analysis one — they are unrecoverable from the committed artefacts and can
only be fixed by scripts printing their own arm column.

## L1 — is the census's measure sound? (84 live books, every point reported)

`target_gross` never runs a backtest, so the whole census rests on it. Against realised
held gross over 7 panels × 6 n × {FIXEDTOT, NORM}: **max |held − target| = 0.0005**
(mean 0.0002), correlation **1.0000**, and **0 of 14 (panel × arm) LADDER/FLAT verdicts
flip** when realised gross replaces target gross. The measure is validated.

## L2 — rule 8 (n chosen on 2009-2016 IS Sharpe alone, 2017-2026 read once)

| panel | IS pick (FIXEDTOT / NORM) | OOS Sharpe, correct label | RULES v2 OOS | EW_ALL OOS | SPY OOS |
|---|---|---|---|---|---|
| U56 | 20 / 20 | 1.1680 / 1.1307 | 1.2851 | 1.1119 | 0.8820 |
| B136 | 30 / 10 | 0.9032 / 0.7806 | 1.1185 | 1.0185 | 0.8820 |
| BSTK100 | 60 / 10 | 1.1285 / 0.7489 | 1.1377 | 1.0096 | 0.8820 |
| STK20 | 10 / 10 | 1.3635 / 1.4104 | 1.4433 | 1.4337 | 0.8820 |
| SMALL | 20 / 20 | 0.4873 / 0.4657 | 0.5680 | 0.2910 | 0.8820 |
| ETF36 | 20 / 40 | 0.9419 / 0.6657 | 0.9272 | 0.6658 | 0.8820 |
| ETF24 | 20 / 20 | 0.8886 / 0.7276 | 0.8677 | 0.7259 | 0.8820 |

Correctly labelled, the IS-chosen n beats **RULES v2 OOS in 2 of 14** cells at 10 bps and
**0 of 14 at 25 bps**, EW_ALL in 8/14, SPY in 8/14; mean OOS regret vs the oracle n is
**+0.0768**. This is the 244 KILL again, not a new one.

**THE OOS COST OF THE LABEL (new).** Running the same book with n chosen under the *wrong*
convention label — exactly what a mislabelled census cell invites a reader to do — the
label **moves the pick in 5 of 14 (panel × rung) cells**, and where it moves it is worth
**mean +0.0012, median 0.0000, min −0.3558 (BSTK100 FIXEDTOT), max +0.2721** of OOS Sharpe;
it hurts in 5 of 28 cells, helps in 5, is a no-op in 18. So the mislabelling is
**consequential per-cell and a coin flip on average**: it can cost a third of a Sharpe
point on one panel, but nobody should expect a directional edge from getting it right.

## L3 — both KEEP paths, all 168 live points

**4a 0/168** against the live RULES v2 on each book's own panel. **4b 17/168**
(10 bps: FIXEDTOT 10, NORM 5; 25 bps: FIXEDTOT 2, NORM 0); binding bars H2 107 / DD 100 /
H1 97 / CAGR 97 / OOS 96. Best 4b point is **STK20 n=20 FIXEDTOT @10 bps: CAGR 12.05%,
Sharpe 1.3367 (H1 1.3409 / H2 1.3414), OOS Sharpe 1.4459, MaxDD −12.11%** — and it fails
4a on H1, sits below RULES v2 on its own panel (1.4288 / OOS 1.4433) and below EW_ALL OOS
(1.4337), and lives on STK20, the 20-name survivor panel this record has repeatedly
flagged. **No KEEP, no memo, no candidate.**

## Caveats

SURVIVORSHIP: every panel is current constituents, one-directional and hardest on STK20 /
BSTK100 / SMALL; the 44 small-cap tickers with `max_1d_move >= 1.0` are dropped first
(439 tradable remain). The census inherits the bias of every parent script it reads. The
AST resolver is a *static* analysis: it decides which weighting expressions are reachable
from a CSV's writer function, not which one produced a given row byte-for-byte, so the 138
multi-arm-no-column cells remain honestly undecidable rather than guessed.
