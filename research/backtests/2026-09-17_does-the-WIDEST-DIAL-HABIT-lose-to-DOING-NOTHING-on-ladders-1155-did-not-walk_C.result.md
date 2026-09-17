# Idea 1206 (lane C, 2026-09-17) — does the WIDEST-DIAL HABIT lose to DOING NOTHING?

**ANSWERED = (B) A THREE-DRAW ACCIDENT. The do-nothing advantage does not survive dozens of
picks, and 3 of its 4 signs FLIP. Nor does the habit beat doing nothing: the whole ordering is
unresolved, max |t| = 0.30 over 472 picks per rule. KILL as a capital finding.**

## What was asked

Idea 1155's Arm C found the do-nothing control `C_ANCHOR` ahead of all four matching rules out
of sample — mean OOS Sharpe **0.8934** vs M_D2 0.8865 / M_NONE 0.8672 / M_SUBSAMPLE =
M_PAIRWISE 0.8198 — and read it as "the record's *tune the widest dial* habit loses to doing
nothing". That comparison rested on **three picks per rule** (3 panels x 1 anchor x 1 split).
This run rolls the IS window and walks four anchors so each rule makes **472 picks**.

## Dials (rule 4, max 2; the queue names both)

| dial | rungs |
|---|---|
| WINDOW (rolling IS length) | 2y, 3y, 4y |
| ANCHOR | A_REC (20/126/0.75/W, 1155's), A_TIGHT (10/63/0.55/W), A_SLOW (30/252/0.75/M), A_FAST (5/21/0.50/W) |

Not dials, reported at every value: PANEL {U56, B136, SMALL} (rule 9); 1155's four ladders
{N 6 rungs, H 4, GROSS 10, CADENCE 2} and four matching rules, inherited unchanged; three
controls `C_ANCHOR` (never move), `C_RANDOM` (uniform ladder, then its IS argmax) and
`C_BEST_IS` (global IS argmax). Folds = one calendar year of OOS, stepped one year, 2013-2026,
non-overlapping and tiling the span exactly (G5). 10 bps, t+1 execution, 260-row warm-up.

## The arithmetic, printed before any data was touched

A 3-draw mean has SE `s/sqrt(3)`. To resolve 1155's largest gap (0.0736) at 2 SE the per-pick
SD must be below **0.0637**; its smallest (0.0069) needs **0.0060**. Real book OOS Sharpes on
this tape have a per-pick SD of order 0.3. **1155's ordering was arithmetically unresolvable
before the data was looked at.**

## Result

1155's Arm C **reproduces bit-for-bit** — all five rules within **3.5e-05** of the committed
figures (G4). The rolling walk then says:

| rule | mean OOS Sharpe (472 picks) | delta vs C_ANCHOR | clustered SE | t | 1155's gap |
|---|---|---|---|---|---|
| M_NONE | 0.9895 | **+0.0017** | 0.0526 | 0.03 | +0.0262 |
| M_SUBSAMPLE | 1.0046 | **-0.0135** | 0.0463 | -0.29 | +0.0736 |
| M_PAIRWISE | 1.0046 | **-0.0135** | 0.0463 | -0.29 | +0.0736 |
| M_D2 | 1.0054 | **-0.0143** | 0.0479 | -0.30 | +0.0069 |
| C_ANCHOR | 0.9911 | 0 | — | — | — |
| C_RANDOM | 0.9718 | +0.0193 | 0.0281 | 0.69 | not run by 1155 |
| C_BEST_IS | 0.9803 | +0.0109 | 0.0615 | 0.18 | not run by 1155 |

SEs are clustered by fold (folds tile the tape without overlap, so fold means are the
independent units; panels and anchors inside a fold are not). **No delta clears 2 SE, and the
largest |t| in the table is 0.30.** Outcome (B).

**Sign stability.** C_ANCHOR is ahead at 8 / 6 / 6 / 5 of the 12 (window, anchor) cells against
M_NONE / M_SUBSAMPLE / M_PAIRWISE / M_D2, at 2 of 3 panels, and at 6 / 5 / 5 / 5 of 14 folds —
i.e. at or below a coin flip on three of the four. **C_ANCHOR is top of the seven rules at only
3 of 12 grid points, median rank 3.5**, against top-of-five in 1155's single reading.

**The comparison has content (not outcome D).** Move rates 0.7267-0.9915 for every chooser;
0.0000 for C_ANCHOR by construction (G6). Restricted to picks that moved, the deltas are
+0.0019 / -0.0174 / -0.0174 / -0.0184 at |t| <= 0.30 — the same answer with the zero-deltas
dropped.

**The panel split is the largest real effect in the run and it is not the one 1155 published.**
C_ANCHOR wins on the two large-cap panels (U56 1.2165 vs 1.1689-1.1823; B136 1.1708 vs
1.1270-1.1475) and **loses badly on SMALL (0.5298 vs 0.6718-0.6783)**. Doing nothing is a
large-cap fact; on the small-cap panel the widest-dial habit is worth +0.15 of OOS Sharpe.

**GROSS is called widest at 0 of 1,888 matching-rule picks** — 1189's gross-rung degeneracy,
confirmed from a fifth direction and without looking for it. The habit lands on H (0.43-0.48)
and N (0.25-0.46), with CADENCE taking 0.31 under the count-matched rules and only 0.06 under
M_NONE — the count-inflation 1155 measured, showing up as a change of which dial gets tuned.

## Rule 8 and both KEEP paths

Dials chosen on folds ending 2016 or earlier, 2017-2026 folds read once. Naively this looks
decisive — C_ANCHOR picks (2y, A_SLOW) and gets OOS mean fold Sharpe **1.0562 / 13.51% CAGR /
-12.84% DD** against the matching rules' 0.7376-0.8325 at their own IS-chosen (3y, A_FAST).
**That gap is a dial confound, not a chooser effect: the two cells are different books.** Read
at MATCHED cells over all 12 of them the means collapse to **M_NONE +0.0272, M_SUBSAMPLE
-0.0012, M_PAIRWISE -0.0012, M_D2 +0.0013**, with a per-cell range of **-0.2223 to +0.1689** —
cell-to-cell noise roughly ten times the effect. Stitched over 2017-2026 at each rule's own
cell: C_ANCHOR 12.83% / 0.8773 / -25.42%, M_SUBSAMPLE 10.61% / 0.7665 / -20.06%, M_NONE 9.19% /
0.7234 / -23.01%, C_BEST_IS 12.79% / 0.7650 / -31.15%, against SPY OOS Sharpe 0.8741 and the
live RULES v2 book's 1.0099.

**Books (228 = 3 panels x 76):** 4a **1 of 228**; 4b full 45; 4b OOS 50; **BOTH 43**, of which
U56 29 books sit on 16 distinct (N, H, cadence) cells and B136 14 on 8 — the rest are one book
at a different gross rung. SMALL 0 on every path.

**Stitched chooser curves (252):** 4a **0 of 252**; 4b full 22; 4b OOS 42; **BOTH 21**, every
one on U56 or B136, nine of them the do-nothing control. Best: U56 / A_REC / 2y / M_SUBSAMPLE
16.85% / 1.1651 / -19.99%, halves 1.190/1.164, OOS 17.75% / 1.1715 — against C_ANCHOR at the
same cell 15.90% / 1.1523 / -19.47%, OOS 16.13% / 1.1042, and SPY 14.88% / 0.9116 / -33.72%.
**RECORDED, NOT PROMOTED, NO MEMO:** 4a is 0 of 252, the 21 are survivors of 252 readings over a
12-cell dial grid x 7 rules x 3 panels, the best beats the do-nothing anchor at one cell while
the paired grid-wide delta is within noise of zero, and the deployable object underneath is the
anchor book itself (U56 N=20 / H=126 / g=0.75 / W), which is the record's standing lineage. The
chooser adds nothing to it.

## Gates — 10 of 10

G1 fast runner == `engine.backtest` on the record's anchor **2.78e-17** (carrying 1155's own
decision-time correction, `Wdec[t] = W[t+1]`); G2 the gross ladder is provably the selection
frame scaled, **0**; G3 live RULES v2 U56 MaxDD -12.0549% vs the record's -12.05%; **G4 1155's
Arm C reproduces at 3.48e-05 on all five rules**; G5 folds tile the span with no overlap and no
gap; G6 C_ANCHOR move rate exactly 0; G7 paired design balanced (identical pick count per rule);
G8 stitched length == sum of its folds; G9 the IS window ends strictly before its fold's first
bar; G10 on a 2-rung ladder M_NONE == M_SUBSAMPLE == M_PAIRWISE, by identity.

## Survivorship (rule 9)

U56 and B136 are current-constituent lists; SMALL is the current output of a sub-$2B screen less
the documented `max_1d_move >= 1.0` exclusion. Every CAGR and drawdown LEVEL is optimistic and
the 4b counts are an UPPER bound. The chooser comparison is one construction against itself on
one tape and the bias very largely cancels out of the DELTAS; it does not cancel out of the
levels.

## Proposed, not enacted (rule 6)

**A chooser comparison may not be published without its pick count, and a published mean over
fewer picks than its own per-pick SD can resolve should carry that SD.** On 1155's Arm C the
whole five-way ordering spans 0.0736 on three draws of a statistic whose per-draw SD is ~0.3.

## Follow-ups filed

1208 (is the SMALL-panel reversal of the do-nothing advantage a panel fact or a turnover fact),
1209 (does the count-matched rules' shift of the widest dial from N to CADENCE change any
committed verdict), 1210 (how many committed chooser comparisons in the record rest on fewer
than ten picks).

Script `research/backtests/2026-09-17_does-the-WIDEST-DIAL-HABIT-lose-to-DOING-NOTHING-on-ladders-1155-did-not-walk_C.py`,
10 CSVs, console log. **KILL.**
