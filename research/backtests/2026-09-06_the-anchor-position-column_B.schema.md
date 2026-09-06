# LEADERBOARD schema proposal - the anchor-position columns (idea 183, lane B, 2026-09-06)

Every "arm X beats control C" claim is a claim about the pair (X, position of C).  Three columns
make the second half readable.  All three are mechanical; none is tuned.

| column | definition | why |
|---|---|---|
| `ANCHOR-POS` | `i/K`, 1-based position of the control's value in the ORDERED grid of the dial that was swept | a control with no neighbour on one side is the cheapest thing on the ladder to beat |
| `ANCHOR-EDGE` | 1 if `i in {1, K}` | the single bit a reader needs; the headline count below is its mean |
| `ANCHOR-RANK` | rank of the control's OWN outcome among the K points, 1 = best | distinct from ANCHOR-POS: where it SITS vs how it DID |

Write `n/a` when the claim has no swept ladder behind it.  Never re-anchor a ladder onto its
nearest point when the incumbent is absent from the grid - record `n/a` and say so.

## Back-fill over the committed record (10593 auditable ladders, 29 files)

* **18.4%** of all auditable ladders have the control at a GRID EDGE
  (49.7% over the five headline dials GROSS/COUNT/VOLCAP/VOLPOW/CADENCE).
* Of the **1656** ladders where a uniform random draw beats the control in expectation -
  i.e. the claim the record actually makes - **64.4%** had the control at an edge.
* The CADENCE dial drives it: **79.4%**
  of cadence ladders in the record START at W, so RULES v1's own cadence sits on the low edge of
  its own grid with no faster neighbour to be averaged against.
* The pooled cross-dial over-representation ratio (3.50x) is a **Simpson artefact** of mixing
  COST (0.3% edge share, 7402 of 10593 ladders) with BAND/SLEEVE (edge-anchored by construction,
  RULES v1 having neither dial).  Stratified on the five headline dials it is 0.81x - an edge
  anchor is NOT more likely to have been beaten.  The finding is the level, not the ratio.
* Re-anchoring the same ladders at every GRID POSITION (nothing forces a coordinate to any
  particular beat-rate): a uniform draw beats the control **0.864** of the time at the HIGH
  grid edge, **0.211** at the middle and **0.166** at the LOW edge - a
  **0.698** swing from moving the control alone on otherwise identical ladders.
* The bias is TWO-SIDED.  Because the record's dials are predominantly increasing in their grid
  coordinate, a LOW-edge control is often the ladder's best point and is therefore unusually
  HARD to beat (median claimed margin at an edge is 0.58x the margin at the middle).  A
  reader cannot sign the bias without the position, which is the argument for the column.

## Reproduction

Idea 173's published `.anchorposition.csv` is reproduced from its `.grid.csv` to
< 1e-12 on all 90 rows, and its headline constants 0.74 / 0.32 re-derive exactly.
