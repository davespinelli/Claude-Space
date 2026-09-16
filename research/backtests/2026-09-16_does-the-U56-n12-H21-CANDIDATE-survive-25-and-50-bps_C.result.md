# Idea 1094 (lane C, 2026-09-16) — does the U56 n=12 / H=21 CANDIDATE survive 25 and 50 bps?

**ANSWERED = YES, IT SURVIVES BOTH, AND THE QUEUE'S COST-EXPOSURE PREMISE IS KILLED. The
candidate clears every 4b leg full-sample AND out of sample at 25 and at 50 bps, and breaks at
63 bps — on the HALVES SHARPE leg, not the CAGR floor. But the run replaces the objection it
removed with a sharper one: the candidate's rule-8 REACHABILITY dies between 10 and 15 bps,
roughly FIVE TIMES earlier than the cell itself. Still PARK, still NOT proposed, no RULES change,
no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.** SELECTION: lane C takes the SECOND open idea; 1094 was the second line
under '## Open' and names no EDGAR / Form 4 / 8-K / options / live-data source.

**THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4).** N {5, 8, 10, 12, 15, 20, 25, 30, 40} x
H {21, 63, 126} — 1082/1086's grid verbatim — = 27 cells per panel, 54 in total, ALL published at
ALL 11 published rungs (594 (cell, rung) pairs). **COST IS NOT A DIAL THE BOOK CAN CHOOSE.** It is
PROTOCOL rule 2's execution assumption; nothing here is selected on it, the rule-8 choosers are
re-run SEPARATELY at every rung (each sees only the cost its own book pays), and the verdict is
quoted at the harshest rung the queue asked for. Everything else frozen at 936/1064/1071/1082/1086's
construction: cap INF, CAND20 legs, max_vol 0.60, gross 0.75, W cadence, LAG 1.

**THE COST LADDER IS EXACT, NOT RE-RUN.** `engine.backtest` computes `r = (held*rets).sum - turnover
* c/1e4` and neither `held` nor `turnover` depends on cost, so one run per cell gives the whole
ladder exactly. **G1/G1b/G1c check this against `engine.backtest` at 10, 25 and 50 bps at
1.39e-17** — which is what licenses the 201-rung fine ladder (0..200 bps in 1 bp steps) used to
solve each cell's BREAKEVEN rung c\*.

**THE ANSWER.** U56 n=12, H=21 at 0 / 10 / 25 / 50 / 75 bps: CAGR **17.64% / 16.80% / 15.54% /
13.48% / 11.46%**, Sharpe **1.2131 / 1.1625 / 1.0865 / 0.9595 / 0.8322**, MaxDD **−19.45% / −19.48%
/ −19.51% / −19.61% / −19.75%**, halves **1.301/1.150 → 1.248/1.102 → 1.167/1.029 → 1.033/0.907 →
0.898/0.785**, OOS **18.45%/1.1919 → 17.57%/1.1426 → 16.26%/1.0685 → 14.11%/0.9448 → 12.00%/0.8209**.
Against SPY (full 15.10% / 0.8829 / −33.72%, halves 0.9588/0.8207; OOS 15.21% / 0.8711 / −33.72%;
DD cap 20.23%, CAGR floor 10.57%) it **passes all five 4b legs and all three OOS legs at every rung
up to and including 63 bps**, and fails at 64 on **L_H1** (H1 Sharpe falling under SPY's 0.9588),
with **L_CAGR still clearing by +0.9 pp at 75 bps**. c\*_OOS = 64 bps. The pass set is contiguous
from 0 at **54 of 54 cells** (H_MONO PASS), so "breakeven rung" is a well-defined object here.
**H_DIE25 and H_DIE50 both FAIL; H_LEG FAILS.** The rival reading declared in advance — that a
book binding on drawdown at 10 bps would die on the CAGR floor as cost rose — is wrong: cost
reaches the **Sharpe** legs first, because SPY pays no turnover and the book's vol barely moves.

**THE QUEUE'S 2.4x TURNOVER PREMISE BUYS ONE BASIS POINT.** H_QUEUE technically PASSES —
c\*(12,21) = **63** bps against c\*(12,126) = **64** bps — but the gap is **1 bp on a 2.4x turnover
ratio** (7.19x/yr vs 3.04x/yr), because the two cells bind on different legs: the H=21 cell on
L_H1, the H=126 cell on **L_DD**, which cost barely moves. **D1 quantifies why:** over 0→50 bps the
mean cell loses **1.66 to 4.69 pp of CAGR** and gains only **0.07 to 0.51 pp of |MaxDD|** — a ratio
of **8x to 42x**. A book whose binding leg is drawdown is nearly cost-immune on that leg; the rung
is a statement about the Sharpe and CAGR legs alone.

**THE MOST COST-ROBUST CELL IN THE FAMILY IS THE INCUMBENT, NOT THE CANDIDATE.** U56 **n=20,
H=126** — 936/1071's own construction — clears 4b full and OOS at **every rung to 117 bps**
(c\*_OOS 149), at 2.90x/yr turnover: 50 bps leaves it at **14.25% / 1.0535 / −19.35%**. **H_FAMILY
FAILS** (c\* spread across the nine cells that pass at 0 bps is **109 bps**, not ≤10), so the rung
is emphatically NOT a family-turnover fact: c\* runs 8 / 36 / 38 / 40 / 50 / 63 / 64 / 68 / 117 bps
across the passing cells, and **H_CSTAR_TURN PASSES at Spearman(c\*, turnover) = −0.65** — churn
predicts cost fragility, but loosely, and the binding leg predicts it better.

**GATES 12 of 12, printed before any result number.** G1/G1b/G1c the exact cost ladder ==
`engine.backtest` at 10/25/50 bps, 1.39e-17; G2 CROSS-RUN 936/1071/1082's committed W/H126 N=20
triple 3.18e-07; G3 SPY OOS triple 1.70e-04; **G4 CROSS-RUN 1086's committed candidate — both
triples, full and OOS — at 0.00e+00, bit-identical**; G4b/G4c its committed turnovers 7.19x and
3.04x/yr at 3.6e-04 and 6.4e-04; G5 live RULES v2 MaxDD == −12.05% at 4.95e-05; G6 CAGR
non-increasing in the rung at all 54 cells, 0.00e+00; G7 determinism 0.00e+00; G8 the cost axis is
live (9.11 pp of U56 CAGR spread). **HYPOTHESES 7 of 11** — H_DIE25, H_DIE50, H_LEG and H_WF50
fail, and the first three failures ARE the result.

**RULE 8, AND THE NEW OBJECTION.** (N, H) chosen on IS 2009-2016 ALONE by three choosers at each of
11 rungs, OOS 2017-2026 read ONCE. **H_WF25 PASSES (1 of 6 picks at 25 bps); H_WF50 FAILS (0 of 6).**
The reachable band is **0 to 30 bps**: at 15 bps and above **U56's IS-Sharpe chooser stops picking
the candidate** and switches to (n=5, H=63), which fails 4b on drawdown at every rung; from 15 to 30
bps the only surviving reachable pass is C_ISDD's **(n=40, H=21)** (25 bps: OOS 12.18% / 1.0636 /
−19.37%), and by 40 bps that chooser moves to (40, 63) and nothing is reachable at all. **So the
property 1086 headlined — "the first cell in this family an honest IS-only procedure reaches" — is
itself the most cost-fragile thing about the candidate, dying at roughly a fifth of the rung the
cell dies at.** **H_HOLD PASSES 6 of 6:** every (panel, chooser) sequence moves weakly to LONGER
holds as the rung rises, which is the queue's mechanism showing up where it actually lives — in the
CHOICE, not in the cell. **H_4A PASSES: 0 of 594 (cell, rung) pairs clear 4a**, at any cost, on
either panel. Grid totals, U56: 4b full **8 / 7 / 7 / 5 / 4 / 1** at 0 / 10 / 25 / 40 / 50 / 75 bps;
B136: **1 / 1 / 1 / 1 / 1 / 0**, the lone survivor being (15, 126), c\* = 68 bps. Benchmarks: U56
RULES v2 live **8.62% / 1.2007 / −12.05%** at 10 bps, **8.33% / 1.1631 / −12.09%** at 25, **7.85% /
1.1004 / −12.16%** at 50; B136 SPY full 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72%.

**D2 — THE CANDIDATE'S COST ROBUSTNESS IS NOT A COIN FLIP.** 40 gross-matched random-rank draws at
the same cell (1082/1086's seed recipe, same hold, no eligibility gate) turn over **12.91x/yr**
median against the book's 7.19x and clear 4b at **0.050 / 0.025 / 0.000** at 0 / 10 / ≥15 bps; the
median null c\* is **9 bps** against the book's **63**, and the book sits at percentile **1.000** of
the null c\* distribution. Whatever else is wrong with this candidate, its survival to 63 bps is not
something a random book of the same shape does.

**D3 — THE BENCHMARK ASYMMETRY, BRACKETED RATHER THAN ASSERTED.** PROTOCOL's 4b bar is SPY
buy-and-hold, which pays no turnover at any rung, so raising the rung is a one-sided handicap (the
record's open idea 1063). Charging SPY the BOOK's own turnover at the same rung — the opposite
extreme — flips **no verdict** in the eight (panel, cell, rung) pairs examined: U56 (12,21) and
(12,126) pass under both conventions at 25 and 50 bps, B136's fail under both. The convention is
one-sided; on this question it is not load-bearing.

**SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-CONSTITUENT lists. Every level is optimistic,
every 4b count an UPPER bound, and **every breakeven rung c\* published here is an UPPER bound on
the cost a real book of this shape could have paid** — the survivorship bias flatters the numerator
of the margin and not the turnover in the denominator.

**WHERE THIS LEAVES THE CANDIDATE.** 1086's memo gave five reasons not to promote. This run
**removes reason 5** (cost exposure: the 2.4x turnover ratio costs it 1 bp of breakeven, and it
absorbs 50 bps with all eight legs intact) and **adds a better one**: what an IS-only procedure can
REACH is far more cost-fragile than what the cell delivers, and above 10 bps the candidate is a
cell no honest procedure selects. Reasons 1-4 (undecidable DD margin, panel fragility, unstable
hold choice, 0 of 4a) stand untouched. **PARK, memo updated, NOT proposed for capital.**

Script `research/backtests/2026-09-16_does-the-U56-n12-H21-CANDIDATE-survive-25-and-50-bps_C.py`,
8 CSVs, console log, memo, 5 LEADERBOARD rows. Follow-ups filed: 1096 (is rule-8 REACHABILITY a
cost-rung object across the record's committed picks), 1097 (is c\* predictable from binding-leg
margin / turnover alone), 1098 (are the record's committed cost claims priced on the CAGR leg when
the SHARPE legs bind first).
