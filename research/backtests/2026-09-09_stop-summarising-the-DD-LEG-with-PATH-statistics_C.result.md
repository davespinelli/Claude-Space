# IDEA 592 — stop summarising the DD LEG with PATH statistics (lane C, 2026-09-09)

**VERDICT: KILL of the proposed episode column, and a KILL of the premise it was built on.
Plus one methodological finding the record needs: the flip flag counts an EXACT TIE as a sign
change.** No promotion, no new book. RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md
untouched.

## The question, and what turned out to be wrong with it

Idea 592 asked whether an EPISODE-LEVEL statistic — which of the control's drawdown episodes the
clause was de-grossed through, at what depth — predicts the MaxDD flip "where the path statistics
cannot (best of 8 is the gross gap at AUC 0.640)".

That 0.640 is **not a number about the record's published cells**. Idea 584 measured it on its
own BLOCK-SHUFFLE population (`sh[sh.L > 0]`, 1,296 synthetic draws), not on the 216 real
de-gross cells. This run reproduces both populations and reports on both:

| | POP A — the record's 216 published DG cells | POP B — idea 584's 1,404 shuffle rows |
|---|---|---|
| MaxDD flips | 28 (13.0%) | 785 (55.9%) |
| of which EXACT TIES (`dU_MaxDD` = 0) | **0** | **342 (43.6%)** |
| PATH column ceiling | **AUC(SD) 0.9669**, GAP 0.7629 | 0.6171 pooled (0.6399 published, L>0) |
| PATH within-market (108 cells) | GAP and SD **0.9223** | — |
| best EPISODE grid point (96 scored) | 0.8266 (BINDRANK θ=0.05/deep) | 0.6757 within-group (BINDREL θ=0.05/deep) |
| episode points beating the path ceiling | **0 of 96** | see below |

The strongest case *for* the episode column, stated rather than buried: within the 108 market-DG
cells its best point (**EPMAXREL θ=0.05/deep, 0.9223**) exactly **ties** the path column's
within-market ceiling (GAP and SD, both 0.9223) — but it takes two tuned parameters to match a
parameter-free statistic, and it never beats it anywhere.

**On the record's own population the path column already orders the DD flips almost perfectly**
— AUC(GAP) is **1.0000 inside BREADTH and inside SPYTR** and 0.8796 inside DD, i.e. perfect
within the two families where the confound is not mechanical. So the record's DD-leg claims do
**not** need an episode column: the premise "no scalar summary of the path works" is a POP-B
statement that does not transfer.

## What the DD flip actually is on POP B (found at the provenance gate)

The record's flag is `sign(A − U) != sign(A − M)`, and `np.sign(0) = 0`. A book whose MaxDD
**equals** its control's is therefore labelled a flip. On POP B that is **342 of 785 "flips"**.
These labels are not merely close to zero, they are zero: G3d shows all 166 that changed under
the price restatement sit at a margin of **8.9e-16**, so **12% of POP B's MaxDD labels are
undetermined at the data's own precision**.

The episode reading of the ties is real but **partial, not an identity**: `BIND == 0` (the clause
never de-grossed through the binding episode) agrees with `|dU_MaxDD| == 0` on **83.26%** of
POP-B rows (251 both-true, 229 ties *with* non-zero cover — de-grossing on the **recovery leg**
of the binding episode also leaves MaxDD untouched — and 6 zero-cover non-ties).

**And the episode column's POP-B win is carried entirely by those tie labels.** Dropping the 491
undetermined rows leaves 913 with a 48.0% flip rate, and there the ordering reverses back:
**path GAP 0.7374 vs the best episode statistic 0.6310** (BINDRANK θ=0.10/flat, pooled).

## The decisive test, and a reversed pre-registration

The pre-registered direction was that flips carry a **low** binding-episode excess cover. It is
**reversed**: raw AUC(BINDREL) = 0.7715 on POP A — flips carry a *high* one. The placebo says why.
Circularly shifting the episode windows (episode count, lengths and depths frozen; only the
alignment destroyed) keeps most of the discrimination, because cover tracks the gross gap whatever
it is aligned to: real BINDREL 0.2285 vs shifted [0.1035, 0.5933] (real beats **1 of 8**),
BINDRANK 0.3785 vs [0.3494, 0.5218] (**2 of 8**); only EPMAXREL beats 7 of 8. The alignment —
the thing an episode column would add — carries nothing on POP A.

## Gates

- **G0 VINTAGE** — panels truncated to idea 584's window (4700/4699/4194 rows asserted exactly);
  U56 had gained one bar.
- **G1** runner vs `engine.backtest` max |dReturn| 1.4e-17. **G2** matched gross < 1e-12.
- **G3 PROVENANCE** — B136, whose cache is **bit-identical** between the two commits, reproduces
  idea 584's 108 cells and 468 shuffle rows to **9.9e-17** (the code-identity gate). U56 differs
  by 1.9e-06 because `data/prices.csv` was **restated** since idea 584: 23,250 of 272,600 shared
  cells changed, max **3.71e-4** relative (idea 257's known restatement). Cell flip flags agree
  exactly (0 of 972). On the 1,130 draws whose label agrees, the published ceiling re-derives to
  **|d| = 0.00e+00**, so the whole 0.0392 headline gap is undetermined labels moving, not this run
  scoring something else.
- **G4 EPISODES** — episodes partition the underwater time exactly and the binding episode's
  trough equals the control's MaxDD to 0.0e+00 on all 12 controls. **G5** placebo preserves
  episode count and length exactly.
- **PART E VINTAGE ARM** — U56's 72 DG cells re-run on the untruncated current panel: max |ΔAUC|
  over 36 (statistic × θ × weight) points = **0.0000**. The dropped bar changes nothing.

## Rule 8 (walk-forward, 2009–2016 pick → 2017–2026 untouched)

Identical to ideas 581/584, as it must be — the books are theirs. IS sign holds OOS on 16 of 27
picks. **4a 1/27, 4b 3/27 on the picks; 4a 6, 4b 50, BOTH 0 over all 324 grid points.** Every 4b
passer is a re-derivation of a book already PARKed in the record; no book here is new and none is
proposed for capital.

## Tuned parameters

Two, exactly as the queue allows: **θ** (episode-set minimum depth, 4 values) and **w** (depth
weighting: flat / dd / deep). All 12 combinations × 8 statistics are reported for both
populations in `.grid.csv`; the (dial, gross) book grid is idea 581's, unchanged, and all 324
cells are in `.cells.csv`. Survivorship: B136 and SMALL439 are current constituents, so every
level is biased up; every claim here is a clause-vs-its-own-control difference on a fixed panel.

## Follow-ups filed

594 (census the record for MaxDD/Calmar comparisons whose delta is an exact tie), 595 (does the
tie-as-flip convention change any published verdict), 596 (is the recovery leg the missing 17% of
the tie mechanism).
