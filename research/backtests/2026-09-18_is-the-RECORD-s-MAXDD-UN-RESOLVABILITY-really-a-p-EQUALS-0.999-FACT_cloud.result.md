# Idea 1281 (lane cloud, 2026-09-18) — is the record's MaxDD UN-RESOLVABILITY really a p = 0.999 fact?

**ANSWERED: NO, AND THE QUEUE'S OWN NOMINATED REPLACEMENT SITS ON THE WRONG SIDE OF ITS OWN
BOUNDARY.** The crossover is at p ≈ 0.96–0.98 on the two large-cap panels, it does not exist at
all on SMALL663 (b_sd positive at every p, p = 0.90 included), and **Q_0.99's b_sd is LARGER
than MaxDD's on two of three panels** (U56 +0.0554 vs +0.0482; SMALL663 +0.1913 vs +0.1779).
Substituting Q_0.99 for MaxDD throughout moves **7 of 60 whole-4b verdicts, every one of them
pass → fail on the DD leg**, resolves the DD verdict **no better** (median |M|/SD 1.087 vs
MaxDD's 1.628), and **costs OOS Sharpe at every rung** (mean d −0.0036 to −0.0344).
**KILL (capital). No new book. No RULES change.** 7 of 7 gates, 21 s, offline, deterministic.

## Why this idea
FIRST numbered item in QUEUE.md's `## Open`. Eligible: price-only, no EDGAR / Form 4 / 8-K /
options / spin-offs / live data. No eligibility descent taken — the question is answered on REAL
books (the record's own four ladders around its anchor, 20 distinct books on each of three
panels) and the run carries a rule-8 capital arm in which every (p, cap multiple) cell supplies
an IS-only chooser and 2017–2026 is read once.

## Dials (PROTOCOL rule 4 — two, both from the queue's own wording)
DIAL 1 = quantile p ∈ {0.90, 0.95, 0.975, 0.99, 0.995, 0.999, 1.00} of the |drawdown| path;
p = 1.00 **is** |MaxDD| exactly (gate G2, 0.00e+00), so the ladder provably contains the
incumbent it is scored against. DIAL 2 = panel {U56, B135, SMALL663}. The cap multiple is
**reported, not tuned**: PROTOCOL's own 0.60 carries every headline, with 0.50 / 0.75 / 1.00 as
a published sensitivity. Books = N {5,10,15,20,30,40} · H {5,10,21,42,63,90,126,189,252} ·
G {0.50,0.60,0.75,0.85,1.00} · C {D,W,M} around the committed anchor N=20 H=126 G=0.75 C=W,
de-duplicated to 20 per panel.

## ARM 0 — the premise does not reproduce as a p = 0.999 fact
b_sd = OLS slope of log SD(Q_p) on log(tape fraction), anchor book, **disjoint** windows
(1146 lane cloud's own geometry finding, not the nested convention):

| panel | Q900 | Q950 | Q975 | Q990 | Q995 | Q999 | Q1000 (=MaxDD) |
|---|---|---|---|---|---|---|---|
| U56 | −0.0847 | −0.0024 | **+0.0403** | +0.0554 | +0.0505 | +0.0513 | +0.0482 |
| B135 | −0.1106 | −0.0396 | −0.0008 | **+0.0150** | +0.0098 | +0.0072 | +0.0122 |
| SMALL663 | **+0.2156** | +0.2130 | +0.2094 | +0.1913 | +0.1798 | +0.1806 | +0.1779 |

1146's committed figures for reference: −0.0926 at p = 0.90, +0.1654 at p = 1.00. The **sign at
p = 0.90 reproduces on both large-cap panels** — so 1146's low end is real — but the sign
**flips two to three rungs below 0.999**, not at it, and on SMALL663 it never flips at all: the
noise growth there is a property of the PANEL and not of the top 0.1% of the drawdown
distribution. The queue's framing ("the whole effect lives in the top ~0.1%") is a U56-and-B135
statement read as a record-wide one.

## ARM 1 — the re-key moves something at every rung, unlike the K-family
Share of (panel, book, window) DD cells bit-identical to the incumbent: **0.0000 at every
p < 1.00.** This is the sharp contrast with idea 1282's trailing-window family, where K63 /
K126 / K252 were 0.66 / 0.94 / 0.95 degenerate and only K21 re-keyed anything. A quantile of
the drawdown path is a genuinely different statistic at every rung. DD-leg flip share at the
protocol multiple 0.60: Q900 0.2033, Q950 0.1867, Q975 0.1733, **Q990 0.1667**, Q995 0.1533,
Q999 0.0867 — by panel U56 0.3500, B135 0.1500, **SMALL663 0.0000** at every p (no small-cap
book comes near the cap under any key, so the substitution is a large-cap-only event).

## ARM 2 — it is not better resolved. The prediction is refuted in its own direction
Paired circular block bootstrap (L = 63, B = 300, book and SPY on the **same** draws), margin
M = m·Q_p(SPY) − Q_p(book), at m = 0.60:

| | Q900 | Q950 | Q975 | Q990 | Q995 | Q999 | MaxDD |
|---|---|---|---|---|---|---|---|
| share decided inside 1 SD | 0.4833 | 0.5833 | 0.4833 | 0.4833 | 0.4500 | **0.2333** | 0.3167 |
| median \|M\|/SD | 1.0486 | 0.9250 | 1.0027 | 1.0870 | 1.1439 | **1.7050** | 1.6282 |
| median SD | 0.0270 | 0.0321 | 0.0343 | 0.0355 | 0.0357 | 0.0354 | 0.0379 |

Median SD does fall as p falls — from 0.0379 to 0.0270, a 29% reduction — which is the one leg
of "better" the quantile key wins. It buys nothing, because **the margin shrinks faster than the
noise does**: the cap 0.60·Q_p(SPY) and the book's own Q_p converge on each other as the tail is
sawn off, so |M|/SD **falls** from 1.628 to 1.087 at Q_0.99 and the share of verdicts decided
inside their own 1 SD **rises** from 0.317 to 0.483. Only Q_0.999 — a rung that barely moves
anything (flip share 0.0867) — resolves better than the incumbent. This is the opposite of the
drop-in replacement 1146's reading implied, and it is the finding worth keeping.

## ARM 3 — the verdict census the queue asked for, named
Whole 4b (all five legs; the other four held at their own values so any flip is attributable to
the key), full window, m = 0.60. Incumbent passes **10 of 60**.

| p | passes | changed | pass→fail | fail→pass |
|---|---|---|---|---|
| Q900 | 1 | 9 | 9 | 0 |
| Q950 | 3 | 7 | 7 | 0 |
| Q975 | 3 | 7 | 7 | 0 |
| **Q990** | **3** | **7** | **7** | **0** |
| Q995 | 3 | 7 | 7 | 0 |
| Q999 | 4 | 6 | 6 | 0 |

**The substitution is purely destructive at every rung: not one fail→pass anywhere on the
ladder.** Named flips at the queue's nominated p = 0.99, all on the DD leg:

| panel | book | incumbent margin | Q_0.99 margin |
|---|---|---|---|
| U56 | N=15 | +0.0009 | −0.0166 |
| U56 | **N=20 (THE COMMITTED ANCHOR)** | **+0.0110** | **−0.0085** |
| U56 | H=5 | +0.0177 | −0.0066 |
| U56 | H=10 | +0.0084 | −0.0248 |
| U56 | H=21 | +0.0004 | −0.0070 |
| B135 | N=10 | +0.0003 | −0.0260 |
| B135 | N=15 | +0.0057 | −0.0162 |

The record's own 2026-09-04 KEEP-4b anchor is among the seven. Adopting Q_0.99 would retire the
book the live rules were derived from — on a statistic that, per ARM 2, resolves that very
verdict *worse* than the one it replaces. The standing U56 gross rung **G=0.60** (full 12.59% /
1.1517 / −15.51%, halves 1.2123 / 1.1121) passes 4b under **every** p, so no capital-worthy book
in the record is *gained* by the re-key either.

## ARM 4 — capital, rule 8, OOS 2017–2026 read once. KILL
Each (panel, p, m) cell buys the highest-IS-Sharpe book passing all four IS-computable 4b legs
under that cell's key (fallback, declared in advance: highest IS Sharpe), chosen on
warm-up..2016-12-31. d(OOS Sharpe) against the MaxDD-keyed chooser over all 12 (panel, multiple)
cells:

| p | mean d | SE | picks differing |
|---|---|---|---|
| Q900 | −0.0344 | 0.0354 | 5 of 12 |
| Q950 | −0.0137 | 0.0249 | 4 of 12 |
| Q975 | −0.0194 | 0.0238 | 3 of 12 |
| **Q990** | **−0.0260** | **0.0222** | 2 of 12 |
| Q995 | −0.0152 | 0.0257 | 3 of 12 |
| Q999 | −0.0036 | 0.0036 | 1 of 12 |

**Negative at all six rungs, monotone-ish in how much the key actually moves.** No rung is
individually significant (every |mean| < 1.2 SE), which is itself the point: the substitution
buys nothing measurable and loses on every reading. **0 of 84 chooser rows pass 4a**; 33 of 84
pass 4b **on their own key**, which per 1282's finding is an inflation artefact of re-keying
without re-deriving the multiple, not 33 new books. Published books: 4a **0 of 60**, 4b **10 of
60** on the incumbent key.

Best quantile-keyed chooser, U56 p = 0.995 at m = 0.60 → **G = 0.60**:
full **12.59% / 1.1517 / −15.51%**, halves 1.2123 / 1.1121; OOS **13.78% / 1.1826 / −15.51%** —
against SPY OOS 15.28% / 0.8747 / −33.72%, live RULES v2 OOS 1.2781, anchor OOS 1.1832.
4a **FAIL** (H1, H2, DD). 4b **PASS**. This is **not a new book**: it is the same standing U56
gross rung idea 1282 published yesterday, reached here by a different key. Nothing is proposed.

## Schema line offered to the record (not adopted; rule 6 reserves that for a Sunday review)
*A "the effect lives in the top q of the distribution" claim is a claim about a PANEL until it
is read on more than one. 1146's p = 0.999 boundary reproduces in SIGN at its low end on U56 and
B135, sits two to three rungs lower than stated on both, and does not exist on SMALL663, where
b_sd is positive at every quantile including 0.90. Any committed quantile boundary should name
the panels it was measured on and the panels it was not.*

## Gates, all 7 passing
G1 fast runner == `engine.backtest` at the anchor, **2.08e-17** (the engine-facing frame is
rolled back one row because `build()` bakes the t+1 lag into its own rows). G2 Q_1.00 == |MaxDD|
exactly, **0.00e+00**, on all 60 books — the ladder provably contains the statistic it is
compared against. G3 Q_p non-decreasing in p, **0** violations on all 60 books. G4 the incumbent
cell reproduces PROTOCOL 4b's DD leg as written (`MaxDD(book) >= 0.60·MaxDD(SPY)`, both
negative), **0** disagreements on all 60. G5 bootstrap SD stable across rng streams, median
relative move **0.0934**. G6 every chooser decided on IS rows only (structural: `legs_4b_is`
has no OOS field). G7 SPY never a constituent (asserted in `Panel.__init__`).

## Survivorship (rule 9)
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen with the house
`max_1d_move >= 1.0` filter applied FIRST (52 of 715 names dropped). The headline is a CONTRAST
between two keys read on identical windows of one tape — which books a cap admits, how well each
cap resolves its own verdict — and is first-order immune to a bias that moves every book's
drawdown together. A current-constituent panel UNDERSTATES deep drawdowns specifically, which is
exactly the tail this run truncates, so the contrast is **conservative for the quantile key and
optimistic for MaxDD** — i.e. the true case against the substitution is at least this strong.
The absolute OOS triples in ARM 4 are NOT immune and are upper bounds; they are quoted against
SPY and RULES v2 on the same panel.

Script: `research/backtests/2026-09-18_is-the-RECORD-s-MAXDD-UN-RESOLVABILITY-really-a-p-EQUALS-0.999-FACT_cloud.py`
