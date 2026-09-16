# Memo — the TRANCHE-LIFT clause (idea 999, lane C, 2026-09-16)
Proposed as a PROTOCOL rule 4 reporting clause. **NOT applied** (rule 6: rules change only at
Sunday review). Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` was
touched by this run.

**Exact wording, to be added to PROTOCOL.md rule 4 if the Sunday review adopts it:**

> *A claim that phase-tranching (averaging a book over all P rebalance phases) improves a book's
> 4b standing is published with (a) the cell's mean pairwise phase-book correlation, (b) the same
> cell's null 4b base rate under BOTH estimators, and (c) the null's median OOS |MaxDD| under
> both estimators against the cell's own 0.60 × |SPY MaxDD| cap. A tranche gain is reported as a
> DOUBLE CROSSING of the drawdown cap and the CAGR floor, never as a property of the
> construction: over 30 (panel, book, cadence) cells the correlation's regression on the lift is
> negative at every cadence but explains only R² 0.2356, an in-sample correlation reading ranks
> the out-of-sample lift at Spearman −0.3653, the in-sample lift ranks it backwards at −0.2504,
> and book width over k = 9.9 → 91.7 adds adjusted R² −0.0180. The lowest-correlation cell in
> that grid (B136/TOP10/Q, 0.9081) carries a lift of −0.050 while a cell 3.2 points more
> correlated (U56/TOP40/Q, 0.9398) carries +0.990, so correlation alone is not a licence to
> claim the gain. Any lift quoted from fewer than 100 null draws states its resolution
> (±0.100 at 50 draws, ±0.200 at 25).*

**Why.** Idea 975-TRANCHE published the lift as living "where the phase-books differ". This run
fit it and the mechanism is elsewhere: the tranche compresses null drawdown by a stable
+0.84 pp (median +0.91, positive in 23 of 30 cells) everywhere, and that compression converts to
4b passes only where a cell already sits within ~1–3 pp of a cap fixed outside it. All 6
positive lifts are U56/M and U56/Q; B136 collects 0 of 15 because its null median drawdown
starts 3 pp too far out. On the REAL books the tranche moves 7 of 40 4b passes to 9 of 40, and
in the largest-lift cell of all (U56/TOP40/Q, null base rate 0.010 → 1.000) the real book still
fails on `L4_DD` at −22.16%.

**Evidence.** `2026-09-16_is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION_C.py`,
40 cells / 240 REAL / 19,200 NULL rows, gates 9 of 9 including exact cross-run of 975-B's
committed `phasecorr.csv` (12 of 12 cells, 1.11e-16) and its `nulls.csv.gz` (5,760 rows,
2.22e-16). Rule 8: 2 of 8 IS-only picks clear OOS 4b, both of them 964's already-published
`EWELIG` tranche; the correlation chooser this idea was asked to build is **0 of 2**. OOS 4a
0 of 8. Survivorship: current-constituent panels raise phase-book correlation and so bias the
predictor toward the no-lift end — against this memo's own hypotheses, not for them.
