# Memo — proposed PROTOCOL clause 11b wording (idea 207, cloud, 2026-09-05)

Not a RULES change and not a KEEP candidate: no book is proposed and `RULES.md`, `scan.py`,
`bot.py` and `baseline.py` are untouched. This is the draw-count answer idea 207 was queued to
produce, for a Sunday review to adopt or reject as a PROTOCOL edit.

**Proposed clause 11b (replaces idea 186's wording).** An instrument's null band is the **95th
percentile** of |Δmetric| over **100** matched null draws — **not** the maximum. Publish the
band, the number of draws, and the band's own sampling sd beside every `clears` verdict. Read
any verdict whose |margin| is below **0.010** as undetermined. The clause is **report-only**:
it may not gate, select, or promote.

**Why the maximum must go.** `max` of K draws is the (K/(K+1)) order statistic, so K sets the
test's size, not its precision: on the 180-row corpus the band rises **+65.9%** (0.1686 →
0.2797) from K=20 to K=200, the clear rate falls **15.6% → 2.2%**, and the band's absolute
sampling sd does **not** fall (0.0502 → 0.0492). Idea 186's K=20 is a 4.8% test; K=200 is a
0.5% test; neither is more precise than the other.

**Why 100, and why Q95.** The Q95 band's level is stable (**+6.7%** over the same ladder) and
its sd falls **0.0242 → 0.0076 = 1/3.18** against sqrt(10) = 3.16 — exactly 1/sqrt(K), which
is what makes a draw count meaningful. At Q95/K=100 the pairwise flip rate across disjoint
blocks is **2.5%** (7.7% at K=20), the undetermined zone is |margin| < **0.0097** (0.0921 at
K=20), and 16.1% of the corpus lies inside it. K=200 doubles the cost for no measured gain here.

**What does not change.** Every clause-gated rule-8 selector, at every K and both statistics,
loses to the do-nothing control (best −0.0145, worst −0.0652; S0 0.7766 mean OOS Sharpe), and
all **28 of the corpus's 28 4b passes are inside their own band even at K=200**. More draws
buy a readable column, not a decision rule.
