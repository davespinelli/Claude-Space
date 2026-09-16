# Idea 1096 (cloud lane, 2026-09-16) — is RULE-8 REACHABILITY a COST-RUNG object across the record's COMMITTED PICKS?

**ANSWERED = NO, NOT AS A GENERAL FACT.** 1094's numbers reproduce EXACTLY and its reading does
not generalise: across the record's committed rule-8 ladders **only 2 of 8 CORE picks move at or
below 25 bps**, 3 of 8 never move within 200 bps, and the median MOVE RUNG is **71 bps** against a
median c\* of **117 bps** — a ratio of **1.65x**, not 5x. **KILL of the queue's own generalisation
(H_MOVE, H_5X, H_TURNSPREAD, H_DIR, H_VERDICT all FAIL), CONFIRM of 1094's specific numbers
(c\* = 63 bps at 0.00e+00; its 15-bps switch reproduces to the bp on its own published ladder), a
CORRECTION (that 15 bps is 1094's RUNG SPACING — on a 1-bp ladder the switch is at 11 bps), and
two structural findings that matter more than the headline.** No RULES change, no book promoted,
no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

SELECTION: this lane takes the FIRST open line for idea 1. QUEUE carries TWO lines numbered 1096
(idea 932's defect again); this is the rule-8-reachability one, not the gate one.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**CLAIM SET {CORE, WIDE} x COST RUNG {0, 10, 25, 50} bps = 8 cells, ALL published.** CORE = the
four ladder families the record's committed rule-8 runs actually walked — N {5,8,10,12,15,20,25,
30,40} (1071/1082/1094), H {21,63,126,252} (1086), GROSS {0.30..0.75 in 10 rungs} (1083), CADENCE
{D,W,M,Q} (930/931) — on both panels, 8 ladders. WIDE adds the joint (N,H) grid, the book family
{TOP5,TOP10,TOP20,EWELIG,BAND03} and a max_vol ladder, 6 more. **146 cells, 48 (panel, ladder,
chooser) picks, 192 priced picks, 201 fine cost rungs.**

**COST IS NOT A DIAL THE BOOK CAN CHOOSE.** It is PROTOCOL rule 2's execution assumption; every
chooser is re-run separately at each rung and only ever sees the cost its own book pays. The
CHOOSER axis {C_ISSHARPE, C_ISDD, C_ISCAGR} is REPORTED at every cell and never fitted on — the
headline is C_ISSHARPE, the record's default, fixed before the run. FROZEN: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, W, min hold 126, LAG 1, warm-up 260, IS end 2016-12-31 (each except
where it is the dial). D1–D4 are labelled post-hoc diagnostics and are excluded from every count.

## THE ANSWER — HOW MANY PICKS MOVE, AND AT WHICH RUNG

C_ISSHARPE, vs the pick each ladder states at PROTOCOL's 10 bps:

| | @0 bps | @25 bps | @50 bps | move within 200 bps | median MOVE RUNG | median c\*(10-pick) |
|---|---|---|---|---|---|---|
| CORE (8) | 0/8 | **2/8** | 2/8 | 5/8 | **71 bps** | 117 bps |
| WIDE (6) | 1/6 | 1/6 | 1/6 | 5/6 | 142 bps | 43 bps |
| ALL (14) | 1/14 | 3/14 | 3/14 | 10/14 | — | — |

C_ISDD moves 0/14 at 25 bps and 2/14 at 50; C_ISCAGR 1/14 and 2/14. **H_MOVE FAILS** (declared: a
majority of CORE picks move by 25 bps; observed 2 of 8). The two movers are both U56: the HOLD
ladder at **14 bps** (H=21 -> 63 -> 126) and the CADENCE ladder at **21 bps** (W -> Q). Everything
else is cost-stable across the queue's whole range, and the GROSS ladder's pick does not move
anywhere in 200 bps on either panel.

**H_5X FAILS, and the two ways of computing it disagree by 3x — which is itself the finding.**
Ratio of medians **117/71 = 1.65x**; median of per-ladder ratios **5.04x**, but that median is
taken over the **2 of 8** CORE picks where both quantities exist at all. 1094's "~5x" is the
second statistic on the two U56 ladders where it is defined; it is not a property of the record's
picks.

**H_ABSORB PASSES 8 of 8 on CORE** — once a CORE C_ISSHARPE pick moves it never returns, so
"the rung at which the pick moves" is a well-defined object here (2 of 48 picks across all
choosers do flicker, both with a 0-bps move, i.e. a pick that differs at zero cost and returns).
**H_DIR FAILS 1 of 8**: B136's N ladder moves 8 -> 5 at 82 bps, i.e. toward HIGHER turnover —
that move is noise, not cost. **H_TURNSPREAD FAILS**: the movers are not the widest-turnover-
spread ladders (the GROSS ladder spans 1.21–2.90x/yr of turnover and never moves; the CADENCE
ladder spans 1.65–4.06x and moves at 21 bps). **H_VERDICT FAILS**: over {0,10,25,50} bps identity
moves in 11 of 48 picks while the 4b-full verdict changes in 8 and 4b-OOS in 9 — identities are
marginally LESS stable than verdicts, not more.

## CONFIRM, AND A CORRECTION TO THE RUNG AT WHICH 1094'S CHOOSER SWITCHED

G4 reproduces 1086/1094's U56 N=12/H=21 candidate triple at **0.00e+00** and G4b its breakeven
**c\* = 63 bps at 0.00e+00**; G2 reproduces 936/1071/1082/1094's W/H126 N=20 triple at 3.18e-07.
**D1 (labelled):** on 1094's EXACT joint grid (H restricted to {21,63,126}) and its own published
rung ladder {0,5,10,15,20,25,30,40,50,75,100}, the U56 IS-Sharpe chooser first differs from its
10-bps pick at **15 bps** — 1094's number, to the bp. On a **1-bp** ladder the same chooser
switches at **11 bps**. 1094's "15 bps" is the resolution of its own ladder, not the switch; the
switch is 11 bps and the destination (5/63) is unchanged. The record should quote 11.

## TWO STRUCTURAL FINDINGS THAT MATTER MORE THAN THE HEADLINE

**D2 — for 76.2% of picks the question has no referent.** c\*(10-bps pick) is UNDEFINED — the pick
already fails 4b at **zero** cost — for **32 of 42** (panel, ladder, chooser) picks. On B136 every
single chooser on every ladder lands on a cell that fails 4b at 0 bps. "The procedure is more
cost-fragile than the cell" can only be asked of the 10 picks that clear 4b uncharged, and 1094
generalised from two of them.

**D3 — reachability is a property of the LADDER, not of the book.** The anchor cell (936/1071/
1082/1094's W / H=126 / N=20 / gross 0.75 book — the standing top-20 family) is a rung of ALL
FOUR CORE ladders. C_ISSHARPE reaches it from **2 of 4** at 0 and 10 bps on both panels (GROSS and
CADENCE), 1 of 4 at 25 bps on U56, 2 of 4 at 50 bps. The N ladder picks 40 (U56) / 8 (B136) and
the H ladder picks 21 (U56) / 63 (B136) at every rung. **The same book is rule-8 reachable or not
depending on which dial you happened to walk**, at the same cost, on the same tape — a far larger
effect on "reachability" than the cost rung is.

**D4 — a stable pick is not a resolved pick.** The IS-Sharpe margin between the 10-bps pick and
its runner-up runs **0.0001 to 0.1238**, and **8 of 14** picks are decided by less than the
record's own committed seed-noise floor (877: 0.0145 of Sharpe). The GROSS ladder — the most
cost-stable pick in the run, unmoved across 200 bps on both panels — is decided by **0.0001 /
0.0003** of IS Sharpe over a whole-ladder spread of 0.0014 / 0.0034. Cost-stability of that pick
means only that gross barely moves Sharpe at all, and the record should not read it as strength.

## GATES 12 of 12, printed before any result number

G1/G1b/G1c `r(c) = g - tn*c/1e4` == `engine.backtest` at 10/25/50 bps, 1.39e-17 each (this is
what licenses the exact 201-rung ladder). G2 CROSS-RUN 936/1071/1082/1094's committed U56 W/H126
N=20 triple 3.18e-07. G3 SPY OOS triple 1.70e-04. G4 CROSS-RUN 1086/1094's committed candidate
triple **0.00e+00**. G4b CROSS-RUN 1094's committed c\* = 63 bps **0.00e+00**. G5 live RULES v2
MaxDD == committed −12.05% at 4.95e-05. G6 CAGR non-increasing in the rung at all 146 cells
(0.00e+00). G7 determinism 0.00e+00. G8 the cost axis is live (5.66 pp of CAGR spread 0 -> 50
bps). G9 the within-ladder turnover spread is live (7.42x/yr).

## RULE 8 AND BOTH KEEP PATHS

Every pick is chosen on IS 2009-2016 ALONE and its OOS 2017-2026 read ONCE, separately at each
rung. Benchmarks: **U56 SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588/0.8207), OOS 15.21% /
0.8711 / −33.72%; RULES v2 live full 8.62% / 1.2007 / −12.05%, OOS 9.45% / 1.2762 / −12.05%.
B136 SPY OOS 15.33% / 0.8767 / −33.72%; RULES v2 OOS 7.88% / 1.1059 / −12.24%.**

U56 picks (8 ladders incl. the labelled L_NH94 duplicate of L_NH): **4b full 6/8 and 4b OOS 6/8 at
0 and 10 bps, 2/8 at 25 bps, 3/8 at 50 bps. 4a 0/8 at every rung.** B136: **0/8 at 10, 25 and 50
bps** (1/8 at 0 bps, on 4b-OOS only). Whole-grid, 146 cells: 4b full **35 / 33 / 29 / 21** and 4b
OOS **39 / 36 / 30 / 27** at 0 / 10 / 25 / 50 bps; **4a 0 of 146 at every rung.**

**NOTHING IS PROPOSED, and no memo is written.** Every 4b-passing pick at PROTOCOL's 10 bps is an
object the record already holds: the U56 H-ladder / (N,H)-grid pick is 1086's PARKed N=12/H=21
candidate (16.80% / 1.1625 / −19.48%, OOS 17.57% / 1.1426 / −19.48%), and the GROSS- and
CADENCE-ladder picks are the standing top-20 family anchor (15.58% / 1.1397 / −19.13%, OOS
16.97% / 1.1643 / −19.13%, c\* = 117 bps — 1094's own figure, reproduced). The one genuinely new
observation is filed as an idea rather than a proposal: at 25 and 50 bps the CADENCE chooser moves
to **QUARTERLY** (1.65x/yr turnover) and that cell clears 4b full and OOS at both rungs (15.11% /
1.1203 / −19.94% at 25 bps; 14.64% / 1.0891 / −19.94% at 50) — but at PROTOCOL's 10 bps no
chooser selects it, so it is not rule-8 reachable at the cost the protocol actually fixes.

## SURVIVORSHIP (rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels. Every level here is optimistic, every 4b/4a count an
UPPER bound and every c\* an UPPER bound on the cost a real book of this kind could have paid. The
PICK half is a contrast between two selections over the same inflated tape and the bias very
largely cancels out of it; it does NOT cancel out of the 4b legs, which are measured against SPY,
a real index.

Script `research/backtests/2026-09-16_is-RULE-8-REACHABILITY-a-COST-RUNG-object-across-the-record-s-COMMITTED-PICKS_cloud.py`,
8 CSVs, console log, 4 LEADERBOARD rows.
