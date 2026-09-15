# Idea 945 (cloud, 2026-09-15) — ANSWERED = NO / KILL

**Question.** Idea 943 found the gross-matched null's median cadence gain is negative at 0 bps and
positive at 10/25/50, so a book beats its null on 6 of 16 cells at one rung and 0 of 16 at the next.
Does that *rung reversal* generalise to the record's other turnover dials?

**Answer: no, and the premise needs one correction.** 5 dials × 3 panels × 4 cost rungs = 60 book
rows, 24,000 null rows, 60 gain cells, all published. **0 of 15 (panel, dial) cells show 943's
shape.** The cells split three ways: 7 positive at both rungs (cadence ×3, width ×3, eligibility on
SMALL), 4 POS→NEG — the *opposite* flip (gross ×3, eligibility on B136), 4 negative at both rungs
(band ×3, eligibility on U56).

**The correction.** 943's "negative at 0 bps" is a **median over its 16 cells** (−0.0279, positive on
only 2 of 16), not a property of any one cell. The record's own standing-candidate cell, U56 W→M, is
one of those 2 positive cells. This run reproduces it at **+0.0540 / +0.3419 / +0.7712 / +1.4620**
against idea 931's committed **+0.0466 / +0.3334 / +0.7624 / +1.4501** — ≤ 0.012 at every rung. So
943's aggregate is right about its family and wrong as a statement about any single book.

**The mechanism.** The rebate is priced off the **null's own** turnover drop, not the book's:
corr(predicted, observed 0→10 bps shift) = **+0.8213** using the null's drop, **+0.4460** using the
book's. A coin flip turns over 27–51/yr more weekly than monthly; the book only 5.9–10.6. Two
instructive exceptions: **gross is Sharpe-neutral** (halving it halves turnover *and* vol, so the
rebate cancels — predicted +0.18 to +0.26, observed −0.002 on all three panels), and **tightening
eligibility raises turnover** on all three panels (G7 FAIL 12 of 15), so its "rebate" is a penalty.

**Rule 8.** Dial setting chosen on 2009–2016 by IS Sharpe, 2017–2026 read once. **OOS 4b 11 of 60,
4a 0 of 60.** All 11 passes are books already in the record; best is U56 monthly CORE/TOP20 @0 bps,
OOS 18.09% / 1.342 / −19.45% against SPY 15.27% / 0.874 / −33.72% and RULES v2 9.66% / 1.302 /
−12.03%. 4a is 0 of 60 — v2's OOS Sharpe with a −12% drawdown is not beaten in both halves anywhere.

**Gates 6 of 9; the three failures are reported as failures, no bar moved.** G3 misses on the
monthly leg by dCAGR 0.0059 against the record's own 0.005 bar (the same leg lane 931 failed). G6's
0.50 gross floor was written for CORE/TOPn and is wrong for the de-grossing BAND family (realised
gross 0.4286); the failure mode it was built to catch is gated exactly by G2, which passes at
3.33e-16. G7 fails on the eligibility dial, which is the finding above.

**Nothing promoted. No RULES change, no PROTOCOL edit (rule 6).** 943's proposed clause survives but
cannot be stated as a single sign: quote the null's median gain **at the claim's own rung, on the
claim's own dial**, and do not assume the 0 bps sign.

**SURVIVORSHIP.** U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52
tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown level is
optimistic and both 4b bars are easier here than on a point-in-time panel. A coin flip drawn from a
survivor panel is a better book than one drawn in real time, so every null gain is an upper bound and
every book excess a lower bound — which cuts against this run's own headline, not for it.
