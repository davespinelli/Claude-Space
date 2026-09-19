# Idea 1440 (lane cloud, 2026-09-19) — ANSWERED / KILL of the chooser swap

**The question.** 1429's beta-keyed band passes 4b full AND OOS at 16 of 16 biting U56 cells and
widens the binding DD leg fourfold, yet rule 8's argmax-IS-Sharpe chooser picked c = 0 (the frozen
anchor) on U56 and B136. The queue's hypothesis: *the chooser, not the book, is what declined it.*
Re-ran 1429's own 60 cells (3 panels x c {0,0.25,0.50,0.75,1.00} x B {20,63,126,252}) under two
choosers reading the identical IS window (warm-up..2016-12-31), 2017-2026 read ONCE.

**Answer: the two choosers disagree on 1 of 3 panels, and the disagreement resolves at neither leg.**

| panel | A = argmax IS Sharpe | B = argmax IS DD margin \| IS CAGR floor | OOS gap B − A |
|---|---|---|---|
| U56 | (c 0.00, B 20) → OOS 17.32% / 1.1857 / −19.13%, 4b OOS **pass** | (c 1.00, B 126) → OOS 13.67% / 1.1768 / −15.83%, 4b OOS **pass** | CAGR **−3.6525 pp**, Sharpe **−0.0089 (t −0.08)**, MaxDD **+3.3011 pp (t +1.63)** |
| B136 | (0.00, 20) → 16.19% / 1.0180 / −20.74%, 4b OOS fail (DD leg) | **same cell** | 0 |
| SMALL | (1.00, 126) → 10.21% / 0.6385 / −31.38%, 4b OOS fail (all four legs) | **same cell** | 0 |

Comparands, OOS 2017-2026: SPY 15.26% / 0.8738 / −33.72%; live RULES v2 @10 bps 9.46% / 1.2769 /
−12.05% (U56 tape); frozen anchor 17.32% / 1.1857 / −19.13%.

**Three things kill the swap.**
1. **It changes no verdict.** 4b OOS passes on 1 of 3 panels under *either* chooser, on the same
   panel, and both U56 picks pass. The chooser was never what declined the band on B136 — there
   the DD-margin argmax *is* the anchor (its IS DD margin −1.4033 pp is the grid maximum), so B
   picks c = 0 for exactly the reason A does.
2. **Where it does disagree it is a pure CAGR-for-DD trade at zero resolved Sharpe.** B buys
   +3.3011 pp of OOS drawdown (|t| 1.63) for −3.6525 pp of OOS CAGR, moving OOS Sharpe by −0.0089
   (|t| 0.08). It swaps 4b margin between legs: OOS DD margin +1.103 → +4.404 pp, OOS CAGR margin
   +6.643 → +2.991 pp. Neither leg's move survives a paired 63-day block bootstrap at |t| > 2.
3. **Neither chooser is stable inside its own IS window.** Re-run on the two halves of the IS
   window alone (no OOS row read), chooser A picks the same cell in both halves on **0 of 3**
   panels and chooser B on **0 of 3** — A picks (0.25,20)/(0.00,20) on U56, (1.00,126)/(0.00,20)
   on B136, (1.00,20)/(1.00,126) on SMALL; B picks (0.25,126)/(1.00,126), (0.00,20)/(1.00,126),
   (1.00,252)/(0.00,20). Each chooser's own sampling noise is larger than the gap between them, so
   the U56 disagreement is a draw, not a finding.

**The CAGR floor is decoration.** It is feasible at 20 of 20 cells on every panel, so B ≡ B'
(unconstrained) everywhere: the constraint never binds and buys the chooser nothing.

**Not a KEEP.** 4a fails at 0 of 60. 4b passes FULL and OOS at 34 of 60 cells — that is 1429's
already-PARKed band re-confirmed, not a new book, and B's U56 pick is indistinguishable from the
frozen incumbent it would replace (OOS Sharpe −0.0089, t −0.08). Nothing here licenses a rules
change.

**Survivorship (rule 9).** U56/B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010 (tickers with max_1d_move ≥ 1.0 dropped per data/small_meta.csv), so
every absolute level is an upper bound and every 4b pass optimistic. The *contrast* between two
choosers over the same 60 books on the same days is what this run reads, and the bias cannot
manufacture that — but it cannot rescue the level either.

Script `2026-09-19_dd-margin-keyed-rule8-chooser_cloud.py`; 60 cells in `.grid.csv`, picks in
`.choosers.csv`, the disagreement in `.disagreement.csv`, 12 gates all passing in `.gates.csv`.
