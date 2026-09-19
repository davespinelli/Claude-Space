# Idea 1444 (lane C, 2026-09-19) — does a CAGR-NEUTRAL BETA BAND exist at all?

**ANSWERED: NO on the panel that carries the book. KILL (capital), NO NEW BOOK. The beta family
is now closed on the RETURN leg as well as the drawdown leg.**

Script `2026-09-19_cagr-neutral-beta-band_C.py`, 90 cells (3 panels x 5 c x 6 H), all published
in `.grid.csv`. All 20 gates pass. 10 bps, t+1, weekly, no leverage, no shorting.

## The question and the answer

1429's beta-keyed floor-and-cap band widens the incumbent's binding 4b drawdown margin but pays
in CAGR at every cell. This run asked whether that exchange rate is a CONSTANT or a CHOICE, by
sweeping the band half-width `c` against the one incumbent dial that cuts turnover, the min-hold
`H`. The beta lookback is FROZEN at 126 days, so there are exactly two tuned parameters.

**U56 frontier: 0 of 24 biting cells.** Every biting cell costs CAGR against the frozen
incumbent (-0.824 .. -4.753 pp), and no cell is both CAGR-neutral and wider on the DD margin
than the anchor's own +1.1028 pp. The 8 cells that DO widen the margin cost -0.837 .. -4.753 pp
of CAGR; the 2 cells that ARE neutral under the paired convention both have a NEGATIVE margin
(-0.951, -0.746 pp).

## Three findings, in order of what they cost

**1. The frontier's existence is a question about the SE convention, and the loose one is wrong.**
The idea's literal wording — "within its own bootstrap SE" — reads as the anchor's MARGINAL
CAGR SE, which on U56 is 2.8609 pp. Under that convention the frontier is NON-EMPTY: 3 cells
(c = 0.25/0.50/0.75 at H = 126). But cell and anchor hold the same names on the same days and
share almost all their variance, so the marginal SE is the wrong ruler: the PAIRED block-
bootstrap SE of the same difference is 0.3133 .. 1.8983 pp — up to **9.1x smaller** on U56,
10.8x on B136, 11.6x on SMALL. Under the paired SE the U56 frontier is EMPTY. A neutrality
claim scored against a marginal SE is roughly an order of magnitude too easy to pass.

**2. The exchange rate IS a choice — and the incumbent is already standing on the best rung.**
The DD-per-CAGR slope is not constant across H: U56 reads -0.462 / -0.391 / **-0.901** / -0.755
/ -0.608 / -0.810 pp of drawdown per pp of CAGR at H = 21 / 63 / 126 / 189 / 252 / 378, and B136
peaks at H = 126 too (-1.047). **The steepest rung on both large-cap panels is H = 126, the
incumbent's own value.** So the queue's premise was right that the rate is a choice, and the
choice has already been made optimally; H buys no improvement in the terms of trade.

**3. The de-gross wins again — the sixth consecutive run.** Scaling THIS H's own anchor to the
cell's exact CAGR (so gross AND H are both shut, leaving only the band) draws down **less at
24 of 24 U56 biting cells** (dDD -0.005 .. -3.722 pp, |t| > 2 at 0 of 24) while deploying ~11%
less capital. Against the FROZEN anchor's de-gross, the cell is shallower at 4 of 45 attainable
cells. Whatever the band buys, a scalar buys it cheaper.

## Capital

4a **0 of 90**. 4b full 20 of 90, 4b OOS 20 of 90, both 20 (U56 16, B136 4, SMALL 0) — but the
frozen incumbent is already one of them and none of the other 19 improves on it out of sample.

RULE 8, two pre-registered choosers, 2017-2026 read ONCE:

| panel | chooser | IS pick (c,H) | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | SHARPE | (0.50, 378) | 14.00% | 1.0455 | -20.30% | no |
| U56 | FRONTIER | (1.00, 378) | 12.45% | 1.0188 | -18.93% | yes |
| B136 | SHARPE | (1.00, 378) | 13.23% | 0.8955 | -22.79% | no |
| B136 | FRONTIER | (1.00, 378) | 13.23% | 0.8955 | -22.79% | no |
| SMALL | SHARPE | (1.00, 252) | 11.05% | 0.7204 | -31.49% | no |
| SMALL | FRONTIER | (1.00, 21) | 10.73% | 0.6649 | -37.97% | no |

Frozen incumbent OOS on U56: **17.32% / 1.1857 / -19.13%**. SPY OOS: 15.26% / 0.8738 / -33.72%.
Both choosers LOSE to the frozen incumbent on OOS Sharpe (-0.140 and -0.167, t -1.01 and -1.04)
and on OOS CAGR (-3.3 and -4.9 pp) on U56. The FRONTIER chooser's pick is the only one that
clears 4b OOS, and it clears it by giving up 4.9 pp of OOS CAGR to buy 0.19 pp of drawdown that
is indistinguishable from zero (t +0.08). The choosers agree on 1 of 3 panels.

## Two honest caveats, stated rather than glossed

**The band is not always a CAGR cost.** On SMALL it RAISES CAGR above its own H-anchor at all 24
biting cells, which is why SMALL's frontier reads 16 of 24 non-empty — and why no de-gross twin
exists there at all (de-grossing can only lower return; PROTOCOL rule 2 forbids f > 1). This is
NOT a capital finding: SMALL's anchor misses the 4b DD cap by 16.28 pp, so every SMALL cell is
outside the cap before the band is applied. It is a real asymmetry of the rule across panels and
is published as one, not converted into a headline.

**Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010. Every absolute level is an upper bound and every 4b pass an
optimistic one. What this run reads is a CONTRAST between books over the same names on the same
days, which the bias cannot manufacture.

## Verdict

**KILL (capital). No new book, no rules change.** The DD/CAGR exchange is a fact about the book,
not a dial: no CAGR-neutral band exists on U56 under the correct (paired) SE, the exchange rate's
best rung is the one the incumbent already occupies, and a plain de-gross dominates the band on
drawdown at every U56 cell at matched return. Together with 1436 (the band is a beta-matched
exposure dial, KILL) **the beta band family is closed.**
