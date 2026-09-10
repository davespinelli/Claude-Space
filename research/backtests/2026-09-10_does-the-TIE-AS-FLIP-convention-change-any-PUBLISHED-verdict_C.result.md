# IDEA 595 — does the TIE-AS-FLIP convention change any PUBLISHED verdict? (lane C, 2026-09-10)

**VERDICT: SPLIT. KILL of the strong reading — no published verdict, no KEEP path and no panel
ordering on the record's own book populations moves at any tie bar. CONFIRMED on the synthetic
draw populations, where every one of idea 592's POP-B headline numbers moves. Plus one
CORRECTION the record needs: idea 592's "342 exact ties" are 99 exact ties and 243 sign
comparisons of float noise, and only the first group is the `np.sign(0) = 0` mechanism it
published.** No RULES change, no book promoted, no memo. RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.

## What was asked, and what the object under test is

The queue asked to re-score every ladder and draw population in the record under a three-way
label (better / worse / TIE) instead of the binary flip `np.sign(A−U) != np.sign(A−M)`, and to
report which published flip rates, AUCs and orderings move. Two tuned parameters, both the ones
the queue names: **population set** (5 levels) × **tie bar τ** (8 levels) = **40 grid points,
all reported** in `.grid.csv`, `.auc.csv` and `.ordering.csv`.

The three-way label is
`lab(d, τ) = TIE if |d| ≤ τ else sign(d)`, and a pair is `FLIP` / `SAME` / `UNDET` (either leg a
TIE). **Gate G3 asserts this is the record's own arithmetic with one branch added**: at τ = 0
with `UNDET` folded into `FLIP`, the labeller reproduces every committed `flip_*` column —
**0 disagreements over 6,480 row-legs**.

## Gates, all PASS, all before any result was read

| gate | what it asserts | measured | bar |
|---|---|---|---|
| G0 | panels truncated to idea 584's window, row counts exact | 4700 / 4699 / 4194 | exact |
| G1 | vectorised runner vs `engine.backtest` on 3 books | **1.39e-17** | 1e-12 |
| G2 | idea 592's committed `.ties.csv` re-derived from its OWN committed cells and shuffle rows | POP A 216/28/0 and POP B 1404/785/342, **both exact** | exact |
| G3 | three-way at τ=0, UNDET folded into FLIP, reproduces every committed `flip_*` | **0 / 6,480** | 0 |
| G4 | matched gross on all 324 fresh cells | **1.78e-15** | 1e-12 |
| G5 | fresh cells reproduce idea 592's committed cells | max\|d(dU)\| **9.89e-17**, 0 flag disagreements; B136 (bit-identical cache) **9.71e-17** | 1e-4 / 0 / 1e-12 |

G5 is *tighter* than idea 592's own provenance gate (which needed 1e-4 for the price
restatement): between that run and this one `data/prices.csv` gained one bar and nothing else
moved on the truncated window, so the fresh build reproduces at machine precision.

## PART A — the census: this is not one file's bug

An AST walk over all **541 committed scripts** finds **185 sign-comparison sites in 90 scripts**,
every one of them missing a tie branch. Classified structurally, never from a filename:

| shape | what a tie does | sites | scripts |
|---|---|---|---|
| `np.sign(A) != np.sign(B)` | spurious **FLIP** | 64 | 34 |
| `np.sign(A) == np.sign(B)` | spurious **NON-HOLD** | 76 | 40 |
| `(A > 0) != (B > 0)` | **asymmetric** — 0 silently counted with the `<` side | 28 | 22 |
| `np.sign(A) == <literal>` | depends on the literal | 17 | 9 |

**75 sites report DISAGREEMENT** (a tie *inflates* a flip count) and **110 report AGREEMENT** (a
tie *deflates* it). The record has published the first bias once, in idea 592, and has never
published the second — yet the `sign_holds` column of every walk-forward file in the corpus is
the second shape, so every IS→OOS agreement rate the record quotes is biased **down** by exactly
its tie rate. Direction matters and the two are opposite.

**The re-scorable footprint is small and is stated rather than assumed.** A site can only be
re-scored if the run published *both operands* as columns. Exactly **three distinct populations,
2,160 rows**, do: the 324 real book cells (ideas 581, 584, 591 and 592 all publish the *same*
324 books — max \|d(dU)\| between them 1.19e-6 to 1.03e-3 — so they are one population, not four,
and are not pooled), idea 584's 432-row λ ladder, and the 1,404-row block-shuffle draws.
Everything else in the record would have to be re-run to be re-scored.

## PART B/C — what moves and what does not (40 grid points)

**Nothing moves on real books.** On REC-CELLS and FRESH-CELLS the UNDETERMINED share is
**0.0000 on all three legs at every τ ≤ 1e-9**, and the MaxDD flip rate is 8.64% published vs
8.64% three-way. On REC-LADDER it is 0.0000 up to 1e-6. The **Sharpe and CAGR legs carry zero
exact ties on every population tested** (H1 confirmed): a statistic summed over ~4,000 bars does
not coincide bit-for-bit.

**Everything moves on the shuffle draws.** At idea 592's own 1e-12 bar:

| statistic | published (binary) | three-way | |
|---|---|---|---|
| MaxDD flip rate | **55.9%** | **47.9%** over the 924 determined rows | −8.0 pp |
| undetermined share | not reported | **34.2%** of the population | — |
| AUC ceiling (8 path predictors) | **0.6171** | **0.7343** | +0.117 |
| AUC argmax | GAP | GAP | unchanged at **0 of 40** grid points |
| panel ordering by flip rate | U56 > SMALL439 > B136 | **SMALL439 > U56 > B136** | moves at **12 of 40** points |

The AUC ceiling is the number idea 592 built its whole case around ("best of 8 is the gross gap
at 0.640"). Deleting the undetermined rows raises it to **0.734**, which is the same direction
and the same size as the correction idea 592 itself reported in one line of its result
("dropping the 491 undetermined rows leaves path GAP 0.7374"). This run confirms that as the
right reading and shows it is not a one-cell artefact: it holds at every τ from 1e-15 up, and it
is reproduced independently on a freshly built shuffle population.

**The panel ordering flip is the substantive move.** The published draw-level ordering
U56 > SMALL439 > B136 becomes SMALL439 > U56 > B136 as soon as τ reaches one ulp — the whole
U56/SMALL439 gap on that population is made of undetermined labels. No committed artefact quotes
that particular ordering as a claim, so no published sentence is wrong today; the point is that
the record's draw-population orderings are not robust to a branch the convention omits.

## PART D — the correction: 342 ties, 99 of them zeros

Idea 592's prose reads "*exact zeros, not near-misses*" and its `ties.csv` counts them at
`|d| < 1e-12`. Those are different claims, and the difference decides whether the *mechanism*
it published is the one generating the labels:

* `|dU_MaxDD| == 0` **exactly** — `np.sign` returns 0, the published bug: **99** of 785 flips
  (12.6%).
* `0 < |dU_MaxDD| ≤ 1e-12` — `np.sign` returns ±1, so these are *genuine opposite-sign
  comparisons of float noise*, a different failure with the same consequence: **243** more.
* The smallest non-zero `|dU_MaxDD|` on the shuffle population is **1.110e-16**, about one ulp
  of a MaxDD near 0.21.

Both groups are undetermined and idea 592's *conclusion* stands unchanged. Its stated
*mechanism* covers 12.6% of the flips, not 43.6%, and the record should say so — a tolerance
count is not an exactness count.

## PART E — the KEEP paths have the same missing branch, and it is visible

4a is `H1 > base AND H2 > base AND MaxDD >= base`: the two Sharpe legs **fail** a tie, the
drawdown leg **passes** one. 4b has the same asymmetry. Over all 324 fresh books:

* **2 cells tie all three 4a bars exactly**, and they are not a coincidence:
  **`BAND-DG at dial 0.03, gross 0.75` IS `baseline.rules_v2_weights`** — same mask, same
  de-gross-to-cash, same weights. That 4a comparison is the live book against itself, and the
  `>=` drawdown leg credits it with beating its own drawdown. It fails 4a only because the
  Sharpe legs happen to carry the opposite tie convention. (On SMALL439 the identity does not
  hold: SPY is a benchmark column there, not a tradable name.)
* **No 4a or 4b PASS is created by a tie at any τ** — 0 and 0 at every bar up to 1e-3.
* The smallest \|margin\| on any 4b bar is **6.59e-05**, so the convention cannot move a 4b
  verdict at machine precision. **But 4 of the 50 4b passes clear their tightest bar by ≤ 1e-3
  and 35 of 50 by ≤ 1e-2** — U56 `MA-DG 150 @ g=1.00` passes on a CAGR margin of **0.000133**,
  U56 `BREADTH-DG 0.35 @ g=1.00` on a DD margin of **0.000186**. Those are not ties; they are
  KEEP verdicts standing on a margin the record does not publish beside them.

## PART F / rule 8 — walk-forward, both KEEP paths

(dial, g) chosen on 2009–2016 by IS dSharpe against the unmatched control — the record's own
selection rule — evaluated on 2017–2026 untouched. All 27 picks and all 324 grid points in
`.walkforward.csv` / `.keeppaths.csv`.

* IS sign holds OOS on **16 of 27** picks. **`sign_holds` is unaffected here** — 0 IS legs and
  0 OOS legs are exactly zero, which is H1 again — so the mirror bias is real in the code and
  empty in this sample.
* KEEP paths on the picks: **4a 1/27, 4b 3/27**. Over all 324 grid points: **4a 6, 4b 50,
  BOTH 0.** Identical to idea 592's counts, as G5 requires.
* OOS Sharpe beats RULES v2 on **12/27** picks and SPY on **18/27**. Benchmarks (OOS 2017+):
  U56 RULES v2 9.51% / 1.2817 / −12.05% and SPY 15.38% / 0.8786 / −33.72%; B136 7.98% / 1.1185 /
  −12.24%; SMALL439 3.85% / 0.5680 / −14.68%.
* Best OOS pick: U56 `BREADTH-DG 0.20 @ g=1.00`, **16.39% / 1.4563 / −14.16%** — 4b pass, 4a
  fail. It is idea 581's already-PARKed book, re-derived, not a new candidate; its IS dSharpe
  was **negative** (−0.0169), so rule 8 selected it *against* its own in-sample edge.

**No KEEP-candidate.** Every 4b passer here is a re-derivation of a book already in the record.

## What the record should take from this

1. The tie branch is a corpus-wide convention gap (185 sites, 90 scripts), not idea 592's bug.
2. It is inert on real books and severe on synthetic draw populations, so a flip rate quoted on
   a shuffle, bootstrap or permutation population needs an UNDETERMINED count beside it; a flip
   rate quoted on real books does not.
3. `sign_holds` carries the same gap in the opposite direction and has never been flagged.
4. Idea 592's tie count is a tolerance count; its mechanism sentence covers 99 of 342 rows.
5. The KEEP paths' own tie asymmetry (strict `>` on Sharpe, `>=` on drawdown) is visible in the
   grid — the live book scores a drawdown win against itself — and the useful fix is not a
   convention change but publishing the **margin** beside every KEEP verdict: 4 of 50 4b passes
   here sit inside 0.1 pp of a bar.

## Artefacts

`.console.txt` (the full 40-point grid and every table above) · `.sites.csv` (185 census sites)
· `.grid.csv` (40 points × 3 legs) · `.auc.csv` · `.ordering.csv` · `.cells.csv`
· `.shuffle.csv.gz` · `.walkforward.csv` · `.keeppaths.csv` · `.barmargins.csv` · `.gates.csv`.
Deterministic, no network, 298 s.

**SURVIVORSHIP:** B136 and SMALL439 are current constituents, so every *level* is biased up.
Every claim here is a clause-vs-its-own-control difference on a fixed panel, or a label count.
