# Idea 1425 — does the frozen incumbent's weight vector carry ANY drawdown information at all?

**2026-09-22, lane cloud, run 11.  Script:** `2026-09-22_incumbent-weight-vector-dd-information_cloud.py`
**Verdict: ANSWERED, and the answer splits.  The axis is LIVE and OOS-PERSISTENT, but it is
IMMATERIAL and ORTHOGONAL to the leg that actually binds.  KILL as a capital device; no KEEP
candidate on either path.**

## What was measured
The live RULES v2 book (equal weight inside the 200d ±3% band) was re-sized by random weight
vectors over **its own held set at its own gross on every rebalance date** — same names, same
exposure, same cadence, same t+1 execution, same costs — and the equal-weight anchor's PROTOCOL 4b
drawdown margin was placed inside that distribution.  Two tuned parameters (Dirichlet/Gamma
concentration α ∈ {0.5,1,2,5,20,100}, draw count ∈ {50,200}); panel, null shape and cost rung are
reported axes.  240 cells published.

**Two null shapes, because a re-sizing null is not automatically turnover-matched.**  `IID`
(fresh draw every week) trades a median **18.1x/yr** against the anchor's 1.77x and is therefore a
joint test of sizing and trading — published, but read only at 0 bps.  `PERS` (one multiplier
vector held for the whole sample) trades **1.93x/yr on u56 and 2.10x on broad** against the
anchor's 1.77x / 2.01x, and is the null that answers the question.

**A bug caught by the gross-match gate, stated because it changed the answer.**  The live book
weights `gross/N_PRICED` and sends gated-out weight to CASH, so its realised gross is
`0.75 × N_held/N_priced`, not 0.75.  A first cut normalised each draw to a flat 0.75, handing the
null ~2x the anchor's exposure and 4.3x its turnover, and read the anchor at the 100th percentile
on every cell.  G2 now requires each draw to carry the anchor's **own** gross date by date and the
anchor passed through the identical pipeline to reproduce `rules_v2_weights` to 3.5e-18.  Every
number below is post-fix.

## The answer to the filed question: the anchor sits MID-BAND
Over all 60 (panel × α × cost) PERS cells at 200 draws, the anchor's 4b DD margin sits at
percentile **median 52.0, range [45.5, 58.5]**; its Sharpe percentile median 62.5 [50.0, 83.0];
its **CAGR percentile median 53.5 [47.0, 62.0]**.  On the idea's own stated criterion — *"if the
anchor sits mid-band, intra-book sizing is a dead axis"* — equal weight is **not special**.

## But the axis is not noise: it is OOS-persistent, and worth 0.66 pp
Rule 8 (chooser sees 2009–2016 only, 2017–2026 read once): the IS-only DD chooser `C_DD` beats the
anchor's OOS MaxDD at **60 of 60 cells**, landing at OOS-DD percentile **median 95.5 (mean 90.7)** —
in-sample drawdown ranking of a weight vector genuinely survives out of sample.  `C_SHARPE` lands
at OOS-DD percentile 52.2, i.e. picking on Sharpe finds none of it.

**It is worth 0.66 pp.**  `C_DD`'s OOS MaxDD is a median **−11.52%** against the anchor's −12.18%,
and the null's whole DD-margin spread narrows as α tightens: sd **1.17 / 0.77 / 0.49 / 0.33 / 0.17 /
0.07 pp** at α = 0.5 / 1 / 2 / 5 / 20 / 100.  At any dispersion a real sizing rule would produce,
the **entire** re-sizing null is inside a small fraction of the record's own committed 2.93 pp
drawdown-leg SE (idea 1511).  A sizing result of this size is not resolvable by this record.

## And it cannot move the leg that binds
The anchor clears 4b in **0 of 60** cells and the draws in **107 of 12,000 (0.9%)** — all 107 on u56
at α ≤ 2, where the null is near-degenerate (a handful of names carry the gross), i.e. concentration
risk, not sizing.  **0 of 60 `C_DD` picks clear 4b** and 0 of 60 clear 4a.  The reason is direct: the
live book's binding 4b leg is the **CAGR floor** (anchor 8.62% against SPY's 15.14%, floor 10.60%),
and the anchor sits at the **53.5th percentile on CAGR** — re-sizing buys drawdown the book does not
need and cannot buy the return it does.  u56 @10 bps the anchor reads 8.62% / 1.2010 / −12.05%
(halves 1.2276/1.1806, OOS 1.2767) against SPY 15.14% / 0.8851 / −33.72% (OOS 0.8751).

## Consequence for the record
Every committed intra-book SIZING result, read against this null, is a draw from a distribution
whose 90% width is under 1.2 pp of drawdown and under 0.08 of Sharpe at α ≥ 5 — and one whose
centre is the anchor.  A sizing finding is only a finding if it states its α-equivalent dispersion
and clears this width.

## Caveats
Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are current constituents, so every CAGR
level is optimistic and both 4b bars are easier than on a point-in-time panel; the anchor-vs-null
contrast is same-tape / same-names / same-gross and is first-order immune.  Gamma coordinates are
i.i.d., so this is a SIGN-FREE null: a null that tilts on a characteristic (vol, beta, size) is a
different test and is not run here — `C_DD`'s persistence is consistent with it having found such a
tilt, which this run does not identify.  PERS matches turnover by construction but not exactly
(1.93x vs 1.77x); its realised turnover is published, not asserted.  One cadence (W), one delay
(t+1), one gate (200d ±3%).  Flat costs, no spread/impact/borrow.  Moving 50 → 200 draws moves the
anchor's DD percentile by a median of 4.5 points, so percentiles here are ±5 points, not ±1.
