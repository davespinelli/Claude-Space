# Idea 2067 (lane cloud, 2026-09-20) — is the FRACTION RULE's crash-excised edge RESOLVABLE?

**VERDICT: ANSWERED / KILL of the RESOLUTION (not of the sign).** Idea 2026's headline — the
ladder-free fraction threshold `h_t = f*g_t` keeps a POSITIVE turnover-matched-calendar edge on
the 2020-excised tape (+0.0377, 4 of 4 arms) where the incumbent constant `h = 0.12` does not
(-0.0050, 0 of 4) — **reproduces to 0.000e+00 and does not survive its own standard error.**

## What was done
The same paired circular-block bootstrap idea 2022/1537 use, applied to idea 2026's own statistic:
`d = Sharpe(book) - Sharpe(turnover-matched CALENDAR interp over R in {D,W,M,Q})`, with the
interpolation weight FROZEN at its full-sample turnover match and book / rung-A / rung-B resampled
on IDENTICAL day blocks. 42 FRACG cells (panel {U56, B136, SMALL665} x trade cadence {W, M} x
f {0.02 .. 0.50}) x 2 tapes (ALL, XCRASH = 2020-02-19..2020-03-23 excised) x 2 windows x 4 block
lengths, 2000 draws (8000 as a draw-count read). Two dials, both bootstrap dials: block length and
draw count. `t` is FIXED at 0.16 (inherited), cost 10 bps for the bootstrap, 0/10/25/50 for the
census. 9 of 9 gates pass, including exact reproduction of 2026's four published `d_matched_cal`
and `x_d_matched_cal` values and of the incumbent's four.

## The four numbers that answer the question
1. **V1 NOT TRIGGERED — the sweep is not resolvable.** On the XCRASH tape, OOS window, block 21:
   **2 of 42 cells (0.048)** have a 95% basic interval excluding zero; mean edge **-0.0204**,
   mean SE **0.0456**. On the FULL tape the edge is +0.0660 and 42 of 42 positive, but still only
   **11 of 42 (0.262)** resolvable. Excising 24 days does not merely shrink the edge — it moves the
   mean NEGATIVE across the ladder while the SE stays ~0.046.
2. **V2 NOT TRIGGERED — the committed "4 of 4" is 2 of 4 once it carries an interval.** Arm by arm
   (XCRASH, OOS, block 21): U56/W +0.0374 [+0.0029, +0.0739] RESOLVABLE; B136/W +0.0470
   [+0.0089, +0.0829] RESOLVABLE; U56/M +0.0277 [-0.0160, +0.0724] NOT; B136/M +0.0388
   [-0.0056, +0.0836] NOT. The incumbent's "0 of 4 positive" is likewise **0 of 4 resolvable**
   (every FIXH interval straddles zero at roughly +/-0.08, i.e. it contains the fraction rule's
   whole edge).
3. **V4 NOT TRIGGERED — the contrast that carries the headline is the weakest leg of all.** Paired
   directly on identical blocks, FRACG(0.10) minus FIXH(0.12) is **+0.0350, 6 of 6 arms positive,
   0 of 6 resolvable** (SE 0.021-0.040). Two separately-signed point estimates were never a
   difference test; the difference test does not clear.
4. **The pre-stated f\* = 0.10 sits ON the XCRASH ladder's peak.** The edge runs +0.004 / +0.005 /
   **+0.037** / -0.030 / -0.080 / -0.061 / -0.070 across f = 0.02 / 0.05 / 0.10 / 0.15 / 0.20 /
   0.30 / 0.50 on U56/W, and the same hump on B136 and SMALL665. The one rung that was pre-stated
   is the argmax of the ladder it was pre-stated on — a coincidence the record should carry
   beside the +0.0377.

## Stability and hygiene
**V3 TRIGGERED**: the V1 share moves 0.095 / 0.048 / 0.048 / 0.143 across blocks 5 / 10 / 21 / 63
(span 0.095 <= 0.20), so this is not a block-length artefact; at 8000 draws the share is unchanged
(0.048) and mean SE moves 0.0456 -> 0.0457. **10 of 42 FRACG cells are CLAMPED** (book turnover
outside the calendar ladder's range, so "matched" is a single endpoint rung, not a match); they
are flagged in every table and the matched-only share is reported beside the full one (0.0625).

## Capital (V5, both KEEP paths, every cell)
FRACG 4b FULL+OOS: **25 / 24 / 24 / 17 of 42** cells at 0 / 10 / 25 / 50 bps. **4a: 0 of 42 at
every cost rung** (live RULES v2's MaxDD is unbeatable by a 0.93-gross book, as the record already
holds). Rule-8 walk-forward (f chosen on 2009-2016 by four legal IS-only choosers, 2017-2026 read
once): **10 of 24 picks clear 4b FULL+OOS, 0 of 24 clear 4a**; picks land on f = 0.10/0.15 on
U56/B136 and on f = 0.50 on SMALL665, which clears nothing. Pre-stated arm at 10 bps: U56/M
15.81% / 1.2470 / -19.12% (OOS 16.55% / 1.2928 / -19.12%), B136/M 16.03% / 1.2364 / -17.00%
(OOS 16.10% / 1.2621 / -17.00%) against live RULES v2 U56 8.62% / 1.2010 / -12.05% (OOS 9.46% /
1.2766) and SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737). SMALL665 clears nothing on either
path at any f (binding L2_H2|L3_OOS|L4_DD|L5_CAGR), reproducing 2026's small-panel row.

**NO NEW KEEP IS FILED.** The 4b passes here are idea 2026's standing candidate re-scored, not a
discovery, and this run's own finding is that the evidence separating that candidate from the
incumbent constant is inside its own standard error.

## What this cannot do (stated, not repaired)
The bootstrap resamples DAYS in blocks, so it prices the sampling error of a Sharpe DIFFERENCE, not
the selection error of having chosen the crash window, the statistic or the family. The crash
window is idea 2022's, quoted; a different 24-day excision is a different experiment. SURVIVORSHIP:
U56/B136 are current-constituent lists and SMALL665 a current sub-$2B screen (54 tickers with
`max_1d_move >= 1.0` dropped first), so every CAGR/drawdown LEVEL is optimistic and both 4b bars
are easier here than on a point-in-time panel; the edge CONTRAST is same-tape/same-names/same-blocks
and first-order immune, the PASS COUNTS are not.
