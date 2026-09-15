# Idea 686 (cloud, 2026-09-15) — is the 4b footprint still a cap-mix function once k is a free axis?

**ANSWERED = YES, IT IS STILL A CAP-MIX FUNCTION. KILL for the queue's premise: with panel width
free over 10.0× the boundary does NOT become a (cap mix, PANEL WIDTH) property — it stays the
(cap mix, BOOK SIZE) property idea 285 published. Nothing promoted, no memo, no RULES or PROTOCOL
change.**

Script `2026-09-15_is-the-4b-FOOTPRINT-still-a-cap-mix-function-once-k-is-a-free-axis_cloud.py`.
73 synthetic panels over 25 feasible (q, k) cells × 6 books = **438 scored book-cells**, every one
published. Two tuned parameters, the queue's own: **q** (5 levels) and **k** (6 levels, 40…400 =
**10.0×**, against idea 525's 2.5×). Books, metrics and both KEEP verdicts come from idea 525's
own `do_panel`, imported unmodified; panels from idea 276's `build_sources`.

## The answer, on the three axes the question needs

Within-level Spearman of the 4b pass indicator against each axis, with the record's own bar
(|ρ| ≥ 0.30, sign holding in ≥ ⌈8/11 × L⌉ levels):

| axis | mean within-level ρ | sign | verdict |
|---|---|---|---|
| **q — cap mix** (within k) | **−0.2936** | 4 of 4 | FAIL — *narrowly, and directionally perfect* |
| **k — PANEL WIDTH** (within q) | **−0.1329** | 3 of 3 | FAIL |
| **n — BOOK SIZE** (within q) | **+0.3125** | 3 of 3 | **PASS** |

Pooled partial Spearman: ρ(pass4b, q | k) = **−0.2652**, ρ(pass4b, k | q) = **−0.0838**
(CAND-only −0.0822), ρ(pass4b, n | q) = **+0.2332**. Linear probability fit on the CAND slice
(365 cells): `pass4b ~ 1 + q + log k + log n` gives **q −0.2144, log k −0.0160, log n +0.0775**,
R² 0.1585 — **cap mix is 13× the coefficient of panel width, and book size is 4.8×**.

**H_285 FAILS**, and it fails in the direction that vindicates idea 285: panel width is the
weakest of the three axes on every reading, so the boundary the record called a
(cap mix, book size) property is exactly that.

## The footprint, every cell published

4b pass rate by (q, k); `.` = cell outside the feasible envelope:

| q \ k | 40 | 60 | 80 | 100 | 200 | 400 |
|---|---|---|---|---|---|---|
| 0.00 | 0.278 | 0.278 | 0.167 | 0.167 | . | . |
| 0.25 | 0.111 | 0.167 | 0.000 | 0.056 | . | . |
| 0.50 | 0.056 | 0.000 | 0.000 | 0.000 | 0.000 | . |
| 0.75 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 1.00 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

Overall **4b 21 of 438 (0.0479)**; **4a 0 of 438 (0.0000)**. **H_MONO PASSES**: the pass rate is
non-increasing in q at every one of the 6 k levels — 525's monotone reading survives the wider
ladder. By book: CAND30 and CAND20 carry the passes (0.800 and 0.300 at q = 0), CAND5 passes
**0.000 everywhere**, EWall 0.100 at q = 0 and 0 elsewhere.

## The limit of this run, stated plainly and not buried

The feasible envelope is `q·k ≤ 663` and `(1−q)·k ≤ 100`, so **k > 100 requires q ≥ 0.50** — the
large-cap pool has only 100 names. Every wide cell therefore sits in the region where the q axis
has *already* zeroed the footprint (q ≥ 0.50 passes 1 of 216 cells even at k ≤ 100). So the run's
k arm is **0 of 90 at k > 100**, and that zero is not independent evidence about width: it is what
the cap-mix result predicts. **The honest statement is that on the committed caches the width axis
cannot be read at q ≤ 0.25 at all**, which is the half of the ladder where 4b lives. H_K's failure
is therefore a *negative* result about width with a named blind spot, not a clean refutation.
Widening the large-cap pool is the only way to close it and needs a live download (filed as 927).

## Gates — 4 of 5, with the one failure decomposed rather than relaxed

G1 envelope (73 panels, 0 violations), G2 the k-identity `log Ebar = log breadth + log k`
(max residual 8.9e-16), G4 one shared SPY comparand (spread 0.0 across all 438 rows;
14.06% / 0.858 / −33.72%), G5 determinism (0.0) all **PASS**.

**G3, the load-bearing cross-run gate, FAILS — and the cause is worth more than the gate.**

- **G3a shape reproduces**: 348 cells / 58 panels, exactly 525's.
- **G3b the headline count reproduces**: **21 of 348**, exactly 525's.
- **G3c the CELLS do not**: verdict agreement **0.9655** (12 of 348 flip), max |ΔSharpe| **0.6065**,
  max |ΔEbar| **6.98** at the same (q, k, draw) label.
- **G3d the cause, verified**: idea 525's own console records `pools: SMALL 439, BSTK 100` on a
  4,194-day calendar ending 2026-09-04. This tree's identical code path yields **SMALL 663** on a
  **4,198**-day calendar ending 2026-09-11. **The small-cap pool has been restated 439 → 663
  names**, and 525 committed no column lists, so **its panels cannot be rebuilt from this tree at
  any seed.** The same-day `SMALL_PANEL_README.md` records a 715-ticker re-cache, and idea 276's
  own docstring still says "minus the 44 tickers" where the screen now drops 52. The label
  `SMALL439` denotes a 663-name pool today.
- **G3e what the restatement costs the published claim**: 525 published *"highest q carrying any
  4b pass: 0.25"*. On the restated pool the highest q carrying a pass is **0.50**. The
  passer/failer means move with it: Ebar **38.9 / 35.9** here against 525's **42.7 / 33.5**,
  breadth **0.6582 / 0.5164** against **0.6479 / 0.4874**.

Everything this run concludes about (q, k, n) is computed **within one vintage** and is unaffected
by this. What is affected is the transportability of 525's published numbers — and, by extension,
of every committed result on the `SMALL439` label.

## Rule 8 (required) — the cell chosen on 2009-2016 alone, 2017-2026 read once

9 picks = 3 supports (ALL / WIDE-only / NARROW-only) × 3 IS-only choosers (max IS Sharpe; max IS
Sharpe at the lowest q; max IS Sharpe at the widest k). **OOS 4b 0 of 9 on every draw and on any
draw; OOS 4a 0 of 9.** SPY OOS Sharpe 0.877; RULES v2 on these panels OOS Sharpe mean 0.817
(0.432…1.236).

- `PICK_ISSHARPE` (ALL) → q=0.50, k=40, CAND10: IS 1.227, **OOS 9.65% / 0.703 / −25.15%**
- `PICK_ISQMIN` (ALL) → q=0.00, k=100, CAND15: IS 1.089, **OOS 13.79% / 0.921 / −21.15%**
- `PICK_ISKMAX` (ALL) → q=0.75, k=400, EWall: IS 0.839, **OOS 6.36% / 0.571 / −26.09%**

The best OOS book in the run is the one an IS chooser reaches only by being *told* to minimise q,
and even it fails 4b on the DD cap (−21.15% against −20.23%). **Nothing on this ladder is
capital-worthy**, which is the same answer 525 gave on a narrower one.

## Survivorship

The small-cap pool and BSTK100 are current constituents of their screens (the small pool
additionally drops the tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR
and drawdown **level** above is optimistic and both 4b bars are easier here than on a
point-in-time panel. The (q, k, n) contrasts are same-days comparisons across synthetic panels
drawn from the same two pools and are far less exposed; the pass counts and the rule-8 triples are
levels read against SPY, which is not survivorship-inflated, so those are upper bounds.

## Follow-ups filed

- 927 — the width axis is unreadable at q ≤ 0.25 because BSTK100 has 100 names; cache a wider
  large-cap pool (LOCAL ONLY — needs a live download) and re-read H_K where 4b actually lives.
- 928 — `SMALL439` now denotes 663 names. Census every committed result carrying that label for
  the pool size it was actually computed on, and report which published numbers are unreachable
  from the current tree.
- 929 — CAND5 passes 4b 0.000 on all 438 cells while CAND30 passes 0.800 at q = 0; price the
  book-size axis on its own ladder at fixed (q, k) and find where the pass rate turns over.
