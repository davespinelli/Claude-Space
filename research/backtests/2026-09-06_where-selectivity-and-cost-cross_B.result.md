# Idea 155 — where-selectivity-and-cost-cross (lane B, 2026-09-06)

**Verdict: KILL of the crossing.** The argmax selectivity does not move with cost. On the
two large-cap panels it does not even start on the selective side, so there is no crossing
to locate; on the small panel there is one, between 20 and 25 bps, on a panel that has now
failed 4b fifteen times.

**Answer to the pre-registered question.** At the protocol's own 10 bps the q that maximises
the net Sharpe premium over EWall is **0.90 on U56** and **0.95 on B136** — at or near 1.00,
as the queue guessed, and therefore a third independent derivation of idea 82's "drop the
ranking". The number it comes with is small: **+0.0316** (U56) and **+0.0171** (B136) Sharpe,
i.e. the entire value of RULES v1's composite on a large-cap panel is worth at most three
Sharpe hundredths, and only when it is used to *delete the worst 5–10%* rather than to pick a
top-n. Every q ≤ 0.75 loses to holding the whole eligible set.

**Why there is no crossing.** Turnover is exactly monotone in q — Spearman(q, turnover/yr)
= **−1.000 on all three panels** — so raising the cost rung shifts the premium curve down by
an amount that is itself monotone in q. That changes the level everywhere and the argmax
nowhere: U56's argmax is 0.90 at all seven rungs, B136's is 0.95 at all seven, SMALL484's is
0.30 through 25 bps. Costs are not what decides how selective to be.

**Idea 78's premise does not survive being read inside a panel.** Its "gross spread rises
with selectivity, net premium falls with pool size" was measured across sub-panels of
different sizes. At matched cash inside one panel, Spearman(q, **gross** premium) is
**+0.430 (U56)** and **+0.899 (B136)** — breadth already wins before a single basis point of
cost. Only SMALL484 reproduces the opposite sign (−0.359 gross), and there the tilt crosses
zero between 20 and 25 bps (−0.026 → +0.117). The "two curves of opposite sign" is a
cross-panel artefact, not a within-panel fact.

**The argmax's location is construction-dependent (do not quote 0.90 as a constant).** With
the same selectivity expressed as a *constant* count at equal cash, the U56 argmax moves to
0.55 and the B136 argmax to 1.00; under idea 78's raw `gross/n` convention the U56 argmax
drifts 0.85 → 1.00 as costs rise and B136's q=1.00 premium *rises* from +0.0279 to +0.0878
across the ladder — the latter is pure cash, idea 157's channel showing through again. What
is robust across all four constructions and all seven rungs on the large-cap panels is only
the direction: **the optimum sits in the top decile of q; nothing selective wins.**

**Rule 8 kills the parameter outright.** With q chosen on 2009–2016 and 2017–2026 read once,
the in-sample chooser picks **q = 0.15 (U56)** and **q = 0.10 (B136)** — the far end of the
ladder from the full-sample argmax — and loses **−0.1881 / −0.2439 / −0.0764** OOS Sharpe
against doing nothing (holding q = 1.00), mean **−0.1695**. The cost-blind chooser loses
−0.1253 and a *random* q loses only −0.0213, so both informed selectors are worse than the
size-matched null. OOS levels: do-nothing 1.1133 / 1.0191 / 0.4086; SPY 0.8820; RULES v1
0.7471 / 0.5763 / 0.5540. This is the tenth time in the record that selecting a dial out of
sample loses to not selecting it.

**KEEP paths, all 420 points.** 4a 45/420 (B136 8/7/7/6/5/5/5 across the rungs; **U56 0 of
140**, always on drawdown against the live low-vol book — idea 136's standing diagnosis;
SMALL484 2/140). 4b 47/420. At 10 bps, 4b passes for q ∈ [0.55, 0.95] on U56 and q ∈ [0.80,
1.00] on B136, intersection **q ∈ [0.80, 0.95]**; nothing passes on B136 at 15 bps or above.
**SMALL484 passes 4b 0 of 140 — the fifteenth reproduction of idea 136.**

**PARK, not KEEP, and nothing is proposed.** A *pre-registered* top-decile trim (q = 0.90,
never chosen) does clear 4b at 10 bps on both large-cap panels while the q = 1.00 endpoint
misses it on U56 by 0.23pp of CAGR. It is parked rather than proposed for three reasons that
are all in the run's own output: the margin (+0.0072 Sharpe on B136) is smaller than the
sign change the same selectivity takes under a constant-count construction (−0.0018); rule 8
shows the ladder position is not selectable, so "q = 0.90" can only ever be a full-sample
argmax; and per idea 144 a re-dialled book is the same book. Costs at 15 bps and above erase
it on B136 entirely.

**Reproduction.** Idea 2's U56/CAND20 row, the live RULES v1 row and idea 78's published
B136 trio all reproduce to |d| ≤ 0.0002 (EWall 1.0261, CAND20 0.9569, CAND5 0.8802, ordering
intact). The cost-ladder identity `net(c) = gross − turnover·c/1e4` holds at **0.000e+00**,
which is what makes the seven rungs exact rather than re-simulated.

**Caveats.** Current-constituent survivorship on `universe_broad.json` and on the small
panel (idea 54); every arm inherits it equally, so the paired premia are unaffected and no
*level* here is tradable. The ladder's q = 1.00 endpoint is EWall over the *rankable*
eligible set and sits 0.0009 Sharpe below plain EWall (713 unrankable-but-eligible cells on
B136 across 426 of 4699 days) — every premium in this run is measured against that endpoint,
not against plain EWall. The 20 q points are not independent draws, so no p-value is quoted
on the argmax. Ideas 38, 126, 136 and 144 carry over.

**Follow-ups queued:** 227, 228, 229.
