# Idea 966 (lane cloud, 2026-09-22) — is 4b PASSABILITY a PANEL fact rather than a BOOK fact?

**Question.** Idea 962 found U56 carries 9 of 12 4b-passing families, B136 3 and SMALL 0, across all five
books. If the panel decides the verdict, every published "book X clears 4b" is really "panel U56 clears
4b", and no book work on B136 or SMALL can ever reach it.

**Design.** Rectangular grid: panel {U56 56 names, B136 136, SMALL 665 tradable} x book {BAND03_G075 =
live RULES v2, BAND03_G100, V1TOP5, TOP20EW = the 2026-09-04 KEEP-4b form, **EWALL = equal-weight the
whole panel, a book with zero rule in it**} x cadence {D,W,M,Q} x phase {0..4 for W/M/Q} x cost
{0,10,25,50} bps x window {FULL,IS,OOS} = **2,898 published rows**. Tuned params, exactly 2 as the idea
specifies: DECOMPOSITION in {eta2, linear-probability-model partial R2} x PANEL SET in {U56+B136,
U56+B136+SMALL}; both settings of both reported. Rule 8: (book, cadence) on 2009-2016 IS Sharpe alone.

**Gates.** G1 phase-0 weekly mask == `engine.rebalance_mask(W)`, 0 differing rows on all three panels.
G2 the BAND03_G075 book == `baseline.rules_v2_weights`, max|d| **0.0** on all three. G3 local runner +
cost reconstruction == `engine.backtest`, max|d| **<= 3.2e-17**. G4 0 clipped quarters at d=4.
G5 tradable names 56 / 136 / 665. External: the FULL-window 10 bps panel counts come out **9 / 4 / 0**
against idea 962's published **9 / 3 / 0** on a different grid.

## A. The answer: mostly a BOOK fact — by a factor of 3 to 7

| window | panel set | eta2 panel | eta2 book | eta2 cadence | LPM R2 |
|---|---|---|---|---|---|
| FULL | U56+B136 | 0.0131 | **0.2909** | 0.0941 | 0.398 |
| OOS | U56+B136 | 0.0299 | **0.2343** | 0.0687 | 0.333 |
| FULL | +SMALL | 0.0413 | **0.1884** | 0.0609 | 0.291 |
| OOS | +SMALL | 0.0532 | **0.1524** | 0.0447 | 0.250 |

Both decompositions return the SAME numbers to four places, because the grid is balanced and the model is
additive — on a rectangular design the record's two candidate decompositions are not two readings.
Cadence outweighs the panel in three of four settings. The premise as stated is **refuted**: the book
axis carries 2.9x to 7.6x the panel axis.

## B. But the panel is an absolute GATE, and out-of-sample U56 dominates completely

Marginal 4b pass rates at 10 bps: U56 **9/80 FULL, 9/80 OOS**; B136 4/80, 2/80; SMALL **0/80, 0/80**
(1 of 240 SMALL cells passes anywhere, and it is in-sample). Asked directly — *does any book pass on a
panel U56 does not?* — **OOS: 0 of 80, on both other panels, at every one of the four cost rungs.**
FULL: 1 of 80 (V1TOP5/W3 on B136) and only at 0 bps. The only window where B136-only passes exist is
**IS** (8 of 80 at 10 bps, all BAND03_G100), and none survives into OOS.

## C. What the panel actually moves is WHICH LEG BINDS, not the pass rate

Among OOS 4b failures at 10 bps: U56 binds DD 44 / CAGR 32 / H1 14 of 71; B136 DD 63 / CAGR 42 / H1 41
of 78; SMALL **H1 79, H2 80, DD 66, CAGR 63 of 80** — on the small panel the Sharpe legs bind almost
everywhere, which is a different failure in KIND. The pure-panel control settles it: **EWALL, which
contains no rule at all, passes 0 of 16 cells on every panel in every window, and its binding leg is the
DD cap in 16 of 16, never the CAGR floor.** The panel supplies the CAGR leg for free; the DD leg is what
a book has to buy, and only one of the five books buys it (BAND03_G100: 8/16 on U56 OOS, 2/16 B136, 0
SMALL; TOP20EW 1/16 on U56 OOS only).

## D. Rule 8 (2017-2026 read once): the chooser reaches 4b on 0 of 3 panels

IS Sharpe picks **EWALL/Q on U56** — the zero-information book — OOS 18.84% / 1.1634 / -28.56% (H1 1.309
H2 1.010), 4b FAIL on the DD cap alone at 5/5 phases and 4/4 cost rungs; **TOP20EW/M on B136**, OOS
20.71% / 1.0016 / -33.68%, 4b FAIL on DD; **V1TOP5/M on SMALL**, OOS **0.71% / 0.1187 / -39.54%**
(H1 0.404, H2 -0.188), 4b FAIL on all four legs. Comparands: SPY OOS 15.29% / 0.8751 / -33.72%;
RULES v2 OOS 9.46% / 1.2767 / -12.05% (U56), 7.85% / 1.1017 / -12.24% (B136), 3.63% / 0.5447 / -14.16%
(SMALL). That an IS-Sharpe chooser prefers EWALL to every real book on U56 reproduces 2119(D)'s
"the objective cannot see the dial that decides the verdict" on a new family.

**Verdict: ANSWERED — KILL of the 'panel fact' reading (book beats panel 3-7x in both decompositions),
but KILL also of any hope of reaching 4b off U56: no book passes out-of-sample on a panel U56 does not,
at any cost rung, and SMALL is 0 of 80 in FULL and OOS alike. No KEEP candidate.**

**SURVIVORSHIP:** the SMALL panel is current constituents of a sub-$2B screen, so its levels are biased
UP; names with max_1d_move >= 1.0 were dropped first (665 tradable of 719). Every SMALL reading here is
therefore an UPPER bound, which only strengthens the 0-of-80 result.
