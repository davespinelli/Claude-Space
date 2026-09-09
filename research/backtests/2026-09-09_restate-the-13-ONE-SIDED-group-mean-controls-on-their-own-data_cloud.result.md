# Idea 511 — restate the ONE-SIDED group-mean controls on their own data (cloud, 2026-09-09)

**Verdict: ANSWERED / PREMISE CONFIRMED BUT BOUNDED — no KEEP, no RULES change.**
The exposure the queue names is real, is now *measured* rather than bounded, and is small
everywhere except one script.

## What was run

Idea 483's runtime census logged `(N, p)` at every fit but not the cell-size vector `m`, so
the leave-one-out restatement of a one-sided `groupby(...).transform("mean")` demeaning —
exactly `x_i - mean_{-i} = m/(m-1) * (x_i - mean)` — was bounded and unmeasured. The three
scripts carrying that family were re-executed under an instrumented pandas that logs the
full cell-size vector at every `transform("mean")` call and, **at the three target sites
only**, substitutes an out-of-fold cell mean, all inside a write sandbox that mirrors every
repo write into scratch. 15 runs = 3 scripts × 5 fold forms, rc==0 on 15/15.

Two tuned parameters, every point reported: **FOLD FORM** {PUBLISHED, K2, K5, K10, LOO} ×
**SCRIPT** {the 3 target files} (STAGE 4 swaps SCRIPT for the CELL KEY).

## The cell sizes — what was missing

| site | calls | N | p | m min / med / max | m/(m−1) max | m/(m−1) row-weighted mean |
|---|---|---|---|---|---|---|
| `census-every-CROSSING…_C.py:148` | 212 | 42–1152 | 2–70 | 5 / 20 / 576 | 1.2500 | 1.0698 |
| `the-mid-tercile-band_cloud.py:340` | 8 | 1203–1696 | 3–92 | 1 / 90.5 / 632 | 2.0000 | 1.0291 |
| `why-the-035-045-share-window-dips_cloud.py:295` | 1 | 560 | 70 | 5 / 8 / 11 | 1.2500 | 1.1469 |

Pooled over **4,124 cells**: m median 10, q10 5, min 1, max 632. Over the 4,096 cells with
m>1 the exact rescale factor is **median 1.1111, q90 1.2500, max 2.0000**; 28 cells have
m=1, where LOO is undefined and the demeaned value is 0 either way.

## The restatement

**6,279 of 3,201,888 published numeric artefact cells move (0.196%)**, and the movement is
concentrated in one file, not spread across the family:

| script | moved / cells | share | max relative move | console lines changed (K2/K5/K10/LOO) | **verdict-token flips** |
|---|---|---|---|---|---|
| `census-every-CROSSING…_C` | 5,924 / 84,860 | **6.98%** | 1.90 | 40 / 39 / 27 / 21 of 538 | **5 / 7 / 1 / 1** |
| `the-mid-tercile-band_cloud` | 223 / 123,888 | 0.18% | 0.70 | 7 / 8 / 7 / 4 of 264 | 0 / 0 / 0 / 0 |
| `why-the-035-045-share-window-dips_cloud` | 132 / 2,993,140 | 0.004% | 1.88 | 34 / 34 / 34 / 35 of 260 | 0 / 0 / 0 / 0 |

The crossing census is the one file whose *readings* move, not just its digits: YES/NO
crossing verdicts flip on individual grid rows, and its held-out headline moves
`mean |error| in grid steps: POOLED 1.571 → 1.111, FE 1.714 → 1.111` under LOO, with the
count of rows on which both readings are defined falling 28 → 27. Its published direction
("FE is not better than POOLED", FE better in 0 of 28) is **unchanged** — LOO moves the
level of both legs together and the ordering survives.

## Reproduction gate (a by-product, and a caveat on the above)

Only **14 of 24** committed CSV artefacts are reproduced cell-for-cell by the instrumented
PUBLISHED arm today; 10 move without any substitution at all, i.e. those three scripts are
not reproducible against today's `data/`. Every number above is therefore a **within-run**
PUBLISHED-vs-form contrast, which is the correct control anyway. This corroborates open
idea 513 and widens it from 3 scripts to at least these 3 as well.

## Rule 8 + both KEEP paths

The same demeaning used as a **selector** on idea 78/83's committed 300 B136 books, chosen
on 2009–2016 only, 2017–2026 untouched, over 3 cell keys × 5 fold forms + the incumbent:

- The fold form changes the pick on **2 of 12** rows (K5 on two cell keys); K2, K10 and LOO
  pick exactly what PUBLISHED picks on 3/3 cell keys.
- Mean OOS Sharpe: PUBLISHED / K2 / K10 / LOO **1.0211** (mean OOS rank 53.7/150), K5
  1.1045 (rank 19.0) — and the **raw IS-Sharpe incumbent, which fits nothing, gets 1.1045
  (rank 19)**. No fold form beats the no-control incumbent.
- SPY 15.23% / 0.889 / −33.72% (halves 0.957/0.834, OOS 0.882); RULES v2 8.03% / 1.106 /
  −12.24% (halves 1.229/0.984, OOS 1.119).
- **KEEP paths: 4a 0/16, 4b 0/16, both 0/16.** The 4b bar that binds is the CAGR floor on
  16/16 rows.

## Conclusion

The one-sided group-mean control family is a real but **bounded and mostly immaterial**
exposure: a median 11% per-row rescale that moves 0.196% of the record's published cells in
these files and reverses no published direction. The single script it does move materially
(the crossing census, 7.0% of cells and up to 7 YES/NO row readings) should carry the LOO
restatement beside its published column; the other two need no restatement. As an
instrument it is worthless — 0/16 on both KEEP paths and never better than fitting nothing.

Artefacts: `.cellsizes.csv`, `.sites.csv`, `.gate.csv`, `.restated.csv`, `.artefactdiff.csv`,
`.consolediff.csv`, `.walkforward.csv`, `.keeppaths.csv`, `.sweepstatus.csv`, `.console.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
